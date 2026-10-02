---
name: verify-combinational-truth-tables
description: "Evaluate a bounded acyclic Boolean netlist against an independently specified target truth function and return counterexamples or complete agreement."
---

# Verify a combinational circuit exhaustively

## When to use

A logic implementation, generated puzzle or reusable circuit needs evidence for every possible input under its combinational model.

## Required inputs

- Netlist with stable input/gate identities and chosen output
- Independent target function or explicit expected truth table
- Supported gate vocabulary and maximum input count for exhaustive enumeration

## Workflow

1. Validate references and topological order. Reject cycles, nonexistent outputs and unsupported gates rather than treating them as zero. State that propagation delay and analog behavior are outside the model.
2. Enumerate all input assignments in a declared bit order. Evaluate every gate and the selected output for each assignment without deriving the target from the same gate implementation.
3. Compare complete output vectors and retain every failing input as a counterexample. Passing the currently displayed input is not circuit equivalence.
4. If a minimum-gate claim is requested, establish it separately with a bounded exhaustive search or proof. A working example only establishes an upper bound. For tiny NAND systems, truth-function bitmask search can enumerate reachable signal sets.
5. Return the netlist identity, truth rows and result. Do not call three-input construction budgets optimal merely because smaller-input searches completed.

### Make a failing row actionable

Retain each node’s value for a counterexample so the user can locate the earliest divergence. The target function must be specified independently; copying the netlist into a second evaluator is not an independent functional specification. Keep input bit ordering and selected output explicit.

For larger input counts, estimate the exhaustive row count before running. If only a subset is tested, report that denominator and do not use “equivalent” without qualification. Gate-count search and functional correctness are separate outcomes.

## Output

An exhaustive truth table or bounded-test report, counterexamples, and any independently justified gate-count bounds.

## Verification and limits

Check repeated-input inversion, shared nodes, direct input output, invalid references and all example rows. Explain when input count makes exhaustive enumeration impractical.

## Output record

Netlist identity; gate vocabulary; input/output ordering; number of possible and tested assignments; expected/actual vectors; counterexamples with intermediate values; separate minimum-gate evidence, if any.

## Worked example

A two-input NAND network defines t=NAND(A,B), u=NAND(A,t), v=NAND(B,t), and out=NAND(u,v). The independent target is XOR.

For input order 00, 01, 10, 11, the expected XOR outputs are 0, 1, 1, 0. The intermediate t values are 1, 1, 1, 0, and evaluation of the network produces the same output vector. This establishes agreement on all four Boolean inputs under the acyclic combinational model.

Selecting t as the output instead produces 1, 1, 1, 0 and fails at 00. Return that counterexample rather than a general “wrong circuit” message. The four-gate working network alone does not prove four is the minimum; that needs a separate bounded proof/search.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
