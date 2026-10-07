"""Normal text fixtures for the read-only collection checker; no skill code runs."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).with_name("check-skill-links.py")
REPOSITORY = CHECKER.parent.parent


class SkillLinkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in ("fixture-source.md", "fixture-target.fr-FR.md"):
            self.write(f"skill/translation-release-review/{name}",
                       "[Manage order]({{manage_order_url}})\n")

    def write(self, path, text):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")

    def run_check(self, expected=0):
        result = subprocess.run([sys.executable, "-I", "-B", str(CHECKER),
                                 "--root", str(self.root)],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_relative_file_directory_root_and_image_links(self):
        self.write("README.md", "# Collection\n")
        self.write("skill/demo/other.md", "# Other\n")
        self.write("skill/demo/assets/ordinary.txt", "A supporting asset.\n")
        self.write("skill/demo/nested/SKILL.md", """
[Other](../other.md)
[Assets](../assets/)
[Root](/README.md#collection)
![Text fixture](../assets/ordinary.txt)
""")
        self.assertIn("4 local destinations", self.run_check())

    def test_url_encoding_unicode_query_and_angle_destination(self):
        self.write("skill/demo/résumé notes.md", "# Café notes\n")
        self.write("skill/demo/SKILL.md", """
[Encoded](r%C3%A9sum%C3%A9%20notes.md?view=1#caf%C3%A9-notes)
[Angle](<résumé notes.md#café-notes> "An ordinary title")
""")
        self.assertIn("2 checked fragments", self.run_check())

    def test_balanced_parentheses_and_markdown_escapes(self):
        self.write("skill/demo/notes (draft).md", "# Details\n")
        self.write("skill/demo/report(draft).md", "# Details\n")
        self.write("skill/demo/SKILL.md", r"""
[Balanced](report(draft).md#details)
[Escaped](report\(draft\).md#details 'A title')
[Angle](<notes (draft).md#details>)
[Label with \] punctuation](report(draft).md)
\[Literal](missing.md)
""")
        self.assertIn("4 local destinations", self.run_check())

    def test_reference_definitions_and_optional_titles(self):
        self.write("skill/demo/target.md", "# Target\n")
        self.write("skill/demo/SKILL.md", """
[Full][destination] and [collapsed][] and [shortcut].
[destination]: target.md#target "Title"
[collapsed]: <target.md#target> 'Title with ) punctuation'
[shortcut]: target.md (Title)
[unused]: target.md
[Missing definition] is plain text.
""")
        self.assertIn("4 local destinations", self.run_check())

    def test_reference_missing_destination(self):
        self.write("skill/demo/SKILL.md", "[details][ref]\n\n[ref]: missing.md\n")
        self.assertIn("skill/demo/SKILL.md:3: 'missing.md': missing file", self.run_check(1))

    def test_explicit_html_ids_names_and_case(self):
        self.write("skill/demo/target.md", '<a id="Stable-ID"></a>\n<a name="legacy"></a>\n')
        self.write("skill/demo/page.html", '<h2 id="html-anchor">Ordinary HTML</h2>\n')
        self.write("skill/demo/SKILL.md", """
[Stable](target.md#Stable-ID)
[Legacy](target.md#legacy)
[HTML](page.html#html-anchor)
""")
        self.assertIn("3 checked fragments", self.run_check())

    def test_duplicate_heading_suffixes_and_collisions(self):
        self.write("skill/demo/SKILL.md", """
# A
# A
# A-1
# A
[First](#a) [Second](#a-1) [Collision](#a-1-1) [Third](#a-2)
""")
        self.assertIn("4 checked fragments", self.run_check())

    def test_atx_setext_formatting_and_punctuation(self):
        self.write("skill/demo/SKILL.md", """
  ## A **bold** `code` [label](other.md) &amp; _emphasis_! ##
Title_with_underscores
======================
[Formatting](#a-bold-code-label--emphasis)
[Setext](#title_with_underscores)
""")
        self.write("skill/demo/other.md", "# Other\n")
        self.run_check()

    def test_heading_full_reference_link_uses_its_label(self):
        self.write("skill/demo/SKILL.md", "# [Useful guide][guide]\n"
                   "[guide]: target.md\n[Heading](#useful-guide)\n")
        self.write("skill/demo/target.md", "# Target\n")
        self.run_check()

    def test_heading_balanced_destination_uses_its_label(self):
        self.write("skill/demo/SKILL.md", "# [Useful guide](report(draft).md)\n"
                   "[Heading](#useful-guide)\n")
        self.write("skill/demo/report(draft).md", "# Report\n")
        self.run_check()

    def test_heading_reference_variants_and_literal_undefined_labels(self):
        self.write("skill/demo/SKILL.md", """
# [Collapsed][] and [Shortcut] and [Full][ Mixed   CASE ]
# [Undefined][unknown]
[collapsed]: target.md
[shortcut]: target.md
[mixed case]: target.md
[Defined](#collapsed-and-shortcut-and-full)
[Literal](#undefinedunknown)
""")
        self.write("skill/demo/target.md", "# Target\n")
        self.run_check()

    def test_seven_existing_presentation_links_are_valid(self):
        source = REPOSITORY / "skill/source-backed-presentation"
        packet = (source / "source-packet.md").read_text(encoding="utf-8")
        script = (source / "slide-script.md").read_text(encoding="utf-8")
        links = [line for line in script.splitlines() if
                 "source-packet.md#s0-brief" in line or
                 "source-packet.md#s5-rejected-draft-claims" in line]
        self.assertEqual(len(links), 7)
        self.write("skill/demo/source-packet.md", packet)
        self.write("skill/demo/SKILL.md", "\n".join(links))
        self.run_check()

    def test_code_fences_inline_code_and_comments_are_not_links(self):
        self.write("skill/demo/SKILL.md", """
```markdown
[Example](missing-one.md)
````
~~~text
[Example](missing-two.md)
~~~
``[Example](missing-three.md) `literal tick` ``
<!-- [Example](missing-four.md) -->
[Actual](target.md)
""")
        self.write("skill/demo/target.md", "# Target\n")
        self.assertIn("1 local destinations", self.run_check())

    def test_shorter_fence_does_not_close_longer_fence(self):
        self.write("skill/demo/SKILL.md", "````\n```\n[Example](missing.md)\n````\n")
        self.run_check()

    def test_fence_inside_comment_does_not_hide_a_real_link(self):
        self.write("skill/demo/SKILL.md", "<!--\n```\n-->\n[Missing](missing.md)\n")
        self.assertIn("skill/demo/SKILL.md:4: 'missing.md': missing file", self.run_check(1))

    def test_comment_inside_fence_does_not_hide_a_real_link(self):
        self.write("skill/demo/SKILL.md", "```\n<!--\n```\n[Missing](missing.md)\n")
        self.assertIn("skill/demo/SKILL.md:4: 'missing.md': missing file", self.run_check(1))

    def test_comment_inside_inline_code_does_not_hide_a_real_link(self):
        self.write("skill/demo/SKILL.md", "`<!--` [Missing](missing.md)\n")
        self.assertIn("skill/demo/SKILL.md:1: 'missing.md': missing file", self.run_check(1))

    def test_unmatched_inline_tick_does_not_hide_a_link(self):
        self.write("skill/demo/SKILL.md", "Unmatched ` and [actual](missing.md)\n")
        self.assertIn("'missing.md': missing file", self.run_check(1))

    def test_escaped_backticks_do_not_hide_a_link(self):
        self.write("skill/demo/SKILL.md", r"\` [Actual](missing.md) \`" + "\n")
        self.assertIn("'missing.md': missing file", self.run_check(1))

    def test_literal_underscores_in_heading_code_and_escapes(self):
        self.write("skill/demo/SKILL.md", "# `_code_` and \\_literal\\_\n"
                   "[Heading](#_code_-and-_literal_)\n")
        self.run_check()

    def test_frontmatter_example_is_not_a_link(self):
        self.write("skill/demo/SKILL.md", '---\nname: demo\ndescription: "[Example](missing.md)"\n---\n# Demo\n')
        self.run_check()

    def test_code_and_comments_do_not_create_anchors(self):
        self.write("skill/demo/SKILL.md", """
```
# Example
<a id="example-id"></a>
```
`<a id="inline-id"></a>`
<!-- <a id="comment-id"></a> -->
[Heading](#example) [HTML](#example-id) [Inline](#inline-id) [Comment](#comment-id)
""")
        self.assertEqual(self.run_check(1).count(": missing fragment"), 4)

    def test_external_schemes_and_protocol_relative_urls_are_skipped(self):
        self.write("skill/demo/SKILL.md", """
[HTTPS](https://example.invalid/missing#fragment)
[Mail](mailto:author@example.invalid)
[Scheme](custom:ordinary-reference)
[Protocol relative](//example.invalid/missing)
""")
        self.assertIn("0 local destinations", self.run_check())

    def test_missing_file_and_fragment_diagnostics_are_deterministic(self):
        self.write("skill/demo/target.md", "# Existing\n")
        self.write("skill/demo/SKILL.md", "[File](missing.md)\n[Anchor](target.md#absent)\n")
        output = self.run_check(1)
        self.assertEqual(output, self.run_check(1))
        self.assertIn("skill/demo/SKILL.md:1: 'missing.md': missing file or directory", output)
        self.assertIn("skill/demo/SKILL.md:2: 'target.md#absent': missing fragment", output)

    def test_ordinary_fixture_passes_then_missing_target_fails(self):
        self.write("skill/demo/target.md", "# Expected\n")
        self.write("skill/demo/SKILL.md", "[Target](target.md#expected)\n")
        self.run_check()
        (self.root / "skill/demo/target.md").unlink()
        self.assertIn("missing file or directory", self.run_check(1))

    def test_ordinary_fixture_passes_then_changed_fragment_fails(self):
        self.write("skill/demo/target.md", "# Expected\n")
        self.write("skill/demo/SKILL.md", "[Target](target.md#expected)\n")
        self.run_check()
        self.write("skill/demo/target.md", "# Changed\n")
        self.assertIn("missing fragment", self.run_check(1))

    def test_two_exact_template_pairs_are_counted(self):
        self.assertIn("2 documented template links; 0 error(s)", self.run_check())

    def test_same_template_elsewhere_is_not_exempt(self):
        self.write("skill/demo/SKILL.md", "[Template]({{manage_order_url}})\n")
        self.assertIn("skill/demo/SKILL.md:1: '{{manage_order_url}}': missing file", self.run_check(1))

    def test_changed_template_is_not_exempt(self):
        self.write("skill/translation-release-review/fixture-source.md", "[Template]({{other_url}})\n")
        output = self.run_check(1)
        self.assertIn("'{{other_url}}': missing file", output)
        self.assertIn("expected one documented template link, found 0", output)

    def test_duplicate_template_exception_fails(self):
        self.write("skill/translation-release-review/fixture-source.md",
                   "[A]({{manage_order_url}})\n[B]({{manage_order_url}})\n")
        self.assertIn("expected one documented template link, found 2", self.run_check(1))

    def test_template_exception_does_not_hide_a_missing_neighbor(self):
        self.write("skill/translation-release-review/fixture-source.md",
                   "[Template]({{manage_order_url}})\n[Actual](missing.md)\n")
        self.assertIn(":2: 'missing.md': missing file", self.run_check(1))

    def test_empty_collection_is_not_a_success(self):
        with tempfile.TemporaryDirectory() as directory:
            self.root = Path(directory)
            self.assertIn("skill/: no Markdown files found", self.run_check(1))


if __name__ == "__main__":
    unittest.main()
