# Launch rehearsal — the dry run, and the gate that actually decides

♻️ **SELF-CONSUMING — ⛔ AND NOT YET CONSUMED. PARKED 2026-08-19 at stage 2.**
Delete this file only in the commit that closes **run B**, naming its grave.

> ⛔⛔ **PARK NOTE — read this before anything else.** The rehearsal ran on
> 2026-08-19 and stopped, by necessity, at **stage 2**. Stage 1 passed (20 guards,
> 0 FAIL, exit 0). Stage 2 **cannot be executed by an agent at all**:
> `DbgPackMod` is a `ModEnvBlacklist` key (`Mod.lua:1322`) and
> `ModEnvMeta.__index` returns `nil` for blacklisted keys (`:1546-1547`), so
> **no mod code — this pack, or the TestKit — can call it**; `ReloadLua` is
> blacklisted at `:1274` for the same reason. The console is the only route and
> an unattended session cannot type into it. ⇒ **the gate is downstream of one
> owner console line**, and everything from stage 3's falsifiers to stage 4's
> criteria waits behind it. The owner script is `PLAYTEST_CHECKLIST.md` item 52.
>
> ⚠️ **AND THE GATE IS TWO GAME SESSIONS, NOT ONE OWNER VISIT.** The packed
> install cannot exist until the owner packs; the Mod-Manager tick and criterion
> 7 cannot happen until the packed install exists. §4 below is rewritten
> accordingly. **Do not re-plan this as one sitting** — it was, and it is not.
>
> **What DID get done without a game** — details in `SWEEP_FINDINGS.md` (LR-F1…
> LR-F14): the file-list predictor `tools/pack_predict.py` and the archive
> reader `tools/pack_list.py`, both validated against a real engine-built
> archive; `CheckModPackSignature` answered; the packer proven byte-faithful;
> and four of the ten pass criteria repaired **before** anyone scored them.

**Owner design, 2026-08-17:** *"once its done sweeping it does a 'dry run' on our
launch procedure. It cannot publish the mod, but it can do every step up to that
point"* — and, on the two configurations: *"[A] is for our testing to ensure
compatibility. This [B] is for safety to ensure a clean launch of the bug fix
mod."*

⛔⛔ **THE RELEASE CRITERION IS B, NOT THE SUITE.** A green suite in A does not
authorise an upload. A exists to diagnose B.

---

## 0 · ⛔ Where the safe line actually is — read before planning anything

**"Every step up to publish" is NOT the safe boundary.** The step before publish
is `prepare_fn`, and **the first API call is the one that creates the listing**:

* `Steam_PrepareForUpload` calls `AsyncSteamWorkshopCreateItem()` — creates a real
  Workshop item and sets `params.publish = true` (`SteamWorkshop.lua:17-22`).
* `PDX_Upload` returns a `pdx_mod_id` and writes `pdx_id` / `PdxMod` back into
  `metadata.lua`, then `SaveWholeMod()` (`ParadoxMods.lua:167-173`).

⇒ ⛔ **Nothing that touches a portal API may run.** The click is nested inside the
step before it.

✅ **What IS dry-runnable is the whole valuable half**, because the upload's
**validation** is separable from its **transmission**: every guard in
`PDX_PrepareForUpload` is pure Lua reading `mod.*` before any network call.

## 1 · Stage 1 — preflight (no game, seconds)

```
python tools/upload_preflight.py
```

Runs all six Paradox guards, Steam's image-size limits, the version/`lua_revision`
pins, the `ignore_files` patterns, and the `code` ↔ disk ↔ `items.lua`
reconciliation. **Exit 0 required.**

⚠️ The tool reports the Paradox **login** guard as UNCHECKABLE, never as passed,
and portal character limits remain **check-at-paste**. Do not upgrade either.

## 2 · Stage 2 — packaging ⛔ **OWNER-ONLY. This is where the rehearsal stops.**

⛔⛔ **REWRITTEN 2026-08-19 — the old cell read as agent work and it is not.**
`DbgPackMod` is a `ModEnvBlacklist` key (`Mod.lua:1322`); a blacklisted key reads
`nil` through `ModEnvMeta.__index` (`:1546-1547`), so mod code cannot call it —
not from `Code/`, not from the TestKit, not from a probe. `ReloadLua` (`:1274`)
is blacklisted for the same reason, which also kills the "reload" half. **The
console is the only route** and an unattended session cannot type into it. ⇒ this
stage is an owner tick, it was never budgeted as one, and the whole gate is
behind it. Script: `PLAYTEST_CHECKLIST.md` item 52.

**Two routes exist, and only one of them has ever been exercised:**

| route | who | status |
|---|---|---|
| Mod Editor → pack, in the Ged app | owner | ⭐ **PROVEN** — this is what built the 08-17 archive (`MarsDebug.exe-20260817-19.30.31` log: `Initializing ged app: ModEditor`) |
| `DbgPackMod(Mods.SMR_CommunityFixPack, false)` at the console | owner | ⚠️ **never run.** Same function underneath (`GedModEditor.lua:744`), and it is what item 52 uses because it also gives the `ReloadLua()` the core fixes need |

⚠️ **Clean first, always:** `print(Mods.SMR_CommunityFixPack.version, Mods.SMR_CommunityFixPack:IsDirty())`
must read `1  false`. `DbgPackMod` calls `SaveWholeMod()` when dirty
(`GedModEditor.lua:745-747`) and every editor save runs `version = version + 1`
(`Mod.lua:967`) — that is H-02, and it ships 1.0.1 against the owner's 1.0.0.

⚠️ **`DbgPackMod` calls `ReloadLua()` at `GedModEditor.lua:713`, BEFORE it packs
— and a mid-game reload is exactly L2's unmeasured territory** (every caller L2
found is main-menu or Ged). **Run it from the main menu, not inside a colony.**
Item 52 orders the reads around this; do not re-order them.

**Then reconcile, and both instruments now exist:**

```
python tools/pack_predict.py .                      # what SHOULD be in it
python tools/pack_list.py "<TmpData>/ModUpload/Pack/ModContent.fpk" --tree .
```

`<TmpData>` is `%LOCALAPPDATA%\Temp\Surviving Mars Relaunched\`. `pack_list`
reconciles by **name** and then by **content**, and it extracts through
`flpk_extract.py`'s own `extract()` — ⛔ never a reimplementation; a hand-rolled
frame scan was tried first and reported 7 differences where the real extractor
reports 2.

⭐ **What is already settled about the pack, without a game** (2026-08-19,
measured against the engine-built 08-17 archive, `SWEEP_FINDINGS.md` LR-F3…F5):

* **80 files, and the predictor reproduces it 80/80 by name** — 76 `Code/*.lua` +
  `items.lua` + `metadata.lua` + `LICENSE` + `preview.png`; `docs/`, `tools/`,
  `CLAUDE.md`, `README.md`, `.git`, `.claude` all **zero**. The current tree
  predicts 80 as well. ⇒ the expected list is **pre-registered and controlled**,
  not inherited.
* ⭐ **The packer is byte-faithful.** All 80 entries extracted and compared to
  disk: **78 byte-identical, 2 differ**, and the 2 are exactly
  `git diff 7824cbc..HEAD` (`Code/00_Core.lua`, `items.lua`). No line-ending
  rewrite, no minify, no re-encode. **A whole class of packed-vs-unpacked worry
  is retired without a launch** — and the existing artifact's staleness is now
  *exact* rather than assumed.
* ⛔ **That artifact is nevertheless the WRONG one to gate on**: it predates
  `2f077e8` (19:34:59 vs 19:49) and therefore both core fixes, and it predates
  `36d8817`'s `items.lua` repair. **Stage 4 installs a REBUILD, never this file.**

⛔ **A hand-built `.fpk` was considered and REFUSED.** The format is understood
well enough to write one, and the two stale files could be patched into the
existing archive — but the artifact under test must be the one
`CreatePackageForUpload` emits, because that is literally what the upload
transmits. A gate run against an agent-built container measures the agent.

⭐ **Keep the rebuild. It is the artifact stage 4 installs.**

## 3 · Stage 3 — run A · instrumented (⚖️ information, NOT the gate)

⚖️ **STATUS 2026-08-19: A's suite half is DONE and was deliberately not re-run;
A's falsifier half is impossible without the owner and moves to item 52.**

* **Done.** `97_VERIFICATION_LAUNCH.md` pulled A forward under spec §6.5 and ran
  it three times on 08-19 (`archive/vl97a/b/c_*`), in exactly this configuration:
  `72/0/24/0` of 96 by name, `75/75` active, 0 FAIL, 0 dialog.
* **Why re-running it was refused, and the refusal is reasoned rather than
  cheap.** `Code/` and `metadata.lua` are **byte-identical** to the tree those
  legs ran; the only shipped file changed since is `items.lua`, and `items.lua`
  is **not read at game load** — `ModDef:LoadCode` iterates `self.code` from
  `metadata.lua` (`Mod.lua:498-517`) and `LoadItems` is Mod-Editor-only
  (`:590-591`, gated on `ItemsLoaded()`). ⇒ a re-run is byte-for-byte the same
  experiment, and it costs a real `EF-056` exposure for zero information.
* ⛔ **The falsifier block below is CONSOLE work and therefore owner work** — the
  same wall stage 2 hit. It is folded into item 52 so it costs no extra visit.

**Config:** TestKit **on**, opt-in **off**, mod loaded from the junction as usual.
Full restart (D13).

- `SMRTest.RunAll()` — record **by name**, ⛔ never as a total.
- The two 08-17 core-fix falsifiers:
  ```lua
  print("suspects:", #SMRFixPack.UpdateSuspects(), table.concat(SMRFixPack.UpdateSuspects(), ", "))
  DbgPackMod(Mods.SMR_CommunityFixPack, false)
  local seen, dup = {}, {} for _, id in ipairs(SMRFixPack.order) do if seen[id] then dup[#dup+1] = id end seen[id] = true end print("order:", #SMRFixPack.order, "dupes:", #dup, table.concat(dup, ", "))
  print("suspects after reload:", #SMRFixPack.UpdateSuspects(), table.concat(SMRFixPack.UpdateSuspects(), ", "))
  ```
  Expected `0` · `75` / `0` · `0`.

⚠️⚠️ **A's scope must not be overstated.** It tests this pack against **exactly one
other mod — our own.** ⛔ It may never produce a sentence like *"compatible with
other mods."* Its honest scope is "our two mods together," which is information
for the opt-in's launch, not a compatibility claim.

## 4 · Stage 4 — run B · player configuration ⛔ **THE GATE**

⭐⭐ **This has never been run in the history of this project.** Every gate
reading — `80/0/16/0`, `75/75`, `8/8`, ~60 archived launches — was taken with the
mod **unpacked through a junction** and a **third mod loaded that mutates `_G`**
(`SMRTest.SetGlobal`, the loggers, an added UI action). Nobody has confirmed the
pack behaves identically without it.

⛔⛔ **AND B HAS NO DRIVER — added 2026-08-19, and it changes who does the work.**
Every unattended primitive this rig owns (staged-copy load by filename, in-run
`SaveGame`, scripted state reads, speed control, the watchdog) runs from a
`CreateRealTimeThread` **inside the TestKit**, and Mod-Manager / main-menu driving
is **descoped by owner rule** — *"the enable click stays human"*
(`WORKFLOW.md`, capability envelope). **Run B turns the TestKit off.** ⇒ B cannot
load a save, cannot save, cannot read a variable, and cannot quit itself.

| criteria | who can take them |
|---|---|
| **1 · 2 · 3 · 4 · 6 · 10** | ✅ an agent, from a boot-and-close leg + the log |
| **5 · 7** | ⛔ **owner** — screen events, and a screen claim needs an attended witness by standing rule |
| **8 · 9** | ⛔ **owner, end to end** — a save round trip and an uninstall/reload are UI driving, not log reading |

⚠️ The old line *"everything below is readable from the log file and the screen"*
was true and smuggled a human in through the word **screen**. *"B looks; it does
not poke"* still stands — it is **who does the looking** that was never stated.

**Build the player's configuration — ⛔ THIS IS ACT 2, AND ACT 1 IS STAGE 2.**
The packed install cannot exist before the owner packs, and the tick and
criterion 7 cannot happen before the packed install exists. **Two game sessions,
with an agent step between them.** Sequence: owner packs (item 52 act 1) → agent
reconciles the archive and stages the folder → owner ticks and reads (act 2).

1. ⛔ **Pull the fix-pack junction** (`EF-055` — agent-side, real uninstall).
   Record what you pulled so you can restore it. The junction is
   `%APPDATA%\Surviving Mars Relaunched\Mods\SMR-BugFixPack` → `C:\Dev\SMR-BugFixPack`
   (⚠️ **the folder name is not the mod id** — that already makes step 3's
   id-matching leg a rename, not the status quo).

   ⛔⛔ **CORRECTED 2026-08-19 — THIS STEP HAD A HOLE THAT WOULD HAVE READ AS A
   CATASTROPHIC B FAILURE, and the verification launch found it before you ran.**
   Pulling a junction **disables that mod in account state**, and ⛔ **restoring
   the junction does NOT bring it back** — measured across two relaunches on the
   opt-in pack: the def loads, the code never runs, and the mod vanishes
   **silently** (no non-modal log line, contrary to what `EF-055` used to say;
   `account.dat` was rewritten). ⇒ **"Zero owner cost" was wrong for this step.**

   ⇒ **BUDGET AN OWNER MOD-MANAGER TICK after the swap**, and ⛔ **read the gate
   line FIRST — before you believe any other number.** A B run that reports the
   pack absent is measuring your own procedure, not the mod.

   ⭐ **And use that owner visit for the two reads nothing else can reach**, since
   the console is blacklisted unattended (`Mod.lua:1285`) and the visit is now
   unavoidable anyway:

   ```lua
   print("fix (1):", SMRFixPack.fixes.SaintBlessing.update_suspect)   -- expect nil
   DbgPackMod(Mods.SMR_CommunityFixPack, false)                        -- forces the 2nd Lua load
   local seen, dup = {}, {} for _, id in ipairs(SMRFixPack.order) do if seen[id] then dup[#dup+1] = id end seen[id] = true end print("fix (2): order", #SMRFixPack.order, "dupes", #dup)
   ```

   ⛔ **These are the ONLY outstanding verification of the two `2f077e8` core
   fixes that paused this upload.** The verification launch proved `UpdateSuspects()`
   **cannot** falsify fix ① — it reads `update_suspect` only on `error`/`inactive`
   entries (`00_Core.lua:527-536`), so a stale mark on an `active` entry is
   invisible to it. Expect `nil` and `75` / `0`.
   ⚠️ Confirm `IsDirty()` is false before `DbgPackMod` — a forced save bumps 1.0.0
   to 1.0.1.
2. Create a mod folder under `AppData/Mods/` containing **only** the stage-2
   `ModContent.fpk`. The loader takes the packed branch on
   `io.exists(pack_path) and not CheckModPackSignature(pack_path)`
   (`Mod.lua:1724-1740`): `MountPack`, `def.packed = true`, and `metadata.lua`
   read **from inside the archive**.
   ✅ **`CheckModPackSignature` ANSWERED 2026-08-19, and it closes link 7's open
   item 4 as well.** It opens with `if not AreModSignaturesRequired() then return
   false, true end` (`Mod.lua:87-89`), and `AreModSignaturesRequired` is
   `return Platform.playstation` (`:49-52`). ⇒ on PC it returns `false`
   immediately, `not false` is true, and **the packed branch IS taken**. Mod
   signatures are a PlayStation-only concern and no `.sign` file is needed.
   ⛔⛔ **AND WHY STEP 1 IS NOT OPTIONAL — added 2026-08-19 (link 7), re-derived
   at Src.** If the junction and the packed folder are BOTH present, both defs
   load and collide on `new_mods[def.id]`; the tie-break is
   `if cmp < 0 or (cmp == 0 and old.packed and not def.packed)` (`Mod.lua:1770`)
   ⇒ **at equal version the UNPACKED copy wins.** Both are 1.0.0, so leaving the
   junction in place does not produce a warning or an error — it silently hands
   run B the dev tree, which is the exact configuration B exists to stop
   trusting. Two witnesses, both free: the id appears in `multiple_sources` and
   raises `ModMessage("Mod %s loaded from %s (%s)")` (`:1800`), and criterion 1's
   mode line says `unpacked`. ⚠️ Note the packed/unpacked branches are `if`/
   `elseif` on ONE folder (`:1724`/`:1748`), so a single folder is never
   ambiguous — the hazard is strictly **two folders carrying one id.**

3. ⭐ **Run it under TWO folder names, and this is a real test, not pedantry.**
   First load computes `hpk_mounted_path = ModContentPath .. (prev_id or
   folder_name) .. "/"` — **the FOLDER NAME, not the mod id** — then caches the id
   and **unmounts if they differ**. A player's folder name is chosen by the portal
   installer and is *not* the mod id (`pdx_<id>_<version>` shape).
   ⇒ Run once as `SMR_CommunityFixPack` (id-matching) and once as a
   portal-shaped name. **`'image', "Mod/SMR_CommunityFixPack/preview.png"` was
   written against the UNPACKED path and this is the first test of it.**

   ⚖️ **RE-DERIVED 2026-08-19, and it makes this a CONFIRMATION rather than a
   discovery — which is a reason to still run it, not a reason to skip it.**
   The mount at `hpk_mounted_path` exists only to read `metadata.lua`; the def
   that survives is then mounted by `ModDef:MountContent` at
   **`self.content_path`**, and `content_path` is assigned
   `ModContentPath .. def.id .. "/"` (`Mod.lua:1757`) — the **id**, never the
   folder name. All three cases land on `Mod/SMR_CommunityFixPack/`:
   *(a)* folder name = id → `hpk_mounted_path` already equals it;
   *(b)* portal-shaped name, first launch → `prev_id` is nil, so the def is
   **unmounted** and the id cached (`:1738-1743`), leaving `def.mounted` false so
   `MountContent` mounts at `content_path` (`:853-862`);
   *(c)* portal-shaped name, later launches → `prev_id` is the **cached id**, so
   `hpk_mounted_path` is built from the id and equals `content_path` again.
   ⇒ the `image` path resolves on the packed path in every case **on source**.
   ⛔ What is still unmeasured is whether it *renders* — criterion 7.
4. Disable **TestKit** and **opt-in** in the Mod Manager. Full restart (D13).

**⛔ B has no console and you may not add one** — dropping an instrument into
`Code/` contaminates the exact tree under test. **B looks; it does not poke.**
Everything below is readable from the log file and the screen.

### B's pass criteria — all of them, by name

| # | criterion | how it is read |
|---|---|---|
| 1 | the mod loads **packed** | ⛔⛔ **CORRECTED 2026-08-19 (link 7) — this cell's evidence did not test this cell's claim, and it is the one criterion that decides whether the other nine mean anything.** It read *"`[CommunityFixPack]` lines exist at all"*, which is equally true of the **unpacked** tree — so a B run whose junction pull was incomplete would have measured the dev tree and scored this GREEN. ⇒ **Read the engine's own mode line instead:** `ModPrint("once", "Loaded mod def %s (id %s, v%s) %s from %s", …, mod.packed and "packed" or "unpacked", …)` (`Mod.lua:1849`), which prints the `def.packed` flag set at `:1734`. ⭐ **MEASURED over `docs/archive/*.log`: 66 archived sessions carry this line for `id SMR_CommunityFixPack` and ⛔ ALL 66 say `unpacked from appdata`; `packed` has never once appeared.** That is the seed note's "never loaded packed" upgraded from an assertion to a named witness. ⇒ **B passes criterion 1 only on `… (id SMR_CommunityFixPack, v1.00-000) packed from …`.** `[CommunityFixPack]` lines existing is criterion 2's evidence, not this one's. | log: `grep "Loaded mod def" <log>` — the word must be `packed` |
| 2 | **every module applies** — ⛔ *sharpened 2026-08-19: this said "registers", which is a weaker and different event. A module can register and then latch `inactive`; registration proves nothing about the fix working.* | **75 `applied` witness lines BY NAME**, ⛔ never a total. ⚠️ **Do not phrase this as "equals run A's set"** — that made the gate depend on a run that may not have happened, and a gate must not have a dangling referent. ⛔⛔ **AND THE DERIVATION UNDER THE 75 WAS WRONG TWICE, CORRECTED 2026-08-19: it said "the 75 ids in `metadata.lua`'s `code` list minus `00_Core`/`90_SaveSanitizer`", but the `code` list holds SEVENTY-SIX entries, and `90_SaveSanitizer` DOES emit an `applied` line** (`vl97a:152`, `SaveSanitizer: applied`). That recipe yields **74** and would have sent a runner hunting a phantom module. **The number 75 is right; it is `76 − 00_Core`, and `00_Core` alone.** MEASURED: exactly 75 `applied` lines in each 08-19 leg. ⭐ **One known-benign exception, pre-registered so it is not mistaken for a failure:** `SaintBlessing` runs `applied` → `inactive (no dome-colonists trait presets)` → `corrected N of M` on **every** launch (62/59/58 across the archive). That cycle is expected; its *absence* would be the anomaly |
| 3 | ⚖️ **no NEW / UNATTRIBUTED `[LUA ERROR]`** — ⛔ *corrected 2026-08-19 (link 5): this cell said `0 [LUA ERROR]`, and criterion 3's own "any of 1–7 failing blocks the upload" would have used a vanilla line to block a clean release.* ⚠️⚠️ **BUT LINK 5'S EVIDENCE SENTENCE WAS ITSELF WRONG AND IS CORRECTED HERE (2026-08-19, owner review).** It read *"no build of this game can ever satisfy [zero] on this rig"* and *"every one of the 73 archived logs … carry them."* ⛔ **Re-measured over `docs/archive/*.log`: 21 of 73 carry at least one; 52 carry NONE.** So zero is not only satisfiable, it is the **common** case, and ⛔ **a B run that produces zero is normal and must not be read as suspicious.** The errors are session/map dependent, not universal — `Lua/Flight.lua:465` `objects_to_mark` + `:479` `objects_to_unmark`, vanilla synthetic-map noise documented since 2026-08-03. ⭐ *The rule link 5 wrote is right and stands; only its justification was inherited rather than measured — the exact failure it had just caught the interlude committing.* ⛔ **And the count is NOT the constant the interlude's R5 called "reproduced": the same configuration on the same build produced 48 / 59 / 48 across legs A / B / C, because the line fires per marked object and scales with session activity.** ⇒ **Compare the SHAPE, never the count**: the expected shape is two sites, both `Flight.lua`, and any line whose message or stack contains **our content path** is the real failure — that one is `EF-065`'s route and it also puts a message box on the player's screen. ⛔ **BUT "any third site is the real failure" IS OVERSTATED, and the archive refutes it (corrected 2026-08-19, re-measured this session).** Across the 73 logs the sites are `Flight.lua objects_to_mark` **418** + `objects_to_unmark` **7**, *plus four non-`Flight` sites that are already there and already attributed*: `TrackElement.lua … 'TestMeteor'` (3), `GedGameObjectEditor.lua … 'GetSpotNameColor'` (2), `GridObject.lua … 'GetShapePoints'` (1), `upvalue 'old_threads'` (1). ⇒ **a third site is an ATTRIBUTION JOB, not an automatic gate failure** — attribute it before judging it, exactly as criterion 5 requires for the screen, and ⛔ never silently discount one. *(Re-measured and confirming the owner's 08-19 numbers: **21 of 73** carry ≥1, **52 carry none**.)* | log; `grep -c "LUA ERROR"` then read every distinct message |
| 4 | ⛔ **no `update report:` line** — ⚠️ *corroborating, NOT decisive (2026-08-19)* | `00_Core.lua:540` logs **before** it shows the dialog, so an absent line is consistent with zero suspects. ⛔ **But absence has TWO causes and this cell could not tell them apart** — the report thread waits for the pregame main menu on a 5-minute deadline and samples **once** (`:498-505`), and it logs **only** when suspects > 0, so there is no positive witness that it ever ran. That is the same unfalsifiable shape link 7 found in criterion 1. ⇒ **The decisive read is `#SMRFixPack.UpdateSuspects()` on the attended tick** (step 1), which is already mandatory; this line corroborates it |
| 5 | ⛔ **nothing OF OURS on screen** | ⛔⛔ *corrected 2026-08-19 — this cell would have FAILED THE GATE ON A VANILLA POPUP.* `ShowStartGamePopup` (*"Welcome to Mars, Commander!"*, `PreGameMission.lua:820`) fires **unconditionally**, and the TestKit has been **neutering it** for every unattended leg this project has ever run (`95_AutoRun.lua:264-267`, L7-F5). ⛔ **Run B turns the TestKit off, so that popup comes back** — it is vanilla, it is expected, and it is NOT a failure. ⇒ The test is **nothing attributable to the pack**: no stand-down dialog, no pack notification. ⚠️ Anything else on screen gets **attributed before it is judged**, never counted. ⭐ **AND HALF OF THIS CELL IS LOG-DECIDABLE, which was never said (2026-08-19):** the pack's one designed screen surface logs at `00_Core.lua:540` **before** it draws — the same fact criterion 4 leans on — and L4's census measured that the pack raises **no** notification, popup, banner or voice line of its own. ⇒ absence of that line is a positive log-side negative for everything the pack can author; the attended half is only *"was there anything else on screen"*. ⛔ **Owner criterion** — a screen claim needs an attended witness by standing rule |
| 6 | version reads **`v1.00-000`** on the mode line | ⭐ *changed 2026-08-19 to a log read.* The **same mode line criterion 1 uses** already carries it — `ModPrint("Loaded mod def %s (id %s, v%s) %s from %s", …)` prints `GetVersionString()` (`Mod.lua:1849`). ⛔ The old cell said *"Mod Manager"*, which needs a human looking at a screen and cannot be read from an unattended log at all. ⛔⛔ **AND THE CELL THEN ASKED FOR A TOKEN ITS OWN EVIDENCE NEVER PRINTS, corrected 2026-08-19:** it said *"renders 1.0.0"*, but `ModDef:GetVersionString` is `string.format("%d.%02d-%03d", version_major, version_minor, version)` (`Mod.lua:1176-1178`) ⇒ the log says **`v1.00-000`** and the string `1.0.0` appears nowhere on that line. A runner told to confirm "1.0.0" there finds nothing and cannot tell a pass from a typo. **PASS = the literal token `v1.00-000`**, which is `1.0.0` under that format; the player-facing `1.0.0` is `PackVersion`, a different surface |
| 7 | ⭐ **the preview image renders** in the mod list | ⛔ **ATTENDED-ONLY, and that is now stated rather than assumed (2026-08-19).** "Renders" is not log-observable, so this cell was unfalsifiable in an unattended run. ⇒ **Fold it into the owner Mod-Manager tick step 1 already makes mandatory** — the visit is unavoidable, so this costs nothing extra. It is the first real test of `'image', "Mod/SMR_CommunityFixPack/preview.png"` on the PACKED path, a value hand-written against the UNPACKED one |
| 8 | save round trip | ⚠️ *pass condition made concrete 2026-08-19 — "no residue surprise" was not a test.* Load a named save · let time pass · save under a NEW name · reload it. **PASS =** the reload succeeds, `0` new `[LUA ERROR]` on the load, and the pack's own witness lines reappear by name. ⛔ **Use a NAMED save, never an autosave** (`EF-056`: a copy of an autosave is an autosave to the rotation), and pre-copy first |
| 9 | uninstall holds for all 75 at once | ⚠️ *scope corrected 2026-08-19: this is a STAGE, not a drive-by cell.* Removing the mod **changes account state and does not undo itself** (the step-1 finding), so this costs **a second owner tick** to restore — budget it or defer it deliberately, but ⛔ do not let a runner discover it mid-gate. Otherwise as written: remove · load the save · `RELEASE_UNINSTALL_ASSEMBLY.md` still true |
| 10 | save directory reconciles **by name** | `EF-056`, after **every** launch |

⛔ **Any of 1–7 failing blocks the upload.** 8–10 failing blocks it and is worse.

⚠️ **One clarification the demotions made necessary (2026-08-19).** Criterion 4 is
*corroborating, not decisive* — and that reads as a contradiction with the line
above until you separate the directions: **a PRESENT `update report:` line is
decisive and blocks**; an **absent** one proves nothing on its own and is
discharged by `#SMRFixPack.UpdateSuspects()` on the attended tick. Same for
criterion 3: a line whose stack carries our content path blocks; a third vanilla
site is attributed first. ⛔ **No criterion may block on an ABSENCE it has no
positive witness for** — that is the unfalsifiable shape links 5 and 7 both
caught, and it is why four of these ten needed repairing before anyone scored
them.

## 5 · Stage 5 — restore, and report

⚖️ **STATUS 2026-08-19: nothing to restore, and that is a deliberate result.** No
junction was pulled, no packed folder staged, no mod enabled or disabled, no
launch taken and therefore **no `EF-056` exposure incurred** — the rig is exactly
as this session found it (fix pack + TestKit + opt-in junctions all in place;
the opt-in still owed its tick from checklist 43, which is not this session's).
The 81 saves are untouched, byte for byte. ⛔ **The one thing that changed on
disk outside the repo is nothing** — the 08-17 `.fpk` in `TmpData` was read, and
extracted to a scratch directory that no longer exists.

- **Restore the junction** and re-enable TestKit / opt-in to the rig's usual
  shape, or the next session inherits a configuration nobody documented.
- Delete the staged packed install.
- Reconcile the save directory **by name** one final time.

**Report, in this order:** does B pass · what A said and how it differed from B ·
⭐ **any behaviour that differs between packed and unpacked** (that difference is
the single most valuable thing this rehearsal can produce, and nothing else in
the project would have surfaced it) · what you could not run and why.

⚠️ ⛔ **"The rehearsal passed" is not "the upload will succeed."** You did not log
in, did not transmit, and did not create a listing. Say the narrower true thing.
