#!/usr/bin/env python3
"""Pack/install only this reviewed original fixture; no downloads or arbitrary inputs."""
import argparse
import base64
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'switchboard-registry-demo'
VERSION = '0.4.0'
FILENAME = f'{NAME}-{VERSION}.tgz'
FILES = ('core.cjs', 'index.cjs', 'index.mjs', 'package.json')
MODES = ('import-only', 'require-only', 'import-first', 'require-first')
SPLIT_CHECKS = {
    'first_write_visible_to_second', 'second_write_visible_to_first',
    'replacement_visible_to_first', 'names_agree',
}


def digest(data, algorithm='sha256'):
    return hashlib.new(algorithm, data).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def source_bytes(candidate):
    result = {}
    for name in FILES:
        path = ROOT / 'fixtures' / 'source' / name
        if candidate == 'corrected' and name == 'index.mjs':
            path = ROOT / 'fixtures' / 'repair' / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 4096:
            raise ValueError(f'Unexpected fixture input: {path.name}')
        result[name] = path.read_bytes()
    metadata = json.loads(result['package.json'])
    assert metadata['name'] == NAME and metadata['version'] == VERSION
    assert metadata['private'] is True
    assert metadata['exports'] == {'.': {'import': './index.mjs', 'require': './index.cjs'}}
    assert metadata['files'] == ['core.cjs', 'index.cjs', 'index.mjs']
    for key in ('scripts', 'dependencies', 'devDependencies', 'optionalDependencies',
                'peerDependencies', 'bundleDependencies', 'bundledDependencies', 'workspaces'):
        assert key not in metadata, f'Unexpected executable/dependency declaration: {key}'
    return result


def inspect_archive(path, expected):
    raw = path.read_bytes()
    assert 0 < len(raw) <= 65536, 'Unexpected archive size'
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
        expanded = stream.read(131073)
    assert len(expanded) <= 131072, 'Expanded archive exceeds fixture limit'
    ledger = []
    with tarfile.open(fileobj=io.BytesIO(expanded), mode='r:') as archive:
        members = archive.getmembers()
        assert len(members) == len(FILES), 'Unexpected member count'
        assert {m.name for m in members} == {f'package/{f}' for f in FILES}
        for member in members:
            assert member.type == tarfile.REGTYPE and not member.issparse()
            assert not member.linkname and not member.pax_headers
            assert 0 < member.size <= 4096
            assert member.mode & 0o111 == 0, 'Unexpected executable member'
            data = archive.extractfile(member).read()
            assert data == expected[member.name.removeprefix('package/')], 'Member differs from reviewed fixture'
            ledger.append({'member': member.name, 'size': len(data), 'sha256': digest(data)})
    return {'size': len(raw), 'sha256': digest(raw), 'members': sorted(ledger, key=lambda row: row['member'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--verify-bundled', action='store_true')
    args = parser.parse_args()
    output = args.output.expanduser().absolute()
    # Refuse clobbering and all output nested in the distributed inputs.
    if output.exists() or output.is_symlink():
        raise FileExistsError('Output already exists; choose a new directory')
    if output.resolve().is_relative_to(ROOT):
        raise ValueError('Output must be outside this companion directory')
    node = shutil.which('node')
    npm = shutil.which('npm')
    if not node or not npm:
        raise RuntimeError('Existing Node.js and npm are required; no install fallback')
    expected = {candidate: source_bytes(candidate) for candidate in ('rejected', 'corrected')}
    source_before = {candidate: {name: digest(data) for name, data in files.items()}
                     for candidate, files in expected.items()}
    output.mkdir(parents=True)
    work = output / 'work'
    work.mkdir()
    for filename in ('empty-user.npmrc', 'empty-global.npmrc'):
        (work / filename).write_text('', encoding='utf-8')
    # Do not read or alter user/global config, credentials or network settings.
    # Only these two inherited-independent variables are passed to subprocesses.
    env = {'PATH': os.environ.get('PATH', os.defpath), 'LANG': 'C.UTF-8'}
    commands = []

    def portable(text):
        return text.replace(str(output), '.').replace(str(ROOT), '<companion>')

    def run(argv, cwd, expected_exit=0):
        result = subprocess.run(argv, cwd=cwd, env=env, text=True,
                                capture_output=True, timeout=60, check=False)
        record = {
            'argv': [('node' if item == node else 'npm' if item == npm else portable(item)) for item in argv],
            'cwd_relative_to_output': str(cwd.relative_to(output)) or '.',
            'exit': result.returncode, 'expected_exit': expected_exit,
            'stdout': portable(result.stdout), 'stderr': portable(result.stderr),
        }
        commands.append(record)
        save(output / 'evidence' / 'commands.json', commands)
        if result.returncode != expected_exit:
            raise RuntimeError(f'Unexpected exit from {Path(argv[0]).name}: {result.returncode}; see commands.json')
        return result.stdout

    runtime = {
        'node': run([node, '--version'], output).strip(),
        'npm': run([npm, '--version', '--userconfig', 'work/empty-user.npmrc',
                    '--globalconfig', 'work/empty-global.npmrc', '--cache', 'work/version-cache',
                    '--offline', '--ignore-scripts', '--no-audit', '--no-fund',
                    '--update-notifier=false'], output).strip(),
        'python': platform.python_version(),
        'platform': sys.platform, 'architecture': platform.machine(),
        'environment': {'inherited_names': ['PATH'], 'literal': {'LANG': 'C.UTF-8'},
                        'all_other_variables_omitted': True},
    }
    assert runtime['node'].startswith('v24.'), 'This bounded example requires Node 24'
    assert runtime['npm'].split('.')[0] == '11', 'This bounded example requires npm 11'

    def npm_options(cwd, cache):
        rel = lambda path: os.path.relpath(path, cwd)
        return ['--offline', '--ignore-scripts', '--no-audit', '--no-fund',
                '--workspaces=false', '--update-notifier=false',
                '--userconfig', rel(work / 'empty-user.npmrc'),
                '--globalconfig', rel(work / 'empty-global.npmrc'),
                '--cache', rel(cache)]

    manifest = {'package': {'name': NAME, 'version': VERSION}, 'runtime': runtime,
                'route': 'offline npm install of inspected local tarballs',
                'mode': 'verify-bundled' if args.verify_bundled else 'pack-copies',
                'candidates': {}}
    bundled = json.loads((ROOT / 'evidence' / 'manifest.json').read_text()) if args.verify_bundled else None
    for candidate in ('rejected', 'corrected'):
        artifact_dir = output / 'artifacts' / candidate
        artifact_dir.mkdir(parents=True)
        artifact = artifact_dir / FILENAME
        if bundled:
            original = ROOT / 'artifacts' / candidate / FILENAME
            original_bytes = original.read_bytes()
            assert digest(original_bytes) == bundled['candidates'][candidate]['sha256']
            artifact.write_bytes(original_bytes)
        else:
            source = work / f'{candidate}-source'
            source.mkdir()
            for filename, data in expected[candidate].items():
                (source / filename).write_bytes(data)
            pack_stdout = run([npm, 'pack', '.', '--json', '--pack-destination',
                               os.path.relpath(artifact_dir, source),
                               *npm_options(source, work / f'{candidate}-pack-cache')], source)
            pack_record = json.loads(pack_stdout)
            assert len(pack_record) == 1 and pack_record[0]['filename'] == FILENAME
            save(output / 'evidence' / f'{candidate}-pack.json', pack_record)

        # Inspect every selected member before allowing npm to unpack any bytes.
        ledger = inspect_archive(artifact, expected[candidate])
        ledger['artifact'] = artifact.relative_to(output).as_posix()
        save(output / 'evidence' / f'{candidate}-contents.json', ledger)
        consumer = work / f'{candidate}-consumer'
        consumer.mkdir()
        (consumer / 'package.json').write_text(json.dumps({
            'name': f'consumer-{candidate}', 'version': '1.0.0', 'private': True,
        }) + '\n', encoding='utf-8')
        shutil.copyfile(ROOT / 'scripts' / 'consumer.mjs', consumer / 'consumer.mjs')
        absent = json.loads(run([node, '--no-global-search-paths', 'consumer.mjs', 'absent'], consumer))
        before_install_digest = digest(artifact.read_bytes())
        assert before_install_digest == ledger['sha256']
        run([npm, 'install', os.path.relpath(artifact, consumer), '--save-exact',
             *npm_options(consumer, work / f'{candidate}-install-cache')], consumer)
        lock = json.loads((consumer / 'package-lock.json').read_text())
        lock_entry = lock['packages'][f'node_modules/{NAME}']
        integrity = 'sha512-' + base64.b64encode(hashlib.sha512(artifact.read_bytes()).digest()).decode()
        assert lock_entry['integrity'] == integrity and lock_entry['version'] == VERSION
        assert lock_entry['resolved'] == 'file:' + os.path.relpath(artifact, consumer)
        assert not lock_entry.get('link', False)
        installed_root = consumer / 'node_modules' / NAME
        assert not installed_root.is_symlink() and installed_root.resolve() == installed_root
        assert sorted(path.name for path in installed_root.iterdir()) == sorted(FILES)
        installed = []
        for filename, data in expected[candidate].items():
            path = installed_root / filename
            assert path.is_file() and not path.is_symlink() and path.read_bytes() == data
            installed.append({'path_relative_to_consumer': path.relative_to(consumer).as_posix(),
                              'sha256': digest(path.read_bytes()), 'size': path.stat().st_size})
        observations = {}
        for mode in MODES:
            should_fail = candidate == 'rejected' and mode.endswith('first')
            raw = run([node, '--no-global-search-paths', 'consumer.mjs', mode],
                      consumer, expected_exit=1 if should_fail else 0)
            observed = json.loads(raw)
            failed = {key for key, passed in observed['checks'].items() if not passed}
            assert failed == (SPLIT_CHECKS if should_fail else set()), 'Unexpected failure signature'
            assert observed['contract_pass'] is (not should_fail)
            observations[mode] = observed
        assert digest(artifact.read_bytes()) == before_install_digest
        readback = {'consumer_relative_to_output': consumer.relative_to(output).as_posix(),
                    'absent_before_install': absent, 'artifact_sha256': before_install_digest,
                    'npm_lock_entry': lock_entry, 'installed_files': installed,
                    'observations': observations}
        save(output / 'evidence' / f'{candidate}-readback.json', readback)
        manifest['candidates'][candidate] = {
            'artifact': ledger['artifact'], 'size': ledger['size'], 'sha256': ledger['sha256'],
            'archive_members': len(ledger['members']), 'installation': 'pass',
            'standalone_modes': 'pass', 'mixed_modes': 'fail' if candidate == 'rejected' else 'pass',
        }
    source_after = {candidate: {name: digest(data) for name, data in source_bytes(candidate).items()}
                    for candidate in expected}
    assert source_before == source_after
    manifest['source_preservation'] = {'unchanged': True, 'sha256': source_after}
    manifest['result'] = 'expected rejected failures and corrected contract passes observed'
    save(output / 'evidence' / 'manifest.json', manifest)
    print(json.dumps(manifest['candidates'], indent=2))


if __name__ == '__main__':
    main()
