# hotfix2 — the chain manifest

Effort: turn the 1.1.0 re-verification's findings into a shipped patch.
Authored 2026-09-08 by `smr-bugfixpack-91` under `prompts/HOTFIX_2_HANDOFF.md`
(now consumed). Method: `agent/reports/CHAIN_METHOD.md`. Authoring mechanics:
`agent/WORKFLOW.md` "Authoring a prompt" elements 1–8.

> ⚖️ **THE BAR, in the owner's words:** *"The last thing I want is to release a
> half-baked patch and then have to immediately repatch it."* Every prompt below
> is written against that sentence. Marathon, not sprint.

## The queue

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| ~~01~~ | ~~`01_CORE_AND_TOOLING.md`~~ | Fable | no | ✅ **DONE 2026-09-08** (`smr-bugfixpack-25`): `probe` form `6d452a3` · `tools/bodycheck.py` + falsifier `401f8a0` · `FIX_POLICY` §2a branch guard + §2b manifest grammar `6db7457` · all 35 KEEP modules stamped `e2490f3`. Outbox is in 02–05 and 99 |
| ~~02~~ | ~~`02_REMOVE_BLOCK.md`~~ | Opus | no | ✅ **DONE 2026-09-08** (`smr-bugfixpack-11`): ck98 ruled DELETE + ck117 ruled KEEP, both in-session. 36 modules deleted with `items.lua` **and** `metadata.lua`'s `code` list, 81→45 in all three `2dc1dbe` · R-7 half-edit + the sanitizer's dead F03 pass `f707903` · 43 bug entries stamped `9b0b82c` · 36 site fix-list entries removed (`SMR-CommunityMods` `7cef4f3`) · `C54` filed. ⛔ No F-5 cleanup — owner ruled it off (ck120). Outbox is in 03, 04, 06 and 99 |
| ~~03~~ | ~~`03_HARMS.md`~~ | Opus | ✅ no | ✅ **DONE 2026-09-08** (`smr-bugfixpack-91`): F-1 `SaintBlessing` behaviour probe (the form's first real use) + a SECOND one-shot save re-base for the 1.1.0 branch `3db4984` · F-2 `StaleReservations` expedition exemption + the narrowed premise stated in the header `f38d6d2` · F-3 `ShelterReflex` half (a) deleted, half (b) kept `19b5aaa` · all three stamped, 3 bug entries given their dated 1.1.0 section, 3 controls batched as ONE ~12-min checklist sitting. `Code/` unchanged at 45/44, so `items.lua` and `metadata.lua` were not opened. ⛔ **Two Test Kit probes now report a FALSE `FAIL`** (`SaintBlessing`, `ShelterReflex`) — filed, not fixed, and the owner is warned in the same checklist block. Outbox is in 04, 04b, 05, 06 and 99 |
| ~~04~~ | ~~`04_RECOPIES.md`~~ | Fable | ✅ no | ✅ **DONE 2026-09-08** (`smr-bugfixpack-ba`): F-7 `RocketDroneChurn` re-copied on the 1.1.0 body carrying the `refuel_disabled` clause, shape-`test` decline on 1.0.7 `3f8394b` · F-6 `PayloadTemplateRefill` re-copied (three 1.1.0 changes carried; gate AFTER the tutorial return; stamp on `Apply`'s CONFIRMED path, `Apply` now a body copy), behaviour-`probe` decline on 1.0.7 `177c7b2` · §7 F116: ck111 rehome loop + ck119 combined-list processing landed in-body, no gate (the WhenActive trap), header rewritten `fc318c7`. Both re-copies stamped, `bodycheck` OK and seen RED both ways; every body diffed TWO-SIDED because the 1.0.7 tree is back (`ad5f93d`). ⛔ Nothing run in a game; `Code/` still 45/44. ⚠️ The `SRC:` re-stamp §7 asked for was a false instruction (the pin hashes the SHIPPED body) — 99's Pass D corrected. A third Test Kit probe FALSE-FAILs (`PayloadTemplateRefill`). Outbox in 06 and 99 |
| ~~04b~~ | ~~`04b_RECOPIES_C.md`~~ | Fable | ✅ no | ✅ **DONE 2026-09-09** (`smr-bugfixpack-94`): F-8 `LandscapeUnitFilter` re-armed on the 1.1.0 `(map, mark, callback)` body, F115 gate KEPT (sense inverted) + behaviour probe `799f145` · F-10 `TrainCargoDumping` re-copied carrying both nil-guards and the BlackCube hook, F114 gate KEPT (inverted) + probe fed the F114 input, ⛔ premise unestablished and said so `3d4c933` · F-9 `VacuumWalks` re-copied on the 98-line rewrite (all seven 1.1.0 changes carried), accidental gate made deliberate, probe on `need_work` `7a401f1`. All three stamped, bodycheck OK and seen RED both ways, each run through the pack's REAL `Require` on a desk harness with the shipped bodies as the game. ⚠️ Drift: my prompt's "reach is Clear-Waste-Rock only" is wrong (inheritance) — in 99's inbox. ⛔ Nothing run in a game; F-9 did NOT need `04c`; 2 more TestKit probes will ERROR (Landscape, Vacuum). Outbox in 06, 07 and 99 |
| ~~05~~ | ~~`05_TOOLS_TAIL.md`~~ | Opus | no | ✅ **DONE 2026-09-09** (`smr-bugfixpack-2b`): A-4 `sigcheck` resolves the `SetGlobal` sites, 38→43 sites, 0 UNRESOLVED `f25e530` · A-3/A-2 `logscan` heal-aware + benign latch = RETIRE, and the `00_Core` log string `c9811e1` · A-1 `GeneForging` off the abandoned `TechDef` map `7ae0fc9` · plus the three items 01/02/03/04b routed here: `doccheck` gains the H-10 module-set gate + `bodycheck --selftest` `29b7a68`, `tools/parsecheck.py` replaces the balance checker three links kept rewriting `8754e00`, `sigcheck --coverage` names 04b's manifest gaps `39e4ffe`. Every new inference ships with a falsifier (9/13/7 legs), each falsified in both directions before use. ⛔ **Census corrected to 64 applied / 16 inactive, not 63/17** — stated, never quietly corrected. ⚠️ NOT a fresh find: the report's own A-3 row already called it; 05 implemented it and added a second independent route (a non-benign latch is always named, and the `:190` report naming 14 omits SaintBlessing), with link 03 supplying a third. ⛔ Nothing run in a game; no status moved. Outbox is in 06, 07 and 99 |
| ~~06~~ | ~~`06_TEXT.md`~~ | Opus | no | ✅ **DONE 2026-09-09** (`smr-bugfixpack-05`): the site text link 02's 36 removals left false — judgment calls 6→**3** in all four places, the F73 card cut to one thing, two dead save-repair passes, "Under the hood" four→three (`SMR-CommunityMods` `5abbfaa`) · the store card recounted from the deployed fix list, 82→**46**, with 11 of its 20 bullets and 3 of its 4 headline clauses replaced, the veto example re-pointed at a live fix id, ck118's 1.0.7 line added, and `last_changes` REWRITTEN wholesale for hotfix 2 — `metadata.lua` + `UPLOAD_WORKFLOW` §3 + `STORE_CARD_LIVE` in ONE commit, proven byte-identical rather than eyeballed `641613e`. ⛔ ck112 bullet 3 UNTOUCHED per the owner's ruling, and the chain's "DEFERRED" label for it corrected. ⛔ No "Fixed" claimed anywhere; nothing run in a game; `version` untouched. ⭐ Found a FOURTH stale public claim nobody had routed (F92, a KEPT module). Outbox is in 99 |
| ~~07~~ | ~~`07_TESTKIT.md`~~ | Opus | no | ✅ **DONE 2026-09-09** (`smr-bugfixpack-ee`): the kit told the truth about a pack that no longer exists. Census RE-DERIVED, not inherited — the brief's "37 orphans / ~45 FAILs" was wrong in a load-bearing way: only **12 of 38 orphan probes call `FixMissing` at all**, so 26 had been silently running against vanilla for weeks. **Unit A** `cd2be43` `FixRetired` + the `retired` kind (PASS = vanilla fixed it, FAIL = a REMOVE was WRONG, ERROR = evidence of nothing) · 8 commits `92325fe`…`320904e` convert **32 retired**, delete **6** by name. ⛔ **SEVEN probes would have reported a confident FAIL on a HEALTHY 1.1.0 game** — `SmallLandscapeSites` asserted OUR clamp of 5 where vanilla's default is 10, `IndependenceTerraforming` encoded a flipped sign convention, `CommandCenterNumbers` demanded shims with 0 hits in the tree, `AstrogeologistExtractors` would have read "pays 0 of 12" against a better label-wide profile, `TrainMinors` demanded OUR recompute of a field that is now display-only, plus 03/04's two — every one caught only by reading the shipped body. **Unit B** `10ad343` all six live-module probes rewritten (incl. link 05's `GeneForging`, which **could not pass in any research state**), + the F114 input and the F66 forced case `4f48c7b` that ck125(a) landed untested. **Unit C** `91e465c` `DispatchReach` REGENERATED with its own tool 105→72 rows (a hand-prune would have missed the rows that MOVED). ⭐ Two new gates: `aliascheck` caught a nil-call bug I had already committed, which `parsecheck` cannot see. ⛔ Nothing ran in a game; census is a PREDICTION. Outbox in 99 |
| ~~08~~ | ~~`08_SAVE_RESIDUE.md`~~ | Opus | ⚠️ raises one | ✅ **DONE 2026-09-09** (`smr-bugfixpack-54`): a third pass in `90_SaveSanitizer.lua` removes our deleted module's two `Effect_ModifyLabel` entries from the persisted `UIColony.label_modifiers` `dcb4ef4`. No new file, so `items.lua`/`metadata.lua` untouched and `Code/` stays 45/44. **§1's kill attempt FAILED and the premise came out STRONGER**: vanilla says *"stored keys are deserialized copies"* itself (`MarsGameEffects.lua:312`, `:443`) and ships FOUR one-shot fixups that would be pointless if a load rebuilt the table, and our own 2026-08-02 keyboard measurement discriminates the two hypotheses. ⛔ **Three route corrections**: `display_text` is **`false`, not `nil`** (the brief's untested tell — a `== nil` test would have made the pass SILENTLY INERT); the key can be READ though not reconstructed, and vanilla's own `RefreshAstrogeologistExtractorBonus` (`:309`) proves the shape, so the match is **narrower** than the value-only one specced; the population is **Astrogeologist colonies only**. ⚠️ **Deliberate deviation: NO one-shot flag** (comparison pass like F35; an unrun premise must not be latched) — reasons in the module header, overturnable by 99. **Unit C raised as checklist 126**, together with the fact that the owner had ruled this cleanup OFF on 09-08 (ck120) before asking for this prompt on 09-09. ⛔ Nothing ran in a game; no status word moved. ⚠️ One vanilla finding filed not fixed (that fixup narrows on `Percent == 20`; archived 1.0.7 pays 10 — NOT established, an intermediate branch is likely). Outbox is in 99 |
| ~~99~~ | ~~`99_TERMINAL_AUDIT.md`~~ | Fable | ✅ raised three | ✅ **DONE 2026-09-09** (`smr-bugfixpack-a8`): **SHIP WITH CHANGES** — `reports/HOTFIX_2_AUDIT.md`. Instruments re-run and falsified by hand; every FIX-set body three-way diffed and holding; Pass D re-read every KEEP wrapper on a changed target (58 branch diffs, four fresh readers, every finding re-opened on the shipped lines): **F117** `ArrivalDeaths` THROWS on 1.1.0 (`ChooseDome` takes the colonist now; P1, source-read, live in v5) ⇒ ck127 · **F118** `LayoutTechLock` clears 1.1.0's delete-on-load registration · **F60** REMOVE candidate (the gate no longer reads the tally) · **C55** vanilla pre-sort assert on repair-site tracks (F45 KEEP confirmed). Pass F: strings vs both backups byte-identical by script, but the change note's bullet 2 contradicts link 08's pass ⇒ ck128 rides ck126 (06 ran before 08). Site publish WITH the upload ⇒ ck129. Pass G: NO boot of the 44-module pack exists; prediction 44/0. ⛔ Nothing ran in a game; no status moved; no code edited. Authored `100_DOCSWEEP.md` as its last act. ✅ **`99_TERMINAL_AUDIT.md` CONSUMED by its own session on the owner's word (2026-09-09), after `99a` was fired** — `99a` §10 step 5 therefore has only itself to `git rm`. The report `reports/HOTFIX_2_AUDIT.md` is the authority and survives |
| ~~99a~~ | ~~`99a_F117_FIX.md`~~ | Opus | no | ✅ **DONE 2026-09-09** (`smr-bugfixpack-0f`): the last code in hotfix 2. **F117** `777249d` — ⛔ **not one token**: the argument is picked by a BEHAVIOUR probe on `Community:GetScoreFor` (two calls on one stub, differing only in where a probe trait is hung; the life-support term cancels in the difference, so no constant's VALUE is read), run at first use because the 1.1.0 body opens on a GameVar, routed through `Require`'s `probe` form, and **fail-closed** — UNKNOWN ⇒ the re-choose stands down and vanilla's destination survives. Falsified on a desk harness that extracts the shipped bodies from **BOTH** trees with `luafn.find_bodies` and the probe from the module: answers `colonist` on 1.1.0 and `traits` on 1.0.7, the old call still THROWS on 1.1.0, and ck118's forbidden shortcut is shown to MIS-SCORE silently on 1.0.7 (110→100) — plus two controls where it must and does answer UNKNOWN. **Riders** `0136af1`: F118's `s_ConstructionControllerDeleteOnLoad` re-assert (`EF-009`/`EF-017` route, no `Require` line — the GameVar is nil at apply time) and the `FlightPolicies` named decline. **`cb6415f`** publishes `SMRFixPack.ArrivalDeaths.ReadArgShape` (pure) so the kit asserts THIS module's verdict, not a copy — kit probe `ArrivalDeathsChooseDomeArg` in wave 2, **no new kit file so `metadata.lua` stayed shut and the `SELFCHECK_PILOT` lane was never entered** (kit `c1114ed`, local). ⛔ Nothing ran in a game; NEITHER defect reproduced; NO status word moved; F118 has no probe and its effect is still unmeasured. ⚠️ Both falsifiers are SCRATCHPAD-only — promoting them is checklist **131**. Outbox: `100_DOCSWEEP` §3.2 keys off `777249d` |
| ~~99b~~ | ~~`99b_BENCH.md`~~ | Fable | no | ✅ **DONE 2026-09-09 (late)** (`smr-bugfixpack-96`): the bench link — nothing ran in a game, no status word moved, `Code/` bodies byte-identical. **Unit A** kit `29fd13b`: `AnomalyCaveInMap`'s fake `[LUA ERROR] HGE::GetDomeAtHex` header gone (the stand-in map now answers with a stand-in strut that takes the shipped `:109-113` branch, `ok` is asserted, C43's two dead stubs go with it) · `LandscapeCostGuard`'s BACKWARDS FAIL repaired at the stub (`GetTargetAmount`, called only after delegation; `:748` tail stood in) · `MoraleComfortTooltip` FAIL→named SKIP on every path (beyond the four, free) · kit `4f062de`: `LanderReturnFuel`'s unsatisfiable `reserve` assertion dropped (`:1894` returns one value) · `SaveSanitizerUpgradeLeak` DELETED (its pass went at `f707903`; F03 `closed`) ⇒ probes 95→94. **Unit B** (same commit): `LanderEmptyLaunch` + `FreedHousingNotice` REBUILT on the 1.1.0 bodies read line by line, desk-falsified 9/9 both ways with the OLD text reproducing each sitting ERROR line byte for byte; ⚠️ 1.1.0's one-hour automode gate (`UniversalRocket.lua:554-556`) is a false-FAIL trap for a fresh fixture and NARROWS F67 without fixing it (K-26 KEEP stands). **Unit C** `a8e0ca2`: the §4 hand-off list drained — 6 sites + 1 adjacent cite; `harvest_wrap_targets.py:174` was already fixed in `29b7a68` (the list entry was stale, the file was not); no comment described changed behaviour. **Unit D** `94cfa2c`: `bugs/F117.md` §Control RE-DERIVED — the far landing yields an EMPTY list; the elevator route stands down BY DESIGN (paired picks); the forceable route is the passenger-station sweep (`_GameUtils.lua:450-478`), desk 8/8 on the shipped span, ⛔ UNTESTED in play, in-play falsifier = `CachedArgShape()` nil ⇒ vacuous; frequency claim WITHDRAWN. **Unit E**: STATE measured 12215 B / 129 lines vs warn 12288, growing ⇒ checklist **132**; **131** re-raised once. Left by name: `C47OpenFarmSeedBufferShape` FAIL (needs a C47 re-derivation); retired ERRORs `LanderCargoRatchet`/`DroneUnreachableForever`/`AutoExportPriority`. All four desk harnesses PROMOTED to `tools/desk_*.py` right after (ck131 ruled; `tools/deskbench.py` runs them). The commit that strikes this row `git rm`s the prompt |
| 100 | `100_DOCSWEEP.md` | Opus | ✅ 126 + 127 RULED `ab7e0f5` | ⏳ **AUTHORED 2026-09-09 by link 99; NOT FIRED.** The inverted public-surface sweep for this patch plus the agent-doc drift the audit found. ⛔ Fires only after the owner rules **126** (the F95 pass) and **127** (F117 first or later), and BEFORE the upload sitting — the change note's bullet 2 ships inside `metadata.lua` and today contradicts the pass link 08 built; both wordings are in the prompt. Seeds re-checked 2026-09-09: link 06's fence is CLEAN; still live are `README.md:137` ("1.0.7 tree is GONE" — it is archived), `PUBLIC_SURFACE_SWEEP.md:100/:110/:272` ("Eighty"), `POST_UPLOAD_CLOSE.md:59` ("82 entries"), `WORKFLOW.md:407` (a VOID suite baseline), `bugs/F115.md:10/:14/:168` ("17 inactive" as a measurement). `PackVersion` gloss: do not touch. ⚠️ A folder holding this file + `README.md` is the chain's designed end state, not an unfinished chain |

> ✅ **THE FOLDER IS NOW `100_DOCSWEEP.md` + THIS FILE, AND THAT IS THE DESIGNED
> END STATE — not an unfinished chain.** Every other prompt has been consumed by
> its own session (99 by `aac8e9c`, 99a and 99b by their close-outs). One link is
> left: `100_DOCSWEEP`, and then the upload sitting.
>
> 📨 **For `100_DOCSWEEP`'s session:** §3.2 keys off 99a's commit, and it exists —
> **`777249d`** (the F117 repair). The riders are `0136af1`, the kit hook is
> `cb6415f`. ⛔ No status word moved and neither defect was reproduced, so the
> change-note line must not say "Fixed". One extra thing to carry: the routed
> stale-1.0.7 instance at the bottom of this file. (Checklist **131** is RULED
> and LANDED — the desk falsifiers are `tools/desk_*.py`, run by
> `tools/deskbench.py`; nothing to carry.)
> ⭐ **From 99b (2026-09-09 late):** your §4 "Handed on, NOT this sweep's" list
> is DRAINED (`a8e0ca2`) — do not re-file it and do not re-fix it. The two kit
> items that joined the upload blockers 09-09 eve have landed (kit `29fd13b`,
> `4f062de`), so you are again the ONLY thing between the tree and the upload.
> `bugs/F117.md` §Control is re-derived (`94cfa2c`): if your §3.2 line describes
> when F117 bites, it is a rare layout (passenger-station arrivals), not
> "ordinary mid-game". STATE.md sits just under its warn (checklist **132**;
> measure it, never quote it): expect the WARN, add facts not stories, and evict
> per `STATE_EVICTION.md` with a SESSION_LOG grave. Your full inbox is in your
> `## Notes from upstream`.

**Ordering.** 01 is strictly first — 02, 03 and 04 all use `bodycheck.py` and the
`probe` form. **02 before 03 and 04**, because 02 owns `items.lua` and the
`metadata.lua` `code` list and no other prompt may touch them. 03 and 04 are
independent of each other and may run in either order. **04 and 04b are also
independent of each other** — either order, or in parallel by two sessions, since
they share no module and no file. 05 and 06 are independent of everything except
01. **07 runs after 02, 03, 04 AND 04b** (it needs the final module set) and
before 99; it is independent of 05 and 06, except that it re-reads the
`GeneForging` probe if 05 has closed. **08 runs after 07** (07 found the residue
and wrote the probe that reports it) and before 99; it touches ONE module and is
independent of everything else. 99 is last and runs only on an empty folder — ⚠️ **and `100_DOCSWEEP.md`
comes AFTER 99, authored BY 99.** A folder holding `99` + `100` + this file at
the end is the designed end state, not an unfinished chain.

⭐ **Why 04 split into 04 + 04b, recorded per `CHAIN_METHOD` §3.** Split
2026-09-08 **before either half ran**, under rule 4 and the owner's explicit
pre-authorisation (ck123: *"If the work is really that heavy we should have a 04
and and 04b"*). Six modules at this discipline — a body diff, a re-copy, a
manifest stamp, a `probe` gate, `bodycheck.py` either side and its own commit
each — do not fit one context, and F-9 alone is a ~98-line rewritten function.
⚠️ The judgement was made up front rather than left to a session to discover
mid-link, because **a link cannot see its own context budget** (owner,
2026-09-08). ⛔ Both halves carry a FULL inbox; neither points at the other for
link 01's probe spec, because each `git rm`s itself on close-out.

⚠️ **Deviation from the handoff's suggested split, stated per `CHAIN_METHOD` §3.**
The handoff put F-4/F-5/R-20 in the "harms" prompt and the rest of the removals
in the "remove block". This chain instead cuts **deletions vs repairs**: every
module deletion lands in 02. Reason: `H-10` inverts on this patch — with 37
modules leaving, the failure mode is a module dropped from `Code/` but left in
`items.lua` (or the reverse), and both portals rebuild `metadata.lua`'s `code`
list from items on a forced save. Splitting the deletions across two prompts
splits that consistency check across two sessions. One prompt owns it.

## Binding chain rules — every prompt inherits these

1. **Staleness check first.** `git log --oneline -10`, `git pull`, `ListAgents`.
   Several smr-bugfixpack sessions edit this tree at once; message any peer whose
   lane you are about to enter, and never touch a stranger's unstaged file.
2. **Inbox / outbox.** Read `## Notes from upstream` at the bottom of your prompt
   before you start. On close-out, append your outbox to the NEXT prompt's
   `## Notes from upstream` **and** to `99_TERMINAL_AUDIT.md`'s, update your row
   in this README (strike it), `git rm` your own prompt file, and commit all of
   it together.
3. **Route, do not drop.** Anything you find that is out of your fence gets
   FILED (a bug entry, a fact, a checklist item), never fixed and never dropped.
   Unsure whether it is yours? **STOP AND ASK** — do not guess.
4. **Self-split at a clean commit boundary.** If the job will not finish
   comfortably in this context, split it: commit what is done, write `NNb_*.md`
   as a first-class chain member with a full inbox, add its row here. Never push
   a job to the edge of a window.
5. **Capture drift as evidence, not shame.** Every mistake you catch in your own
   or an upstream prompt's work — including ten-second fixes — gets appended to
   99's `## Notes from upstream`. A silently-corrected instance is destroyed
   evidence.
6. **Re-derive the ROUTE, always.** The pinned shapes in your prompt are design,
   not permission to skip verification. Every route failure this project has had
   sat on top of individually-correct citations (`CHAIN_METHOD` §2.3). Read the
   1.1.0 body before you edit against it.
7. **⛔ No instrument here is a clearance.** `sigcheck.py` bounds ARITY only and
   rated `Fix_TrackSalvageWipe` OK both before and after its defect was found; a
   name sweep sees names; the runtime existence checks see existence. F114 was
   invisible to all three. Only a body read clears a body.
8. **Live todo list, one item per commit-and-verify unit**, marked complete the
   moment it completes. The owner reads it to decide when to step in.
9. **Green gates before every commit:** `python tools/doccheck.py` GREEN,
   `python tools/sigcheck.py`, `python tools/bodycheck.py` (from 01 onward), and
   a parse sweep of every `.lua` you touched. Commit with `git commit -F <file>`
   (embedded quotes split args under PS 5.1), then push.
10. **⛔ `Code/` edits only with `Mars.exe` closed.** A packed folder must never
    be staged beside a live junction (`H-09`).
11. **⛔ Never move a status you did not witness.** A source read is never
    `tested`. A patch note that says "Fixed" is a CLAIM, false until confirmed
    (owner rule, 2026-09-08).
12. **Bindings in force:** `H-02` (no Mod Editor, no `version` edit, no upload —
    those are the owner's sitting), `H-03`, `H-04`, `H-08`, `H-09`, `H-10`.
    Owner decisions go to `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on
    you", never only into an agent doc.
13. **A doccheck WARN goes verbatim into your summary.** `STATE.md` is
    byte-capped (warn **12288**, raised from 9216 by owner ruling 2026-09-09
    because items were going unrecorded). ⚠️ **Headroom is a number that goes
    stale in hours — measure it (`python tools/doccheck.py`, the `STATE + STUBS`
    line) and never quote it from here.** 99b found the file 73 B under the warn
    and compressed four history lines to pointers (grave in its close-out
    commit); the next link should expect the warn rather than assume room. It is
    still a kernel: add the fact, not the story, and when the warn does fire it
    goes verbatim to the owner (`prompts/STATE_EVICTION.md`).

## ⛔ The constraint that binds every code prompt (ck118)

Nothing stops this build reaching a **1.0.7** player. Our `lua_revision` is
350453 and 1.1.0's `ModMinLuaRevision` / `ModRequiredLuaRevision` are BOTH
350453, so `ModDef:IsObsolete()` is false on both branches and the pack installs
and loads on 1.0.7 silently. For a deletion that is a regression. **For a module
carrying a 1.1.0 function body it is the F114 failure mode in reverse** — our
copy applied over a function that does not match it.

⇒ **Every module that gains a 1.1.0 body must carry a self-check that DECLINES on
1.0.7**, and that check must test the thing, not a label. This is not a
preference and it is not conditional on decision 98.

## Read path — declared

`docs/agent/STATE.md` (mandatory) · `agent/reports/VANILLA_FIX_QA.md` **§0 first**
· `agent/reports/PACK_1_1_0_REVERIFICATION.md` (the rows your prompt names) ·
`agent/FIX_POLICY.md` · `agent/WORKFLOW.md` "Authoring a prompt" ·
`docs/PLAYTEST_CHECKLIST.md` items 98, 111–118 · your own prompt's inbox.
⛔ QA §0 corrects the main report in four places and the main report says so —
read it before any row of the main report.

Game source: the 1.1.0 tree at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`. The 1.0.7 tree is
GONE (`EF-075`) — every "1.0.7 said X" is our module's own header or a bug entry,
never a re-read.

> ⚠️ **ROUTED, NOT FIXED (99a, 2026-09-09 — for `100_DOCSWEEP`).** The paragraph
> directly above is **stale and load-bearing**: the 1.0.7 tree is **archived, not
> gone**, at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` (`ad5f93d`, `EF-075`), and
> 99a read both trees side by side for every claim it made. Left alone here
> because it is outside 99a's four-item fence — it belongs to the same "1.0.7
> tree is GONE" seed `100_DOCSWEEP` already carries for `README.md:137`, and this
> is a **second instance of it** that the seed list does not name.
