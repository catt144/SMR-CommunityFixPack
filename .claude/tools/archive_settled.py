"""archive_settled.py -- move SETTLED checklist item BODIES into the archive.

Dry run by default (prints a plan + a byte tally). `--apply` performs the move.
Run from the repo root: `python .claude/tools/archive_settled.py`.

Scope (see docs/PLAYTEST_CHECKLIST.md's "## Decisions waiting on you"):
  - a CANDIDATE is an item whose marker (the `<!-- ck:N status:S owner:O -->`
    line directly under its `### ` header) says `status:ruled` or
    `status:closed`. Unmarked items are NEVER candidates.
  - what moves is the item's BODY ONLY -- everything after the marker line up
    to (not including) the next `### ` header or the next `## ` section. The
    header + marker line ALWAYS stay in place as a stub, so every `ck<N>`
    citation into the checklist keeps resolving and `grep -c "^### "` over the
    whole file is unchanged by an apply.
  - three exclusion rules narrow candidates -> MOVE:
      (a) title-citation  -- STATE.md or a perma/*.md prompt quotes (in
          straight double quotes) a fragment of the item's header text.
      (b) register-named  -- docs/WAITING_ON_YOU.md's "Needs a marker to
          settle" section names the item (belt-and-braces: that section is
          about UNMARKED items, so a marked candidate should never appear
          there; this rule exists to prove the overlap is zero, not to do
          real work).
      (c) procedure-bearing -- the body itself contains a fenced code block
          or a 3+ line numbered step list. These are reported and counted,
          never judged.
  - ARCHIVE-OLD is a SEPARATE, REPORT-ONLY bucket: unmarked, undated-numbered
    (no bare decision number in the header), header prose not already
    closed-looking, dated before 2026-09-01 (owner ruling D4 covers this
    class, but marking is a human's call -- this tool only counts it).

Byte accounting is done on the RAW BYTES of the files (UTF-8, no re-encode
round trip for the parts that move), never on decoded character counts, so
the tally is exact even with multi-byte emoji in headers.
"""
import argparse
import glob
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from datetime import date

ROOT = os.getcwd()
CHECKLIST = "docs/PLAYTEST_CHECKLIST.md"
ARCHIVE = "docs/archive/PLAYTEST_ARCHIVE.md"
STATE = "docs/agent/STATE.md"
PERMA_GLOB = "docs/agent/prompts/perma/*.md"
WAITING = "docs/WAITING_ON_YOU.md"

ARCHIVE_OLD_CUTOFF = "2026-09-01"
QUOTE_MIN_LEN = 14   # below this a quoted fragment is too generic to trust
                      # (measured: 10 pulled in "unemployment", "nothing owed"
                      # as noise on unmarked/non-candidate headers; 14 keeps
                      # the known "THE SITTING RAN" case -- 15 chars -- while
                      # dropping those two)

sys.path.insert(0, "tools")
try:
    import doccheck
except ImportError:
    print("RED  could not import tools/doccheck.py -- run this from the repo root.")
    sys.exit(2)


# --------------------------------------------------------------------------
# Byte-exact line/offset helpers. Everything that touches the two files this
# tool reads or writes works on raw bytes; text decoding is only used to
# APPLY regexes (header text, marker text, quote hunting), never to rebuild
# the bytes that get written back out.
# --------------------------------------------------------------------------

def load_lines(path):
    """-> (raw_bytes, eol_bytes, [line_bytes...], [offset_of_each_line...]).

    Lines split on LF, with one trailing CR stripped per line, so a file with
    MIXED endings keeps every line. The old loader split on CRLF whenever the
    file held any: a lone-LF line then glued onto its neighbour, its `### `
    header vanished, and the header-count invariant refused every run
    (2026-09-16). eol_bytes is the DOMINANT ending, used only for the bytes this
    tool writes. offsets has one extra trailing entry = len(raw_bytes), and
    raw_bytes[offsets[i]:offsets[i+1]] always reproduces line i plus its own
    original ending (or nothing, for a last line with none).
    """
    with open(path, "rb") as fh:
        raw = fh.read()
    crlf = raw.count(b"\r\n")
    eol = b"\r\n" if crlf > raw.count(b"\n") - crlf else b"\n"
    parts = raw.split(b"\n")
    lines = [p[:-1] if p.endswith(b"\r") else p for p in parts]
    offsets = [0] * (len(parts) + 1)
    pos = 0
    for i, p in enumerate(parts):
        offsets[i] = pos
        pos += len(p)
        if i < len(parts) - 1:
            pos += 1
    offsets[len(parts)] = pos
    assert offsets[-1] == len(raw), "line-offset bookkeeping is broken"
    return raw, eol, lines, offsets


def slice_bytes(raw, offsets, start_idx, stop_idx):
    """Raw bytes spanning 0-indexed lines [start_idx, stop_idx) -- byte-exact."""
    return raw[offsets[start_idx]:offsets[stop_idx]]


# --------------------------------------------------------------------------
# Checklist item model -- reuse tools/doccheck.py's own parser (same section
# boundaries, same fencing rules, same marker regex) so this tool can never
# quietly disagree with doccheck about what a header or a marker says.
# --------------------------------------------------------------------------

def section_bounds(text_lines):
    """0-indexed (start, end) of the '## Decisions waiting on you' section,
    replicated from doccheck.checklist_items() so we can locate the section
    end (doccheck doesn't expose it)."""
    start = next(i for i, l in enumerate(text_lines) if l.startswith(doccheck.CK_SECTION))
    end = next((i for i in range(start + 1, len(text_lines)) if text_lines[i].startswith("## ")),
               len(text_lines))
    return start, end


def build_items(raw, eol, lines_b):
    """-> list of item dicts: doccheck's own fields plus byte-exact indices.

    header_idx   0-indexed line of the '### ' header (stays forever)
    marker_idx   0-indexed line of the marker comment, or None
    body_start   0-indexed line where the movable body begins
    stop_idx     0-indexed line where the item ends (next header, or section end)
    """
    items = doccheck.checklist_items()
    if items is None:
        print("RED  could not find '## Decisions waiting on you' in %s" % CHECKLIST)
        sys.exit(2)
    text_lines = [l.decode("utf-8", "replace") for l in lines_b]
    _, section_end = section_bounds(text_lines)
    for k, it in enumerate(items):
        header_idx = it["line"] - 1
        it["header_idx"] = header_idx
        it["stop_idx"] = (items[k + 1]["line"] - 1) if k + 1 < len(items) else section_end
        marker_idx = None
        if it["marker"]:
            for off in range(1, 5):
                if header_idx + off >= len(text_lines):
                    break
                if doccheck.MARKER_RE.search(text_lines[header_idx + off]):
                    marker_idx = header_idx + off
                    break
        it["marker_idx"] = marker_idx
        it["body_start"] = (marker_idx + 1) if marker_idx is not None else (header_idx + 1)
        it["is_candidate"] = bool(it["marker"] and it["marker"]["status"] in ("ruled", "closed"))
    return items, section_end


# --------------------------------------------------------------------------
# Exclusion rule (a): title-citation. STATE.md / perma/*.md quote a fragment
# of the item's header in straight double quotes.
# --------------------------------------------------------------------------

def title_citation_sources():
    paths = [STATE] + sorted(glob.glob(PERMA_GLOB))
    quotes = []   # (fragment, source_path)
    for p in paths:
        if not os.path.exists(p):
            continue
        text = open(p, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r'"([^"\n]{%d,})"' % QUOTE_MIN_LEN, text):
            quotes.append((m.group(1), p))
    return quotes


def number_citation_blob():
    """-> one text blob of STATE.md + every perma/ prompt.

    Rule (d) asks a different question from rule (a): not "is this item's
    TITLE quoted" but "is its NUMBER cited". STATE.md line 43 reads
    "RULED 09-12, bodies in the checklist, do not re-derive: 162 . 163 ...",
    which pins those BODIES by number and matches no header text at all.
    Archiving one of those moves it behind the docs/archive/ .rgignore
    boundary, so an agent following STATE greps the checklist, finds a stub,
    and a default rg never sees the body -- exactly the silent failure the
    boundary rider exists to prevent, aimed at the owner's own rulings.

    Deliberately permissive: a false KEEP costs nothing but bytes, a false
    MOVE destroys a decision record.
    """
    paths = [STATE] + sorted(glob.glob(PERMA_GLOB))
    blob = []
    for p in paths:
        if os.path.exists(p):
            blob.append(open(p, encoding="utf-8", errors="replace").read())
    return chr(10).join(blob)


# A number counts as a citation only when it is NAMED as a checklist item.
# The first version matched any standalone token, so a commit hash (`153d180`),
# a count ("40 sols", "59 -> 34"), a bug id (C98, F73) or a file name
# (`73_SMRTK_Infopanel.lua`) pinned an unrelated item: on 2026-09-16 six of the
# nine remaining pins, 32,863 B, were such coincidences.
_NAMED_CK_RE = re.compile(r"(?<![A-Za-z])ck\*{0,2}(\d+)", re.I)
_NAMED_WORD_RE = re.compile(
    r"\b(?:checklist|items?|decisions?)\*{0,2}\s+\*{0,2}"
    r"(\d+(?:\*{0,2}\s*(?:/|,|–|-|\+|&|and)\s*\*{0,2}\d+)*)", re.I)
_HASH_RE = re.compile(r"(?<![\w&])#(\d+)\b")
# STATE's owner-register idioms list bare item numbers; WAITING_ON_YOU parses them.
_IDIOM_LINE_RE = re.compile(r"STILL OPEN:|Owner OWES:")
_BARE_NUM_RE = re.compile(r"(?<![\w.§])(\d+)(?![\w.])")
_cited_cache = {}


def cited_numbers(blob):
    if blob in _cited_cache:
        return _cited_cache[blob]
    found = set(_NAMED_CK_RE.findall(blob)) | set(_HASH_RE.findall(blob))
    for run in _NAMED_WORD_RE.findall(blob):
        found.update(re.findall(r"\d+", run))
    for line in blob.split("\n"):
        if _IDIOM_LINE_RE.search(line):
            found.update(_BARE_NUM_RE.findall(line))
    found = {n.lstrip("0") or "0" for n in found}
    _cited_cache[blob] = found
    return found


def cited_by_number(num, blob):
    """True if this decision number is cited AS a checklist item (see above)."""
    num = str(num) if num is not None else ''
    if not num or not num.isdigit():
        return False
    return (num.lstrip("0") or "0") in cited_numbers(blob)


def rule_a_matches(items, quotes):
    """-> {header_idx: [(fragment, source), ...]} over ALL items (not just
    candidates) -- this rule is an audit net first, a candidate filter
    second, so an unmarked item that STATE depends on still shows up."""
    hits = {}
    for it in items:
        header_text = it["header"]
        for fragment, source in quotes:
            if fragment in header_text:
                hits.setdefault(it["header_idx"], []).append((fragment, source))
    return hits


# --------------------------------------------------------------------------
# Exclusion rule (b): register-named in WAITING_ON_YOU.md's
# "Needs a marker to settle" section (belt-and-braces -- see module docstring).
# --------------------------------------------------------------------------

def waiting_needs_marker_lines():
    if not os.path.exists(WAITING):
        return set()
    text = open(WAITING, encoding="utf-8", errors="replace").read()
    m = re.search(r"## Needs a marker to settle.*?(?=\n## |\Z)", text, re.S)
    if not m:
        return set()
    return set(int(n) for n in re.findall(r"PLAYTEST_CHECKLIST\.md#L(\d+)", m.group(0)))


# --------------------------------------------------------------------------
# Exclusion rule (c): procedure-bearing -- a fenced code block, or a 3+ line
# numbered step list, inside the body that would move.
# --------------------------------------------------------------------------

NUMBERED_STEP_RE = re.compile(r"^\d+\.\s")


def body_text(raw, offsets, eol, body_start, stop_idx):
    return slice_bytes(raw, offsets, body_start, stop_idx).decode("utf-8", "replace")


def is_procedure_bearing(body):
    if "```" in body:
        return True, "fenced code block"
    steps = 0
    for line in body.split("\n"):
        stripped = re.sub(r"^[>\s]+", "", line)
        if NUMBERED_STEP_RE.match(stripped):
            steps += 1
    if steps >= 3:
        return True, "%d-step numbered list" % steps
    return False, ""


# --------------------------------------------------------------------------
# ARCHIVE-OLD -- reported-only bucket, never moved by this tool.
# --------------------------------------------------------------------------

def is_archive_old(it):
    return (not it["marker"] and it["num"] is None and not it["prose_closed"]
            and it["date"] and it["date"] < ARCHIVE_OLD_CUTOFF)


# --------------------------------------------------------------------------
# doccheck / git safety rails
# --------------------------------------------------------------------------

def doccheck_is_green():
    try:
        out = subprocess.check_output([sys.executable, "tools/doccheck.py"],
                                       stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        out = exc.output
    text = out.decode("utf-8", "replace")
    last = [l for l in text.splitlines() if l.strip()]
    ok = bool(last) and last[-1].strip() == "doccheck: GREEN"
    return ok, text


def git_is_clean():
    out = subprocess.check_output([
        "git", "status", "--porcelain", "--", CHECKLIST, ARCHIVE
    ]).decode("utf-8", "replace")
    return out.strip() == "", out


# --------------------------------------------------------------------------
# Archive rendering -- matches the existing '## <label> ...' + '---' section
# convention already used in docs/archive/PLAYTEST_ARCHIVE.md (see e.g. its
# "Resolved decision records" section). Body bytes are copied byte-exact;
# only the small dated header line + separator around them are new text.
# --------------------------------------------------------------------------

def full_heading(it):
    """The checklist heading exactly as written, minus its `###` level.

    ck180 (approved 2026-09-14): the archive heading used to go through
    doccheck._ask(), a register helper that drops the date, strips brackets and
    pipes, and cuts at 200 characters. `ck139` was cut mid-word. The archive is
    append-only, so a lossy heading can never be corrected after the fact.
    """
    return re.sub(r"^#+\s*", "", it["header"]).strip()


def archive_heading_prefix(it, today):
    label = "ck%s" % it["num"] if it["num"] is not None else "ck-"
    return "## %s -- archived %s (was checklist status:%s): " % (
        label, today, it["marker"]["status"])


def archive_entry_bytes(it, body_bytes, eol, today):
    header_line = archive_heading_prefix(it, today) + full_heading(it)
    prefix = eol.join([b"", b"---", b"", header_line.encode("utf-8"), b""]) + eol
    # body_bytes already ends with its own trailing eol (it runs up to, not
    # including, the next header/section line), so no extra eol is added
    # after it -- appending is a pure concatenation.
    return prefix + body_bytes


def stub_pointer_bytes(it, eol, today):
    """ck180 (approved 2026-09-14): the old pointer said "search `ck-` and this
    heading", which found nothing -- the archive heading had lost its date, and
    `ck-` is shared by most unnumbered items. The pointer now quotes the exact
    prefix of the archive heading, which is followed by this item's heading
    verbatim, so one search for that prefix plus the heading lands on the body."""
    text = ('Body archived in [archive/PLAYTEST_ARCHIVE.md]'
            '(archive/PLAYTEST_ARCHIVE.md) under the heading "%s" followed by '
            'this heading.' % archive_heading_prefix(it, today).rstrip())
    return eol + text.encode("utf-8") + eol + eol


STUB_MAX_BYTES = 800


def is_pointer_stub(body):
    """True for a body that is only a pointer into the archive.

    The tool used to recognise its own stubs byte for byte, which missed every
    stub written by hand in other wording ("Owner ruling archived in [...]") and
    would have archived the pointer itself, leaving a pointer to a pointer. It
    also would have stopped recognising its own 35 stubs the moment the pointer
    wording changed. A false KEEP here costs only bytes; a false MOVE archives a
    stub, so the test is deliberately loose.
    """
    text = body.strip()
    return (len(text.encode("utf-8")) <= STUB_MAX_BYTES
            and "archive/PLAYTEST_ARCHIVE.md" in text)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                     help="perform the move (default is dry run / report only)")
    ap.add_argument("--headers-file", help="JSON list of exact reviewed headings; refuse missing/ineligible members")
    args = ap.parse_args()

    # A piped Windows console is cp1252; doccheck output carries non-ASCII, and
    # printing it crashed the RED refusal itself (2026-09-16).
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    if not os.path.exists("tools/doccheck.py"):
        print("RED  run this from the repo root (tools/doccheck.py not found here).")
        return 2

    ok, doccheck_out = doccheck_is_green()
    if not ok:
        print("RED  tools/doccheck.py is not GREEN -- refusing to run at all.")
        print(doccheck_out[-2000:])
        return 1

    raw, eol, lines_b, offsets = load_lines(CHECKLIST)
    checklist_sha = hashlib.sha256(raw).digest()
    items, section_end = build_items(raw, eol, lines_b)

    quotes = title_citation_sources()
    a_hits = rule_a_matches(items, quotes)
    b_lines = waiting_needs_marker_lines()

    candidates = [it for it in items if it["is_candidate"]]
    archive_old = [it for it in items if is_archive_old(it)]

    rows = []           # for the per-item table
    move_items = []      # candidates that actually move
    excl_a = excl_b = excl_c = excl_d = 0
    num_blob = number_citation_blob()
    selected = None
    if args.headers_file:
        with open(args.headers_file, encoding="utf-8") as fh:
            selection = json.load(fh)
        if (not isinstance(selection, list) or not selection
                or any(not isinstance(h, str) for h in selection)
                or len(set(selection)) != len(selection)):
            print("RED  selection must be a nonempty JSON list of unique headings.")
            return 1
        selected = set(selection)
    d_details = []
    c_details = []

    for it in items:
        body = body_text(raw, offsets, eol, it["body_start"], it["stop_idx"])
        body_bytes_n = len(slice_bytes(raw, offsets, it["body_start"], it["stop_idx"]))
        status_label = it["marker"]["status"] if it["marker"] else "unmarked"

        if is_pointer_stub(body):
            rows.append((it["num"], status_label, body_bytes_n, "KEEP-archived"))
            continue

        if selected is not None and it["header"] not in selected:
            rows.append((it["num"], status_label, body_bytes_n, "KEEP-unselected"))
            continue

        if not it["is_candidate"]:
            decision = "KEEP-archive-old" if is_archive_old(it) else "KEEP-unmarked"
            rows.append((it["num"], status_label, body_bytes_n, decision))
            continue

        hit_a = it["header_idx"] in a_hits
        # b_lines holds 1-indexed checklist line numbers pulled from
        # WAITING_ON_YOU's own '#L<N>' anchors -- compare like for like
        # (it["line"] is the header's 1-indexed line), never against the
        # decision number itself (a 2-3 digit ck# could collide by chance
        # with an unrelated large line number).
        hit_b = it["line"] in b_lines
        proc, why = is_procedure_bearing(body)

        hit_d = cited_by_number(it.get("num"), num_blob)

        if hit_a:
            excl_a += 1
            decision = "KEEP-a"
        elif hit_d:
            excl_d += 1
            d_details.append((it["num"], body_bytes_n))
            decision = "KEEP-d"
        elif hit_b:
            excl_b += 1
            decision = "KEEP-b"
        elif proc:
            excl_c += 1
            c_details.append((it["num"], why, body_bytes_n))
            decision = "KEEP-c"
        else:
            decision = "MOVE"
            move_items.append((it, body_bytes_n))

        rows.append((it["num"], status_label, body_bytes_n, decision))

    if selected is not None and (len(move_items) != len(selected)
            or {it["header"] for it, _ in move_items} != selected):
        print("RED  selection rail: missing, duplicate or ineligible headings -- refusing.")
        for heading in sorted(selected - {it["header"] for it, _ in move_items}):
            print(heading)
        return 1

    archived_bytes = sum(n for _, n in move_items)
    live_before = len(raw)

    # Build the new checklist bytes (cut every MOVE body out, header+marker
    # left in place) and the archive addendum -- entirely in memory; nothing
    # is written unless --apply, and even then only after the tally holds.
    today = date.today().isoformat()
    move_by_start = {it["body_start"]: (it, n) for it, n in move_items}
    new_checklist_parts = []
    archive_addendum = []
    cursor = 0
    # Walk items in document order so cuts are applied left-to-right.
    for it in items:
        if it["body_start"] in move_by_start:
            new_checklist_parts.append(raw[cursor:offsets[it["body_start"]]])
            new_checklist_parts.append(stub_pointer_bytes(it, eol, today))
            body_bytes = slice_bytes(raw, offsets, it["body_start"], it["stop_idx"])
            archive_addendum.append(archive_entry_bytes(it, body_bytes, eol, today))
            cursor = offsets[it["stop_idx"]]
    new_checklist_parts.append(raw[cursor:])
    new_checklist = b"".join(new_checklist_parts)
    addendum_bytes = b"".join(archive_addendum)

    pointer_bytes = sum(len(stub_pointer_bytes(it, eol, today)) for it, _ in move_items)
    live_after_predicted = live_before - archived_bytes + pointer_bytes
    balances = (len(new_checklist) == live_after_predicted)

    archive_raw = open(ARCHIVE, "rb").read() if os.path.exists(ARCHIVE) else b""
    archive_sha = hashlib.sha256(archive_raw).digest()
    archive_before = len(archive_raw)
    archive_after_predicted = archive_before + len(addendum_bytes)

    # header-count invariant, checked either way
    header_count_before = sum(1 for l in lines_b if l.startswith(b"### "))
    header_count_after = sum(1 for l in new_checklist.split(b"\n") if l.startswith(b"### "))
    if header_count_after != header_count_before:
        print("RED  header-count invariant failed -- refusing.")
        return 1

    # ---------------- report ----------------
    print("doccheck: GREEN (checked before running)")
    print()
    print("Items in 'Decisions waiting on you': %d" % len(items))
    print("Candidates (marker status:ruled/closed): %d  (ruled %d, closed %d)"
          % (len(candidates),
             sum(1 for it in candidates if it["marker"]["status"] == "ruled"),
             sum(1 for it in candidates if it["marker"]["status"] == "closed")))
    print("  excluded (a) title-citation : %d" % excl_a)
    print("  excluded (d) number-cited   : %d  (%d B -- STATE/perma pin these bodies)"
          % (excl_d, sum(n for _, n in d_details)))
    print("  excluded (b) register-named : %d" % excl_b)
    print("  excluded (c) procedure-bearing: %d" % excl_c)
    print("  actually movable            : %d" % len(move_items))
    print()
    print("Rule (a) title-citation matches (audit over ALL %d items, not just candidates):"
          % len(items))
    if a_hits:
        for it in items:
            if it["header_idx"] in a_hits:
                frag, src = a_hits[it["header_idx"]][0]
                cand = "candidate" if it["is_candidate"] else "unmarked/other"
                print("  ck%-4s [%s] matched %r from %s -- header: %s"
                      % (it["num"] if it["num"] is not None else "-", cand, frag, src,
                         doccheck._ask(it["header"], 70)))
    else:
        print("  (none)")
    print()
    print("Rule (b) register-named: WAITING_ON_YOU 'Needs a marker to settle' "
          "names %d line(s)/number(s); overlap with candidates = %d (expected 0)."
          % (len(b_lines), excl_b))
    print()
    print("Rule (c) procedure-bearing candidates:")
    if c_details:
        for num, why, n in c_details:
            print("  ck%-4s %s (%d B)" % (num if num is not None else "-", why, n))
    else:
        print("  (none)")
    print()
    print("ARCHIVE-OLD (report-only; unmarked, no header number, prose not "
          "closed-looking, dated before %s): %d items, %d B"
          % (ARCHIVE_OLD_CUTOFF, len(archive_old),
             sum(len(slice_bytes(raw, offsets, it["body_start"], it["stop_idx"]))
                 for it in archive_old)))
    print("  (owner ruling D4 covers this class; NOT moved by this tool)")
    print()
    print("Per-item table (ck#, status, body bytes, decision):")
    print("%-6s %-10s %8s  %s" % ("ck#", "status", "bytes", "decision"))
    for num, status_label, n, decision in rows:
        print("%-6s %-10s %8d  %s" % (num if num is not None else "-", status_label, n, decision))
    print()
    print("---- TALLY (bytes) ----")
    print("checklist live before      : %d" % live_before)
    print("archived (sum of MOVE body): %d" % archived_bytes)
    print("checklist live after (pred): %d" % live_after_predicted)
    print("checklist live after (built): %d" % len(new_checklist))
    print("stub pointers added       : %d" % pointer_bytes)
    print("balance check: live before (%d) + pointers (%d) == live after (%d) + archived (%d) -> %s"
          % (live_before, pointer_bytes, len(new_checklist), archived_bytes, balances))
    print()
    print("archive before  : %d B" % archive_before)
    print("archive addendum: %d B (includes %d B of new per-item archive headers)"
          % (len(addendum_bytes), len(addendum_bytes) - archived_bytes))
    print("archive after (projected): %d B" % archive_after_predicted)
    print()
    print("header-count invariant: %d '### ' headers before this run (grep -c \"^### \" "
          "docs/PLAYTEST_CHECKLIST.md should read the same after an apply)."
          % header_count_before)

    if not balances:
        print()
        print("RED  byte tally does not balance -- refusing to apply.")
        return 1

    if not args.apply:
        print()
        print("Dry run only -- nothing written. Re-run with --apply to perform the move.")
        return 0

    # ------------- apply -------------
    clean, git_out = git_is_clean()
    if not clean:
        print()
        print("RED  write-path cleanliness rail blocked -- refusing to apply.")
        print("Checked paths: %s, %s; dirty paths:" % (CHECKLIST, ARCHIVE))
        print(git_out)
        return 1

    if not move_items:
        print()
        print("Nothing to move (0 candidates cleared every exclusion) -- not writing.")
        return 0

    def atomic_write(path, data):
        tmp = path + ".tmp-archive-settled"
        with open(tmp, "wb") as fh:
            fh.write(data)
        os.replace(tmp, path)

    # Check both captured files before the first mutation. In particular a peer
    # commit after load can leave git clean while invalidating our planned bytes.
    for path, expected in ((CHECKLIST, checklist_sha), (ARCHIVE, archive_sha)):
        current = open(path, "rb").read() if os.path.exists(path) else b""
        if hashlib.sha256(current).digest() != expected:
            print("RED  SHA256 load-to-write rail: %s changed -- refusing to apply." % path)
            return 1
    atomic_write(ARCHIVE, archive_raw + addendum_bytes)
    atomic_write(CHECKLIST, new_checklist)
    print()
    print("APPLIED: moved %d item bodies, %d B, into %s" % (len(move_items), archived_bytes, ARCHIVE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
