# Pre-release audit — the mod as ONE ORGANISM, and a hostile re-read of today's core fixes

**Owner ask, 2026-08-17 (at the upload sitting, minutes before the first
upload):** *"create a fable audit prompt to not only check your work here, but
also to do a top level pre release sweep of the mod. We did one for the
documentation, I should have thought to do one for the mod. Something that does
a peak at the mod as one organism instead of looking at individual pieces which
we have pretty much only done."*

♻️ **SELF-CONSUMING.** You finish by fixing what you find (or routing what is not
yours), committing, and **deleting this file in the same commit**, with the
close-out naming its grave
(`git show <sha>:docs/agent/prompts/PRERELEASE_MOD_AUDIT_fable.md`). The file's
absence is the done-condition.

⛔⛔ **THE UPLOAD IS ONE OWNER ACTION AWAY AND IT IS PAUSED FOR YOU.** The package
was already built and verified at 80 files; the owner then overruled a
ship-now-fix-later recommendation with *"I don't want to launch with an immediate
planned 1.0.1 fix routed for launch. I want us to be clean period."* Two core
defects were fixed on that word. **Nothing has been published, so there is no
1.0.1 — `metadata.lua` is untouched and 1.0.0 is simply what 1.0.0 now is.**
Whatever you find either gets fixed now or is the reason the owner does not
upload tonight.

⚖️ **The owner's framing is the whole point of this brief.** Every audit this
project has run looked at *pieces* — one entry, one module, one chain, one
document set. **Nobody has ever looked at the mod as a single running thing.**
The two defects fixed today were both organism-level: invisible in any one
module, obvious the moment you asked what happens when all 75 run together and
the game reloads Lua underneath them. Assume that is not a coincidence, and that
the same class of defect is still in there.

---

## 0 · Staleness check and read path, before anything else

```
git log --oneline -8
git pull
python tools/doccheck.py --emit-counts
```

**Check against `2f077e8`** (*"The pack refuses to launch with a known false
alarm in it…"*) — the core-fix commit this brief audits. If HEAD is behind it,
stop and report. The release tag `fixpack-v1.0.0` sits at **`7824cbc`**, one
commit BEHIND HEAD **on purpose**: it is not moved onto unverified code. Moving
it is part of your close-out if you clear the fixes.

**Read path — file granularity, in this order:**

| file | why |
|---|---|
| `docs/agent/STATE.md` | mandatory every session |
| `Code/00_Core.lua` | the organism's nervous system, and where today's fixes landed |
| `docs/agent/FIX_POLICY.md` §1 (techniques), §2 (fail safe), §3+§3a (save discipline), §6 (engine semantics), §8 (release hygiene) | the rules every module claims to obey |
| `docs/agent/WORKFLOW.md` §"Probe hygiene", §"Testing checklist per fix", §"Log review", §"BOTH MODS LOADED", §"Release steps", §"Release marking" | the gates |
| `docs/agent/reports/RELEASE_PORTAL_PREP.md` §0.5 | today's upload mechanics — you re-derive these |
| `docs/agent/facts/INDEX.md` → at minimum `EF-054`, `EF-056`, `EF-058`, `EF-059`, `EF-064` | the traps that have bitten this project repeatedly |
| `docs/agent/bugs/INDEX.md` | the registry side of the registry↔package↔promise reconciliation |
| `metadata.lua`, `items.lua` | what actually ships |

⛔ **`docs/archive/MOD_DESCRIPTION.md` IS FROZEN** — ≥6 known-false claims kept on
purpose. Do not touch it, do not cite it.

## 1 · 🗒 Live todo list, from your first action

**One item per commit-and-verify unit** (WORKFLOW §"Authoring a prompt" element
1). Part One's two fixes are separate items; every Part Two pass is its own item;
each launch is its own item. **Expand the list the moment a pass turns out to be
four things.** Mark complete as they complete, never in a batch. Exactly one in
progress. The owner reads this list to decide when to step in — a stale list is a
wrong answer to that question.

## 2 · ⛔ Probe hygiene gate — before ANY test result is recorded

```
grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/
```

CLEAN = zero hits, or every hit declared in this brief and in your todo list.
**This brief declares none.** Anything else: repair and commit first, or stop and
report. No result recorded before this runs.

---

# PART ONE — audit today's two core fixes, hostilely

Both landed in `Code/00_Core.lua` in `2f077e8`. **Re-derive the ROUTE, not just
the citations** (`EF-057` / the standing lesson: this project has been wrong in
both directions in one week with every cited line correct both times). Read the
commit message last, so it cannot lead you.

### 1.1 The `update_suspect` leak

**Claimed:** `SMRFixPack.Require` marks `update_suspect` on a target-shape
failure; several modules fail a pass and then succeed (first pass runs before the
class hierarchy is flattened); nothing cleared the mark on success; it then got
read by `UpdateSuspects` on any later `inactive`, **including a
`latch(..., "benign")`**. The fix clears the mark at **both** sites that restore
`active` — `ctx.heal()` and `run_apply`'s success branch.

**⛔ The adversarial question that matters most: does clearing the mark now HIDE
GENUINE PATCH ROT?** Construct the case. A module that succeeds and *later*
genuinely rots — does anything still catch it? If a target is replaced by a game
update between the successful apply and a later re-fire, which path notices, and
does the report still fire? **If the answer is "nothing notices", this fix traded
a false positive for a false negative and that is worse.** Say so plainly.

Then:
- **Is there a THIRD site?** Re-derive every assignment of `status` and of
  `update_suspect` yourself. Do not inherit the two-site claim.
- **Is `nil` the right clear value** rather than `false`, given every reader?
- Does `UpdateSuspects`' substring fallback (`"game update changed"`,
  `"could not install"`, `"could not replace"`, `"did not land"`) still behave
  when `detail` is cleared to `""`?

### 1.2 The `order` double-append

**Claimed:** `SMRFixPack` survives a Lua reload by design (`rawget(_G, …) or {…}`);
`Register` appended unconditionally; `ReloadLua` therefore pushed a second copy
of every id while `fixes[id]` was replaced in place; everything walking `order`
double-counted. Guarded now on whether `fixes[id]` existed **before** the
overwrite.

**⛔ The planted criticism — test it, do not take it on trust.** Before the fix,
two *different* modules registering the **same id** produced two `order` entries
and one silently-overwritten entry table. After the fix it produces **one** entry
and the same silent overwrite — so **the guard may have made a genuine id
collision quieter than it was.** Decide whether re-registration with a
*different* `def` should log. If it should, that is a real finding against
today's work and you should fix it.

Also: can `fixes[id]` ever be set by a path *other* than `Register`, which would
make the guard read the wrong signal? Re-derive.

### 1.3 The rest of today's work, re-derived

| claim | how to falsify |
|---|---|
| `'image', "Mod/SMR_CommunityFixPack/preview.png"` resolves | ⭐ **the unpacked case is NOT the shipping case.** A player gets a PACKED mod mounted by `MountPack` (`Mod.lua:859`). Confirm the path resolves for a packed mod, not just the junctioned dev tree |
| Paradox before Steam | re-derive at Src: `ParadoxMods.lua` saves AFTER upload, `SteamWorkshop.lua` saves BEFORE packing |
| every editor save bumps `version` | `ModDef:SaveDef` — confirm, and confirm `serialize_only` is not in play on the upload path |
| the package is 80 files | re-list the real `.fpk` (`tools/flpk_extract.py`), do not inherit |
| 1.0.0 is what a player sees | `PackVersion`; and note what Paradox is *sent* as `VersionDisplayName` |
| the update report "has never fired in ~60 archived launches" | re-count `docs/archive/*.log` yourself |

---

# PART TWO — the organism sweep

**This is the half nobody has done.** Each pass below asks a question that is
*structurally invisible* to a per-module review. Where a pass cannot be answered
from source, say it is unmeasured — ⛔ **do not convert "no evidence of a problem"
into "no problem."**

### Pass A — ⭐ the collision map (do our own modules fight each other?)

Build, mechanically, the full map: **every symbol the pack patches → which
module(s) patch it.** Class methods, globals, table slots, preset fields, own
threads (the five exposure shapes, `WORKFLOW` §"fpk verification").

- **Any symbol with more than one patcher is a finding.** Per-module review
  cannot see this, because each module only knows its own target.
- Where two modules do share a target: does order change behaviour? Is either
  one's wrapper defeated by the other's?
- ⛔ This has never been produced. Produce it as an artifact, not a sentence.

### Pass B — ⭐ idempotency under reload (the direct descendant of today's bug)

`ReloadLua` re-runs every module's `apply`. Today's fix stopped `order` growing —
**it did NOT change the fact that apply runs again.**

- ⛔⛔ **Does any module wrap its own wrapper on a second apply?** A double wrapper
  doubles an effect. `C39` deliberately measured *"our delta 0 at every read (no
  double-pay)"* on a single load — **the two-apply case is a different question
  and appears not to have been asked.**
- `DataPatch` sites have a `ctx.patched` guard. **Plain `§1.4` wrappers may not.**
  Sweep all of them.
- The reachability question is real and must be answered rather than assumed: a
  player disabling a mod needs a full restart (D13), but **what else calls
  `ReloadLua` on a retail install?** Answer at Src, name the callers.

### Pass C — the core as a single point of failure

Every module routes through `00_Core`. Ask what a per-module review never does:
- If one module's `apply` throws, are the other 74 unaffected? (`run_apply`
  pcalls — verify, and check the *runtime* paths, not just apply.)
- If an installed **wrapper** throws mid-game, what does the player experience?
  `FIX_POLICY` §2 says fail safe, never loud — is that true in aggregate?
- Does an `OnMsg` handler throwing get swallowed (`procall`, `cthreads.lua:20` —
  the named F87 failure mode: reporting `active` while having done nothing)?

### Pass D — aggregate save footprint

The card tells players the pack *"writes almost nothing into your savegame."*
Every module was verified individually. **Nobody has summed it.**
- What is the total across all 75 — measured, not reasoned?
- `90_SaveSanitizer` is the organism-level actor here; does its coverage match
  the current module set, or the module set of whenever it was written?
- `FIX_POLICY` §3a is a HARD RULE. Does the pack obey it *in aggregate*?

### Pass E — aggregate runtime cost

75 wrappers, several on per-tick or per-entity paths.
- Identify which modules sit on hot paths. Name them.
- Has aggregate cost **ever** been measured? If not, **say that** — do not assert
  it is fine because each one is small.

### Pass F — global namespace footprint

- Enumerate every global the pack creates or writes. Expected:
  `SMRFixPack`, `SMRFixPack_Disabled`, `SMRFixPack_Optional`.
- ⛔ **Any module leaking an accidental global is a collision risk with other
  mods** — and other mods exist on the same rig by ruling. `EF-064` is relevant
  (`ProtectedPropertyObject` protects nothing in retail).

### Pass G — registry ↔ package ↔ promise reconciliation

Five surfaces must agree, and they have drifted before:
`bugs/INDEX.md` entries · `metadata.lua` `code` list · `items.lua` · the shipped
`.fpk` · the player-facing fix list and card.
- Any module shipping with no entry? Any entry promising a fix not in the
  package? (The `F24`/`F28` class — bullets promising DELETED fixes — has
  happened here.)
- Does 76 files = 75 modules + core actually reconcile, including
  `90_SaveSanitizer`?

### Pass H — the veto mechanism, as a whole

The README was rewritten **today** to advertise the veto-mod route (replacing a
false console-disable claim).
- ⛔ **"You can X" needs a route check.** Verify a real player can walk it — a
  citation proving the mechanism exists is a *different* check, and the owner has
  overturned a line three reviews passed on exactly this.
- Does `SMRFixPack_Disabled` actually stop **all 75**, including modules that
  patch at load without going through `WhenActive`?

### Pass I — first-run experience, as one event

**What does a player actually SEE on a first launch?** Dialogs, notifications,
log lines, anything.
- The answer should be **nothing**. Today's defect was exactly this class, caught
  only because a box appeared on screen during an upload sitting.
- Check the log noise a player could stumble into, not just what is correct.

### Pass J — known traps, applied across all 75

Cross-cutting sweeps of traps that have already bitten this project:
- ⛔ **Flattened-class trap** (`EF-058`) — bit this project **four** times,
  including once mid-chain. `rawget(b,'class')` and method-wrapping on built
  classes. Sweep every module.
- **Reserve semantics / `desired_amount`** (`EF-059`) — anything relying on it.
- ⚠️ **`EF-054`** — wrapper ordering and mod-id keying.
- **Dead-coded targets** — the F85 lesson: a fix whose target is unreachable on
  retail (`local cond = false`). **Is F85 the only one?** Nobody has swept for a
  second instance, and *player-route ≠ source citation* has now been the finding
  three times.

### Pass K — uninstall, as one event

Removal takes all 75 out at once. The uninstall story was **assembled from
pieces** (`RELEASE_UNINSTALL_ASSEMBLY.md`). Does it hold in aggregate — latched
heals, rains migration, layer-2 residue, the save-mod-ref line?

---

## 3 · Verification — what you may run, and how

⭐ **You may run unattended launches; owner cost is zero and that is the point.**
The junction makes the checked-out tree the running mod.

⛔⛔ **`EF-056` IS LIVE AND HAS ALREADY EATEN FILES.** Byte-copy every
autosave-tagged save **before every launch**, keep the copies **outside** the
save directory (a copy of an autosave *is* an autosave to the rotation), and
**reconcile by name after every launch, not just the one you expect to fire.**
A pre-copy from 2026-08-17 exists for `Autosave Sol 406` / `Sol 411`; take your
own, do not rely on it. ⚠️ The ④ sheet's held list previously named a save that
no longer exists — verify what is on disk, do not inherit a list.

**The two fixes need a falsifier each, not a green suite:**

```lua
print("suspects:", #SMRFixPack.UpdateSuspects(), table.concat(SMRFixPack.UpdateSuspects(), ", "))
DbgPackMod(Mods.SMR_CommunityFixPack, false)   -- forces the ReloadLua that caused the bug
local seen, dup = {}, {} for _, id in ipairs(SMRFixPack.order) do if seen[id] then dup[#dup+1] = id end seen[id] = true end print("order:", #SMRFixPack.order, "dupes:", #dup, table.concat(dup, ", "))
print("suspects after reload:", #SMRFixPack.UpdateSuspects(), table.concat(SMRFixPack.UpdateSuspects(), ", "))
```

Expected: `0` · `75` / `0` · `0`. **Pre-register your predictions in a pushed
commit before the launch** (house practice — `3f1856f` / `94eb508` / `d762964`
are the precedents, and the audit that closed them proved the commits preceded
the launches in git).

⚠️ **The suite baseline is configuration-dependent.** `80/0/16/0 of 96` and gates
`75/75` + `8/8` were measured with **BOTH mods loaded** (the rig's normal config,
owner ruling 2026-08-12). The **shipping** configuration is the fix pack ALONE.
⇒ Run both if you can; **compare SKIPs BY NAME, never as a total** — a moved
total is not a regression, a missing PASS name is.

⭐ **Leave the owner a short attended checklist** for their own opt-in-disabled
pass (they asked for it explicitly: *"I will also turn off the opt in mod to see
if we see any references that shouldn't be there"*). Keep it to a handful of
lines they can walk without reading this brief.

## 4 · Scope fence

**IN:** `Code/` of this repo · `metadata.lua` / `items.lua` · the audit artifacts
(the collision map above all) · fixing real defects you find and can verify ·
re-verifying today's two fixes · routing anything owner-shaped.

**OUT:**
- ⛔ **Any change that alters what the mod PROMISES** rather than whether it keeps
  the promise. That is an owner decision — route it, do not make it.
- ⛔ **A version bump.** 1.0.0 is ruled. Nothing has shipped. If you believe a
  bump is needed, that is a stop condition, not an edit.
- ⛔ **Publishing anything**, to any portal or to the web. Pages is OFF and stays
  off. No agent uploads.
- ⛔ **The opt-in and rescue repos' code** — both defects mirror there and the
  mirror is an **open owner decision** on the checklist. Note it; do not do it
  unless the owner has ruled by the time you run.
- ⛔ `docs/archive/` (append-only) · `archive/MOD_DESCRIPTION.md` (frozen) · the
  queued `smrcf-*` / `jumbo-cave` chains.
- ⛔ New fixes for newly-found *game* defects — **file the entry, do not build.**
  Item 34 (build the four coverage-sweep findings now or after launch) is already
  waiting on the owner with a recommendation of AFTER.

## 5 · Stop conditions — permission, not failure

- **Today's fixes do not survive your re-read** → stop, report, do not paper over
  it. The owner paused an upload for them.
- **A pass finds a defect that cannot be fixed without changing what the mod
  does** → route to the checklist. Not yours.
- **You cannot answer an organism question from source** → say "unmeasured" and
  move on. ⛔ Never upgrade silence to safety.
- **doccheck goes red** → fix before committing; red blocks.
- **A launch produces `[LUA ERROR]`** → stop, report, do not keep launching.
- **The save directory does not reconcile after a launch** → stop and restore
  from your pre-copy before anything else.

## 6 · ⛔ What may NOT be claimed

- ⛔ **"The mod is clean"** / **"ready to ship"** on the strength of a read-through.
  Name what you checked, how, and **what you did not reach.** The owner is buying
  the last sentence; it must be honest enough to be worth buying.
- ⛔ **Any count you did not emit or measure.** `--emit-counts` or a measured log.
  Inheriting numbers is how "95 checks" survived two corrections.
- ⛔ **"No collisions"** without the Pass A map as an artifact.
- ⛔ **"Idempotent under reload"** without having actually reloaded.
- ⛔ **"Save-safe in aggregate"** without an aggregate measurement — per-module
  verifications do not sum themselves.
- ⛔ **A player-route claim** without walking the route on each platform.
- ⛔ **`tested`** — the bare word is CLOSED to new work. Use
  **`tested-unattended`** (real launches, nobody watching; ⛔ never for a screen
  event) or **`tested-attended`**. 46 legacy entries hold the bare word and only
  29 cite a sitting; ⛔ it must not be read as "attended".
- ⛔ **"Not caused by our leg"** as a dismissal. That is an attribution verdict.
  Report every unexplained log line with its age — every pushback on this rule so
  far has found a real vanilla defect.
- ⛔ Blanket verification over a table — **provenance per row**, and the ROUTE
  sentence tagged separately from its citations (`WORKFLOW` R3).

## 7 · Close-out — how this file disappears

One commit:
- fixes applied and each one **verified by its own falsifier**, not by a green suite;
- the **Pass A collision map** committed as a real artifact under
  `docs/agent/reports/`;
- findings that are game defects filed as entries; findings that are owner calls
  on `docs/PLAYTEST_CHECKLIST.md` → *"Decisions waiting on you"* (**an ask
  recorded only in an agent doc is not asked**);
- `RELEASE_PORTAL_PREP.md` updated if anything you measured moves it (packaging
  count, upload mechanics, the held-saves list);
- `STATE.md` **extended, not grown** — 60-line cap, evict resolved material to
  `archive/SESSION_LOG.md`, never an obligation;
- load-bearing logs archived (`R8`);
- ⭐ **move `fixpack-v1.0.0` to the verified tree** (local **and** remote,
  `--force`) if and only if you clear it — the tag must mark what actually gets
  packed, and it is deliberately sitting behind HEAD right now;
- `python tools/doccheck.py` GREEN;
- `git rm` this file; commit naming the grave; push.

**End with a plain-language owner report:** what was wrong, what you fixed, what
you left and why, what you could not measure — and, in **one sentence**, whether
this mod should be uploaded tonight. ⚠️ *"I found nothing"* is a legitimate
answer only if you can say what you looked at; **an organism sweep that finds
nothing on its first ever run is itself a finding worth doubting**, and you
should say which passes were shallow.
