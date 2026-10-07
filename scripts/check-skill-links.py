#!/usr/bin/env python3
"""Read-only, standard-library local-link check for Markdown under skill/.

Coverage: ordinary single-line inline links/images (including balanced or escaped
parentheses and angle-bracket destinations), single-line reference definitions,
ATX and one-line Setext headings with ordinary inline formatting, duplicate
heading IDs, and explicit HTML id/a
name anchors. Relative and repository-root paths, URL escapes, Markdown escapes,
and optional link titles are supported. Reference destinations are checked once
at their definitions, even if unused; undefined reference labels are plain text.

This is not a full CommonMark/GFM parser. It excludes fenced code (up to three
leading spaces), inline code spans, initial YAML frontmatter and HTML comments.
It does not interpret
multiline links/definitions, indented code, container-nested fences/headings,
HTML links, autolinks, or arbitrary renderer extensions. Fragments are checked
only in Markdown and HTML targets. External URLs are skipped, never fetched.
It never imports or executes skill code, writes files, or evaluates templates.
"""

import argparse
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import string
import unicodedata
from urllib.parse import unquote, urlsplit


# Synthetic translation fixtures deliberately leave this substitution unresolved.
# Require each exact source/destination pair once; no general template exemption.
TEMPLATE_LINKS = {
    ("skill/translation-release-review/fixture-source.md", "{{manage_order_url}}"),
    ("skill/translation-release-review/fixture-target.fr-FR.md", "{{manage_order_url}}"),
}
ESCAPE = re.compile(r"\\([" + re.escape(string.punctuation) + r"])")


def blank(text):
    """Keep offsets and line numbers while masking non-prose."""
    return re.sub(r"[^\n]", " ", text)


def prose(text, inline_code=True):
    text = re.sub(r"\A---\r?\n[\s\S]*?\r?\n---[ \t]*(?:\r?\n|\Z)",
                  lambda m: blank(m[0]), text)
    lines, fence, comment = [], None, False
    for line in text.splitlines(keepends=True):
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) +
                            "{" + str(len(fence)) + r",}[ \t]*\r?\n?", line):
                fence = None
            lines.append(blank(line))
            continue
        start = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)", line)
        if not comment and start and (start[1][0] != "`" or "`" not in start[2]):
            fence = start[1]
            lines.append(blank(line))
            continue
        # Comments and fences have separate state: neither delimiter can open
        # the other construct from inside one. Preserve all source offsets.
        chars, i = list(line), 0
        while i < len(line):
            if comment:
                close = line.find("-->", i)
                end = len(line) if close == -1 else close + 3
                chars[i:end] = blank(line[i:end])
                comment = close == -1
                i = end
            elif line[i] == "\\":
                i += 2
            elif line.startswith("<!--", i):
                comment = True
            elif line[i] == "`":
                run = re.match(r"`+", line[i:])[0]
                close = re.search(r"(?<!`)" + re.escape(run) + r"(?!`)", line[i + len(run):])
                i = i + len(run) + close.end() if close else i + len(run)
            else:
                i += 1
        lines.append("".join(chars))
    text = "".join(lines)
    if inline_code:
        # A closing run must have exactly the opener's length. Unmatched ticks
        # are literal text, so they must not hide later links.
        runs = list(re.finditer(r"`+", text))
        chars, i = list(text), 0
        while i < len(runs):
            preceding = text[:runs[i].start()]
            if (len(preceding) - len(preceding.rstrip("\\"))) % 2:
                i += 1
                continue
            j = next((j for j in range(i + 1, len(runs))
                      if len(runs[j][0]) == len(runs[i][0])), None)
            if j is None:
                i += 1
                continue
            start, end = runs[i].start(), runs[j].end()
            chars[start:end] = blank(text[start:end])
            i = j + 1
        text = "".join(chars)
    return text


def destination(text, start):
    """Return (raw destination, end offset) or None for unsupported syntax."""
    if start >= len(text):
        return None
    if text[start] == "<":
        i = start + 1
        while i < len(text):
            if text[i] == "\\" and i + 1 < len(text):
                i += 2
            elif text[i] == ">":
                return text[start + 1:i], i + 1
            elif text[i] in "\n<":
                return None
            else:
                i += 1
        return None
    i, depth = start, 0
    while i < len(text):
        char = text[i]
        if char == "\\" and i + 1 < len(text):
            i += 2
            continue
        if char.isspace() or (char == ")" and depth == 0):
            break
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        i += 1
    return (text[start:i], i) if depth == 0 else None


def title_tail(text):
    """An optional single-line quoted/parenthesized title."""
    return not text.strip() or bool(re.fullmatch(
        r'''\s+(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\((?:\\.|[^)\\])*\))\s*''', text))


def reference_label(text):
    return " ".join(unescape(ESCAPE.sub(r"\1", text)).split()).casefold()


def reference_definition(line):
    match = re.match(r"^ {0,3}\[((?:\\.|[^\]\\])+)\]:[ \t]*", line)
    if match:
        item = destination(line, match.end())
        if item and title_tail(line[item[1]:]):
            return reference_label(match[1]), item[0]
    return None


def bracket_end(line, start):
    """Offset after a balanced label's closing bracket, or None."""
    j, depth = start + 1, 1
    while j < len(line) and depth:
        if line[j] == "\\":
            j += 2
            continue
        if line[j] == "[":
            depth += 1
        elif line[j] == "]":
            depth -= 1
        j += 1
    return j if not depth else None


def inline_destination(line, start):
    """Read the (...) after a label, using the same grammar everywhere."""
    if start >= len(line) or line[start] != "(":
        return None
    i = start + 1
    while i < len(line) and line[i] in " \t":
        i += 1
    item = destination(line, i)
    if item:
        target, end = item
        for close in range(end, len(line)):
            if line[close] == ")" and title_tail(line[end:close]):
                return target, close + 1
    return None


def links(text):
    """Yield source line and destination, in source order."""
    for number, line in enumerate(prose(text).splitlines(), 1):
        definition = reference_definition(line)
        if definition:
            yield number, definition[1]
            continue
        i = 0
        while i < len(line):
            if line[i] == "\\":
                i += 2
                continue
            if line[i] != "[":
                i += 1
                continue
            end = bracket_end(line, i)
            item = inline_destination(line, end) if end is not None else None
            if item:
                yield number, item[0]
                i = item[1]
            else:
                i += 1


class HTMLAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and (key == "id" or (tag == "a" and key == "name")):
                self.ids.add(value)


def heading_link_text(title, references):
    """Keep rendered labels for ordinary inline and defined reference links."""
    result, i = [], 0
    while i < len(title):
        if title[i] == "\\":
            result.append(title[i:i + 2])
            i += 2
            continue
        if title[i] == "`":
            run = re.match(r"`+", title[i:])[0]
            close = re.search(r"(?<!`)" + re.escape(run) + r"(?!`)", title[i + len(run):])
            end = i + len(run) + close.end() if close else i + len(run)
            result.append(title[i:end])
            i = end
            continue
        start = i + 1 if title.startswith("![", i) else i
        end = bracket_end(title, start) if title[start] == "[" else None
        if end is not None:
            label = title[start + 1:end - 1]
            item = inline_destination(title, end)
            finish = item[1] if item else None
            if not item and end < len(title) and title[end] == "[":
                ref_end = bracket_end(title, end)
                if ref_end and reference_label(title[end + 1:ref_end - 1] or label) in references:
                    finish = ref_end
            elif not item and reference_label(label) in references:
                finish = end
            if finish is not None:
                result.append(heading_link_text(label, references))
                i = finish
                continue
        result.append(title[i])
        i += 1
    return "".join(result)


def heading_slug(title, references):
    title = heading_link_text(title, references)
    title = re.sub(r"<[^>]*>", "", title)
    # Underscores inside ordinary code spans or escaped literal text survive.
    title = "".join(part if part.startswith("`") else re.sub(
        r"(?<![\w\\])(_+)(?=\S)(.+?)(?<=\S)(?<!\\)\1(?!\w)", r"\2", part)
        for part in re.split(r"(`+[^`]*`+)", title))
    title = unescape(ESCAPE.sub(r"\1", title)).lower()
    return "".join("-" if c == " " else c for c in title
                   if c in " -_" or unicodedata.category(c)[0] in "LNM")


def anchors(text, markdown=True):
    visible = prose(text, inline_code=False) if markdown else text
    parser = HTMLAnchors()
    parser.feed(prose(text) if markdown else text)
    found = set(parser.ids)
    if not markdown:
        return found
    # Heading collisions include previously generated suffixes, not just an
    # independent count of each title: 'A', 'A', 'A-1' => a, a-1, a-1-1.
    used = set()
    lines = visible.splitlines()
    references = {item[0] for line in prose(text).splitlines()
                  if (item := reference_definition(line))}
    for index, line in enumerate(lines):
        match = re.match(r"^ {0,3}#{1,6}(?:[ \t]+(.*?)|[ \t]*)$", line)
        if match:
            title = re.sub(r"[ \t]+#+[ \t]*$", "", match[1] or "").strip()
        elif (index + 1 < len(lines) and line.strip()
              and re.fullmatch(r" {0,3}(?:=+|-+)[ \t]*", lines[index + 1])
              and not re.match(r"^\s*(?:[-*+>] |\d+[.)] |#| {4})", line)):
            title = line.strip()
        else:
            continue
        base, suffix = heading_slug(title, references), 0
        slug = base
        while slug in used:
            suffix += 1
            slug = f"{base}-{suffix}"
        used.add(slug)
        found.add(slug)
    return found


def check(root):
    root = root.resolve()
    sources = sorted((root / "skill").rglob("*.md"))
    errors, seen, cache = [], Counter(), {}
    local_count = fragment_count = 0
    if not sources:
        errors.append("skill/: no Markdown files found")
    for source in sources:
        name = source.relative_to(root).as_posix()
        try:
            if not source.resolve().is_relative_to(root):
                raise ValueError("source is outside repository root")
            text = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{name}: cannot read source: {error}")
            continue
        for line, raw in links(text):
            target = unescape(ESCAPE.sub(r"\1", raw))
            label = f"{name}:{line}: {raw!r}"
            try:
                url = urlsplit(target)
            except ValueError:
                errors.append(f"{label}: invalid destination")
                continue
            if url.scheme or url.netloc:
                continue
            if (name, raw) in TEMPLATE_LINKS:
                seen[name, raw] += 1
                continue
            local_count += 1
            path = unquote(url.path)
            candidate = (root / path.lstrip("/") if path.startswith("/")
                         else source.parent / path) if path else source
            try:
                resolved = candidate.resolve()
                if not resolved.is_relative_to(root):
                    errors.append(f"{label}: destination is outside repository root")
                elif not resolved.exists():
                    errors.append(f"{label}: missing file or directory")
                elif url.fragment and resolved.suffix.lower() in (".md", ".html", ".htm") and resolved.is_file():
                    fragment_count += 1
                    if resolved not in cache:
                        cache[resolved] = anchors(resolved.read_text(encoding="utf-8"),
                                                  resolved.suffix.lower() == ".md")
                    if unquote(url.fragment) not in cache[resolved]:
                        errors.append(f"{label}: missing fragment")
            except (OSError, UnicodeError, ValueError) as error:
                errors.append(f"{label}: cannot read destination: {error}")
    for source, target in sorted(TEMPLATE_LINKS):
        count = seen[source, target]
        if count != 1:
            errors.append(f"{source}: {target!r}: expected one documented template link, found {count}")
    for error in errors:
        print(error)
    print(f"Skill links: {len(sources)} Markdown files, {local_count} local destinations, "
          f"{fragment_count} checked fragments, {sum(seen.values())} documented template links; "
          f"{len(errors)} error(s).")
    return bool(errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="repository root (defaults to this script's parent repository)")
    return int(check(parser.parse_args().root))


if __name__ == "__main__":
    raise SystemExit(main())
