---
name: run-bounded-local-sql
description: "Analyze small authorized tabular inputs with read-only SQL in a disposable local database, preserving cell types and exact results while enforcing query, resource and output limits."
---

# Run Bounded Local SQL Analysis

## When to use

Use this when a user or agent needs SQL joins, grouping or inspection over a small supplied dataset without connecting to or modifying a live database. The outcome is a bounded result and query plan tied to the input selection. This is not a production database gateway, an OS sandbox or permission to retrieve additional private records.

## Required inputs

- Authorized table data, stable table/column names and explicit cell types
- The exact query or analysis question
- Row, column, cell, input-byte, execution-time and output limits
- An already available local SQL runtime and an isolated execution destination
- The intended result format and treatment of truncation and large integers

Resolve type ambiguity before making analytical claims. CSV normally supplies strings, including leading zeros and empty fields; do not silently turn identifiers into numbers or blanks into null. If conversion is requested, record it and check invalid conversions separately from valid zero values.

## Workflow

### 1. Validate the supplied data before SQL construction

Check table and column identities, case sensitivity, duplicate names, row widths, value types and total size. Reject unsupported or unsafe numeric inputs rather than accepting an already rounded number. Keep per-cell and aggregate bounds separate.

Use parameter binding for every cell insertion. Quote validated identifiers using the engine's rules; never interpolate a user-provided cell value into SQL. A strict identifier grammar can simplify a small tool, but any generated replacement names must be shown beside the original headers.

### 2. Create a disposable database with no production connection

Create a new in-memory database for the request. Populate only the authorized supplied tables, then change to read-only query operation. Do not attach files, open arbitrary paths, inherit a production connection or enable extensions as part of this workflow.

Where the implementation uses a child process, pass data over a bounded input channel rather than a shell command. Use the trusted runtime and script paths directly; convert file URLs with the runtime's path utility so extraction paths containing spaces still work. Avoid inheriting credential-bearing environment variables or runtime injection options that the query does not need.

### 3. Enforce allowed operations at the engine boundary

Use a real engine authorization mechanism, not a regular expression that merely requires SQL to begin with SELECT. Permit reads of supplied tables and the needed functions; reject writes, attachments, schema access, extension loading and unsupported recursion.

For Node's SQLite binding, [setAuthorizer](https://nodejs.org/api/sqlite.html) provides action callbacks. Confirm the installed runtime supports it and test its actual callback arguments. Some count queries report an empty column and no database name; handle only the observed narrow case for known supplied tables rather than broadly allowing unknown reads.

Require exactly one statement. If the engine prepares only the first statement, compare its accepted source with the request and reject trailing executable text. Do not report success for SELECT 1 while silently ignoring a second requested operation.

### 4. Bound computation independently of returned rows

A row limit does not bound a join, aggregation or sort's work. Enforce a parent-controlled deadline and a database allocation cap where the runtime supports one. In SQLite, [hard_heap_limit](https://www.sqlite.org/pragma.html#pragma_hard_heap_limit) can cap its allocator; check the applied value rather than assuming an unknown pragma succeeded.

A synchronous native query may not respond to a browser abort. A disposable child process lets the parent terminate the computation itself. Bound concurrent requests and captured output as well, and release capacity after completion, error or cancellation. These controls are not a substitute for an OS security boundary.

### 5. Preserve exact result values and coverage

Return ordered columns and row arrays so duplicate output labels cannot overwrite values in an object. Preserve null separately from empty strings. Serialize integers outside JavaScript's exact range as tagged decimal strings rather than converting them to Number; use a consistent typed representation for all integers if that simplifies consumers.

Reject unsupported non-finite numbers and oversized cells explicitly. If returning only the first N rows, read enough to know whether another row exists and mark truncation. Do not label N as the total result count unless independently computed. Include the query plan as diagnostic evidence, not a promise of production performance.

### 6. Verify failure containment and interrupted UI flows

Test a valid aggregate and join, nulls, exact large integers, duplicate column labels and an intentionally over-limit result. Confirm write/attachment/schema/extension/recursive attempts fail before affecting anything outside the supplied dataset.

Run an expensive synthetic query under the deadline, then verify a normal query still succeeds. Check malformed input, repeated requests, cancellation and a late response after the user edits the data. An old response must not re-enable export or replace the new draft.

For a loopback web interface, bind to the loopback address, validate Host and Origin, require the intended content type, avoid caching data responses and do not log query bodies. Do not expand to public hosting or add access credentials under the guise of finishing local analysis.

## Worked example

The supplied orders table contains rows [A,12], [A,18] and [B,7], with amounts explicitly numeric. Grouping by client and summing amount returns A→30 and B→7. Return the query, ordered columns and typed values, plus the relevant plan and input row count.

If the same data arrived as CSV, an ID 001 remains the string 001. An empty amount remains an empty string unless the user approves a null/conversion rule. A CAST can turn some malformed numeric text into zero, so successful SQL execution alone does not validate that column.

A separate query returning the integer 9223372036854775807 must preserve that exact decimal value. Converting it to a JavaScript Number would lose precision even though the database produced a correct result.

The local implementation used for this workflow passed real SQLite aggregate/precision checks, operation-denial cases, a killed over-budget query, subsequent-query recovery, loopback HTTP limits and obsolete-response interaction tests. Those checks do not establish safety for a public multi-user deployment.

## Deliverable and stopping point

Return the exact query, input scope/types, result coverage, typed values, plan and observed limits. Identify truncated or failed stages without substituting stale output. Exported results may themselves contain private data; save or share them only within the user's authorized destination. Discard the temporary database/process after the request and leave original sources unchanged.
