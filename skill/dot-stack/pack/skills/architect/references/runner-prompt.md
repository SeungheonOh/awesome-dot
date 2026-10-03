# Candidate design brief

The coordinator supplies the actual task, source revision or input identities, grounding, constraints, authorized output directory, allowed actions, and acceptance criteria. Do not send an unfilled brief to a worker.

Produce one design package using [the rationale format](rationale-template.md). Do not inspect other candidates until comparison begins. Do not edit application code, publish changes, or create a new environment unless the brief explicitly authorizes it.

- Write caller examples before types. Include the ordinary operation and a meaningful failure, retry, or cancellation
- Choose data structures by actual access patterns. Explain index or cache needs from those patterns, not anticipated fashion
- Give each invariant one owner. Parse external data once at the relevant trust boundary and define the failure result
- Specify lifecycle and concurrency. For multiple writers, explain isolation, integration, or a real transaction. Do not recommend locks without identifying the shared state
- Express variants in types when they exclude real invalid combinations. Validate constraints the language cannot express
- Keep stub implementations unmistakable. Place them only in the authorized design output, not on the production execution path
- Read [red flags](design-red-flags.md), and distinguish justified boundaries from empty forwarding layers
- State what your candidate deliberately does not solve. Record the strongest alternative you rejected and the evidence that would change your mind

Return the full sketch and rationale, evidence locations, and any blocker. If files cannot be written, return a clearly unapplied document. An unavailable model or worker tool is a capability limit, not a reason to guess tool names.
