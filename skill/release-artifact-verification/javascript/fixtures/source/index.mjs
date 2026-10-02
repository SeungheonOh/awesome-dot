// Deliberate defect: this entry allocates a second registry.
const registry = new Map();

export function register(name, value) {
  if (typeof name !== 'string' || name.length === 0) {
    throw new TypeError('name must be a nonempty string');
  }
  registry.set(name, value);
  return value;
}

export function lookup(name) { return registry.get(name); }
export function names() { return [...registry.keys()].sort(); }
