'use strict';

const registry = new Map();

function register(name, value) {
  if (typeof name !== 'string' || name.length === 0) {
    throw new TypeError('name must be a nonempty string');
  }
  registry.set(name, value);
  return value;
}

function lookup(name) { return registry.get(name); }
function names() { return [...registry.keys()].sort(); }

module.exports = { register, lookup, names };
