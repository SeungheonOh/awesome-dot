// Offline plain-text consumer for the deliberately bounded grammar in README.md.
// No evaluation, HTML handling, filesystem writes, network calls, or link opening.
const own = (o, k) => Object.hasOwn(o, k);
const id = /^[A-Za-z_][A-Za-z0-9_]{0,63}$/;
const fail = (code, detail) => { throw new Error(`${code}: ${detail}`); };
const requireThat = (ok, code, detail) => { if (!ok) fail(code, detail); };
const object = (o) => o !== null && typeof o === 'object' && !Array.isArray(o);
const sortedKeys = (o) => Object.keys(o).sort();
const equalKeys = (a, b) => JSON.stringify(sortedKeys(a)) === JSON.stringify(sortedKeys(b));
function shape(value, required, optional = []) {
  requireThat(object(value), 'E_STRUCTURE', 'expected an object');
  requireThat(required.every(k => own(value, k)) &&
    Object.keys(value).every(k => required.includes(k) || optional.includes(k)),
    'E_STRUCTURE', `expected fields ${required.join(',')}`);
}

export function parseTemplate(text) {
  requireThat(typeof text === 'string' && text.length <= 4096, 'E_STRUCTURE', 'template must be a string of at most 4096 UTF-16 code units');
  const parts = [];
  let literal = '';
  const flush = () => { if (literal) parts.push({literal}); literal = ''; };
  for (let i = 0; i < text.length;) {
    if (text.startsWith('{{', i)) { literal += '{'; i += 2; }
    else if (text.startsWith('}}', i)) { literal += '}'; i += 2; }
    else if (text[i] === '{') {
      const end = text.indexOf('}', i + 1);
      const name = end === -1 ? '' : text.slice(i + 1, end);
      requireThat(id.test(name), 'E_GRAMMAR', `invalid argument at offset ${i}`);
      flush(); parts.push({argument: name}); i = end + 1;
    } else {
      requireThat(text[i] !== '}', 'E_GRAMMAR', `unescaped closing brace at offset ${i}`);
      literal += text[i++];
    }
  }
  flush();
  return parts;
}

function validateContract(c) {
  shape(c, ['version', 'sourceLocale', 'targetLocale', 'maximumCount', 'messages']);
  requireThat(c.version === 1 && c.sourceLocale === 'en-US' && c.targetLocale === 'fr-FR', 'E_STRUCTURE', 'this adapter supports version 1, en-US to fr-FR only');
  requireThat(Number.isSafeInteger(c.maximumCount) && c.maximumCount >= 0 && c.maximumCount <= 1000000,
    'E_STRUCTURE', 'maximumCount must be an integer from 0 to 1000000');
  requireThat(object(c.messages) && Object.keys(c.messages).length > 0, 'E_STRUCTURE', 'messages contract missing');
  for (const [key, rule] of Object.entries(c.messages)) {
    requireThat(id.test(key), 'E_STRUCTURE', `invalid key ${key}`);
    shape(rule, ['kind', 'arguments', 'occurrences', 'exact'], ['countArgument', 'maximumCodePoints']);
    requireThat(['text', 'plural'].includes(rule.kind) && object(rule.arguments) && object(rule.occurrences), 'E_STRUCTURE', `invalid rule ${key}`);
    requireThat(equalKeys(rule.arguments, rule.occurrences), 'E_STRUCTURE', `argument occurrence contract ${key}`);
    for (const [name, type] of Object.entries(rule.arguments)) {
      requireThat(id.test(name) && ['string', 'count'].includes(type) &&
        Number.isSafeInteger(rule.occurrences[name]) && rule.occurrences[name] >= 1,
        'E_STRUCTURE', `invalid argument rule ${key}.${name}`);
    }
    requireThat(Array.isArray(rule.exact) && rule.exact.every(x => typeof x === 'string' && x.length > 0) &&
      new Set(rule.exact).size === rule.exact.length, 'E_STRUCTURE', `invalid protected text ${key}`);
    if (rule.kind === 'plural') {
      requireThat(own(rule, 'countArgument') && typeof rule.countArgument === 'string' && id.test(rule.countArgument) && own(rule.arguments, rule.countArgument) &&
        rule.arguments[rule.countArgument] === 'count', 'E_STRUCTURE', `count selector ${key}`);
    } else requireThat(!own(rule, 'countArgument'), 'E_STRUCTURE', `unexpected selector ${key}`);
    if (own(rule, 'maximumCodePoints')) requireThat(rule.kind === 'text' && Object.keys(rule.arguments).length === 0 &&
      Number.isSafeInteger(rule.maximumCodePoints) && rule.maximumCodePoints >= 0,
      'E_STRUCTURE', `length budget requires static text ${key}`);
  }
}

function compileTemplate(text, rule, key) {
  const parts = parseTemplate(text);
  const occurrences = Object.create(null);
  for (const p of parts) if (own(p, 'argument')) occurrences[p.argument] = (occurrences[p.argument] ?? 0) + 1;
  requireThat(equalKeys(occurrences, rule.occurrences) &&
    Object.entries(rule.occurrences).every(([k, v]) => occurrences[k] === v), 'E_PLACEHOLDER', key);
  for (const exact of rule.exact) requireThat(text.split(exact).length - 1 === 1, 'E_EXACT', `${key} must contain the protected literal once`);
  if (own(rule, 'maximumCodePoints')) requireThat([...text].length <= rule.maximumCodePoints, 'E_LENGTH', key);
  return parts;
}

function compileBundle(bundle, contract, locale, complete) {
  shape(bundle, ['version', 'locale', 'messages']);
  requireThat(bundle.version === 1 && bundle.locale === locale, 'E_LOCALE', `expected ${locale}`);
  requireThat(object(bundle.messages), 'E_STRUCTURE', 'messages must be an object');
  requireThat(Object.keys(bundle.messages).every(k => own(contract.messages, k)), 'E_KEY', 'unknown resource key');
  if (complete) requireThat(equalKeys(bundle.messages, contract.messages), 'E_KEY', `incomplete ${locale} bundle`);
  requireThat(Intl.PluralRules.supportedLocalesOf([locale]).length === 1, 'E_LOCALE', `runtime lacks ${locale}`);
  const plural = new Intl.PluralRules(locale, {type: 'cardinal'});
  const categories = plural.resolvedOptions().pluralCategories;
  const messages = new Map();
  for (const [key, entry] of Object.entries(bundle.messages)) {
    const rule = contract.messages[key];
    requireThat(entry?.kind === rule.kind, 'E_STRUCTURE', `wrong kind ${key}`);
    if (rule.kind === 'text') {
      shape(entry, ['kind', 'value']);
      messages.set(key, {parts: compileTemplate(entry.value, rule, key)});
    } else {
      shape(entry, ['kind', 'countArgument', 'forms']);
      requireThat(entry.countArgument === rule.countArgument && object(entry.forms), 'E_STRUCTURE', `invalid plural ${key}`);
      requireThat(Object.keys(entry.forms).every(k => categories.includes(k)), 'E_BRANCH', `unexpected category ${key}`);
      if (complete) requireThat(categories.every(k => own(entry.forms, k)), 'E_BRANCH', `missing category ${key} (${categories.join(',')})`);
      const forms = new Map(Object.entries(entry.forms).map(([form, text]) => [form, compileTemplate(text, rule, `${key}.${form}`)]));
      messages.set(key, {forms});
    }
  }
  return {locale, plural, messages};
}

export function createConsumer(source, target, suppliedContract, options = {}) {
  requireThat(object(options), 'E_OPTIONS', 'options must be an object');
  const allowIncompleteTarget = own(options, 'allowIncompleteTarget') ? options.allowIncompleteTarget : false;
  requireThat(typeof allowIncompleteTarget === 'boolean', 'E_OPTIONS', 'allowIncompleteTarget must be a boolean when supplied');
  // Snapshot the contract so a caller's later mutation cannot change a compiled release.
  const contract = structuredClone(suppliedContract);
  validateContract(contract);
  const en = compileBundle(source, contract, contract.sourceLocale, true);
  const fr = compileBundle(target, contract, contract.targetLocale, !allowIncompleteTarget);
  function render(requestedLocale, key, args = {}) {
    requireThat(typeof requestedLocale === 'string', 'E_LOCALE', 'requested locale must be a string');
    requireThat(own(contract.messages, key), 'E_KEY', `unknown message ${key}`);
    const rule = contract.messages[key];
    requireThat(object(args) && equalKeys(args, rule.arguments), 'E_ARGUMENTS', key);
    for (const [name, type] of Object.entries(rule.arguments)) {
      const value = args[name];
      if (type === 'count') requireThat(Number.isSafeInteger(value) && value >= 0 && value <= contract.maximumCount,
        'E_COUNT', `${name} must be an integer from 0 to ${contract.maximumCount}`);
      else requireThat(typeof value === 'string' && [...value].length <= 200, 'E_ARGUMENTS', `${name} must be a string of at most 200 code points`);
    }
    let selected = requestedLocale === fr.locale ? fr : en;
    let fallback = requestedLocale === fr.locale || requestedLocale === en.locale ? null : 'missing-bundle';
    let category = rule.kind === 'plural' ? selected.plural.select(args[rule.countArgument]) : null;
    let entry = selected.messages.get(key);
    if (selected === fr && (!entry || (rule.kind === 'plural' && !entry.forms.has(category)))) {
      fallback = !entry ? 'missing-key' : 'missing-branch';
      selected = en;
      category = rule.kind === 'plural' ? en.plural.select(args[rule.countArgument]) : null;
      entry = en.messages.get(key);
    }
    const parts = rule.kind === 'plural' ? entry.forms.get(category) : entry.parts;
    const text = parts.map(p => own(p, 'literal') ? p.literal : String(args[p.argument])).join('');
    return {key, requestedLocale, usedLocale: selected.locale, category, fallback, releaseBlockers: fallback ? ['fallback-used'] : [], text};
  }
  return {render, localeOptions: {source: en.plural.resolvedOptions(), target: fr.plural.resolvedOptions()}};
}
