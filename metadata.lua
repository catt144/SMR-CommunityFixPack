local def = PlaceObj('ModDef', {
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
	-- ⭐ 2026-09-11, v8 words: Forty-eight → FIFTY (F119 + C86; one headliner, the trade-rocket
	-- bullet). Shipped in v8 the same afternoon (Steam page read: count word Fifty).
	-- ⭐ 2026-09-11 (later): FIFTY → FORTY-NINE — F60 retired (`9bc4360`, count `0392162`).
	-- Headliners unchanged: F60 never had one, and F59's bullet stays true. Ships in v9.
	-- ⭐ 2026-09-12 for v10 (`RELEASE.md` step 1 over the outbox's Held + 3 Pending):
	-- count word STAYS Forty-nine — F37, F43 and F31 retire (−3) and C85, C88, C89 land
	-- (+3). ⛔ Re-derived from the site list (`grep -c '^??? '` = 49, section tally sums),
	-- NOT carried: `WORDING_RULED.md` predicted Forty-six from the retirements alone.
	-- Headliners 21 → 20: F37's farm-oxygen and F31's stopped-story bullets OFF, F58's
	-- bullet re-worded to the ruled headline, C85's dust-storm bullet ON (two player
	-- reports, a visibly stuck building — clears §2's recognisable bar). C88 and C89 stay
	-- in the "… and a good deal more" tail. Intro: F21's Comfort example → the train
	-- travel-time one (ruled), and "three of them you cannot see" → "two" (F43 leaves
	-- that set). `short_description` untouched — it states no count and no claim that moved.
	-- ⭐ 2026-09-16 for v11 (`release_prompt.md` §1, the outbox's three Pending entries): count word
	-- Forty-nine → FIFTY-TWO — C93, C95, C96 land, nothing retires. ⛔ Re-derived from the site list
	-- (`^??? ` rows = 52, section tally 2+15+4+6+9+6+6+2+2 sums), not carried. Headliners 20 → 21:
	-- C93's ranch bullet ON (two independent player reports, food visibly stranded — the C85 bar).
	-- C96 (one report) and C95 (a judgment call; its row belongs on the fix list) stay in the tail.
	-- ⭐ 2026-09-17 for v12 (`release_prompt.md` §1, the outbox's C95/C102 entry and the owner's
	-- store-card task): count word Fifty-two → FIFTY-THREE — C102 lands as a new row and C95's
	-- existing row turns from a judgment call into a plain repair; nothing retires. ⛔ Re-derived
	-- from the site list (`^??? ` rows = 53, section tally 2+16+4+6+9+6+6+2+2 sums), not carried.
	-- ⚖️ OWNER'S TASK, decided 2026-09-17: headliners 21 → 14. Seven bullets cut, each with its
	-- reason recorded in the outbox (a premise the module's own header says narrowed on 1.1.0; a
	-- symptom the word "paralysed" outran; one nobody noticed; one provable only by console read;
	-- one already covered by the two salvage lines; a side-panel tint with a known PT-09 regression;
	-- and one the owner judged long and only alright). ⛔ The remaining 14 were verified true the
	-- same day — each has a module in Code/ registered in this file's code list, none rests on a
	-- retired, parked or opt-in fix. Do not re-QA them and do not reword them.
	-- Also ruled the same day: a FEATURED section for C95 above the headline list, from the owner's
	-- approved draft — including the gotcha paragraph, which names the game's own safety system as
	-- the thing choosing where a homeless colonist goes and says we do not override it; the
	-- "… and a good deal more" tail sentence CUT (the heading already says "some", and the full
	-- list is linked); and the 1.0.7 section MOVED to the very bottom, after FOR MODDERS.
	-- Net length 6,376 → **6,551** (+175) — a small increment over a body that demonstrably went
	-- through the upload path at v11, which is the only length data point that matters here.
	'description', "Bug fixes for Surviving Mars: Relaunched.\n\nForty-three repairs, each one written up on the fix list with what you would\nhave seen and what was actually wrong. Every one targets something the game's\nown code gets wrong — the code says one thing, does another, and the fix makes\nit do what it says. It fixes bugs; it does not rebalance the game. Preferences\nand features are deliberately not in it.\n\nSome of them you could hardly miss: an entire train line and every train on it\ndeleted by salvaging a single hex, colonists suffocating on a walk between two\ndomes, an artificial lake burying the rover that was building it.\n\nMore of them you would never have blamed on a bug, because the game looked\nperfectly normal while the arithmetic underneath it was wrong — a researched\nbreakthrough the game restored to only one of the three wind turbine types it\ncovers, a track refund that paid a stub's worth of Metals however long the line\nwas, a water saving a technology promised that four of the farms it names never\nreceived.\n\nAnd two of them repair things you cannot see at all today: real defects that\nthe shipped numbers happen to hide, which another mod, a game patch or a DLC\ncould walk straight into.\n\nSOME OF WHAT IT FIXES\n\n· Colonists walked across the surface between domes and suffocated.\n· Rocket loads of new arrivals died on their way to a dome.\n· New arrivals moved into a dome that was switched off, quarantined or without air.\n· A bed that fell vacant sat empty while colonists were homeless.\n· Building an artificial lake buried the rover that built it.\n· Salvaging one piece of track deleted the whole line, and its trains with it.\n· Automatic rockets and landers took off with nothing aboard.\n· A Jumbo Cave mystery could get stuck clearing waste rock and never complete.\n· The Philosopher's Stone mystery hung one step from the end.\n\nBUGS, QUESTIONS AND MODDING\n\nFound a bug, or one this pack did not fix? Want the details behind a fix, or to\nknow how the pack gets along with your own mod? It is all on the pack's site.\nBugs can be reported there from a browser, with no account needed, and a save\nor a log can be attached privately. If this page has a comment section, that\nworks too. Still on game version 1.0.7? A frozen build for it is there too.\nhttps://catt144.github.io/SMR-CommunityMods/\n\nFEATURED: EXPEDITION CREWS COME HOME\n\nColonists living in habitats can join expeditions again, and they come back to\nthe habitat they left. If their habitat is too far from the landing site to\nwalk, they are set down at its door, the same way the rocket picked them up. If\nthe habitat is gone or unusable, they go to the nearest dome that is working and\nhas air.\n\nOne gotcha. If every dome is switched off and only habitats are alive, and those\nhabitats refuse the colonist through their filters, the colonist still walks to\nthe nearest dome and dies there. That is the game's own safety system choosing\nwhere a homeless colonist goes, and this mod does not override it. Changing it\nwould mean rewriting how the game houses colonists, which is not what a bug-fix\nmod should do.\n\nFEATURED: SEVEN MACHINES THAT WORKED IN SILENCE\n\nThe Rare Metals Extractor's hammer, the MOXIE, the Water Extractor, Shuttle Hub\nshuttles, the RC Driller, the RC Dozer and The Excavator all had sounds or\neffects made for them that never played. They play now.\n\nTwo of them also have a skin that is silent by design, so if one of these stays\nquiet, check its skin before you blame the fix:\n· Rare Metals Extractor — the hammer strikes and puffs steam; the drill never\n  strikes. NASA, SpaceY, BlueSun, Brazil, Roscosmos, Japan and ISRO colonies\n  get the drill by default.\n· MOXIE — the double-pump skin thumps and puffs; the blocky one is silent.\n\nSelect the building and press Change Skin (the paintbrush on its panel) to\nswitch. The screenshots on this page show which skin is which.\n\n\nHOW IT WORKS\n\n· No game files are modified. The pack wraps the game's own code while it runs.\n· Safe to add to a save you have already played. It writes almost nothing into\n  your savegame, and removing it simply lets the original bugs come back.\n· Every fix checks the game's code before it touches anything, and stands down\n  by itself if what it was written for has been renamed, removed or reshaped.\n  A fix that stands down does nothing at all — it never guesses. Every game\n  patch is read against the pack as well, and the fixes it changed are updated\n  or retired.\n· A few of the fixes are judgment calls rather than plain repairs. Those are\n  marked as such on the fix list, with the reasoning, rather than folded in\n  quietly.\n",
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
	-- ══ `last_changes` — what this field IS, and the standing rules for writing it ══
	-- Per-version drafting history for v6-v14 is NOT kept here any more: it lives in
	-- `docs/archive/RELEASE_HISTORY.md` (what each release shipped) and
	-- `docs/agent/reports/STORE_CARD_LIVE.md` (the words, and what was read back live).
	-- This block was rewritten wholesale 2026-09-23 for v15; the one it replaced still
	-- gated on a fix module this release deletes, and on a stale body-replacement count.
	--
	-- ⛔ IT IS NOT A DESCRIPTION — it is the PER-VERSION CHANGE-NOTE ENTRY on BOTH
	-- storefronts, sent automatically at upload and archived there forever:
	--   Paradox  `ChangeLog = last_changes`   (`ParadoxMods.lua:151`)  -> CHANGELOG panel
	--   Steam    `change_note = last_changes` (`SteamWorkshop.lua:114`) -> Change Notes tab
	-- ⇒ three consequences. (1) REWRITE IT WHOLESALE BEFORE EVERY upload, never append,
	-- or the next upload posts a duplicate entry under a new version. (2) Keep it TERSE
	-- — the house style on both stores is a dashed line or two. `lines = 3`
	-- (`Mod.lua:254`) is the Ged text-box HEIGHT and truncates nothing, so more bullets
	-- are allowed where disclosure needs them: terseness loses to disclosure, never the
	-- other way round. (3) It is HISTORICAL — it describes the version it ships with,
	-- forever, so never write it in the present tense of the pack as a whole.
	-- ⛔ DO NOT "REPAIR" THIS STRING IN PLACE after an upload. Rewriting it does not
	-- edit the entry already posted; it posts a duplicate under the next version.
	--
	-- Standing content rules:
	-- ⛔ No fix ids, no module names, no load-order advice, no other mod named
	--   (EF-054, FIX_POLICY §8).
	-- ⛔ No carried count. The one number this note may state is the fix-list total, and
	--   it is RE-DERIVED in the same commit with `grep -c '^??? ' content/fix-list.md`
	--   — never carried, never arithmetic on a previous total. The judgment-call count
	--   is recounted the same way (`grep -c '^??? question'`), never from a comment.
	-- ⛔ A note that says "Fixed" is a CLAIM, false until we have confirmed it ourselves
	--   (owner rule 2026-09-08). Say what was watched; say plainly what was not.
	-- ⚠ Player-visible LOSSES are STATED, not dropped quietly — a retirement, a
	--   narrowed fix or a known issue belongs in the note the player actually reads.
	-- ⛔ A defect in one of OUR OWN fixes, found and repaired before it ever reached a
	--   player, is deliberately ABSENT: naming it would describe a problem nobody had.
	--   (Ruled for F107.)
	-- ⛔ Do NOT resurrect the withdrawn low-Food-warning loss claim: 1.1.0 REPLACED both
	--   warnings (`StarvingColonists`, `MaintenanceStuckBuildings`), so telling players
	--   they now get none is FALSE.
	-- Licence for editing this string: the owner's standing 22b word ("change any
	-- wordings to their accurate versions"); text-only, no behaviour. The editor/version
	-- rail (`release_prompt.md § Release rails`) leaves the version bump to the upload
	-- sitting — never hand-set a version field here.
	--
	-- ⭐ SHIPPED TEXT IS THE OWNER'S BOX TEXT, not the tree draft — v9, v11, v12 and v14
	-- all differ from what was drafted here, because the owner edits the Ged box at the
	-- upload sitting. The serializer strips comments and rewrites values; it does not
	-- delete a sentence from the middle of a field. So after an upload this file records
	-- WHAT POSTED, never what was drafted; the draft is in the pre-upload commit.
	--
	-- ⭐ WRITTEN 2026-09-24 for v16 (`release_prompt.md` §1, from `RELEASE_OUTBOX.md`).
	-- The hub set: five new rows (C114, C115, C116, C117, C111) and one respecified row
	-- (F127 inside C83's arrivals row, our own defect that shipped, so it is stated). The
	-- number is re-derived from the file (`grep -c '^??? '` = 43; 38 -> 43). What each line
	-- may claim follows the entries' evidence: C114 and C117 were read working in play on
	-- both builds (07B, instrument- and log-read, not owner-watched), so "seen working in a
	-- running game"; C111 was owner-watched; C115, C116 and F127 were never exercised in
	-- play, so the last line says so plainly. C111's `Untranslated` line is disclosed.
	'last_changes', "Five repairs added, most of them around passage hubs and shuttle rescues.\n\n-A colonist on a passage hub, or crossing one of its passages, next to a large dome now walks into that dome instead of being sent a rescue shuttle. Seen working in a running game.\n-Salvaging one passage of a busy hub now lets the colonists crossing it arrive before it disconnects, instead of leaving them outside at the hub. Seen working in a running game.\n-A colonist who has already made it home no longer walks back outside to wait for a rescue shuttle booked earlier.\n-A colonist who has left a passage hub is no longer treated as sheltered by it.\n-A rescue back to a colonist's own dome now reads \"Returning to Dome\" instead of \"Moving to a new Dome\". Seen in a running game. The new line is in English in every language for now.\n-When new arrivals are redirected from a dome that cannot take them, the bed held for them there is now released instead of sitting empty.\n-The rescue shuttle, hub shelter and bed repairs have not been watched happening in a running game yet.\n\nThe fix list goes from thirty-eight to forty-three.",
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
		"*/.agents/*",
		"*/.claude/*",
		"*/tools/*",
		"*README.md",
		"*CLAUDE.md",
		"*AGENTS.md",
		"*.gitignore",
		"*.rgignore",
		"*.gitattributes",
		"*/store_screenshots/*",
		-- 2026-09-16: the owner's private folder holds junctions to Claude session
		-- transcripts; the packer walks through junctions. Never ship it.
		"*/zz-owner/*",
		-- 2026-09-17: junctions to the owner's save folders plus reporter saves.
		"*/saves/*",
		-- 2026-09-21: durable in-tree material that must not ship (owner
		-- ruling on where non-repo material lives; local/README.md is the gate).
		"*/local/*",
		-- 2026-09-21: agent/subagent working space, git-ignored, swept at 14 days.
		"*/scratch/*",
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
	-- 2026-09-11 (v8, F119 + C86): version 7 → 8, `pdx_version` "6" → "7". ⚠️ That writeback
	-- was committed with every comment in this file and `items.lua` STRIPPED (`9bc4360`);
	-- restored by merge the same night (v8 close-out inside the `RELEASE.md` run for v9).
	-- The comments are the record; a SaveDef round-trip always deletes them (POST_UPLOAD_CLOSE).
	-- 2026-09-12 (v9, F59 repair + F60 retirement): version 8 → 10 (TWO saves this sitting —
	-- ck71: never chase the gap), `pdx_version` "7" → "8". Writeback committed STRIPPED again,
	-- inside a card edit (`1583dcd`); restored by merge on 09-12 (v9 close-out, `smr-bugfixpack-d0`).
	-- The shipped `last_changes` below is the owner's box text as uploaded (em-dashes, no space
	-- after the bullet dash) — it differs from the tree's draft and is kept as shipped.
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
	-- 2026-09-13 (v10, C85 + C88 + C89 landed, F37/F43+F118/F31 retired): version 10 → 11,
	-- `pdx_version` "8" → "9". Both portals ran this sitting (owner's word). Writeback
	-- committed STRIPPED again by the forced save; restored here (POST_UPLOAD_CLOSE).
	-- 2026-09-16 (v11, C93 + C95 + C96 landed): version 11 → 14 (three saves this sitting — ck71:
	-- never chase the gap), `pdx_version` "9" → "10". Both portals ran (owner's word). Stripped by
	-- the forced save and restored in the close-out, before any other commit. The shipped
	-- `last_changes` is the owner's box text as uploaded; it differs from the tree's draft and is kept.
	'version_major', 1,
	'version', 21,
	'lua_revision', 350453,
	'saved_with_revision', 405907,
	-- saves made with the pack load fine without it (FIX_POLICY §3), so don't
	-- nag players who removed it with the missing-mods prompt
	'optional_mod', true,
	-- ⛔ 2026-08-12 (the opt-in split): this pack had NO `default_options` FIELD,
	-- AND THAT WAS THE POINT. This field is what makes Options → Mod Options list a
	-- mod at all (ModDef:HasOptions reads it, Mod.lua:473-475). The pack's eight
	-- optional modules — and every toggle and dial they owned — moved to the
	-- standalone Community Opt-In Pack (SMR_CommunityOptInPack), so this pack
	-- had nothing for a player to set and correctly stopped appearing on that
	-- page. 00_Core.lua kept its `optional`/OptionEnabled/ApplyModOptions
	-- machinery: dormant, not wrong, and not worth an unforced edit to the one
	-- file every fix depends on.
	-- ⭐ 2026-09-25 (LOAD_ORDER_FIRST, owner's choice of option B): the condition
	-- that ruling was made under no longer holds — the pack now has ONE thing a
	-- player may set, the opt-out of the load-order promotion (01_LoadFirst.lua),
	-- and a player opt-out is a FIXED requirement of that brief. So the field is
	-- back with exactly that one key, the pack lists on the Mod Options page
	-- again, and the dormant reconciler in 00_Core.lua is what drives the toggle.
	-- The key must equal the Register id, the items.lua toggle name and the
	-- `default_options` key, the rule the opt-in pack kept (its FIX_POLICY §5).
	-- SaveDef regenerates this table from the ModItemOptionToggle in items.lua.
	'default_options', {
		LoadFirst = true,
	},
	'code', {
		"Code/00_Core.lua",
		"Code/01_LoadFirst.lua",
		"Code/Hubset_OnHubNow.lua",
		"Code/Fix_LanderEmptyLaunch.lua",
		"Code/Fix_ShelterReflex.lua",
		"Code/Fix_TrackSalvageWipe.lua",
		"Code/Fix_LakeEntombment.lua",
		"Code/Fix_RocketDroneChurn.lua",
		"Code/Fix_ShuttleTransportCache.lua",
		"Code/Fix_VacuumWalks.lua",
		"Code/Fix_ArrivalDeaths.lua",
		"Code/Fix_PassageHubSalvageDrain.lua",
		"Code/Fix_HubLocalAccess.lua",
		"Code/Fix_HubMarkerDeparture.lua",
		"Code/Fix_RescueReturnText.lua",
		"Code/Fix_ObsoleteHomeRescue.lua",
		"Code/Fix_StaleReservations.lua",
		"Code/Fix_CrystalMysteryHang.lua",
		"Code/Fix_DustSicknessBiorobots.lua",
		"Code/Fix_PayloadTemplateRefill.lua",
		"Code/Fix_ShuttleHubOffAvailable.lua",
		"Code/Fix_FreedHousingNotice.lua",
		"Code/Fix_LandscapeUnitFilter.lua",
		"Code/Fix_RocketInteractGuard.lua",
		"Code/Fix_TrackConnectorPingPong.lua",
		"Code/Fix_TrackTunnelPowerBridge.lua",
		"Code/Fix_SequenceLatents.lua",
		"Code/Fix_TrackSalvageRefund.lua",
		"Code/Fix_DroneTransportMinors.lua",
		"Code/Fix_ScanDowngrade.lua",
		"Code/Fix_BombardmentSpread.lua",
		"Code/Fix_ExtenderFlapChurn.lua",
		"Code/Fix_SaintBlessing.lua",
		"Code/Fix_ExoticDepositSign.lua",
		"Code/Fix_JumboCaveReinforcementWedge.lua",
		"Code/Fix_SilentHitMomentFX.lua",
		"Code/Fix_CloggedBuildingRelease.lua",
		"Code/Fix_FactionDomeSizeGate.lua",
		"Code/Fix_HabitatExpeditionReturn.lua",
		"Code/Fix_HabitatExpeditionDraft.lua",
		"Code/Fix_RoverSubclassManifest.lua",
		"Code/Fix_DryFarmingFarms.lua",
		"Code/Fix_WildfireCureVisit.lua",
		"Code/Fix_GhostPowerCells.lua",
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
	'saved', 1790306966,
	'code_hash', 7113849772352010722,
	-- ⭐ ADDED 2026-09-10 (owner: the card should point players at pictures of the two
	-- skins) — the store GALLERY. Both uploaders read screenshot1..5: the Mod Editor copies
	-- each to TmpData/ModUpload/Screenshots as `ModScreenshot_<name>` (GedModEditor.lua:
	-- 687-702); Paradox uploads them (ParadoxMods.lua:97-110, :159); Steam adds/updates/
	-- removes ONLY `ModScreenshot_*` previews and never touches images added by hand on the
	-- page (SteamWorkshop.lua:43-81). Caps: Steam 1 MB each (SteamWorkshop.lua:85, :101),
	-- Paradox 2 MB (ParadoxMods.lua:87, :101) — the owner's ~2 MB PNGs would fail, so
	-- `tools/store_screenshots.py` re-encodes them (~350 KB JPEGs) from the marked-up
	-- originals in <parent>\SMR-ScreenCaptures\c74_skins. `Mod/`-prefixed like 'image', so
	-- FixRelativePaths skips them (Mod.lua:579) and the mod stays CLEAN; `ignore_files`
	-- keeps store_screenshots/ OUT of the player's pack (`tools/pack_predict.py` shows it).
	'screenshot1', "Mod/SMR_CommunityFixPack/store_screenshots/1_rare_metals_drill_skin.jpg",
	'screenshot2', "Mod/SMR_CommunityFixPack/store_screenshots/2_rare_metals_hammer_skin.jpg",
	'screenshot3', "Mod/SMR_CommunityFixPack/store_screenshots/3_moxie_skins.jpg",
	'pdx_id', 156049,
	'pdx_version', "15",
	'steam_id', "3787202810",
	'TagGameplay', true,
})
-- ⭐ C CANARY (LOAD_ORDER_FIRST, 2026-09-25; owner's design). Hand-written code
-- beyond the declared properties, in the shape of option C's bootstrap (the def
-- held in a local, extra statements, then returned) but INERT: a local nothing
-- reads, no method override, no field written on the def, no effect on loading.
-- Its one job is to show, after the next upload, whether code of this shape
-- survives the Mod Editor's regeneration of this file (ModDef:SaveDef,
-- Mod.lua:973-993, serialises declared properties only). Prediction: stripped
-- from the tree by the upload's forced save and absent from the Steam package.
-- The check, three parts, is in docs/agent/reports/LOAD_ORDER_FIRST_BUILD_2026-09-25.md,
-- "The C canary"; the release outbox names it. metadata.lua runs in an env that
-- holds only PlaceObj and box (Mod.lua:1715-1724), so it cannot log a line.
local SMRFixPack_LoadOrderCanary = "SMRFP-LOADORDER-CANARY-2026-09-25-b7e1"
return def
