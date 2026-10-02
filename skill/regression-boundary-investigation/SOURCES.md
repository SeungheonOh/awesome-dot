# Official documentation checked

Checked on 2026-10-02. The executed fixture used Git 2.52.0 and Python 3.12.14; online manuals can describe newer versions. The example uses established commands available in that installed toolchain and does not depend on newer convenience options.

- [Git: bisect](https://git-scm.com/docs/git-bisect): `run` exit classification, ambiguous skipped neighbors, retained logs, first-parent scope, and returning to the pre-search checkout with `bisect reset`. The external-predicate placement follows the manual's warning about test scripts inside a moving checkout. The documentation's destructive example commands were not used
- [Git: clone](https://git-scm.com/docs/git-clone): `--no-hardlinks` copies local object files rather than hardlinking them. This does not make historical code safe to run or preserve dirty files in the clone
- [Git: status](https://git-scm.com/docs/git-status): status may refresh/write the index; `--no-optional-locks` avoids that optional mutation during original-state inspection
- [Python: subprocess](https://docs.python.org/3/library/subprocess.html): argument-list execution, timeouts, captured output and the negative POSIX signal convention for `returncode`. The fixture uses `subprocess.run` without a shell and classifies product assertions separately from runner failure

These sources establish tool behavior. The half-open interval contract, histories, test matrix, original-work preservation checks and causal controls are original example material, not claims quoted from those manuals.
