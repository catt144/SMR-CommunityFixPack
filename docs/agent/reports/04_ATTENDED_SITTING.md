# 04 — the attended sitting (`C50` + `C51`): PRE-REGISTERED PREDICTIONS

**Written and committed BEFORE the game opens** (`04_TEST.md` §0; the house
pattern from `97_VERIFICATION_LAUNCH.md`). Results are appended BELOW the
prediction block at close-out, **never edited into it**.

⛔ Everything in the pack right now is **built and unobserved**. Nothing below is
a claim about a screen; it is what the code says should happen, written down so
the sitting can falsify it.

---

## 0 · Preparation that ran before the owner sat down

| step | result |
|---|---|
| `git log --oneline -15` · `git pull` | at `72e7c21`, **already up to date**, working tree clean |
| `python tools/doccheck.py --emit-counts` | **GREEN** — 77 registered modules · 78 `Code/*.lua` · 98 probes · 103 F + 12 D + 53 C |
| `python tools/upload_preflight.py` | **20 checked · 0 FAIL · 1 UNCHECKABLE** (PDX login); `items.lua` ≡ metadata `code`, **78 entries, in order** |
| `python tools/pack_predict.py .` | **82 files** — matches the expected shape |
| ⚠️ `EF-056` autosave pre-copy | **DONE before any launch.** `Autosave Sol 406` (56,195,934 B) and `Autosave Sol 411` (56,195,463 B) byte-copied to `%USERPROFILE%\Saved Games\_SMR_autosave_backup_20260820_link4`, **outside the save dir**. Reconcile by name after every launch. |

⚠️ **The rig runs cheats and both mods are loaded — the normal config** (owner
rule). Neither fix here is touched by any cheat: `C50` is pre-game sponsor text
and `C51` is UI string ids. The rig is not clean, and no reading below depends on
it being clean.

⚠️ **Two boots exist that no archive names** — `Mars.exe-20260819-21.22.47` and
`Mars.exe-20260820-01.13.45`, in the live logs dir. Both read **75 `applied`**,
i.e. they **predate** `C50`/`C51`, and both are ~25 s. The only non-vanilla lines
in either are `[Braze] SessionStart error The server name or address could not be
resolved` ×2 — the game's telemetry client with no network. **Attributed, not
discounted**; they are not this leg's evidence and are not archived here.

---

## 1 · The exact log lines, predicted verbatim

Log tag is `[CommunityFixPack]` (`00_Core.lua:30`); the game prefixes `[mod] `.

**At boot, both new modules:**

```
[mod] [CommunityFixPack] LocalizedUIText: applied
[mod] [CommunityFixPack] SpaceYDroneCapBullet: applied
```

⭐ **The count moves from 75 to 77.** Run B (08-19, packed) logged exactly **75**
`: applied` lines from 75 registered modules; the tree now registers **77**.
⇒ `grep -c ": applied"` should read **77**.

⚠️ **One `inactive` line is EXPECTED and is not a stand-down.** `SaintBlessing`
prints the same three-line sequence it printed in run B and in act 1:

```
[CommunityFixPack] SaintBlessing: applied
[CommunityFixPack] SaintBlessing: inactive (no dome-colonists trait presets)
[CommunityFixPack] SaintBlessing: corrected 1 dome-colonists trait modifier label(s) of 2
```

⛔ An `inactive` line on **`LocalizedUIText` or `SpaceYDroneCapBullet`** is the
stand-down §2 step 1 means — capture its parenthesised reason verbatim.

**Per-site, on first successful patch only** (both modules log the first hit at
each site and then stay silent — these panels redraw constantly):

```
[CommunityFixPack] SpaceYDroneCapBullet: summary now carries the Drone Hub capacity bullet (translation id 4706)
[CommunityFixPack] SpaceYDroneCapBullet: descr now carries the Drone Hub capacity bullet (translation id 4706)
[CommunityFixPack] SpaceYDroneCapBullet: challenge now carries the Drone Hub capacity bullet (translation id 4706)
[CommunityFixPack] LocalizedUIText: terraforming heading now renders translation id 914616772802
[CommunityFixPack] LocalizedUIText: Back to Earth rollover now renders translation ids 407456913268 / 316233855405 (2 of 2 strings)
```

⭐ **The log names the site, so it tells us which of the three `C50` sites fired
independently of anyone's eyes.** That is the cross-check on §2a's skip rule.

⛔ **But the `Back to Earth` line is NOT proof of a screen reading** — see §3.

---

## 2 · ⭐ The number is **40**, and it is derivable before the sitting

`04_TEST.md` §2a illustrates the working bullet as *"…control (**100**)"*. That
was an example, not a claim, and the real value is **40**:

* `CommandCenterMaxDrones` ships with `value = 20` (`Lua\__const.lua:53-57`).
* SpaceY carries `Effect_ModifyLabel{ Label="Consts", Prop="CommandCenterMaxDrones", Amount=20 }`
  (`Data\MissionSponsorPreset.lua`, the SpaceY block).
* `GetModifiedConsts` computes `t[Prop] = MulDivRound(g_Consts[Prop], 100+Percent, 100) + Amount`
  (`Lua\PreGameMission.lua:518-532`). Pre-game `g_Consts.CommandCenterMaxDrones`
  is the unmodified **20** ⇒ **20 + 20 = 40**.

✅ **PREDICTION: the bullet reads *"Maximum number of Drones a Drone Hub can
control (40)"*.** A number that is not 40 on a pre-game screen is a finding.

---

## 3 · Screen-by-screen predictions

### `C50` site 1 — pre-game mission summary panel
`GetSponsorSummary` → `PGMissionSummaryDlg` (instantiated at
`PGMissionSponsorRemastered.generated.lua:609`).
✅ SpaceY's summary gains a **fourth** bullet: *"Maximum number of Drones a Drone
Hub can control (40)"*.

### `C50` site 2 — hover rollover on the sponsor picker
`GetSponsorDescr` → `GetSponsorEntryRollover` → `XPGMission.lua:158`.
✅ Same bullet, same number, at the **end** of the rollover.
(The module declines rather than misplacing it if SpaceY ever gains starting laws
or flavour text; it has neither today, re-checked per call.)

### `C50` site 3 — challenge landing-spot screen
`LandingSiteObject:GetMissionSponsorEffect` →
`PGChallengeLandingSpotRemastered.generated.lua:611`, reachable from the three
shipped Challenges that set `sponsor = "SpaceY"`.
⚖️ Checklist 59 recommends **skipping** it. If skipped, it is named as an
**unobserved site**, never counted as a pass.

### ⛔ The regression that would matter more — SpaceY's FIRST bullet
✅ Must still read *"Dragon Rocket - has smaller cargo capacity **(N)** but is
faster and requires less fuel"* with a real number in the parentheses. `<cargo>`
resolves from the sponsor's own property (`context[prop.id] =
sponsor:GetProperty(prop.id)`, `PreGameMission.lua:583-585`), and route 2 would
have destroyed it. ⛔ Missing number or raw `<cargo>` ⇒ **stop the sitting**.

### `C51` heading — the terraforming overview
⭐ **Where it actually is:** `TerraformingOverall` is opened by
`OpenPlanetaryView` (`Lua\PlanetaryView.lua:47-57`) — it is the heading on the
**planetary / Mars view**, the HUD's planetary-view button. ⚠️ It is opened
**only when the `NoTerraforming` game rule is off** (`:52`).
✅ **English: NO visible change** — that is the whole reading.
✅ **German: `TERRAFORMING-GESAMTFORTSCHRITT`.**

### `C51` rollover — the rocket's *Back to Earth* button
⛔ **The single most likely way this reading is missed.** `idBackToEarth` is
`SetVisible(available)` where
`available = IsPlayerControlled() and not arrival_loc and command == "CmdWaitOrder"
and working and not is_asteroid_lander and not g_Tutorial`
(`Lua\UniversalRocket.lua:2172-2177`), and the button carries
`FoldWhenHidden = true` (`customUniversalRocket.generated.lua:26`).
⇒ **The rocket must be a Universal Rocket landed on Mars and IDLE** — no
destination set, not loading, not launching, not an asteroid Lander. If the
button is not on the panel, cancel its flight first.
⚠️ **The log line fires at `Init`, whether or not the button ends up visible** —
so a `2 of 2 strings` line proves the patch ran, **not** that anyone saw it.
✅ **English: NO visible change.**
✅ **German: title `Zurück zur Erde`**, body the full German sentence (id
`316233855405`).

---

## 4 · ⛔ PRE-REGISTERED FINDING — `C50` has a FOURTH surface, it is IN-GAME, and the number there is predicted WRONG

Derived at `Src` during this link's preparation, before any launch. It is
recorded here as a **falsifiable prediction**, not as a verdict.

**The surface.** `PGMissionSummaryDlg` — the panel site 1's wrapper feeds — is
instantiated from **two** places, not one:

| instantiated at | when | reaches `GetSponsorSummary`? |
|---|---|---|
| `PGMissionSponsorRemastered.generated.lua:609` | pre-game sponsor screen | ✅ yes (site 1 as recorded) |
| `MissionProfileDlgRemastered.generated.lua:342` | ⛔ **IN-GAME** — HUD Goals button, `OpenDialog("MissionProfileDlgRemastered", …)`, `Lua\X\HUD.lua:283-288` | ✅ **yes, and this was not on record** |

Its context-update calls `GetSponsorSummary(entry)` whenever
`visible = (… id == "idMissionSponsor" …) and (MainCity or not
random_mission_params[id])` (`PGMissionSummaryDlg.generated.lua:108-120`).
In-game `MainCity` is truthy ⇒ **visible**. `g_CurrentMissionParams` survives the
save (`PreGameMission.lua:316, :321`), so the running game's sponsor entry is
live there.

⇒ ⛔ **`Fix_SpaceYDroneCapBullet.lua`'s header claim — *"All three sites are
pre-game screens"*, *"the sponsor's +20 shows once"* — is FALSE for site 1.**

**The number.** In a running game the sponsor's own modifier is already applied
to `g_Consts`: `Colony.lua:76` does `self:AddToLabel("Consts", g_Consts)`, and
`Effect_ModifyLabel:OnApplyEffect` sets a `Modifier` on every object in that
label (`MarsGameEffects.lua:161-172`). So on a **SpaceY colony**:

| | `base` = `g_Consts[Prop]` | `value` = `GetModifiedConsts(sponsor)[Prop]` | guard `value <= base` | bullet prints |
|---|---|---|---|---|
| pre-game | 20 | 20 + 20 = 40 | passes (40 > 20) | **40** ✅ |
| ⛔ in-game | **40** | 40 + 20 = **60** | ⛔ passes (60 > 40) — does **not** catch it | ⛔ **60** |

⛔ **PREDICTION: on a SpaceY colony, the in-game Mission Profile dialog shows
*"…control (60)"* while the real cap is 40** — the sponsor's own bonus counted
twice. The `value <= base` guard cannot catch this; it is satisfied by the very
double-count that causes it.

⚠️ **Vanilla does not have this problem on that panel.** SpaceY's own
`<cargo>` tag resolves from a sponsor **property**, not from a `Consts` label
prop, so vanilla's bullets are stable in-game. The skew is introduced by ours.

⚠️ **Scope of the consequence:** it is visible only to a player who is (a)
playing SpaceY and (b) opening the in-game Mission Profile. It is cosmetic and
touches no save (`§3a` Layer 3 is unaffected — the module still writes nothing).

⭐ **How the sitting falsifies it, on any save, in ~20 seconds** — the module
exposes `bullet_for` with a dedicated `probe` bucket precisely so it can be
driven without disturbing the three real sites:

```
*r local sp = table.find_value(MissionParams.idMissionSponsor.items, "id", "SpaceY")
   ModLog(g_Consts.CommandCenterMaxDrones)
   ModLog(_InternalTranslate(SMRFixPack.SpaceYDroneCapBullet.bullet_for(sp, "probe")))
```

⚠️ On a **non-SpaceY** save this prints `20` and `(40)` — which looks correct and
proves nothing about the double-count. It only bites where `g_Consts` already
carries the sponsor's own modifier. The decisive reading needs a **SpaceY
colony**, or the in-game Mission Profile opened on one.

---

## 4b · ⚖️ RULED AND BUILT, still before any launch — what §4 now predicts instead

**Owner ruling 2026-08-20 (checklist 61): fix it.** Chosen over ship-and-file and
over pulling `C50`. ⛔ §4 above is left exactly as written — it was the
pre-registration and it is not edited after the fact. This section is what
changed underneath it.

**The change** (`Code/Fix_SpaceYDroneCapBullet.lua`, parse-clean): `bullet_for`
declines while a game is running, keyed on `MainCity` — the game's own
pre-game/in-game discriminator on this very panel
(`PGMissionSummaryDlg.generated.lua:110`). Two header claims that this proved
false were corrected in place rather than quietly dropped.

⇒ **REVISED PREDICTIONS:**

* ✅ Pre-game (all three `C50` sites): **unchanged — the bullet, with 40.**
* ✅ In-game Goals / Mission Profile dialog on a **SpaceY** colony: **no bullet
  at all**, vanilla text, and one log line:
  `[CommunityFixPack] SpaceYDroneCapBullet: a game is running, so the Drone Hub capacity already includes SpaceY's own bonus and this bullet would count it twice — nothing was added (this repair is for the pre-game sponsor screens)`
* ⚠️ In-game on a **non-SpaceY** colony: **nothing at all, and no log line** —
  `ours(sponsor)` gates before `bullet_for` is ever reached.

⛔ **CONSEQUENCE FOR THE SITTING, AND IT MATTERS.** The owner's save (`C47FARM`)
is not a SpaceY colony, so *"open Goals and see no bullet"* would have been true
before the fix as well. **That check proves nothing there** and must not be
reported as if it did. The control that does work on any save, in ~20 seconds:

```
*r local sp = table.find_value(MissionParams.idMissionSponsor.items, "id", "SpaceY")
   ModLog(tostring(SMRFixPack.SpaceYDroneCapBullet.bullet_for(sp, "probe")))
   ModLog(SMRFixPack.SpaceYDroneCapBullet.stats.probe.reason)
```

✅ Expect **`nil`** and the running-game reason. Before the fix this printed a
rendered bullet. ⚠️ It drives the `probe` bucket, so it cannot disturb the three
real sites' counters.

**The probe was changed too** (`SMR-BugFixPack-TestKit`, separate repo, separate
commit — not shipped, not part of the 82-file pack). ⭐ **It had reproduced the
fix's own arithmetic** — clause 3 derives the number as
`g_Consts[PROP] + modifier.Amount`, exactly what `GetModifiedConsts` does — so it
agreed with the defect and reported PASS. It now branches on a running game and
asserts the stand-down instead, and clause 7 no longer reads a running-game
decline as a site that never worked. Probe count is unchanged at **98**.

⚠️ **What is still unproven and must not be claimed:** nobody has yet seen the
in-game panel on a SpaceY colony, before or after. The fix is argued from source
plus the console control above. Seeing it would need a SpaceY game started and
landed — out of the sitting's ruled bar unless the owner wants it.

## 5 · What a silent failure looks like, so it is not read as a pass

* ⛔ **Tags did not resolve** — literal `<drone_cap_help>` or
  `<CommandCenterMaxDrones>` on screen, a `{#4706}`-shaped token, or the sentence
  with an empty `()`. The form `T{"<tag> …", context}` appears **nowhere** in the
  shipped game (whole-tree `T{"<` → 0 hits), so this sitting is its first proof.
  **Report it verbatim; do not paraphrase.**
* ⛔ **Bullet present, number absent** — context bound, const read failed.
* ⛔ **Nothing at all, no log line** — the module never reached the site.
* ⛔ **Nothing at all, but a decline line in the log** — the module stood down on
  purpose; the reason is the evidence and it is the fix telling us the game is
  not shaped the way we read it.
* ⛔ **German step: English text on a German UI** — that is `EF-039` failing in
  the direction the project has never watched, and it retires that gap either
  way.

---

## 6 · Results — RAN 2026-08-20, attended, owner at the keyboard

⭐⭐ **BOTH FIXES WORK, AND BOTH WERE SEEN — including in German.** Two launches:
an English session (`link4en_…19.40.49`) and a German one (`link4de_…20.12.50`),
plus the language-change restart (`link4lang_…20.12.19`). All three archived and
`git add -f`'d; `docs/archive/` reconciles 105 tracked = 105 on disk, nothing
ignored-but-present.

### 6.1 · The readings, screen by screen

| # | reading | verdict |
|---|---|---|
| 1 | boot, both languages | ✅ **77 `applied`** (predicted 77, was 75); the single `inactive` is `SaintBlessing`, the standing pattern |
| 2 | `C50` sponsor **rollover**, EN | ✅ bullet present, **(40)** — the predicted number |
| 3 | `C50` **summary panel**, EN | ✅ same bullet, **(40)** |
| 4 | `C50` first bullet (the regression check), EN | ✅ `Dragon Rocket … (40,000)` intact |
| 5 | `C50` rollover + summary, **DE** | ✅ **`Maximale Anzahl an Drohnen, die ein Drohnen-Hub kontrollieren kann (40)`** — byte-for-byte the German the pack extraction predicted |
| 6 | `C50` in-game stand-down | ✅ console: `nil` + the running-game reason |
| 7 | `C51` heading, EN | ✅ **no visible change** — exactly the promise the site entry makes |
| 8 | `C51` heading, **DE** | ✅ **`TERRAFORMING-GESAMTFORTSCHRITT`** |
| 9 | `C51` rocket rollover, EN | ✅ no visible change |
| 10 | `C51` rocket rollover, **DE** | ✅ **`Zurück zur Erde`** / `Schicke die Rakete ohne Ressourcen direkt zurück zur Erde.` + log `2 of 2 strings` |
| 11 | suite (`SMRTest.RunAll()`) | ✅ **74 PASS · 0 FAIL · 24 SKIP · 0 ERROR** of 98 |

⭐ **The two `C50` sponsor readings are provably different code paths, not one
screen twice:** between the rollover and the summary, *Starting Rockets* moved
5 → 6 and *Research per Sol* 200 → 3,200 (commander + game rules, which only
`GetSponsorSummary` folds in) while **our number stayed 40 in both**. That is
also the live control on the module's decision to omit the commander when
computing the value — until today an argument from source.

### 6.2 · ⭐⭐ `EF-039`'s standing note is CLOSED, positively

*"No leg has watched a shipped-id string render in a non-English language"* —
discharged twice over in one sitting: `C50`'s **borrowed** id 4706 rendered German
(row 5), and `C51`'s **repointed** ids rendered German (rows 8, 10). ⭐ Row 8 is
the strongest single proof in the sitting: the terraforming heading is a raw Lua
string with no id and no `Translate` flag in vanilla, so there is **no path** by
which it becomes German on its own. It is German because of our code.

⭐ And the suite independently confirmed the defect is real, in German:
> *the XDef's own unenrolled id still falls back to its embedded English
> ('Back to Earth'), which is what a player sees today*

### 6.3 · ⛔ Code changed DURING the sitting — three times, and why

| # | change | who ruled it | verified by |
|---|---|---|---|
| 1 | `C50` stands down in a running game | ⚖️ **owner, checklist 61** | row 6 + the wave-13 probe's stand-down clause |
| 2 | `C51` finds the button with `XWindow:ResolveId` | fence §4 (the sitting found the fix broken) | row 10 |
| 3 | `C51` install loop over six rocket classes | same | ⚠️ **repaired nothing — see below** |

⛔ **Change 3 was built on a conclusion that was WRONG, and the verifying run is
what said so.** From `stats.rocket` reading `0/1` this session concluded the five
rocket subclasses each carry their own composed `Init` and that a parent wrapper
never reaches them. The verifying boot logged `wrapped on 1 rocket class(es):
customUniversalRocket` — the subclasses are **absent from `_G` at apply time**, so
only the parent was ever wrapped — **and the Zeus rocket patched anyway.** ⇒ the
parent wrapper does reach subclass panels; `0/1` was a thin count with a story
read into it. **Change 2 alone was the repair.**

⚠️ The loop is kept **because it is precisely the code that was verified**, and
its rationale comment is rewritten to say the above rather than the false claim.
⛔ **Comments only were edited after verification — the runtime code is
byte-identical to what rows 1-11 measured.**

⚠️ **A conclusion this session nearly acted on:** with change 3 apparently having
failed, the recommendation put to the owner was to **cut `C51`'s rocket half and
ship heading-only**. The owner's next screenshot showed `Zurück zur Erde`. ⇒ a
working fix was one message from being cut on a bad inference. Recorded because
the near-miss is the lesson, not the outcome.

⭐ **The method that actually resolved it was the owner's, not this session's.**
Asked why the cause could not be *watched* instead of reasoned about, a console
tracer on all six classes produced `kids=5 resolve=InfopanelButton
title=885571832096` in one shot — which killed the direct-child assumption,
proved `ResolveId` reaches the control, and confirmed the ids were unrepaired.
Three static readings had been wrong; the first measurement was right.

### 6.4 · ⛔ NOT observed — by name, never as a pass

- ⛔ **`C50`'s third render site, the challenge landing-spot screen.** Never
  opened. The probe confirms *"all three install points hold a wrapper"*, and
  checklist 59 (owner-ruled) makes looking optional — but **no human has seen
  that screen** and this entry does not claim otherwise.
- ⛔ **The in-game Mission Profile panel on a SpaceY colony.** The stand-down is
  proven by console and probe; the *screen* was never opened on a SpaceY game.
  `C47FARM` is a **USA** colony (`logo: USA`), which is why the "open Goals and
  see no bullet" check was withdrawn — it would have looked identical either way.
- ⚠️ **Step ⑥, the English restore, has no fresh-boot log.** The owner reported
  switching back and confirming; the game was closed without a further launch, so
  there is **no logged English session after the switch**. English was the
  sitting's starting state and was fully observed at rows 2-4, 7, 9; this is a
  tidy-up step, not a fix reading. Recorded as reported, not as observed.

### 6.5 · The whole log, attributed — nothing discounted

- ⚠️ **`[LUA ERROR] … attempt to call a nil value (global 'unpack')`** in
  `link4en_`. ⛔ **THIS IS THIS SESSION'S OWN CONSOLE SNIPPET, NOT THE PACK.**
  `unpack` is nil in the mod sandbox; the tracer used it. It was contained by the
  engine's `procall`, fired *after* its useful readings, and no pack file
  contains the word. ⛔ **The audit must not read it as pack behaviour.**
- ⚠️ `[ResManager Error] … LawOfficeDoor_opening.hgacl` / `_idle.hgacl`, both
  sessions — **vanilla's own missing animation asset.** Cannot be ours: the pack
  ships no assets at all (82 files, all Lua + metadata + LICENSE + preview).
- ⚠️ `This savegame tries to load … Opt-In Modules … present, but not loaded` —
  **expected**: `C47FARM` was saved with the opt-in pack on and it is deliberately
  unticked (checklist 43).
- ⚠️ `[Braze] SessionStart error …` ×6 — the game's telemetry client with no
  network. Present in every log this project has ever taken.
- ⚠️ `[SMRTest] no debug.getinfo (mod sandbox)` — standing, and the reason 8 of
  the 24 suite skips are skips.

### 6.6 · Suite — the store card's number is now measured

**`74 PASS · 0 FAIL · 24 SKIP · 0 ERROR`** = **98**, in German, on a loaded save.
⇒ checklist 60 is discharged: the card's *"an automated suite of 98 checks"* is
no longer an unmeasured claim. Prior reading was `80/0/16/0` of 96 (08-15).

⚠️ **The +8 skips are configuration, not regression**, and every one is named:
8 retail-sandbox introspection · 8 opt-in mod absent · 6 save-rescue mod absent ·
1 tech with no description `T` · 1 undeclared stub target. **24 accounted for,
0 unexplained.**

⚠️ **One wording flaw found in the `LocalizedUIText` probe, for link 5.** It
reports *"a later mod has chained on top of ours on TerraformingOverall,
customUniversalRocket — legitimate"*. **No later mod exists here**; the live
`Init` is simply not the raw function either party assigned, because the class
builder composes it. The probe is right to pass, but its explanation names a
cause that is not the cause. Not fixed here — it is a message, not a verdict.

### 6.7 · Rig state at close

✅ `EF-056` discharged both ways: pre-copied before the first launch, and
reconciled by name after the last — `Autosave Sol 406` (56,195,934 B) and
`Autosave Sol 411` (56,195,463 B) present, byte-identical to the held copies.
**Nothing was lost.** `C47FARM` untouched (mtime still 2026-08-15).
⚠️ Cheats and both mods are the rig's normal config; no reading above intersects
anything a cheat changed.
