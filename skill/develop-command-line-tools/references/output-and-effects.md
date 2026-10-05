# Output, processes, and file effects

Read this for streaming callers, complete machine documents, or commands that save results. Begin with the destination promise in the command contract, then implement the publication and failure behavior that makes it true.

## Data is not completion

Choose framing that the consumer can parse: one document, records with a defined delimiter, or an established binary format. Escaping, encoding, order, and empty-result meaning should be explicit where callers depend on them. A syntactically valid result can still describe incomplete work, so parsing alone is not the success condition.

For an incremental stream, publish records as the established contract permits. A late read, validation, or serialization failure can leave earlier records downstream. Describe that prefix as incomplete unless the contract explicitly defines independent item outcomes. Do not silently skip a failed input and label a smaller population complete.

For a bounded complete document, finish computation and serialization privately before writing it to stdout. Choose a supported input/result bound or use private staging if retaining the result would otherwise be excessive. This can prevent a known input failure from emitting document bytes; it cannot make writes to a pipe transactional. Include final output flushing in the process success path. Never promise empty stdout after every possible failure.

A caller that commits a saved derivative only on success must check both the producer and its own processing. Receiving parseable records is insufficient. A producer may complete successfully while a downstream predicate rejects the reported state; report these outcomes with their different meanings.

## Preserve process outcomes

Capture stdout, stderr, and status separately in direct process checks. Use the actual caller's invocation path and environment. A bounded Python 3.12 subprocess check can use `subprocess.run` with an argument sequence and captured streams; choose byte or text handling deliberately. `Popen` is appropriate when the caller actually needs incremental interaction. Draining one pipe while ignoring another can deadlock; use the runtime's documented process I/O support rather than a new ad hoc loop. See [Python 3.12 subprocess](https://docs.python.org/3.12/library/subprocess.html).

In Bash, a pipeline normally reports its final command's status. `pipefail` changes that aggregate; it does not preserve each component's meaning. When those meanings matter, save `PIPESTATUS` immediately or use a process API that retains both results. An intervening command can replace the array. Avoid letting automatic shell error exit prevent the observation from being recorded. These are Bash semantics, not a portable `sh` recipe. See the [Bash 5.3 reference, pipelines and variables](https://tiswww.case.edu/php/chet/bash/bashref.html#Pipelines).

When the command really supports early-closing consumers, decide how that closure is reported and exercise the real pipe. Keep it distinct from malformed input or failure to save a requested result. In Python, broken-pipe handling must consider final stream flushing; changing global signal disposition is not a generic fix. Use the [Python 3.12 SIGPIPE guidance](https://docs.python.org/3.12/library/signal.html#note-on-sigpipe) for that runtime. Do not add signal handlers or a pipe-error policy to every small command by default.

## Publish a complete file

When a designated file must preserve its previous complete contents, use a publication boundary the application owns:

1. Resolve the destination and input relationships before opening it. Settle collisions with input files and existing overwrite behavior
2. Create a unique staging file on the destination filesystem using the runtime's supported temporary-file API. Avoid a predictable shared staging name
3. Write and validate the complete result there; finish and close the write successfully before publication
4. Replace the intended destination using the filesystem operation appropriate to the promised behavior
5. Clean up only staging resources this invocation owns. Before publication, failure leaves the prior destination intact. After publication, report the state actually reached

Staging in the destination directory is a common way to stay on the same filesystem. Python 3.12 `tempfile.mkstemp` provides a created temporary file and its open handle; the caller owns cleanup. `NamedTemporaryFile` has platform-dependent reopening/deletion considerations. See [Python 3.12 tempfile](https://docs.python.org/3.12/library/tempfile.html).

Python 3.12 `os.replace` can overwrite an existing file and can fail across filesystems; its documentation describes successful rename as atomic. This is a single-path publication mechanism, not a multi-file transaction or proof of crash durability. Check actual platform behavior. See [Python 3.12 os.replace](https://docs.python.org/3.12/library/os.html#os.replace).

Choose metadata, symlink, and concurrent-writer behavior only to the depth the real destination requires. Replacing a file can change its metadata; atomic replacement alone does not prevent two writers from losing each other's work. A simple single-writer exporter need not grow a locking system. A shared updater may need the storage system's comparison or transaction facility. Add sync operations and crash testing only when durability is a promised requirement.

An error after replacement may leave the new file committed. Re-read the destination before retrying an uncertain operation; do not promise that every nonzero exit restores old bytes. An interruption before publication differs from one after it. Ordinary cleanup cannot promise to run after forced termination. If interruption matters, check an existing controllable seam and state what that observation covers.

## Respect caller-owned redirection

With ordinary Bash output redirection, `>` creates or truncates the destination as part of preparing the command, subject to shell options and errors. The command cannot restore the prior file merely by delaying its first write. See the [Bash redirection rules](https://tiswww.case.edu/php/chet/bash/bashref.html#Redirections).

If the consumer must protect a previous result, use the tool's explicit saved-output mode or let the caller create its own temporary file, wait for the required producer and consumer results, and then publish. Do not teach a direct redirection over the protected destination as equivalent to staged replacement. Append is another contract entirely: a prefix may remain after failure, and retry may duplicate records.

These language examples refer to Python 3.12 documentation and the Bash 5.3 manual. Check the target runtime and filesystem; they are not evidence that a particular tool has been executed on them.
