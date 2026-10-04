import { mkdir, readFile, open } from "node:fs/promises";
import { dirname, resolve, basename } from "node:path";
import { createHash } from "node:crypto";
import { regular, withLock } from "./atomic-store.mjs";
import { fail, cell } from "./core.mjs";

export const LOG_HEADER = "ts\tphase\tdecision\twhy\tevidence\tresult";
export async function appendDecision(
  file,
  fields,
  { now = () => new Date().toISOString(), run = null } = {},
) {
  fail(
    Array.isArray(fields) && fields.length === 5,
    "log requires FILE PHASE DECISION WHY EVIDENCE RESULT",
  );
  const path = resolve(file),
    directory = dirname(path);
  await mkdir(directory, { recursive: true });
  const lockName = `.log-${createHash("sha256").update(basename(path)).digest("hex").slice(0, 16)}.lock`;
  return withLock(
    directory,
    async () => {
      let raw = "";
      if (await regular(path, true)) raw = await readFile(path, "utf8");
      if (raw) {
        fail(
          raw.split(/\r?\n/, 1)[0] === LOG_HEADER,
          "Existing decision log has the wrong header",
          "CORRUPT",
        );
        fail(
          raw.endsWith("\n"),
          "Existing log ends in a partial row; preserve it and repair explicitly",
          "CORRUPT",
        );
        for (const line of raw.split(/\r?\n/).slice(1).filter(Boolean))
          fail(
            line.split("\t").length === 6,
            "Existing log contains malformed row",
            "CORRUPT",
          );
      }
      const ts = now();
      fail(
        !/[\t\r\n]/.test(ts) && Number.isFinite(Date.parse(ts)),
        "Invalid log timestamp",
      );
      const rows = [];
      if (run) {
        const starts = raw
          .split(/\r?\n/)
          .filter((l) => l.split("\t")[1] === "start");
        const last = starts.at(-1)?.split("\t")[4];
        if (last !== cell(run))
          rows.push([
            ts,
            "start",
            "began or resumed this run",
            "separate provenance from earlier entries",
            run,
            raw ? "prior rows retained" : "new log",
          ]);
      }
      rows.push([ts, ...fields]);
      const addition =
        (raw ? "" : LOG_HEADER + "\n") +
        rows.map((r) => r.map(cell).join("\t")).join("\n") +
        "\n";
      const h = await open(path, "a", 0o600);
      try {
        await h.writeFile(addition);
        await h.sync();
      } finally {
        await h.close();
      }
      return {
        file: path,
        timestamp: ts,
        appendedRows: rows.length,
        historyRewritten: false,
      };
    },
    { name: lockName },
  );
}
