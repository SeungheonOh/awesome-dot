#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const compiler = process.env.TSC_BIN || "tsc";
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "dot-stack-types-"));
const run = (command, args) => {
  const result = spawnSync(command, args, {
    encoding: "utf8",
    timeout: 60000,
    maxBuffer: 4 * 1024 * 1024,
  });
  if (result.error)
    throw new Error(
      `${command}: ${result.error.message}. Provide an installed TypeScript compiler via TSC_BIN; this script does not install one.`,
    );
  return result;
};
try {
  const version = run(compiler, ["--version"]);
  if (version.status !== 0) throw new Error(version.stderr || version.stdout);
  const source = path.join(root, "skills/typescript-best-practices/references");
  for (const name of ["examples.ts", "type-checks.ts"])
    fs.copyFileSync(path.join(source, name), path.join(temporary, name));
  const flags = [
    "--strict",
    "--noUncheckedIndexedAccess",
    "--exactOptionalPropertyTypes",
    "--target",
    "ES2022",
    "--module",
    "commonjs",
  ];
  const positive = run(compiler, [
    ...flags,
    "--outDir",
    path.join(temporary, "compiled"),
    path.join(temporary, "examples.ts"),
    path.join(temporary, "type-checks.ts"),
  ]);
  if (positive.status !== 0)
    throw new Error(
      `Positive and expected-error fixtures failed:\n${positive.stdout}${positive.stderr}`,
    );
  const negativeFile = path.join(temporary, "type-checks.ts");
  const original = fs.readFileSync(negativeFile, "utf8");
  const directives = original.match(/@ts-expect-error/g) || [];
  if (directives.length !== 8)
    throw new Error(
      `Expected eight documented negative cases, found ${directives.length}. Re-review the fixture contract.`,
    );
  fs.writeFileSync(
    negativeFile,
    original.replace(
      /@ts-expect-error/g,
      "expected-error-disabled-for-control",
    ),
  );
  const negative = run(compiler, [
    ...flags,
    "--noEmit",
    path.join(temporary, "examples.ts"),
    negativeFile,
  ]);
  const count =
    `${negative.stdout}${negative.stderr}`.match(/error TS\d+:/g)?.length ?? 0;
  if (negative.status === 0 || count !== 8)
    throw new Error(
      `Negative control expected eight compiler errors, got status ${negative.status} and ${count}:\n${negative.stdout}${negative.stderr}`,
    );
  const runtime = run(process.execPath, [
    path.join(root, "tests/typescript-runtime.cjs"),
    path.join(temporary, "compiled/examples.js"),
  ]);
  if (runtime.status !== 0)
    throw new Error(
      `Runtime examples failed:\n${runtime.stdout}${runtime.stderr}`,
    );
  console.log(
    JSON.stringify(
      {
        ok: true,
        compiler: version.stdout.trim(),
        positive_typecheck: "passed",
        negative_control_errors: count,
        runtime: JSON.parse(runtime.stdout),
      },
      null,
      2,
    ),
  );
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
} finally {
  fs.rmSync(temporary, { recursive: true, force: true });
}
