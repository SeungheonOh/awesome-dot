"""Reproduce locally with already-installed tools. Never installs or accesses the network."""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from prepare import load_source, make_plan
from check import check, digest
from test_controls import controls


def run(command, log):
    result = subprocess.run([str(x) for x in command], capture_output=True, text=True, timeout=120)
    log.write(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {command[0]}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True, help='New output directory')
    parser.add_argument('--node-modules', type=Path, required=True, help='Existing node_modules containing @oai/artifact-tool')
    parser.add_argument('--node', default='node')
    parser.add_argument('--work-dir', type=Path, help='Optional parent for disposable working files')
    args = parser.parse_args()
    base = Path(__file__).resolve().parents[1]
    source = base/'fixture/source.json'
    raw, data = load_source(source)
    before = digest(source)
    plan = make_plan(source.name, raw, data)
    package = args.node_modules.resolve()/'@oai/artifact-tool/package.json'
    if not package.is_file(): raise SystemExit('Required installed authoring library is unavailable')
    for tool in [args.node, 'soffice', 'pdftoppm']:
        if not shutil.which(tool): raise SystemExit('Required installed tool is unavailable: '+tool)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix='nested-export-', dir=args.work_dir) as directory:
        temp = Path(directory)
        (temp/'node_modules').symlink_to(args.node_modules.resolve(), target_is_directory=True)
        shutil.copyfile(base/'scripts/build.mjs', temp/'build.mjs')
        (temp/'plan.json').write_text(json.dumps(plan), encoding='utf-8')
        native = temp/'native'
        native.mkdir()
        with (output/'run.log').open('w', encoding='utf-8') as log:
            run([args.node, temp/'build.mjs', temp/'plan.json', output/'nested-export.xlsx'], log)
            authored = check(source, output/'nested-export.xlsx')
            profile = '-env:UserInstallation='+(temp/'lo-profile').as_uri()
            run(['soffice', profile, '--headless', '--convert-to', 'xlsx', '--outdir', native, output/'nested-export.xlsx'], log)
            consumed = check(source, native/'nested-export.xlsx')
            tests = controls(source, output/'nested-export.xlsx', temp)
            run(['soffice', profile, '--headless', '--convert-to',
                 'pdf:calc_pdf_Export:{"SinglePageSheets":{"type":"boolean","value":"true"}}',
                 '--outdir', native, native/'nested-export.xlsx'], log)
            previews = output/'previews'
            previews.mkdir()
            run(['pdftoppm', '-png', '-r', '100', native/'nested-export.pdf', previews/'sheet'], log)
            for i, name in enumerate(['collections', 'items', 'labels', 'source-paths', 'read-me'], 1):
                (previews/f'sheet-{i}.png').rename(previews/f'{name}.png')
            versions = {'python': sys.version.split()[0], 'artifact_tool': json.loads(package.read_text())['version']}
            for executable, key in [(args.node, 'node'), ('soffice', 'libreoffice')]:
                versions[key] = subprocess.check_output([executable, '--version'], text=True).strip()
        for name, value in [('reconciliation.json', authored), ('native-readback.json', consumed), ('controls.json', tests), ('versions.json', versions)]:
            (output/name).write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')
        # The author may emit a local inspection log. It is not a deliverable.
        inspection = output/'nested-export.xlsx.inspect.ndjson'
        if inspection.exists(): inspection.unlink()
    assert digest(source) == before
    print('Saved-file and negative controls passed. Visually inspect all five previews before delivery.')


if __name__ == '__main__':
    main()
