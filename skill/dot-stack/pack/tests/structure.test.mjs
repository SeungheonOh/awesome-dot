import test from "node:test";
import assert from "node:assert/strict";
import { parseFrontmatter } from "../scripts/validate.mjs";

test("portable scalar metadata parses without host dependencies", () => {
  assert.deepEqual(
    parseFrontmatter(
      '---\nname: a-skill\ndescription: "Review a change: preserve its scope."\n---\n# Skill',
    ),
    { name: "a-skill", description: "Review a change: preserve its scope." },
  );
});
test("duplicate keys are rejected rather than shadowing intent", () => {
  assert.throws(
    () => parseFrontmatter("---\nname: first\nname: second\n---\n"),
    /Duplicate/,
  );
});
test("missing, malformed, implicit object and empty fields are rejected", () => {
  for (const text of [
    "# no metadata",
    "---\nname:\n---\n",
    "---\nname: {nested: value}\n---\n",
    '---\nname: "unterminated\n---\n',
  ])
    assert.throws(() => parseFrontmatter(text));
});
test("quoted apostrophes and CRLF retain their content", () => {
  assert.equal(
    parseFrontmatter(
      "---\r\nname: test\r\ndescription: 'Keep the user''s changes.'\r\n---\r\n",
    ).description,
    "Keep the user's changes.",
  );
});

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {
  validate,
  REQUIRED_SKILLS,
  REQUIRED_PRINCIPLES,
  REQUIRED_PLAYBOOKS,
} from "../scripts/validate.mjs";
function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "dot-stack-structure-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const put = (file, text = "") => {
    fs.mkdirSync(path.dirname(path.join(root, file)), { recursive: true });
    fs.writeFileSync(path.join(root, file), text);
  };
  const skill = (prefix, name) =>
    put(
      `${prefix}/${name}/SKILL.md`,
      `---\nname: ${name}\ndescription: "Inspect a specific fixture without side effects."\n---\n# Fixture\n`,
    );
  for (const name of [
    ...REQUIRED_SKILLS,
    ...REQUIRED_PRINCIPLES.map((x) => `principle-${x}`),
  ])
    skill("skills", name);
  for (const name of [
    "reproduce-and-fix-issues",
    "setup-benny",
    "triage-issue-reports",
  ])
    skill("automations/benny/skills", name);
  for (const name of REQUIRED_PLAYBOOKS)
    put(`skills/dot-mode/playbooks/${name}.md`, "# Fixture\n");
  for (const name of [
    "package.json",
    "plugin.json",
    ".claude-plugin/plugin.json",
  ])
    put(name, JSON.stringify({ name: "dot-stack", version: "0.1.0" }));
  for (const name of [
    "README.md",
    "VERIFICATION.md",
    "tools/README.md",
    "tools/dot-stack.mjs",
  ])
    put(name, "");
  put(
    "LICENSE",
    fs.readFileSync(new URL("../LICENSE", import.meta.url), "utf8"),
  );
  return { root, put };
}
test("complete structural fixture passes and reports actual counts", (t) => {
  const { root } = fixture(t);
  const report = validate(root);
  assert.equal(report.ok, true, JSON.stringify(report.errors));
  assert.equal(report.counts.skills, 50);
});
test("omitted skill and playbook are not hidden by matching totals", (t) => {
  const { root, put } = fixture(t);
  fs.renameSync(path.join(root, "skills/how"), path.join(root, "skills/other"));
  fs.unlinkSync(path.join(root, "skills/dot-mode/playbooks/bug-fix.md"));
  const report = validate(root);
  assert.equal(report.ok, false);
  assert(report.errors.some((x) => x.includes("skills/how")));
  assert(report.errors.some((x) => x.includes("bug-fix")));
});
test("host-specific metadata, identity and version mismatches fail", (t) => {
  const { root, put } = fixture(t);
  put(
    "skills/how/SKILL.md",
    '---\nname: how\ndescription: "Inspect subsystem."\nallowed-tools: "shell"\n---\n',
  );
  put("plugin.json", JSON.stringify({ name: "different", version: "0.2.0" }));
  const report = validate(root);
  assert.equal(report.ok, false);
  assert(report.errors.some((x) => x.includes("nonportable")));
  assert(report.errors.some((x) => x.includes("identity")));
  assert(report.errors.some((x) => x.includes("version mismatch")));
});
test("broken and escaping local links fail; external and code examples are excluded", (t) => {
  const { root, put } = fixture(t);
  put(
    "README.md",
    "[lost](missing.md)\n[escape](../secret.md)\n[external](https://example.com/reference)\n```md\n[example](not-an-actual-link.md)\n```\n",
  );
  const errors = validate(root).errors;
  assert(errors.some((x) => x.includes("broken local link")));
  assert(errors.some((x) => x.includes("escapes package")));
  assert(!errors.some((x) => x.includes("not-an-actual-link")));
});
test("symlinks are rejected before distribution traversal", (t) => {
  const { root } = fixture(t);
  fs.symlinkSync(os.tmpdir(), path.join(root, "outside"), "dir");
  assert.equal(validate(root).ok, false);
});
test("license attribution must survive packaging", (t) => {
  const { root, put } = fixture(t);
  put("LICENSE", "Copyright someone else");
  assert(validate(root).errors.some((x) => x.startsWith("LICENSE:")));
});

test("ambiguous YAML scalars cannot falsely pass host metadata checks", () => {
  for (const raw of [
    "Note: do this",
    "false",
    "true",
    "null",
    "yes",
    "123",
    "2026-10-02",
    "text # silently truncated",
  ])
    assert.throws(() =>
      parseFrontmatter(`---\nname: example\ndescription: ${raw}\n---\n`),
    );
});
test("truncated license cannot satisfy attribution-only substring checks", (t) => {
  const { root, put } = fixture(t);
  put(
    "LICENSE",
    fs.readFileSync(new URL("../LICENSE", import.meta.url), "utf8").slice(0, 100),
  );
  assert(validate(root).errors.some((x) => x.startsWith("LICENSE:")));
});

test("closed YAML subset rejects remaining implicit syntax", () => {
  for (const raw of ["- item", "# comment", "trailing:", "'can't'"])
    assert.throws(() =>
      parseFrontmatter(`---\nname: example\ndescription: ${raw}\n---\n`),
    );
});
