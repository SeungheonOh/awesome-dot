# Review the saved French meaning

This is a bilingual draft review against the saved English source, not an independent native-speaker report. The audience assumption is France (`fr-FR`); instructions use formal `vous`. All app behavior belongs to the fictional source, not to a real product or policy.

| Key | Source proposition | French treatment and decision |
| --- | --- | --- |
| `welcome` | Welcome the named person to Brume Notes | `Bienvenue dans Brume Notes, {name}.` retains the addressee and exact product name |
| `drafts` | Give the precise number of drafts in the supplied folder | `brouillon` for French `one`; `brouillons` for `other` and `many`; count and folder remain once in every branch |
| `saveWarning` | Do not close while saving the file; do not retry unless an error appears | `Ne fermez pas … pendant l’enregistrement de {file}` retains the prohibition and interval. `Ne réessayez pas, sauf si une erreur s’affiche` retains the exception without turning an error into a command to retry |
| `closeWarning` | Do not close | `Ne fermez pas.` keeps the complete prohibition in 14 code points. Its relationship to the relevant action must be checked in the actual UI |
| `help` | Identify product help and display the supplied destination | `Aide pour` localizes the label. Product and destination, including `lang=en&topic=drafts`, stay exact. The URL was not opened or silently localized |
| `entryHint` | Type the supplied label; show the example folder on the next line | `Saisissez « {label} ».` is a formal instruction. The newline and `C:\Brume\Drafts` remain; replacing English quotation marks with guillemets is an intentional punctuation change |
| `patternHint` | Display a literal brace-delimited pattern and a supplied value | `Modèle : {draft} ; valeur : …` distinguishes literal text from interpolation. Stored `{{draft}}` produces literal braces; caller data is never reparsed |

`Ne … pas` remains in both warnings. `pendant` preserves the saving interval and `sauf si` the retry exception. No new promise, troubleshooting step, refund rule, retention policy or permission was added. Shortening never changes “do not” into a suggestion or a positive command.

## Zero, large counts and caller data

`0 brouillon` matches the observed French cardinal `one` selection and is readable in this counter. “Aucun brouillon” could be considered with the real product context, but would require explicit zero handling in its message format; it is not silently introduced here.

At 1,000,000, the measured French category is `many`, with plural `brouillons`. Ungrouped decimal digits are a consumer simplification. A real UI should apply its approved numeric style and inspect spacing and layout.

Folder names and filenames are caller data. Preserve user-authored text without guessing that it should be translated. `0 drafts in Idées.` is therefore an English fallback sentence with unchanged caller data, not an acceptable French release.

## What the mechanical negative control demonstrates

The runner substitutes `Fermez.` for `Ne fermez pas.`. It is grammatical, short and structurally valid, so it compiles. It means “Close” and reverses the prohibition. This review rejects the mutation. The saved French resource still contains the original negative instruction.

Before an actual release, review the current saved resources against their source and real UI context. Record the person who resolves consequential wording questions. Use specialist review where required by the actual subject matter or release process; this example does not invent a universal approval requirement.
