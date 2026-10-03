# Verification for dot-stack 0.4.0

This experimental workflow library includes 50 skills (47 core and three optional issue-automation skills) and 23 task playbooks. Local structural checks and helper tests do not establish better engineering outcomes or live-host behavior.

## Reproduce the local checks

Run from this `pack/` directory with Node.js 22 or later and Python 3.10+ on a POSIX filesystem:

```sh
node scripts/validate.mjs
PYTHONDONTWRITEBYTECODE=1 npm test
node tools/dot-stack.mjs doctor
node tools/dot-stack.mjs --help
```

The validator checks metadata, relative links, version alignment, distribution inventory, and license preservation. The executable tests cover helper behavior and packaging, including native and single-entry resource closure, unsafe paths, and overwrite refusal. These checks use synthetic fixtures and do not require account credentials.

To check the TypeScript examples with an already installed compiler, run `npm run test:types`. The command does not install a compiler.

To build either archive, choose a fresh absolute output path outside this directory:

```sh
python3 scripts/package.py --format native --output /fresh/output/dot-stack-0.4.0-native.zip
python3 scripts/package.py --format single-entry --output /fresh/output/dot-stack-0.4.0-single-entry.zip
```

## Observed local checks

On 2026-10-03, Linux with Node.js 24.19.0 and Python 3.12.14 passed structural validation for 50 skills and 23 playbooks, all 117 Node tests, and all 19 Python packaging tests. The doctor and help commands passed, and both archive formats built successfully. The optional TypeScript check passed using an explicitly selected existing TypeScript 7.0.2 compiler: positive compilation, eight expected negative-control errors, and all 51 runtime assertions. The compiler was selected with `TSC_BIN`; no compiler was installed by the check. These are local regression checks, not live-host or effectiveness measurements.

## Scope and limits

A successful local test run verifies only its observed checks. It does not establish productivity, token savings, lower cost, universal superiority, live provider installation or upload acceptance, account-specific permissions, or production behavior. Each host and real task needs its own checks. Reading or uploading this skill grants no credentials, capabilities, permissions, or scheduling.

No benchmark results or private evaluation materials are included.
