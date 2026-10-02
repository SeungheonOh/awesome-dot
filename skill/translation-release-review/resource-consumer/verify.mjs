// Execute against saved files; write a new, uniquely named results directory only.
import assert from 'node:assert/strict';
import {readFileSync, mkdirSync, writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {join} from 'node:path';
import {createConsumer, parseTemplate} from './consumer.mjs';

const base = fileURLToPath(new URL('.', import.meta.url));
const outputName = process.argv[2];
assert.match(outputName ?? '', /^[a-z][a-z0-9-]{0,63}$/, 'supply a new output directory name, e.g. run-local-1');
const output = join(base, outputName);
mkdirSync(output); // EEXIST is intentional: no overwrite or append to previous evidence.
const files = ['source.en-US.json', 'target.fr-FR.json', 'contract.json', 'consumer.mjs', 'verify.mjs', 'json-preflight.py'];
const raw = Object.fromEntries(files.map(f => [f, readFileSync(join(base, f))]));
const digest = b => createHash('sha256').update(b).digest('hex');
const hashes = Object.fromEntries(files.map(f => [f, digest(raw[f])]));
const readJson = name => JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(raw[name]));
const source = readJson('source.en-US.json');
const target = readJson('target.fr-FR.json');
const contract = readJson('contract.json');
const consumer = createConsumer(source, target, contract);
const copy = o => structuredClone(o);
const controls = [];
const outputs = [];
const record = (id, got) => { outputs.push({id, ...got}); return got; };
function rejects(id, fn, code) {
  assert.throws(fn, error => error.message.startsWith(code + ':'), id);
  controls.push({id, result: 'rejected', code});
}
function changedTarget(fn) { const t = copy(target); fn(t); return t; }
function rejectedTarget(id, fn, code) {
  rejects(id, () => createConsumer(source, changedTarget(fn), contract), code);
}

// Literal expected sentences are independently written examples, not derived from templates.
const expected = {
  'en-US': {0:'0 drafts in Ideas.', 1:'1 draft in Ideas.', 2:'2 drafts in Ideas.', 21:'21 drafts in Ideas.', 1000000:'1000000 drafts in Ideas.'},
  'fr-FR': {0:'0 brouillon dans Idées.', 1:'1 brouillon dans Idées.', 2:'2 brouillons dans Idées.', 21:'21 brouillons dans Idées.', 1000000:'1000000 brouillons dans Idées.'}
};
const selected = {'en-US': ['other','one','other','other','other'], 'fr-FR': ['one','one','other','other','many']};
for (const locale of ['en-US','fr-FR']) {
  [0,1,2,21,1000000].forEach((count, index) => {
    const got = record(`${locale}-drafts-${count}`, consumer.render(locale, 'drafts', {count, folder:locale === 'fr-FR' ? 'Idées' : 'Ideas'}));
    assert.equal(got.text, expected[locale][count]);
    assert.equal(got.category, selected[locale][index]);
    assert.equal(got.fallback, null);
    assert.deepEqual(got.releaseBlockers, []);
  });
}
const calls = [
  ['welcome', {name:'Anaïs'}, 'Bienvenue dans Brume Notes, Anaïs.'],
  ['saveWarning', {file:'carnet.txt'}, 'Ne fermez pas Brume Notes pendant l’enregistrement de carnet.txt. Ne réessayez pas, sauf si une erreur s’affiche.'],
  ['closeWarning', {}, 'Ne fermez pas.'],
  ['help', {}, 'Aide pour Brume Notes : https://help.brume.invalid/guide?lang=en&topic=drafts'],
  ['entryHint', {label:'Idées'}, 'Saisissez « Idées ».\nDossier : C:\\Brume\\Drafts'],
  ['patternHint', {value:'{count} & <nom>'}, 'Modèle : {draft} ; valeur : {count} & <nom>.']
];
for (const [key, args, text] of calls) {
  const got = record(`fr-FR-${key}`, consumer.render('fr-FR',key,args));
  assert.equal(got.text,text);
  assert.equal(got.fallback,null);
  assert.deepEqual(got.releaseBlockers, []);
}
assert.deepEqual(parseTemplate('A {{x}} {name} }}'), [{literal:'A {x} '},{argument:'name'},{literal:' }'}]);
assert.throws(() => JSON.parse(String.raw`{"x":"\q"}`), SyntaxError);
controls.push({id:'malformed-json-escape', result:'rejected', code:'SyntaxError'});
rejectedTarget('wrong-resource-kind', t => {t.messages.welcome.kind='plural';}, 'E_STRUCTURE');
rejectedTarget('unknown-schema-field', t => {t.messages.welcome.note='extra';}, 'E_STRUCTURE');
rejectedTarget('placeholder-case-change', t => {t.messages.welcome.value=t.messages.welcome.value.replace('{name}','{Name}');}, 'E_PLACEHOLDER');
rejectedTarget('missing-placeholder', t => {t.messages.welcome.value=t.messages.welcome.value.replace('{name}','Anaïs');}, 'E_PLACEHOLDER');
rejectedTarget('duplicate-placeholder', t => {t.messages.welcome.value += ' {name}';}, 'E_PLACEHOLDER');
rejectedTarget('malformed-opening-brace', t => {t.messages.welcome.value=t.messages.welcome.value.replace('{name}','{name');}, 'E_GRAMMAR');
rejectedTarget('malformed-closing-brace', t => {t.messages.welcome.value += '}';}, 'E_GRAMMAR');
rejectedTarget('unsupported-icu-expression', t => {t.messages.welcome.value='{count, plural, one {one} other {other}}';}, 'E_GRAMMAR');
rejectedTarget('url-language-change', t => {t.messages.help.value=t.messages.help.value.replace('lang=en','lang=fr');}, 'E_EXACT');
rejectedTarget('product-token-change', t => {t.messages.welcome.value=t.messages.welcome.value.replace('Brume Notes','Notes Brume');}, 'E_EXACT');
rejectedTarget('missing-many-release', t => {delete t.messages.drafts.forms.many;}, 'E_BRANCH');
rejectedTarget('missing-other-release', t => {delete t.messages.drafts.forms.other;}, 'E_BRANCH');
rejectedTarget('missing-key-release', t => {delete t.messages.drafts;}, 'E_KEY');
rejectedTarget('unexpected-plural-category', t => {t.messages.drafts.forms.two=t.messages.drafts.forms.other;}, 'E_BRANCH');
rejectedTarget('short-warning-too-long', t => {t.messages.closeWarning.value='Ne fermez pas ! !';}, 'E_LENGTH');
for (const [name, count] of [['negative',-1],['fraction',0.5],['not-finite',Infinity],['not-a-number',NaN],['numeric-string','2'],['above-bound',1000001]]) {
  rejects(`count-${name}`, () => consumer.render('fr-FR','drafts',{count,folder:'Idées'}), 'E_COUNT');
}
rejects('missing-call-argument', () => consumer.render('fr-FR','welcome',{}), 'E_ARGUMENTS');
rejects('extra-call-argument', () => consumer.render('fr-FR','welcome',{name:'Anaïs',other:'x'}), 'E_ARGUMENTS');
rejects('wrong-call-type', () => consumer.render('fr-FR','welcome',{name:2}), 'E_ARGUMENTS');
rejects('unknown-message-key', () => consumer.render('fr-FR','missing',{}), 'E_KEY');
const brokenSource=copy(source); delete brokenSource.messages.drafts;
rejects('incomplete-source-cannot-fallback', () => createConsumer(brokenSource,target,contract,{allowIncompleteTarget:true}), 'E_KEY');
const malformedTarget=changedTarget(t => {t.messages.welcome.value='{name';});
rejects('malformed-target-cannot-fallback', () => createConsumer(source,malformedTarget,contract,{allowIncompleteTarget:true}), 'E_GRAMMAR');

// Recovery is observable and does not convert a failed release gate into a pass.
const noMany=changedTarget(t => {delete t.messages.drafts.forms.many;});
for (const [name, value] of [['string-false','false'],['null',null],['number',0],['undefined',undefined]]) {
  rejects(`invalid-fallback-option-${name}`, () => createConsumer(source,noMany,contract,{allowIncompleteTarget:value}), 'E_OPTIONS');
}
rejects('explicit-false-keeps-strict-gate', () => createConsumer(source,noMany,contract,{allowIncompleteTarget:false}), 'E_BRANCH');
assert.equal(createConsumer(source,target,contract,{allowIncompleteTarget:false}).render('fr-FR','drafts',{count:2,folder:'Idées'}).text,'2 brouillons dans Idées.');
controls.push({id:'explicit-false-complete-target',result:'accepted',code:'complete target compiled with strict gate enabled'});
const recovery=createConsumer(source,noMany,contract,{allowIncompleteTarget:true});
let got=record('missing-many-recovery',recovery.render('fr-FR','drafts',{count:1000000,folder:'Idées'}));
assert.deepEqual(got.releaseBlockers, ['fallback-used']);
assert.deepEqual([got.usedLocale,got.category,got.fallback,got.text], ['en-US','other','missing-branch','1000000 drafts in Idées.']);
const noKey=changedTarget(t => {delete t.messages.drafts;});
got=record('missing-key-recovery-zero',createConsumer(source,noKey,contract,{allowIncompleteTarget:true}).render('fr-FR','drafts',{count:0,folder:'Idées'}));
assert.deepEqual(got.releaseBlockers, ['fallback-used']);
assert.deepEqual([got.usedLocale,got.category,got.fallback,got.text], ['en-US','other','missing-key','0 drafts in Idées.']);
got=record('missing-bundle-fr-CA',consumer.render('fr-CA','drafts',{count:0,folder:'Idées'}));
assert.deepEqual(got.releaseBlockers, ['fallback-used']);
assert.deepEqual([got.usedLocale,got.category,got.fallback], ['en-US','other','missing-bundle']);
controls.push({id:'fallback-traces',result:'observed',code:'whole-message English fallback; release still blocked for incomplete French'});

// Change the input contract independently: the old accepted count is now rejected.
const lower=copy(contract); lower.maximumCount=1;
const constrained=createConsumer(source,target,lower);
assert.equal(constrained.render('fr-FR','drafts',{count:1,folder:'Idées'}).text,'1 brouillon dans Idées.');
rejects('changed-contract-rejects-two', () => constrained.render('fr-FR','drafts',{count:2,folder:'Idées'}), 'E_COUNT');
// Rename an argument in BOTH resources and the contract; prove the consumer isn't
// hard-coded to the fixture's old argument name, then reject the stale call site.
const renamed=copy(contract); renamed.messages.welcome.arguments={customer:'string'}; renamed.messages.welcome.occurrences={customer:1};
const renamedEn=copy(source),renamedFr=copy(target);
for(const bundle of [renamedEn,renamedFr]) bundle.messages.welcome.value=bundle.messages.welcome.value.replace('{name}','{customer}');
const adapted=createConsumer(renamedEn,renamedFr,renamed);
got=record('changed-contract-customer',adapted.render('fr-FR','welcome',{customer:'Zoé'}));
assert.equal(got.text,'Bienvenue dans Brume Notes, Zoé.');
rejects('changed-contract-rejects-old-call-site', () => adapted.render('fr-FR','welcome',{name:'Zoé'}), 'E_ARGUMENTS');
controls.push({id:'changed-placeholder-contract',result:'accepted',code:'new argument and resources compiled; old call rejected'});

// A deliberately wrong translation can pass every mechanical gate.
const lostNegation=changedTarget(t => {t.messages.closeWarning.value='Fermez.';});
got=record('semantic-negative-control',createConsumer(source,lostNegation,contract).render('fr-FR','closeWarning',{}));
assert.equal(got.text,'Fermez.');
controls.push({id:'lost-negation',result:'mechanically accepted; meaning review must reject',code:'no semantic guarantee'});
for(const f of files) assert.equal(digest(readFileSync(join(base,f))),hashes[f],`${f} changed during execution`);
const result={status:'PASS for the stated mechanical and consumer tests; semantic control intentionally exposes a gap',
  runtime:{node:process.versions.node,icu:process.versions.icu,cldr:process.versions.cldr,unicode:process.versions.unicode},
  localeOptions:consumer.localeOptions,inputHashes:hashes,controls,outputs,
  releaseAssessment:{originalCandidateMechanicalGate:'pass',incompleteTargetControls:'blocked',fallbackRequestedLocaleReleaseValid:false,linguisticApproval:'not established by this runner',visualIntegration:'untested'},
  untested:['real framework parser/compiler','native application integration','visual layout','screen-reader behavior','independent native-speaker approval']};
const save=(name,text)=>writeFileSync(join(output,name),text,{encoding:'utf8',flag:'wx'});
save('consumer-output.json',JSON.stringify(result,null,2)+'\n');
const cell=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('|','\\|').replaceAll('\n',' ⏎ ');
const lines=['# Observed offline consumer run','',
  `Node ${result.runtime.node}; ICU ${result.runtime.icu}; CLDR ${result.runtime.cldr}; Unicode ${result.runtime.unicode}.`, '',
  'The saved JSON files passed this consumer’s contract gate. The following sentences and fallback metadata came from executing the consumer. They are not screenshots or proof of native integration. Counts are rendered as plain ungrouped decimal digits.', '',
  '## Actual output','', '| Case | Used locale / category | Fallback | Text |','| --- | --- | --- | --- |',
  ...outputs.map(o=>`| ${cell(o.id)} | ${o.usedLocale} / ${o.category??'—'} | ${o.fallback??'none'} | ${cell(o.text)} |`),'',
  'The ⏎ marker in the table denotes a real newline; the JSON output preserves it as a JSON escape. The semantic negative control deliberately renders a wrong instruction. It is not part of the French candidate.', '',
  '## Controls','', '| Control | Observed result | Detail |', '| --- | --- | --- |',
  ...controls.map(c=>`| ${cell(c.id)} | ${cell(c.result)} | ${cell(c.code)} |`),'',
  '## Input identity','', '| Input | SHA-256 |','| --- | --- |', ...Object.entries(hashes).map(([f,h])=>`| ${f} | ${h} |`),'',
  'All listed inputs were reread at the end and their hashes matched. Fallback output carries a fallback-used release blocker; requested-locale release validity is false for every fallback control. Successful rendering without fallback still does not establish release approval. A successful run does not certify linguistic meaning or UI behavior.', '',
  '## Not tested','', ...result.untested.map(x=>`- ${x}`),''];
save('results.md',lines.join('\n'));
for(const name of ['consumer-output.json','results.md']) assert.ok(readFileSync(join(output,name)).length>0);
assert.deepEqual(JSON.parse(readFileSync(join(output,'consumer-output.json'),'utf8')),result);
console.log(`PASS: ${outputs.length} actual outputs; ${controls.length} control observations; saved results read back; input hashes unchanged.`);
console.log(`Saved ${outputName}/results.md and ${outputName}/consumer-output.json (exclusive creation).`);
