# C90 — build the two apply-success guards (one-off, model-agnostic)

**Written 2026-09-12 by `smr-bugfixpack-c2`. Lifecycle: `git rm` this file when it has been fired.**
**Owner ruling that authorises it, 2026-09-12: v10 CARRIES C90.** The shape was already ruled; what is
new is the ship authorisation. Both live in `docs/PLAYTEST_CHECKLIST.md`, checklist **158**'s C90 paragraph.

> ⛔ **This is a BUILD, and it is on the v10 critical path.** It is the only item from
> `perma/HANDOFF_ORCHESTRATOR.md` §3b that the owner has pulled forward. Do not take anything else from
> §3b while you are in here, and do not open a new front, audit or sweep before v10 is live.

> ⚠️ **A SIBLING SESSION IS WORKING IN THIS TREE RIGHT NOW.** `smr-bugfixpack-c2` lands the three ruled
> retirements (F37, F43+F118, F31) in parallel. §6 is the lane fence — read it before your first write.

---

## 0 · Orient (before you touch anything)

`git pull` · `git log --oneline -15` · `git status --short` · `ListAgents` · `docs/agent/STATE.md` ·
`prompts/perma/DISPATCH.md` §0–§1. **Open a live todo list and keep it current** — the owner reads it to
decide when to step in.

Then read, in this order, and do not re-derive what they already establish:

1. `docs/agent/bugs/C90.md` — the mechanism, the six measured rows, the census, the limits.
2. `docs/agent/reports/DESKBENCH_C90.md` — the full measurement, the eight scratch falsifiers, the limits.
3. `Code/Fix_FactionDomeSizeGate.lua:149`, `:235`, `:415-430` — **C89, which already does this correctly.**

⛔ **Do not re-measure C90.** The desk work is done: 18/18 control, eight scratch variants discriminating,
a complete four-plus-two callback census. You are building the repair that measurement already scoped.

---

## 1 · The job, and its boundary

Add a **per-module apply-success guard** to exactly two modules:

- `Code/Fix_SaintBlessing.lua`
- `Code/Fix_SinkholeIndestructible.lua`

That is the whole job.

⛔ **NOT the shared core's apply-verdict contract.** `Code/00_Core.lua` is out of scope. The census in
`bugs/C90.md` §2c is why: the other two DataPatch callers already guard or have no decline path, and
neither `OnDataReady` caller exposes the mutation bypass. Widening this is a different, unruled change.

⛔ **NEVER gate the pass on `entry.status == "active"`.** `run_apply` (`00_Core.lua:460`) writes status
only *after* `apply()` returns, so a legitimate live re-apply calls the pass while the previous status
still reads inactive. Gating on status would break working re-applies. Use a module-local flag.

### Why these two and not the others

Both currently write data **before** they notice a missing target, then call `ctx.heal()` — which
restores `active` and clears the failed self-check out of UpdateSuspects. Measured endpoints:

| module | what it writes after a declined self-check |
|---|---|
| `Fix_SinkholeIndestructible` | `class.indestructible = true` (`:102`), then `template.indestructible = true` (`:107`), then heal (`:109-114`) — the pass never checks or calls the missing `DestroyBuildingImmediate` at all |
| `Fix_SaintBlessing` (1.0.7 data) | `rebased_from[Saint]` (`:268`), then `Saint.modify_trait = "TraitReligious"` (`:269`), then heal |
| `Fix_SaintBlessing` (1.1.0 data) | arms the save repair (`rebase_resolved = candidates`, `:280`), then heal (`:281`) |

---

## 2 · The shape to copy — C89 already carries it

`Fix_FactionDomeSizeGate.lua` was built with this guard and its comment block already names C90 and both
of your target modules. **Match it**, including the reasoning comment — a future reader needs the *why*:

```lua
local self_check_passed = false            -- :149, file scope

-- inside pass = function(ctx)
    if not self_check_passed then return end    -- :235, BEFORE any pass work

-- inside apply = function()
    local err = SMRFixPack.Require(FIX_ID, { ... })
    if err then return err end
    self_check_passed = true                    -- :424, AFTER Require clears
    patch()
```

The flag must be tested **before the pass does any work at all** — before the target lookups, not merely
before the writes. Sinkhole's guard goes ahead of the `g_Classes` lookup at `:86`; Saint's ahead of the
`TraitPresets` lookup at `:207`.

`FIX_POLICY.md` §2 (enable path / declaring class) and §2a (a branch guard is a behaviour probe, never a
version check) still bind. You are adding a guard, not a branch — do not introduce a version test.

---

## 3 · ⭐ VERIFY THIS FIRST — the reset/retry gap, and C89 may share it

`bugs/C90.md` requires that the implementation *"define reset/retry behavior, rather than treating a
once-true flag as an everlasting successful verdict."* **C89's shape as written may not satisfy that**,
and if so, copying it verbatim would carry the gap into two more modules.

**The claim, stated so you can falsify it:** `Fix_FactionDomeSizeGate.lua` sets `self_check_passed = true`
at `:424` and never assigns `false` anywhere after its `:149` initialiser. `run_apply` is called from two
sites (`00_Core.lua:525` and `:558`), so a re-apply is a real path. ⇒ **If a first apply succeeds and a
later re-apply's `Require` fails, the flag stays true and the pass keeps running on a module whose
self-check has now declined** — the exact everlasting-verdict shape C90's entry forbids.

⛔ **This is a claim I derived from reading, not a measured fact, and it is not a filed defect.** Establish
it or refute it **before** you write the guards:

- Read `00_Core.lua:460-530` and `:540-570` and determine whether `apply()` can actually re-run after a
  success, and whether a re-run's `Require` can fail where the first passed.
- If it **can**: the correct shape sets the flag `false` at the top of `apply()`, before `Require` — so a
  declining re-apply revokes the previous verdict. Build your two guards that way, and say so in the
  comment.
- If it **cannot**: build C89's shape verbatim and **record in `bugs/C90.md` why reset is moot**, naming
  the ordering that makes it so. That discharges the entry's reset/retry demand honestly.

**Either way, report to the owner what you found about C89.** ⛔ **Do not back-port a change into
`Fix_FactionDomeSizeGate.lua` without asking** — C89 is `tested-attended` in this release and was attended
at the keyboard on 09-12 (ck158, the boundary-pair A/B). Touching it re-opens an attended module on the
eve of upload, and that is the owner's call, not yours. Surfacing it costs nothing; changing it costs the
attendance.

---

## 4 · Controls — what must be green before you claim this is built

Run these and quote the real output lines; ⛔ never hand-type a count.

- `python tools/parsecheck.py` — every Lua change, no exceptions.
- `python tools/desk_c90_datapatch.py` — **was 18/18.** After the guards, the demands that assert the
  bypass **must change verdict**: a declined self-check must now produce **zero writes** and must **not**
  reach `ctx.heal()`. ⚠️ **A fix invalidates its own tests** — re-base the harm legs on the pre-fix body
  and keep them; do not delete a demand because it now fails. Run the **whole** suite, not the changed legs.
- `python tools/c90_scratch_verify.py` — the eight scratch falsifiers must still discriminate.
- `python tools/bodycheck.py` — both modules keep their `-- SRC:` + `-- DEFECT:` headers (`FIX_POLICY` §2b).
- `python tools/doccheck.py` — **GREEN before any doc commit.** Counts from `--emit-counts`.
- The deskbench's other harnesses: confirm none is invalidated (`tools/desk_migration_cluster.py` was
  20 harnesses / 254 demands green on 09-12; `desk_f59_expedition.py` 23/23).

⛔ **Do not claim `tested-attended`.** The guard cannot fire in an ordinary boot — no target is missing on
a healthy 1.1.0 install, so a playtest exercises nothing. It ships **unexercised**, exactly like the Saint
heal (ck130 precedent), and the honest status is `fixed` on desk evidence. Say that plainly; do not dress
a desk control as a witness. The **VOICE RULE** binds anything player-facing: plain for players, precise
for the two Paradox developers — no "unverified" / "no guarantees" hedging.

---

## 5 · Records to update when it is built

- **`docs/agent/bugs/C90.md`** — status flip `cand` → `fixed`. ⛔ **A status flip must hit BOTH the front
  matter AND the body's heading tag**; doccheck goes RED on one without the other. Update `row_status`,
  `evidence` and `updated` too. Record the §3 reset/retry finding in the body.
- **⭐ THE MARKER OBLIGATION** — checklist items carry a status marker (`<!-- ck:158 status:closed owner:no -->`)
  and a register is generated from them. **Changing an item's status ALSO means updating its marker**, and
  nothing in `WORKFLOW.md` or `CLAUDE.md` says so yet, which is why it is said here. Permitted vocabulary:
  `open` · `ruled` · `closed` · `deferred`, with `owner:yes|no`. ⛔ Do not invent a status word.
- **After a CHECKLIST-ONLY edit run `python tools/doccheck.py --regen-waiting`, NOT `--regen`.** If you
  also touched entries — and you will have, C90.md is an entry — the full `--regen` is required. The
  distinction is about what you changed, not a preference.
- **`prompts/perma/RELEASE_OUTBOX.md`** — C90 gets **no public row**. It is our own bug, invisible to
  players, and the precedent is hardening row 3 in `Fix_StaleReservations` (v10's fourth changed module
  with no row). But the RELEASE pass must know a **fifth** module changed, so add it to the batch notes.
- **`docs/agent/STATE.md`** — ⚠️ **it is at 17,385 bytes against an 18,432-byte HARD cap that BLOCKS
  commits** (read the live number from doccheck, never this line). ~1 KB of headroom, and the release pass
  still has to write here. **Replace a line, do not add one.** ⛔ Eviction is deferred by owner ruling
  until v10 is live — do not fire `STATE_EVICTION.md`, and the byte warn is expected, not a reason to stop.
  If a write would genuinely breach the hard cap, tell the owner and let them choose; never silently trim
  something load-bearing to fit.

---

## 6 · ⛔ THE LANE FENCE — a sibling session is in this tree

`smr-bugfixpack-c2` is landing the three ruled retirements in parallel. **All sessions share ONE git
identity, so `git log --author` cannot attribute anything** — identify work by **sha + diff**.

**Do not touch, in any way:** `items.lua` · `metadata.lua` · `Code/Fix_GhostFarmOxygen.lua` ·
`Code/Fix_LayoutTechLock.lua` · `Code/Fix_AnomalyCaveInMap.lua` · `docs/agent/bugs/F37.md` · `F43.md` ·
`F118.md` · `F31.md`. Your build adds no module and removes none, so you have no business in `items.lua`
or `metadata.lua` (H-10 is the other lane's problem, not yours).

**Two files you and the other lane both write — handle them carefully:**

- **`docs/PLAYTEST_CHECKLIST.md`** — edit only your own item block. Re-read `git status` immediately
  before writing, and stage **your own hunks** (`git add -p`), never the whole file.
- **`docs/agent/bugs/INDEX.md`** — ⛔ **`--regen` rebuilds the index from every entry ON DISK, a peer's
  uncommitted ones included.** Run `git status docs/agent/bugs/` first; if you see foreign ` M` or `??`,
  coordinate before regenerating rather than sweeping their work into your commit.

⛔ **A pathspec is only HALF a commit fence.** It protects every *other* file, but for a path you *name*,
git commits that path's **working-tree** content — a peer's unstaged edits included (this happened on
09-12, `cc3edf2`). On a file two sessions are inside at once: stage your own hunks and commit **without**
a pathspec. Otherwise the house form is `git add <explicit paths>` then `git commit -F <file> -- <same
paths>`. ⛔ Never `git add -A`, never a directory pathspec, never a bare `git commit`. `-F` because
embedded quotes split under PS 5.1. Then **push** — pushing is standing-allowed.

⛔ **Never modify the game directory or `C:\Dev\SMR-SrcArchive\`** — source is read-only truth, and every
citation names its game version. ⛔ **`C:\Dev\SMR-CommunityMods` is a DIFFERENT repo with three
uncommitted files awaiting the owner** — do not commit, stash, discard or checkout there.

---

## 7 · Traps that have each cost this project a real error

1. ⛔ **Never state an absence from a truncated grep.** `| head -5` is not an enumeration. A claim that
   something is *nowhere* needs the presence side counted.
2. ⛔ **Never discard or overwrite a file you did not write without reading it first.**
3. ⚠️ **`pcall` does not catch an `assert()` in shipped code** (`EF-008`) — if your guard's error handling
   leans on `pcall`, it does not cover assert.
4. ⚠️ **A stub for a function that can REFUSE is a behaviour change** (F59 A3) — desk shims must preserve
   the refusal, or the harness measures a different program.
5. ⛔ **Trust runtime over source** (`EF-078`). Records describe **1.0.7.396349**; the installed build is
   **1.1.0.403908**. Old entries keep their version stamp — never re-point a citation.
6. ⚠️ **Check `Mars.exe` is not running** (`tasklist`) before touching loadable code, in a step separate
   from the edit.

---

## 8 · Report back

- The shas you landed, with a one-line diff summary each — **shas, not "I committed the guards"**.
- The real control output: parsecheck, `desk_c90_datapatch.py`, `c90_scratch_verify.py`, doccheck's
  `--emit-counts` block.
- **The §3 verdict on reset/retry, and what you found about C89** — established or refuted, with the
  `00_Core.lua` ordering that decides it.
- Anything you did **not** do and why, by name. ⛔ SKIPs by name, never a total.
