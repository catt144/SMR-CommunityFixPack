# Lens notes — the detailed questions, one block per lens

⛔ **RE-RUNNABLE reference, not a job.** `01_LINK.md` is the job. This file exists
so a link taking lens `Lx` inherits the specific questions rather than
re-inventing them.

⛔ **These are a FLOOR, not a ceiling.** Every under-count in this project's
history happened because *the brief never asked*. If your lens suggests a question
that is not written here, **that question is the valuable one** — ask it, and add
it to this file at close-out so the next link inherits it.

⚠️ Where a question cannot be answered from source: ⛔ **never convert "no
evidence of a problem" into "no problem."** It goes in the ledger's *NOT reached*
column.

---

## L1 · Structure & collision

⭐ **Build the map, mechanically: every symbol the pack patches → which module(s)
patch it.** Cover all five exposure shapes (`WORKFLOW` §"fpk verification"):
class method · table slot · global assignment · preset field · own thread.

- **Any symbol with more than one patcher is a finding.** Per-module review
  cannot see this — each module only knows its own target.
- Where two modules share a target: does order change behaviour? Is one's wrapper
  defeated by the other's?
- ⛔ **This map has never been produced.** Commit it as an artifact under
  `docs/agent/reports/`, not as a sentence in a report.

> ⭐ **Added by link 1 (2026-08-17), and it is the whole reason the map found
> anything: RESOLVE THE FILE-LOCAL ALIAS FIRST.** Modules capture targets as
> locals (`local C = rawget(_G,"Colonist")`) and then write `function C:Idle`. A
> plain grep reports `C:Idle`, which cannot be joined across files — so a naive
> sweep sees **zero** same-symbol collisions and reports the pack clean. The
> first pass of link 1's own script did exactly that. Build the alias map per
> file, then resolve every patch site through it.
>
> ⭐ **And ask the inheritance question, not just the same-symbol question.** The
> map's most valuable output was not the one double-wrap; it was **C1** — for
> every `Parent:Method` we patch, which subclasses in Src declare their own
> `Method` and therefore never see our repair. Two real coverage gaps came from
> that check and from nothing else. Each C1 hit is decided by one thing: **read
> the subclass override and see whether it calls the parent.** 5 of 8 did, and
> were clean. ⛔ Do not stop at the shadow list — it over-reports badly.
>
> ⚠️ **Link 1 left the preset-field half NON-mechanical** (enumerated by reading
> 13 modules). A later link that wants depth there should extract it properly.

## L2 · Lifecycle & idempotency

`ReloadLua` re-runs every module's `apply`. The 2026-08-17 fix stopped `order`
growing; ⛔ **it did not change the fact that apply runs again.**

- ⛔⛔ **Does any module wrap its own wrapper on a second apply?** A double wrapper
  doubles an effect. `C39` measured *"our delta 0 at every read (no double-pay)"*
  on a **single** load — the two-apply case is a different question and appears
  never to have been asked.
- `DataPatch` sites carry a `ctx.patched` guard. **Plain §1.4 wrappers may not.**
  Sweep every one.
- **Answer the reachability question at Src rather than assuming it:** a player
  disabling a mod needs a full restart (D13), so **what else calls `ReloadLua` on
  a retail install?** Name the callers.
- Ordering: `ClassesBuilt` / `DataLoaded` / `ModsReloaded` / `DataChanged`
  (`SMRFixPack.OnDataReady`) — is every module's assumption about which fires
  first actually true?

## L3 · Save & exit

The card tells players the pack *"writes almost nothing into your savegame."*
Every module was verified alone. ⛔ **Nobody has summed them.**

- What is the **total** footprint across all 75 — measured, not reasoned?
- Does `90_SaveSanitizer`'s coverage match the **current** module set, or the set
  it was written against?
- `FIX_POLICY` §3a is a HARD RULE (owner, 2026-07-31). Does the pack obey it **in
  aggregate**?
- Uninstall takes all 75 out at once, and the story was **assembled from pieces**
  (`RELEASE_UNINSTALL_ASSEMBLY.md`): latched heals, rains migration, layer-2
  residue, the engine's savegame-mod-ref line. Does it hold together?

> ⭐⭐ **Added by link 3 (2026-08-18) — ASK WHAT THE CENSUS WAS KEYED ON. This
> generalises past L3 and is the question that produced this link's only
> non-cosmetic finding.** The authoritative exposed-set derivation swept
> persisted state using the `SMRFixPack_*` token as its grep key, because
> `FIX_POLICY` §3 says that is how we name what we persist. ⇒ **the naming rule
> is not a style preference, it is the key the census runs on**, and the single
> site that breaks the rule is structurally invisible to the census meant to
> enumerate it. The pack had exactly one, and the record actively *cleared* the
> global it lives in. **Whenever you inherit a count, find the KEY it was
> gathered with and ask what that key cannot see** — then test membership a way
> that does not depend on the convention. Here that was: take every field name
> the pack writes on a non-local carrier and test it against the whole shipped
> tree (4,446 files / 131,363 tokens). A name absent from Src is ours, whatever
> it is called.
>
> ⚠️ **What a re-take of L3 owes, in priority order.** ① **13 of the 18
> load-time passes were never cross-read against the game's own 237
> `SavegameFixups`** — only the 5-module track cluster was. The hazard is real
> and documented (`90_SaveSanitizer:315-324` was bitten by it once), and §6.1 of
> `reports/L3_SAVE_FOOTPRINT.md` establishes it is live on exactly one load per
> save: the first load of a save that still owes that fixup — which is the
> population the repairs target. Unswept: the meteors/storm pair, the
> rains/disaster pair, the three preset-patch heals. ② **Nobody has ever walked
> an uninstall, let alone a REINSTALL** (uninstall → play → save → reinstall).
> The reinstall route is where the exit law bites, and it is a real player
> action — Paradox Mods replaces the folder on update. ③ **The simultaneous
> liveness of the six game-time threads has never been measured by anything**,
> so "how much is in a save at once" still has no upper bound a reader can point
> to. ④ The opt-in pack's own footprint (D12–D15) was not re-derived.
>
> ⭐ **And the shape that made the exit legible, offered as a template:** stop
> asking "does this site persist" per module and ask **"who owns the CARRIER".**
> A persisted name of ours survives uninstall iff its carrier is vanilla's — one
> line that sorts all twelve keys, and it is the inverse of what one shipped
> header had been disclosing for weeks.

## L4 · Player experience

**What does a player actually SEE and READ?** The answer should be **nothing** —
and the 2026-08-17 defect was exactly this class, caught only because a box
appeared on screen during an upload sitting.

- First launch through to a loaded save: dialogs, notifications, banners.
- Log lines a curious player could stumble into — is any of it alarming or false?
- In-game wording anywhere the mod speaks (the stand-down dialog is the only
  designed one — is it?).
- ⚠️ Read it as **a player who arrived from a store link and knows nothing**, not
  as someone who knows what the mod is for.

> ⭐⭐ **Added by link 4 (2026-08-18) — ASK WHERE THE SURFACE'S WORDS COME FROM,
> NOT WHETHER THE SURFACE WORKS. This generalises past L4 and it is the question
> that produced both of this link's real findings.** The pack has exactly one
> designed screen surface and the obvious questions about it (does it fire, does
> it fire twice, does it fire falsely) had all been asked. Nobody had asked the
> boring one: **what STRING does it print, and where did that string come from?**
> Two answers, both defects. It prints `table.concat(suspects, ", ")` — internal
> module ids — while the registry beside it carries a plain-English `title` for
> all 75 modules; and its single sentence covers `status == "error"` as well as
> `inactive`, so a crash of **ours** is announced to the player as a **game
> update**. ⇒ **A surface that works is not a surface that is honest.** Trace
> every player-read string back to the variable it is built from and ask what
> else can be in that variable.
>
> ⭐ **And the corollary that found the third one: enumerate the STATE
> TRANSITIONS, then ask which of them is silent.** Every status change in
> `00_Core` writes a log line except `ctx.heal()`, which writes none — so a log
> can end on a false `inactive`. That is not visible in any single module; it is
> visible in one table of transitions against one column of log lines, and the
> archive then measures it (56 of 57 logs carry the stale line). **Whenever a
> component reports its state, list the transitions and diff them against the
> reports.**
>
> ⚠️ **What a re-take of L4 owes, in priority order.** ① **The one designed
> surface has never executed** — 0 occurrences in 57 archived logs — so every
> claim about it, including this link's four Src re-derivations, is source-only.
> The first configuration that makes it fire is worth staging deliberately.
> ② ⛔ **No console platform has ever been touched by this project**, and
> `FIX_POLICY` §7 makes that dialog the ONLY player-facing surface there — the
> highest-leverage unreached territory in this lens by a distance. ③ **No
> non-English run, ever**: two re-used translation ids ship on player screens and
> neither was tested against `Local\*.fpk`, though `tools/flpk_extract.py` and the
> `C51` precedent make it a cheap, mechanical job. ④ **The aggregate notification
> RATE** — one module deliberately revives a warning class vanilla could never
> fire, and nobody has watched a colony with it on.
>
> ⭐ **A negative worth inheriting so it is not re-derived:** the pack mints **no**
> notification, popup, banner or voice line of its own. All 17 screen call sites
> raise a surface the game already owns, inside vanilla-body copies. The player
> experience of this pack is, by construction, the game's own — which is why the
> two defects both landed in the one place the pack speaks with its own voice.

## L5 · Failure & containment

Every module routes through `00_Core`.

- One module's `apply` throws — are the other 74 unaffected? (`run_apply` pcalls;
  verify, and check the **runtime** paths too, not just apply.)
- An installed **wrapper** throws mid-game — what does the player experience?
  `FIX_POLICY` §2 says *fail safe, never loud*. Is that true **in aggregate**?
- An `OnMsg` handler throwing is swallowed by `procall` (`cthreads.lua:20`) —
  the named **F87 failure mode**: reporting `active` while having done nothing.
  How many modules could be in that state right now and nobody would know?

> ⭐⭐ **Added by link 5 (2026-08-19) — ASK WHO OWNS THE FAILURE SURFACE, NOT WHAT
> THE COMPONENT DOES WHEN IT FAILS. This generalises past L5 and it is the
> question that produced everything this link found.** The three bullets above
> are all asked *about the pack's own code*, and the pack's whole fail-safe story
> is told about `apply` — one of **six** entry classes. Ask instead: *for each
> way the engine can enter our code, who is holding the pcall?* The map then
> inverts. The two loudest failure surfaces this pack has are **raised by the
> engine, keyed on our mod's `content_path`, with no call site of ours involved**
> (`EF-065`): an uncaught runtime error whose stack touches our path pops
> *"Mod-related problem detected … Mod Flagged: Relaunched Fix Pack"*, and a
> file-scope throw pops the load-errors box. ⇒ **L4's census of 17 screen call
> sites in `Code/` was correct and structurally could not see either.** A
> component's failure surface is not necessarily in the component.
>
> ⭐ **Corollary that found the widest blast radius: a throw at FILE SCOPE does
> not make a module `inactive` — it makes it ABSENT.** `Register` never runs, so
> the id is in neither `fixes` nor `order`, and `ListFixes` / `UpdateSuspects`
> are structurally blind to it. **Whenever a component reports its own health,
> ask what a failure looks like that removes the reporter.**
>
> ⚠️ **What a re-take of L5 owes, in priority order.** ① **The 53 method wrappers
> were never traced to their callers** — "who holds the pcall at a wrapper" is
> answered structurally and not per site; that is a concrete, mechanical ~53-row
> job and it is the largest unswept surface in this lens. ② ⛔ **Whether
> `map:MapForEach`'s C loop `procall`s its callback per object** decides whether
> three unguarded load-time repairs lose one object or the rest of the colony —
> one console line settles it (routed, checklist 44). ③ **Whether
> `OnMsg.OnLuaError` fires for a THREAD error** (`cthreads.lua:137-141` raises
> `OnThreadError`, a different message) — if not, the pack's 8 threads are
> quieter than its wrappers, which is a design lever nobody has had. ④ The
> TestKit's own containment, excluded here for the fifth time and the one
> component measured to have emitted `[LUA ERROR]` lines of its own.
>
> ⭐ **Two donor shapes the pack already contains — measure the rest against
> them.** `Fix_ExtenderFlapChurn:70-104` is how to install OUTSIDE apply's pcall
> (probe the target into `install_error`, gate the install, `return install_error`
> from apply) — it is the only module that does, and it cannot throw.
> `Fix_TrainMinors:141` / `Fix_TrackTunnelPowerBridge:164` are the **per-ITEM**
> `pcall` inside a sweep, so one bad object costs one object instead of the whole
> repair. Three sweeps do not hold to it.

## L6 · Promise vs behaviour

Five surfaces must agree and have drifted before: `bugs/INDEX.md` ·
`metadata.lua` `code` · `items.lua` · the shipped `.fpk` · the card/site/README.

- Any module shipping with no entry? Any entry promising a fix not in the package?
  (The `F24`/`F28` class — bullets promising **deleted** fixes — has happened.)
- ⛔ **Dead-coded targets: is F85 the only one?** Its dialog's sole caller sits
  behind a literal `local cond = false`. **Nobody has swept for a second
  instance**, and *player-route ≠ source citation* has been the finding **three**
  times.
- The **veto route** the README began advertising on 2026-08-17: does
  `SMRFixPack_Disabled` actually stop **all 75**, including modules that patch at
  load without going through `WhenActive`? ⭐ *"You can X" needs a route check* —
  a citation proving the mechanism exists is a **different** check, and the owner
  has overturned a line three reviews passed on exactly this.

> ⭐⭐ **Added by link 6 (2026-08-19) — ASK WHAT REWRITES THE SURFACE, NOT
> WHETHER THE SURFACES AGREE TODAY. This generalises past L6 and it is the
> question that produced this chain's first launch blocker.** The five surfaces
> above are treated as five things to *compare*, and comparing them is how the
> `F24`/`F28` class was caught. But one of them — `metadata.lua`'s `code` list —
> is not authored, it is **DERIVED**: `ModDef:SaveDef` rebuilds it solely from
> `items.lua`'s items (`Mod.lua:816-840`, called at `:973`), with no disk scan,
> and **both portals force that save on a first upload** — Steam's *before*
> packing (`SteamWorkshop.lua:17-22`, `GedModEditor.lua:772-824`). ⇒ **The
> surfaces agreeing on disk today says nothing about what the store receives.**
> `items.lua` had 75 entries against a 76-entry `code` list and the mod would
> have shipped a fix missing. **For every surface, ask: who writes this, and does
> anything rewrite it between here and the player?**
>
> ⭐ **And the corollary that explains why nobody had caught it: A GUARD IS A
> CLAIM TOO — go read the guard, not its verdict.** `upload_preflight.py` has a
> check for exactly this defect and it printed PASS, because it counted the
> string `"ModItemCode"` over the whole file including **the header comment that
> explains the guard**. 75 real + 1 comment = 76. Two errors cancelling. This is
> L3's *"ask what the census key cannot see"* pointed at our own tooling: **when
> a guard covers the thing you are checking, re-derive what it measures before
> you let it stand in for the check.** Same day, the same lens's own extractors
> were wrong three times — one of which (a negative lookahead behind `\s*`, which
> backtracks) would have inverted the veto verdict.
>
> ⚠️ **What a re-take of L6 owes, in priority order.** ① **Preset-FIELD patches
> are unswept for dead targets.** The dead-code sweep covers 13 global
> replacements and 55 class/table members against 4,446 Src files; a preset field
> we write that nothing READS is the same defect class and is invisible to a
> call-shaped census — link 1 left the same half non-mechanical. ② **The veto has
> never been exercised by an actual foreign mod**; every verdict about it is
> source-derived. ③ **`ListFixes()` has never been observed** — the surface the
> README points a modder at, 0 occurrences in the archive. ④ **Whether an assert
> in mod code reports at all in a RETAIL build** — `EF-008` is unqualified,
> `autorun.lua:243` says it is build-specific, and this project's one measurement
> is a MarsDebug log.
>
> ⭐ **A negative worth inheriting so it is not re-derived:** a **foreign** mod's
> write to one of our globals DOES reach us. `ModEnvMeta.__newindex`'s
> `rawset(original_G, …)` runs in every branch (`Mod.lua:1562`, the `EF-064`
> shape), and `ModsLoadCode()` sits between `Loading = true` and
> `Loading = false` (`autorun.lua:1`/`:423`/`:560`), so the strict-global
> create-assert is suppressed for **all** mod code, ours and theirs. The read
> assert at `:1553` has **no** such guard — which is why every read of the veto
> table inside `Code/` uses `rawget(_G, …)` and why the snippet we publish should.

## L7 · Environment & namespace

- **Enumerate every global the pack creates or writes.** ⚖️ **CORRECTED by link 7
  (2026-08-19): this bullet said "Expected: `SMRFixPack`, `SMRFixPack_Disabled`,
  `SMRFixPack_Optional`" and the real set is FIVE** — those three plus the two
  `GameVar`s `SMRFixPack_MeteorLatch` (`Fix_MeteorFrequency.lua:76`) and
  `SMRFixPack_FirstAsteroidPrefabs` (`Fix_FirstAsteroidPrefabs.lua:115`, declared
  through an alias `GameVar(FLAG, false)` a plain grep cannot join). Both are
  deliberate and headered; the *expectation* was what was wrong. ⛔ Any accidental
  global is a collision risk with other mods — and other mods are on this rig by
  ruling. `EF-064` is relevant (`ProtectedPropertyObject` protects nothing in retail).
- ⭐ **Packed vs unpacked.** A player gets `MountPack` + `def.packed = true` +
  `metadata.lua` read from **inside** the archive (`Mod.lua:1724-1740`). We have
  only ever run `MountFolder` through a junction. See
  `98_LAUNCH_REHEARSAL.md` §4.
- ⭐ **What has the TestKit been hiding?** It loads innermost, **mutates `_G`**
  (`SMRTest.SetGlobal`, the loggers), registers a UI action and enables the
  console — and **every gate reading this project owns was taken with it loaded.**
- Console platforms (`FIX_POLICY` §7): achievements block on exactly
  playstation / xbox / **windows_store** (`Achievement.lua:61-63`) ⇒ say *"Steam
  and other PC versions"*, ⛔ never bare "PC".

> ⭐⭐ **Added by link 7 (2026-08-19) — WHEN A QUESTION IS DECIDED BY SCOPE, DO
> NOT ASK A PATTERN. ASK THE COMPILER. This generalises past L7 and it is what
> made everything below cheap.** "Enumerate every global" reads like a grep job
> and is not one: whether `x = 1` is a global or a local is decided by **scope**,
> and the same eight characters are a local write inside `local x` and a global
> write outside it. This project has three sessions on record of extractors that
> were wrong in exactly that way, one of which would have inverted a verdict.
> But Lua 5.2+ compiles every global access to an indexed access on the `_ENV`
> upvalue, so the bytecode carries the answer with no ambiguity at all —
> `SETTABUP`/`GETTABUP` where the upvalue is named `_ENV`. `lupa` is already a
> dependency (`tools/l2_reload_sim.py`), and `tools/l7_env_map.py` is ~250 lines
> that cannot be fooled by shadowing, nested closures, method definitions,
> for-loop variables, parameters or `local _ENV`. ⇒ **Before hand-rolling a
> scanner, ask whether a real compiler or parser already decides the thing you
> are about to approximate.**
>
> ⭐ **And the corollary that produced this link's gate finding: A CRITERION IS A
> CLAIM TOO — read what its EVIDENCE COLUMN actually tests.** Link 6 established
> *"a guard is a claim too"* about `upload_preflight`. Point it at the release
> gate itself: `98_LAUNCH_REHEARSAL.md` criterion 1 said *"the mod loads
> **packed**"* and offered *"`[CommunityFixPack]` lines exist at all"* as its
> evidence — lines that are equally present unpacked. The criterion certifying
> that run B measured the player's configuration **could not fail**. The engine
> prints the fact plainly (`Mod.lua:1849`), and 66 of 66 archived sessions say
> `unpacked`. ⇒ **For every pass criterion anywhere, ask whether its evidence
> can come out NO. One that cannot is not a criterion.**
>
> ⚠️ **What a re-take of L7 owes, in priority order.** ① ⛔ **The runtime `_G`
> has never been enumerated by anything.** This link proves what the *source*
> writes; the live-process global set has never been listed or diffed against
> vanilla, and that is the direct falsifier for "no sixth name". It needs one
> console line or one probe — both barred pre-launch, so it is **post-launch
> work, deliberately parked**, not an oversight. ② **`CheckModPackSignature` was
> not read**, so whether the packed branch is even taken on this rig is open —
> and it gates everything about configuration B. ③ **The TestKit was swept for
> NAMESPACE only**; its second-load behaviour and its own containment are still
> unswept after seven links, and it is the one component measured to emit
> `[LUA ERROR]` lines of its own. ④ **No console platform, ever** — that the pack
> never reads `Platform` is a real result but a different claim from behaving
> correctly there.
>
> ⭐ **Negatives worth inheriting so they are not re-derived** (all re-derived at
> Src this link, artifact §2–§5): neither engine assert is reachable by this pack
> — no write can trip the strict-global create-assert (every nested-scope write
> targets a `GameVar` or a file-scope global function), and no read can trip the
> undefined-global assert (all 187 read names resolve, because every
> possibly-absent name is reached through `rawget(_G, "…")` and never bare). The
> pack creates **zero** env-table shadows. `writes ∩ ModEnvBlacklist = ∅`.
> **`content_path` is `"Mod/<id>/"` in BOTH the packed and unpacked cases**
> (`Mod.lua:1755` + `ModContentPath` `:6`), which closes link 5's open worry that
> `EF-065`'s mod-flag match might behave differently in run B. And the pack and
> the TestKit are **disjoint on global writes in both directions**, with the pack
> reading nothing the kit provides — the first evidence that six links' worth of
> "the TestKit was loaded for every reading" is not hiding a dependency.

## L8 · Adversarial / hostile modder

Assume another mod is installed that is not ours and not friendly.

- It wraps what we wrap, and loads **before** us. Then: **after** us. What breaks?
- ⚠️ Inter-mod order is the player's **enable** order, decided before our Lua
  runs; there is no priority field and enabling APPENDS (`ModManager.lua:36`),
  while the visible list is a **cosmetic title sort** (`Mod.lua:1674`) — so a
  player cannot verify any advice we gave. ⛔ Load order must NOT appear as player
  advice (owner ruling 2026-08-16); this lens is about **resilience**, not
  guidance.
- If a conflict does occur, **whose fault does it look like** — and does our
  stand-down machinery report something true, or something that blames the game?
- `EF-054` (wrapper ordering, mod-id keying) and `EF-058` (the flattened-class
  trap — bit this project **four** times) are the known shapes.

> ⭐ **Added by link 1: the pack already contains the benchmark shape — measure
> the rest against it.** `Fix_DustDevilSpawnGate:250-258` swaps a global and, when
> restoring, re-reads the live value and only swaps back **`if cur == wrapper`** —
> so a replacement installed *after* ours by another mod is left alone instead of
> being clobbered. That is the correct save/restore discipline. ⛔ Link 1 did NOT
> sweep whether the pack's other 15 global replacements hold to it; that sweep is
> this lens's, and it is a concrete, mechanical job.
