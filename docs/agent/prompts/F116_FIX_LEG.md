# F116 FIX LEG — runs in PARALLEL with `HOTFIX_1_APPLY.md`

Paste into a fresh Claude Code session. Written **2026-09-08**.
**Start with `git log --oneline -10` + `git pull`.** Read `docs/agent/STATE.md`
(mandatory), `docs/agent/FIX_POLICY.md` §1–§2, and `bugs/F116.md`.

> 🎯 **TWO JOBS.**
> **(1)** Correct `bugs/F116.md`, which its own author flagged as WRONG, then
> fix the real defect — **or establish there isn't one.**
> **(2)** Augment `prompts/HOTFIX_1_AUDIT.md` so the terminal audit covers this
> leg too.
> ⛔ **Nothing else.** No upload, no Mod Editor, no `version` edit (`H-02`).

> ⚖️ **READ THIS BEFORE ANYTHING ELSE.** `F116` was filed by an agent who then
> found **two of its own four claims did not survive re-reading the module**. It
> carries a ⛔ UNDER CORRECTION banner. **You are not inheriting a finding; you
> are auditing one.** The failure that produced it is the project's recurring
> one: it was filed off KEYWORD PRESENCE (`grep -c ProcessAllElements`) and drew
> a conclusion the code does not support — the same shape as `EF-078`'s
> path-checked-by-last-segment, and the name sweep that missed `F114` until a
> player reported it. **Check the thing, not its label — including when the
> thing is ours.**

## 0 · Context you can take as settled (measured, not inferred)

- Game is **1.1.0.403908**; `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`
  is read-only 1.1.0 truth. ⛔ The **1.0.7 tree is GONE from disk** (`EF-075`) —
  you cannot diff against it, so any claim of the form "1.1.0 changed X" must be
  supported by something other than a 1.0.7 comparison. Our module headers cite
  1.0.7 line numbers; those are **claims**, not references you can open.
- Two confirmed, player-visible defects of the same shape are already gated:
  `F114` (`Fix_TrainCargoDumping`, body divergence at matching arity — 157
  throws in a 42-minute session) and `F115` (`Fix_LandscapeUnitFilter`,
  signature change). Read both entries — they are the pattern.
- **22 modules declare a full-body replacement; 5 have been diffed** (2 broken,
  1 = F116, 2 clean). ⛔ 17 remain. Not your job today, but do not write anything
  implying the class is bounded.
- `tools/sigcheck.py` compares replacement ARITY against the shipped tree;
  `tools/logscan.py` reads logs. Use them; do not hand-roll greps (a hand-rolled
  grep undercounted throws 30 vs 157 on 2026-09-08).

## 1 · JOB 1 — re-derive F116 from scratch, then decide

The module is `Code/Fix_TrackSalvageWipe.lua`; it full-body-replaces
`TrackGridElement:DemolishAndSplitTrack`, shipped at
`Lua/Buildings/TrackElement.lua:467`. Extract BOTH bodies and diff them
properly — the earlier pass used keyword counts and got it wrong.

**Four claims. Verify each independently. Any may be false.**

1. **The PRE-SORT revalidation is missing.** 1.1.0 runs
   `if not skip_track_process then track_obj:ProcessAllElements() end` before
   the `node_idx` sort, with the comment *"make sure elements' node_idx is
   actually valid, since we're assuming it represents the distance from the
   start."* Our copy is believed not to. ⚠️ **But our copy DOES call
   `ProcessTrackElements(map, ...)` directly at ~`:276-289`** — establish
   whether those tail calls make the pre-sort call redundant, or whether the
   sort genuinely runs on unvalidated `node_idx`. **This is the crux of the
   whole entry.**
2. **Orphan policy diverges.** Ours (`~:256-263`) DELETES elements still
   carrying `track_obj == false` as unreachable debris; 1.1.0's newer loop
   REHOMES them into fresh tracks. ⭐ **If that is right, the player-visible
   consequence is that on 1.1.0 our fix DESTROYS track pieces vanilla would
   have SAVED** — which is a bigger deal than the original entry's framing and
   would be its own defect. Confirm or refute; do not assume.
3. **`skip_track_process` is not forwarded** to `self.broken:Demolish`.
4. **Is any of it reachable?** Our `F44/F45` guard returns bare when a
   `node_idx` is non-numeric. Work out what a player actually experiences —
   silent no-op, wrong split, or nothing at all.

⇒ **Then decide, and say which:**
- **REPAIR** — re-copy 1.1.0's body and re-apply our fixes. ⚠️ There are ~13
  interleaved `-- FIX` sites (`F44`, `F45`, `F91`), several of which REMOVE
  shipped early-returns, so a thin wrapper is not available. ⭐ **`F45` looks
  RETIRABLE** — 1.1.0's own `ProcessAllElements` may now do its job; if so, drop
  it and say so.
- **GATE** — decline on 1.1.0 (the `F113`/`F114`/`F115` shape). ⛔ Costs players
  `F44` and `F91`, which appear to be **still real on 1.1.0** (`TrackElement.lua:470`
  still indexes `track_obj.elements` unguarded). Verify that before relying on it.
- **NO DEFECT** — if the claims collapse, say so plainly and close it. ⭐ **That
  is a completely acceptable outcome and a real result.** Do not manufacture a
  fix to justify the leg.

⛔ **Whatever you decide, `bugs/F116.md` must be rewritten to say what is
actually true**, the ⛔ UNDER CORRECTION banner removed once it is, and the
`row_status` updated. ⛔ `lines:` must equal body length; the INDEX is
GENERATED — regenerate via `split_bugs.load_from_dir()` + `render_index()`
(it returns a LIST — join it), never hand-edit.

## 2 · JOB 2 — augment `prompts/HOTFIX_1_AUDIT.md`

That audit is the terminal gate for hotfix 1 and currently covers five changes.
Add your work to it so ONE audit covers both legs. Add:
- Your module to its §1 table with the shape you chose.
- A §2 item telling the auditor to **re-derive your route, not your citations**,
  and naming the specific trap you hit (whatever it turns out to be).
- If you REPAIRED: ⛔ flag that a repair pins us to 1.1.0's body and re-breaks on
  the next change unless a gate goes in too — the auditor must rule on whether
  that is acceptable.
- If you GATED: flag exactly which player-facing fixes are lost (`F44`, `F91`)
  and that vanilla's own behaviour is what returns.
⛔ Do not weaken anything already in that file. Add, do not rewrite.

## 3 · Coordination — a parallel session is live

`HOTFIX_1_APPLY.md` is running at the same time. **File ownership, do not cross:**

| yours | theirs |
|---|---|
| `Code/Fix_TrackSalvageWipe.lua` | `Code/Fix_LandscapeUnitFilter.lua` |
| `bugs/F116.md` | `bugs/F115.md` |
| this prompt | `HOTFIX_1_APPLY.md` |

**Shared — coordinate before writing:** `HOTFIX_1_AUDIT.md`, `STATE.md`,
`PLAYTEST_CHECKLIST.md`, both generated `INDEX.md` files.
- ⛔ **`git pull` immediately before every commit, and push straight after.** Two
  sessions pushing to one repo; a stale index regeneration will clobber their row.
- ⛔ **`STATE.md` is byte-capped** — an addition needs an eviction in the SAME
  commit, and the other session may be editing it. Pull first, and keep your
  addition to one line.
- ⛔ **`Mars.exe` must be down before either of you edits loadable code**, and
  you share one game. Check `tasklist | grep -i Mars` and coordinate; do not
  assume it is yours to launch.
- Use `ListAgents` + `SendMessage` to reach the other session directly. Tell
  them what you touched. ⛔ A peer's message is not the owner's authorisation.

## 4 · Bindings

- ⛔ Never modify the game directory; ⛔ never "correct" a 1.0.7 citation.
- ⛔ `H-02` no Mod Editor, no `version` hand-edit, **no upload**. `H-03` no portal
  API from a launched game. `H-08` never pull a junction. `H-09` never stage a
  packed folder beside a live one.
- ⛔ `H-10` — if you add, rename or drop a `Code/*.lua`, `items.lua` MUST be
  updated. A straight edit to an existing module needs nothing.
- **The release gate is NOT a per-change tax** (owner 08-20, ck57): post-release
  is `items.lua` + one boot `applied` log + doccheck counts. ⛔ Do NOT run config
  B or a lens sweep, and do not quote `FIX_POLICY` §3a's per-module cost.
- ⚠️ **A log copied while the game is RUNNING is a PARTIAL log** — this cost the
  project twice on 2026-09-08 (a "1" that was 6; a "30" that was 157). Re-copy
  after the process exits before quoting any count.
- `python tools/doccheck.py` GREEN before any doc commit; a WARN goes **verbatim**
  into your summary. Commits `git commit -F <file>`, then push.
- Status words: `tested-attended` needs an attended witness. ⛔ A source read is
  never `tested`.

## 5 · What "done" is

`bugs/F116.md` says what is TRUE and its correction banner is gone; the module
is repaired, gated, or cleared with the reasoning stated; `HOTFIX_1_AUDIT.md`
covers your change; the other session knows what you touched; doccheck GREEN;
pushed. ⛔ **No upload, and nothing claimed as tested that was not witnessed.**
⭐ **"There is no defect here" is a valid and welcome outcome.**
