#!/usr/bin/env python3
"""Read-only provenance leads, not automatic build classification.

Print JSON with --inventory. Every body line retains its blame commit and date;
version mentions are leads even when negated or historical. --selftest must pass
before producing inventory. No inference from updated: and no fact writes.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def split_fact(text):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing front matter")
    end = lines.index("---", 1)
    pins = [line[len("derived_at:"):].strip().strip('"')
            for line in lines[1:end] if line.startswith("derived_at:")]
    if len(pins) != 1:
        raise ValueError("missing or duplicate derived_at")
    return pins[0], end + 2, lines[end + 1:]


def blame_rows(text):
    rows, current = [], None
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{40}) (\d+) (\d+)(?: (\d+))?", line)
        if match:
            current = {"sha": match[1], "line": int(match[3])}
        elif line.startswith("author-time "):
            current["author_date"] = datetime.fromtimestamp(
                int(line.split()[1]), timezone.utc).isoformat()
        elif line.startswith("committer-time "):
            current["date"] = datetime.fromtimestamp(
                int(line.split()[1]), timezone.utc).isoformat()
        elif line.startswith("filename "):
            current["origin"] = line[9:]
        elif line.startswith("\t"):
            if not current or "date" not in current or "origin" not in current:
                raise ValueError("incomplete blame record")
            rows.append(dict(current, text=line[1:]))
            current = None
    return rows


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8")


def inventory():
    result = {"head": git("rev-parse", "HEAD").strip(), "facts": []}
    for path in sorted((ROOT / "docs/agent/facts").glob("EF-*.md")):
        text = path.read_text(encoding="utf-8-sig")
        pin, start, body = split_fact(text)
        relative = path.relative_to(ROOT).as_posix()
        rows = blame_rows(git("blame", "--line-porcelain", "--", relative))
        body_rows = [row for row in rows if row["line"] >= start]
        if [row["text"] for row in body_rows] != body:
            raise ValueError("blame/body mismatch: " + relative)
        result["facts"].append({
            "id": path.stem, "pin": pin, "body_start": start,
            "body_sha256_lf": hashlib.sha256("\n".join(body).encode()).hexdigest(),
            "rows": body_rows,
        })
    result["count"] = len(result["facts"])
    return result


def selftest():
    pin, start, body = split_fact(
        '---\r\nupdated: "2099-01-01"\r\nderived_at: "old (inferred)"\r\n---\r\n'
        'Not measured on 1.1.0.\r\nSource is 1.0.7.\r\n')
    assert (pin, start, body) == ("old (inferred)", 5,
                                ["Not measured on 1.1.0.", "Source is 1.0.7."])
    sha = "a" * 40
    fixture = (sha + " 9 5 2\nauthor-time 0\ncommitter-time 172800\nfilename old/fact.md\n\t" + body[0] +
               "\n" + sha + " 10 6\nauthor-time 86400\ncommitter-time 259200\nfilename old/fact.md\n\t" + body[1])
    rows = blame_rows(fixture)
    assert [r["line"] for r in rows] == [5, 6]
    assert [r["text"] for r in rows] == body
    assert rows[0]["author_date"].startswith("1970-01-01")
    assert rows[0]["date"].startswith("1970-01-03")
    assert rows[1]["date"].startswith("1970-01-04")
    for malformed in ('---\nderived_at: "x"\n',
                      '---\nderived_at: "x"\nderived_at: "y"\n---\n'):
        try:
            split_fact(malformed)
        except ValueError:
            pass
        else:
            raise AssertionError("bad fact accepted")
    try:
        blame_rows(sha + " 1 1\n\tno provenance")
    except ValueError:
        pass
    else:
        raise AssertionError("missing provenance accepted")


def summary(data):
    inferred = [f for f in data["facts"] if "(inferred" in f["pin"]]
    old = [f for f in inferred if f["pin"].startswith("game 1.0.7.396349")]
    late = [(f["id"], row["line"], row["sha"])
            for f in old for row in f["rows"]
            if row["text"].strip() and row["date"] >= "2026-09-08"]
    print("HEAD " + data["head"])
    print("FACT PROVENANCE: %d facts; %d inferred; %d old-build inferred; "
          "%d nonblank old-build body lines committed on/after 2026-09-08" %
          (data["count"], len(inferred), len(old), len(late)))
    for fact in inferred:
        row = max((r for r in fact["rows"] if r["text"].strip()),
                  key=lambda r: r["date"])
        print("%s | %s | latest body %s %s | %s" %
              (fact["id"], fact["pin"], row["date"][:10], row["sha"],
               fact["body_sha256_lf"]))
    for row in late:
        print("POST-UPDATE BODY LINE " + repr(row))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    selftest()
    if args.inventory:
        print(json.dumps(inventory(), ensure_ascii=True, indent=2))
    elif args.summary:
        summary(inventory())
    else:
        print("PROVENANCE SELFTEST: PASS (CRLF, misleading dates/versions, blame mapping, malformed input)")
