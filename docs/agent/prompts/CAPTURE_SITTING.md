# One-off brief — the retained screenshot sitting

> ⚖️ **OWNER RULING 2026-09-09: KEEP — *"we may get to it."*** Reviewed in the
> prompt-pruning pass and retained. ✅ **It is UNFIRED**, not spent. The
> preview-art floor was completed separately and already shipped; that consumed
> Pass G, not the owner's instruction to keep the remaining screenshot job.
>
> ✅ The old D13 and hotfix-2 scheduling gates are discharged. They are history,
> not current prerequisites. The owner's scheduling word is the only gate this
> file adds before its own preflight.
>
> ⚠️ **It needs an era pass before it is fired, and the reason is not cosmetic.**
> This was written 2026-08-13 for game 1.0.7. `EF-079`: **1.0.7 saves cannot load
> on 1.1.0**, so every fixture and colony this brief's shot list assumes is
> unreachable — a 1.1.0 capture sitting needs a colony provisioned from scratch
> (hours), which is exactly the cost `EF-080`'s triage-only override does not buy
> back. ⭐ Against that, the *reason* to fire it is stronger than when it was
> written: the store card now describes a 1.1.0 + DLC build, so the shots would
> want retaking regardless of this brief's age.

**Authored 2026-08-13; retained by owner ruling at `edf1fdf`.** At execution,
start with `git log --oneline -6`, `git pull`, and `git status --short`; compare
the current surfaces and entries with `edf1fdf..HEAD` before trusting a shot.

**Owner-attended, in game, ONE sitting.** Most of the work is capture; Pass C's
toggle observation and Pass E's render observation are measurements and follow
the testing rails below. Full reasoning and each shot's original job:
`docs/agent/reports/PUBLIC_DOCS_DESIGN.md` §8B.

⚠️ **Delete this file when consumed** (one-off convention), and record what was
captured — by file name — wherever the images land.

## Execution progress — initialise when the owner schedules the sitting

Before any action, mark the first row `IN PROGRESS` and the others `PENDING`;
keep exactly one unfinished row in progress and put each reading in its row.

- Revalidate current player surfaces, existing image assets and every required
  fixture; drop shots already satisfied or no longer consumed anywhere.
- Run the remaining A–E capture/observation queue, with each dropped shot named.
- Record file names and readings, update current consumers, delete this prompt
  and its prompt-map row in the same commit.

Read path: this file; `docs/agent/reports/PUBLIC_DOCS_DESIGN.md` §8B as historical
design; `docs/agent/bugs/INDEX.md` before the named F13/F14/F19/F102 passages;
`docs/agent/facts/INDEX.md` before EF-056 and EF-079; `docs/agent/WORKFLOW.md` "Probe
hygiene" and "Testing checklist per fix"; current `metadata.lua`,
`store_screenshots/`, and the current site source only if a shot still has that
consumer. Read STATE only to check current scheduling/probe-age status.

## Derived facts and falsifiers

| fact | measured | falsifier |
|---|---|---|
| the owner retained this unfired screenshot job | owner ruling recorded at `edf1fdf` and in the prompt map | a later owner ruling; an agent does not infer one from age |
| 1.0.7 fixtures cannot simply be reused on the installed 1.1.0 branch | EF-079, whose 1.1.0 build fingerprint held at the 2026-09-15 audit | `python tools/doccheck.py --emit-fingerprint`; re-derive if the group moved |
| F13, F14 and F19 remain live fix-pack subjects; F102 remains a named capture subject | focused bug-index lookup at `638db00` | re-run `rg -n 'F13|F14|F19|F102' docs/agent/bugs/INDEX.md` and inspect only moved entries |
| preview art is already complete, so Pass G is consumed | `preview.png` plus final assets under `docs/agent/reports/preview_art/`, with release receipt in `docs/agent/reports/RELEASE_PORTAL_PREP.md` | inventory those paths and the current release receipt before restoring any art work |

---

## ⛔ BEFORE THE GAME LAUNCHES — non-negotiable

1. ⛔ **`EF-056`. Byte-copy EVERY autosave first, and list them by name at
   close-out.** Loading a *copy* of a real campaign still runs that campaign's
   autosave, and its rotation deletes the owner's autosaves. **This has already
   cost this project `Autosave Sol 306`, unrecoverably.** "Use a designated
   copy" protects the file; it does not protect the folder.
2. ⚠️ **The rig has CHEATS ENABLED.** No shot below should depend on a cheated
   state — but if a colony has to be posed with one, **say so beside the image**
   so a caption never implies otherwise.
3. ⛔ **Probe hygiene before the session.** Run WORKFLOW's exact stale-probe
   sweep across the pack and TestKit whether or not the TestKit will be loaded.
   Check STATE's current age/change gate; the owner may override scheduling, but
   an agent does not silently turn an old stamp into current evidence. Record the
   sweep in any commit that records a measurement.
4. ⭐ **Check the save fixtures FIRST and re-route anything whose state does not
   already exist.** ⛔ **Do not ask the owner to BUILD colony state for a
   screenshot** — drop or substitute the shot instead, and record which.
   The remaining shots that need state the save may not have are:

   | shot | state it needs |
   |---|---|
   | `F14-before` / `F14-after` | ⭐ **a dome with colonists whose stats are actually low** — no low stats, no red highlight, and the pair has no subject at all. **Check this before Pass A**, because it is the only fixture that has to hold across *both* restarts |
   | `F19-after` | a Command Center graph with enough history that maintenance is visibly part of "Consumed" |
   | `optin-nohomeless-on` | a dome that actually has jobseekers in it (was already flagged inline; it belongs here) |
   | `multiplesuns` (D) | two Artificial Suns built |
   | `F102-signs` (E) | an asteroid with subsurface Exotic Minerals |

   `F13` needs nothing — any Command Center will do — which is why it is the
   pair to rely on if `F14`'s fixture is missing.

   ⭐⭐ **THE FIXTURE CHECK RAN 2026-08-13 from the save directory itself — not
   from prose.** Method: every
   `*.savegame.sav` in `…\Saved Games\Surviving Mars Relaunched\<id>\` read at
   its plain-text metadata header (`displayname`, `elapsed_sols`, `loaded_maps`,
   `active_mods`); 90 files, all readable without launching the game. What it
   settles and what it cannot:

   | shot | verdict from the directory | what to do |
   |---|---|---|
   | `F102-signs` (E) | ⛔ **RE-ROUTE. There is no save named `Sylmacaink BH25`** — the name in `COMBINED_SITTING.md` moment C and in `F102.md`'s playtest item matches nothing on disk. Worse, **no save anywhere carries the leg's map**: the only asteroid maps in the whole directory are `BlankAsteroidDonut_01` and `BlankAsteroidBranchOut_01` (the campaign's own two), and the 2026-08-12 negative-repro leg ran on a console-spawned `BlankAsteroidSlim_02`, which was never saved. `TEST2 AST` despite its name has **no asteroid map loaded at all** | ⛔ Do not send the owner looking for that save. Either **respawn** the D-type with `F102.md`'s own recorded call (`UIColony:SpawnAsteroid(Presets.DiscoveryAsteroidPreset.Default["Asteroid_D"], true)`) — a rig action, not colony-building — or take the shot on one of the campaign's two existing asteroids **only if** a subsurface Exotic Minerals deposit is actually on them, which the metadata cannot tell us. If neither is quick, **drop the shot** |
   | `optin-*` (C) | ✅ nothing needed from a save — the Mod Options page is reachable from the main menu. (For the record: only 6 saves were written with the opt-in pack loaded, all 2026-08-12 `SPWIT*`/`SPCONRT` and one `Autosave Sol 311`) | proceed |
   | `optin-nohomeless-on` | ⚠️ **UNKNOWABLE from outside the game** — no metadata field carries "this dome has jobseekers in it" | the row itself is the instrument: it reads `(N would move)` before you click. **If every dome reads `(0 would move)`, drop the pair** and say so. ⛔ Do not build the state |
   | `F14-before`/`after` | ⚠️ **UNKNOWABLE from outside the game** | check it in Pass A before spending the restart; if no dome shows low stats, fall back to the `F13` pair as the brief already says |
   | `F19-after` | ✅ any campaign save has the history — the directory holds 30+ saves at 285–336 sols | proceed |
   | `multiplesuns` (D) | ⚠️ **UNKNOWABLE, and it is the one shot that would cost real colony-building** — a second sun has to be *built*. `D04`'s PT-50/PT-55 legs (2026-07-27 / 07-30) did build one, but no save from those dates in this directory is identifiable as carrying it | check once, early. ⛔ If a second sun is not already standing, **drop the shot** rather than asking for one — it is a store-card nicety, not a claim anything rests on |

   ⚠️ **What this check does NOT establish.** Metadata carries maps, sols, mods
   and timestamps — nothing about colony contents. Several fixtures are
   therefore still open at the keyboard, which is exactly why they are written
   above as *checks with a drop rule* rather than as shots.

## ⚠️ Why the order matters

**A Mod-Manager toggle needs a FULL game restart.** A naive shot list costs one
restart per before/after pair. The order below costs **two, total**.

---

## Pass A — both mods OFF (first restart into it)

Capture ONLY the "before" frames. Keep the same save loaded and the camera
still between shots so the pair matches.

| shot | frame |
|---|---|
| `F13-before` | Command Center resource panel — the eleven rows rendering as **blank space** |
| `F14-before` | Domes Overview — low colonist stats **not** highlighted red |

## Pass B — restart with both mods ON, same save, same camera

| shot | frame |
|---|---|
| `F13-after` | the same rows, now showing their numbers |
| `F14-after` | the same overview, low stats now red |
| `F19-after` | a Command Center graph caption where "Consumed" now includes maintenance ⚠️ weak as an image; site only, not a store card |

## Pass C — the opt-in pack's surfaces (same session)

⭐ **The strongest material the project has.** Take your time here.

⭐⭐ **ONE FREE MEASUREMENT WHILE THE PAGE IS OPEN (added 2026-08-13, `02_QA.md`).**
The page is already on screen for `optin-modoptions`, so this costs nothing:
**flip one toggle, press Apply, and look at the game without restarting it.**
`Opt_MultipleSuns` is the sharpest one — its effect (the Artificial Sun build
limit) is visible immediately in the build menu.

* **Expected:** the change takes effect at once. Source says every module has a
  live route — seven consult their active flag per call, `MultipleSuns` carries
  explicit activate/deactivate handlers.
* **Why it is worth a minute:** this is a *store-page claim about what a player
  can do*, and it is currently **source-verified and never play-verified** — the
  exact shape of claim that has already been wrong twice on this project. Two of
  our own documents contradicted each other on it until this week.
* **Verdict words:** "toggle took effect without a restart" / "needed a restart"
  / "could not tell". ⛔ Any of the three is a result; "could not tell" is not a
  failure and must be recorded rather than retried into a better answer.

| shot | frame |
|---|---|
| `optin-modoptions` | Options → Mod Options → the opt-in pack: 7 toggles + 2 dials on one page |
| `optin-dials` | the drone speed (or carry) dropdown **open**, showing its options |
| `optin-domerows` | a Dome infopanel showing **both** policy rows at once |
| `optin-nohomeless-off` | ⭐⭐ **the best shot in the project** — the Nursery/Retirement row reading `off (N would move)` |
| `optin-nohomeless-on` | the same row reading `N moving out` ⚠️ needs a dome that actually has jobseekers in it |

## Pass D — set pieces

| shot | frame |
|---|---|
| `multiplesuns` | two Artificial Suns on screen — the only shot that looks like a *feature* |
| `modmanager` | the Mod Manager listing both mods enabled |

## Pass E — the asteroid

| shot | frame |
|---|---|
| `F102-signs` | three subsurface Exotic Minerals deposit signs rendering. ⭐ The owner's 2026-08-12 negative-repro leg already staged this exact scene — **reuse that recipe** (`docs/agent/bugs/F102.md`) |

⛔ **This is NOT a before/after.** The "before" is a hard freeze on hardware we
do not own. The caption may say the signs render; it may **never** imply we
photographed a cure.

## Consumed branches — do not run

Pass F protected a `ListFixes()` sentence that now exists only in
`docs/archive/MOD_DESCRIPTION.md`; no current player surface consumes that shot.
Pass G asked for preview-art backdrops, but final preview art already exists under
`docs/agent/reports/preview_art/` and the root `preview.png` shipped. Both branches
were cut by the 2026-09-15 prompt-content audit; their history remains in git.

## Close

* Record every captured file **by name**, and every shot **dropped** and why.
  ⛔ A silently missing shot reads as "we got everything" when we did not.
* ⛔ **THE SHOT NAMES IN THIS BRIEF ARE INTERNAL AND MUST NOT BECOME CAPTIONS**
  (added 2026-08-13, `02_QA.md`). `F13-before` and `F102-signs`
  are filing labels. Chain rule 4 bars `F##` ids, file names and function names
  from anything a player reads, and a caption lifted from a filename is the
  easiest way for one to slip through onto a store card.
* Record the Pass C toggle observation; it settles a standing claim without
  producing an image on its own.
* ⛔ **Re-list the autosave folder by name** and confirm nothing went missing
  (`EF-056`).
* Put retained captures in `store_screenshots/`; identify any site-only file in
  the close-out. Update only current consumers—never the deleted public-docs
  chain—and correct the capture item in `PLAYTEST_CHECKLIST.md`.
* Delete this file in the same commit.
