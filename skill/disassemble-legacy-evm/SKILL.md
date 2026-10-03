---
name: disassemble-legacy-evm
description: Inspect supplied legacy EVM bytecode under an explicit fork profile, preserving PUSH boundaries and separating syntactic jump candidates from runtime conclusions. Use for a bounded disassembly or control-flow sketch, not transaction execution, decompilation or a vulnerability verdict.
---

# Disassemble legacy EVM bytecode

## When to use

Use when someone needs to inspect hexadecimal EVM code and understand its instruction boundaries and visible branch structure. Deliver an exact disassembly and a clearly partial block map. Opcode recognition does not prove that a contract is safe, reachable, deployed or associated with any particular source code.

## Required inputs

- Supplied bytecode or an authorized public retrieval source
- Intended fork and bytecode format
- Whether the bytes are runtime code, creation code or an unknown artifact
- Requested output and a practical size bound

Do not infer runtime-code identity from an arbitrary hex string. Unknown metadata or embedded data should remain a caveat; do not strip it based on a guessed compiler signature. If the format is EOF or the requested instruction set is unsupported, report that instead of silently interpreting it as the supported legacy profile.

## Workflow

### 1. Normalize transport syntax without changing bytes

Accept a documented optional prefix and whitespace convention. Require complete hexadecimal byte pairs and a finite size limit. Preserve the normalized original byte string in a local inspection artifact when authorized, alongside its source description and chosen fork.

Reject unexpected URLs, comments, odd nibbles or unsupported container headers rather than extracting a plausible-looking substring. The artifact may contain proprietary code or embedded data; disassembly does not authorize uploading it elsewhere.

### 2. Decode sequentially using the declared profile

Maintain a byte program counter. For legacy PUSH1 through PUSH32, consume the specified immediate width and never decode the payload as separate instructions. PUSH0 has no immediate bytes. Preserve each instruction's offset, opcode byte, mnemonic, declared width and available operand bytes.

At end of code, distinguish available bytes from EVM's effective padded operand. In the supported legacy semantics, a short PUSH read is right-padded with zero bytes. Do not report it as a generic parser truncation that automatically makes execution invalid; show the missing-byte count and effective literal separately. The program counter still advances by the declared instruction width.

Recognize opcodes only under the chosen fork. A byte undefined in Cancun may acquire a meaning in a later specification. Keep undefined bytes visible and label their profile-specific exceptional-halt semantics rather than guessing from a current web table covering every revision.

### 3. Identify actual jump destinations

Collect JUMPDEST only at decoded instruction boundaries. A payload byte equal to 0x5b is not a jump destination. Build the destination set from the disassembly, not by searching the raw hex for “5b.”

Use integer-safe representations for pushed values. A PUSH32 literal may exceed JavaScript's safe integer range. Compare it as a big integer against the code range before converting it to a bounded byte offset.

### 4. Construct a deliberately partial block map

Start blocks at entry, at JUMPDEST boundaries and after terminating instructions where more decoded bytes exist. Keep the work linear in the instruction count; repeatedly scanning all instructions for every block can become quadratic on a large sequence of destinations.

For a narrow static sketch, an immediately preceding PUSH in the same block supplies a literal candidate for JUMP or JUMPI. Check that candidate against the actual destination set. Leave other jumps unresolved rather than guessing a value from a distant PUSH through unknown stack operations.

For JUMPI retain the conditional fallthrough as a separate syntactic edge. An invalid literal target does not mean the instruction necessarily faults: a false condition may take the fallthrough. Conversely, a valid target does not prove execution reaches it or that sufficient stack and gas exist.

Do not label blocks unreachable merely because the partial graph has no incoming edge. Dynamic jumps, execution context and the distinction between code and trailing data remain unresolved. Calls and state-changing opcodes are not executed by this workflow.

### 5. Present evidence and limits together

Show the disassembly beside the selected block and its outgoing candidates. Use clear distinctions for valid destination boundaries, invalid literal targets and dynamic/unresolved jumps. Bound the rendered rows or paginate without dropping records from the full local export.

Invalidate an older result when the input or fork selection changes. Keep the original bytes, declared profile and decoding rules in the export. Explain that this is neither a gas estimate nor a stack/reachability proof, decompiler output or security audit.

### 6. Check boundary handling independently

Use small fixtures that expose likely mistakes:

- Every PUSH width, including embedded 0x5b payload bytes
- Every shorter available tail length for those widths
- PUSH0 and fork-specific additions
- Literal jumps to a real destination, an operand byte and an out-of-range value
- A dynamic jump and a conditional fallthrough
- Undefined bytes and unsupported container headers

For randomized byte arrays, compare destination detection to a separate skip-counter oracle that ignores the declared number of following PUSH payload bytes. Reconcile the instructions across blocks so none are lost or duplicated. Keep synthetic execution-like examples labeled as syntax fixtures; testing the disassembler is not testing those byte strings in a live EVM.

## Worked examples

For `61 5b 00 5b 00`, byte 0 is PUSH2, whose immediate bytes occupy offsets 1 and 2. The first actual JUMPDEST is at offset 3. A raw search would incorrectly count offset 1 as another destination.

For `61 ff`, the two available code bytes describe a PUSH2 with one available operand byte. Its effective literal is 0xff00, with one missing byte supplied by right-zero padding. Preserve the original `ff` operand separately from that effective value.

For `36 60 08 57 60 00 5b 00 5b 00`, CALLDATASIZE is followed by PUSH1 0x08 and JUMPI. The literal branch candidate is offset 8, which is a real JUMPDEST; the conditional fallthrough begins at offset 4. This establishes syntactic candidates only, not the actual branch taken for a particular call.

A local Node 24.19 implementation checked all 32 complete PUSH-width fixtures and 528 short-tail cases, then 300 seeded byte arrays against the separate skip-counter oracle. It also checked a 64 KiB destination-heavy input to exercise linear block construction, plus simulated UI pagination, target navigation, stale-result invalidation and export. No chain connection, contract execution or real-browser layout was tested.

## References

- [Ethereum opcode reference](https://ethereum.org/developers/docs/evm/opcodes): cross-check names while retaining an explicit fork profile
- [Cancun stack instructions](https://ethereum.github.io/execution-specs/src/ethereum/forks/cancun/vm/instructions/stack.py.html): PUSH widths and program-counter advancement
- [Cancun buffer reads](https://ethereum.github.io/execution-specs/src/ethereum/forks/cancun/vm/memory.py.html): right-zero padding of short reads
