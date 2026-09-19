"""Open the Paradox store description as a formatted page, ready to copy.

The Paradox Mods page stores its description as HTML, so the plain text the
upload fills in arrives with no heading, no bold and no line breaks
(docs/UPLOAD_WORKFLOW.md §3). This reads the Paradox block from that file and
opens it in the browser in the owner's page format (2026-09-19): the first line
as the one heading, each ALL-CAPS section line in bold, and every other line
exactly as written, line breaks and blank lines included. No bold inside the
paragraphs and no font of its own, so the paste takes the editor's font.
Select all, copy, paste into the Paradox editor.

Nothing is stored: the page is rebuilt from UPLOAD_WORKFLOW.md on every run, so
it cannot drift from the maintained block.

    python tools/paradox_card.py            build and open the page
    python tools/paradox_card.py --check    build only; print the headings
"""
import html
import io
import os
import re
import sys
import tempfile
import webbrowser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(ROOT, "docs", "UPLOAD_WORKFLOW.md")
PARADOX_HEADING = "#### 📋 Paradox Mods — description (plain text, paste as-is)"
URL_RE = re.compile(r"https?://\S+")


def fenced_block(text, heading):
    i = text.index(heading)
    a = text.index("```\n", i) + 4
    return text[a:text.index("\n```", a)]


def is_section(line):
    s = line.strip()
    return s == s.upper() and re.search(r"[A-Z]{3}", s) is not None


def build():
    plain = fenced_block(io.open(WORKFLOW, encoding="utf-8").read(), PARADOX_HEADING)
    lines = plain.split("\n")
    body, sections = [f"<h3>{html.escape(lines[0].strip())}</h3>"], []
    # One paragraph per source line, an empty one per blank line: the same shape
    # as pressing Enter at the end of every line in the editor.
    for line in lines[1:]:
        if not line.strip():
            body.append("<p><br></p>")
        elif is_section(line):
            sections.append(line.strip())
            body.append(f"<p><strong>{html.escape(line.strip())}</strong></p>")
        else:
            text = URL_RE.sub(lambda m: f'<a href="{m.group(0)}">{m.group(0)}</a>',
                              html.escape(line.rstrip()))
            body.append(f"<p>{text}</p>")
    page = ("<!doctype html><html><head><meta charset='utf-8'>"
            "<title>Paradox description</title></head><body>"
            + "\n".join(body) + "</body></html>")
    return page, lines[0].strip(), sections


def main():
    page, title, sections = build()
    print("heading:", title)
    print("bold section lines:", ", ".join(sections))
    if "--check" in sys.argv:
        return
    path = os.path.join(tempfile.gettempdir(), "smr_paradox_description.html")
    io.open(path, "w", encoding="utf-8").write(page)
    print("opened", path)
    print("In the browser: Ctrl+A, Ctrl+C. In the Paradox editor: select all, paste.")
    webbrowser.open("file:///" + path.replace("\\", "/"))


if __name__ == "__main__":
    main()
