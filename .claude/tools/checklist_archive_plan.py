"""Task-local reproducible selection for CHECKLIST_ARCHIVE (raw bytes)."""
import importlib.util
import json
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location('archive_settled', '.claude/tools/archive_settled.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def derive():
    raw, eol, lines, offsets = a.load_lines(a.CHECKLIST)
    items, _ = a.build_items(raw, eol, lines)
    hits = a.rule_a_matches(items, a.title_citation_sources())
    blob = a.number_citation_blob()
    groups = {1: [], 2: []}
    for it in items:
        if it['marker']:
            continue
        done = re.search(r'\u2705|RULED|CLOSED|DONE|RAN|LANDED|DISCHARGED', it['header'])
        if not (done or (it['date'] and it['date'] < '2026-09-08')):
            continue
        if it['header_idx'] in hits or a.cited_by_number(it['num'], blob):
            continue
        body = a.slice_bytes(raw, offsets, it['body_start'], it['stop_idx'])
        proc, _ = a.is_procedure_bearing(body.decode('utf-8'))
        if proc:
            continue
        groups[1 if done else 2].append(dict(it, body_bytes=len(body)))
    return raw, eol, offsets, groups


if __name__ == '__main__':
    raw, eol, offsets, groups = derive()
    print(json.dumps(groups, ensure_ascii=False, indent=2))
