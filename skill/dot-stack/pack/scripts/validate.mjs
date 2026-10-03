#!/usr/bin/env node
import fs from "node:fs";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

export const REQUIRED_SKILLS = [
  "architect",
  "arena",
  "automate-me",
  "blast-radius",
  "bro",
  "create-verification-skill",
  "dot-mode",
  "figure-it-out",
  "how",
  "interrogate",
  "maintain-verification-skill",
  "make-bot-ui",
  "no-comments",
  "recall",
  "reflect",
  "setup-dot-stack",
  "show-me-your-work",
  "swarm",
  "tdd",
  "teach",
  "technical-writing",
  "typescript-best-practices",
  "unslop",
  "why",
];
export const REQUIRED_PRINCIPLES = [
  "attack-the-premise",
  "boundary-discipline",
  "build-the-lever",
  "encode-lessons-in-structure",
  "exhaust-the-design-space",
  "experience-first",
  "fix-root-causes",
  "foundational-thinking",
  "guard-the-context-window",
  "laziness-protocol",
  "make-operations-idempotent",
  "migrate-callers-then-delete-legacy-apis",
  "minimize-reader-load",
  "model-the-domain",
  "never-block-on-the-human",
  "outcome-oriented-execution",
  "prove-it-works",
  "redesign-from-first-principles",
  "separate-before-serializing-shared-state",
  "sequence-verifiable-units",
  "subtract-before-you-add",
  "test-behavior-not-implementation",
  "type-system-discipline",
];
export const REQUIRED_PLAYBOOKS = [
  "authoring-a-skill",
  "autonomous-run",
  "autopilot-full",
  "autopilot-stack",
  "babysit",
  "bug-fix",
  "eval",
  "feature",
  "hillclimb",
  "investigation",
  "multi-phase-plan",
  "opening-a-pr",
  "orchestrate",
  "pause-safely",
  "perf-issue",
  "prototype",
  "refactoring",
  "runtime-forensics",
  "session-pickup",
  "shipping",
  "trace-forensics",
  "visual-parity",
  "worktree-cleanup",
];

function walk(root, dir = root) {
  const files = [];
  for (const entry of fs
    .readdirSync(dir, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name))) {
    if ([".git", "node_modules", "__pycache__"].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isSymbolicLink())
      throw new Error(
        `Distribution contains a symlink: ${path.relative(root, full)}`,
      );
    if (entry.isDirectory()) files.push(...walk(root, full));
    else if (entry.isFile()) files.push(full);
  }
  return files;
}

// This pack deliberately uses the portable scalar subset, not arbitrary YAML.
export function parseFrontmatter(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) throw new Error("Missing frontmatter");
  const values = {};
  for (const line of match[1].split(/\r?\n/)) {
    if (!line.trim() || line.trimStart().startsWith("#")) continue;
    const item = line.match(/^([a-z][a-z-]*):\s*(.+?)\s*$/);
    if (!item) throw new Error("Frontmatter must use top-level scalar fields");
    const [, key, raw] = item;
    if (Object.hasOwn(values, key)) throw new Error(`Duplicate field ${key}`);
    let value = raw;
    if (raw.startsWith('"')) {
      try {
        value = JSON.parse(raw);
      } catch {
        throw new Error(`Invalid quoted ${key}`);
      }
    } else if (raw.startsWith("'")) {
      if (!/^'(?:[^']|'')*'$/.test(raw))
        throw new Error(`Invalid single-quoted ${key}`);
      value = raw.slice(1, -1).replaceAll("''", "'");
    } else if (
      key !== "name" ||
      !/^[a-z][a-z0-9-]*$/.test(raw) ||
      /^(true|false|null|yes|no|on|off)$/i.test(raw)
    ) {
      throw new Error(
        `Use a quoted string for ${key}; only skill names may be bare.`,
      );
    }
    if (typeof value !== "string" || !value.trim())
      throw new Error(`Empty/non-string ${key}`);
    values[key] = value;
  }
  return values;
}

export function validate(root) {
  root = path.resolve(root);
  const errors = [];
  const fail = (file, message) => errors.push(`${file}: ${message}`);
  const required = (f) => {
    if (!fs.existsSync(path.join(root, f))) fail(f, "required file missing");
  };
  let files;
  try {
    files = walk(root);
  } catch (e) {
    return { ok: false, errors: [e.message], counts: {} };
  }
  for (const name of [
    ...REQUIRED_SKILLS,
    ...REQUIRED_PRINCIPLES.map((p) => `principle-${p}`),
  ])
    required(`skills/${name}/SKILL.md`);
  for (const name of REQUIRED_PLAYBOOKS)
    required(`skills/dot-mode/playbooks/${name}.md`);
  for (const name of [
    "reproduce-and-fix-issues",
    "setup-benny",
    "triage-issue-reports",
  ])
    required(`automations/benny/skills/${name}/SKILL.md`);
  for (const f of [
    "plugin.json",
    ".claude-plugin/plugin.json",
    "package.json",
    "LICENSE",
    "README.md",
    "VERIFICATION.md",
    "tools/dot-stack.mjs",
    "tools/README.md",
  ])
    required(f);
  const skillFiles = files.filter((f) => path.basename(f) === "SKILL.md");
  if (skillFiles.length !== 50)
    fail(
      "skills",
      `expected 50 canonical skills including automation recipes, found ${skillFiles.length}`,
    );
  for (const file of skillFiles) {
    const rel = path.relative(root, file);
    try {
      const meta = parseFrontmatter(fs.readFileSync(file, "utf8"));
      if (meta.name !== path.basename(path.dirname(file)))
        fail(rel, "name must equal directory name");
      if (
        !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(meta.name ?? "") ||
        (meta.name?.length ?? 0) > 64
      )
        fail(rel, "invalid skill name");
      if (!meta.description || meta.description.length > 1024)
        fail(rel, "description missing or exceeds 1024 characters");
      for (const key of Object.keys(meta))
        if (!["name", "description", "compatibility", "license"].includes(key))
          fail(rel, `nonportable field ${key}`);
    } catch (e) {
      fail(rel, e.message);
    }
  }
  let version;
  for (const file of [
    "package.json",
    "plugin.json",
    ".claude-plugin/plugin.json",
  ]) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
      if (data.name !== "dot-stack") fail(file, "incorrect package identity");
      if (!/^\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?$/.test(data.version ?? ""))
        fail(file, "invalid version");
      if (version && data.version !== version) fail(file, "version mismatch");
      version = data.version;
    } catch (e) {
      fail(file, e.message);
    }
  }
  const license = fs.existsSync(path.join(root, "LICENSE"))
    ? fs.readFileSync(path.join(root, "LICENSE"), "utf8")
    : "";
  if (
    createHash("sha256").update(license).digest("hex") !==
    "bc957ca6bee02792566a1a028d105e02e247c6e77cf057061674273da77b200e"
  )
    fail("LICENSE", "complete required MIT notice differs or is absent");
  for (const file of files.filter((f) => /\.md$/i.test(f))) {
    const rel = path.relative(root, file);
    const text = fs.readFileSync(file, "utf8");
    const prose = text.replace(/^```[^\n]*\n[\s\S]*?^```\s*$/gm, "");
    for (const match of prose.matchAll(/!?\[[^\]\n]*\]\(([^)\n]+)\)/g)) {
      let href = match[1].trim().replace(/^<|>$/g, "").split(/\s+"/)[0];
      if (/^(?:[a-z][a-z0-9+.-]*:|#|\/\/)/i.test(href)) continue;
      href = href.split("#")[0].split("?")[0];
      if (!href) continue;
      try {
        href = decodeURIComponent(href);
      } catch {
        fail(rel, `bad link encoding ${href}`);
        continue;
      }
      const target = path.resolve(path.dirname(file), href);
      if (target !== root && !target.startsWith(root + path.sep))
        fail(rel, `local link escapes package: ${href}`);
      else if (!fs.existsSync(target)) fail(rel, `broken local link: ${href}`);
    }
  }
  // Dependency-free runtime helpers use literal ESM imports. Check their closure
  // without importing or executing code from the selected distribution.
  for (const file of files.filter((f) => f.endsWith(".mjs"))) {
    const rel = path.relative(root, file);
    const text = fs.readFileSync(file, "utf8");
    for (const [, specifier] of text.matchAll(/\bfrom\s*["'](\.[^"'\n]+)["']/g)) {
      const target = path.resolve(path.dirname(file), specifier);
      if (!target.startsWith(root + path.sep))
        fail(rel, `module import escapes package: ${specifier}`);
      else if (!fs.existsSync(target) || !fs.statSync(target).isFile())
        fail(rel, `missing local module: ${specifier}`);
    }
  }
  return {
    ok: errors.length === 0,
    version,
    counts: {
      files: files.length,
      skills: skillFiles.length,
      playbooks: REQUIRED_PLAYBOOKS.length,
    },
    errors,
  };
}

export function validateSingleEntry(root) {
  root = path.resolve(root);
  const report = validate(path.join(root, "pack"));
  const errors = [...report.errors.map((message) => `pack/${message}`)];
  try {
    const entry = fs.readFileSync(path.join(root, "SKILL.md"), "utf8");
    const meta = parseFrontmatter(entry);
    if (meta.name !== "dot-stack" || path.basename(root) !== meta.name)
      errors.push("SKILL.md: name must match the dot-stack root directory");
    if (!meta.description || meta.description.length > 200)
      errors.push("SKILL.md: description must contain 1–200 characters");
    if (Object.keys(meta).some((key) => !["name", "description"].includes(key)))
      errors.push("SKILL.md: only portable name and description metadata are supported");
    if (entry !== fs.readFileSync(path.join(root, "pack/exports/dot-stack.SKILL.txt"), "utf8"))
      errors.push("SKILL.md: entrypoint differs from the reviewed template");
    if (!fs.readFileSync(path.join(root, "LICENSE")).equals(fs.readFileSync(path.join(root, "pack/LICENSE"))))
      errors.push("LICENSE: root notice must equal the complete library notice");
    const links = [...entry.matchAll(/!?\[[^\]\n]*\]\(([^)\n]+)\)/g)];
    if (!links.length) errors.push("SKILL.md: resource links are missing");
    for (const [, href] of links) {
      // This short controlled entrypoint uses only plain local resource links.
      if (/^(?:[a-z][a-z0-9+.-]*:|\/|#)/i.test(href) || href.includes("\\")) {
        errors.push(`SKILL.md: expected a local resource link: ${href}`);
        continue;
      }
      const target = path.resolve(root, decodeURIComponent(href));
      if (!target.startsWith(root + path.sep))
        errors.push(`SKILL.md: local link escapes package: ${href}`);
      else if (!fs.existsSync(target) || !fs.statSync(target).isFile())
        errors.push(`SKILL.md: missing resource: ${href}`);
    }
    for (const file of walk(root)) {
      if (fs.lstatSync(file).isSymbolicLink()) errors.push(`Symlink: ${file}`);
    }
  } catch (error) {
    errors.push(error.message);
  }
  return { ...report, ok: errors.length === 0, format: "single-entry", errors };
}

if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
  const root =
    process.argv[2] ??
    path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
  const report = process.argv.includes("--single-entry")
    ? validateSingleEntry(root)
    : validate(root);
  console.log(JSON.stringify(report, null, 2));
  process.exitCode = report.ok ? 0 : 1;
}
