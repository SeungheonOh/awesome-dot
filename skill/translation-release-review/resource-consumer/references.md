# Primary technical references

Inspected **2026-10-02**. The grammar, count bound, error codes and fallback policy are defined by this packet, not claimed as ECMAScript requirements.

- [ECMAScript: `Intl.PluralRules.prototype.select`](https://tc39.es/ecma402/#sec-intl.pluralrules.prototype.select) defines category selection. This is the living specification; the executed runtime is identified separately
- [ECMAScript: `resolvedOptions`](https://tc39.es/ecma402/#sec-intl.pluralrules.prototype.resolvedoptions) exposes resolved locale/options and plural categories; the consumer uses runtime-reported categories
- [MDN: `Intl.PluralRules`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules) describes locale-dependent cardinal/ordinal categories and locale support checks; complete sentence wording still requires review
- [MDN: `JSON.parse`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse) describes JSON parsing and syntax errors; duplicate-member checking is supplied separately here
- [MDN: `Number.isSafeInteger`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isSafeInteger) describes safe-integer checks without string coercion; the consumer separately enforces its range

The French outcomes for 0, 1, 2, 21 and 1,000,000 are [measured runtime observations](observed-run/results.md), not guarantees about every historical locale-data version. No documentation page or example URL is executed by the consumer.
