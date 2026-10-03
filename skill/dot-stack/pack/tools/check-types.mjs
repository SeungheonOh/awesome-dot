#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const compiler = process.argv[2] ?? process.env.DOT_STACK_TSC ?? "tsc";
const fixture = fileURLToPath(
  new URL("./test/types.compile.mts", import.meta.url),
);
const consumerFixture = fileURLToPath(
  new URL("./test/public-api.compile.mts", import.meta.url),
);
const result = spawnSync(
  compiler,
  [
    "--strict",
    "--noEmit",
    "--target",
    "ES2022",
    "--module",
    "NodeNext",
    "--moduleResolution",
    "NodeNext",
    "--lib",
    "ES2022",
    fixture,
    consumerFixture,
  ],
  { stdio: "inherit", shell: false },
);
if (result.error) {
  process.stderr.write(
    "Type proof was not run: supply an already-installed TypeScript compiler path. No installation attempted.\n",
  );
  process.exitCode = 2;
} else process.exitCode = result.status ?? 1;
