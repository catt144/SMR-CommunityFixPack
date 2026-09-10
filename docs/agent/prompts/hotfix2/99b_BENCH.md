# 99b · The bench link — everything owed before the doc sweep, and nothing that needs a game

Paste into a fresh Claude Code session. **No owner needed. No game is launched.**
This link drains every item standing between hotfix 2 and `100_DOCSWEEP`, except
the two repairs that can only be settled by watching them in play.

**Staleness anchor: `044354b`.** `git log --oneline -15` · `git pull` ·
`ListAgents` before you touch anything — several sessions share this worktree and
a directory pathspec has twice swept a stranger's work into a commit.

> ⚖️ **THE BAR, unchanged, in the owner's words:** *"The last thing I want is to
> release a half-baked patch and then have to immediately repatch it."*

> ⛔ **`H-04` BINDS THIS FILE.** Nothing here clears the release. This link
> removes *reasons not to ship*; it does not produce a verdict that we should.

## 0 · Why this link exists, and what it deliberately does NOT do

Sitting 2 (2026-09-09 evening, `1851b1a`) exercised six repairs in a game and
passed all six. The owner then ruled three things that had been offered as
"file for hotfix 3": **repair the stale instruments now**, **build the missing
probes now**, and **withdraw F03's stale claim**. F03 is done (`closed`,
`1851b1a`). The rest is this link.

⛔ **OUT OF SCOPE, by the owner's explicit instruction: the "repaired but never
observed" pair.** `F117` and `F118` are repaired, source-derived, and have never
been seen working or failing. **This link does not try to observe them**, does
not launch a game, and does not move their status words. It touches F117 in
exactly one way — §4, correcting a recipe that is *known wrong* — because leaving
a false recipe in a bug entry is a defect in the record, not an observation.

⛔ **This link does NOT run `100_DOCSWEEP`.** That is the next and last link.
Everything here is upstream of it.

## 1 · Live todo list — REQUIRED

Build it before the first edit, one item per unit below. Mark each the moment it
completes; keep exactly one in progress; put the **reading** in the item text.
⚠️ If a unit turns out to be two things, split it at that moment. There may be no
`TodoWrite` tool — then keep the list as a visible block in every message.

## 2 · Preconditions

| gate | check | why |
|---|---|---|
| **`Mars.exe` not running** | `tasklist` | ⛔ **Units A and B edit the Test Kit.** Editing loadable code while a game runs makes the kit on disk stop matching the kit in the session, and any suite result becomes unattributable. This is why sitting 2 deliberately deferred this work rather than doing it between rows |
| **Stale-probe gate** | `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` — CLEAN is zero | ⛔ and re-run it at close-out, because this link ADDS probe code |
| `97`/`98` disarmed, `96` absent | kit `metadata.lua` code list | keep them so (`EF-081`) |
| tree clean, `git pull` done | `git status --short` | peers share this worktree |

⚠️ **The Test Kit is local-only BY DESIGN and that is settled.** It is not
published and never will be. ⛔ Do not raise it as an owed item; do not try to
ship it. Commit it in its own repo as usual.

## 3 · Unit A — repair the four stale instruments (owner-ruled: **now**)

All four are the **instrument**, not the pack. Sitting 1 triaged them; sitting 2
re-confirmed the census unchanged. ⛔ **None of them is evidence of a defect in
`Code/`** — do not "fix" the pack to make a probe pass.

| # | probe | what is actually wrong | ⭐ the trap |
|---|---|---|---|
| A1 | **`CaveInRubble` / `IsNearDome` stub gap** | prints a genuine **`[LUA ERROR] HGE::GetDomeAtHex`** header into **every** log, caught in a `pcall`. Harmless to play | ⭐ **Do this one first.** It is the only one with a cost outside the suite: it will trip every future `logscan` run, including the owner's, and a real header from a fake problem is exactly what trains people to ignore headers |
| A2 | **`LandscapeCostGuard`** `[retired]` | its stub `request` lacks `GetTargetAmount`, which 1.1.0's `InterruptExcessDeliveries` now calls (`ConstructionSite.lua:1385`) | ⛔ **The FAIL is BACKWARDS.** Reaching that line *proves* the body delegated, which *confirms* the F105/F107 removal. Repair the stub; do not touch the verdict it was reporting |
| A3 | **`LanderReturnFuel`** `[retired]` | asserts a two-value return the no-destination branch never makes (`UniversalRocket.lua:1891-94`) | its meaningful clause already passed at 3500 — keep that clause, drop the assertion the branch cannot satisfy |
| A4 | **`SaveSanitizerUpgradeLeak`** `[behavior]` | outlived the pass it tested — that pass was deleted `f707903` under ck117 | ⭐ F03 is now `closed` (`1851b1a`) for the same reason. **Deleting this probe is a legitimate repair**; a probe for code that no longer exists is not coverage. Decide delete-vs-rewrite on that basis and say which you chose and why |

⚠️ **`C47OpenFarmSeedBufferShape` also FAILs** (1.1.0 halved Herbs to 50
seeds/hex) and **`MoraleComfortTooltip` cannot pass once retired** (its own title
says it needs a screen check). Neither is in the owner's ruling of four.
⇒ **Fix them only if the fix is obvious and free; otherwise leave them and say
so by name.** ⛔ Do not silently widen the ruling.

## 4 · Unit B — build the two missing probes (owner-ruled: **build**)

`LanderEmptyLaunch` and `FreedHousingNotice` are **shipped modules with no
working coverage at all** — their `[behavior]` probes ERROR on 1.1.0 methods that
were removed. Blind spots, not defects.

1. Read the two shipped modules in `Code/` first, then the 1.1.0 bodies they
   wrap. ⛔ **Write the probe against what the shipped body does now**, not
   against what the old probe asserted — link 07 found **seven** probes that
   would have reported a confident FAIL on a healthy 1.1.0 game, every one caught
   only by reading the shipped body.
2. ⭐ **Prefer a `probe`-form behaviour question over a shape assertion.** The
   pack's own F117 repair is the model: ask the shipped body which shape it has,
   and treat "cannot tell" as a decided verdict rather than a guess.
3. ⛔ **A probe that cannot fail is not coverage.** For each one, state in the
   file what would make it FAIL, and *falsify it in both directions on a desk
   harness before committing* — that is house practice (links 04b, 05, 07).
4. Run `python tools/doccheck.py` (probe count moves) and `aliascheck`.

## 5 · Unit C — the orphaned `Code/` comment corrections

⚠️ **`100_DOCSWEEP` §4 hands a list of `Code/` comment errors to "decision 127's
link, which is in `Code/` with the game closed anyway". That link (`99a`) has
FIRED AND CLOSED.** The list is therefore orphaned, and this link is the session
it was waiting for: `Code/`, game closed. The sweep's own instruction for that
case is *"if it has [fired], file it as one checklist line under 'nothing to
decide'"* — ⭐ **but fixing them is better than filing them, and cheap here.**

Take the list **verbatim** from `100_DOCSWEEP.md` §4 ("Handed on, NOT this
sweep's"). It is stale comments citing deleted or moved things:
`00_Core.lua:239`, `:304-305` · `Fix_CrystalMysteryHang.lua:39,76` ·
`Fix_ExtenderFlapChurn.lua:48,93` · `Fix_TrackConnectorPingPong.lua:110,209` ·
`Fix_JumboCaveReinforcementWedge.lua:102` · `Fix_AnomalyCaveInMap.lua:106` ·
`tools/harvest_wrap_targets.py:174`.

⛔ **Re-check every line before editing it** — that list was compiled 2026-09-09
and hand-off notes have a shelf life. ⛔ **Comments only.** If a comment turns out
to be describing real behaviour that changed, that is a **finding**, not a comment
fix: stop, file it, and do not repair code in this link.
⚠️ Editing comments does not change `Code/` file count or `items.lua` — if you
find yourself touching either, you have left the unit (`H-10`).

## 6 · Unit D — F117's control recipe (desk only)

⛔ **This is NOT an attempt to observe F117.** It repairs a *document* that is
known to be wrong.

`bugs/F117.md` §Control and the (now rewritten) sitting brief both said: *land a
passenger rocket beyond walking distance of **every** dome*. Sitting 2 refuted
that from the shipped source:

* `GetDomesReachableByColonists` (`_GameUtils.lua:390-420`) adds a dome to the
  candidate list **only** if it IS in walking distance (and welcoming), or sits
  behind a reachable elevator.
* `ChooseDome` (`:486-500`) is `for _, dome in ipairs(domes) do dome:GetScoreFor(colonist)`.

⇒ land beyond walking distance of everything and the list is **empty**,
`GetScoreFor` is never called, and the throw site (`Community.lua:442`/`:449`) is
unreachable. **The row would have shown a clean arrival whether or not the bug
were present.**

Three things owed:

1. **Fix `bugs/F117.md` §Control.** Either derive a recipe that provably reaches
   `GetScoreFor` — the branch needs the assigned dome out of walking distance
   **while another welcoming dome is in it**, and the live route looks to be the
   **elevator / cross-map** case the module itself singles out — or record
   plainly that no recipe is forceable and say why. ⛔ **Do not replace one
   unverified recipe with another.** If you cannot falsify it at the desk, write
   down that it is untested.
2. ⚠️ **Re-examine the entry's frequency claim.** It says the trigger is
   "ordinary mid-game". Sitting 2's trace suggests **rarer**. That is a claim
   about player impact and it is currently unsupported. Correct it or mark it
   unestablished. ⛔ Do not leave it as it stands.
3. ⭐ **Promote the desk falsifiers.** `bugs/F117.md` carries an ask to promote
   the scratchpad-only falsifiers into `tools/`; the owner was offered the F117
   bench in checklist 131 and never answered. **Raise it once, as one checklist
   line — do not build it unasked.**

## 7 · Unit E — one owner decision to surface, not to make

⚠️ **`STATE.md` sits close to its warn threshold with very little headroom.**
The warn was raised 9 KiB → 12 KiB on 2026-09-09 *for exactly this pathology*,
budgeted in its own source comment as "~32 lines spare … a runway, not a licence"
with a written revisit condition — and the runway was consumed the same day by
genuine 1.1.0 fallout. Sitting 2's close-out evicted twice to get back under.

⛔ **Not an agent's call, and the HARD cap stays where it is either way.** Put it
to the owner as one checklist line: **raise the warn again, or accept
per-session eviction until the 1.1.0 fallout is closed?** ⭐ Measure the current
number yourself (`python tools/doccheck.py`) — ⛔ never quote a stored byte count.

## 8 · What may NOT be claimed

- ⛔ **Not "hotfix 2 is ready."** `H-04`. `100_DOCSWEEP` still has to run, and the
  upload is the owner's.
- ⛔ **Not "F117/F118 are fixed."** Nothing in this link observes either. No
  status word moves.
- ⛔ **Not "the suite is clean"** — say *"no failures beyond the triaged
  instrument noise"*, and re-state the noise list by name if you re-run it.
- ⛔ **Not a `tested` grant on anything.** No game runs in this link.
- ⛔ **Never quote a count from a partially-copied log** (no logs here — if you
  find yourself reading one, you have left the scope).
- ⛔ **SKIPs BY NAME, never a total.**

## 9 · Stop conditions — permission to report instead of push

- **A comment in Unit C turns out to describe real behaviour that changed** ⇒
  stop, file it, do not repair code here. That is a finding and it outranks
  finishing the unit.
- **A probe in Unit B cannot be made to fail** ⇒ say so and leave it unbuilt
  rather than shipping a probe that always passes. A vacuous probe is worse than
  a named blind spot, because it enters the record as coverage.
- **A repair in Unit A would require touching `Code/`** ⇒ stop. These are
  instrument repairs; a pack change is a different link with a different bar.
- **The kit census changes in a way you did not intend** ⇒ report the before and
  after by name, never as a total.

## 10 · Close-out

1. `python tools/doccheck.py` GREEN before any doc commit; **WARNs verbatim** in
   the summary (18 standing `frozen index-row cell` warns are expected — report,
   do not "fix"). ⚠️ The probe count moves in Unit B; re-emit the build-state
   block with `--emit-counts`, never hand-typed.
2. **Re-run the stale-probe gate** — this link adds probe code.
3. Commit by **explicit individual file paths** on `add` AND `commit`,
   `git commit -F <file>`, then push. The kit commits in its own repo.
4. **Update `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"**: the existing
   block, not a second one. Receipts for the three ruled items; Unit E's question;
   Unit D's outcome stated as *"recipe corrected"* or *"no forceable recipe —
   F117 remains untestable"*, whichever is true.
5. **Update `STATE.md`** in the kernel's one-fact-per-line style, minding §7.
6. **Update `prompts/hotfix2/README.md`**: mark this row done with its commits,
   in the voice of the rows above it.
7. ⭐ **`git rm` THIS FILE** when every unit is done or explicitly shelved by an
   owner ruling, and **name the deleting commit in the close-out**. If units
   remain, rewrite this file for what is left rather than adding another link.
8. **Hand off to `100_DOCSWEEP.md`** — say in the close-out that it is now the
   only thing between the tree and the upload, and ⚠️ tell it that Unit C
   consumed its §4 "Handed on, NOT this sweep's" list so it does not re-file it.

## 11 · Read path — files, not folders

`agent/STATE.md` (mandatory) · `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting
on you", the 2026-09-09 (evening) block · `archive/SESSION_LOG.md` newest two ·
`prompts/hotfix2/100_DOCSWEEP.md` §4 (Unit C's source list — **verbatim**) ·
`prompts/hotfix2/README.md` (chain manifest) · `agent/bugs/F117.md` (⚠️ its
§Control is WRONG — Unit D) · `agent/FIX_POLICY.md` §2a/§2b ·
`../SMR-BugFixPack-TestKit/Code/` · `agent/facts/INDEX.md` — ⛔ check it before
deriving any engine claim.
