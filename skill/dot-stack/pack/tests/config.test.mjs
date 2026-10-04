import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { validateConfig } from "../scripts/validate-config.mjs";

test("default and published example validate without selecting a model", () => {
  assert.deepEqual(validateConfig({ schema_version: 1 }), []);
  assert.deepEqual(
    validateConfig(
      JSON.parse(
        fs.readFileSync(
          new URL("../config/config.example.json", import.meta.url),
          "utf8",
        ),
      ),
    ),
    [],
  );
});
test("invalid limits, unknown keys, and missing versions fail explicitly", () => {
  for (const value of [
    null,
    [],
    {},
    { schema_version: 2 },
    { schema_version: 1, max_concurrency: 0 },
    { schema_version: 1, max_concurrency: 1.5 },
    { schema_version: 1, max_concurrency: Infinity },
    { schema_version: 1, approval_mode: "automatic" },
  ])
    assert(validateConfig(value).length > 0);
});
test("artifact preferences cannot lexically escape project or encode a drive", () => {
  for (const artifact_directory of [
    "../x",
    "a/../../x",
    "/tmp/x",
    "C:/x",
    "a\\b",
    "a//b",
    "a\0b",
    "",
  ])
    assert(
      validateConfig({ schema_version: 1, artifact_directory }).length > 0,
    );
  assert.deepEqual(
    validateConfig({
      schema_version: 1,
      artifact_directory: ".dot-stack/artifacts",
    }),
    [],
  );
});
test("role choices are scalar preferences, not fabricated entitlement validation", () => {
  assert.deepEqual(
    validateConfig({
      schema_version: 1,
      role_models: { reviewer: "a-host-observed-choice" },
    }),
    [],
  );
  assert(
    validateConfig({ schema_version: 1, role_models: { reviewer: [] } })
      .length > 0,
  );
  assert(
    validateConfig({ schema_version: 1, role_models: { reviewer: "\n" } })
      .length > 0,
  );
  assert(
    validateConfig({ schema_version: 1, role_models: ["inherit"] }).length > 0,
  );
});
