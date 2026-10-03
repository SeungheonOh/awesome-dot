import { randomUUID } from "node:crypto";
import { hostname } from "node:os";
import { resolve, join, dirname, basename } from "node:path";
import {
  mkdir,
  lstat,
  open,
  readFile,
  rename,
  unlink,
  rm,
} from "node:fs/promises";
import { ToolError, fail, record } from "./core.mjs";

export async function regular(path, optional = false) {
  try {
    const s = await lstat(path);
    fail(
      s.isFile() && !s.isSymbolicLink(),
      `Expected regular file: ${path}`,
      "UNSAFE_PATH",
    );
    return s;
  } catch (error) {
    if (optional && error.code === "ENOENT") return null;
    throw error;
  }
}
export async function atomicWrite(
  path,
  text,
  { beforeRename, afterRename } = {},
) {
  const stat = await regular(path, true);
  const temp = join(dirname(path), `.${basename(path)}.${randomUUID()}.tmp`);
  let handle;
  try {
    handle = await open(temp, "wx", stat ? stat.mode & 0o777 : 0o600);
    await handle.writeFile(text, "utf8");
    await handle.sync();
    await handle.close();
    handle = undefined;
    await beforeRename?.(temp, path);
    await rename(temp, path);
    await afterRename?.(path);
    try {
      const directory = await open(dirname(path), "r");
      try {
        await directory.sync();
      } finally {
        await directory.close();
      }
    } catch (error) {
      if (!["EINVAL", "EISDIR", "EPERM", "ENOTSUP"].includes(error.code))
        throw error;
    }
  } finally {
    await handle?.close();
    await rm(temp, { force: true });
  }
}

export async function withLock(
  directory,
  operation,
  { name = ".writer.lock", waitMs = 5000 } = {},
) {
  const lock = join(directory, name),
    token = randomUUID();
  const owner = {
    schemaVersion: 1,
    token,
    pid: process.pid,
    host: hostname(),
    createdAt: new Date().toISOString(),
  };
  const until = Date.now() + waitMs;
  let handle;
  while (!handle) {
    try {
      handle = await open(lock, "wx", 0o600);
    } catch (error) {
      if (error.code !== "EEXIST") throw error;
      if (Date.now() >= until)
        throw new ToolError(
          `Writer lock exists at ${lock}; inspect it and recover only after all writers stop`,
          "LOCKED",
        );
      await new Promise((r) => setTimeout(r, 15));
    }
  }
  try {
    await handle.writeFile(JSON.stringify(owner));
    await handle.sync();
  } catch (error) {
    const ownStat = await handle.stat();
    const current = await lstat(lock);
    if (current.ino === ownStat.ino && current.dev === ownStat.dev)
      await unlink(lock);
    throw error;
  } finally {
    await handle.close();
  }
  try {
    return await operation();
  } finally {
    try {
      await regular(lock);
      const current = JSON.parse(await readFile(lock, "utf8"));
      if (current.token === token) await unlink(lock);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
}

export async function recoverLock(directory, expectedToken) {
  // Deliberately no --force. Recovery is a quiescent local operation.
  const rootInfo = await lstat(resolve(directory));
  fail(
    rootInfo.isDirectory() && !rootInfo.isSymbolicLink(),
    "Store directory cannot be a symlink or non-directory",
    "UNSAFE_PATH",
  );
  const path = join(resolve(directory), ".writer.lock");
  return withLock(
    resolve(directory),
    async () => {
      await regular(path);
      const raw = await readFile(path, "utf8"),
        owner = JSON.parse(raw);
      fail(
        record(owner) &&
          owner.token === expectedToken &&
          owner.host === hostname() &&
          Number.isSafeInteger(owner.pid),
        "Lock identity/host is not proven",
        "LOCKED",
      );
      let dead = false;
      try {
        process.kill(owner.pid, 0);
      } catch (error) {
        dead = error.code === "ESRCH";
      }
      fail(
        dead,
        "Lock holder is alive or its death cannot be proven",
        "LOCKED",
      );
      fail(
        (await readFile(path, "utf8")) === raw,
        "Lock changed during recovery",
        "LOCKED",
      );
      const quarantine = `${path}.recovered-${randomUUID()}`;
      await rename(path, quarantine);
      return { recovered: true, quarantine, owner };
    },
    { name: ".recovery.lock", waitMs: 0 },
  );
}

export class JsonStore {
  constructor(
    directory,
    validate,
    initial,
    { now = () => new Date().toISOString(), lockWaitMs = 5000 } = {},
  ) {
    this.directory = resolve(directory);
    this.path = join(this.directory, "state.json");
    this.validate = validate;
    this.initial = initial;
    this.now = now;
    this.lockWaitMs = lockWaitMs;
    this.closed = false;
    this.queue = Promise.resolve();
  }
  ensureOpen() {
    fail(!this.closed, "Store is closed", "CLOSED");
  }
  async ensureDirectory() {
    const info = await lstat(this.directory);
    fail(
      info.isDirectory() && !info.isSymbolicLink(),
      "Store directory cannot be a symlink or non-directory",
      "UNSAFE_PATH",
    );
  }
  async init() {
    this.ensureOpen();
    await mkdir(this.directory, { recursive: true });
    fail(
      !(await lstat(this.directory)).isSymbolicLink(),
      "Store directory cannot be a symlink",
      "UNSAFE_PATH",
    );
    await withLock(this.directory, async () => {
      if (await regular(this.path, true)) await this.read();
      else {
        const state = this.initial(this.now());
        this.validate(state);
        await atomicWrite(this.path, `${JSON.stringify(state, null, 2)}\n`);
      }
    });
    return { store: this.directory };
  }
  async read() {
    this.ensureOpen();
    try {
      await this.ensureDirectory();
      await regular(this.path);
      const state = JSON.parse(await readFile(this.path, "utf8"));
      this.validate(state);
      return state;
    } catch (error) {
      if (error.code === "ENOENT")
        throw new ToolError(
          `Store is not initialized: ${this.directory}; run orch init`,
          "UNINITIALIZED",
        );
      if (error instanceof SyntaxError)
        throw new ToolError("state.json is malformed JSON", "CORRUPT");
      throw error;
    }
  }
  transact(operation, expectedRevision, { afterCommit } = {}) {
    const transaction = async () => {
      this.ensureOpen();
      await this.ensureDirectory();
      return withLock(
        this.directory,
        async () => {
          // A recovery operation is only valid with quiescent writers; never enter while it is running.
          fail(
            !(await regular(join(this.directory, ".recovery.lock"), true)),
            "Lock recovery in progress",
            "LOCKED",
          );
          const state = await this.read();
          fail(
            expectedRevision === undefined ||
              expectedRevision === state.revision,
            "State revision changed; re-read before retrying",
            "STALE",
          );
          const result = await operation(state);
          state.revision += 1;
          state.updatedAt = this.now();
          this.validate(state);
          await atomicWrite(this.path, `${JSON.stringify(state, null, 2)}\n`);
          await afterCommit?.(result, state);
          return structuredClone(result);
        },
        { waitMs: this.lockWaitMs },
      );
    };
    const result = this.queue.then(transaction, transaction);
    this.queue = result.catch(() => {});
    return result;
  }
  withSnapshot(operation) {
    const lockedRead = async () => {
      this.ensureOpen();
      await this.ensureDirectory();
      return withLock(
        this.directory,
        async () => operation(await this.read()),
        { waitMs: this.lockWaitMs },
      );
    };
    const result = this.queue.then(lockedRead, lockedRead);
    this.queue = result.catch(() => {});
    return result;
  }
  async close() {
    await this.queue;
    this.closed = true;
  }
}
