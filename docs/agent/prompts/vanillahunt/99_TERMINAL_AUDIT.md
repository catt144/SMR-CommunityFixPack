# 99 — the terminal audit: disbelieve the chain

⛔ ONE-SHOT: this file `git rm`s itself on close-out; the README stays as the
record with every row struck. Model: **Fable** · owner needed: raises the
kickoff · runs ONLY on a folder holding `99` + `README.md`.

> 🎯 Fresh context, trusts nothing forward. Every "done", every count, every
> `C` entry and every "nothing found" upstream is a CLAIM. Your two rulings:
> **were the instruments sound**, and **do the findings survive re-derivation
> from the two trees**. You have room to chase — use it; the audits that paid
> compound interest produced new primary evidence because they did.

## 0 · Open in this order

`git log --oneline -30` · `git pull` · `ListAgents` · `README.md` (whole) ·
`STATE.md` · `reports/vanillahunt/TRIAGE.md` (whole) ·
`reports/vanillahunt/agents/*.md` (04's verbatim agent reports — the primary
evidence for every 04 finding; audit verdict-by-verdict against them, and
treat a finding with no agent report behind it as unevidenced) · every `bugs/C##.md`
with `updated:` inside the chain's date range (list them with `git log
--diff-filter=A -- docs/agent/bugs/` over the chain's commits) · your
`## Notes from upstream` (every link's outbox lands here — read it LAST, after
you have formed a first view from the artefacts, and say which order you
actually used). Pin check (README §0): if the buildid moved during the chain,
say which links ran against which build.

## 1 · 🗒 Live todo list, from your first action — one item per pass

## 2 · Passes

### A · Instruments — re-falsify by hand, then plant something fresh

1. `python tools/treediff.py --selftest` and `python tools/presetdiff.py
   --selftest` GREEN — then read each fixture list against 01 §2.B.7 and
   §2.B2: is every required case actually asserted, or merely printed? And
   the churn rules: 01 sampled 20 rows per class — re-sample 10 per class
   yourself; a hidden value change voids the class for the whole chain.
2. **Plant a fresh change.** Copy ONE archived file pair into your scratchpad
   (⛔ never write under `SMR-SrcArchive\`), edit a body, a signature, and a
   preset value, run both tools on the scratch pair, confirm three rows.
3. **Banner integrity:** the digests in every TSV banner equal the two
   `MANIFEST.sha256` tree digests recomputed now.
4. **Soundness sample.** Pick 5 random `hand` changed files (seeded RNG, seed
   in the report) and 2 random `generated` ones; run a raw `diff` between the
   two archived copies; account for EVERY hunk with an inventory/preset row or
   with a stated imprecision (`SPAN-SUSPECT`, non-function-level text, a
   churn rule). An unaccounted hunk that changes behaviour ⇒ the instrument
   missed a class; rule **SOUND / SOUND WITH STATED GAPS / UNSOUND** and say
   which gaps.
5. The one-line-function trap: 01 measured it or did not — which, and what
   did the count do to the links' coverage claims?

### B · The controls

Seeds hit rate and self-sample agreement as the ledger states them — re-derive
both from `INVENTORY.tagged.tsv` (are the four seed rows classed right NOW?),
then **blind-reclassify 20 random `WORTH-READING`/`CHURN` rows yourself** from
the two trees and compare. A `CHURN` that was a value change is a triage miss;
count them and say what it does to every link's "reached" claim.

### C · The findings — re-derive a sample from scratch

Every `C` entry the chain filed: re-derive **at least a third, minimum 5, and
ALL rated P1/P2**, from the two trees and never from the entry's text. Per
entry: route holds / route wrong / citation wrong / recipe does not fire the
trigger / falsifier missing or non-executing / severity mis-stated / non-owner
question unanswered where DLC-adjacent. ⭐ **Try to REFUTE each** the way C54
was refuted — count the presence side, check `facts/INDEX.md`, run the
executing falsifier the other way. A refuted entry stays filed with the
refutation (C54's precedent: the reasoning error is the reusable part).

### D · Coverage — what the chain did NOT reach

Collect every link's and every 04 agent's NOT-reached section; add what they
did not admit: 01's churn classes by sample size, 04's tooling table by loader
citation, 02's `other` rows, `SPAN-SUSPECT`/`MULTI`/fpk-divergent rows,
`DLC/` (by design), ⭐ the `PASSING` surface sweep's real reach (it covers
only bodies someone opened — count them against the unchanged-body total in
the fragile systems, so the owner sees what fraction of unchanged code was
ever looked at),
and README's blind-spot list re-read in the light of the run — did the chain
learn a new one? State it. ⛔ A "nothing found" in a system is reported with
its row count and its agent count, never alone.

⭐ **The three field reports (README §2b)** each get one plain-language paragraph
in `HUNT_AUDIT.md` for the owner: what the chain read for it (rows and
surfaces), what it found, what it could not see, and what would settle it —
for FR-1, a log from an affected player (checklist 136). Check that 02's FR
tagging was by function, that 03 wrote FR-1(b), and that 04 wrote FR-1, FR-2
and FR-3; a missing subsection is a chain defect. ⛔ A report the chain found
nothing for is written up with its surfaces read, never as cleared.

### E · Consistency

Ledger counts vs TSV counts; README rows struck vs prompts consumed (`git
log --diff-filter=D`); every inbox item landed, routed with TAKEABLE WHEN, or
named as dropped (a dropped item is a finding about the chain); **no status
word moved** (`git log -p` over the chain's commits on `bugs/` shows no
`status:` change except new `cand` files); **`Code/` untouched** (`git diff
--stat <chain-start>..HEAD -- Code/` empty); `items.lua`/`metadata.lua`
untouched; both archives' manifests re-hash identical (nobody wrote there);
STATE/checklist/SESSION_LOG say what the chain did and nothing more.

### F · The rulings and the owner report — `reports/vanillahunt/HUNT_AUDIT.md`

1. Instruments: SOUND / WITH GAPS / UNSOUND, with A.4's table.
2. Controls: the numbers, re-derived.
3. Findings: ranked by **player severity**, each with the non-owner sorter,
   `DIFF-CAUSED` or `PASSING`, the falsifier's state (executing / source-only
   / needs a game), and your verdict (holds / weakened / refuted). ⛔ Not a fix list — what becomes a fix
   is `FIX_POLICY` §4 + the owner: route ONE checklist decision item
   ("which of these, if any, go to a hotfix-3 candidate list") with a
   recommendation per finding, and say plainly that most will be "file and
   watch".
4. Coverage, from D, verbatim into the owner report — ⭐ *state up front what
   this hunt could not see* was part of the brief's deliverable.
5. Drift ledger: every upstream mistake the links captured (rule 5), plus
   yours.
6. **The kickoff line for `prompts/DLC_DEEP_CHECK.md`** (CHAIN_METHOD §4.6),
   pointing it at `TRIAGE.md` → "For dlccheck" as its inherited base-game
   result, and naming anything this chain learned that changes ITS shape
   (e.g. if 04 found the DLC patches base behaviour more than "mostly
   additive" allows, say so — that brief's §6 asks for exactly that signal).

## 3 · Scope fence

**In:** A–F, `HUNT_AUDIT.md`, refutation edits to chain-filed `C` entries
(with the refutation dated, never a deletion), the routed decision item,
STATE/SESSION_LOG close-out, emptying the folder. **Out:** new hunting beyond
what a re-derivation needs (a new finding you stumble on is filed as `cand`
with "found by the audit, un-audited" on it); any `Code/` edit; any status
word; the DLC chain's authoring (you write its kickoff LINE, not its chain).

## 4 · Stop conditions

Pass A rules UNSOUND — STOP after writing the ruling and route "re-run the
inventory with the fixed instrument" as an owner decision; do not audit
findings built on an unsound inventory as if they stood · a seed row is
misclassed in the tagged TSV NOW (the control was scored on something else —
say so, re-score) · the folder holds more than `99` + README (a link did not
close; STOP AND ASK).

## 5 · What may NOT be claimed

That the game is clean in any system. That a source-read finding is
reproduced. That coverage exceeds the sampled fraction (say the fraction).
That a refutation of one entry generalises. That the instrument is sound
beyond the sampled files and the stated regex. `tested`, ever.

## 6 · Close-out

`HUNT_AUDIT.md` committed; every chain-filed entry it touched updated;
checklist decision item routed with recommendation; STATE.md one line (measure
the cap — rule 13), SESSION_LOG entry (`tags:` line, pointers, the grave
`git show <sha>:docs/agent/prompts/vanillahunt/99_TERMINAL_AUDIT.md`); README
row 99 struck with the verdict word and the report path; `git rm` this file;
explicit-path `git add`; doccheck GREEN; commit `-F`; push. The owner report
ends with the `DLC_DEEP_CHECK.md` kickoff line, or says why it should not fire.

## Notes from upstream

*(authoring session, 2026-09-09/10)* Top tier is the authoring RECOMMENDATION;
at five links the owner assigns (README §1). The chain was consolidated from
eight links to five on 2026-09-10 (README §1's deviation note) — 04 is now a
parent over agents, so its `agents/` reports are your primary evidence and a
04 finding with no report behind it is a chain defect. Nothing has run; the three seeds and their expected classes
are in README §4 and their pins in 01's inbox. The authoring session's own
numbers (README §0 shape table) were produced by a declaration-line regex and
a manifest comparison, not by `treediff` — if 01's inventory disagrees with
them, 01 is right and the README table is the drift.

---

*(from link 01, `smr-bugfixpack-04`, 2026-09-10)*

**What exists to audit.** `tools/treediff.py` + `tools/presetdiff.py`, the five
TSVs and `TRIAGE.md` §0 in `docs/agent/reports/vanillahunt/`, and `EF-085` (fpk
parity). Both tools import `luafn.find_bodies` rather than re-implementing it;
`treediff` also imports `sigcheck.params`. Re-run both `--selftest`s: 16 PASS /
0 FAIL each, exit 0. Full counts in `TRIAGE.md` §0; my outbox to 02 is the
reading guide and is not repeated here.

⭐ **THE ASSERTION I BROKE ON PURPOSE, AND ITS RED** (both tools — an instrument
nobody has watched fail is not an instrument):

- `treediff.py`: inverted the whitespace negative to demand the row EXISTS.
  ```
  FAIL   ⛔ CRLF + trailing-space-only change is NOT A ROW   -> None
  SELFTEST: *** FAIL ***          exit=1
  ```
  Restored → 16 PASS, exit 0. **The exit code was verified in both states**, so
  the green gate is a real gate and not a print statement.
- `presetdiff.py`: inverted the `T-ID` expectation to `FORMAT`.
  ```
  FAIL   ⭐ T() id changed, TEXT IDENTICAL -> `T-ID`
         -> ['Data/Widget.lua', 'Widget', 'alpha', 'label', 'T(111, "Hello")',
             'T(222, "Hello")', 'T-ID', '']
  SELFTEST: *** FAIL ***          exit=1
  ```
  Restored → 16 PASS, exit 0. ⚠️ My FIRST attempt at this break used `sed` and
  produced a `SyntaxError`, which also exits 1 — I caught that the RED was the
  interpreter and not the assertion, and redid it as a clean edit. **A non-zero
  exit is not by itself evidence that a falsifier fired.**

⛔ **DRIFT — every mistake caught, mine and upstream's.**

1. ⭐ **My own first design was wrong, and the falsifier caught it, not me.**
   `treediff` v0 hashed the whole body span — which includes the declaration
   line. So every signature change reported as `body+sig` (the planted F115
   fixture failed) and a RENAME could never hash-match its partner (that
   fixture failed too). Fixed by hashing twice: `hash` (whole span, byte-for-byte
   `bodycheck`-compatible so a row cross-checks against a `SRC:` pin) and
   `ihash` (declaration line dropped) for the body verdict and for `RENAME?`.
   ⚠️ **Audit point: if the two fixtures had not been in the brief, this ships
   silently and every `sig` row is mislabelled.**
2. **`RENAME?` had no triviality guard and fired 1,328 times inside one
   `LuaExportedDocs` file** on bodies like `end` and `return true` (57 pairs
   with a ONE-line body, 304 with two, single hashes with 32 partners). Guarded
   to ≥4 distinct non-blank body lines and ≤3 candidates; both rejection counts
   are in the banner. After the guard it found the real thing: the modding
   backend MOVED `CommonLua/Classes/` → `CommonLua/Modding/`.
3. **`presetdiff` had three parser defects, all found by SAMPLING the real
   trees, none by the fixtures.** (a) `call()` counted bracket depth manually
   while `value()` also consumed the nesting, so the two desynced and the
   parser ran to end-of-file — it arrived as a `RecursionError`, which is lucky;
   it could equally have been a wrong answer. (b) Embedded `function … end`
   bodies in `XDef`/`FlightPolicyDef` fields were shredded into pseudo array
   items, so a one-line handler edit produced hundreds of rows whose "values"
   were `local`, `then`, `end`, `dlg` — **42,072 such rows, every one
   mis-explained by my own REINDEX rule as positional churn.** (c) Nested
   `PlaceObj` sub-items use the POSITIONAL PAIR form
   `{'Name', value, 'Name2', value2}`, which I was indexing as `[1][2][3]…`, so
   property names became values and one insertion shifted everything
   (`XDef:PoliticsDlg` alone: 5,307 rows). Row count across the three fixes:
   **78,243 → 54,291 → 37,512.** All three are now PINNED by fixture
   assertions. ⚠️ **Audit point: fixtures I wrote could not find defects in a
   parser I wrote — only the real data could. Judge the other instrument the
   same way.**
4. ⭐ **A churn class I had to split after reading it.** The brief requires 20
   rows per class read by the author. Reading 20 `REINDEX` rows showed the class
   was two different claims: the `<absent>` half is provable (I found the
   matching pair — `XDef:ipTrack`'s `T(529, "Today…")` leaving `children[6]`,
   arriving at `children[5]`), the value-vs-value half is not. Split into
   `REINDEX` (10,462) and **`REINDEX-SWAP` (1,924, ⛔ must be read)**.
   `T-ID`: all 22 rows read, 0 misses.
5. ⚠️ **I shipped an overstated justification in `presetdiff`'s own header and
   corrected it from my own run.** The header claimed preset identity had to be
   `class::id` because "the generated files were renamed wholesale, and
   file-keying would have produced thousands of false rows". The measurement
   says **0 matched presets changed file** (17 generated files exist only in
   1.0.7, 59 only in 1.1.0). The identity choice is still right — it is how the
   GAME names a preset — but the stated reason was a story. Corrected in the
   docstring and the banner. **Check the other headers for the same failure.**
6. ⚠️ **`FORMAT` and `SAVE-ID` classify 0 real rows.** They pass on fixtures and
   never fire on the trees. I report them as UNFALSIFIED rather than as working
   rules.
7. **Drift against my own brief, reported rather than acted on.** The prompt
   defers the `luafn.py` delimiter fix because "a delimiter change re-hashes
   every `SRC:` pin in `Code/`". I resolved all **49** pins against the 1.1.0
   tree: **0** target a self-closing declaration, so a narrow fix moves **0**
   hashes. I did not fix it (fence), but checklist **135** now puts the real
   cost in front of the owner instead of the assumed one.
8. **README §0 reconciles exactly** once DLC is separated — no drift there. Its
   "138 are `DLC/norman`" is right; the 139th DLC add is `DLC/thomas`.
9. `01_INVENTORY.md` §2.B.4 asked whether the one-line-function trap is real:
   **confirmed at source AND measured** — 441 self-closing declarations
   over-span, 133 rows flagged, 567 spans reach EOF.

⚠️ **WHAT I DID NOT DO, so you can weigh the silence.** I did not read a single
row for meaning (fence §3) — including the three pure-`sig` rows I noticed while
testing the tool and passed to 02 unread (`Station:GetScoreFor` `:traits` →
`:colonist`, and the two `TraverseTunnel` methods). I did not touch `luafn.py`,
`bodycheck.py`, `sigcheck.py` or `doccheck.py`. I did not wire either selftest
into `doccheck` (01's fence says you re-run them). I did not read `DLC/` or
`Code/` beyond resolving the 49 `SRC:` pins for checklist 135.

⭐ **THE HOLE TO WEIGH HARDEST.** `treediff` covers **indent-0 declarations
only**. **8,473 indented declarations exist on the 1.1.0 side; 4,883 of them are
in `hand` files and are covered by NEITHER instrument** (`presetdiff` reaches
only the `generated` share). Plus every anonymous `function(` literal
(~12,200 lines). I sampled the indented set and it is overwhelmingly preset
data, which is why the contract was set at indent-0 — but that sample is an
argument, not a proof, and the hand-file remainder is unmeasured territory. If
you re-falsify one thing in this link, make it that.

**Re-falsification handles for you.** Plant fresh changes with
`python tools/treediff.py --old <dir> --new <dir>` on two temp trees (the
fixture builders `OLD_FIX`/`NEW_FIX` in each tool show the shape), and
`python tools/presetdiff.py --sample <churn-class> -n 20 --seed <n>` prints any
class for reading. The four seeded positives are re-scored by
`treediff --selftest` PART 2 on every run, so a regression in the real trees
shows up there and not only in a ledger.

---

*(from the authoring session `smr-bugfixpack-c3`, 2026-09-10 — DRIFT TO
AUDIT, filed under rule 5 by the session that caused it.)* **`treediff.py`
gained a second author after link 01 closed.** The owner asked whether 01's
stated hole (indented declarations) could be repaired; I measured it (2,033 of
4,142 were always covered by an outer span; 2,109 were not), extended the tool
to v1.1 (`_orphans`, `_diff_orphans`, `bare_name`; `INDENTED`/`ONE-LINE`
flags), extended `--selftest` by six assertions on a new fixture, broke one on
purpose in memory and watched it go RED, and re-emitted the TSVs (INVENTORY
9,832 → 11,742; the other three banner-only). `TRIAGE.md` §0.13 records all of
it. Three things for you specifically:
1. **The "one tool, one author" rule (README §4) was bent** — with a falsifier,
   but bent. Re-run Pass A.2 with a planted INDENTED change (a table-field
   method inside a `DefineClass{}` block, and a `Run` step inserted among
   same-named steps) and confirm one row each, no cascade.
2. **The `ONE-LINE` deviation is a design choice, not a measurement**: a
   self-closing orphan hashes its own line only. Rule on whether it hid
   anything — sample 10 `ONE-LINE` rows against a raw diff of their files.
3. **The `@anchor` key is a locality heuristic.** A declaration whose nearest
   indent-0 line changed between trees gets a NEW anchor and therefore shows as
   removed + added (hash-matching only cancels within one anchor group), not as
   `body`. MEASURED by me: `INDENTED` added/removed pairs sharing a file and an
   `ihash` = **11, all `generated`, 0 `hand`** (`TRIAGE.md` §0.13). Re-derive
   that count; it is a labelling error, not a coverage one.

---

*(from `smr-bugfixpack-04`, 2026-09-10, after link 01 closed — ⛔ DRIFT IN LINK 01's COMPLETENESS STATEMENT, found downstream)*

Link 02 (`smr-bugfixpack-b6`) found NVIDIA DLSS 2 → 4 sitting in a top-level
DATA TABLE of `CommonLua/Core/options.lua`, a change with no `INVENTORY` row
and no `PRESETS` row. Link 01's `TRIAGE.md` §0.11 listed the indented
declarations and the anonymous `function(` literals as the inventory's holes
and **did not name this one**. Measured the same day: **123 of the 897 changed,
added or removed hand files have ZERO inventory rows but real content** (1
more is whitespace-only). They are top-level config, const and option tables
(`Lua/Config/*`, `Lua/__const.lua` with 347 changed lines,
`CommonLua/Core/const.lua`, …) and preset data stored OUTSIDE the four
`generated` prefixes (`CommonLua/Data/` 28, `CommonLua/Libs/` 26, mostly their
`Data/` and `ClassDefs/` folders), which `presetdiff` never reads by design.
Because link 02 partitions ROWS, **none of the 123 could reach any 04 reader.**

Fixed as `treediff` **v1.2**: a sixth generated TSV, `NOROWS.tsv`, lists every
changed file with no row, with its `reader` (`NONE` / `presetdiff`), `content`
(`yes` / `ws-only`, under the tool's own normalisation) and normalised
`lines_changed`. Three fixture assertions were added: a data-table-only change
is LISTED; a whitespace-only file is marked `ws-only`; a file with rows is NOT
listed. Selftest 24 PASS / 0 FAIL, exit 0. **Broken on purpose** on a scratch
copy (the real file untouched), with the data-table assertion inverted:

```
FAIL   ⭐ a DATA-TABLE-only change (no function touched) is LISTED, content=yes, reader=NONE — the options.lua / DLSS 2->4 shape   -> ['Lua/Tbl.lua', 'changed', 'hand', 'NONE', 'yes', 2]
SELFTEST: *** FAIL ***          exit=1
```

Regenerating left INVENTORY, STORAGE, FILES and CALLERS byte-identical apart
from their banner's version string (0 non-banner diff lines, checked).
`TRIAGE.md` §0.11 was NOT amended: it is link 01's closed record, and the file
is link 02's live lane. This note plus README §2b / §6 and 04 §2 point 7 carry
the correction. ⛔ Audit points: re-derive the 123 yourself, check that 04
assigned every `NONE`+`yes` file to an agent as a text-diff item, and ask
whether `presetdiff`'s fixed four-prefix scope should become "every file that
holds `PlaceObj` blocks" (it could not change mid-chain without invalidating
02's `PRESETS.tagged.tsv`). Minor: in the owner session I first said "124
files"; that count included the one whitespace-only file.

---

*(from link 02, `smr-bugfixpack-b6`, 2026-09-10 — TRIAGE.md §1–§4 is WRITTEN. ⛔ A class is a sort key, `WORTH-READING` a routing flag, a `SMELL` a PASSING candidate to derive; no row here is a finding.)*

**The control, in numbers (TRIAGE.md §2):** seeds **4/4 by content, 2/4 by strict label** — F114 returned (i)+(g), F117 returned (b); the parent ruled 4/4 with reasons you may overturn (F117's (b′) caller was OUR module, absent from vanilla; F114's change IS two guards). Second numbers: BLIND self-sample n=20 — WR/CHURN 20/20, guard 19/20, primary class 15/20; round 2 on 295 rows (B05, B06) — WR/CHURN 99 %, primary class 77 %. B12.r2 issued, not ingested. ⭐ F115's agent independently re-found the known F34(d) dead `filter_embark` (tell 2) — the surface sweep's own positive control.


# 02 drift + deviations log (for 99's inbox) — kept as it happens

## Deviations by the parent (stated, deliberate)
- D1 dlc-adjacent tag two-tier (T1 literal + T2 qualified), not the brief's literal 25-term list (2,918 Lua / 8,209 preset rows literal vs 1,289 / 1,618 applied). Reason: a tagged row leaves 04; 03 cannot hold thousands.
- D2 Taxonomy "our scar" cells for F115 and F117 redacted to `[example withheld]` in every agent brief — the brief demands both "taxonomy VERBATIM" and "not told which rows are seeds"; the verbatim cells named the seeds' functions and changes. Agents also told not to open C:\Dev\SMR-BugFixPack\docs (bugs/F11x would name them).
- D3 Agents wrote their verbatim return to a private scratchpad file (returns/Bxx.txt) and replied with COUNTS+NOTES only — the brief says "It does not write files". Reason: 24 inline returns would have put ~140k tokens into the parent context and forced hand re-typing into the TSV; the parent still wrote every shared file, and ingestion is mechanical (tri_ingest.py validates each row).
- D4 Fan-out pool includes the 13 non-SPAN-SUSPECT pure `sig` rows (brief names body/body+sig only).
- D5 Returned per-row fields follow the 02 brief §2.C.2 list; README §4's "who reaches it" and "the falsifier" were NOT asked of triage agents (02 classifies, 03/04 derive — 02 fence).
- D6 PRESETS: REINDEX-SWAP, added-preset, removed-preset rows routed to 04-E as READ (brief names only `none`); REINDEX / T-ID / COMMENT are NOT-READ.
- D7 A third tagged copy, CALLERS.tagged.tsv, holds unit D's verdicts (README §6 names "the two working copies").
- D8 Long bodies (>400 lines, mostly Lua/Scenario/*.generated.lua `Create@` rows) shown to agents as hunks + 8 lines context (`--full` available) — "both bodies open" is partial there.
- D9 Trains forced into their own batch (B01) so the four seeds sit in three agents, not two.

## Agent drift (each noted by the agent itself or caught at ingest)
- PARENT drift caught by an agent: unit D first marked 3 `from_ui` caller rows `unsure` (LanderRocket.lua:803, customLanderRocket ×2); agent B10's notes showed they resolve to LanderRocketBase's override, whose (…, from_ui) signature is unchanged on both trees — parent re-checked (LanderRocket.lua:787/:801 both trees) and flipped them to benign. The call-form homonym test cannot see a same-named override on a sibling class.
- PARENT drift caught by an agent, the second and more serious: unit D marked `ActionFX:GetLocObj`'s four `same` callers (ActionFX.lua:2052/:2821/:3967, _fixup.lua:1335) benign under the appended-param heuristic ("tested/passed-on"). Agent B16 showed the appended `action_pos` feeds a NEW `Source == "ActionObj"` branch — the play paths were updated, the destroy/follow/should-play paths were not. Parent re-read both bodies (ActionFX.lua 1.0.7:1245-1275, 1.1.0:1318-1350) and flipped all four to F117-SHAPE. ⇒ The heuristic can see an unguarded INDEX of a new parameter, never a new BRANCH that only a passed parameter reaches; all ~1,460 appended rows are now worded "benign BY SHAPE — whether the caller needed the new behaviour is not read here". 99: re-derive a sample of appended callees whose new param gates a new branch.
- PARENT drift caught by an agent, the third: unit D ruled all 9 `GetEnvironment` `same` callers benign because `ResolveMap` is documented to take a game object — but `Lua/X/Infobar.lua:582` (C00694) passes a CITY (agent B24), and City.lua defines no GetMap/GetMapSlot in either tree. The reason covered objects, not the argument actually passed; C00694 flipped to `unsure`, the 8 object-passing callers stay benign. ⇒ a per-callee verdict needs each call's ARGUMENT kind checked, not just the callee's contract.
- A (b′) shape unit D cannot see by construction: R08311 `Funding:CalcBaseExportFunding(amount, res_id)` — SAME signature both trees, but the body now needs `res_id`; `RocketBase.lua:966` still omits it (agent B12). CALLERS.tsv is keyed on signature changes, so it never listed this call. Reaches 04 via the agent's (b′) row verdict.
- B02, B09, B10, B13: wrote a temporary rowdump dump file in the scratchpad to read in chunks, deleted after (rule 1 of the brief breached, disclosed by both).
- B07: 52 rows returned `WORTH-READING` with no reason clause (format lapse; accepted, counted, marked `[no reason clause returned]`); 1 row with a three-part class `(a)+(c)+(i)` (validator widened).
- B06: three SMELLs (R10333, R10393 `#log` on false; R10383 `next(nil)`) rest on "throws in stock Lua" — EF-005 says this engine TOLERATES #nil / next(nil) / ipairs(false); those smells are probably void. B01 withdrew its own such smell after reading a dev comment.
- B08: its first return file was read mid-write (123/228, no COUNTS) before the completion notice — parent waited for the notice; no partial ingest was kept (ingest re-reads the final file).
- PERF gap: B01–B15 briefed before README §2b (10eecc8) landed; B16–B24 carry the PERF clause (brief hashes `_v2_perf`).

## Control notes
- Seeds by CONTENT 4/4 (every change sentence names the real change). By strict LABEL 2/4: F114 returned (i)+(g) [expected (a) — (i) is the guard-specific derived shape of a body change and F114's change IS two nil-guards]; F117 returned (b) [expected (b′) — F117's (b′) caller was OUR module in Code/, absent from the vanilla tree; the agent enumerated the vanilla callers (0 kept the old contract, DroneFactory.lua:230 traced safe)]. Parent ruled 4/4 and re-issued a random 3 of 21 non-seed batches anyway (B05, B06, B12; seed 20260910) for an independent agreement number — a parent grading its own control must not let a lenient ruling stand alone.
- F115's agent SMELL independently rediscovered the known F34(d) dead `filter_embark` (REVERIFICATION F-8) — evidence the surface sweep works.

## Unit D notes
- 0 of the 15 pure-sig rows have a byte-identical body still reading a dropped parameter name (measured).
- The appended-param heuristic (indexed-unguarded vs tested/passed-on) found 0 unguarded indexings; object-typed appended params were each read (all defaulted or guarded).
- 14 unchanged caller-only files had no link until hand-assigned (tri_other.py caller-only group).


### From 03 · close-out gate and evidence, 2026-09-10

GATE: original 03's consumed prompt does NOT mean all seams are finished.
03b_SEAM_PRESETS.md,03c_PROGRESS_SEAM.md,03d_CALLER_SEAM.md and 04_HUNT.md
(plus any declared children) must close before this terminal audit/DLC kickoff.
03's required ~400-row stop yielded396 complete present spans in 25 files, six
complete caller/contract reads. Deferred:893 inventory + 1,618 presets + 24 callers+
18NOROWS. `SEAM_COVERAGE.tsv` gives2,955 unique items and disjoint owners;
`python tools/seam_coverage.py` verifies original-input membership and partition.
It reproduces declared read attestations, not independently measured reading.

Audit `SEAM_REPORT.md` (parent synthesis, not verbatim chaser transcripts),
`SEAM_PLAN.md`, C56-C62, `tools/desk_seam_food.py`, `SEAM_DESK.txt`, and
TRIAGE §03 coverage / For dlccheck. Parent owns all judgments and writes.
Five DIFF-CAUSED, two PASSING(C59/C62). C56 accepting-producer desk mismatch
old 2400/2400,new 2500/1200 at48 performance; C57 synthetic disabled-stock control;
C59 bounded gap/adjacent controls both trees. C58 native requests, C60 cost and
C61 actual death-popup outcomes unobserved. No module, metadata or game writes.
Checklist carries fresh-fixture riders; C59/C62 lack real player recipes.

Control numbers:0 eligible seeded positives; random6-row parent sample 6/6
actual-change agreement,5/6 route precision before correcting GetCropName to
no literal caller. Full Building.Destroy/GetUIWarning rereads repaired output
truncation before final coverage. Rows overlap and malformed spans remain.
All24 pending caller records stay pending even where four call lines were checked.

Drift (EVERY detailed correction is in SEAM_REPORT → Drift and audit inbox):
wrong task slash; brief guard scope3/1Lua versus10/1Lua + Data; required split;
DLC ingredient/recipe excerpt lookup exceeded the single-function fence, stopped,
and gives no DLC clearance; ranch zero prediction and old 1200 corrected using
real helper and old Chicken food200; C57 one caller corrected to two, registry
group/food-set distinction corrected; absent old FoodServiceBuilding desk path;
localization concat and Research dot-self false positives rejected; Hungry raw-food
flag corrected; C61 synthetic-harness possibility and owner-override caveat;
bulk truncation resolved; GetCropName route narrowed; synthesis method/path/field
names corrected; NOROWS `file`->`path` generator error, scratch syntax and stray
patch sentence corrected. Initial commit messages missed PROBE SWEEP line;
explicit clean sweep plus desk/gate reruns reverified the result for close-out.

Repeated hook warning, VERBATIM:
`  WARN kit-tree state is UNKNOWN on this run — re-run doccheck before trusting a clean kit tree`
Standalone doccheck reported kit clean. Do not call the commit hook warning-free.

FR-1(b)3/10 rows read, FR-2 zero/seven, FR-3 eleven/21; remaining keys have
owners and no report is closed. For dlccheck must include successor verdicts:
base classes do not establish concrete non-owner recipe instances, and missing
literal callers do not exclude dynamic/native/DLC dispatch. The report retains
all chain blind spots and does not rule on the DLC chain's additive premise.
