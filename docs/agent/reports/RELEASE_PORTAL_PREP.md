# Portal prep — the sheet for the launch sitting (④)

> ⛔⛔ **REWORKED 2026-08-17 — THE FIX PACK LAUNCHES ALONE** (owner ruling,
> checklist 35). The opt-in mod is not ready and does not publish; Save Rescue
> was already hold-off (17). **④ is now a ONE-mod sitting: upload the fix pack
> → its store link into the site → Pages.** Opt-in rows below are struck or
> marked *PARKED*, never deleted — they are the record for the day it ships.
> Every removed player-facing passage: `PARKED_OPTIN_REFERENCES.md`.
> ✅ **The version call is RULED AND APPLIED — 2026-08-17, owner: "lets go
> with 1.0.0."** `metadata.lua` now `version=0` ⇒ renders **1.0.0**; the tag
> moved with it (`fixpack-v1.0.0`). ④ owes no decisions.
> ⭐ **RENAMED 2026-08-17 (owner ruling, checklist 36): the product you are
> uploading is "Relaunched Fix Pack"** — `metadata.lua` `title` already says
> so; if the portal asks for a display name separately, type exactly that.
> The mod `id` (`SMR_CommunityFixPack`) and the `[CommunityFixPack]` log tag
> deliberately did not change, and the GitHub repos keep their names — repo
> URLs reading `SMR-CommunityFixPack` under a mod called *Relaunched Fix Pack*
> is normal, product names and repo names differ constantly.

**Built 2026-08-14 by `agent/prompts/release-3/01_BUILD_DESCRIPTIONS.md`, Job 3.**
Read top to bottom. Everything below was measured or re-derived this session;
⛔ nothing was copied from `STATE.md`.

⛔ **No agent publishes anything** (chain rule 5). Every action on this sheet is
yours.

---

## 0. ⛔ READ THIS BEFORE YOU BOOK THE AFTERNOON

**Two things can stop ④ from finishing, and one of them is not a decision.**

### (a) ✅ The preview art EXISTS and is CHOSEN — the blocker is cleared

You ruled the floor (checklist 24: text-on-image), the agent painted six
candidates without opening the game (designed Mars backdrops, no screenshot
needed), and **you picked C1 for both mods, 2026-08-14**. The files to upload:

* `docs/agent/reports/preview_art/FINAL_fixpack_preview.png` (40 KB)
  ⭐ **2026-08-17, at the sitting: this is now WIRED IN, not just chosen.** It was
  copied to the mod root as `preview.png` (1024×1024, 44,322 bytes) and
  `metadata.lua` gained `'image', "Mod/SMR_CommunityFixPack/preview.png"` —
  ⛔ without it the Paradox upload is hard-rejected before it packs anything
  (§0.5(a)). The `preview_art/` copy stays as the record; the root copy is what
  ships (packaging **79 → 80**, §4).
* ~~`docs/agent/reports/preview_art/FINAL_optin_preview.png` (37 KB)~~ —
  *PARKED 2026-08-17: not uploaded at this launch; stays chosen for the day
  the opt-in ships*

Both 1024×1024, far under the recorded limits (**Paradox Mods ≤ 2 MB, Steam
≤ 1 MB**). The four unchosen candidates stay in the same folder as alternates.

⭐ **RE-LETTERED 2026-08-17 for the rename** — the art itself had the old name
painted in (the fix-pack title read "COMMUNITY / FIX PACK"; the opt-in's kicker
read "COMMUNITY FIX PACK"), a surface no text grep could see. Both FINAL files
now carry **RELAUNCHED FIX PACK** in the same C1 design: only the affected text
line was repainted (background rebuilt, star field preserved from the same
image, typeface matched to the original — Bahnschrift SemiBold Condensed,
0.90 IoU against the untouched "FIX PACK" line). The 2026-08-14 originals are
preserved beside them as `fixpack_C1_communityname_2026-08-14.png` /
`optin_C1_communityname_2026-08-14.png`. ⚠️ The four unchosen alternates keep
the old lettering on purpose (they are the record of the candidates offered);
re-letter before use if one is ever promoted.
ℹ️ The floor stays replaceable: if a capture sitting ever produces real vistas
(Pass G), the same lettering drops onto one and the portal image is swapped —
costs nothing, touches nothing else. No rescue-mod art exists or is needed
(17 hold-off); if the contingency fires, the C1 template makes a third in
minutes.

⚠️ **One catch on ever swapping that image later (`C52`, filed 2026-08-16): the
in-game mod browser caches preview thumbnails keyed on mod id + version only,
with no revalidation** (`ParadoxMods.lua:221-225`). Replace a preview after
publication *without a version bump* and every player who has already seen the
old image keeps it permanently; new players get the new one. So a post-launch
art swap should ride a version bump — which any real update gives you for free.
Upload-day choice of image is unaffected.

### (b) + (c) ✅✅ ALL FIVE CALLS RULED 2026-08-14 AND APPLIED — nothing here waits on you any more

| item | ruling | applied |
|---|---|---|
| **29** the notice paragraph | **STRIKE** | ✅ deleted from both cards, the rescue card, the assembly and the site FAQ; source records corrected |
| **17** Save Rescue publish | **HOLD OFF** — reserve; launch only if post-release reports show players stuck with dial residue | ✅ fill-in marker + assembly section deleted per defaults; card kept as the ready contingency draft |
| **28** the rescue dialog | closes with 17: **ship as built** — re-decide (incl. the save-step line) before upload if the contingency fires | ✅ recorded on item 17 |
| *cleanliness sentence* | **Reading A — the pack alone** | ✅ no text change; the card's deliberate absence stands |
| *opt-in version* | **1.0** | ✅ `metadata.lua` set to 1.0.0 |

⇒ ~~**④ is now decision-free AND art-complete: upload two mods (with their FINAL
previews from §0(a)) → links → Pages.**~~ ⚖️ **SUPERSEDED 2026-08-17: upload ONE
mod (the fix pack, with its FINAL preview) → link → Pages.** ✅ The version call
that briefly reopened ④ was ruled the same day (1.0.0, banner above) — **④ is
decision-free again.**

---

## 0.5 ⛔⛔ UPLOAD MECHANICS — READ BEFORE YOU OPEN THE MOD EDITOR (added 2026-08-17 at the sitting)

**Three things about the game's own upload code decide whether you ship 1.0.0 or
1.0.1, and none of them were on this sheet before.** All read at Src, by symbol.

### (a) ✅ FIXED THIS SITTING — the upload would have been hard-rejected

`metadata.lua` had **no `image` field at all**, and `ParadoxMods.lua:39-42`
fails the upload before it packs anything: *"Missing mod Preview image"*. Steam
does not reject, but uploads with no thumbnail (`SteamWorkshop.lua:113`).
⇒ The chosen art is now wired in: `preview.png` at the **mod root**, referenced
as `'image', "Mod/SMR_CommunityFixPack/preview.png"`.

⚠️ **It was written BY HAND, on purpose — do not re-set it in the Mod Editor.**
`content_path` is `ModContentPath .. id .. "/"` (`Mod.lua:1758`) and the folder is
mounted there (`:859-860`), so that path resolves; and because the string starts
with `Mod/`, `FixRelativePaths` skips it (`:577`) and nothing is rewritten in
memory on load. **The mod therefore loads CLEAN** — which is the entire point,
per (b).

### (b) ⛔⛔ EVERY MOD EDITOR SAVE BUMPS THE VERSION

`ModDef:SaveDef` runs **`self.version = self.version + 1`** (`Mod.lua:967`) on
every save that is not `serialize_only`. Our `version=0` ⇒ a single save ships
**1.0.1**, against the owner's ruled 1.0.0, and orphans the `fixpack-v1.0.0` tag.
`ValidateModBeforeUpload` *forces* that save if the mod is dirty
(`GedModEditor.lua:836-844`), and a save also **regenerates `metadata.lua` from
memory — every hand-written comment in it is lost**. ✅ `ignore_files` SURVIVES
(a real saved property, `Mod.lua:255`), so item 23 is not at risk.

⇒ **At the editor, before pressing anything: confirm the version reads 1.0.0 and
the preview thumbnail is populated. If you are prompted *"The mod needs to be
saved before uploading"*, STOP** — something dirtied the mod and the number is
about to move.

### (c) ⛔⛔ THE TWO PORTALS SAVE AT DIFFERENT MOMENTS ⇒ PARADOX GOES FIRST

Both portals call `SaveWholeMod()` unavoidably on a *first* upload (`steam_id`
defaults to 0, `SteamMods.lua:50-61`; `pdx_id` unset). **But not at the same
point in the sequence, and that decides what is inside the package:**

| portal | when it saves | what the portal receives |
|---|---|---|
| **Paradox Mods** | **AFTER** the content upload returns — `mod.pdx_id = res.ModId; mod:SaveWholeMod()` (`ParadoxMods.lua:167-173`) | ✅ the pack is built from the tree **exactly as tagged, at 1.0.0** |
| **Steam Workshop** | **BEFORE** packing — `Steam_PrepareForUpload` creates the item then saves (`SteamWorkshop.lua:17-22`), and `CreatePackageForUpload` runs after | ⛔ the bump is **inside** the package ⇒ ships **1.0.1** |

⇒ ⛔ **Paradox Mods first is not a preference.** Steam first would bump the tree
to 1.0.1 and Paradox would then receive 1.0.2.

**After the Paradox upload the tree sits at `version=1`.** For Steam to also ship
1.0.0: close the game, set `version = -1` on disk, relaunch — Steam's forced save
lands it on 0 and packs 1.0.0. ⚖️ **Owner's call**; the alternative is accepting
Steam at 1.0.1, and it can be decided after Paradox is done. ⛔ Do not run both
uploads in one session without deciding: Steam would ship **1.0.2**.

⚠️ **Cosmetic, but you will see it.** Paradox is sent
`VersionDisplayName = tostring(mod.version)` (`ParadoxMods.lua:156`) — the
**revision integer alone**, so the portal page gets `"0"`, not `"1.0.0"`. The
in-game browser renders the real 1.0.0 from `PackVersion`. Edit that field on the
portal page if it lets you.

### (d) ⚠️ CHECK AFTER THE PARADOX UPLOAD — the portal's "required game version" field (terminal audit, 2026-08-19)

The in-game browser's **"only compatible"** filter keys on a portal-side
`RequiredGameVersion` (`ModsUIIsModCompatible`, `ModManager.lua:230-234`:
`version >= ModMinLuaRevision and version <= LuaRevision`), and **the upload
code never sends one** (`RequiredGameVersion` appears nowhere in
`ParadoxMods.lua`'s upload params). Absent ⇒ the check reads `false` and the
pack is **hidden from any player who enables that filter** (default off,
`:908`, so most players are unaffected). ⇒ After the upload, look for a
required-game-version field on the portal page and set it to **350453** (the
value in our `metadata.lua` `lua_revision`, equal to this build's
`ModMinLuaRevision`, `Mod.lua:15`). If the portal has no such field, record
that here and move on — nothing else to do.

Related, recorded by the same audit (`reports/99_TERMINAL_AUDIT.md` §3b): the
engine never blocks a too-new mod on the **load** path (`IsTooNew` is
UI-only), so a player on an older game build loads the pack gated only by its
own shape checks. Reachability low (Steam auto-updates; the final SM patch is
years old); no action, recorded so nobody re-derives it.

### (e) ⭐ Two ids get written back, and they are how updates find the store entries

The forced saves write `pdx_id` / `PdxMod` / `pdx_version` and `steam_id` into
`metadata.lua`. **Commit them.** Losing them means a future update cannot target
the published mod. Restore the stripped comments from git in the same commit.

### (f) ⭐ CHECK AFTER EACH UPLOAD — the delivered bytes (verdict review, 2026-08-19)

Every byte-fidelity check in the release chain ends at the **local** `.fpk`.
Nothing verifies the leg the player actually receives: portal → download.

⛔⛔ **THE MD5 THIS CHECK USED TO NAME IS GONE, AND NO AGENT CAN SUPPLY THE NEW
ONE.** This step read *"md5 the download against `8dcb0692…`"* until 2026-08-20.
That hash belonged to the 08-17 archive of an 80-file tree; the close-out chain
added `Fix_LocalizedUIText.lua` and `Fix_SpaceYDroneCapBullet.lua`, so **the
pack you are about to build is a different file and would fail that check on a
perfectly correct upload.** A replacement hash exists only after *you* pack —
⛔ **never accept one written into this sheet by a session that did not compute
it from a real `.fpk`.**

⇒ **At the sitting, in this order:**

1. **When you pack** (Mods Manager → Edit → File → Pack Mod), before uploading,
   record the archive's own fingerprint here — it is the only reference the
   delivered-bytes check can have:

   | packed | md5 | bytes | entries |
   |---|---|---|---|
   | **2026-08-20 21:46:38** | **`6621384b99ff17b894ef4c1578fbb5e2`** | **391,567** | **82** |

   ✅ **FILLED IN AT THE SITTING, computed from the real archive** at
   `%LOCALAPPDATA%\Temp\Surviving Mars Relaunched\ModUpload\Pack\ModContent.fpk`
   — not predicted, not carried from any record. ⭐ **And it was reconciled
   against the tree in the same breath: `pack_list.py --tree .` reports
   `82 byte-identical to disk, 0 differ`**, both new modules among them
   (`Fix_LocalizedUIText.lua`, `Fix_SpaceYDroneCapBullet.lua`). ⇒ the artifact
   the portal receives IS the tagged tree, entry for entry.
   *(sha256 first 32, if a portal ever offers that instead:
   `4b03f079413927d30c4986cd3f229f2e`)*

   The expected **entry count is 82** — `python tools/pack_predict.py .`,
   re-derived 2026-08-20 = 78 `Code/*.lua` + `items.lua` + `metadata.lua` +
   `LICENSE` + `preview.png`. ⚠️ A different number means stop, not adjust.
   ⛔ Bytes and md5 are **not** predictable and are not written above on purpose.

2. **After the listing is live**, subscribe back / download the pack and md5 the
   delivered `.fpk` **against the row you filled in at step 1** (or reconcile
   with `tools/pack_list.py` if the portal re-wraps the archive — then compare
   the 82 entries by content, which is what actually matters).

⛔⛔ **2026-08-20, AFTER THE REAL UPLOADS — THE ROW ABOVE MATCHES ONE PORTAL, NOT
BOTH, AND A STRAIGHT md5 COMPARE WOULD READ AS A FAILURE ON THE OTHER.**

| portal | what it actually received | compare how |
|---|---|---|
| **Paradox Mods** (`pdx_id` 156049) | the package built **before** its save — `version = 0`, comments intact ⇒ **1.0.0** | ✅ md5 against the row above (`6621384b…`, 391,567 B) |
| **Steam** (`steam_id` 3787202810) | ⛔ **a DIFFERENT archive.** Steam saves *before* packing, so its copy carries `version = 2` **and** the comment-stripped `metadata.lua`/`items.lua` that save produced ⇒ **1.0.2**, and the page reports **385,131 B** against our 391,567 | ⛔ **never md5 against the row** — reconcile with `pack_list.py`: expect the same **82** entries and the same 78 `Code/*.lua` **byte-identical**; only `metadata.lua` and `items.lua` legitimately differ |

⇒ **The code both portals ship is identical.** What differs is one integer and
the comments in two non-code files. ⚠️ Do not "fix" this by re-uploading: a
further upload bumps again and would make it worse, not better.

⛔ **File-level only, never behavioral:** with the dev
junction present, the unpacked copy wins silently at equal version
(`Mod.lua:1770`, hazard `H-09`), so a launch with a subscribed copy installed
proves nothing about the downloaded bytes. If the download is not reachable as
a file on this rig, record that here with the route that was tried and move on
— the check is cheap insurance, not a gate.

---

## 1. The order of operations — links only exist after the step that creates them

⛔ **Do not reorder these.** Each step's output is the next step's input, and
doing them backwards means going back to edit a live page.

| # | step | what it creates | who |
|---|---|---|---|
| 1 | **Upload the fix pack** — ⛔ **Paradox Mods FIRST, Steam second (§0.5(c))**; ⛔ not the opt-in (parked 2026-08-17); ⛔ not Save Rescue (held in reserve, item 17) | ⭐ the **store URL**, one per portal. It does not exist until now | you |
| 2 | **Put the store links into the site pages** | the site stops saying "no store links yet" | ⛔ **agent work, ~10 min, already filed** — see §5 |
| 3 | **Switch GitHub Pages on** | ⭐ the **site URL**. GitHub prints it on the Pages settings screen — copy it from there, do not type it | you |
| 4 | **Fill the site links into the store card** and re-save it | the card's FILL-IN markers close | you |

⚠️ **Step 4 means editing a store page you have already published.** That is
normal and expected — it is why every site link in the card is a marker with a
delete-instead answer, so the card is complete and honest at step 1 and merely
*better* after step 4.

~~ℹ️ The **store cross-links between the two mods** (each card pointing at the
other) become available at the end of step 1, not step 4.~~ *(PARKED 2026-08-17
— one mod, nothing to cross-link; FILL-IN 2 left the card with its sentence.)*

---

## 2. What to paste, per product

| product | paste this | into |
|---|---|---|
| **Relaunched Fix Pack** | `RELEASE_DESCRIPTION_FIXPACK.md`, everything between the two `═══ PLAYER TEXT ═══` rules | the mod page body |
| ~~Opt-In Modules~~ | ⚖️ **PARKED 2026-08-17** — not uploaded at this launch; its card keeps waiting as the audited paste source | — |
| ~~Save Rescue~~ | ✅ 17 ruled **hold off** — nothing pasted; the card waits as the contingency draft | — |

⛔ **Search the pasted block for `>>> FILL-IN` before you save the page.** Every
marker sits on its own line and every one tells you how to delete itself.
**Three markers in the fix-pack card** — FILL-IN 2 (the opt-in store link) left
the card with its sentence on 2026-08-17, and the numbering keeps its gap on
purpose. *(History: six across the two cards — 4 + 2 — before the solo-launch
parking; the opt-in's third was the Save Rescue sentence, deleted with the 17
ruling; the 08-14 strike of the notice paragraph also shortened both bodies
below.)*

**Body sizes, re-measured 2026-08-15 by the `unattended-3` terminal audit**
(markers excluded; the fix-pack card grew by that chain's two modules — the
Automation-policy disclosure paragraph, the sixth judgment-call bullet, and the
five→six / 94→96 count edits, all diff-proven VERBATIM against the audited
STORE file after the change):

| card | characters | words |
|---|---|---|
| Relaunched Fix Pack | **10,782** | **1,881** |
| ~~Opt-In Modules~~ *(parked, not pasted)* | 15,907 | 2,774 |
| ~~Save Rescue~~ *(contingency draft, not pasted)* | 4,202 | 792 |

⭐ *(Fix-pack cell re-measured 2026-08-17 AGAIN after the rename: the paste
body's H1 is the one place the display name appears in it, so "Community" →
"Relaunched" moves it exactly +1 character: 10,781 → **10,782**, words
unchanged at 1,881 — measured by the same method, which first reproduced the
pre-rename 10,781/1,881 from git HEAD exactly. VERBATIM vs the STORE block
re-proven after the edit: the pair's diff is line-identical to the pre-rename
diff — only the documented marker/HOLE lines.)*

⭐ *(Fix-pack cell re-measured 2026-08-17 after the solo-launch parking removed
the separate-mod clause, the companion-mod bullet tail, FILL-IN 2 and the
uninstall cross-reference: 11,209/1,957 → **10,781 / 1,881**. Same method as the
2026-08-16 correction — the paste block with marker lines dropped. Smaller
again, so no limit risk moves. VERBATIM vs the STORE block re-proven IDENTICAL
after the edit.)*

⛔ *(Fix-pack cell CORRECTED 2026-08-16 by the public-docs checkup: the 08-15
"11,581 → 11,542" re-measure subtracted the count edits but **never the deleted
distress bullet itself** (~54 words). Re-measured today over the actual paste
block — marker lines dropped, same method that reproduces the other two cells
exactly: **11,209 characters, 1,957 words**. The body also now says "96 checks"
(same length as "95"). Direction is smaller, so no limit risk moves.)*

---

## 3. The `metadata.lua` strings — state, counts, and what to check at the paste

**State: applied and live in all three files.** The fix-pack and opt-in strings
were corrected and applied on your instruction 2026-08-13 (`1ac1187`). ⭐ **Two
more defects were found and corrected 2026-08-14** under your standing 22b word
(*"change any wordings to their accurate versions"*) — text only, no behaviour,
no version bump:

1. ⛔ **The fix pack's changelog still sent players to the wrong name.** It read
   *"…their own mod, the Community Opt-In Pack"* — the dead working title. The
   08-13 pass corrected that name in the `description` and missed it four lines
   below in `last_changes`, in the same file, under a comment saying it had been
   corrected. A player told to look for that name finds nothing on any store.
2. ⛔ **Save Rescue's changelog quoted a repository file path** — and the folder
   it names is on that mod's own exclusion list, so the document it invited a
   reader to consult was never inside the download. Rewritten in plain words.

### ⚠️ Character limits — counted, but NOT checkable from here

**Every string is counted below. ⛔ No portal's limit could be verified from any
local source, and none is asserted from memory** — that is a claim about a
website neither of us can check without an account, and this project does not
ship those. **Treat every row as check-at-paste**: the portal will either show a
counter or refuse the field, and both answers arrive in two seconds.

| mod | `title` | `short_description` | `description` | `last_changes` |
|---|---|---|---|---|
| Relaunched Fix Pack | **19** | 184 | **779** | **16** |
| ~~Opt-In Modules~~ *(parked)* | **35** | **178** | **889** | **101** |
| ~~Save Rescue~~ *(hold-off)* | **32** | **148** | **734** | 442 |

⭐ *(`title` cells re-measured 2026-08-17 after the rename: fix pack
"Community Fix Pack" 18 → "Relaunched Fix Pack" **19**; and on the owner's
same-day "rename them now" ruling (checklist 36) the sibling titles were
applied in their repos — opt-in "Relaunched Fix Pack: Opt-In Modules" **35**,
rescue "Relaunched Fix Pack: Save Rescue" **32** (the item-26 pre-approved
family form, landing early on the owner's word). ⭐ Later the same day, under
the owner's widened license, the sibling STRING cells moved too — renamed in
place and re-measured: opt-in 178 / 889 / 101, rescue 148 / 734 / 442-unmoved.
⚠️ One honest discrepancy surfaced by the re-measure: the opt-in `description`
measured **888 BEFORE the rename** against the recorded 884, by the same
code-point count that reproduces every other cell in this table exactly — this
is the one string carrying the two-code-point ⚠️ and the →, so the 08-14
count evidently normalized those differently. The 889 above is the code-point
count; the string itself last changed before the 08-14 audit, and every limit
stays check-at-paste regardless.)*

⭐ *(Fix-pack `description` and `last_changes` re-measured 2026-08-17 after the
solo-launch parking: 844 → **779** and 112 → **16** ("Initial release."). The
old strings named the opt-in mod — the one surface that could never be fixed
after upload without a version bump. Originals: `PARKED_OPTIN_REFERENCES.md`
P38/P39. `title`/`short_description` re-measured unchanged.)*

*(fix-pack `description` re-measured 2026-08-15: "Five of the fixes are
judgment calls" → "Six", 844 → 843 — the only string the `unattended-3` chain
moved; the other cells were re-measured unchanged.)*
⛔ **RE-MEASURED AGAIN 2026-08-15 (later), after the item-31 removal: back to
"Five", 843 → 844.** The F85 module was pulled (its popup is dead-coded out of
retail), so the judgment-call count reverted everywhere. The **card** lost its
distress bullet with it and re-measures **11,581 → 11,542 characters** *(⛔ that
11,542 was itself wrong — it never subtracted the deleted bullet; the true
figure is **11,209**, see the corrected table in §2)*. Both
figures above are the post-removal ones; no other cell moved.
→ `agent/bugs/F85.md` §2026-08-15, `SHELVED_F85_DISTRESS_PAUSE.md`.

*(characters, re-measured 2026-08-14 by the terminal audit from the three
`metadata.lua` files. ⛔ Two corrections to the original table: the Save Rescue
`description`/`last_changes` cells were TRANSPOSED as first written, and the
rescue strings then grew — the audit added the missing save step and fixed the
stand-down sentence, per its record in `RELEASE_DESCRIPTION_RESCUE.md`.)*

⭐ **The one thing worth eyeballing at the paste**, and it is measurable locally:
**the Opt-In Modules `description` is the only string carrying characters beyond
plain text** — an arrow (`→`) and a warning sign built from two code points
(`⚠` plus an invisible modifier). Its **card body carries the same three**. If
any field renders as boxes, question marks or a stray character, that is what
happened, and the fix is to retype those few characters in the portal's own
editor. Every other string and both other card bodies use nothing but ordinary
text and an em dash. *(2026-08-17: applies only on the day the opt-in uploads —
nothing at THIS launch carries those characters.)*

---

## 4. Packaging — what actually lands in a player's download

⭐ **Checklist item 23 is DONE, 2026-08-14** — your ruling was *"yes, add the
missing patterns, at launch prep"*, and this is launch prep. Measured over the
real trees, before and after:

| mod | files shipped BEFORE | AFTER | what stopped shipping |
|---|---|---|---|
| Relaunched Fix Pack | **90** | **78** | `CLAUDE.md`, `.gitattributes`, all **10** files of `tools/` |
| ~~Opt-In Modules~~ *(parked — not uploaded at this launch)* | **22** | **12** | `CLAUDE.md`, `.gitattributes`, all **8** files of `tools/` |
| Save Rescue | **4** | **4** | nothing — it was already clean, built after the lesson |

The 78 and 12 reconcile to the emitter exactly: 75 + 9 code files, plus
`items.lua`, `metadata.lua` and `LICENSE` each.

⭐ **2026-08-15 (`unattended-3` audit): the fix pack now ships 80 files** — the
chain's two new modules (`Fix_DistressPopupPause.lua`,
`Fix_AutomationLawCompensation.lua`) land in `Code/`. Re-simulated over the
real tree with the shipped `ignore_files` (the same method as the table above):
**80 = 77 `Code/*.lua` (emitter-matched) + `items.lua` + `metadata.lua` +
`LICENSE`**, nothing else. The opt-in and rescue packages are untouched.
⛔ **CORRECTED THE SAME DAY — it ships 79.** `Fix_DistressPopupPause.lua` was
removed on the owner's item-31 ruling and its row pulled from `metadata.lua`'s
file list, so the true figure is **79 = 76 `Code/*.lua` + `items.lua` +
`metadata.lua` + `LICENSE`**. Counts re-emitted with `--emit-counts`, not
hand-adjusted.

⭐ **2026-08-17 AT THE SITTING — IT NOW SHIPS 80.** `preview.png` was added at the
mod root to satisfy the `image` field (§0.5(a)), so **80 = 76 `Code/*.lua` +
`items.lua` + `metadata.lua` + `LICENSE` + `preview.png`**. ⛔ Re-simulated over
the real tree against the shipped `ignore_files` (same method as the table
above), not hand-adjusted — the run enumerated 7,726 files and filtered 7,646,
and the 76 `Code/*.lua` reconciles to `doccheck --emit-counts` exactly.
⚠️ **Still a SIMULATION, not the engine.** `MatchWildcard` has no Lua body, so
whether `*` crosses `/` — which decides whether `*/docs/*` filters the whole
`docs/` tree or only its top level — remains the open question
`WORKFLOW.md` §882-887 has owed since 08-13. **One `DbgPackMod` run at the
sitting settles it, and the console is free inside the Mod Editor**
(`archive/CHEATS_INVENTORY.md`). ⛔ Do it BEFORE the upload, and note
`DbgPackMod` itself calls `SaveWholeMod()` if the mod is dirty (§0.5(b)) — so the
version guard applies to it too.

⛔ **2026-08-20 (close-out chain link 3) — IT WILL SHIP 82, AND THE 80 ABOVE IS
NOW HISTORY.** `C51`'s `Fix_LocalizedUIText.lua` and `C50`'s
`Fix_SpaceYDroneCapBullet.lua` landed on 08-20, so **82 = 78 `Code/*.lua` +
`items.lua` + `metadata.lua` + `LICENSE` + `preview.png`** — emitted by
`python tools/pack_predict.py .`, with the 78 reconciling to `doccheck
--emit-counts` and to `upload_preflight`'s two-list agreement (0 FAIL, 78 entries
in order) exactly. ⛔ **This is a PREDICTION of the next pack, not a reading of
one.** The 08-17 archive is superseded and no `.fpk` of the current tree exists
anywhere — ⇒ **every hash and byte size this sheet records belongs to the 80-file
tree and none of them applies to the upload you are about to make** (§0.5(f),
rewritten the same day for exactly that reason). The paragraphs above are left as
they were written; they are correct about the days they describe.

⚠️ **`LICENSE` still ships, deliberately.** Item 23 listed it among the misses,
but the rescue mod — built later — states *"LICENSE ships on purpose"*, and a
licence inside the package is right. All three now agree. **Say the word if you
want it out and it is one line each.**
✅ **Item 23's one unverifiable sub-case is moot**: whether `.github/` slips past
the `.git` pattern does not matter, because **no mod repo has a `.github/`
directory** (checked in all three). Only the site repo does, and it is not a mod.

### ⚖️ The version numbers are yours, and one of them contradicts its own changelog

| mod | ships as | its changelog says | note |
|---|---|---|---|
| Relaunched Fix Pack | ✅ **1.0.0** (`version_major=1, version_minor=0, version=0`) | "Initial release." | ✅ **RULED 2026-08-17 ("lets go with 1.0.0") and APPLIED** — the table's old "1.0" cell had read major.minor only and hid a third digit rendering 1.0.1; caught at solo-launch prep, routed, ruled the same day. Tag moved to `fixpack-v1.0.0` |
| ~~Opt-In Modules~~ *(parked)* | **1.0** | "Initial release" | ✅ **RULED 2026-08-14 ("we go 1.0, especially with the amount of QA we have done") and APPLIED** — `metadata.lua` now 1.0.0 |
| ~~Save Rescue~~ | **0.1** | "Initial pre-release" | ✅ consistent; not publishing at launch (item 17 hold-off) |

---

## 5. Filed for the agent side, so you do not do it by hand

| item | what | when |
|---|---|---|
| **Store links into the site** | `content/install.md` opens with *"No store links yet — this page gets the links when they exist."* One admonition to replace, plus store buttons on the landing page if wanted. ⭐ **2026-08-17: the owner is uploading to BOTH portals, so this is TWO links (Paradox Mods + Steam Workshop), not one** — the page's wording must carry both | step 2, after upload |
| ✅ ~~**Save Rescue's repo README is stale**~~ | **CLOSED 2026-08-17** — re-read at source: its Status section already carries the 2026-08-14 attended pass, witnessed dialogs included; whoever fixed it never retired this row. ⚠️ The genuinely stale line was in that repo's `CLAUDE.md` ("attended pass still owed"), corrected 2026-08-17 with the correction noted in place | done |
| ✅ ~~**`Opt_DroneOverhaul.lua`'s header comment** names the old *"Mod Options → Community Fix Pack"* path~~ | **FIXED 2026-08-17** under the owner's widened rename license — now *"Relaunched Fix Pack: Opt-In Modules"* (family name and missing suffix both corrected) | done |
| ✅ ~~**This repo's own `README.md` is stale far beyond its name**~~ | **REWRITTEN 2026-08-17** on the owner's instruction ("update the readme with whatever is needed"): the ghost optional-modules section is gone, every count re-emitted this sitting (75 modules · 96 checks · 167 tracked findings), the false console-disable claim replaced with the accurate veto-mod mechanism, install/restart/achievements wording aligned to the audited surfaces, and the bug-report route (item 27) added | done |

⛔ **The site's five pages are terminal-audited and are not edited in passing.**
Anything found in them is filed, which is why the first row above is a filed task
and not something already done.

---

## 6. Save hygiene at the sitting — `EF-051`, and whether it touches you

⛔⛔ **CORRECTED 2026-08-17 AT THE SITTING — THE PARAGRAPH BELOW WAS WRONG, AND
IT WAS WRONG IN THE DIRECTION THAT COSTS A FILE.** It said ④ never opens the
game. **It does: the upload route IS the in-game Mod Editor**
(`WORKFLOW.md:901`; `CreatePackageForUpload` is game-side,
`GedModEditor.lua:678-741`). ⇒ **`EF-056` is LIVE for this sitting.**

✅ **Pre-copy DONE 2026-08-17 before any launch.** The two autosave-tagged files
on disk — `Autosave Sol 406` (56,195,934 B, MD5 `392cbaaa…`) and
`Autosave Sol 411` (56,195,463 B, MD5 `2c645da1…`) — were byte-copied and
verified MD5-identical. ⛔ **The copies live OUTSIDE the save directory**, because
`EF-056`'s own amendment says a byte copy of an autosave *is* an autosave to the
rotation: copies kept inside would join the firing line.
⚠️ **Reconcile by name after EVERY launch, not just the one you expect to fire.**
ℹ️ Exposure is genuinely low if the sitting never loads a campaign (the rotation
is driven by a loaded campaign's own autosave timer) — but "probably won't fire"
is how `Autosave Sol 306` was lost, and the pre-copy costs seconds.

~~**It does not touch ④ as scoped.** Uploading a mod page, pasting text and
switching Pages on never open the game and never touch a savegame.~~

⚠️ **It touches ④ the moment the capture sitting rides along** (§0(a) — and it
probably should, since the preview art needs the game anyway). In that case, both
standing rules are live:

* ⛔ ~~**`EF-051` — Steam Cloud is ON**, at your own request and temporarily, so a
  save deleted with the game closed comes back on the next launch. Nothing is
  called *gone*; close-outs say **"deleted, listing verified"**.~~ ⚖️ **STALE,
  corrected 2026-08-17: the `EF-051` hold was LIFTED 08-14 (owner: cloud OFF)** —
  "gone — NAMED listing" is allowed again, and the falsifier is any stray at the
  next launch. `CP60RT` is **HELD** and present. ⚠️ **`Autosave Sol 311` is NOT on
  disk** and is removed from the held list here: the autosaves have since rotated
  ~100 sols on (406/411), so this is old rotation and nothing from this sitting —
  but a held list naming a file that no longer exists is worse than no list.
  Save directory stood at **81** files at the pre-copy (last by-name
  reconciliation was 77, 08-15).
* ⛔ **`EF-056` — a byte copy of an autosave is still an autosave**, and its
  rotation deletes real ones. It ate `Autosave Sol 306` for good and took
  `Sol 311` twice more during the last sitting. **Pre-copy every autosave before
  any launch, and reconcile after every launch** — not after the one you think
  will do it.

---

## 7. What is ready, in one line each

| | state |
|---|---|
| Fix-pack card | ✅ **paste-ready** (item-29 strike + 2026-08-17 solo-launch parking applied), **3 fill-ins**, every one deletable; VERBATIM to STORE re-proven post-parking |
| ~~Opt-in card~~ | ⚖️ **PARKED 2026-08-17** — not uploaded at this launch; stays audit-ready for the day it ships |
| Save Rescue card | ✅ **held in reserve** (17 hold-off) — audit-corrected contingency draft, nothing pasted at launch |
| Uninstall story | ✅ reconciled; **four** defects in the inherited draft found and corrected — three by assembly, the missing save step by the audit (`RELEASE_UNINSTALL_ASSEMBLY.md` §2) |
| `metadata.lua` (fix pack) | ✅ solo-launch strings applied and re-counted 2026-08-17 (779 / 16); no opt-in reference survives in any player string |
| Packaging | ✅ item 23 done, re-simulated 2026-08-17 (fix pack ships **80** — 79 + the new `preview.png`); ⚠️ the `*/docs/*` wildcard question is still owed one `DbgPackMod` run at the sitting (§4) |
| Preview `image` field | ✅ **ADDED 2026-08-17** — was MISSING and would have hard-rejected the Paradox upload (§0.5(a)); written by hand so the mod loads clean |
| Version guard | ⛔ **LIVE RISK, §0.5(b)+(c)** — any editor save bumps 1.0.0 → 1.0.1. **Paradox Mods uploads FIRST**; Steam's own prepare saves before packing, so it needs `version = -1` in a fresh session to also ship 1.0.0 ⇒ ⚖️ **one owner call, decidable after Paradox** |
| `EF-056` pre-copy | ✅ **DONE 2026-08-17** — both autosave-tagged files copied outside the save dir, MD5-verified (§6). ⛔ §6's "④ never opens the game" was wrong and is corrected |
| Site | ✅ built + audited + item-29 strike + 2026-08-17 one-mod parking applied, `mkdocs --strict` GREEN, ⛔ **nothing on the web**; needs step 2 then step 3 |
| Preview art | ✅ **chosen 2026-08-14 — C1**, re-lettered 2026-08-17 to the new name (§0(a)), fix-pack FINAL file named in §0(a), size verified under both limits |
| Decisions owed by you | **0** — the version call was ruled 1.0.0 the day it was raised |
| Release tag | **`fixpack-v1.0.0`** placed 2026-08-17 on the final pre-upload tree (`WORKFLOW.md` §"Release marking"; the interim `fixpack-v1.0.1` tag was deleted when the ruling landed) — record portal version → commit sha here at upload |
