"""Post-hoc contract diagnostic only; not part of frozen primary scoring."""
import importlib
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, sys.argv[1])
CardEditor = importlib.import_module('card_editor').CardEditor
text = chr(0xD800) + '\n'
source = {'document_id': 'surrogate-contract-edge', 'revision': 0, 'text': text}
editor = CardEditor(source, source, source)
result = {'post_hoc': True, 'changes_primary_score': False, 'input': 'U+D800 followed by LF',
          'constructed': True, 'view_text_exact': editor.view()['text'] == text}
with tempfile.TemporaryDirectory(prefix='posthoc-') as directory:
    path = Path(directory) / 'surrogate.json'
    try:
        record = editor.save(path)
        parsed = json.loads(path.read_text(encoding='utf-8'))
        restored = CardEditor.load(path)
        result.update({'saved': True, 'parsed_record_equal': parsed == record,
                       'state_equal_after_reload': restored.session.to_state() == editor.session.to_state(),
                       'view_equal_after_reload': restored.view() == editor.view(),
                       'text_equal_after_reload': restored.view()['text'] == text})
    except Exception as error:
        result.update({'saved': False, 'error_type': type(error).__name__, 'error': str(error)})
print(json.dumps(result, ensure_ascii=True))
