return PlaceObj('ModDef', {
	-- ⭐ RENAMED 2026-08-17 (owner ruling, checklist 36): "Community Fix Pack"
	-- → "Relaunched Fix Pack", before first upload — a same-purpose mod named
	-- "SMR Community Fixes" already exists on Paradox Mods (154004) and the
	-- shared word invited mis-routed reports both ways. Display name ONLY: the
	-- mod `id` below and the `[CommunityFixPack]` log tag are deliberately
	-- unchanged (every archived log and gate baseline greps them; nothing
	-- player-searchable contains them).
	'title', "Relaunched Fix Pack",
	-- ⚠️ REWRITTEN 2026-08-13 (owner instruction, public-docs chain prompt 3).
	-- The previous `description` carried TWO defects that would have shipped:
	-- it told players individual fixes can be disabled "via the console", which
	-- is FALSE (Register reads the veto table at mod load, 00_Core.lua:384-388 —
	-- the fixes are applied long before anyone can type), and it named the
	-- sibling mod by its dead working title "Community Opt-In Pack". Both are
	-- corrected below. Full pages + the claim traces: docs/agent/reports/
	-- STORE_FIXPACK.md and STORE_METADATA_STRINGS.md.
	-- ⚖️ 2026-08-17 (SHIP_SOLO_PREP): the owner ruled the fix pack LAUNCHES ALONE
	-- — the opt-in mod is not ready and does not publish. Both player strings
	-- below (`description`, `last_changes`) therefore no longer name it: a string
	-- that ships inside the mod cannot be changed without a version bump and a
	-- re-upload, and it must not name a mod no player can install. The removed
	-- wordings are VERBATIM in docs/agent/reports/PARKED_OPTIN_REFERENCES.md
	-- (P38/P39) with the restore trigger and checklist.
	-- ⭐⭐ 2026-08-24: this is now THE CARD BODY, not a summary — owner ruling.
	-- Both portals fill their page from this string on EVERY upload
	-- (`LongDescription`, `ParadoxMods.lua:158`; `description`,
	-- `SteamWorkshop.lua:110`), so a hand-pasted page body cannot survive one.
	-- Shipping the card here makes the automatic result complete and correct
	-- instead of a 779-char summary; the two portal blocks in
	-- `reports/STORE_CARD_LIVE.md` are now OPTIONAL POLISH (headings, bold,
	-- BBCode) re-applied by hand only when wanted, never to fix a wrong page.
	-- ⛔ PORTAL-NEUTRAL, and it must stay that way: the Paradox block says
	-- "this page has no comment section" and links "Also on the Steam
	-- Workshop" — both FALSE on Steam. Those two passages are rewritten and
	-- removed here. Never paste a portal block into this field verbatim.
	-- ⚠️ Length is UNVERIFIED against the upload API (the web editor took
	-- 5,165 chars; the upload is a different path and no portal limit was ever
	-- confirmed). If an upload rejects it, revert this field and say so.
	-- ⭐ MEASURED 2026-09-09, and the caveat above understates what is proven:
	-- the body v5 actually SHIPPED through the upload path was **5,228** chars,
	-- not 5,165, so the upload API is known to accept at least that. This rewrite
	-- takes it to **5,342** (+114). Still unverified, but it is a small increment
	-- over a length that demonstrably went through, not a leap past the only
	-- data point. ⚠️ `reports/STORE_CARD_LIVE.md` said "5,124 chars" until
	-- today; that figure predated the F105/F108/F110 lines and was already wrong.
	-- ⭐⭐ REWRITTEN 2026-09-09 for hotfix 2 (`prompts/hotfix2/06_TEXT.md`). Link 02
	-- deleted 36 of the 80 fix modules because game 1.1.0 repairs those bugs
	-- itself, which made ELEVEN of this string's twenty "SOME OF WHAT IT FIXES"
	-- bullets and three of its four headline clauses describe fixes that are no
	-- longer in the pack. All of them are replaced from the surviving set.
	-- ⛔ THE COUNT IS RECOUNTED FROM THE DEPLOYED FIX LIST, never from this file
	-- and never from memory: `grep -c '^??? ' content/fix-list.md` = **46** in
	-- `SMR-CommunityMods` (was 82), and the section tally sums to the same
	-- (1+13+4+3+9+4+7+2+3). "Four of them repair things you cannot see" is now
	-- THREE — the fix list's own "Under the hood" section lost the battery/tank
	-- rate-modifier entry. Both numbers stay checkable by the reader on the page
	-- this card links to, which is the only thing that makes a count safe here.
	-- ⚠️ The site page is committed but NOT PUBLISHED (`publish-site.yml` is
	-- `workflow_dispatch` only) — publish it in the same sitting as the upload or
	-- the card's count disagrees with the page it tells the reader to check.
	-- ⛔ THE VETO EXAMPLE named `DustDevilSpawnGate`, which link 02 deleted. It is
	-- now `LakeEntombment` — a live id, verified at `Code/Fix_LakeEntombment.lua:41`.
	-- ⭐ The 1.0.7 line is ck118, ruled: portal-neutral, pointing at the site page
	-- that carries the frozen v5 for players who stayed on the old game branch.
	-- ⛔⛔ HOW IT WORKS BULLET 3 IS DELIBERATELY UNTOUCHED, and that is a RULING,
	-- not an oversight (checklist 112, 2026-09-09). The owner rejected BOTH
	-- recorded options — (a) reword it down now, (b) leave it for the next cycle
	-- — and commissioned `prompts/SELFCHECK_PROMISE_AUDIT.md` on a third the item
	-- never offered: make the sentence TRUE rather than reword the promise to
	-- match what the code can do. ⚠️ It therefore ships OVER-PROMISING for this
	-- upload; that is the owner's accepted, recorded cost. Do not "fix" it here.
	-- ⭐ 2026-09-10, v7 words (`RELEASE.md` step 1): count word Forty-six → FORTY-EIGHT
	-- (fix list recounted 48, C74+C77 and C83 added) and one headliner, C83's arrivals
	-- bullet, beside the F53 one it is easily confused with. Length now **5,428**
	-- (+86 on the 5,342 both portals accepted at v6). Why C83 and not C74: STORE_CARD_LIVE.
	'description', "Bug fixes for Surviving Mars: Relaunched.\n\nForty-eight repairs, each one written up on the fix list with what you would\nhave seen and what was actually wrong. Every one targets something the game's\nown code gets wrong — the code says one thing, does another, and the fix makes\nit do what it says. It fixes bugs; it does not rebalance the game. Preferences\nand features are deliberately not in it.\n\nSome of them you could hardly miss: an entire train line and every train on it\ndeleted by salvaging a single hex, colonists suffocating on a walk between two\ndomes, an artificial lake burying the rover that was building it.\n\nMore of them you would never have blamed on a bug, because the game looked\nperfectly normal while the arithmetic underneath it was wrong — a reward for\nfreeing the wisps that paid about a thousandth of what its own message promised,\na researched breakthrough the game restored to only one of the three wind\nturbine types it covers, a track refund that paid a stub's worth of Metals\nhowever long the line was, a Comfort penalty billed for longer than the journey\nactually took.\n\nAnd three of them repair things you cannot see at all today: real defects that\nthe shipped numbers happen to hide, which another mod, a game patch or a DLC\ncould walk straight into.\n\n\nSOME OF WHAT IT FIXES\n\n· Colonists walked across the surface between domes and suffocated.\n· Rocket loads of new arrivals died on their way to a dome.\n· New arrivals moved into a dome that was switched off, quarantined or without air.\n· A dome sat half empty and still refused to house anyone.\n· A bed that fell vacant sat empty while colonists were homeless.\n· Colonists stayed homeless after you built a Shuttle Hub.\n· Night-shift colonists never came back to work after midnight.\n· A salvaged farm kept supplying its dome with oxygen forever.\n· Building an artificial lake buried the rover that built it.\n· Drone Hubs paralysed themselves every time an Extender flickered.\n· Salvaging one piece of track deleted the whole line, and its trains with it.\n· Demolishing a station permanently deleted the trains parked there.\n· Meteor-damaged track could not be salvaged at all.\n· Two train buildings fought over the same connector hex forever.\n· A destroyed tunnel still worked as a shortcut.\n· Automatic rockets and landers took off with nothing aboard.\n· A Jumbo Cave mystery could get stuck clearing waste rock and never complete.\n· The Philosopher's Stone mystery hung one step from the end.\n· A story step asked for a cave-in on a map that does not exist, and the story stopped.\n· The Gene Forging research did nothing at all.\n· The Domes Overview stopped marking domes in trouble.\n\n… and a good deal more, including quieter repairs to drones, shuttles, domes,\nrockets, research, storylines and the interface.\n\nThe full list — every fix, what you would have seen, and what was actually\nwrong — is here:\nhttps://catt144.github.io/SMR-CommunityMods/fix-list/\n\n\nSEVEN MACHINES THAT WORKED IN SILENCE\n\nThe Rare Metals Extractor's hammer, the MOXIE, the Water Extractor, Shuttle Hub\nshuttles, the RC Driller, the RC Dozer and The Excavator all had sounds or\neffects made for them that never played. They play now.\n\nTwo of them also have a skin that is silent by design, so if one of these stays\nquiet, check its skin before you blame the fix:\n· Rare Metals Extractor — the hammer strikes and puffs steam; the drill never\n  strikes. NASA, SpaceY, BlueSun, Brazil, Roscosmos, Japan and ISRO colonies\n  get the drill by default.\n· MOXIE — the double-pump skin thumps and puffs; the blocky one is silent.\n\nSelect the building and press Change Skin (the paintbrush on its panel) to\nswitch. The screenshots on this page show which skin is which.\n\n\nSTILL PLAYING ON GAME VERSION 1.0.7?\n\nThis pack tracks the current version of the game. If you stayed on 1.0.7, there\nis a separate frozen build for it, with instructions:\nhttps://catt144.github.io/SMR-CommunityMods/legacy-1-0-7/\n\n\nHOW IT WORKS\n\n· No game files are modified. The pack wraps the game's own code while it runs.\n· Safe to add to a save you have already played. It writes almost nothing into\n  your savegame, and removing it simply lets the original bugs come back.\n· Every fix checks the game's code before it touches anything, and stands down\n  by itself if an official patch changes what it was written for. A fix that\n  stands down does nothing at all — it never guesses.\n· A few of the fixes are judgment calls rather than plain repairs. Those are\n  marked as such on the fix list, with the reasoning, rather than folded in\n  quietly.\n\n\nFOUND A BUG, OR ONE THIS PACK DID NOT FIX?\n\nReports are read and acted on, and a save file where it reliably happens is\nworth more than any description of it.\n\n· Issue tracker — the route for everyone, and the only one that can carry a\n  save file or a log:\n  https://github.com/catt144/SMR-CommunityFixPack/issues\n  It needs a free GitHub account and works from a browser on any device.\n\n· If this page has a comment section, that works too for anything you can\n  describe in words. Only the tracker can carry a file.\n\nOn console — every Xbox and PlayStation player — there is nothing to attach in\nthe first place, and a plain description in your own words is genuinely useful.\n\n\nFOR MODDERS\n\nThe pack is built to share the game with your mod rather than take it over. It\nhooks the game's functions and calls the original where it can, so another mod\nthat touches the same function keeps working. Where a bug sits in the middle of\na function and cannot be hooked, the fix copies the corrected body instead —\nthose are the ones most likely to clash, and each one names in its source the\ngame file and lines it came from.\n\nAny single fix can be switched off from another mod, without touching this one.\nSet the fix's id as a key on the veto table before the pack loads:\n\n    SMRFixPack_Disabled = rawget(_G, \"SMRFixPack_Disabled\") or {}\n    SMRFixPack_Disabled[\"LakeEntombment\"] = true\n\nThe id is the key, not a list entry — a plain list looks valid and switches off\nnothing. \"Before the pack loads\" means your mod has to load first.\n\nSource, and the reasoning behind every fix:\nhttps://github.com/catt144/SMR-CommunityFixPack",
	'short_description', "Bug fixes for Surviving Mars: Relaunched — it repairs defects verified in the game's own code rather than rebalancing the game, and it is safe to add to a save you have already played.",
	-- ⭐ ADDED 2026-08-17 AT THE UPLOAD SITTING (④ step 1). Without it the
	-- Paradox Mods upload is HARD-REJECTED before it packs anything —
	-- `ParadoxMods.lua:39-42` fails on `mod.image == ""` with "Missing mod
	-- Preview image"; Steam does not reject but uploads with no thumbnail
	-- (`SteamWorkshop.lua:113`). The file is the C1 art chosen 2026-08-14 and
	-- re-lettered 2026-08-17 for the rename, copied to the mod root from
	-- docs/agent/reports/preview_art/FINAL_fixpack_preview.png (1024×1024,
	-- 44,322 bytes — under both recorded limits, PDX ≤2 MB / Steam ≤1 MB).
	-- ⚠️ WRITTEN BY HAND, NOT SET IN THE MOD EDITOR, AND THE PATH FORM MATTERS:
	-- `content_path` is `ModContentPath .. id .. "/"` (Mod.lua:1758) and the
	-- folder is mounted there (Mod.lua:859-860), so this resolves. Starting the
	-- string with `Mod/` also makes `FixRelativePaths` skip it (Mod.lua:577), so
	-- nothing is rewritten in memory on load and the mod stays CLEAN — which is
	-- the whole point: any Mod Editor save runs `self.version = self.version + 1`
	-- (Mod.lua:967) and would ship 1.0.1 against the owner's ruled 1.0.0.
	-- ⛔ The copy at docs/agent/reports/preview_art/ is the RECORD and stays;
	-- this root copy is what ships (packaging 79 → 80).
	'image', "Mod/SMR_CommunityFixPack/preview.png",
	-- ⭐ ADDED 2026-09-10 (owner: the card should point players at pictures of the two
	-- skins) — the store GALLERY. Both uploaders read screenshot1..5: the Mod Editor copies
	-- each to TmpData/ModUpload/Screenshots as `ModScreenshot_<name>` (GedModEditor.lua:
	-- 687-702); Paradox uploads them (ParadoxMods.lua:97-110, :159); Steam adds/updates/
	-- removes ONLY `ModScreenshot_*` previews and never touches images added by hand on the
	-- page (SteamWorkshop.lua:43-81). Caps: Steam 1 MB each (SteamWorkshop.lua:85, :101),
	-- Paradox 2 MB (ParadoxMods.lua:87, :101) — the owner's ~2 MB PNGs would fail, so
	-- `tools/store_screenshots.py` re-encodes them (~350 KB JPEGs) from the marked-up
	-- originals in C:\Dev\SMR-ScreenCaptures\c74_skins. `Mod/`-prefixed like 'image', so
	-- FixRelativePaths skips them (Mod.lua:579) and the mod stays CLEAN; `ignore_files`
	-- keeps store_screenshots/ OUT of the player's pack (`tools/pack_predict.py` shows it).
	'screenshot1', "Mod/SMR_CommunityFixPack/store_screenshots/1_rare_metals_drill_skin.jpg",
	'screenshot2', "Mod/SMR_CommunityFixPack/store_screenshots/2_rare_metals_hammer_skin.jpg",
	'screenshot3', "Mod/SMR_CommunityFixPack/store_screenshots/3_moxie_skins.jpg",
	-- ⚠️ `last_changes` no longer quotes a fix COUNT, on purpose: every previous
	-- wording carried one and it drifted every time a fix was retired or added
	-- (68 -> 66 after F24/F28 went `wontfix`, 67 after F83). If launch prep puts
	-- a number back, recount it from `python tools/doccheck.py --emit-counts`
	-- in the same commit — never from this comment.
	-- ⚖️ 2026-08-15 (unattended-3 audit): "Five of the fixes are judgment calls"
	-- → "Six", because the F85 distress-popup flip shipped as a design-judgment
	-- tweak. ⛔ REVERTED TO **FIVE** the same day (owner ruling, checklist 31):
	-- F85's module was REMOVED — the popup it paused is dead-coded out of the
	-- retail build, so the fix could never fire for a player. The count is
	-- settled as FIVE consistently across card, this string, site FAQ and fix
	-- list; the removed module is preserved verbatim with a re-arm trigger in
	-- docs/agent/reports/SHELVED_F85_DISTRESS_PAUSE.md, and re-applying it puts
	-- this number BACK to six. Reasoning: STORE_FIXPACK.md notes, F85.md.
	-- ⛔ SUPERSEDED 2026-08-28 — THE COUNT IS **SIX** AGAIN, for a different
	-- reason: F108 (Extractor AI staffed-performance) shipped as a judgment
	-- call. F85 is still `wontfix` and still out; the two movements are
	-- unrelated and the "settled as FIVE" sentence above is now FALSE. Measured
	-- 2026-08-29 off the DEPLOYED site: fix-list marks six entries
	-- `judgment call`, FAQ names the same six, and this string states no number
	-- at all ("A few of the fixes"), which is why the store never drifted.
	-- ⇒ recount from the fix list, never from this block. Audit:
	-- docs/agent/reports/SITE_AUDIT_0829.md.
	-- ⛔ CORRECTED 2026-08-14 (release-3 prompt 1): this field STILL carried the
	-- dead working title "Community Opt-In Pack" that the comment ten lines above
	-- says was corrected — the 08-13 pass fixed `description` and missed this
	-- string. A player told to look for that name would find nothing on any
	-- store. Licence: the owner's standing 22b word ("change any wordings to
	-- their accurate versions"); text-only, no behaviour, no version bump.
	-- ⭐ REWRITTEN 2026-08-24 for the first patch. Until now this said
	-- "Initial release.", which is what the 1.0.0 upload shipped and what both
	-- live listings still show. ⚠️ It is the CHANGELOG a player reads on the
	-- store, so it must describe THIS version, not the pack. Player's words, no
	-- fix ids, no counts (counts drift, see the comment above `last_changes`).
	-- ⛔ IT IS NOT A DESCRIPTION — it is the PER-VERSION CHANGE-NOTE ENTRY on BOTH
	-- storefronts, sent automatically at upload and archived there forever:
	--   Paradox  `ChangeLog = last_changes`   (`ParadoxMods.lua:151`)  -> CHANGELOG panel
	--   Steam    `change_note = last_changes` (`SteamWorkshop.lua:114`) -> Change Notes tab
	-- ⇒ three consequences. (1) REWRITE IT BEFORE EVERY upload or the next one
	-- posts a duplicate entry under a new version. (2) Keep it TERSE — the field
	-- is `lines = 3` (`Mod.lua:254`) and the house style on both stores is a
	-- dashed line or two, not a paragraph. (3) It is HISTORICAL: it describes the
	-- version it ships with, forever, so never write it in the present tense of
	-- the pack as a whole.
	-- ⛔ F107 is deliberately absent: it was a defect in our own fix for F105,
	-- found and repaired before either ever reached a player, so naming it on a
	-- store page would describe a problem nobody could have had.
	-- Licence for this edit: the owner's standing 22b word ("change any wordings
	-- to their accurate versions"); text-only, no behaviour, and `H-02` as
	-- reworded 2026-08-24 puts hand edits to this string squarely in scope while
	-- leaving the version bump to the owner's sitting.
	-- ⭐ REWRITTEN 2026-09-08 for the 1.1.0 hotfix (HOTFIX_1_APPLY). The v5 text
	-- above described the F110 Jumbo Cave fix and would post a duplicate CHANGELOG
	-- entry if left alone. This version's change is a COMPATIBILITY pass, so the
	-- note leads with the two things a player actually saw break.
	-- ⛔ WRITTEN AHEAD OF THE PROOF. At the time of writing the F114/F115 gates
	-- were desk-verified only — no boot log yet. The owner's rule of 2026-09-08 is
	-- that a "Fixed" line is a CLAIM until confirmed, and that binds OUR notes too:
	-- do not upload this string until a 1.1.0 boot reads the predicted 17 inactive /
	-- 14 named with ZERO Fix_TrainCargoDumping.lua:89 and ZERO
	-- Fix_LandscapeUnitFilter.lua:63 lines (checklist, the 109/110 block).
	-- ⚠️ The third line is not hedging for its own sake: 17 of the pack's 22
	-- full-body replacements have never been diffed against 1.1.0, and no instrument
	-- we own bounds body divergence — the name sweep sees names, sigcheck sees
	-- arity, the runtime self-checks see existence, and F114 was invisible to all
	-- three. Claiming 1.1.0 compatibility outright would be the exact "Fixed is a
	-- claim" error, aimed at our own players.
	-- ⛔ No fix ids, no counts, no load-order advice, no other mod named (EF-054,
	-- FIX_POLICY §8). Licence: the owner's standing 22b word; text-only, no
	-- behaviour, and H-02 leaves the version bump to the upload sitting.
	-- ⭐⭐ REWRITTEN WHOLESALE 2026-09-09 for hotfix 2 (`prompts/hotfix2/06_TEXT.md`).
	-- ⛔ NOT APPENDED — the hotfix-1 text above it is a CHANGELOG entry that was
	-- already posted to both stores, so keeping any of it would post a duplicate.
	-- ✅ ck113 (ruled 2026-09-08) IS honoured rather than sidestepped: the track-
	-- salvage clause reads "updated for the new game code", never "brought in line
	-- with". ⚠️ It now describes THIS version's F116 work (ck111 + ck119), not
	-- hotfix 1's, and it is capped at "matching the base game" — link 04's ceiling,
	-- because F116 was never reproduced.
	-- ⛔ NO "FIXED" ANYWHERE, and the last bullet says why in the player's words:
	-- nothing in this version has been watched in a running colony on 1.1.0. Every
	-- in-play control from links 03 and 04 was still owed when this was written
	-- (owner rule 2026-09-08: a note that says "Fixed" is a CLAIM, false until we
	-- confirm it ourselves). ⛔ It also does NOT claim 1.1.0 compatibility outright:
	-- 17 of the 22 full-body replacements have never been diffed against 1.1.0.
	-- ⚠️ Three player-visible LOSSES are stated rather than dropped quietly, which
	-- is why bullet 2 exists: the retired asteroid-habitat hold (F-3 half (a)), the
	-- train count that stops refreshing after a salvage (F49 `TrainMinors`), and the
	-- stranded Astrogeologist +10% — written as PERMANENT in an existing save, never
	-- as self-clearing, because it is (link 02). A new game is clean.
	-- ⛔ NOTHING is said about F12 `LowStorageWarning` beyond the blanket removal
	-- sentence, and that is deliberate: an earlier draft would have told players
	-- they now get no low-Food warning at all. That is FALSE — 1.1.0 REPLACED both
	-- warnings (`StarvingColonists`, `MaintenanceStuckBuildings`). Checklist 121 is
	-- withdrawn; do not resurrect the loss claim.
	-- ⚠️ Five bullets, not three. `lines = 3` (`Mod.lua:254`) is the Ged text-box
	-- HEIGHT and truncates nothing; this version retires ~36 fixes and repairs or
	-- re-enables eight, and compressing that into two dashed lines would have cost
	-- the three loss statements above. Terseness loses to disclosure here.
	-- ⭐ REWRITTEN WHOLESALE 2026-09-10 for v7 (`RELEASE.md` step 1, from `RELEASE_OUTBOX.md`).
	-- ⛔ NOT APPENDED — the hotfix-2 note above was posted to both stores at v6. Two entries,
	-- both `tested-attended` on 1.1.0.403908, so unlike v6's note this one MAY say they were
	-- watched working: C83 (arrival fallback dome, `bugs/C83.md`) and C74+C77 (seven units'
	-- animation-moment FX, `bugs/C74.md`, `C77.md`). The skin sentence is REQUIRED by the
	-- outbox: the drill extractor and white MOXIE stay silent by design, and a player who
	-- hears nothing on those must not read it as the fix failing. Metatron is out of scope
	-- and deliberately unnamed. No "Fixed", no fix ids, no counts.
	'last_changes', "- New arrivals are no longer sent into a nearby dome that is switched off, quarantined or without life support when the working domes they can reach have no free homes. They go to the nearest working dome instead, even if some of them have to wait there for a home.\n- The missing strike, pump, landing, drilling, shovel and bucket effects are back on seven machines and vehicles: the Rare Metals Extractor's hammer, the classic MOXIE, the Water Extractor, Shuttle Hub shuttles, the RC Driller, the RC Dozer and The Excavator. Sound and visuals only. The drill-style Rare Metals Extractor and the white MOXIE are silent by design; use Change Skin to switch the extractor to its hammer.\n- Both were watched working in a running colony on game 1.1.0.",
	-- the packer includes EVERYTHING recursively minus this list (Mod.lua:250-256,
	-- GedModEditor.lua:716-732) — without the extra patterns docs/, README.md,
	-- .gitignore and .claude/ all ship inside the .hpk. LICENSE ships on purpose.
	-- ⭐ THREE PATTERNS ADDED 2026-08-14 AT LAUNCH PREP (release-3 prompt 1) —
	-- checklist item 23, the owner's ruling "YES, add the missing patterns, at
	-- launch prep", all three mods. MEASURED before and after over the real
	-- tree: without them this package shipped `CLAUDE.md`, `.gitattributes` and
	-- all TEN files of `tools/` into a player's download — 90 files where 78
	-- belong. Nothing there ever RUNS (only `code` executes), but CLAUDE.md is
	-- agent instructions and `tools/` is our build machinery.
	-- ⭐ `*AGENTS.md` added 2026-09-10: the Codex mirror of CLAUDE.md (a byte
	-- copy written by `doccheck.py --regen`, checked on every run), excluded
	-- for the same reason.
	-- ⚠️ `LICENSE` is NOT excluded, deliberately: item 23 listed it, but the
	-- rescue mod built afterwards states "LICENSE ships on purpose" and a licence
	-- inside the package is right. All three mods now agree on that.
	-- ℹ️ Item 23's one unverifiable sub-case — whether `.github/` slips past the
	-- `.git` pattern — is MOOT here: no mod repo has a `.github/` directory
	-- (checked in all three, 2026-08-14). Only the site repo does, and it is not
	-- a mod.
	'ignore_files', {
		"*.git/*",
		"*.svn/*",
		"*/Source/*",
		"*/SourceData/*",
		"*/docs/*",
		"*/.claude/*",
		"*/tools/*",
		"*README.md",
		"*CLAUDE.md",
		"*AGENTS.md",
		"*.gitignore",
		"*.gitattributes",
		"*/store_screenshots/*",
	},
	'id', "SMR_CommunityFixPack",
	'author', "catt144",
	-- ✅ RULED 2026-08-17 (owner, checklist 35 Q2: "lets go with 1.0.0"):
	-- first public release is a clean 1.0.0, matching the opt-in ruling's
	-- logic. PackVersion renders version_major.version_minor.version.
	-- ⛔⛔ MOVED BY THE UPLOADS THEMSELVES, 2026-08-20 — DO NOT "CORRECT" IT BACK.
	-- Both portals force `SaveWholeMod` on a first upload and every save runs
	-- `version = version + 1` (`Mod.lua:967`), but they save at DIFFERENT points,
	-- which is why the two stores hold different numbers for identical code:
	--   * Paradox Mods saves AFTER the content upload returns
	--     (`ParadoxMods.lua:167-173`) ⇒ it received the package built at
	--     `version = 0` and its listing is **1.0.0**, exactly as ruled. The save
	--     then left the tree at 1.
	--   * Steam saves BEFORE packing (`SteamWorkshop.lua:17-22`, then
	--     `CreatePackageForUpload`) ⇒ the bump to 2 is INSIDE the archive Steam
	--     got, so that listing is **1.0.2**, and its file is 385,131 B against
	--     our 391,567 B pack because the same save also stripped every comment
	--     from this file and `items.lua` before packing them.
	-- ⇒ After those two uploads the tree sat at 2. That is the honest record;
	-- resetting it to 0 would make this file lie about the published listings.
	-- ⚠️ `version_minor` is absent below because `SaveDef` omits default-valued
	-- properties — it was `0`, and `PackVersion` still renders
	-- version_major.version_minor.version.
	-- ⭐ UPDATED 2026-08-30 — THE TREE NOW SITS AT 5, and
	-- ⛔⛔ THE VERSION ARITHMETIC CANNOT TELL YOU WHICH PORTALS RAN. 2026-08-24
	-- (F105): version 2 → 3. 2026-08-28 (F108): version 3 → 4. 2026-08-30
	-- (F110): version 4 → 5. **ONE** bump per sitting — and both portals were
	-- uploaded at every sitting.
	-- The reason, re-read at Src 2026-08-29: the forced pre-pack save in
	-- `Steam_PrepareForUpload` sits INSIDE `if mod.steam_id == 0 then`
	-- (`SteamWorkshop.lua:17-22`) — the CREATE-ITEM branch. On an UPDATE
	-- `steam_id` is already set, so it takes the `else` (`params.publish = false`)
	-- and NEVER saves. Paradox's `mod:SaveWholeMod()` (`:173`) is unconditional.
	-- ⇒ one save per sitting, Paradox's, and Steam packs the tree AFTER it.
	-- ⛔ The table in `PORTAL_PREP` §0.5(c) describes a **first** upload and says
	-- so; a session read it as a general rule on 2026-08-29 and concluded Steam
	-- had never been updated. It had. ⇒ the ONLY controls are the store's own
	-- change notes and the SUBSCRIBED archive — never this file. `EF-068`.
	'version_major', 1,
	'version', 7,
	'lua_revision', 350453,
	'saved_with_revision', 403908,
	-- saves made with the pack load fine without it (FIX_POLICY §3), so don't
	-- nag players who removed it with the missing-mods prompt
	'optional_mod', true,
	-- ⛔ NO `default_options` FIELD, AND THAT IS THE POINT (2026-08-12, the
	-- opt-in split). This field is what makes Options → Mod Options list a mod
	-- at all (ModDef:HasOptions reads it, Mod.lua:473-475). The pack's eight
	-- optional modules — and every toggle and dial they owned — moved to the
	-- standalone Community Opt-In Pack (SMR_CommunityOptInPack), so this pack
	-- has nothing for a player to set and correctly stops appearing on that
	-- page. 00_Core.lua keeps its `optional`/OptionEnabled/ApplyModOptions
	-- machinery: dormant, not wrong, and not worth an unforced edit to the one
	-- file every fix depends on.
	'code', {
		"Code/00_Core.lua",
		"Code/Fix_NightShiftWork.lua",
		"Code/Fix_WispRewards.lua",
		"Code/Fix_TrainsToVoid.lua",
		"Code/Fix_LanderEmptyLaunch.lua",
		"Code/Fix_ShelterReflex.lua",
		"Code/Fix_BrokenTrackSalvage.lua",
		"Code/Fix_TrackSalvageWipe.lua",
		"Code/Fix_LakeEntombment.lua",
		"Code/Fix_GhostFarmOxygen.lua",
		"Code/Fix_RocketDroneChurn.lua",
		"Code/Fix_TradeRocketFuelRefresh.lua",
		"Code/Fix_ShuttleTransportCache.lua",
		"Code/Fix_VacuumWalks.lua",
		"Code/Fix_ArrivalDeaths.lua",
		"Code/Fix_StaleReservations.lua",
		"Code/Fix_CrystalMysteryHang.lua",
		"Code/Fix_DomeOverviewHighlight.lua",
		"Code/Fix_TrainCargoDumping.lua",
		"Code/Fix_DestroyedTunnels.lua",
		"Code/Fix_DustSicknessBiorobots.lua",
		"Code/Fix_GeneForging.lua",
		"Code/Fix_MirrorSphereSite.lua",
		"Code/Fix_PayloadTemplateRefill.lua",
		"Code/Fix_ShuttleHubOffAvailable.lua",
		"Code/Fix_FreedHousingNotice.lua",
		"Code/Fix_DomeFreeSpaceMismatch.lua",
		"Code/Fix_LandscapeUnitFilter.lua",
		"Code/Fix_RocketInteractGuard.lua",
		"Code/Fix_TrackConnectorPingPong.lua",
		"Code/Fix_TrackTunnelPowerBridge.lua",
		"Code/Fix_GraphConsumedCaption.lua",
		"Code/Fix_TrainWaitTime.lua",
		"Code/Fix_FounderTraitNotification.lua",
		"Code/Fix_SequenceLatents.lua",
		"Code/Fix_TrackSalvageRefund.lua",
		"Code/Fix_LayoutTechLock.lua",
		"Code/Fix_DroneTransportMinors.lua",
		"Code/Fix_AnomalyCaveInMap.lua",
		"Code/Fix_BombardmentSpread.lua",
		"Code/Fix_ExtenderFlapChurn.lua",
		"Code/Fix_SaintBlessing.lua",
		"Code/Fix_SinkholeIndestructible.lua",
		"Code/Fix_ExoticDepositSign.lua",
		"Code/Fix_JumboCaveReinforcementWedge.lua",
		"Code/Fix_SilentHitMomentFX.lua",
		"Code/90_SaveSanitizer.lua",
	},
	-- ⭐⭐ WRITTEN BY THE UPLOADS, 2026-08-20 — THESE ARE HOW EVERY FUTURE UPDATE
	-- FINDS THE PUBLISHED LISTINGS. ⛔ Losing them means a later release cannot
	-- target the live mod and would create a SECOND listing instead.
	--   `saved` / `code_hash` / `saved_with_revision` are the editor's own
	--   bookkeeping; `code_hash` is what the dirty check compares against
	--   (`GedEditedObject:IsDirty`), so it is kept exactly as written.
	--   `pdx_id` 156049 — the Paradox Mods listing.
	--   `pdx_version` — ⛔ NOT ours at all: `mod.pdx_version = res.Version`
	--   (`ParadoxMods.lua:172`), the number the PORTAL returns from the upload —
	--   its own revision counter, which is why it reads 1, 2, 3, 4 across our
	--   four uploads. ⚠️ It is NOT what the page shows as MOD VER: that is
	--   `VersionDisplayName = tostring(mod.version)` sent at `:156`, i.e. the
	--   version BEFORE `:173`'s save bumps it. The in-game browser renders the
	--   real PackVersion from the archive. (Gloss corrected 2026-08-29 — the
	--   previous two wordings, including one written that morning, both had it
	--   as our own `version`.)
	--   `steam_id` "3787202810" — the Steam Workshop item.
	-- ⚠️ Every comment in this file and in `items.lua` is STRIPPED by the forced
	-- saves and restored here from git in the same commit. ⭐ IT HAS NOW HAPPENED
	-- THREE TIMES (2026-08-20, -08-24, -08-28) — it is not an incident, it is the
	-- writeback step (`reports/RELEASE_PORTAL_PREP.md` §0.5(e)), and a dirty tree
	-- after a sitting is the EXPECTED state, not a mistake by whoever worked last.
	-- ⚠️ `saved_with_revision` now sits further up, beside `lua_revision`, because
	-- `SaveDef` writes the fields in its own order; it is the same editor bookkeeping.
	'saved', 1789081139,
	'code_hash', -3234475764633111646,
	'pdx_id', 156049,
	'pdx_version', "6",
	'steam_id', "3787202810",
	'TagGameplay', true,
})
