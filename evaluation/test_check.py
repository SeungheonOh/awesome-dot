"""Local navigation-check regressions; no models or submitted-code execution."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check


ORIGINAL_GUIDE = "packages/skill/build-text-merge-component/SKILL.md"
REPEATED_GUIDE = "studies/repeated-stress-2026-10-06/guides/skill/build-text-merge-component/SKILL.md"
COMMON_TARGETS = {
    "../parallel-change-integration/SKILL.md",
    "../verify-exact-text-patches/SKILL.md",
    "../implement-scoped-change/SKILL.md",
}
EXPECTED_EXCEPTIONS = (
    {(ORIGINAL_GUIDE, target) for target in COMMON_TARGETS}
    | {(REPEATED_GUIDE, target) for target in COMMON_TARGETS}
    | {(REPEATED_GUIDE, "../document-revision-reconciliation/SKILL.md")}
)


class LinkCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for source, target in sorted(EXPECTED_EXCEPTIONS):
            path = self.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as stream:
                stream.write(f"[Pinned neighboring workflow]({target})\n")

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def run_check(self):
        output = io.StringIO()
        with patch.object(check, "ROOT", self.root), contextlib.redirect_stdout(output):
            check.check_links()
        return output.getvalue()

    def test_allowlist_contains_only_the_seven_documented_pairs(self):
        self.assertEqual(check.OMITTED_PACKAGE_LINKS, EXPECTED_EXCEPTIONS)

    def test_exact_pinned_omissions_are_accepted_and_counted(self):
        self.assertIn("0 checked; 7 explicitly omitted", self.run_check())

    def test_ordinary_missing_destination_still_fails(self):
        self.write("README.md", "[Missing report](missing-report.md)\n")
        with self.assertRaisesRegex(ValueError, "Broken local link: README.md"):
            self.run_check()

    def test_same_target_in_another_source_still_fails(self):
        self.write("notes/README.md", "[Workflow](../parallel-change-integration/SKILL.md)\n")
        with self.assertRaisesRegex(ValueError, "Broken local link: notes/README.md"):
            self.run_check()

    def test_other_missing_link_in_pinned_source_still_fails(self):
        path = self.root / REPEATED_GUIDE
        path.write_text(path.read_text() + "[Missing example](example.md)\n")
        with self.assertRaisesRegex(ValueError, "Broken local link: studies/"):
            self.run_check()

    def test_disappearing_pinned_exception_requires_review(self):
        path = self.root / ORIGINAL_GUIDE
        path.write_text("".join(path.read_text().splitlines(keepends=True)[1:]))
        with self.assertRaisesRegex(ValueError, "cross-link exceptions changed"):
            self.run_check()

    def test_valid_relative_destination_and_heading_are_checked(self):
        self.write("README.md", "[Report](docs/report.md#saved-evidence)\n")
        self.write("docs/report.md", "# Saved evidence\n")
        self.assertIn("1 checked; 7 explicitly omitted", self.run_check())

    def test_missing_heading_still_fails(self):
        self.write("README.md", "[Report](docs/report.md#missing-heading)\n")
        self.write("docs/report.md", "# Saved evidence\n")
        with self.assertRaisesRegex(ValueError, "Broken heading link: README.md"):
            self.run_check()


if __name__ == "__main__":
    unittest.main()
