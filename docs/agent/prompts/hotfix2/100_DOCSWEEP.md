# 100 · Doc sweep for hotfix 2 — the INVERTED public-surface sweep, plus the agent-doc drift the audit found

Chain: `prompts/hotfix2/README.md`. Authored 2026-09-09 by link 99
(`smr-bugfixpack-a8`) as the audit's last act, on the owner's instruction that
the sweep fires AFTER the audit's results exist. ⚠️ **You run AFTER `99a_F117_FIX.md`** (authored `b30d116` under decision
127(a)); its §10 `git rm`s both itself and `99_TERMINAL_AUDIT.md`, so when you
start the folder holds `100` + `README.md` — the chain's designed state, not a
DO NOT SHIP. If `99a` is still present, its link has not closed: STOP, its
commit is what §3.2 keys off. The audit report survives at
`reports/HOTFIX_2_AUDIT.md` and is the authority for everything below.

⚖️ **The bar, in the owner's words:** *"The last thing I want is to release a
half-baked patch and then have to immediately repatch it."*

## 0 · Start

`git log --oneline -15` · `git pull` · `ListAgents` (message any peer in
`metadata.lua`, `docs/UPLOAD_WORKFLOW.md`, `SMR-CommunityMods`, or the checklist).
Staleness anchor: this prompt was written at `24eaea0` + the audit's commit; if
`Code/Fix_ArrivalDeaths.lua` has changed since, decision 127(a) landed — read
its commit before §3.

**Build the todo list before starting, one item per commit-and-verify unit**
(WORKFLOW "Authoring a prompt" element 1), mark each complete the moment it
completes, keep exactly one in progress. The owner reads it to decide when to
step in.

✅ **BOTH GATES RULED 2026-09-09** (relayed by `smr-bugfixpack-77`, who is
writing the receipts into the checklist — read them there, not here): ck126 =
KEEP the F95 pass (§3.1 first wording); ck127 = (a), F117 fixed BEFORE the
upload (§3.2 line applies once that link's commit is on `main` — check
`git log -- Code/Fix_ArrivalDeaths.lua`); ck129 = publish the site AFTER the
upload. ⛔ Still wait for the F117 commit before firing, and confirm the
rulings in the checklist yourself.

⛔ **GATES BEFORE YOU START — do not run this until both are ruled:**
- **ck126** (keep or remove the F95 residue pass in `90_SaveSanitizer`) — §3.1 has
  two wordings and you write the one that matches the ruling;
- **ck127** (fix F117 before the upload, or after) — §3.2 adds a change-note line
  only if (a) landed.
If either is unruled, STOP AND ASK; a sweep written against a description of the
pack is the thing this chain exists to prevent.

**Read path (files, not folders):** `agent/STATE.md` (mandatory) ·
`agent/reports/HOTFIX_2_AUDIT.md` **§1 F-3, §2 Pass F, §5, §6** ·
`prompts/PUBLIC_SURFACE_SWEEP.md` (the template — §0 rule, §1 site, §2 store,
§3 metadata, §5 close the loop) · `docs/UPLOAD_WORKFLOW.md` §3–§4 ·
`agent/reports/STORE_CARD_LIVE.md` ·
`C:\Dev\SMR-CommunityMods\content\{fix-list,faq,index,for-modders}.md` ·
`docs/PLAYTEST_CHECKLIST.md` items 126–129 · `agent/bugs/F95.md`, `F117.md`
· `agent/bugs/INDEX.md` / `agent/facts/INDEX.md` to find more.

## 1 · Scope fence

**In:** every player-facing string in `metadata.lua` (`description`,
`short_description`, `last_changes`) and its two backups (`UPLOAD_WORKFLOW` §3,
`STORE_CARD_LIVE.md`) — **changed together, in ONE commit, proven byte-identical
by a script, never eyeballed** (link 06's `verify_sync` shape: un-escape the Lua
literal, diff against the §3 plain block, compare the BBCode blocks, compare the
change note); the site's `content/fix-list.md`, `faq.md`, `index.md`,
`for-modders.md`; the agent-doc drift list in §4; `bugs/F115.md`'s three
live-claim lines.

**Out:** `Code/*.lua` (every comment fix the audit found in code is routed to
decision 127's link — see §4 "handed on"); `items.lua`; `version` and every
portal (H-02: no upload, no Mod Editor, no `version`/`version_major`/`version_minor`
edit — each upload bumps by itself); `bugs/` beyond F115's wording and the
pointers §3 names; `TestKit`. Anything else you find: FILE it (a bug entry, a
fact, a checklist line), do not fix it, and append it to this file's outbox
section before you delete the file.

**Bindings:** `EF-054` / `FIX_POLICY` §8 — never name fredware's mod, no
load-order advice to players. `H-04` — never call the release ready. Nothing
here moves a status word; every "fixed" in a player string is a CLAIM until the
post-99 sitting confirms it (owner rule 2026-09-08) — write "re-enabled",
"updated", "works again … derived from the new game code", the way link 06 did,
never "Fixed".

## 2 · The inverted questions (why the template is a template, not a form)

`PUBLIC_SURFACE_SWEEP.md` adds one fix; this patch retires 36 and re-arms
several. Its §0 question "does this fix have a player surface at all?" inverts.
Ask instead, for every surface:

1. **What did a player SEE that they will no longer see**, and is it said without
   reading as a capability loss? Link 06's frame stands: *the game fixed these
   itself, and a fix duplicating the game's own is a risk with no benefit.*
   Three removals a player can notice are already named in the change note
   (habitat residents through a power cut; the line's train count after a
   salvage; the Astrogeologist bonus) — keep all three unless the owner cuts.
2. **Which surfaces name a fix that no longer exists?** Link 06 cleared its fence
   on 2026-09-09 (F108, F107/F105, F73's half, F92 on a KEPT module, the
   judgment-call count 6→3, "Under the hood" 4→3). ⚠️ **Re-check, do not re-hunt:**
   run the retired-phrase sweep over the shipped strings and the site
   (`dust devil`, `automation`, `low-Food`, `first asteroid`, `Micro-G prefab`,
   `milestone`, `tourist`, `satisfaction`, `university`, `battery`, `Eighty`,
   `four of them`, `six judgment`) and report the hits by name; the audit's run
   on 2026-09-09 found only false positives (`Meteor-damaged track`, `trains`).
3. **Which counts were derived from the fix list and are now wrong?** Recount,
   never carry: `grep -c '^??? ' content/fix-list.md` (46 on 2026-09-09), the
   "Under the hood" section count (3), the judgment-call count (3), and
   `python tools/doccheck.py --emit-counts` for the module numbers. A count typed
   from this file is the failure mode.

## 3 · The text changes the audit routes here

### 3.1 ⛔ `last_changes` bullet 2 ↔ ck126 (the audit's F-3; ships inside the mod)

Today's bullet 2 ends: *"And in a save you have already played, two extractor
types keep a small Astrogeologist bonus the pack gave them, which removing the
fix cannot take back; a new game is clean."* Written by link 06 under ck120
(cleanup OFF); link 08 then landed the F95 residue pass (`dcb4ef4`) that takes
it back on load. One of the two is wrong on upload.

- **If ck126 = KEEP the pass:** replace the sentence with —
  *"And in a save you have already played, a small Astrogeologist bonus an
  earlier version of this pack gave two extractor types is removed the next time
  that save loads; a new game never had it."* — and add the FAQ line
  (`faq.md:114-118`, the "Some damage needs active repair" list): append
  *", and a small extractor bonus an earlier version of this pack itself left
  behind"* to the enumerated passes. ⚠️ The pass has never run in a game; the
  wording says what the code does on load, not that it was watched.
- **If ck126 = REMOVE the pass:** the sentence stands verbatim, the FAQ stands,
  and the code change is someone else's (a `Code/` link with the game closed) —
  do NOT ship this sweep against a tree that still carries the pass; wait for
  that commit.

### 3.2 `last_changes` line for F117 — only if ck127(a) landed

If `Fix_ArrivalDeaths` was repaired before the upload, players who ran v5 on
1.1.0 ran the broken version, so §0.4 of the template says it gets a line
(precedent: hotfix 1's "an error popup when landscaping"). Draft, to be fitted
into bullet 4's "Updated for 1.1.0:" sentence: *"…and an error that could
appear when a new arrival's dome was out of walking range is gone."* ⛔ If 127(b)
was chosen, write nothing — a note about a known live error is the reporter's
surface (`FIELD_REPORT_REPLIES.md`), not the store's, and it is hotfix 3's line.

### 3.2b The site's two "built against game version" lines (routed by `smr-bugfixpack-77`, 2026-09-09; verified by 99)

`content/faq.md:176` and `content/for-modders.md:15` both read *"built against
game version **1.0.7.396349**"*. Correct for the v5 players have today, false
on upload — the two-clocks structure of the store card, on the site. Rewrite
both to the 1.1.0 build (`1.1.0.403908`, `EF-075`; re-read the number from
`docs/agent/facts/EF-075.md`, do not type it from here), and say the frozen v5
is the 1.0.7 build (the `legacy-1-0-7.md` page already exists; its download
button was route-checked by the same peer: the `v5-game-1.0.7` release exists,
`api.github.com` 200). Grep the whole `content/` tree for `1.0.7.396349` after —
the sweep that found these two was a full-tree grep, and a third copy would
survive a two-file edit.

### 3.3 Sync, then prove it

`metadata.lua` + `UPLOAD_WORKFLOW` §3 (plain, BBCode, change note, short summary)
+ `STORE_CARD_LIVE.md` (plain, BBCode) in ONE commit. The `STORE_CARD_LIVE`
plain block is +143 chars by design (the two portal passages) — do not "repair"
that. Print the script's output in your close-out. `python tools/upload_preflight.py`
must still read 0 FAIL.

## 4 · Agent-doc drift the audit found (each re-checked 2026-09-09; re-check again — hand-off notes have a shelf life)

Fix in this sweep (docs only):

| where | what | do |
|---|---|---|
| `prompts/hotfix2/README.md:137-138` | "The 1.0.7 tree is GONE (`EF-075`)" — it is ARCHIVED on disk (`ad5f93d`, `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`, `EF-075` updated) | correct the read-path sentence; every "1.0.7 said X" CAN now be a re-read |
| `prompts/PUBLIC_SURFACE_SWEEP.md:100`, `:110`, `:272` | "Eighty repairs" as the card's count word, and a grep for `Eighty` | make the template count-agnostic: "the count word on the card", and point the grep at the current word (`Forty-six` today) — a template that carries a number is the drift this chain measured eight times |
| `prompts/POST_UPLOAD_CLOSE.md:59` | "expect **82 entries**" in the packed-artefact check | replace with the command that regenerates it (`grep -c '^??? ' content/fix-list.md` in the site repo, and `python tools/pack_predict.py <root>` for the file count), not a number |
| `agent/WORKFLOW.md:407` | the measured suite baseline `78/0/16/0 of 94` (2026-08-13, 74-module pack on 1.0.7) reads as live | annotate it VOID with the date and the reason (44 modules, 94 probes, 1.1.0); the new baseline is the post-99 sitting's `RunAll()`, which re-stamps it — do not invent one |
| `agent/bugs/F115.md:10`, `:14`, `:168` | three LIVE claims say the boot MEASURED "17 inactive / 14 named"; the heal-aware reading is 16 (`reports/PACK_1_1_0_REVERIFICATION.md:114`, link 05 §1) | reword the three to "17 as read (16 heal-aware) / 14 named"; ⛔ leave `:135` exactly as it stands — it records the PREDICTION and is the evidence the pair was consistent |
| `agent/prompts/hotfix2/README.md` rows 99/100 | struck by 99; row 100 to be struck by you | on close-out |
| `agent/reports/STORE_CARD_LIVE.md` counts block | re-verify after 3.1 | recount |

Handed on, NOT this sweep's (all are `Code/` comments; route to decision 127's
link, which is in `Code/` with the game closed anyway): `00_Core.lua:239` cites
the deleted `Fix_LastTransmissionStorage` as a donor; `:304-305` cite the deleted
`Fix_AstrogeologistExtractors:174` / `Fix_IndependenceTerraforming:128` and a
moved `Fix_SaintBlessing:151`; `Fix_CrystalMysteryHang.lua:39,76`,
`Fix_ExtenderFlapChurn.lua:48,93`, `Fix_TrackConnectorPingPong.lua:110,209` cite
the deleted `Fix_MeteorStormWedge:154/:165` as a precedent;
`Fix_JumboCaveReinforcementWedge.lua:102` ("keys include a plain 'version'" —
1.1.0 moved it out of the table); `Fix_AnomalyCaveInMap.lua:106` (`:27 object_hex_grid`
— the first `map` index is now `map.buildable`, `CaveInRubble.lua:23`);
`tools/harvest_wrap_targets.py:174` describes the deleted `IsSuitable` replacement.
Put the list, verbatim, in that link's inbox if it has not fired; if it has, file
it as one checklist line under "nothing to decide".

⛔ **Do NOT touch:** `metadata.lua`'s `PackVersion` gloss (`:226`, `:243`, `:336`)
— UNVERIFIABLE from source on either branch, not false, rewritten twice already;
a name grep is the wrong instrument. Every "Eighty-two" in a dated record
(`PLAYTEST_CHECKLIST` history, `RELEASE_OUTBOX`, `RELEASE_PORTAL_PREP`,
`docs/archive/*`). ck112's HOW IT WORKS bullet 3 (ruled to ship as is;
`SELFCHECK_PROMISE_AUDIT.md` owns its future).

## 5 · Close the loop (template §5)

- The bug entry is authority; every public surface is derived from it, never
  the reverse. For every sentence you change, name the entry it derives from.
- `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you": one block, receipts
  for 126/127/128 as they were carried out, and the ONE sitting instruction
  that survives (129: upload, then publish the site, `UPLOAD_WORKFLOW` §4).
- `STATE.md`: one line pointing at your commit; it is byte-capped (warn 12288)
  and a doccheck WARN goes verbatim into your summary.

## 6 · Stop conditions (permission to report instead of push)

- ck126 or ck127 unruled → stop, ask.
- The site repo or `metadata.lua` has an uncommitted change by another session
  (`git status`, `ListAgents`) → message them, do not edit over it.
- The sync script reports a differing line you did not write → stop; someone
  else moved a surface after link 06.
- A retired-phrase hit that is NOT a false positive → file it with the line,
  fix it only if it is inside this fence.

## 7 · What may NOT be claimed

- Not "the surfaces are true" — "the surfaces match the entries and the code as
  read on <date>"; the post-99 sitting is what makes any "works" line true.
- Not "the count is 46" from memory — from the recount, in the commit.
- Not "1.1.0 compatible" anywhere; not "Fixed" anywhere.
- No status moved. No upload. No `version` edit.

## 8 · Close-out (chain rule 2)

`python tools/doccheck.py` GREEN (warns verbatim in the summary) · the sync
script's output · `python tools/upload_preflight.py` 0 FAIL · strike row 100 in
`README.md` with the commit list · `git rm` this file · commit with
`git commit -F <file>` · push. The folder then holds `README.md` alone; say so
in the row.

## Notes from upstream

*(From link 99, `smr-bugfixpack-a8`, 2026-09-09 — the audit's findings that bear
on text, verbatim enough that you do not re-derive them.)*

- **Pass F, measured 2026-09-09:** `description` 5342 chars == `UPLOAD_WORKFLOW` §3
  plain block (0 differing lines); §3 BBCode == `STORE_CARD_LIVE` BBCode;
  `last_changes` == the change-note block; `short_description` == the summary
  block; `STORE_CARD_LIVE` plain is +143 chars, the two portal passages, by
  design. Fix list 46 (`grep -c`), "Under the hood" 3, judgment calls 3 in
  `faq.md` ×3 and `index.md`. All 20 "SOME OF WHAT IT FIXES" bullets and the
  four headline clauses map to live modules. Live site fetched: 82 `<details>`
  (76 success + 6 question), "Eighty-two" on the page — consistent with v5,
  wrong for v6; committed `site/` build = 46 — ck129.
- **Unconfirmed claims in the shipped change note, by bullet** (every one is a
  claim under the 09-08 rule; bullet 5 disclaims them in the player's words,
  accepted): bullet 3 in full; bullet 4 in full; bullet 1's "a few of ours had
  quietly become slightly worse" (R-6/R-23/R-30/R-33, source-read); bullet 2's
  train-count line (R-34). **False if the F95 pass ships:** bullet 2's "cannot
  take back" (§3.1).
- **The chain-shape cause of §3.1**, for `CHAIN_METHOD` if you touch it: the text
  link (06) ran before the last code link (08). A text link that is not
  last-but-one can be falsified by its own chain. Not yours to fix; file it.
- **Drift pattern the audit recorded (Pass H):** every one of the eight links
  corrected its own brief, six of the corrections were COUNTS typed into a
  prompt. Rule: a brief carries the command that regenerates a number, never
  the number. §4's template rows apply it.
- **F117 / F118 / C55 / F60** are filed; only F117 has a player line (§3.2) and
  only if repaired first.
- ⚠️ The kit's `AstrogeologistExtractors` probe matches residue on
  `mod.prop` + `mod.percent == 10` — looser than the pass — so at the sitting
  "probe FAIL + `LEFT … ALONE` line" is the near-miss report, not a bug. The
  owner's 126 block already says so; keep it consistent if you touch that block.
