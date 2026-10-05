"""Demonstration contract only; real task graders must be independently verified."""
def grade(submission_dir, runner_dir):
    from pathlib import Path
    passed = (Path(submission_dir) / "result.txt").read_text() == "SYNTHETIC FIXTURE ONLY\n"
    return {"case_id": "synthetic-plumbing", "integrity": {"passed": True},
            "groups": [{"id": f"g{i}", "passed": passed} for i in range(1, 6)]}
