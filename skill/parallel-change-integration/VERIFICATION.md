# Verification and tool references

The original reading-queue rehearsal ran on 2026-10-02 with Git 2.52.0 and Python 3.12.14 on Linux. It used installed tools only, with no network access or dependencies installed. [verification.json](artifacts/verification.json) records the exact revisions, trees, commands, test counts, timestamps, fixture digests and preservation results.

## Observed results

| Check | Observed result |
|---|---|
| Base contract | 3 tests passed |
| Accepted COUNT-1 | 5 tests passed on its immutable commit |
| Accepted MINUTES-1 | 6 tests passed on its immutable commit |
| Proposed alphabetical default | 4 tests ran, 1 failure as expected: the existing input-order assertion |
| Actual MINUTES-1 merge | One content conflict in `queue_summary.py`; captured stage contents match the known inputs |
| Final integration | 10 tests passed on `9e82fb830d86f350a5cd079936e6b968a949e14e`; final tree `f616d5f3bfec66a1d08c950199ad521e3fd7694d` |
| History | Both accepted commits included; held proposal and later count successor excluded |
| Original dirty checkout | Recorded HEAD, branch, refs, index bytes, status, diff digests and working-file contents/modes unchanged |
| Concurrent contributor | Recorded state unchanged after observing its successor commit |
| Bundle | Verified and cloned locally; restored exact final commit and tree; 10 tests passed |
| Patch | Application check passed; applied to base with index update; exact final tree matched; 10 tests passed |
| Bare local remote | New integration ref transferred and read back; contributor successor ref preserved; a fresh clone restored exact commit/tree and passed 10 tests |

The test command was `python -B -m unittest -v`. The patch replay's HEAD remains at the base and its index/worktree contain the patch; its successful test evidence belongs to the resulting tree, not to an invented final commit. Successful committed-revision test runs were clean before and after testing. Logs normalize only the absolute temporary root to `<rehearsal>`; test output and exit status are retained.

## Why the checks matter

The original checkout had staged and unstaged versions of the same file, so comparing only HEAD or final file contents would miss a lost index state. It also had untracked and ignored data, which ordinary tracked diffs would omit. The preservation snapshots measure each of these states separately.

The merge really conflicted. Three-stage source digest checks ensure the documented resolution refers to the intended inputs. Both accepted test files survive, while the joint assertions exercise the combined result. The proposal failure demonstrates incompatible intent rather than a convenient hypothetical reason to defer work.

The count source moved after its accepted commit was pinned. The final history checks prove that integration did not silently absorb the successor or discard it by resetting the source branch. Restoring the bundle and applying the patch independently prove that the delivered files reproduce the checked result. A bare local remote adds a checked delivery boundary: its existing count ref retains the later commit, and the new integration ref is confirmed both by ref readback and a fresh tested clone.

## Git behavior references

Command spellings were checked against the installed Git executable's built-in help. The linked official manuals were also inspected on 2026-10-02 for the behavior described below. The Git rehearsal itself used only local repositories and files:

- [git-merge](https://git-scm.com/docs/git-merge): `--no-ff` and `--no-commit` allow the fixture to retain merge ancestry and inspect the result before its explicit commit. The combination matters because a fast-forward does not create a merge commit to pause
- [git-clone](https://git-scm.com/docs/git-clone): the local fixture uses `--no-hardlinks` for independent object files, a fresh template directory, and an explicit branch when restoring a bundle
- [git-bundle](https://git-scm.com/docs/git-bundle): create, verify and restore a portable history artifact with explicitly named refs
- [git-apply](https://git-scm.com/docs/git-apply): `--check` tests application; `--index` applies the tree patch to the working tree and index
- [git-status](https://git-scm.com/docs/git-status): porcelain output and explicit untracked-file handling provide machine-readable state evidence
- [git-push](https://git-scm.com/docs/git-push) and [git-ls-remote](https://git-scm.com/docs/git-ls-remote): the fixture transfers an explicitly named new ref to its bare local repository and reads back the advertised ID. No force update is used
- [git-worktree](https://git-scm.com/docs/git-worktree): linked worktrees have separate working state while sharing repository data. The rehearsal uses independent local clones instead
- [Git environment variables](https://git-scm.com/docs/git#_environment_variables): the fixture scopes configuration and optional index-lock behavior per process instead of changing the user's settings

The built-in help check confirms available syntax; the recorded rehearsal confirms the exercised behavior on the stated versions. The example does not claim every Git version, platform or repository configuration behaves identically.

## Limits

This is a tiny original fixture with ordinary files and straightforward common ancestry. It does not cover submodules, large-file extensions, sparse checkouts, custom merge drivers or checkout filters, symlinks, generated assets, migrations, unavailable objects, filesystem permission changes, or a live shared-branch race. Those require project-specific inspection and checks. The local bare-repository transfer is a simulation. No human approval, remote CI pass, push to a real service, shared-branch update or publication is claimed.

The artifact checksum list detects changed delivered files when compared with a trusted copy; it is not a signature or an approval record. The fixture's test coverage is evidence for the stated queue contract only.

## Independent readback

An independent inspection and isolated rerun reproduced the recorded final commit and tree, exact patch and bundle bytes, original-state preservation, held successor, and bare-local-remote readback. A second readback confirmed that the bundle's commit authors and committers are the fictional fixture identity. The source packet stayed unchanged.

A separate guide-only case used accepted but incompatible output contracts, an original checkout with a cherry-pick already in progress, and a newer contributor tip. The resulting plan held the incompatible decision, avoided replaying an already included ancestor, and preserved the active operation and newer tip. That case produced a plan only; it did not create a patch or run tests.
