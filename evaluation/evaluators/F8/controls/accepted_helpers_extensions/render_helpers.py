"""Alternate local rendering helper, preserving every positional line."""
def render_lines(lines):
    return "".join(line + "\n" for line in lines)
