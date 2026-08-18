# L4 — the player-surface map

**Link 4 of the pre-launch sweep chain, lens L4 (player experience), 2026-08-18.**
Instrument `tools/l4_player_surfaces.py`; run it to re-emit every count below.
⛔ **Record-only link** (`00_CHAIN_SPEC.md` §4) — nothing here was fixed.

**Configuration label.** Source-derived over the dev tree, unpacked, plus Src read
by symbol, plus the archived log corpus (the **all-three-mods** rig, TestKit
loaded, junction install). ⛔ **No launch. Nothing in this report was seen on a
screen.**

---

## 0 · The question, and why it needed an aggregate

The lens notes put it in one line: *what does a player actually SEE and READ?
The answer should be **nothing**.* Every module was reviewed for correctness;
nobody had ever listed the pack's player-facing surfaces and read them as a
player who arrived from a store link and knows nothing.

The census says the answer is **almost** nothing, and the exceptions are all in
one place: the pack has exactly **one designed screen surface**, it has **never
executed**, and both defects below live in it.

---

## 1 · The census — five tables, all mechanical

| # | census | count | what it counts |
|---|---|---|---|
| 1 | SCREEN | **17** sites | calls that draw pixels or speak |
| 2 | TEXT | **6** sites | `T{…}` / `T(…)` / `Untranslated(…)` |
| 3 | LOG | **59** sites in 13 files | lines a player can read in the log |
| 4 | VERDICT | **181** strings | anything that can become an entry `detail` |
| 5 | SUSPECT | **72** of those 181 | strings matching `UpdateSuspects`' four tests |

The API set for census 1 was **re-derived**, not assumed: each name was confirmed
to be a global `function` in the shipped Src tree before it went in the pattern.

### 1.1 · SCREEN — 17 sites, and not one raises a surface of our own

| file:line | call | verdict |
|---|---|---|
| `Fix_LowStorageWarning` :97 :111 :142 :173 :184 (add) · :99 :113 :146 :177 :188 :193 (remove) | `Add/RemoveObjectToNotification` | vanilla body copied verbatim (`ResourceTracking.lua:204-316`) but for four `-- FIX (F12):` lines; the Power/Water branches are shipped code, untouched |
| `Fix_BombardmentSpread` :138 :153 | `Add/RemoveObjectToNotification` | vanilla `Bombardment` notification, all-vanilla body |
| `Fix_DisasterPredictionLeak` :87 | `RemoveDisasterNotifications` | clears a leaked entry — strictly **fewer** on screen |
| `Fix_FounderTraitNotification` :47 | `AddNotification` | the repair itself: vanilla's own `FounderGainsTrait`, guarded by `if FindNotification(...) then return end` so it cannot stack |
| `Fix_MilestoneCrash` :41 | `WaitPopupNotification` | vanilla's `AllMilestonesCompleted`, inside a vanilla-body copy |

⇒ **Every notification and popup the pack can raise is one the game already
owns.** The pack mints no preset, no banner and no popup of its own. ⛔ Zero
`modal` and zero `voice` sites outside `00_Core`.

⭐ **The aggregate delta, stated plainly:** the pack makes the game *quieter* by
one class (leaked disaster-prediction entries) and *louder* by one class —
`Fix_LowStorageWarning` revives the Food and maintenance-resource
"Insufficient Resources" warning, which vanilla's arithmetic could never fire.
That is the repair, it is disclosed on the fix list (`content/fix-list.md:471-479`),
and it is the single most visible thing the pack does. ⛔ **Nobody has ever
watched a colony with it on** — see §5.

### 1.2 · TEXT — 6 sites, 4 of them the one dialog

| file:line | form | verdict |
|---|---|---|
| `00_Core` :574 :575 | `Untranslated` | the update-report dialog. English in every language, by construction — see §2 |
| `Fix_DomeOverviewHighlight` :33 :35 | `Untranslated` | `<red>%d</red>` and a bare number; the vanilla shape its own header quotes. No words |
| `Fix_GraphConsumedCaption` :70 | `T{8979, …}` | ✅ **verified byte-for-byte against `Lua/X/ColonyControlCenter.lua:181-186`** — same id, same literal, same tag set. A localised build resolves 8979 in its own pack and is unaffected |
| `Fix_TechDescriptionBuilding` :75 | `T(841885693955, …)` | re-used shipped id — and **`F98` is our own filed defect**: the engine discards a re-used id's literal at `T()` construction, so this is a **no-op in retail** |

⭐ **`F98`'s player-surface consequence is contained, and this lens is what
confirms it:** the store card does not promise this fix (0 hits for the tech or
the building name in `RELEASE_DESCRIPTION_FIXPACK.md` / `STORE_FIXPACK.md`) and
the site fix list deliberately omits it. ⇒ **the pack never promises a player
something `F98` fails to deliver.** The only residue is a log line (§4).

---

## 2 · ⭐ The one designed surface — verified at source for the first time

`00_Core.lua:560-578`. A real-time thread polls for the pregame main menu (5-min
deadline), then raises a `WaitMessage` if `UpdateSuspects()` is non-empty.

⛔⛔ **IT HAS NEVER RUN.** `update report:` (`:570`, logged *before* the dialog)
has **0 occurrences in all 57 pack-carrying logs in `docs/archive/*.log`** —
counted this session, not inherited. Everything below is re-derived at Src.

### 2.1 · The mechanism holds — four checks, none previously made

| check | result | source |
|---|---|---|
| call signature | ✅ `WaitMessage(parent, caption, text, …)`; our `(nil, caption, text)` matches | `CommonLua/UI/StdDialogs.lua:617` |
| `parent = nil` | ✅ resolves — `parent or terminal.desktop` | `StdDialogs.lua:596` |
| double `Untranslated` | ✅ **no-op.** `CreateMessageDialog` wraps title and text itself (`:542-543`); `Untranslated` returns any `IsT` value unchanged | `localization.lua:339` |
| gamepad-native | ✅ the OK action carries `ActionGamepad = "ButtonA"` | `StdDialogs.lua:570` |

⇒ the console claim in the `00_Core` header holds, and with it `FIX_POLICY` §7's
reasoning: **on Xbox, PlayStation and the Microsoft Store there is no log, no
console and no file access, so this dialog is the pack's ONLY player-facing
surface.** That is what makes §2.2 matter more than its size suggests.

### 2.2 · ⚠️ L4-F1 — the dialog names internal identifiers, not the titles it already has

`:569` `local list = table.concat(suspects, ", ")`. `UpdateSuspects` pushes `id`
(`:537`) off `SMRFixPack.order`, so the player reads e.g.

> Switched off: AstrogeologistExtractors, SaintBlessing

**Measured:** all **75/75** registered modules supply a `title` — a plain-English
sentence, the same register the fix list is written in ("Command Center graph
captions count maintenance, like the bars do"). The registry has it; the dialog
does not use it.

**Measured:** module identifiers appear on **no player-facing surface**. Over the
site's five pages they occur only in `for-modders.md` (:33, :43, :45 — all
`SMRFixPack_Disabled` examples), and in the README's for-modders section. The fix
list, FAQ, install page, landing page and store card name fixes in prose only.

⇒ a player cannot resolve the list against anything they were given — **and a
console player cannot resolve it at all**, having no log, no console and no
second surface. Same class as this project's own recorded trap:
`BottomlessPitResearchCenter` renders as *"Experiment 1: Big Drop"* on every
player surface (08-15).

**Not blocking.** Route: owner-shaped (it is the pack's voice) → checklist.

### 2.3 · ⚠️ L4-F2 — the sentence is false for the `error` case, and it blames the game

`UpdateSuspects` makes `status == "error"` a suspect unconditionally (`:527-528`).
`error` means `def.apply` **threw under `pcall`** (`run_apply`, `:388-392`) — our
own defect, or another mod's interference (the L8 shape). It is never evidence of
a game update. But the dialog says, in one undifferentiated sentence:

> …found that the game code they patch has changed — usually after a game update —
> and switched themselves off for safety. … if the game was recently updated,
> check for a new version of the Relaunched Fix Pack.

⇒ on a crash of ours we would **attribute it to a Paradox patch** and send the
player looking for a version that does not exist, instead of reporting the bug.
The log line at `:570` carries the same wording ("deactivated over a game-code
change").

This is the house rule *"'not caused by our leg' is an attribution verdict, not a
dismissal"* pointed outward at the game. **Latent** — 0 `error` statuses in the
57 archived logs — but it is exactly the case the dialog exists for.

**Not blocking.** Route: batched with L4-F1 → one checklist item.

---

## 3 · The verdict-string census, and the fence that did NOT leak

Census 5 crosses all 181 verdict strings with the four substring tests
`UpdateSuspects` runs (`:532-535`). **72 match.** Every one of the 72 is a
`Require` reason or a bespoke reason constant — i.e. a genuine target-shape
failure, which *also* sets the `update_suspect` mark. **The two routes agree on
all 72; no benign verdict trips a substring.**

⭐ This is the check the 2026-08-17 defect earned and nobody had run in
aggregate: a benign string that happened to contain *"could not install"* would
fire the false-update dialog on a working pack. None does.

The remaining **109** strings match no substring and reach the dialog only via
the mark — which is the intended design (a `latch(…, "benign")` must not fire it).

---

## 4 · ⚠️ L4-F3 — `ctx.heal()` is the one status transition that writes no log line

Every other transition logs:

| transition | line |
|---|---|
| apply success | `:412` `%s: applied` |
| apply threw | `:392` `%s: FAILED to apply: %s` |
| apply declined | `:396` `%s: inactive (%s)` |
| pre-load veto | `:448` `%s: disabled by user/mod setting` |
| `ctx.latch` | `:279` `%s: inactive (%s)` |
| Mod Options ×4 | `:474` `:483` `:487` `:500` |
| **`ctx.heal`** | **`:281-294` — nothing** |

**Measured consequence, and it is not hypothetical: 56 of the 57 pack-carrying
logs in `docs/archive/*.log` carry**

```
[mod] [CommunityFixPack] SaintBlessing: inactive (no dome-colonists trait presets)
```

**which is false by the end of the same load.** In `c48pair2` the module heals
**642 ms later** (Lua `0:00:18:398` → `0:00:19:040`, log lines 171 → 185), and
its recovery is implied only by a *different* line — `corrected 1 dome-colonists
trait modifier label(s) of 2`. **Nothing in the log ever states the module is
active again.**

Two heal sites log nothing at all — `Fix_DustDevilSpawnGate:308` and
`Fix_DustDevilsDescrMap:112`. On a `DataChanged` re-fire after a latch, those
modules' logs would end on `inactive` with **no counterpart line whatever**.

**Who reads this.** The FAQ asks players to attach a log to a bug report
(`content/faq.md:68-83`) and the owner reads logs for triage. A stale `inactive`
is the most misleading line the file can carry.

⛔ **Not cosmetic** — it corrupts triage and it has already contaminated 56
archived logs — but it is **not visible in game**. Nothing a player experiences
changes. Recommendation for the terminal audit: one `log()` inside `ctx.heal()`.

---

## 5 · Log noise, measured

**82** `[CommunityFixPack]` lines in a full load (`c48pair2`, all-three-mods rig):

| lines | content |
|---|---|
| 75 | `<id>: applied` |
| 7 | substantive — 6 repair reports + 1 `inactive` (the stale one, §4) |

Nothing alarming; nothing false but §4's line. ⚠️ One asymmetry: the
tech-description module logs `applied` on every retail game while `F98` makes it
a no-op there. Already filed (`F98`, P3, SOURCE-VERIFIED); the player surfaces
are clean (§1.2), so this is a log-wording note, not a new defect.

### 5.1 · The tag-vs-name route — checked, and it does NOT break

A player reads `[CommunityFixPack]`; the mod is called **Relaunched Fix Pack**
everywhere they look. The tag was kept deliberately (checklist 36).

⭐ **Route walked, per *"'you can X' needs a route check"*:** the FAQ's bug-report
section tells players where the logs live and asks them to **attach one**; it
never asks them to find our lines, and no player-facing page names the tag.
⇒ **the route does not break.** Recorded here so that a future page which says
*"look for lines from the Relaunched Fix Pack"* is caught before it ships.

---

## 6 · What a store-link player reads — two blanket claims, checked per row

**⭐ *"Every fix checks the game's code before it patches anything and stands
down if an official patch changes what it was written for."*** (`metadata.lua`
`description`) — **holds across all 75.** 69 modules route through
`SMRFixPack.Require`; the remaining **7** each carry a bespoke precondition check,
read at source per row — ⛔ provenance per row, not a blanket verdict
(`WORKFLOW` R3):

| module | check |
|---|---|
| `Fix_DustSicknessBiorobots` | :122 |
| `Fix_ExtenderFlapChurn` | :73-75 (file-scope `install_error`) |
| `Fix_IndependenceTerraforming` | :72 |
| `Fix_LastTransmissionStorage` | :108 |
| `Fix_SequenceLatents` | :136 |
| `Fix_ShelterReflex` | :79 |
| `Fix_StorageRateModifiers` | :75 |

**⭐ *"Five of the fixes are judgment calls."*** — **consistent on every surface.**
The fix list marks exactly **5** entries `— *judgment call*` (`content/fix-list.md`
:95, :283, :323, :344, :698); `metadata.lua` `description`, `faq.md:142` and
`faq.md:155-159` all say five. C39's automation entry (`fix-list.md:502`) ships as
a plain repair with its own "Worth knowing" disclosure at `:519-525` — consistent
with the 08-15 item-30 ruling.

---

## 7 · ⛔ What this lens did NOT reach

- ⛔ **Nothing was run in a game. Fourth link in a row.** No dialog has drawn, no
  notification was observed, no first run was walked. **Every screen verdict here
  is source-derived.**
- ⛔ **The one designed surface has never executed** — 0 `update report:` lines in
  57 logs. How it looks, where it lands, and **whether it opens on top of the Mod
  Manager on the enable path** are all UNMEASURED. (The enable-path re-fire is
  checklist item 39, link 2's open decision — not re-decided here.)
- ⛔ **No console platform has ever been touched by this project**, and §7 makes
  this dialog the only console surface. The gamepad route is re-derived at Src,
  never observed.
- ⛔ **No non-English run, ever.** The dialog is English in every language by
  construction. Whether `T id 8979` and `T(841885693955, …)` resolve correctly in
  a shipped language pack was **not** tested against `Local\*.fpk` — the route
  exists (`tools/flpk_extract.py`, the `C51` precedent) and was not run.
- ⛔ **The aggregate notification RATE is unanswered.** 17 call sites were
  enumerated; "does the pack make the game noisier" needs a running colony, and
  `Fix_LowStorageWarning` revives a whole warning class vanilla never fired.
- ⛔ **`Fix_DomeOverviewHighlight`'s `<red>` markup** was not confirmed to render.
- ⛔ **The store and Mod Manager entries as RENDERED** — truncation, layout,
  character limits — remain check-at-paste and have never been seen.
- ⛔ **TestKit tree excluded a FOURTH time.** Its UI action and console are
  supposed to be absent in configuration B; unswept.
- ⛔ L5 (failure & containment), L6 (promise vs behaviour), L7 (environment &
  namespace), L8 (adversarial) — **entire**.
