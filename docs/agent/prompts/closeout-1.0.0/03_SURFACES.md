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

- *(links 1–2 append here)*
