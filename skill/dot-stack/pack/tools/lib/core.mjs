import { spawn } from "node:child_process";
import { parseArgs } from "node:util";
import { setTimeout as delay } from "node:timers/promises";

export class ToolError extends Error {
  constructor(message, code = "INVALID", exitCode = 1, detail = undefined) {
    super(message);
    this.name = "ToolError";
    this.code = code;
    this.exitCode = exitCode;
    this.detail = detail;
  }
}
export const fail = (condition, message, code = "INVALID", exitCode = 1) => {
  if (!condition) throw new ToolError(message, code, exitCode);
};
export const record = (value) =>
  value !== null && typeof value === "object" && !Array.isArray(value);
export function nonempty(value, label) {
  fail(
    typeof value === "string" && value.trim() !== "" && !/[\r\n\0]/.test(value),
    `${label} must be a nonempty single line`,
  );
  return value;
}
export function positive(value, label = "number") {
  fail(
    /^[1-9]\d*$/.test(String(value)) && Number.isSafeInteger(Number(value)),
    `${label} must be a positive safe integer`,
  );
  return Number(value);
}
export const prNumber = (value) => positive(value, "PR number");
export function sha(value, label = "SHA") {
  fail(
    typeof value === "string" && /^(?:[a-f0-9]{40}|[a-f0-9]{64})$/i.test(value),
    `${label} must be a full 40- or 64-digit commit SHA`,
  );
  return value.toLowerCase();
}
export const cell = (value) => {
  const text = String(value ?? "").replace(/[\t\n\r]/g, " ");
  return /^[\s\x00-\x1f]*[=+\-@]/.test(text)
    ? `'${text}`
    : text.replace(/\0/g, "");
};
export const markdown = (value) =>
  String(value ?? "")
    .replace(/\\/g, "\\\\")
    .replace(/\|/g, "\\|")
    .replace(/[\r\n]/g, " ");
export const realClock = {
  now: () => performance.now() / 1000,
  observedAt: () => new Date().toISOString(),
  sleep: (seconds, signal) => delay(seconds * 1000, undefined, { signal }),
};
export function options(args, specification) {
  try {
    return parseArgs({
      args,
      options: specification,
      allowPositionals: true,
      strict: true,
    });
  } catch (error) {
    throw new ToolError(error.message, "USAGE", 64);
  }
}
export function errorObject(error) {
  return {
    code: error.code ?? "INTERNAL",
    message: error.message,
    ...(error.detail === undefined ? {} : { detail: error.detail }),
  };
}
export function redact(text) {
  return String(text)
    .replace(/(https?:\/\/)[^/@\s]+:[^/@\s]+@/g, "$1[redacted]@")
    .replace(
      /((?:token|secret|password|authorization)[=: ]+)\S+/gi,
      "$1[redacted]",
    )
    .slice(0, 500);
}

/** Bounded process read. Callers pass argv as data, never shell fragments. */
export function runCommand(
  executable,
  args,
  {
    cwd,
    timeoutMs = 30000,
    maxBytes = 8 * 1024 * 1024,
    signal,
    env = process.env,
  } = {},
) {
  return new Promise((resolve, reject) => {
    if (signal?.aborted)
      return reject(new ToolError("Operation cancelled", "CANCELLED", 130));
    let child;
    try {
      child = spawn(executable, args, {
        cwd,
        env,
        shell: false,
        stdio: ["ignore", "pipe", "pipe"],
      });
    } catch (error) {
      return reject(
        new ToolError(
          `Cannot start ${executable}: ${redact(error.message)}`,
          "COMMAND",
          7,
        ),
      );
    }
    let stdout = "",
      stderr = "",
      bytes = 0,
      failure,
      killTimer;
    const stop = (error) => {
      failure ??= error;
      child.kill("SIGTERM");
      killTimer ??= setTimeout(() => child.kill("SIGKILL"), 250);
    };
    const timer = setTimeout(
      () =>
        stop(
          new ToolError(
            `${executable} exceeded ${timeoutMs}ms`,
            "COMMAND_TIMEOUT",
            7,
          ),
        ),
      timeoutMs,
    );
    const abort = () =>
      stop(new ToolError("Operation cancelled", "CANCELLED", 130));
    signal?.addEventListener("abort", abort, { once: true });
    const consume = (stream) => (chunk) => {
      bytes += Buffer.byteLength(chunk);
      if (bytes > maxBytes)
        stop(
          new ToolError(
            `${executable} exceeded output limit`,
            "OUTPUT_LIMIT",
            7,
          ),
        );
      else if (stream === "out") stdout += chunk;
      else stderr += chunk;
    };
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", consume("out"));
    child.stderr.on("data", consume("err"));
    child.once("error", (error) => {
      failure = new ToolError(
        `Cannot start ${executable}: ${redact(error.message)}`,
        error.code === "ENOENT" ? "MISSING_TOOL" : "COMMAND",
        7,
      );
    });
    child.once("close", (code, termSignal) => {
      clearTimeout(timer);
      clearTimeout(killTimer);
      signal?.removeEventListener("abort", abort);
      if (failure) reject(failure);
      else resolve({ code: code ?? -1, stdout, stderr, signal: termSignal });
    });
  });
}

export function assertReadCommand(executable, args) {
  const git = new Set([
    "rev-parse",
    "remote",
    "worktree",
    "status",
    "log",
    "merge-base",
    "symbolic-ref",
    "show-ref",
    "rev-list",
    "for-each-ref",
    "show",
    "diff",
  ]);
  if (executable === "git") {
    const offset = args[0] === "-C" ? 2 : 0;
    fail(
      git.has(args[offset]),
      "Git command is outside the read-only capability",
      "READ_ONLY",
    );
    if (args[offset] === "remote")
      fail(
        args[offset + 1] === "get-url",
        "Only remote get-url is allowed",
        "READ_ONLY",
      );
    if (args[offset] === "worktree")
      fail(
        args[offset + 1] === "list",
        "Only worktree list is allowed",
        "READ_ONLY",
      );
  } else if (executable === "gh") {
    const prRead =
      args[0] === "pr" && ["view", "list", "checks"].includes(args[1]);
    const query =
      args[0] === "api" &&
      args[1] === "graphql" &&
      args.some((a) => a.startsWith("query=query "));
    fail(
      prRead || query,
      "GitHub command is outside the read-only capability",
      "READ_ONLY",
    );
    fail(
      !args.some((a) => /\bmutation\s*[({]/.test(a)),
      "Mutation queries are forbidden",
      "READ_ONLY",
    );
  } else fail(false, "Unknown read executable", "READ_ONLY");
}
export const readRunner = (runner) => (exe, args, config) => {
  assertReadCommand(exe, args);
  return runner(exe, args, {
    ...config,
    env: {
      ...process.env,
      ...config?.env,
      GIT_OPTIONAL_LOCKS: "0",
      GIT_TERMINAL_PROMPT: "0",
      GH_PROMPT_DISABLED: "1",
    },
  });
};
