"""Include the authored action-handoff controls in unified local verification."""
import importlib.util
from pathlib import Path


def load_tests(loader, tests, pattern):
    path = Path(__file__).resolve().parent / "examples/action-handoff/test_check.py"
    spec = importlib.util.spec_from_file_location("action_handoff_authored_controls", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return loader.loadTestsFromModule(module)
