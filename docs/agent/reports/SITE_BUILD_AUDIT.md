# Site build — sweep and arbitration ledger

**Written 2026-08-13 by `agent/prompts/public-docs/05_BUILD_SITE.md`** (the site
build), in the pattern `STORE_BUILD_AUDIT.md` set for the store build. The
artifact this ledger is about lives in a different repo: the site is
`C:\Dev\SMR-CommunityMods` (`catt144/SMR-CommunityMods`, public, **nothing on the
web** — `workflow_dispatch` only, Pages OFF).

> ⚠️ **This is a report, and reports are not authority.** Where it disagrees with
> an `agent/bugs/` entry, an `agent/facts/` fact or the shipped code, they win.
> Every count was re-emitted with `--emit-counts` at the moment it was used.

## What was built

| page | what it is |
|---|---|
| `content/index.md` | the landing page — the three install-gating answers, then which mod is which |
| `content/install.md` | installing, the full-restart rule, what each mod puts in a save (by name), the optional pack's switches, load order, console/gamepad, "checking it is working" |
| `content/fix-list.md` | ⭐ **the searchable fix list** — 74 registered modules, nine sections, every entry folded, three beats each, the five judgment calls labelled |
| `content/faq.md` | the FAQ, opening with **job 4's hostile-reader section** (checklist 22c: *is it you · how do I get you out · where do I tell you*) |
| `content/for-modders.md` | ⭐ **new page** — the identifier-carrying per-fix disable instructions, and design hole 3 (load order) answered honestly |
| `mkdocs.yml` | nav extended for the new page; **one pre-existing defect fixed** (below) |

**Counts re-emitted at write time (2026-08-13):** fix pack 74 registered modules
(74 default-active), 75 `Code/*.lua`, 94 probes, 103 F + 12 D + 46 C rows;
opt-in 8 registered (1 default-active, 7 optional), 9 `Code/*.lua`, same 94-probe
shared kit. ⛔ No count appears in tier 0 or tier 1 of any page, and no
exposed-set count appears anywhere in any form.

---

## ⛔ Findings the WRITE caught, before any sweep ran

These are recorded first because all three are the same failure the `F76`
precedent exists to prevent — **a player-facing page describing a fix that does
not ship** — and all three came out of checking the frozen file's bullets against
the registered module list rather than against prose.

| # | finding | evidence | disposition |
|---|---|---|---|
| W1 | ⛔⛔ **`MOD_DESCRIPTION.md` promises a fix for dome plumbing that was DELETED.** Its bullet *"Domes clean up properly when they grow over a building… stale plumbing behind that a repair pass re-ran on every load"* describes `F24`, closed **wontfix 2026-07-30** with `Code/Fix_DomePipeMoveInside.lua` deleted and removed from `metadata.lua` | `docs/agent/bugs/F24.md:14`; no `Fix_DomePipe*` in `Code/`; `Register(` grep returns 74 modules, none of them this | **struck from the site before it was written down.** ⛔ The frozen file's bullet is a live false claim and is now on record as one |
| W2 | ⛔⛔ **The same file promises the research-counter fix, also DELETED.** *"swapping one researched technology for another keeps the research counters straight"* describes `F28`, closed **wontfix 2026-07-30** (reachable only from mod code, barred by `FIX_POLICY` §4a), `Code/Fix_ReplaceTechCount.lua` deleted | `docs/agent/bugs/F28.md:14` | **struck.** It had already been drafted into the site's "Under the hood" section and was removed; that section is three entries, not four |
| W3 | ⛔⛔ **The sensor-tower claim is BACKWARDS in every record that carries it.** The frozen file says *"Sensor Towers now genuinely delay strikes instead of accidentally making things worse"*; the site's own layout specimens said *"made meteors MORE frequent instead of less"*; `PUBLIC_DOCS_DESIGN.md` §4.3 uses that as its worked search example. **The code says the opposite:** the interval was `Min(spawn_time, warning_time)`, towers ADD warning time, so towers *lengthened* the interval — `F02.md:30-38` states it outright: *"towers **accidentally repair the cadence**… the players actually harmed are early colonies with no Sensor Towers"* | `Code/Fix_MeteorFrequency.lua:6-14`; `docs/agent/bugs/F02.md:30-38`, `:105-107` | **the site says the true thing**, in the meteor entry's *Worth knowing* beat: towers were accidentally papering over the fault, and after the fix the schedule is the same with towers or without. ⚠️ It never reached either store card (neither mentions Sensor Towers), so nothing shipped is wrong — but three of our own records still carry it |

⭐ **The pattern, stated for the next build:** all three were found the same way —
by refusing to write a player sentence from the frozen file's bullet and instead
asking *which registered module delivers this?* Two had no module at all. That
question is cheap and it is the one the six store sweeps did not ask.

## ⛔ A fourth finding — the site scaffold could never have built

`mkdocs.yml:33` read

```
site_description: Bug fixes and optional modules for Surviving Mars: Relaunched.
```

The unquoted value contains `: `, which is a YAML mapping delimiter. **Every
`mkdocs build` fails at the config parse**, so the scaffold committed on
2026-08-13 — and the CI workflow that builds it — had never been run and could
never have succeeded. Fixed by quoting the value. The whole site now builds under
`--strict`.

⚠️ **What that says about the specimens:** the four specimen pages were written,
reviewed and committed without anyone building them once. Local preview costs one
`pip install` and eleven seconds.

## ⭐ A measurement, taken because the design asserted it

`PUBLIC_DOCS_DESIGN.md` §4.3 says entries are collapsed *"and search expands the
match"*. **Measured on the real build** (`mkdocs build`, then reading
`site/search/search_index.json`):

* ✅ **The folded text IS indexed** — searching *Sensor Towers* or *suffocate*
  finds content that is inside a closed `???` block.
* ⛔ **Search does NOT expand the entry.** The index is sectioned by heading, so a
  hit resolves to `fix-list/#disasters-weather` — the reader lands on the category
  with every entry still folded.

⇒ The page now says exactly that: search takes you to the section, the titles are
all visible while folded, and the last click is the reader's. ⛔ No surface claims
the entry opens itself.

---

## The sweeps

Eight one-rule sweeps, each firewalled from the others and from this ledger, each
told to report evidence rather than opinions. Two of them were pointed at the
CODE rather than at the entries, which is where the terminal audit said the store
build's six sweeps under-swept.

| # | rule swept | scope |
|---|---|---|
| 1 | player language (rule 4) | all five pages |
| 2 | unearned claims / vocabulary (rule 6, §4.5), incl. every "you can X" route | all five pages |
| 3 | ⭐ fix-list entries **against the module code**, first three sections | `Code/Fix_*.lua` |
| 4 | ⭐ fix-list entries **against the module code**, remaining six sections | `Code/Fix_*.lua`, `90_SaveSanitizer.lua` |
| 5 | ⭐ every opt-in claim **against the opt-in mod's own code** | `SMR-OptInPack/Code/` |
| 6 | holes, unpublished state, broken anchors, the rescue artifact, exposed-set counts | site repo |
| 7 | site against the two store cards — contradiction, escalation, silent omission | both card texts |
| 8 | coverage both ways: 74 modules ↔ entries; retired work; exactly five judgment calls | `Code/`, `bugs/INDEX.md` |

All eight returned. **44 findings raised, 31 accepted and fixed, 5 accepted and
routed, 8 refused.** Every accepted finding was re-derived by the arbitrator from
the code or the entry before it was applied; every refusal names what the sweep
missed.

### ⛔ The four that matter — accepted, and each one is the same failure family

| # | finding | re-derivation | what changed |
|---|---|---|---|
| S1 | ⛔⛔ **The fix-list entry for the Underground Medium Dome description advertised a repair that reaches nobody.** `F98` (filed, SOURCE-VERIFIED **and live-confirmed**) records that `Fix_TechDescriptionBuilding.lua:75` assigns `T(841885693955, CORRECTED)`, and in a retail build `T()` returns a light userdata carrying only the id, discarding our literal (`localization.lua:250-252`); the 2026-08-02 console control returned `userdata` | read `F98.md:14-40` and the module's line 75 myself; the assignment writes back exactly what was already there, in every language | **the entry is PULLED from the page.** The module still ships and still reports itself patched — that is a code question the owner has already deferred with D10's localisation work — but a player-facing list may not carry it. ⇒ the page now describes **73** of the 74 registered modules, deliberately |
| S2 | **`F13`'s cause was wrong on the page — and it came from the design report's own specimen** (`PUBLIC_DOCS_DESIGN.md` §5.5: *"the numbers were being drawn, but not where you could see them"*) | `Fix_CommandCenterNumbers.lua:1-15`: eleven per-resource getters **do not exist** after the remaster's refactor; a nil makes `FormatResource` produce nothing | rewritten to what the code says — the rows ask for eleven numbers and nothing answers |
| S3 | **`F30`'s "After the fix" described the opposite mechanism.** Page said the ground is cleared of units *before* it drops | `Fix_LakeEntombment.lua:16-24` — a **post**-wrapper on `PlacePrefab`, *"the exact point after `map:RebuildPassability` where the basin exists"*, then `SetCommand("ExitImpassable")` | rewritten: units are sent out once the basin exists, using the game's own escape behaviour |
| S4 | **`F57(a)` was written with an invented symptom.** The page said *"drone work quietly restricted with no rocket in sight"* | `Fix_DroneTransportMinors.lua:56-63` — *"**Latent as the game ships.** `FuelResource` … no assignment anywhere in `ModTools\Src` … Tier R3 — latent by DATA"* | moved to **Under the hood** and rewritten as a latent defect nobody can have seen. ⭐ This is the `F76` failure in miniature: a plausible symptom sentence with no witness behind it |

### Accepted and fixed — the rest, by sweep

* **Sweep 3 (code, first half).** `F17` — flat 10 is the **mid** of a 5–14 spread, not the maximum (the module's own registry title says "maximum" and contradicts its header; the header and `F17.md:22-24` agree with each other) · `F73` — the module fixes **two** things and the page claimed one, and a life-support blip un-homes residents *while it lasts*, not "for good" · `F01` — it checks the **game rule**, not "the map's disaster setting" · `F77` — "the fleet keeps working" overstated; the debounced pass still costs one interruption · `F57(b)` — "drones passing over work" is an inference the module explicitly declines to make (*"no crash is asserted… what is fixed is the state left behind"*) · **four undisclosed save repairs now disclosed** (`F81b` rains loop revival, `F92` saint re-basing, `F95` astrogeologist back-application, `F44` orphan clearing).
* **Sweep 4 (code, second half).** `F48` — the page claimed guards the pass does not have; `90_SaveSanitizer.lua:255-277` walks **every** track with elements under a `pcall`, and the header's own PT-37 record says `OrderTrackElements` *succeeds* on meteor-damaged track. Rewritten to what it really does, including "if one refuses to be walked, that track is left as the game restored it" · `F46` — two deliberate carve-outs (no station on the route accepts it; a train on its way to be stored) now stated · `F29(b)` — not "mishandles objects": a broken two-variable swap of two timing values · `F18` — undisclosed load-time correction of the stored discount, now disclosed · `F67` — vanilla's one-sol departure timer still fires, so empty trips are reduced, not eliminated · `F83` — a player who already opened the dead notification cannot be healed · `F12` — "never fired since the remaster" is not derivable from the code; now "could never fire".
* **Sweep 8 (coverage).** `F15` — `Fix_WispRewards.lua` ships **two** fixes and the page carried one; the destroyed-wisp double payment (200 RP paid against a notification saying 100, `:8-14`, fix at `:40-46`) now has its own entry.
* **Sweep 5 (opt-in code).** *"listed on its own page"* pointed at a page that does not exist · *"every module has a switch"* ×3 — `DroneStatDials` has **no** toggle, it is two dropdowns and registers without `optional` · *"everything is off"* ×2 — seven off, two dials at base · the dial-reset recipe needed its **precondition**: `Opt_DroneStatDials.lua:114-117` returns early when there is no colony, so doing it at the main menu clears nothing · the Apply distinction between dials and toggles is not real — `00_Core.lua:400` gates both · ⭐ **the opt-in mod's persisted fields carry the FIX PACK's prefix** (`SMRFixPack_ack_notworking`, `SMRFixPack_no_homeless`, …), kept byte-identical across the split, so the modders page's "named after the mod that writes them" was wrong in the one place a modder would act on it.
* **Sweep 7 (site vs cards).** The *"means nothing to the game without it"* blanket was reproduced on two pages **without** the card's *"one item is deliberately not inert"* qualifier — the worst omission found, because it is the one fix-pack write that survives uninstall · the console sentence in the FAQ flatly contradicted the modders page · *"PC-only because it needs another mod"* — consoles install mods; what is PC-only is **authoring** one · the Retirement-Dome policy line dropped **unemployed**, which the card is emphatic about · the re-nag interval was given in real minutes; it is **four game hours** (`D02`, measured in PT-38), which is minutes at 1× and seconds at high speed.
* **Sweeps 1 and 2 (language, claims).** "self-check" ×2 and "sweep" ×2 replaced with plain words · "Mystery 10" replaced with the mystery's name · the install page's "checking it is working" section rewritten so it stops reading as a note between developers · "hooks" ×2 replaced · *"that is what makes it coexist"* softened to the effort rather than the outcome · *"the one route that exists"* now says it has a part we cannot tell you how to do · the modders page's *"nothing of ours in the game"* corrected (it **is** registered and marked disabled) · the stand-down dialog's timing made precise (once, at the main menu, next start) · the dismissed-warnings history reduced to what `F32` actually establishes (the game's own data was missing the setting; the developers put it back).

### Accepted → routed, not applied here

| # | finding | why routed |
|---|---|---|
| R1 | ⛔ **The FIX PACK'S STORE CARD still overstates patch-retirement.** `STORE_FIXPACK.md:71-74` — *"an official patch that changes the code a fix was written for **retires our version of it**"*. Our own core says the opposite of the general case: `00_Core.lua:492-497` — *"self-checks … CANNOT notice a same-named function edited in place"* | This is checklist **22d item 1** incompletely landed: the conditional was narrowed to "changes the code", and a body rewrite *is* a change to the code. ⛔ **Not edited here** — it is owner-approved text in another surface's file. Prompt 6 reads both surfaces and owns this |
| R2 | `Fix_TechDescriptionBuilding` ships and reports `patched` while being a retail no-op (S1) | code + owner decision, not a page: the repair is `ModItemLocTable` work already scheduled post-release with D10 |
| R3 | Where bug reports go | checklist item 27 — ✅ **CLOSED the same session: comments first, the issue tracker named once for reports carrying a save or a log.** Written into `faq.md`; the store-page link stays a hole |
| R4 | The screenshot fixtures that cannot be seen from outside the game | `CAPTURE_SITTING.md`, amended in place with drop rules |
| R5 | `F22` has no fix-list entry of its own — it is described inside the Last Transmission entry, so a modder searching "power reserve" will not find it | deliberate for now; noted for prompt 6 to rule on |

### Refused — and what each sweep missed

| # | finding | refusal |
|---|---|---|
| X1 | *"safe to add or remove at any time" is an unearned absolute* | `PUBLIC_DOCS_DESIGN.md` §4.5 lists this exact phrase as ✅ ALLOWED: it says **built to be**, which is a design claim. The card ships it verbatim |
| X2 | *the achievements claim is not covered by the evidence bar* | source-cited: `Achievement.lua:61-63` returns true on exactly `playstation or xbox or windows_store`, consumed `:77`. The negative half (Steam unaffected) is the same line read the other way |
| X3 | *"you can build replacement trains at any station for Metals and Electronics" needs a route check* | it had one — the store build's sweep 4 walked it (`customStation.generated.lua:14-29`, `Station.lua:628-634`); the site quotes the card verbatim |
| X4 | *the `%AppData%` log path and Ctrl+F1 are unverified* | the path exists on this machine (listed today); the rest is the arbitrated card text |
| X5 | *"four things" in the opt-in save list is an exposed-set count* | the ban is on the **fix pack's** exposed-set derivation. The opt-in card's "four small things" is an enumeration that shipped through six sweeps and the terminal audit |
| X6 | *"in either the original or the remaster" claims knowledge of the original game* | it has it — `F97.md:407-421`, the OG disassembly, which the 22b strike re-derived |
| X7 | *the dust-devil entry's "heaviest setting" is heaviest by name, not by mean* | true of the arithmetic, but "heaviest shipped preset" is the card's own re-derived phrasing and the owner-approved frame; changing it on the site alone would create the drift this sweep exists to catch |
| X8 | *the Philosopher's Stone entry should carry an `F103` caveat* | `F103` is a post-release WATCH with **harm nil** and one consumer that wants the message. A player-facing caveat about a harmless duplicate broadcast is noise |

## Prompt 6 — the terminal audit's dispositions (2026-08-14, `06_AUDIT.md`, chain closed)

**The control ran first and firewalled** — the "which shipped module delivers
this?" question over the store cards and the site prose, with this ledger unread
until the pass returned. **Verdict: CLEAN — no new false claim found.** Every
chased claim resolved to a shipped module whose own header says what the page
says, including the ones this ledger corrected (S2's eleven getters, S4's latent
restrictor at `Fix_DroneTransportMinors.lua:45-63`, F48 delivered by
`90_SaveSanitizer.lua:170-`, the F35 restore living in the sanitizer, the
one-wave `SMRFixPack_spawn_gate` behind "holds one decision for as long as a
single weather event lasts", the veto/ListFixes/stand-down mechanics in both
cores, all eight `Opt_*` headers). The two per-call veto re-readers the modders
page calls "a small number" are exactly two (`Fix_DustDevilSpawnGate`,
`Fix_MeteorFrequency`).

**Re-derived at audit time, none inherited:** counts 74/75/94 + 103F/12D/46C and
opt-in 8 (1 default-active) via `--emit-counts` both repos · `mkdocs build
--strict` GREEN · both issue trackers live-verified open via the GitHub API
(`has_issues: true`, public, unarchived — checklist 27's ground truth) ·
exposure gate intact (`docs_dir: content`, CI guard's own greps re-run locally
and passing, dispatch-only, content/ = exactly the five pages, `site/`
gitignored) · both open hedges verified still open at source
(`COMBINED_SITTING.md:367` console question; toggle-flip pass C untaken,
`CAPTURE_SITTING.md` unconsumed) — and verified the pages claim log-only and
say "we have not confirmed" in the right places.

| item | disposition |
|---|---|
| **R1** | ✅ **APPLIED** to `STORE_FIXPACK.md` (both occurrences → "changes the **shape** of the code"; tier 1 carries the two-sentence honest limit). Licence 22d(1) + 22b; record in that file's notes. `metadata.lua` keeps its 22d(1)-approved conditional — awareness, not a defect |
| **R5** | ⚖️ **RULED: leave folded.** The Last Transmission entry carries the storage-figure half a player can meet; the general half's audience is a storybit modder, and the fix list is a player surface. This ledger is the record |
| no opt-in module page on the site | ⚖️ **RULED: not a launch gap.** The store card is the canonical module surface and the site describes modules where a question needs them; duplicating eight module blocks is a second surface to keep true for no reader who lacks one. Revisit only if post-launch questions outgrow the card |
| workflow header comment | fixed in the site repo — it still called content/ "LAYOUT SPECIMENS", which stopped being true on 2026-08-13 and would have misled the owner at publish time |
| X1–X8 | **all eight refusals SUSTAINED** (X2 and X3 independently re-walked in code during the control) |

**Raised by this audit's player reading and REFUSED, with the reasons on record:**

* *"written out by name" vs the fourth bullet's "handful of small stamps and
  flags"* (landing, installing, tier 1) — refused: literal names for the tail
  are the pack's internal identifiers, which the player-language gate bars from
  every surface; "by name" here means itemised rather than waved at, the
  construction shipped through the store build's six sweeps plus its terminal
  audit, and re-wording the site alone would create the card/site drift sweep 7
  exists to catch.
* *the FAQ's one-test ("if the problem is still there, it is not a mod, ours
  included") has a counterexample in the dial residue* — refused: the residue is
  a boost, which cannot present as the problem a player is debugging; the
  engine's mod-reference notice (the other survivor of the test) is answered in
  the very next paragraph; and the dial warning box sits on the same page.

**Routed onward (nothing new owed by the owner):** the stale *"Options → Mod
Options → Community Fix Pack"* path in `Opt_DroneOverhaul.lua`'s header comment
stays with release prep's copy-in (already recorded in `STORE_OPTIN.md` "Owed
elsewhere") · portal character limits for both `metadata.lua` strings stay with
release prep (`STORE_METADATA_STRINGS.md`).

### ⚠️ Deliberate calls a later reader should not mistake for oversights

1. **The page covers 73 of 74 registered modules** (S1). Nothing on the page states a module count, so nothing on the page is now false; the ledger is the record. ⭐ **2026-08-15: 75 of 76** — see the dated note below.
2. **Nine categories on the site against the card's seven lines.** The card merges story with interface; the site splits them and adds *Under the hood*. All nine buckets hold ≥4 entries, re-derived at write time, so §4.3's merge rule is satisfied.
3. **"Under the hood" is on the player page at all.** Four invisible repairs, labelled as invisible, with the reason they are in scope. The alternative — silence — reads as a shorter fix list than the mod delivers.
4. **The search behaviour is described, not promised.** See the measurement above.
5. **The console/controller routes are source-derived and still not play-verified** — the same standing gap the terminal audit noted for the cards. The combined sitting is where it closes.

## 2026-08-15 — two entries added by the `unattended-3` terminal audit (F85 + C39)

The two modules that chain shipped (`Fix_DistressPopupPause`,
`Fix_AutomationLawCompensation`) land on the fix list, and the counts this
ledger records move with them:

* **Coverage: 75 of 76 registered modules** (was 73 of 74; the F98 exclusion is
  unchanged and still deliberate). Modules re-emitted with `--emit-counts` at
  edit time. Neither player page states a count, so nothing on a page went
  false in the interim; this note is the record.
* **Fix-list entries: 78** (76 + the two). C39 → *Buildings & economy*
  (`success`); F85 → *Story & mysteries* (`question`, marked *judgment call*).
* **Judgment calls: SIX** (was five) — settled ONE way across card, `metadata.lua`
  `description`, site FAQ and fix list; reasoning in `STORE_FIXPACK.md`'s
  2026-08-15 note. FAQ updated in all three places it counts them ("Five other
  judgment calls" bullet + a new Automation bullet under *Things we do on
  purpose*; "Three honest notes" under *Does this change game balance?*; "Six:"
  under *Which fixes are judgment calls?*).
* **Shipped-module control, firewalled:** every sentence in both new entries and
  the FAQ additions was derived from Src/module reads taken BEFORE the entries'
  own reasoning was read this session (drafts pinned to the session scratchpad
  first). Building names are DISPLAY names re-read at the templates —
  ⛔ `BottomlessPitResearchCenter` displays as **"Experiment 1: Big Drop"**;
  "Bottomless Pit" appears nowhere on a player surface.
* **Honest-limit lines carried into the entries:** C39 — "we measured one
  building type live … the others follow the same verified rule in the code"
  (one family MEASURED, seven SOURCE, per the entry); the at-most-one-policy
  blast-radius fact (engine-enforced, `LawDef:Activate`). F85 — no screen
  claim anywhere: the entry describes what the code now does; nobody watched a
  clock, and the wording never says anyone did.
* `mkdocs build --strict` GREEN after the edits (1.4 s, no warnings).

## ⛔ 2026-08-15 (later, same day) — the F85 entry is REMOVED again, with its module (owner ruling, checklist 31)

The section immediately above recorded adding two fix-list entries. **One of
them came straight back out**, hours later, on the owner's ruling: the F85
`Fix_DistressPopupPause` module was removed from the pack because the dialog it
pauses is dead-coded out of the retail build — `DistressCallPopup`'s only caller
sits behind a literal `local cond = false`
(`Lua\XDef\POIAdditionalContent.generated.lua:89-111`), so no player can raise
it and the fix could never fire. Derivation: `agent/bugs/F85.md` §2026-08-15
(later); shelf record: `SHELVED_F85_DISTRESS_PAUSE.md`.

⚠️ **Why the entry was wrong quite apart from the removal, and it is worth
keeping on the record:** it opened **"What you saw:"** and then described the
clock running behind a window nobody can open. That is the item-29 class exactly
— a claim about what a player *sees*, resting on a mechanism that is real in
source and absent from the retail screen. It passed the build pass, the site's
own review and this ledger's firewalled shipped-module control, all of which
confirmed the *mechanism* and none of which walked the *route*.

**Counts as they now stand** (re-emitted with `--emit-counts` after the removal,
never inherited from the block above):

* **Coverage: 74 of 75 registered modules** (F98 exclusion unchanged and still
  deliberate).
* **Fix-list entries: 77** (78 − the F85 entry).
* **Judgment calls: FIVE** (five → six → back to five in one day). Swept the
  same way it was set, in all three FAQ places plus the card, `metadata.lua`
  `description`, and `STORE_FIXPACK.md`'s trace rows: the *"Five other judgment
  calls"* bullet is now *"Four other judgment calls … All five"*, and *"Six:"*
  under **Which fixes are judgment calls?** is now *"Five:"* with the
  distress-call clause deleted. ⛔ The C39 Automation bullet added in the same
  session is untouched — that module ships.
* **Suite: 95 checks** (96 − the F85 probe), on both the card and its source.
* `mkdocs build --strict` **GREEN** after these edits, no warnings; `site/`
  build artefact removed again (it is not committed).

⭐ **If the module is ever re-applied** (`SHELVED_F85_DISTRESS_PAUSE.md` §2 has
the re-arm trigger), every count above moves back by one and the fix-list entry
must be **rewritten, not restored** — the struck text's "What you saw" framing
was never true and would not become true just because the feature came back.
