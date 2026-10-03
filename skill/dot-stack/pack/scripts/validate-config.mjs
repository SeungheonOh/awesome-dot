#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const record = (value) =>
  value !== null && typeof value === "object" && !Array.isArray(value);
export function validateConfig(value) {
  const errors = [];
  if (!record(value)) return ["Configuration must be an object."];
  const keys = new Set([
    "schema_version",
    "max_concurrency",
    "role_models",
    "artifact_directory",
  ]);
  for (const key of Object.keys(value))
    if (!keys.has(key))
      errors.push(
        `Unknown field ${key}; preserve it and resolve the schema mismatch before rewriting configuration.`,
      );
  if (value.schema_version !== 1) errors.push("schema_version must be 1.");
  if (
    Object.hasOwn(value, "max_concurrency") &&
    (!Number.isSafeInteger(value.max_concurrency) || value.max_concurrency < 1)
  )
    errors.push("max_concurrency must be a positive safe integer.");
  if (Object.hasOwn(value, "role_models")) {
    if (!record(value.role_models))
      errors.push("role_models must map role names to strings.");
    else
      for (const [role, model] of Object.entries(value.role_models)) {
        if (!/^[a-z][a-z0-9-]*$/.test(role))
          errors.push(`Invalid role name ${role}.`);
        if (
          typeof model !== "string" ||
          !model.trim() ||
          /[\r\n\0]/.test(model)
        )
          errors.push(`Invalid model preference for ${role}.`);
      }
  }
  if (Object.hasOwn(value, "artifact_directory")) {
    const directory = value.artifact_directory;
    if (
      typeof directory !== "string" ||
      !directory.trim() ||
      directory.startsWith("/") ||
      /[\\:\x00-\x1f]/.test(directory) ||
      directory.split("/").some((p) => p === ".." || p === "")
    )
      errors.push(
        "artifact_directory must be a nonempty project-relative forward-slash path without traversal.",
      );
  }
  return errors;
}
if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
  try {
    if (process.argv.length !== 3)
      throw new Error("Usage: node scripts/validate-config.mjs CONFIG.json");
    const errors = validateConfig(
      JSON.parse(fs.readFileSync(process.argv[2], "utf8")),
    );
    console.log(
      JSON.stringify(
        {
          ok: errors.length === 0,
          errors,
          scope:
            "Schema only; host availability and authorization are not checked.",
        },
        null,
        2,
      ),
    );
    process.exitCode = errors.length ? 1 : 0;
  } catch (e) {
    console.error(e.message);
    process.exitCode = 2;
  }
}
