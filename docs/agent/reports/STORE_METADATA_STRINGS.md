# `metadata.lua` strings ×2 — drafted, NOT applied

**Built 2026-08-13 by `agent/prompts/public-docs/03_BUILD_STORE.md` (Job 4).**
Full pages: `STORE_FIXPACK.md` · `STORE_OPTIN.md`.

⛔ **NOT APPLIED, deliberately.** `metadata.lua` is code, and this chain's scope
fence (`prompts/public-docs/README.md`) excludes code. These strings are routed
to the **release-prep pass** — the same pass that bumps the version, refreshes
`last_changes` and adds the `ignore_files` patterns (checklist 23), so the file
is opened once rather than three times.

⚠️ **Both live `description` fields are wrong today**, which is why this is
routed rather than merely drafted:

| file | what is wrong now |
|---|---|
| fix pack `metadata.lua` | *"Individual fixes can be disabled on PC (via the console or a companion mod)"* — **the console half is false** (`PUBLIC_DOCS_DESIGN.md` §9.1, owner-caught). It also names the sibling mod by its **dead working title**, *"Community Opt-In Pack"*; the decided name is *"Community Fix Pack: Opt-In Modules"* |
| opt-in `metadata.lua` | accurate, but pre-dates the tiering and does not match tier 0 |

⚠️ Neither string was counted against a store character limit; release prep
checks Paradox Mods' and Steam's limits before pasting.

---

## Fix pack — `SMR_CommunityFixPack`

**`short_description`** (tier 0, one sentence):

> Bug fixes for Surviving Mars: Relaunched — it repairs defects verified in the
> game's own code rather than rebalancing the game, and it is safe to add to a
> save you have already played.

**`description`** (the metadata blurb, not the mod page):

> Bug fixes for Surviving Mars: Relaunched. Every fix targets a defect verified
> in the game's own code — the code says one thing, does another, and the fix
> makes it do what it says. No rebalancing and no redesigns: preferences and
> features live in a separate mod, Community Fix Pack: Opt-In Modules, and
> neither mod needs the other. Nothing is patched on disk; the mod wraps the
> game's own code at runtime and no game files are modified. Safe to add to a
> save you have already played: the pack writes almost nothing into your
> savegame, what it writes is inert without it, and removing the pack simply
> lets the original bugs come back. Every fix checks the game's code before it
> patches anything and stands down if an official patch changes what it was
> written for. Five of the fixes are judgment calls rather than plain repairs,
> and the mod page says which and why.

## Opt-in modules — `SMR_CommunityOptInPack`

**`short_description`** (tier 0, one sentence):

> Eight opt-in modules for Surviving Mars: Relaunched — every one of them off,
> or at the game's own setting, until you turn it on in Mod Options; works with
> or without the Community Fix Pack.

**`description`**:

> Eight opt-in modules for Surviving Mars: Relaunched — seven off until you
> switch them on, and two drone dials sitting at the game's own values until you
> move them. Rockets that keep requesting fuel while parked, acknowledged "not
> working" warnings, a per-dome "closed to new residents" policy, more than one
> Artificial Sun (with the panel-binding repair that makes a second one work), a
> closest-hub-first drone dispatch overhaul (experimental), automatic cohort
> housing for Seniors and Children, a Nursery/Retirement Dome policy, and two
> drone stat dials for speed and carry capacity. Everything is switched in
> Options → Mod Options → Community Fix Pack: Opt-In Modules, on every platform
> and with a controller, and toggles take effect immediately. Nothing is patched
> on disk: the mod wraps the game's own code at runtime, and a module you leave
> off behaves exactly like the unmodded game. Works with or without the
> Community Fix Pack — neither needs the other. One thing to know before you
> ever uninstall: set both drone dials back to base first, because a dial left
> off base leaves its boost in the savegame.

---

## Notes

* The opt-in `description` above keeps the live string's structure and its
  uninstall warning almost intact — the live one was written after the split and
  is good. What changes: the lede matches tier 0, the second-sun clause says
  what the module actually ships (the limit **and** the panel repair), and the
  Mod Options path is spelled out.
* ⛔ **No count of fixes in either string**, per `PUBLIC_DOCS_DESIGN.md` §4.4.
  `last_changes` is where a count may live if release prep wants one, and it is
  recounted with `--emit-counts` in the same commit — never copied from prose.
* ⛔ **No claim that anything is listed on screen by a console command**
  (design §12 hole 11, unsettled).
