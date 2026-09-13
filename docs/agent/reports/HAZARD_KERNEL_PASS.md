# Hazard kernel pass — implementation handover

Authority: owner's 2026-09-13 rulings in the task brief (grave: phase 2 commit).
The initial scope stop was resolved by the owner's clarification in `06f553f`:
comment lines only, no Lua logic; rewrite all three shipped citations and all
three citations in `tools/doccheck.py`.

## Measurements and commits

MEASURED: initial anchor `06f553f`; phase 1 anchor `ffadd08`. That peer's
committed C92 prompt-map update was preserved. Before every initial write,
`git status --short` and baseline byte comparison checked the target.

Command for checkpoints: `python tools/doccheck.py`, filter `STATE + STUBS`,
`WAITING:`, final verdict. Before:

```text
STATE + STUBS: STATE.md 11971 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 123 checklist items, 44 marked, 5 waiting on the owner, 29 need a marker
doccheck: GREEN
```

Phase 1:

```text
STATE + STUBS: STATE.md 10758 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 123 checklist items, 44 marked, 5 waiting on the owner, 29 need a marker
doccheck: GREEN
```

Phase 2 measurements are recorded below; implementation shas/diff-stats
follow each commit landing.
Full owner-row list before: `[53, 133, 151, 169, 170]`. Command/filter:
Python `re.findall(r'^\| (\d+) \|', text, re.M)` over WAITING_ON_YOU.md,
converted to integers and sorted. Full register bytes are also compared.
Hazards raw-byte delta and exact retained-rail comparison: recorded below.

## Handover table

C1 (citation count): old text from `git show ffadd08:<path>`, minus current text,
count regex **occurrences**, no dedupe, of each removed label. Scope: live
`docs/**/*.md`, excluding archive, STATE, the brief, this report and the old
audit; also metadata.lua, items.lua, tools/doccheck.py. Regexes are
`r"\bH-(01|02|06|07|10)\b"`, counting each captured label separately.
STATE removals are separate. Counts below were emitted by the phase 1 script's
per-file occurrence enumeration and will be cross-checked directly with C1.
Quotes spanning source line breaks join those breaks with spaces.

| item | ruling | new home (file + heading) | rail quoted from new home | citations rewritten (count + command) | left alone, and why |
|---|---|---|---|---|---|
| Module-list rail | Out, double-gated | STATE Hazards preamble; tools/doccheck.py module_set_agreement; tools/upload_preflight.py packaging | "Module lists are gated by `tools/doccheck.py` MODULE SETS + `tools/upload_preflight.py` (membership + order)." | 37, C1 | Gate logic unchanged; only comment/docstring/diagnostic citation text in doccheck edited |
| Tag rail | Out, weak harm | agent/prompts/perma/RELEASE.md, Release rails | "Tag `fixpack-v1.0.0` marks what actually gets packed. ⛔ Never move it again without an equivalent gate (the attended sitting + the one-time release-gate ruling, ck57)." | 1, C1 | Tag untouched. Also added: "Before the handoff, run `python tools/upload_preflight.py`; any FAIL blocks it." |
| Editor/version rail | Out, weak harm | agent/prompts/perma/RELEASE.md, Release rails | "⛔ An agent NEVER opens the Mod Editor and NEVER hand-sets `version`/`version_major`/`version_minor`." Exception: "✅ Every OTHER hand edit to `metadata.lua` (the `code` list checked by doccheck MODULE SETS + tools/upload_preflight.py, `last_changes`, descriptions) is ordinary work." | 40, C1, including both metadata comments | Bump mechanism moved with rail; all Lua properties unchanged |
| Opt-in restore rail | Out, weak harm | agent/reports/PARKED_OPTIN_REFERENCES.md, Restore rail | "Never restore the parked opt-in references before the opt-in pack launches; that is ITS launch obligation. Verbatim parking and the restore checklist are below." | 1, C1 | Parked references and restore procedure unchanged |
| Autosave rail | Out, failed harm test | agent/facts/EF-056.md; PLAYTEST_CHECKLIST.md combined-sitting record | EF-056: "**Never stage a fixture from an autosave** — check the header for `autosave` and copy from a `SaveGame`-written save instead; a fixture that can be deleted mid-sitting is not a fixture." Checklist: "the fixture was re-staged from a save that is not an autosave; `EF-056` is amended." | 8, C1 | Fact unchanged; checklist fixture rider preserved. Owner's manual-save finding is authority, not re-derived |
| H-04 claim rule | Move | STATE Rules in force | "⛔ Never call a FUTURE release ready, and never treat "published" as covering anything the owner has not done." | No rewrite needed: identifier still exists in STATE | Wording unchanged; existing citations still resolve |
| Admission test | Verbatim install; match heading | agent/prompts/perma/STATE_EVICTION.md, Hazards admission test; STATE Hazards heading | "**1 · HARM — name the victim.**"; "**2 · UNIVERSALITY — every agent, or one role?**"; "**3 · GATE — can a machine catch it?**"; STATE: "## Hazards — moderate harm · universal reach · no machine gate" | Not citation work | Full adopted text installed; exact check passed |
| Both mods rule | Collapse to pointer | agent/WORKFLOW.md, BOTH MODS LOADED is the rig's NORMAL condition | "**The baseline rig configuration is BOTH mods enabled** — the fix pack AND the standalone opt-in mod." | STATE pointer to verified home | Whole dedicated section verified |
| Status words rule | Collapse to pointer | agent/WORKFLOW.md, step 5 status protocol | "**`tested-attended`** — the owner was at the keyboard"; "**`tested-unattended`** — confirmed by real launches with nobody watching"; "**`tested` (bare) is LEGACY and closed to new work.**"; "Do not promote one without re-deriving it from the archived record; do not read one as if it were attended." | STATE pointer to verified home | Full attendance, legacy and screen-claim protocol verified |
| Pull-only replies rule | Collapse to pointer | agent/WORKFLOW.md, Binding authoring rules 5b | "Never draft one unasked, never put one on the owner's owed list"; "never raise a waiting `DRAFT` as a nudge, and never gate other work on a reply going out"; "**This does not touch triage**" | STATE pointer to verified home | Full landing verified |
| Other-mod naming/player advice | Retain | agent/FIX_POLICY.md section 8, incomplete landing | "there is deliberately no player-facing load-order instruction" | No collapse | Target lacks the full naming prohibition; original STATE line stays |
| Behaviour decline rule | Collapse guard rule only | agent/FIX_POLICY.md section 2a, Branch guards | "Binding on every module that carries a body, expression or data shape taken from one game branch."; "⛔ **DO NOT BUILD A GAME-VERSION DETECTOR.**"; "It would be a **label check**"; "A probe that confirms the body shape its module was written for **necessarily declines on the branch that has the other shape**" | STATE pointer to verified home | Frozen-v5 service/download sentence stays; absent from that landing |
| Upload page bodies rule | Retain | docs/UPLOAD_WORKFLOW.md section 5, incomplete landing | "**Yes. They always auto-fill.**" and "**REQUIRED** and current every sweep" | No collapse | Full every-upload overwrite rule absent; original STATE rule and its backup/settled-auto-fill clause stay |
| STATE format rule | Collapse to pointer | agent/prompts/perma/STATE_EVICTION.md, Formatting | "format purely for machine safety: one fact per line, every line under the per-line byte cap"; "NEVER widen or pack lines to satisfy any budget" | STATE pointer to verified home | Full landing verified |
| Open decisions | Retain enumeration | STATE Open owner decisions; docs/WAITING_ON_YOU.md | "STILL OPEN: 53 harden now or in 1.0.1 · 47 two modder-page wordings · 152 c open · 133 two `FIX_POLICY` §2a" | No collapse | Parser simulation drops owner rows 53 and 133; blocked on markers |

## Not done and deliberate exceptions

- Phase 2 implements only collapses with complete landings. Final commit and
  measurement evidence is appended as each implementation commit lands.
- Open-decisions collapse blocked on markers. MEASURED without writing sources:
  import tools/doccheck.py; run `classify_items(checklist_items())`; replace
  `state_owed_numbers` **in memory** with `lambda: {144, 151}` (remaining Owner
  OWES values); classify fresh items again. Filter numeric items with status in
  `('open','deferred')` and owner true, sorted. Before:
  `[53, 133, 151, 169, 170]`; hypothetical after: `[151, 169, 170]`.
- Checklist 47 and 152(c) conflict with STATE's STILL OPEN prose but have
  `status:ruled owner:no` markers. Reported only; no owner-only adjudication.
- Naming prohibition and every-upload overwrite rule stay because their
  specified canonical homes are incomplete. No new policy authored to force
  those collapses. Frozen-v5 service information also stays.
- Old audit verdict table is an explicit task exception, not a stale live
  instruction. DOC_OVERHAUL_AUDIT.md matching lines 386, 387, 389, 391, 392, 395
  are untouched (Python line enumeration, removed-label regexes plus H-04).
  No archive files are edited.
- The self-consuming brief was retained through phase 1 and is deleted in
  phase 2. Phase 1 explicitly excluded it; the final absence check excludes
  only the historical audit and archive, and includes this handover report.
- Checklist autosave fixture rider survives as a completed-sitting record;
  no new standing rail authored and no checklist status or reading route changed.
- Checklist 170 policy calls, D4/archive_settled.py, marker vocabulary,
  CLAUDE.md/AGENTS.md, generated indices, decision/defect statuses are out of
  scope. No shipped Lua logic, game, portal, tag or save changes.

Nothing load-bearing exists only in conversation. Commit and measurement
evidence follows.

## Phase 1 invariant checkpoint

Command: temporary verifier using the baseline bytes captured at `06f553f`,
C1 direct git occurrence differences against `ffadd08`, and current files.
The full result follows; exceptions in its absence check are explicit above.

```text
H-03: raw original rail occurs exactly once, byte-identical
H-05: raw original rail occurs exactly once, byte-identical
H-08: raw original rail occurs exactly once, byte-identical
H-09: raw original rail occurs exactly once, byte-identical
Hazards raw bytes before / after / delta: 2467 1115 -1352
WAITING: byte-identical; numeric ck list: [53, 133, 151, 169, 170]
Adopted admission text: exact match after removing blockquote prefix and normalizing line endings
items.lua changed comment lines: [203] ; all non-comment lines identical
metadata.lua changed comment lines: [159, 180] ; all non-comment lines identical
doccheck: inverse citation substitution reproduces baseline bytes exactly; marker vocabulary and gate operations unchanged
C1 direct git occurrence differences: {tag: 1, editor/version: 40, autosave: 8, opt-in: 1, module-list: 37}
Separate STATE removed occurrences: {tag: 1, editor/version: 1, autosave: 1, opt-in: 1, module-list: 3}
Removed-label presence enumeration, live markdown excluding archive and explicit task exceptions: 0
Audit, archive, entry mirror and Code/ unchanged
```

## Implementation commit evidence

Phase 1: `66c16eb5751f79e9fde885bf577fe74eb397d04b`. Command `git show --stat --format= 66c16eb5751f79e9fde885bf577fe74eb397d04b`,
filter final non-empty summary line:

```text
48 files changed, 240 insertions(+), 97 deletions(-)
```

## Phase 2 verification

Command `python tools/doccheck.py`, filters `STATE + STUBS:`, `WAITING:`,
`doccheck:`:

```text
STATE + STUBS: STATE.md 10402 bytes (warn 12288, hard 18432, line 200); 3 stubs present and pointing
WAITING: fresh — 123 checklist items, 44 marked, 5 waiting on the owner, 29 need a marker
doccheck: GREEN
```

Full numeric ck list after phase 1 and after phase 2, using the same
WAITING table-row regex and numeric sort as before:
`[53, 133, 151, 169, 170]` at both checkpoints. The entire register is
byte-identical to the pre-pass register, not merely equal in row count.

Final presence check: enumerate **every** `docs/**/*.md` outside
`docs/archive/` and the expressly exempt `DOC_OVERHAUL_AUDIT.md`;
filter `r"\bH-(?:01|02|06|07|10)\b"` per line. Emitted matches: 0.
The brief no longer exists, and this report is included.

The final invariant checkpoint also reproduced the unchanged hazard bytes,
exact adopted wording, shipped non-comment lines, tool citation-only inverse
substitution, untouched Code/archive/entry mirror, and unchanged register.
Command: the same verifier as phase 1, with the brief exception conditional
on its existence (false at this checkpoint).

Remaining boot-budget warning, copied verbatim from the final doccheck
output (filter `PUSH SET:`):

```text
PUSH SET: 41970 B in 5 file(s) ≈ 19k tokens (budget 40960 B)  ⚠ OVER
```

The warning remains outside this bounded pass; no additional eviction or
owner policy call was made to clear it. Separate-session adjudication of
these output files is still outstanding by the owner's design.
