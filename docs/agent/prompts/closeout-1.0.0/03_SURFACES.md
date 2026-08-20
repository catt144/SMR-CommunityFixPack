# Link 3 — the pages, the counts, and the fingerprint that just went stale

♻️ **SELF-CONSUMING.** `git rm` this file in your closing commit, naming its grave.
📋 Read `README.md` in this folder first — its binding rules govern you.

⛔ **No Lua is written in this link.** If you find a code defect, **STOP AND ASK**
rather than fixing it here — links 1 and 2 are consumed and a late code change
would land unaudited.

## 0 · Read path

```
git log --oneline -15 && git pull
python tools/doccheck.py --emit-counts
python tools/upload_preflight.py
python tools/pack_predict.py .
```

`STATE.md` · both new modules **as built** (read the code, not the briefs) ·
`agent/bugs/C50.md` + `C51.md` · `reports/RELEASE_PORTAL_PREP.md` ·
`reports/RELEASE_DESCRIPTION_FIXPACK.md` · `reports/STORE_FIXPACK.md` ·
`reports/PARKED_OPTIN_REFERENCES.md` (⛔ **so you do not restore a parked
passage** — `H-07`) · the site repo `C:\Dev\SMR-CommunityMods`.

## 1 · 🗒 Live todo list — one item per numbered step below

## 2 · The four jobs

### (a) ⛔ The recorded artifact is stale — this is the one that can ship wrong

STATE and the release sheet quote a built pack: **md5 `8dcb0692…`, 362,894 B,
80/80 files**. Two modules later that is **false**, and it is quoted in a place
that matters: `RELEASE_PORTAL_PREP.md` **§0.5(f)**, the post-upload
delivered-bytes check, tells the owner to checksum their download against that
md5. Left alone it would fail on a correct upload.

⇒ Re-derive the **expected shape** with `tools/pack_predict.py` (it should now
read **82** files) and correct every place the old numbers appear. ⚠️ **You cannot
produce the new md5** — it exists only after the owner packs at the sitting. So
§0.5(f) must be rewritten to say *compare against the md5 recorded at pack time*,
with a blank the sitting fills, **not** a number you invent.

### (b) The player-facing pages owe two entries

Two fixes a player can see are now in the pack and on no page. The site's fix
list is the promise surface — the pre-launch sweep's single most valuable finding
(`L6-F1`) was exactly this class: a page and a build disagreeing.

- `SMR-CommunityMods` `content/fix-list.md` — two entries in house voice: *what
  you saw*, *what was wrong*, in the same shape as the neighbours. ⛔ Neither is a
  **judgment call** — do not mark them, and do not touch the *"Five of the fixes
  are judgment calls"* sentence.
- ⚠️ **The C51 entry has to be honest about who sees it:** an English player sees
  **no change at all**. Say that plainly rather than implying a repair they can
  observe.
- ⛔ **Never name the other mod on a player surface** (`EF-054`, `FIX_POLICY` §8).
  Credit belongs in code headers and entries, which links 1–2 already carry.
- `mkdocs --strict` must build.

### (c) Counts, everywhere they are written down

`doccheck --emit-counts` is the only source: modules **75 → 77**, `Code/*.lua`
**76 → 78**, probes only if links 1–2 added any. Sweep for stale copies of the
old numbers in `docs/` and on the site. ⛔ Never hand-type one.

### (d) The metadata strings — check, probably do not change

`metadata.lua`'s `description` / `short_description` carry **no fix counts**
(verified 2026-08-20), so two new modules do not force an edit. **Confirm that is
still true and then leave them alone.** ⛔ Any change to `metadata.lua` beyond the
`code` list needs an owner ruling — and remember `version` never moves.

## 3 · Scope fence

**IN:** the stale fingerprint · two fix-list entries · counts · a read-only check
of the store strings · the release sheet.

**OUT:** ⛔ Lua · ⛔ the tag · ⛔ `version` · ⛔ portals · ⛔ restoring any parked
opt-in passage (`H-07`) · ⛔ the opt-in and rescue repos · ⛔ `C52`.

## 4 · ⛔ What you may not claim

- ⛔ A pack md5 you did not compute from a real `.fpk`.
- ⛔ **"The pages are complete"** without having read both new entries end to end
  against the code that shipped them.
- ⛔ Any count not emitted by `doccheck`.
- ⛔ That `mkdocs --strict` is green without running it.

## 5 · Close-out

Commits: one here, one in the site repo (**both pushed**; the site repo is a
separate history — `SMR-CommunityMods`). `doccheck` GREEN · `upload_preflight`
0 FAIL · `git rm` this file · push.

**Owner report:** what moved on the pages · the corrected artifact expectation
(**82 files**, md5 pending the sitting) · **the kickoff line for `04_TEST.md`,
and the warning that link 4 is the one that needs their hands.**

## Notes from upstream

- **2026-08-20, link 2 (`C50`, built and consumed).** Counts after link 2, emitted:
  **77 registered modules · 78 `Code/*.lua` · 98 probes** — so §2(c)'s "probes only
  if links 1–2 added any" resolves to **97 → 98** (link 1 added wave 12, link 2
  added wave 13). `upload_preflight` read **0 FAIL, 78 entries in order**.
  ⇒ `pack_predict` should read **82**; that number is unchanged by this link.
- ⚠️ **`C50` reaches THREE player-facing screens, not the one the fix list will
  want to imply**, and §2(b)'s entry must not overstate or understate it: the
  pre-game **mission summary panel**, the **rollover on the sponsor picker**, and
  the **challenge landing-spot screen**. A fourth function the record called a
  render site (`GetMissonProfileText`) has **zero callers in the whole game** and is
  deliberately not touched. Full derivation + the caller table: `agent/bugs/C50.md`,
  the *BUILT 2026-08-20* section. ⭐ The owner has an open note about this
  (**checklist 59**) — read it before writing player-facing wording, because it
  contains the one place they may still cut the third screen.
- ⭐ **The player-facing sentence to describe `C50` is genuinely awkward, and this is
  the link that owns it.** Nothing was re-worded and no behaviour was added: SpaceY
  already granted +20 Drone Hub Drone capacity and simply never said so. ⛔ Do not
  write anything that reads as a balance change or a new feature, and ⛔ do not
  quote "40" as the number — it is `base + the preset's modifier`, computed at
  render time, and the base is not ours to promise.
- **The bullet borrows shipped translation id `4706`** (the `CommandCenterMaxDrones`
  ConstDef help). That is disclosed in the code header and the entry. ⚠️ If any page
  quotes the wording, quote it as *the game's own description of that setting*, not
  as our sentence.
- ⭐ **`4706` was re-verified across all NINE packs this session**, not just German,
  with `tools/flpk_extract.py` — the extractor takes seconds and the recipe is in
  link 2's notes below. Link 1's English-fallback derivation (empty `Translation`
  column ≠ missing record) held up unchanged.
- ⚠️ **`Game.csv` is 23,090 records + 1 header row**; earlier notes said 23,090 and a
  header-inclusive count reads 23,091. Both are right about different things — do
  not "correct" either into the other.

- **2026-08-20, link 1 (`C51`, built and consumed).** Counts after link 1, emitted:
  **76 registered modules · 77 `Code/*.lua` · 97 probes**.
- ⛔ **`python tools/split_bugs.py --write` ABORTS** — it is the one-time migration
  tool, not the regenerator, despite `INDEX.md`'s line-1 banner. A status flip DOES
  change the index row, so `doccheck` goes RED until you rewrite it. What works:
  ```python
  import sys, io; sys.path.insert(0, 'tools')
  import split_bugs as sb
  lines = sb.render_index(sb.load_from_dir())
  io.open('docs/agent/bugs/INDEX.md','w',encoding='utf-8',newline='\n').write('\n'.join(lines)+'\n')
  ```
  Then `git diff --stat` it: **one row per flipped entry.** The resulting
  `warn <ID>: the frozen index-row cell says 'filed', entry says 'fixed'` is the
  house pattern (`C43`, `F100`, now `C50`+`C51`), not a problem.
- **The extractor is seconds, use it:** `sys.path.insert(0,'tools'); import
  flpk_extract as fx; fx.extract(r'A:\SteamLibrary\steamapps\common\Project Spark\Local\German.fpk', out)`.
- ⚠️ **`Src` is under the install dir literally named `Project Spark`** (`EF-014`);
  the `Surviving Mars` folder's `ModTools` has no `Src` and is a decoy. Confirmed
  again by both build links.
- **The TestKit is a SEPARATE REPO** (`C:\Dev\SMR-BugFixPack-TestKit`) — its own
  commit, its own push; `doccheck` only report-warns on its dirty tree. Waves **12**
  and **13** are taken.
- ⛔ **Do not assume a target has one implementor or one caller.** Link 1 found five
  undocumented subclasses; link 2 found two undocumented render sites and one
  documented site with no callers at all. In both cases the brief's own caller count
  was wrong, and in both cases the whole-tree grep is what caught it. Grep the
  FIELD, not one spelling of it.
