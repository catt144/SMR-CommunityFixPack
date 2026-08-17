# `metadata.lua` strings ×2 — drafted, and the corrections APPLIED

> ⚖️ **2026-08-17 — SOLO LAUNCH.** The opt-in mod does not publish at this
> launch (owner ruling, checklist 35). Its section below stays as the record
> for the day it does; the fix-pack `description` block carries its own dated
> note. Removed wordings: `PARKED_OPTIN_REFERENCES.md`.

**Built 2026-08-13 by `agent/prompts/public-docs/03_BUILD_STORE.md` (Job 4).**
Full pages: `STORE_FIXPACK.md` · `STORE_OPTIN.md`.

✅✅ **APPLIED 2026-08-13 ON THE OWNER'S INSTRUCTION** (*"yes fix that"*), after
they were told the live fix-pack string carried a false claim. The scope fence
excludes code, so this was an owner call and not an agent's — text-only fields,
no behaviour, no version bump. **What shipped is below and is what is in the two
`metadata.lua` files now.**

⚠️ **The drafts as first written carried two of the same defects the six sweeps
found in the pages**, and were corrected before being pasted: *"Every fix targets
a defect…"* (two of the five judgment calls are not code-contradiction) and
*"what it writes is inert without it"* (the restored bonus is deliberately not
inert). ⇒ **A string drafted from the same source as a page inherits the page's
defects.** Anything else drafted here needs the sweeps before it ships.

**What was wrong before the change, for the record:**

| file | what was wrong |
|---|---|
| fix pack `metadata.lua` | *"Individual fixes can be disabled on PC (via the console or a companion mod)"* — **the console half is false** (`PUBLIC_DOCS_DESIGN.md` §9.1, owner-caught). It also named the sibling mod by its **dead working title**, *"Community Opt-In Pack"*; the name decided 2026-08-13 was *"Community Fix Pack: Opt-In Modules"* (renamed with the whole family 2026-08-17: now *"Relaunched Fix Pack: Opt-In Modules"*) |
| opt-in `metadata.lua` | one clause of the uninstall instruction was incomplete in the way that costs a player their save — corrected in place; the rest is accurate but pre-dates the tiering |

⚠️ Neither string was counted against a store character limit; release prep
checks Paradox Mods' and Steam's limits before pasting.

---

## Fix pack — `SMR_CommunityFixPack`

**`short_description`** (tier 0, one sentence):

> Bug fixes for Surviving Mars: Relaunched — it repairs defects verified in the
> game's own code rather than rebalancing the game, and it is safe to add to a
> save you have already played.

**`description`** — ✅ **as shipped** (the metadata blurb, not the mod page):

> Bug fixes for Surviving Mars: Relaunched. Almost every fix targets a defect
> verified in the game's own code — the code says one thing, does another, and
> the fix makes it do what it says. It fixes bugs rather than rebalancing the
> game: preferences and features are deliberately not in it. Nothing is patched
> on disk; the mod wraps the game's own code at runtime and no game files are
> modified. Safe to add to a save you have already played — the pack writes
> almost nothing into your savegame, and removing it simply lets the original
> bugs come back. Every fix checks the game's code before it patches anything
> and stands down if an official patch changes what it was written for. Five of
> the fixes are judgment calls rather than plain repairs, and the mod page says
> which and why.

*(⚖️ 2026-08-17, solo launch: the separate-mod clause left this string — the
opt-in mod does not publish at this launch and a string that ships inside the
mod must not name a mod nobody can install. `last_changes` likewise: now
"Initial release." — its previous form named the opt-in mod. Both previous
wordings are VERBATIM in `PARKED_OPTIN_REFERENCES.md` P38/P39. The quoted block
above matches the applied string, which is the authority.)*

*(⚖️ 2026-08-15, `unattended-3` terminal audit: "Five of the fixes" → "Six" —
the F85 distress-popup flip ships disclosed as a design-judgment tweak.
⛔ **REVERSED the same day (item 31, owner-ruled): the F85 module was REMOVED**
— its popup is dead-coded out of retail — and the live string reverted to
**"Five"**, re-measured at **844** characters. ⚠️ 2026-08-16 public-docs
checkup: the quoted block above still said "Six" — the reversal sweep missed
this record — corrected to match the applied string, which is the authority.)*

⛔ **The per-fix disable claim is simply gone**, rather than corrected in place.
The accurate version needs a modder's identifier to be useful, and the blurb has
no room to say "a companion mod that loads before this one, and there is no
in-game switch on any platform". The mod page carries it; the blurb does not
raise it.

## Opt-in modules — `SMR_CommunityOptInPack`

> ⚖️ **2026-08-17 RENAME NOTE — read before pasting anything from this
> section.** The display-name family was renamed *Community Fix Pack* →
> *Relaunched Fix Pack* (owner ruling, checklist 36). The quoted strings below
> are updated to the NEW name. The opt-in repo's `metadata.lua` `title` was
> renamed the same day (owner's "rename them now" ruling), **but its
> `short_description` and `description` still carry the old name** — string
> edits beyond the title were fenced. Before the opt-in ever uploads, those
> two strings must be brought to match these blocks. Original wording, preserved for the record: every
> *"Relaunched Fix Pack"* in the two blocks below read *"Community Fix Pack"*
> as applied 2026-08-13.

**`short_description`** (tier 0, one sentence):

> Eight opt-in modules for Surviving Mars: Relaunched — every one of them off,
> or at the game's own setting, until you turn it on in Mod Options; works with
> or without the Relaunched Fix Pack.

**`description`**:

> Eight opt-in modules for Surviving Mars: Relaunched — seven off until you
> switch them on, and two drone dials sitting at the game's own values until you
> move them. Rockets that keep requesting fuel while parked, acknowledged "not
> working" warnings, a per-dome "closed to new residents" policy, more than one
> Artificial Sun (with the panel-binding repair that makes a second one work), a
> closest-hub-first drone dispatch overhaul (experimental), automatic cohort
> housing for Seniors and Children, a Nursery/Retirement Dome policy, and two
> drone stat dials for speed and carry capacity. Everything is switched in
> Options → Mod Options → Relaunched Fix Pack: Opt-In Modules, on every platform
> and with a controller, and toggles take effect immediately. Nothing is patched
> on disk: the mod wraps the game's own code at runtime, and a module you leave
> off behaves exactly like the unmodded game. Works with or without the
> Relaunched Fix Pack — neither needs the other. One thing to know before you
> ever uninstall: set both drone dials back to base and then save, because
> setting them to base clears the boost from the colony you are playing and
> saving is what clears it from the file.

⛔ **That last sentence was corrected 2026-08-13 and the correction is the point
of this whole file.** As first drafted it said *"set both drone dials back to
base first"* and stopped there — which is the instruction that does **not** save
the player's save. Anyone pasting this draft must paste the corrected form.

---

## What was actually changed in each file

| file | field | change |
|---|---|---|
| `SMR-BugFixPack/metadata.lua` | `description` | **replaced.** Removed the false *"disabled on PC (via the console…)"* claim and the dead working title *"Community Opt-In Pack"*; rewritten to tier 0 + the four gating answers in miniature |
| | `short_description` | **replaced** with the tier-0 sentence |
| `SMR-OptInPack/metadata.lua` | `description` | ⭐ **one clause fixed, and it is the consequential one.** It read *"Set both Drone dials back to base before uninstalling"* — the same incomplete recipe sweep 4 caught on the page. **Setting the dials to base clears the running colony; only saving clears the file.** Now says both steps |
| | `short_description` | **unchanged** — accurate as written (*"all off or at base"*), and it predates nothing |

⚠️ **The opt-in `description` was NOT swapped for the draft below.** The live
string is post-split, accurate and good; replacing it wholesale would have been
change for its own sake, and the draft's improvements (a tier-0 lede, the
second-sun clause saying the module ships the panel repair too) are worth having
but are release-prep's call alongside the display-name and preview-art pass.

## Notes

* The opt-in `description` draft below keeps the live string's structure and its
  uninstall warning almost intact — the live one was written after the split and
  is good. What it would change: the lede matches tier 0, the second-sun clause
  says what the module actually ships (the limit **and** the panel repair), and
  the Mod Options path is spelled out.
* ⛔ **No count of fixes in either string**, per `PUBLIC_DOCS_DESIGN.md` §4.4.
  `last_changes` is where a count may live if release prep wants one, and it is
  recounted with `--emit-counts` in the same commit — never copied from prose.
* ⛔ **No claim that anything is listed on screen by a console command**
  (design §12 hole 11, unsettled).
