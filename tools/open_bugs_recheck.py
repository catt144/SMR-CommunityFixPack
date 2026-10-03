#!/usr/bin/env python3
"""Reconcile the 2026-10-02 open-bug recheck report against its firing set and entries.

Run: python tools/open_bugs_recheck.py [--selftest]
Read-only structural check, not evidence validation. The firing INDEX is the
committed 445a4d59 source named by the brief, and C122 is its added train filing.
Checks named membership, exactly one dated verdict per entry, matching report
verdicts, status disposition and the deciding-read list. Prints verdict members
and independent totals; failures identify the differing ids.
"""
from collections import Counter
from pathlib import Path
import contextlib
import io
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'docs/agent/reports/OPEN_BUGS_RECHECK_2026-10-02.md'
DATE = '2026-10-02'


def require(ok, message):
    if not ok:
        raise SystemExit('FAIL: '+message)


def main():
    baseline=subprocess.check_output(['git','show','445a4d59:docs/agent/bugs/INDEX.md'],cwd=ROOT).decode('utf-8')
    expected=set()
    for line in baseline.splitlines():
        if re.match(r'\| \d+ \|',line):
            cells=[c.strip() for c in line.strip().strip('|').split('|')]
            if cells[3].split()[0] in ('filed','cand','blocked','built','open') and cells[1]!='C121':
                expected.add(cells[1])
    require('C122' not in expected,'train filing unexpectedly in firing index')
    expected.add('C122')
    text=REPORT.read_text(encoding='utf-8')
    rows=re.findall(r'^\| \[?([FCD]\d+)(?:\]\([^)]*\))? \| ([a-z-]+) \|',text,re.M)
    ids=[i for i,v in rows]
    require(len(ids)==len(set(ids)),'duplicate report ids: '+str([i for i,n in Counter(ids).items() if n>1]))
    require(set(ids)==expected,'membership: missing '+str(sorted(expected-set(ids)))+'; extra '+str(sorted(set(ids)-expected)))
    verdicts=dict(rows)
    entry_rows=[]
    for id in sorted(expected):
        entry=(ROOT/'docs/agent/bugs'/f'{id}.md').read_text(encoding='utf-8')
        matches=re.findall(r'^#### Recheck '+DATE+r' — ([a-z-]+)$',entry,re.M)
        require(matches==[verdicts[id]],f'{id}: entry {matches} vs report {verdicts[id]}')
        tail=entry.split('#### Recheck '+DATE+' — ',1)[1]
        require('Falsifying command' in tail,f'{id}: missing command')
        status=re.search(r'^status: "(.*?)"',entry,re.M)[1]
        target={'ours-retired':'closed','vanilla-fixed':'closed','not-a-defect':'wontfix'}.get(verdicts[id])
        require(not target or status==target,f'{id}: status {status}, expected {target}')
        entry_rows.append((id,matches[0]))
    possible={i for i,v in rows if v=='possible-unconfirmed'}
    sitting=text.split('## What a sitting would decide',1)[1].split('\n## ',1)[0]
    reads=re.findall(r'^- \*\*([FCD]\d+)\*\*:',sitting,re.M)
    require(len(reads)==len(set(reads)),'duplicate deciding-read ids')
    require(set(reads)==possible,'deciding reads: missing '+str(sorted(possible-set(reads)))+'; extra '+str(sorted(set(reads)-possible)))
    for verdict in sorted(set(verdicts.values())):
        members=sorted(i for i,v in rows if v==verdict)
        print(verdict,len(members),' '.join(members))
    print('FIRING MEMBERS PLUS TRAIN',len(expected),'REPORT ROWS',len(rows),'ENTRY SECTIONS',len(entry_rows))
    print('DECIDING READS',len(reads),'POSSIBLE ROWS',len(possible))
    print('PASS: report, entry sections, statuses and deciding reads reconcile by id')


def selftest():
    global REPORT
    original=REPORT
    content=original.read_text(encoding='utf-8')
    mutants={
        'missing row': re.sub(r'^\| \[?C57(?:\]\([^)]*\))? \|[^\n]*\n','',content,count=1,flags=re.M),
        'wrong verdict': content.replace('| confirmed |','| not-a-defect |',1),
        'missing deciding read': re.sub(r'^- \*\*C122\*\*:[^\n]*\n','',content,count=1,flags=re.M),
    }
    with tempfile.TemporaryDirectory(prefix='smr-recheck-falsifier-') as folder:
        try:
            REPORT=Path(folder)/'report.md'
            for label,mutant in mutants.items():
                require(mutant!=content,'selftest mutation did not apply: '+label)
                REPORT.write_text(mutant,encoding='utf-8')
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        main()
                except SystemExit as error:
                    print('CAUGHT',label,str(error))
                else:
                    raise SystemExit('FAIL: selftest accepted '+label)
        finally:
            REPORT=original
    print('SELFTEST PASS: named membership, verdict and deciding-read mutants rejected')


if __name__=='__main__':
    main()
    if '--selftest' in sys.argv:
        selftest()
