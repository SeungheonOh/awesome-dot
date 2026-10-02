# Switchboard Registry: Two Working Exports, One Broken Contract

This original, fictional JavaScript companion checks the **exact npm tarball** as a fresh consumer. Every required file is present, both export branches load, and each works alone. The rejected candidate still loses registrations when one application mixes `import()` and `require()`.

## The consumer contract

`switchboard-registry-demo@0.4.0` promises one registry per installed package copy in one Node.js process, shared by its two public entry points:

- `register(name, value)` stores and returns the same value; names must be nonempty strings
- `lookup(name)` returns the exact stored value, or `undefined` for a missing name
- `names()` returns the current unique names in sorted order
- A registration or replacement through either entry is immediately visible through the other, in either load order

Think of an ESM application registering a renderer and a CommonJS plugin looking it up. Separate successful tests of those components do not establish that they communicate through the same registry. Separate physical installations, processes and worker threads are outside this contract.

The reviewed package has no dependencies, lifecycle scripts, network operations or subprocess calls. Its four files are [package.json](fixtures/source/package.json), [core.cjs](fixtures/source/core.cjs), [index.cjs](fixtures/source/index.cjs) and [index.mjs](fixtures/source/index.mjs). The `private` field prevents ordinary registry publication; this example only packs and locally installs it.

## What the received packages did

Observed on Linux x86-64, Node.js **v24.19.0**, npm **11.9.0**, with Python **3.12.14** orchestrating the checks. Each candidate was packed in a separate source copy, inspected, and actually installed from its local tarball into a fresh project with a fresh npm cache. Each consumer mode ran in a new process outside both source copies.

| Evidence | Rejected candidate | Corrected candidate |
| --- | --- | --- |
| npm pack | Exit 0 | Exit 0 |
| Four regular members, exact reviewed bytes | Pass | Pass |
| Offline npm install and lockfile integrity | Pass | Pass |
| `import-only` | Exit 0 | Exit 0 |
| `require-only` | Exit 0 | Exit 0 |
| `import-first`, then `require` | Exit 1: split state | Exit 0 |
| `require-first`, then `import()` | Exit 1: split state | Exit 0 |
| Resolved paths and all installed file hashes | Match tarball | Match tarball |

The rejected mixed-mode checks fail bidirectional visibility, replacement visibility and agreement of names. Both branches still expose all three functions, start empty and pass their own local read/write checks. This is an observed runtime contract defect in the package's entry-point design, not a missing file, installer error or failure to parse JavaScript.

The [consumer](scripts/consumer.mjs) tests actual object identity, inserts keys in reverse sort order, overwrites an existing key, checks an absent name, and rejects both an empty and a non-string name. Its four modes select the package's real export conditions. It uses `import()` and `createRequire()` inside an `.mjs` driver; `require-only` means only the CommonJS package branch is loaded, not that the driver is a `.cjs` application. Merely resolving both branches does not execute them. No static named-import syntax or bundler transformation is being certified.

## The smallest repair

The rejected ESM entry creates its own `Map`; CommonJS uses the one in `core.cjs`. Replace only the copied ESM entry with [this wrapper](fixtures/repair/index.mjs):

```js
import core from './core.cjs';
export const { register, lookup, names } = core;
```

Both entries now delegate to the same cached core. Package metadata, export targets, the CommonJS wrapper and the core implementation are unchanged. The source fixture and rejected tarball are preserved.

These are two **fixture build candidates** with the same name, version and filename, kept in separate folders. They are not interchangeable releases and were not published to a package registry. The hashes identify which bytes passed. Apply a real project's version policy before publishing any repair.

| Candidate | Artifact | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Rejected | [switchboard-registry-demo-0.4.0.tgz](artifacts/rejected/switchboard-registry-demo-0.4.0.tgz) | 669 | `0100c3ac89308f153d172dc49cdd0f721d0f83a012c7fc855fac3d3cd5b7d6af` |
| Corrected | [switchboard-registry-demo-0.4.0.tgz](artifacts/corrected/switchboard-registry-demo-0.4.0.tgz) | 687 | `cfe9b1895f1592b49f3af939055fb5e0d2449e3d02fd428135114a275eb904ca` |

Both archives contain exactly `package/package.json`, `package/core.cjs`, `package/index.cjs` and `package/index.mjs`. [Rejected contents](evidence/rejected-contents.json) and [corrected contents](evidence/corrected-contents.json) give each member's size and SHA-256. The only changed member is `index.mjs` (421 to 151 bytes). A digest identifies content; it does not authenticate a publisher.

## Recheck these bytes, or build another candidate

Prerequisites: existing Node.js 24, npm 11 and Python 3.10+ on a Unix-like system. Read the fixture, [consumer](scripts/consumer.mjs) and [reproducer](scripts/reproduce.py) before execution. The helper is restricted to these adjacent reviewed inputs; it is not a general tarball installer. Do not use Python's `-O` option, which disables its assertions.

From this companion directory, choose a new output directory outside it:

```sh
python3 scripts/reproduce.py --verify-bundled --output ../switchboard-readback
```

That route checks the stored tarball hashes and installs copies of those exact bytes without rebuilding. To pack fresh copies and check the new candidates instead:

```sh
python3 scripts/reproduce.py --output ../switchboard-rebuild
```

The helper creates separate source, consumer and cache directories. It refuses an existing output path and leaves its outputs in place. It never deletes, renames or hides the source checkout. A new build may have different bytes on another toolchain; report its fresh digest instead of reusing the bundled result.

Both npm routes use `--offline --ignore-scripts --no-audit --no-fund --workspaces=false --update-notifier=false`, explicit empty local user/global config files, and fresh caches. Installation names the inspected local `.tgz`, never a registry package or a source directory. A saved npm lockfile entry is checked against the tarball's SHA-512 integrity and local path. There are no tool downloads, dependency downloads or config changes. These flags and a dependency-free fixture are a bounded offline workflow, not a network sandbox for arbitrary programs.

Only `PATH` is inherited by subprocesses; `LANG` is supplied explicitly. No home variable is reassigned, and no credential or existing npm config file is inspected. `NODE_PATH`, `NODE_OPTIONS` and inherited npm settings are omitted. Node runs with `--no-global-search-paths`. Before installation, both resolvers must report the package absent. Afterward, both entries must resolve to regular, non-symlink files under the new consumer's own `node_modules/switchboard-registry-demo/`; every installed file must exactly match its inspected archive member.

Before npm can unpack the tarball, the helper bounds compressed and expanded size and checks all four members for exact names, regular-file type, non-executable mode, no links, no sparse/PAX metadata, and byte equality with the reviewed fixture. It never extracts an archive itself. It also checks source hashes before and after the run. A setup failure, unexpected output, timeout or different failure signature stops the run; an expected rejected-candidate exit is not treated as a general pass.

## Independent installed readback

An independent inspected run installed copies of both exact bundled archives and reproduced the two consumer readback records. Four additional mixed-order runs used zero, false, null, undefined and empty values, replacements and distinct Unicode keys. The rejected package kept split state; the corrected package shared it. Archive members, lockfile integrity, installed bytes and resolved paths were checked, and reusing an existing output was refused unchanged. This review did not repack the archives or test another runtime or package manager.

## Evidence and limits

[The manifest](evidence/manifest.json) ties the stages to exact artifacts and records runtime and source preservation. [Commands](evidence/commands.json) retains argv, working directories, exits and output. Paths in those records are relative to the new output directory; `node` and `npm` denote the installed executables selected for that run. [Rejected readback](evidence/rejected-readback.json) and [corrected readback](evidence/corrected-readback.json) contain npm's lockfile entry, installed-file hashes, exact resolved entry paths relative to each consumer, load orders and individual assertions.

[Additional checks](evidence/rechecks.json) reinstalled the bundled bytes through `--verify-bundled` and independently repeated the consumer matrix with Unicode seed `独立レビュー-Δ-🙂`. Replacing only the ESM entry in a disposable copy of the corrected installation restored the same four failures in both mixed orders. That control tests the defect, not another artifact installation. An existing-output sentinel test also confirmed no-clobber behavior; original inputs and existing installations stayed unchanged.

The observed result covers this one Linux runtime and npm version, these two tarballs, one installed copy per process and the declared API. It does not establish Windows/macOS behavior, other Node versions, pnpm/Yarn, browser bundling, TypeScript declarations, dependency resolution, multiple installed copies, upgrades or release readiness.

Node's [v24.19.0 conditional-export documentation](https://nodejs.org/download/release/v24.19.0/docs/api/packages.html#conditional-exports) defines how `import` and `require` select these branches. Modern Node can also load synchronous ESM with `require()`; this example makes no contrary assumption. The [older dual-package guide](https://github.com/nodejs/package-examples/blob/main/guide/07-dual-packages/README.md) explains the historical shared-state hazard but warns that parts predate `require(esm)`. The conclusion here comes from the recorded consumer runs, not a recommendation to use that older guide for new package design. npm's [v11.9.0 pack documentation](https://github.com/npm/cli/blob/v11.9.0/docs/lib/content/commands/npm-pack.md) and [v11.9.0 install documentation](https://github.com/npm/cli/blob/v11.9.0/docs/lib/content/commands/npm-install.md) describe the local tarball route; the matching documentation shipped with the installed npm was also checked.
