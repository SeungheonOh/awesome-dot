// Run a copied instance in a fresh consumer project, never in the fixture tree.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { lstatSync, readFileSync, realpathSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const name = 'switchboard-registry-demo';
const require = createRequire(import.meta.url);
const mode = process.argv[2];
const seed = process.argv[3] ?? 'render';
assert(['import-only', 'require-only', 'import-first', 'require-first', 'absent'].includes(mode));
assert(seed.length > 0 && seed.length <= 80);
assert.equal(process.env.NODE_PATH, undefined);
assert.equal(process.env.NODE_OPTIONS, undefined);
const cwd = realpathSync(process.cwd());
assert.equal(realpathSync(dirname(fileURLToPath(import.meta.url))), cwd);

if (mode === 'absent') {
  for (const resolver of [() => require.resolve(name), () => import.meta.resolve(name)]) {
    assert.throws(resolver, (error) => ['MODULE_NOT_FOUND', 'ERR_MODULE_NOT_FOUND'].includes(error.code));
  }
  console.log(JSON.stringify({ mode, absent_from_both_resolvers: true }));
} else {
  const packageRoot = join(cwd, 'node_modules', name);
  assert(!lstatSync(packageRoot).isSymbolicLink());
  assert.equal(realpathSync(packageRoot), packageRoot);
  const resolved = {
    import: fileURLToPath(import.meta.resolve(name)),
    require: require.resolve(name),
  };
  const provenance = {};
  for (const [condition, file] of Object.entries(resolved)) {
    assert.equal(file, join(packageRoot, condition === 'import' ? 'index.mjs' : 'index.cjs'));
    assert.equal(realpathSync(file), file);
    assert(lstatSync(file).isFile() && !lstatSync(file).isSymbolicLink());
    provenance[condition] = {
      resolved_relative_to_consumer: relative(cwd, file),
      sha256: createHash('sha256').update(readFileSync(file)).digest('hex'),
    };
  }
  const loadOrder = [];
  async function load(condition) {
    loadOrder.push(condition);
    return condition === 'import' ? await import(name) : require(name);
  }
  const firstCondition = mode.startsWith('import') ? 'import' : 'require';
  const first = await load(firstCondition);
  const mixed = mode.endsWith('first');
  const second = mixed ? await load(firstCondition === 'import' ? 'require' : 'import') : first;
  const checks = {};
  checks.public_functions = [first, second].every(api =>
    ['register', 'lookup', 'names'].every(key => typeof api[key] === 'function'));
  checks.initially_empty = first.names().length === 0 && second.names().length === 0;
  const keyA = `${seed}:z`;
  const keyB = `${seed}:a`;
  const firstValue = { handler: 'render', count: 1 };
  const secondValue = { handler: 'audit', count: 2 };
  const replacement = { handler: 'render-v2', count: 3 };
  checks.first_local_roundtrip = first.register(keyA, firstValue) === firstValue
    && first.lookup(keyA) === firstValue;
  checks.first_write_visible_to_second = second.lookup(keyA) === firstValue;
  checks.second_local_roundtrip = second.register(keyB, secondValue) === secondValue
    && second.lookup(keyB) === secondValue;
  checks.second_write_visible_to_first = first.lookup(keyB) === secondValue;
  second.register(keyA, replacement);
  checks.replacement_visible_to_first = first.lookup(keyA) === replacement;
  const expectedNames = [keyA, keyB].sort();
  checks.names_agree = JSON.stringify(first.names()) === JSON.stringify(expectedNames)
    && JSON.stringify(second.names()) === JSON.stringify(expectedNames);
  checks.missing_is_undefined = first.lookup(`${seed}:missing`) === undefined
    && second.lookup(`${seed}:missing`) === undefined;
  checks.rejects_invalid_name = [first, second].every(api => ['', 0].every(invalid => {
    try { api.register(invalid, 0); return false; }
    catch (error) { return error instanceof TypeError && error.message === 'name must be a nonempty string'; }
  }));
  const contractPass = Object.values(checks).every(Boolean);
  console.log(JSON.stringify({
    mode, seed, load_order: loadOrder, provenance, checks,
    observed_names: { first: first.names(), second: second.names() },
    contract_pass: contractPass,
  }));
  process.exitCode = contractPass ? 0 : 1;
}
