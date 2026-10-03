# Open-bug recheck: which filed defects are still possible on the shipped game, and which can be confirmed

Single use. Authored at `a565a34` on 2026-10-02 on the owner's ask. `git rm` this file and its
row in `prompts/README.md` in the commit that lands the report below. Start with
`git log --oneline -8`, `git pull`, `git status --short`; peers commit concurrently, so commit by
pathspec only and re-read any entry right before writing to it. Open a live todo list before your
first write: one item per entry group, one in progress.

## Authority and outcome

Owner, 2026-10-02, verbatim: *"author an investigation fan out prompt to recheck any of our bugs
that may need fixes and have it decide if they are still possible issues, and if it can confirm
them."* C121 is excluded (fixed the same day, `Code/Fix_UniversalDepotSeedsToggle.lua`).

End state: every open entry carries a dated recheck section with one of the five verdicts below
and its evidence, and one report, `docs/agent/reports/OPEN_BUGS_RECHECK_<date>.md`, ranks the
confirmed, still-possible defects for the owner's build decision. **No fix is built under this
prompt**: building is the owner's call per entry, taken from the report.

Completion evidence: the report's verdict table reconciles against the entry files (one row per
entry, counted by command), `python tools/doccheck.py` GREEN, and every verdict's falsifying
command recorded beside it.

## The work list — derive it, do not copy it

```
PYTHONIOENCODING=utf-8 python - <<'EOF'
import re
rows=[l for l in open('docs/agent/bugs/INDEX.md',encoding='utf-8') if re.match(r'\| \d+ \|',l)]
keep=('filed','cand','blocked','built','open')
for l in rows:
    c=[x.strip() for x in l.strip().strip('|').split('|')]
    if c[3].split()[0] in keep and c[1]!='C121': print(c[1], c[3], c[4])
EOF
```

At `a565a34` this printed **63 rows** (C121 is `fixed`, so the filter never lists it; the
exclusion in the command is belt and braces). Recount at firing; a difference is named
by entry id, not reported as a number. The index's status column is derived from each entry's
heading tag and is known to lag the body (doccheck warns on the frozen cells), so the entry is the
record, never the row.

Pre-settled by the owner, do not reopen; record the verdict `out-of-scope` with the ruling's
location:
- **C47, C48**: retired for this pack, owner 2026-08-16 (`C47.md`, "RETIRED FOR THIS REPO").
- **C92**: held by its own live prompt `C92_ACHIEVEMENT_BUILD.md`, decision 171.
- **D-entries** (design, `dsgn` priority): not defects; skip.
- **C109–C117 P-items** closed by the owner 2026-09-26 ("marking thats as closed unless we get
  reports of actual impact", `MIGRATION_HUB_HANDOFF_high.md` item 3): the entries themselves
  are still rechecked; their closed P-items are not raised again.

## Added 2026-10-02 — the train cargo spoilage report (owner: "Add this to it")

`B:\Dev\SMR\SMR-OptInPack\docs\agent\reports\TRAIN_CARGO_SPOILAGE_BUGREPORT_20261002.md`
(Opt-In repo, commit `e120c83`): a train's Food or delicacy cargo loses about 4% at a
once-per-sol boundary with no Lua writer touching it, but `Train:UnloadAll` hands over the
BOOKED amount (`unload_cargo`, `Lua/Units/Train.lua:779-785` on 1.1.1.406343, re-read by the
authoring seat: `station:AddResource(amount, res)` then `train:AddResource(-amount, res)`), so
the station gains what the train no longer carries. Two archived logs and a log-only trap are
cited there.

This item has no `bugs/` entry yet. Take it as one more group member:
1. File it through `smr-bug-library` as the next free C id before giving it a verdict; the
   report is its Report section's source, cited by path and commit, not restated.
2. The report is a claim from a sibling repo: clear what each verdict rests on. The unload
   arithmetic is a source read (`sed -n` the cited lines). "Spoilage reaches trains from
   outside the Lua tree" is an absence claim: grep the 406343 tree for `CalcResourceSpoilage`
   and `FoodDecay` callers and count the presence side before accepting it.
3. Its evidence class is `confirmed` only if the two logs' lines are re-read from the archived
   logs and still support the arithmetic; otherwise `possible-unconfirmed`. The sitting ran
   with the Opt-In Modules loaded and was never run with them off; that control is what a
   sitting would decide, and it goes in the report's sitting section.
4. The report's candidate fix (reconcile bookings to the carried amount at the top of
   `UnloadAll`, releasing the difference with `RequestUnassignUnit`) is recorded as "shape, not
   a recommendation". Anything that replaces the `UnloadAll` body is a FIX_POLICY §1.5
   decision for the owner; F114 records what a `UnloadAll` body copy cost this pack once.

## Verdicts — exactly one per entry

| verdict | meaning | evidence it needs |
|---|---|---|
| `confirmed` | the defect exists on the shipped build and a control showed it | a desk control on the shipped bodies that FAILS with a falsifying variant and PASSES on the defect, or a prior attended observation already in the entry, re-read and still matching the 1.1.1 body |
| `possible-unconfirmed` | the defective expression is still shipped, no control could decide | the 1.1.1 lines re-read, and one sentence naming what a control would need (a save state, a screen event, owner time) |
| `vanilla-fixed` | the game no longer ships the defect | the REPLACED body read and cited, never a `DEFECT-GONE` or a changed hash alone (FIX_POLICY §2b) |
| `not-a-defect` | intended, or the entry's claim does not hold on re-read | the §4 intent tell that fails, or the line that refutes the claim |
| `ours-retired` | the entry blames a pack module that no longer ships, or one repaired in place | `ls Code/Fix_<name>.lua` showing absence, or the repaired line in `Code/` cited |

"Confirmed" is never a source read alone. A source read that finds the expression still shipped
is `possible-unconfirmed`. A desk control that cannot load the body without stubbing a function
that can refuse is not a control (`tools/README.md`, "Desk bench").

## Fan-out shape

The orchestrating seat groups the entries by game subsystem so one subagent loads one area of
source once: for example colonist movement and domes (C100, C103, C106, C109–C117), food and
farms (C56–C60, C67, C68, C73), mysteries and story (C62, C63, C64, C69–C71, C75, C82),
research and achievements (C76, C79, C104), tracks and trains (C55, F99, F116), the stale F rows
(F98, F103, F111–F114, F117, F118), and the rest. Five to ten entries per subagent. Invoke the
`subagents` skill before launching; choose the lowest tier that can carry the group, and say in
the brief that the subagent is read-only on `docs/` and `Code/`, may write at most one
`tools/desk_<id>_<slug>.py` per entry it controls, runs no gate and no writing git command, and
reports per entry: verdict, the 1.1.1 lines re-read, the command it ran with its key output, and
what it did not do.

Each subagent result is a claim. Before writing any verdict into an entry, clear it with one
command aimed at what it rests on: run the desk control yourself, or `sed -n` the cited lines on
the archived tree. A verdict whose check fails goes back to the subagent or becomes
`possible-unconfirmed`, never into the record on the subagent's word.

Source of truth for every line cited: `B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.406343\Src`,
read on build 25579348 (repinned 2026-10-02: the game moved from 1.1.1.405907 to 1.1.1.406343
the same day this was authored, and the new tree is archived). Read the installed build with a
command before the first citation (`python tools/doccheck.py --emit-fingerprint` prints it); if
it is not 25579348, stop (below). Cited line numbers in older entries were read on 1.0.7, 1.1.0
or 1.1.1.405907: re-derive each with `grep -n` on the 1.1.1.406343 tree before relying on it,
and name the build beside every line you cite.

## Writing the record

- Apply `doc-editing` and `smr-bug-library`. Each rechecked entry gets a dated section
  `#### Recheck <date> — <verdict>` at the end, with the evidence above and the falsifying
  command. Update the heading tag and `evidence:` front matter; leave `row_status:` frozen.
- Status moves only on evidence, per `WORKFLOW.md`: `vanilla-fixed` and `ours-retired` entries
  go `closed`; `not-a-defect` goes `wontfix` with the tell named; `confirmed` and
  `possible-unconfirmed` keep `cand`/`filed`. No entry becomes `fixed` or `tested-*` here.
- A desk control file carries the house docstring (first line is the tool-catalog row) and is
  re-runnable; the catalog regenerates under `--regen`.
- The report: one table (id, verdict, priority, evidence class, falsifying command), the count
  reconciled against the entry sections by command, then **"Fix candidates, ranked"**: only
  `confirmed` entries, ordered by harm in a named game phase (FIX_POLICY §4 pricing), each with
  its intent tell, reachability tier, and a one-line fix shape where FIX_POLICY §1 gives an
  obvious technique, marked "shape, not a recommendation" where it does not. Then one section,
  **"What a sitting would decide"**, listing every `possible-unconfirmed` entry's single
  deciding read, so the owner can price a sitting once; do not estimate owner minutes.
- Commit per group by pathspec: the entries, any desk files, the regenerated `INDEX.md` and
  `tools/README.md`. The report and this prompt's removal land in the last commit.

## Scope

In scope: every entry the command above lists plus the train report below, judged against the
shipped 1.1.1.406343 Lua and
the records already in the repo. Out of scope: building or changing any fix, re-opening an
owner ruling, kit probes (the TestKit is a separate repo; never commit kit code from a pack
lane), and scheduling owner time. A defect found outside the list (a new vanilla defect, or a
new defect in our `Code/`) is reported in the report's last section with its evidence and is
not filed under this prompt, except a defect in shipping `Code/` that throws or writes to a
save, which is filed as an F entry at once and named in the report.

## Stops — report instead of continuing

1. The installed build is not 25579348: stop and route to `perma/GAME_PATCH_PROMPT.md`; this
   prompt's citations are for 1.1.1.406343.
2. A group's recheck finds a shipping `Code/` module that throws or writes into a save: file it,
   commit, and report before taking the next group.
3. The owner is needed to decide a verdict (an intent question with no tell either way): record
   `possible-unconfirmed` with the question in the report; never ask mid-run.

## Claim limits

- Not "fixed by vanilla" from a hash change; say "body changed, replacement read: <lines>" or
  stay `possible-unconfirmed`.
- Not "unreachable" from a one-caller grep; FIX_POLICY §4 requires subclass enumeration
  (`__parents`) before R4.
- Not "confirmed" from a subagent's table; say "confirmed, cleared by <command> at <HEAD>".
- Not "no player impact" for a source-only entry; say "harm unobserved" and price it by phase.

## Unattended runs

If fired unattended, execution and the audit of its verdicts run on different owner-selected
models; no verdict enters an entry unaudited. The audit re-runs every desk control and `sed -n`s
one cited line per entry.

## References

`CLAUDE.md` (trust classes, counts, pathspec commits), `docs/agent/WORKFLOW.md` (records and
rulings, status rules), `docs/agent/FIX_POLICY.md` §2b and §4, `docs/agent/bugs/INDEX.md`,
`docs/agent/facts/INDEX.md`, `tools/README.md` "Desk bench", skills `subagents`, `doc-editing`,
`smr-bug-library`.
