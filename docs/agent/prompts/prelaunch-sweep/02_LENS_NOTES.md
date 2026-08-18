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

## L5 · Failure & containment

Every module routes through `00_Core`.

- One module's `apply` throws — are the other 74 unaffected? (`run_apply` pcalls;
  verify, and check the **runtime** paths too, not just apply.)
- An installed **wrapper** throws mid-game — what does the player experience?
  `FIX_POLICY` §2 says *fail safe, never loud*. Is that true **in aggregate**?
- An `OnMsg` handler throwing is swallowed by `procall` (`cthreads.lua:20`) —
  the named **F87 failure mode**: reporting `active` while having done nothing.
  How many modules could be in that state right now and nobody would know?

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

## L7 · Environment & namespace

- **Enumerate every global the pack creates or writes.** Expected: `SMRFixPack`,
  `SMRFixPack_Disabled`, `SMRFixPack_Optional`. ⛔ Any accidental global is a
  collision risk with other mods — and other mods are on this rig by ruling.
  `EF-064` is relevant (`ProtectedPropertyObject` protects nothing in retail).
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
