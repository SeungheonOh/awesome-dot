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

## Output

An exhaustive truth table or bounded-test report, counterexamples, and any independently justified gate-count bounds.

## Verification and limits

Check repeated-input inversion, shared nodes, direct input output, invalid references and all example rows. Explain when input count makes exhaustive enumeration impractical.
