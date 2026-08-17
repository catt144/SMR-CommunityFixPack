# Release description — Save Rescue (⛔ CONDITIONAL: this may never be posted)

**Assembled 2026-08-14 by `agent/prompts/release-3/01_BUILD_DESCRIPTIONS.md`,
Job 1's "+1".**

✅ **RULED 2026-08-14 (checklist 17): NOT published at launch — held in reserve.**
The owner's word: hold off publishing, and launch it **if post-release reports
show players stuck with the problem it solves**. Both other cards stand without
it (the opt-in card's fill-in was deleted per its default). ℹ️ *2026-08-17
solo-launch note: this card's opt-in mentions are deliberately NOT parked — the
contingency that publishes this tool is dial residue, which only the opt-in
mod's dials can create, so in every world where this card ships the opt-in mod
is already live and the mentions are correct.* **This file is the
ready draft for that contingency** — if the day comes, item 28 (the dialog text,
plus the audit's save-step line) is decided then, before upload. Item 28 was
closed "ship as built" by the same ruling.

⭐ **PRE-UPLOAD CHECKLIST for that day, owner-ruled, do not skip:**
1. ✅✅ **Display name "Relaunched Fix Pack: Save Rescue" — ALREADY APPLIED
   2026-08-17**, ahead of any publish (the family-prefix form the owner
   pre-approved 2026-08-15, checklist 26: *"This is fine for if we ever need
   it"* — ruled then as "Community Fix Pack: Save Rescue"; the family was
   renamed Community → Relaunched and the owner ruled "rename them now" the
   same day, checklist 36; `metadata.lua` `title` edited in its repo) — so the
   three mods sort together, as the opt-in pack already does. ⛔ Still owed at
   publish: this mod's `description`/`short_description` still name the old
   family — sweep them then, along with this card and every player-visible
   string. ⛔ Mod id / global / log tag are save contract and do NOT change.
2. Re-decide item 28's dialog text (the drone-dial line buried third of six).
3. Add the audit's **save-step** sentence to the on-screen dialog string — the
   "load once … delete it again" flow never tells the player to SAVE, and only
   their save writes the clean pass into the file. Fixed everywhere else
   already; the code string is the one surface left.
4. Items 2+3 are one re-witness launch together, per item 28's ruling.

⭐ **This is assembly, not authorship.** Every sentence below already existed, in
an already-written player-facing string or an already-verified statement. The
per-sentence trace is at the bottom, and ⚠️ **prompt 2 re-runs the shipped-module
control over all of it regardless** — this whole file is non-card text, which is
the exact class that inherits its sources' defects (`STORE_METADATA_STRINGS.md`'s
recorded lesson).

⛔ **Not published. Rule 5.**

---

## The two fill-ins

| n | where | needs | if it does not exist yet |
|---|---|---|---|
| **1** | "When you need this" | **store links** to the two pack mods | delete the marker; both mods are named in the sentence already |
| **2** | "Where the list comes from" | site link | delete the marker line |

⚠️ **Site link (2)** wants `content/install.md`'s *"What it puts in your save"*
section — `install/#what-it-puts-in-your-save`, verified to exist in the built
tree — under the site root **GitHub prints on the Pages settings screen**. Pages
is OFF and the publish workflow is `workflow_dispatch`-only.

---

═══════════════════════════ PLAYER TEXT — BEGIN ═══════════════════════════

## Save Rescue — Surviving Mars: Relaunched

A one-shot cleanup tool for savegames that were played with the **Relaunched
Fix Pack** or the **Relaunched Fix Pack: Opt-In Modules** and then lost them. Load
your save once, read what it tells you, save your game, and you can delete it
again.

**Install it only after you have uninstalled those mods.** An installed mod
cleans up after itself, so this tool only removes what a mod that is gone left
behind — and if the mods are still installed and there is nothing for it to do,
it says so once.

### When you need this — and when you do not

Almost everything those mods leave in a save is inert once they are gone: a few
timestamps and flags that nothing reads any more. If that is all your save has,
you do not need this tool, and a save that has nothing to clean gets no message
at all.

**One thing is not inert.** A drone speed or carry dial that was left off its
base setting is stored in your save as one of the game's own bonuses, under the
mod's name — so with the mod uninstalled your drones keep the boost and there is
nothing left in the game to take it off. **That is the reason this tool exists.**
If you set both dials back to base and saved before you uninstalled, that is
already dealt with and you need nothing further.
>>> FILL-IN 1 — store links to the two pack mods, or DELETE THIS LINE <<<

### What it does when you load a save

- **It removes only entries it can name.** There is no pattern matching and no
  guessing: the list is fixed, and anything not on it is left alone.
- **It never deletes a repair.** The Fix Pack repairs a real defect in the game's
  Large Wind Turbine tech bonus, and that repair *lives in your save*. Removing
  it would bring the bug back permanently with no mod left to redo it — so this
  tool keeps it, and tells you on screen that it kept it.
- **For saves that lost an older build of the Fix Pack**, it also puts two things
  back on the game's own machinery: a meteor timer that was left dead, and a rain
  cycle still running an old copy of the game's own loop. Each costs one re-roll
  of that timer, once, and the tool says so when it does it.
- **It tells you what it did**, in one message listing what was removed, anything
  that was repaired, and anything it kept on purpose. If it found nothing, it
  says nothing.
- **Once you have saved, loading that save again does nothing at all** — there
  is nothing left for it to find. Saving is the step that writes the cleaned
  colony into the file; until you save, the file still carries what the tool
  just removed from the game you are looking at.

### What it puts in your save

Nothing. No flags of its own, no saved variables, no background work left
running. A save this tool has run on is a save with *less* in it, never more —
which is why you can delete the tool once you have saved.

### Which versions it knows about

The list of what to remove was derived over the Relaunched Fix Pack and the
Relaunched Fix Pack: Opt-In Modules as they stood when this tool was built, and
it includes older names that only earlier builds of those mods ever wrote — the
too-old case is the one it is built for. It cannot tell which version of a pack
wrote your save, so it does not try: **if you were using a Fix Pack released
after this tool, check whether there is a newer Save Rescue before relying on
it.** A name it does not know is left untouched; it never sweeps.
>>> FILL-IN 2 — site link to the full name-by-name list, or DELETE THIS LINE <<<

**Playing on Xbox, PlayStation or the Microsoft Store version?** One rule that
applies to every mod rather than to this one: **while any mod is enabled, the
game does not unlock achievements on Xbox, PlayStation or the Microsoft Store.**
Steam and other PC versions are not affected. There is nothing to configure here
on any platform — this tool has no options and no settings page.

### Reporting a bug

Tell us what happened, roughly when it started, and whether it survives a save
and reload. A save file where it reliably happens is worth a thousand words. On
PC the game's logs are usually in your
`%AppData%\Surviving Mars Relaunched\logs` folder, and Ctrl+F1 opens the
official bug reporter (on Steam Deck the game leaves that one out). On Xbox and
PlayStation there are no logs to collect, and a plain description is still
genuinely useful.

═══════════════════════════ PLAYER TEXT — END ═══════════════════════════

---

## The shipped-module control — every sentence, because none of this is card text

⚠️ **Run again by prompt 2, firewalled from this table.** That is the design: the
last two chains were each wrong in exactly this way and each control caught it.

| claim | which shipped thing delivers it | evidence |
|---|---|---|
| a one-shot cleanup tool for saves that lost those two mods | mod `SMR_CommunitySaveRescue`, `Code/00_Core.lua` + `Code/10_SaveRescue.lua` | the shipped tree; `metadata.lua` `code` list |
| "install only after you have uninstalled those mods … it does nothing and says so once" | the per-pack stand-down gate; `stand_down_told` makes it session-once | spec §10.1; ⭐ **witnessed 2026-08-14** — the stand-down raised **exactly once** with both packs re-enabled, no duplicate on any later load |
| "a save that has nothing to clean gets no message at all" | the silence branch — the dialog is shown only when the pass removed or repaired ≥ 1 | spec §10.5; ⭐ **witnessed 2026-08-14** — the owner's own reload of a cleaned save was **silent**, with `save-rescue=1/1 active` beside it so the silence meant "found nothing", not "mod absent" |
| the dial is stored as one of the game's own bonuses and survives uninstall | rows `D15a`/`D15b` — `SMRFixPack_DroneSpeedDial` / `SMRFixPack_DroneCarryDial`, kind `label-modifier` | `D13_EXPOSED_SET.md` §2b, **MEASURED**; the opt-in module's own header says the same |
| "removes only entries it can name … no pattern matching" | the fixed `ROWS` table; removal is `field = nil` / `SetLabelModifier(label, id, nil)` per named row | `10_SaveRescue.lua`'s table; ⭐ measured — `removed 1566` **by name**, matching a prediction committed before the run row for row |
| "it never deletes a repair … tells you it kept it" | the two KEEP rows (`D10` wind-turbine buff prefix, `D11` track latch) and the report's *Kept on purpose* line | §5's KEEP list; ⭐ the F48 latch **survived** the witnessed pass and the *Kept on purpose* line was on the screen |
| the two one-shot heals, "one re-roll each" | the meteor-timer restart and the rain-cycle migration, both bounded once per load | spec §10.4. ⚠️ **Evidence tier: the manufactured witness of 2026-08-13**, not the 08-14 sitting — that save had nothing to heal (`heals 0, 0, 0`), which was the prediction and the point |
| "it tells you what it did … removed / repaired / kept on purpose" | `report_text()` | ⭐ the report dialog was **witnessed raising** 2026-08-14 with text matching the built function. ⛔ **The wording quoted to a player here is the BUILT text, per §10.5's 2026-08-14 correction — never the frozen design text** |
| "loading the same save a second time does nothing at all" | idempotence — which is what the spec chose *instead of* a persisted latch | spec §10.5/§10.9(5); measured `removed 0` on the second consecutive load, and again at the sitting |
| "nothing. No flags of its own, no saved variables, no background work left running" | no `GameVar(` call site anywhere; every mutation is a clear; the one thread is real-time and unflagged for persistence | §10.7's clause-by-clause table; **residue-zero MEASURED** — 0 names of its own over 4510 objects, `UIColony`, every rains entry and all 440 persistable globals |
| ~~the engine's mod-reference notice, self-clearing on the next save~~ **STRUCK 2026-08-14 — see audit finding 3 below** (checklist 29, owner-ruled) | the claim had no screen delivery: the line is `ModLog` (log-only) and the screen warning skips `optional_mod` mods | `Mod.lua:1199`, `SavegameMetadata.lua:97-99` |
| "it cannot tell which version of a pack wrote your save … check for a newer Save Rescue" | ⭐ **the spec requires this sentence**: version skew is answered by disclosure because detection is impossible (the only version-stamped name is dropped by the engine on the first load without the pack) | spec §10.6 |
| "a name it does not know is left untouched; it never sweeps" | the too-old case: the table is a whitelist | spec §10.6 |
| "no options and no settings page" | ⛔ **no `default_options`** in `metadata.lua`, stated there as a deliberate absence | the shipped file |
| achievements on Xbox / PlayStation / Microsoft Store | not this mod — a platform rule for every mod | `Achievement.lua:61-63`, consumed `:77`; the same audited sentence both other cards carry |
| the bug-report paragraph | verbatim the opt-in card's audited paragraph | `STORE_OPTIN.md`, audited |

### What was deliberately NOT claimed

1. ⛔ **No evidence boast.** The tool's launch record is real and it is agent
   material; a store card that recites launch counts is upgrading its own claim
   by word choice, which rule 6 forbids. The card says what the tool *does*.
2. ⛔ **"It writes nothing into your save" is not left to be read as "you will
   see nothing."** The engine-notice paragraph sits directly under it, because
   the spec's own §10.9(4) correction says that consequence *belongs in the
   description* and nowhere else.
3. ⛔ **No count of anything**, and **no exposed-set count in any form** — the
   standing bar (`PUBLIC_DOCS_DESIGN.md` §8). The footprint is described in
   player words; the derivation's numbers stay agent-side.
4. ⛔ **The removal dialog's text is not quoted on the card at all**, so this
   file is unaffected by checklist item 28 either way. If the owner rules "fix
   the code", nothing here changes.

### Sources this was assembled from

`C:\Dev\SMR-CommunitySaveRescue\metadata.lua`'s `description` /
`short_description` (already-written player strings) · that repo's `README.md`
(player-shaped sections) · `D13_EXPOSED_SET.md` §10.1, §10.4, §10.5 *as corrected
2026-08-14*, §10.6, §10.7, §10.9 · `D13_VERIFICATION.md` · `D13.md`'s sitting
record · `STORE_OPTIN.md` for the two paragraphs shared across cards.

### Routed — a stale claim in that repo, not fixed here

⚠️ **`C:\Dev\SMR-CommunitySaveRescue\README.md`'s "Status" section is out of
date**: it still says *"Not yet: an attended pass. Nobody has watched the two
dialogs render on screen … That sitting is scheduled."* The sitting **ran
2026-08-14** and all three dialog readings passed. The staleness understates
rather than overstates, so it breaches no rule — but it is a public repo saying
the opposite of the record. **Routed to prompt 2 with the correcting text ready:**
the attended pass ran, `removed 1566` on a native witness, all three dialog
readings witnessed, `tested` granted. Not edited here because it is outside this
prompt's named deliverables and the audit should decide whether a status
paragraph belongs in a shipping repo's README at all.

---

## Terminal audit, 2026-08-14 (release-3 prompt 2) — the firewalled control re-run: three findings, two fixed here, one routed

The control was re-run over the player text **before** reading the table above,
per the chain design. It confirmed most rows and caught three claims the table
had passed:

1. ⛔ **FIXED — the missing SAVE step.** *"Load your save once, read what it
   tells you, and you can delete it again"* described a procedure that loses its
   own work: the pass edits the **loaded** colony on `PostLoadGame`, and only the
   player's next save writes the cleaned state into the file. A player who loads,
   reads, quits without saving and deletes the tool keeps the dial boost forever
   — with the tool gone. The instruction now says **save your game** before
   deleting, here, in `metadata.lua`'s `description`/`short_description`, and in
   the opt-in card's FILL-IN 2 sentence. (Same mechanism the opt-in dial warning
   already states: *"saving is what clears it from the file."*) ⚠️ **The shipped
   report dialog also omits the save step** (`10_SaveRescue.lua`'s closing line
   invites removal without it) — that is a code string, priced by the same
   owner re-witness as item 28, and is noted there rather than edited.
2. ⛔ **FIXED — "while either of them is still installed this tool deliberately
   does nothing."** The shipped gate is **per-mod** (`owner_present`/
   `owner_blocked`): with only one mod removed, the tool DOES clean that mod's
   leftovers — the code's own comment calls the mixed case "the common one" and
   serves it deliberately. The old sentence told exactly that player the tool
   would not help them. Table row "witnessed 2026-08-14" is real but was the
   both-packs case; the mixed case is where the sentence failed. Reworded here
   and in `metadata.lua`.
3. ⚖️ **ROUTED, then RULED — "One thing you will still see … the game itself
   prints a notice."** The measured evidence behind §10.9(4) is a **log** line
   (`ModLog`, `Mod.lua:1199`); the only on-screen missing-mods warning is built
   by `GetMissingMods` (`SavegameMetadata.lua:97-99`), which **excludes mods
   marked optional — and all three of our mods ship `optional_mod = true`**, so
   a player who removes them sees nothing on screen. The same sentence sat on
   both audited store cards, the uninstall assembly's reference text and the
   site FAQ — routed as **checklist item 29**. ✅ **Owner ruled 2026-08-14:
   STRIKE.** The paragraph is deleted from every surface in the same sweep —
   both cards, this card, the assembly, the site FAQ.
