// Both public entry points delegate to the same cached CommonJS core.
import core from './core.cjs';
export const { register, lookup, names } = core;
