# Fictional English-to-French customer instruction release

Solenne Tools, its order process and all source text are invented. The `.invalid` URL cannot be a real customer-support endpoint. No message is sent and nothing is published.

## Request and brief

“Translate the supplied pickup instructions into French for customers in France, using formal ‘vous’. Save a private Markdown candidate and give me the review notes. Preserve placeholders, link destinations and the exact footer. Do not publish it.”

The unchanged authorized source is [fixture-source.md](fixture-source.md); the saved target artifact is [fixture-target.fr-FR.md](fixture-target.fr-FR.md). Both are UTF-8 Markdown. This example claims neither Word/native-app preservation nor certified translation.

Supplied glossary and release-owner clarification:

| Item | Instruction |
| --- | --- |
| pickup | retrait |
| upload | importer; grammatical inflections allowed |
| support | assistance |
| approval | validation |
| Manage order | Gérer la commande; the release owner confirms this matches the French interface |
| Help center | Centre d’aide |
| MB | Mo; both denote the same decimal byte quantity here; no numerical conversion |
| Date | Source uses day/month/year: `05/11/2026` means **5 November 2026**, not 11 May |
| Time | Preserve `16:30 UTC`; do not convert to local time |
| Required footer | Preserve exactly: `© 2026 Solenne Tools. Service terms apply.` |

Before the date clarification, the deadline segment is on hold; the French audience alone cannot resolve the source date. With this supplied clarification, the candidate expands the month name to avoid reintroducing ambiguity. The exact footer deliberately remains in English. The Help center URL retains `lang=en`, as required; the review notes identify the English-destination parameter without claiming the link was opened or silently localizing it.

## Bilingual fidelity review of the saved candidate

| Segment | Meaning retained | Authorized change/check |
| --- | --- | --- |
| Greeting + step 1 | Address the named customer; open the management link for the same order | Formal register, supplied French UI label; all placeholder tokens unchanged |
| Step 2 | One PDF, maximum inclusive size 2.5 MB, deadline inclusive at 16:30 UTC on 5 November | `2,5 Mo` preserves quantity; `ne dépasse pas` preserves ≤; `au plus tard` preserves “by”; month spelled out from clarification |
| Step 3 | No second file unless support requests it; no refresh during upload | `pas … sauf si` preserves the exception and `N’actualisez pas` preserves the prohibition |
| Step 4 | Print scale 100%, minimum clearance 15 mm; do not resize the QR code | `%` spacing is localized; `au moins` preserves ≥; the resizing prohibition is retained |
| Step 5 | Retain confirmation code; cancellation permitted before validation and unavailable after | Glossary term used consistently; no promise about refunds or support response added |
| Help + footer | Same help destination, same exact service-terms text and brand | Link label translated; URL and footer unchanged |

No source step was merged, removed or reordered. No additional product claim was inserted. The canceled/approved process is fictional source wording, not a legal conclusion. A real release would need any review required for its actual consequential claims.

## Repeatable local check

Run the Python 3 block from this folder. It reads the two fixture files, copies the candidate to a temporary saved artifact, reopens it, checks the fixed fixture's invariants and removes only its temporary directory. It uses the standard library and does not visit links.

The role-specific checks normalize the decimal separator and unit label, interpret the source date only under the supplied date order, and compare deadline, UTC, print scale and clearance at their respective steps. The fixture-specific negation checks catch the tested regressions; they do not constitute a general semantic parser.

```python
import hashlib
import re
import tempfile
from collections import Counter
from datetime import datetime, date
from decimal import Decimal as D
from pathlib import Path

source_path = Path('fixture-source.md')
target_path = Path('fixture-target.fr-FR.md')
source_bytes = source_path.read_bytes()
target_bytes = target_path.read_bytes()
source = source_bytes.decode('utf-8')
target = target_bytes.decode('utf-8')
footer = '© 2026 Solenne Tools. Service terms apply.'


def tokens(text):
    # Only this fixture's {{name}} syntax; not ICU, printf or HTML validation.
    return Counter(re.findall(r'\{\{[A-Za-z_][A-Za-z_0-9]*\}\}', text))


def steps(text):
    pairs = re.findall(r'^(\d+)\. (.+)$', text, re.M)
    assert [key for key, _ in pairs] == ['1', '2', '3', '4', '5']
    return dict(pairs)


def deadline(text, date_order):
    if date_order is None:
        raise ValueError('Source date order must be supplied before release')
    assert date_order == 'DMY'
    stamp = re.search(r'by (\d{2}/\d{2}/\d{4}) at (\d{2}:\d{2}) (UTC)', text)
    return datetime.strptime(stamp[1], '%d/%m/%Y').date(), stamp[2], stamp[3]


def validate(candidate):
    s, t = steps(source), steps(candidate)
    assert source.count('\n# ') == candidate.count('\n# ') == 0
    assert len(re.findall(r'^# ', source, re.M)) == len(re.findall(r'^# ', candidate, re.M)) == 1
    assert len(source.strip().split('\n\n')) == len(candidate.strip().split('\n\n')) == 5
    assert tokens(source) == tokens(candidate) == Counter({
        '{{customer_name}}': 1, '{{manage_order_url}}': 1,
        '{{order_id}}': 1, '{{confirmation_code}}': 1})
    assert tokens(source.split('\n\n')[1]) == tokens(candidate.split('\n\n')[1])
    for key in s:
        assert tokens(s[key]) == tokens(t[key])
    # Preserve link order, exact destinations and protected required wording.
    link = r'\[[^\]]+\]\(([^)]+)\)'
    assert re.findall(link, source) == re.findall(link, candidate)
    assert source.count(footer) == candidate.count(footer) == 1
    assert source.rstrip().endswith(footer) and candidate.rstrip().endswith(footer)
    max_s = re.search(r'no larger than ([\d.]+) (MB)', s['2'])
    max_t = re.search(r'ne dépasse pas ([\d,]+) (Mo)', t['2'])
    assert max_s and max_t
    assert D(max_s[1]) == D(max_t[1].replace(',', '.')) == D('2.5')
    assert {'MB': 'Mo'}[max_s[2]] == max_t[2]
    date_s, time_s, zone_s = deadline(s['2'], 'DMY')
    date_t = re.search(r'au plus tard le (\d+) novembre (\d{4}) à (\d{2}:\d{2}) (UTC)', t['2'])
    assert date_t
    assert date_s == date(int(date_t[2]), 11, int(date_t[1])) == date(2026, 11, 5)
    assert time_s == date_t[3] == '16:30' and zone_s == date_t[4] == 'UTC'
    assert 'Upload one PDF' in s['2'] and 'Importez un seul PDF' in t['2']
    assert 'Do not upload a second file unless support asks you to.' in s['3']
    assert 'N’importez pas de deuxième fichier sauf si l’assistance vous le demande.' in t['3']
    assert 'Do not refresh the page while the upload is in progress.' in s['3']
    assert 'N’actualisez pas la page pendant l’importation.' in t['3']
    scale_s = re.search(r'at (\d+)% scale', s['4'])[1]
    scale_t = re.search(r'à l’échelle (\d+) %', t['4'])[1]
    assert int(scale_s) == int(scale_t) == 100
    clearance_s = re.search(r'at least (\d+) (mm)', s['4'])
    clearance_t = re.search(r'au moins (\d+) (mm)', t['4'])
    assert clearance_s.groups() == clearance_t.groups() == ('15', 'mm')
    assert 'Do not resize it.' in s['4'] and 'Ne le redimensionnez pas.' in t['4']
    assert 'may cancel before approval; cancellation is not available after approval.' in s['5']
    assert 'pouvez annuler avant la validation ; l’annulation n’est plus possible après la validation.' in t['5']
    return True

try:
    deadline(steps(source)['2'], None)
except ValueError:
    pass
else:
    raise AssertionError('ambiguous source date was released without clarification')

with tempfile.TemporaryDirectory() as directory:
    saved_path = Path(directory) / 'customer-instructions.fr-FR.md'
    saved_path.write_bytes(target_bytes)
    saved = saved_path.read_text(encoding='utf-8')
    assert validate(saved)
    assert saved_path.read_bytes() == target_bytes
    mutations = {
        'renamed placeholder': saved.replace('{{order_id}}', '{{Order_id}}'),
        'wrong month-day interpretation': saved.replace('5 novembre 2026', '11 mai 2026'),
        'tenfold size': saved.replace('2,5 Mo', '25 Mo'),
        'dropped negation': saved.replace('N’actualisez pas', 'Actualisez'),
        'changed link': saved.replace('lang=en', 'lang=fr'),
        'duplicated token': saved.replace('{{confirmation_code}}', '{{confirmation_code}} {{confirmation_code}}'),
        'moved token': saved.replace('{{order_id}}', '{{confirmation_code}}', 1).replace('le code de confirmation {{confirmation_code}}', 'le code de confirmation {{order_id}}'),
        'changed footer': saved.replace('Service terms apply.', 'Conditions générales applicables.'),
    }
    for name, changed in mutations.items():
        try:
            validate(changed)
        except (AssertionError, AttributeError, TypeError):
            pass
        else:
            raise AssertionError('undetected regression: ' + name)
assert source_path.read_bytes() == source_bytes
assert target_path.read_bytes() == target_bytes
print('PASS: five steps, four exact placeholders, two link destinations, protected footer, numeric/date/unit roles, negative conditions, saved UTF-8 readback')
print('PASS: missing date order held; eight corrupted candidates rejected; source and target files unchanged')
print('SOURCE SHA256', hashlib.sha256(source_bytes).hexdigest())
print('TARGET SHA256', hashlib.sha256(target_bytes).hexdigest())
```

Observed on 2026-10-01 in the repository’s Linux environment with Python 3.12.14: exit status 0, the two PASS lines and source/target digests. The deadline cannot be interpreted before the supplied clarification. Eight corrupted copies must fail; the unchanged saved candidate must pass. These are specific fixture checks plus the explicit bilingual review above, not broad linguistic certification, a native-format round trip or evidence of delivery to customers.
