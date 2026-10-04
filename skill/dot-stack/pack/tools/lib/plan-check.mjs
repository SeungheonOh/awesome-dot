import { readFile, stat, realpath } from "node:fs/promises";
import { resolve, relative, isAbsolute } from "node:path";
import { sha } from "./core.mjs";

const labels = [
  "ID.",
  "Surface.",
  "Depends on.",
  "Files.",
  "Build.",
  "Accept.",
  "You see.",
  "Verify, unit.",
  "Verify, live.",
  "Verify, perf.",
  "Review gate.",
  "Delivery.",
  "Merge.",
];
function evidencePaths(text) {
  return [
    ...text.matchAll(/\bEvidence\s*:\s*(?:`([^`\r\n]+)`|([^\s`]+))/gi),
  ].flatMap((match) => {
    const path = match[1] ?? match[2].replace(/[.,;]+$/, "");
    if (!path || /^(?:pass|when|none|n\/a|not|applicable)$/i.test(path))
      return [];
    if (!match[1] && !/[./\\]/.test(path)) return [];
    return [path];
  });
}
const outside = (root, destination) => {
  const rel = relative(root, destination);
  return (
    rel === ".." ||
    rel.startsWith(`..${process.platform === "win32" ? "\\" : "/"}`) ||
    isAbsolute(rel)
  );
};
export function parsePlan(raw) {
  const lines = raw.replace(/\r\n/g, "\n").split("\n"),
    problems = [],
    units = [],
    sections = [];
  let front = false,
    fence = null,
    section = null,
    block = null;
  if (lines[0] === "---") {
    front = true;
  }
  let title = false;
  for (let i = 0; i < lines.length; i++) {
    const text = lines[i],
      n = i + 1;
    if (front) {
      if (i > 0 && text === "---") front = false;
      continue;
    }
    const marker = /^\s{0,3}(`{3,}|~{3,})/.exec(text);
    if (marker) {
      if (!fence)
        fence = { char: marker[1][0], length: marker[1].length, line: n };
      else if (marker[1][0] === fence.char && marker[1].length >= fence.length)
        fence = null;
      continue;
    }
    if (fence) continue;
    if (/^#\s+\S/.test(text)) title = true;
    const h = /^##\s+(.+)$/.exec(text);
    if (h) {
      section = { title: h[1].trim(), line: n, body: [], blocks: new Map() };
      sections.push(section);
      block = null;
      continue;
    }
    if (section) section.body.push({ text, line: n });
    const b = /^\*\*([^*]+)\*\*\s*(.*)$/.exec(text);
    if (section && b && labels.includes(b[1])) {
      if (section.blocks.has(b[1]))
        problems.push({
          line: n,
          code: "DUPLICATE_BLOCK",
          message: `Duplicate ${b[1]}`,
        });
      block = { line: n, rows: [{ text: b[2], line: n }] };
      section.blocks.set(b[1], block);
    } else if (block) block.rows.push({ text, line: n });
  }
  if (front)
    problems.push({
      line: 1,
      code: "FRONTMATTER",
      message: "Unclosed frontmatter",
    });
  if (fence)
    problems.push({
      line: fence.line,
      code: "FENCE",
      message: "Unclosed code fence",
    });
  if (!title)
    problems.push({ line: 1, code: "TITLE", message: "Missing H1 title" });
  const hasSection = (re) => sections.some((s) => re.test(s.title));
  for (const [re, name] of [
    [/^(Inputs|How to read this)$/i, "Inputs or How to read this"],
    [/^(Phases|Program checklist)$/i, "Phases or Program checklist"],
    [/^(Close|Completion)( the program)?$/i, "Close or Completion"],
  ])
    if (!hasSection(re))
      problems.push({
        line: 1,
        code: "SECTION",
        message: `Missing ${name} section`,
      });
  for (const s of sections.filter((s) => s.blocks.size)) {
    const text = (label) =>
      s.blocks
        .get(label)
        ?.rows.map((r) => r.text)
        .join("\n")
        .trim() ?? "";
    const add = (code, message, label) =>
      problems.push({
        line: s.blocks.get(label)?.line ?? s.line,
        code,
        message: `${s.title}: ${message}`,
      });
    const id = text("ID.");
    if (!/^[a-zA-Z0-9][a-zA-Z0-9_.-]*$/.test(id))
      add("ID", "ID must be a stable identifier", "ID.");
    const surface = text("Surface.").toLowerCase();
    if (!["docs", "cli", "service", "ui", "mixed"].includes(surface))
      add(
        "SURFACE",
        "Surface must be docs, cli, service, ui or mixed",
        "Surface.",
      );
    for (const label of [
      "Depends on.",
      "Files.",
      "Build.",
      "Verify, unit.",
      "Verify, live.",
      "Verify, perf.",
      "Review gate.",
    ])
      if (!text(label)) add("BLOCK", `Missing ${label}`, label);
    if (!text("Accept.") && !text("You see."))
      add("ACCEPTANCE", "Missing observable Accept. or You see. predicate");
    if (!text("Delivery.") && !text("Merge."))
      add("DELIVERY", "Missing Delivery. or Merge. conditions");
    const depends = text("Depends on.").replace(/\.$/, "");
    const dependencies = /^none$/i.test(depends)
      ? []
      : depends.split(/\s*,\s*/).filter(Boolean);
    for (const label of ["Verify, unit.", "Verify, live.", "Verify, perf."]) {
      const content = text(label),
        na = /^(?:Not applicable|N\/A)\.\s+(.+)/i.exec(content);
      if (na) {
        if (na[1].trim().length < 12)
          add("RATIONALE", "Non-applicability needs a concrete reason", label);
        if (label === "Verify, live." && ["ui", "mixed"].includes(surface))
          add("UI_EVIDENCE", "Changed UI needs actual surface evidence", label);
        continue;
      }
      if (evidencePaths(content).length === 0)
        add("EVIDENCE", "Verification must name Evidence: destination", label);
      if (!/\bPass when\b/i.test(content))
        add("PREDICATE", "Verification must state Pass when", label);
      if (
        !/\b(?:Run|Exercise|Review|Check|Measure|Inspect|Validate)\b/i.test(
          content,
        )
      )
        add(
          "SCENARIO",
          "Verification needs a command or concrete scenario",
          label,
        );
    }
    if (
      /<[^>]+>|\b(?:TBD|TODO|FIXME)\b/.test(
        [...s.blocks.values()]
          .flatMap((b) => b.rows.map((r) => r.text))
          .join("\n"),
      )
    )
      add("PLACEHOLDER", "Unfilled placeholder");
    const evidence = [...s.blocks.values()]
      .flatMap((b) => b.rows)
      .flatMap((r) =>
        evidencePaths(r.text).map((path) => ({
          path,
          line: r.line,
        })),
      );
    units.push({
      id,
      surface,
      dependencies,
      title: s.title,
      line: s.line,
      boxes: s.body.filter((r) => /^\s*- \[[ xX]\]/.test(r.text)).length,
      evidence,
    });
  }
  if (!units.length)
    problems.push({
      line: 1,
      code: "UNITS",
      message: "No phase or work-unit sections",
    });
  const seen = new Set();
  for (const u of units) {
    if (seen.has(u.id))
      problems.push({
        line: u.line,
        code: "DUPLICATE_ID",
        message: `Duplicate ID ${u.id}`,
      });
    seen.add(u.id);
  }
  const byId = new Map(units.map((u) => [u.id, u])),
    visited = new Set(),
    active = new Set();
  const visit = (u) => {
    if (active.has(u.id)) {
      problems.push({
        line: u.line,
        code: "CYCLE",
        message: `Dependency cycle at ${u.id}`,
      });
      return;
    }
    if (visited.has(u.id)) return;
    active.add(u.id);
    for (const d of u.dependencies) {
      const dep = byId.get(d);
      if (!dep)
        problems.push({
          line: u.line,
          code: "DEPENDENCY",
          message: `Unknown dependency ${d}`,
        });
      else visit(dep);
    }
    active.delete(u.id);
    visited.add(u.id);
  };
  units.forEach(visit);
  return {
    schemaVersion: 1,
    valid: problems.length === 0,
    units,
    problems,
    meaning: "structural-plan-validation-only",
  };
}
export async function checkPlan(
  path,
  { verifyEvidence = false, root, head } = {},
) {
  const report = parsePlan(await readFile(path, "utf8"));
  if (head) sha(head);
  if (verifyEvidence) {
    const base = await realpath(resolve(root ?? "."));
    for (const item of report.units.flatMap((u) => u.evidence)) {
      if (/^https?:\/\//.test(item.path)) {
        report.problems.push({
          ...item,
          code: "REMOTE_UNVERIFIED",
          message: "Remote evidence was not fetched",
        });
        continue;
      }
      const destination = resolve(base, item.path);
      if (outside(base, destination)) {
        report.problems.push({
          ...item,
          code: "OUTSIDE_ROOT",
          message: "Evidence escapes supplied root",
        });
        continue;
      }
      try {
        const actual = await realpath(destination);
        if (outside(base, actual)) {
          report.problems.push({
            ...item,
            code: "OUTSIDE_ROOT",
            message: "Evidence symlink escapes supplied root",
          });
          continue;
        }
        if (!(await stat(actual)).isFile()) throw new Error("not a file");
      } catch {
        report.problems.push({
          ...item,
          code: "MISSING_EVIDENCE",
          message: "Evidence file does not exist",
        });
      }
    }
    if (head && !(await readFile(path, "utf8")).includes(head))
      report.problems.push({
        line: 1,
        code: "HEAD",
        message: "Plan does not identify the requested candidate head",
      });
  }
  report.valid = report.problems.length === 0;
  return report;
}
