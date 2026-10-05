# Maintenance and delivery

Read the maintenance section when changing an existing command. Read the delivery section only when a reusable artifact or installed command is requested. Both continue the same compact contract used to build the command.

## Change the consumed behavior deliberately

Inspect supplied callers, wrappers, scripts, examples, and relevant tests. Identify which can change together and which are independently deployed or unknown. Lack of a repository match does not establish absence of external use.

Compare affected promises, rather than only option names:

- Old invocations still accepted by the changed command
- New output and statuses still understood by existing callers
- New callers with the old command, only when that mixed-version state must work

Look especially at defaults, config origin, output framing, field meaning, ordering, partial results, and file effects. An added output field is compatible only if the relevant reader accepts it. A stream converted into a final buffer changes observable behavior even if a short sample has identical bytes. A changed process status can alter a build script without changing its parsed data.

Keep a failing-before case when it can be obtained safely, with the input, invocation, status, and affected state. Make the smallest change supported by that observation and the accepted contract. Keep the established stdout promise while changing explicit file publication if those are separate modes. When a caller change is required and authorized, update its failure handling and documentation too.

Rerun the distinguishing case and a nearby existing use against the changed command. Compare semantic values for a semantic format and bytes only when byte stability is promised. Inspect saved effects, including preservation after the relevant failure and replacement after a later successful run. Do not replace a contract check with a help snapshot or freeze irrelevant wording.

## Choose the delivery boundary

A documented source command can be the complete requested deliverable. An extracted source archive demonstrates relocation only if actually exercised there. Neither establishes native package installation. Choose the requested form before spending time on release work.

For an installable CLI, retain its contract and consumer cases while applying the established `release-artifact-verification` method when available. The essential steps remain usable without that skill:

1. Identify the source candidate or supplied package, runtime requirements, public command, and permitted build/install route. Inspect build declarations and executable hooks before running them
2. Preserve and identify the exact package with filename, size, and SHA-256. Inspect its registration, required code/resources, and relevant dependencies rather than trusting a successful build
3. Install those bytes into a fresh disposable consumer environment through an available authorized native route. Avoid editable installs and unintended source or previous-install leakage
4. From outside every source copy, establish the installed origin and invoke the actual public wrapper. Run the same meaningful consumer operation and consequential failure used during development; inspect the saved result as well as status
5. Keep packaging, installation, and runtime observations separate. Bind the result to the tested artifact and environment; a rebuild with the same name is a new candidate

For Python packages, `console_scripts` metadata tells an installer which wrappers to create. The registration is not proof that the generated command can complete its work, and an installer's scripts directory is not necessarily on the caller's PATH. Inspect the wrapper/provenance and call it unambiguously. See [PyPA's entry-points specification](https://packaging.python.org/en/latest/specifications/entry-points/).

An original, fully inspected dependency-free local package can be suitable for an authorized offline check with already installed tools. Confirm the backend and installer actually exist. Supply the exact local artifact and disable unwanted dependency/index retrieval through the chosen tool's supported options and configuration. Do not treat “offline” flags as an operating-system network sandbox, or assume that dependency suppression validates a package that actually needs dependencies. If the route needs missing tools or new authority, finish the available inspection and identify that specific gap.

Keep the checked artifact and useful evidence outside disposable installation directories. Native packaging is conditional; it does not require publishing, downloading a new toolchain, altering shell profiles, or installing into a global environment.

## Hand over the usable result

Use existing project tests and logs where they carry the evidence. A concise note can pair the command contract with the actual invocation, input, observed stdout/stderr/status, saved result, and candidate identity. Avoid a parallel ledger when the project already records these clearly.

State separately what worked from source, after relocation, and after installation. Name untested targets instead of implying universal portability. Deliver the requested command or artifact and its real usage path; if a stage is blocked, preserve the usable work and make the next necessary step precise.
