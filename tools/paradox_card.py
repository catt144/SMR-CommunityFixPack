"""Open the Paradox store description as a formatted page, ready to copy.

The Paradox Mods page stores its description as HTML, so the plain text the
upload fills in arrives with no headings, no bold and no paragraph breaks
(docs/UPLOAD_WORKFLOW.md §3). This reads the Paradox block from that file and
opens it in the browser already formatted: the title and the ALL-CAPS section
lines as headings, `·` lines as a list, links clickable, and bold on the same
phrases the Steam block bolds. Select all, copy, paste into the Paradox editor.

Nothing is stored: the page is rebuilt from UPLOAD_WORKFLOW.md on every run, so
it cannot drift from the maintained block.

    python tools/paradox_card.py            build and open the page
    python tools/paradox_card.py --check    build only; print what was bolded
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
STEAM_HEADING = "#### 📋 Steam Workshop — description (BBCode, paste as-is)"
URL_RE = re.compile(r"https?://\S+")


def fenced_block(text, heading):
    i = text.index(heading)
    a = text.index("```\n", i) + 4
    return text[a:text.index("\n```", a)]


def steam_emphasis(steam):
    """(context, phrase, tag) for each [b]/[i] in the Steam block, where context is
    the plain text just before the tag, used to find the same spot in the Paradox text."""
    out = []
    for m in re.finditer(r"\[(b|i)\](.+?)\[/\1\]", steam):
        before = re.sub(r"\[[^\]]*\]", "", steam[max(0, m.start() - 60):m.start()])
        before = before.split("\n")[-1][-20:]
        phrase = re.sub(r"\[[^\]]*\]", "", m.group(2))
        out.append((before, phrase, "strong" if m.group(1) == "b" else "em"))
    return out


def parse(plain):
    """Plain block -> list of (kind, text): h1, h2, p, li."""
    blocks, para, items = [], [], []

    def flush():
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()
        if items:
            blocks.append(("ul", list(items)))
            items.clear()

    lines = plain.split("\n")
    for n, line in enumerate(lines):
        s = line.strip()
        if not s:
            flush()
        elif n == 0:
            blocks.append(("h1", s))
        elif s == s.upper() and re.search(r"[A-Z]{3}", s):
            flush()
            blocks.append(("h2", s))
        elif s.startswith("· "):
            if para:
                blocks.append(("p", " ".join(para)))
                para.clear()
            items.append(s[2:])
        elif items and line.startswith("  "):
            items[-1] += " " + s
        else:
            if items:
                blocks.append(("ul", list(items)))
                items.clear()
            para.append(s)
    flush()
    return blocks


def render(text, marks, used):
    """Escape, then apply emphasis at the Steam-matched spots, then link URLs."""
    spans = []
    for k, (before, phrase, tag) in enumerate(marks):
        if k in used:
            continue
        at = text.find(before + phrase) if before.strip() else -1
        if at >= 0:
            at += len(before)
        elif text.startswith(phrase):
            at = 0
        if at >= 0 and not any(a < at + len(phrase) and at < b for a, b, _ in spans):
            spans.append((at, at + len(phrase), tag))
            used.add(k)
    out, pos = [], 0
    for a, b, tag in sorted(spans):
        out.append(html.escape(text[pos:a]))
        out.append(f"<{tag}>{html.escape(text[a:b])}</{tag}>")
        pos = b
    out.append(html.escape(text[pos:]))
    joined = "".join(out)
    return URL_RE.sub(lambda m: f'<a href="{m.group(0)}">{m.group(0)}</a>', joined)


def build():
    text = io.open(WORKFLOW, encoding="utf-8").read()
    plain = fenced_block(text, PARADOX_HEADING)
    marks = steam_emphasis(fenced_block(text, STEAM_HEADING))
    used, body = set(), []
    for kind, content in parse(plain):
        if kind == "ul":
            lis = "".join(f"<li>{render(c, marks, used)}</li>" for c in content)
            body.append(f"<ul>{lis}</ul>")
        else:
            body.append(f"<{kind}>{render(content, marks, used)}</{kind}>")
    page = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Paradox description — copy all</title>"
        "<style>body{font-family:sans-serif;max-width:46em;margin:2em auto;line-height:1.5}"
        "</style></head><body>"
        + "\n".join(body) + "</body></html>"
    )
    missed = [marks[k][1] for k in range(len(marks)) if k not in used]
    bolded = [marks[k][1] for k in sorted(used)]
    return page, bolded, missed


def main():
    page, bolded, missed = build()
    print("emphasised:", ", ".join(bolded) or "(none)")
    if missed:
        print("Steam emphasis with no match in the Paradox text (left plain):", ", ".join(missed))
    if "--check" in sys.argv:
        return
    path = os.path.join(tempfile.gettempdir(), "smr_paradox_description.html")
    io.open(path, "w", encoding="utf-8").write(page)
    print("opened", path)
    print("In the browser: Ctrl+A, Ctrl+C. In the Paradox editor: select all, paste.")
    webbrowser.open("file:///" + path.replace("\\", "/"))


if __name__ == "__main__":
    main()
