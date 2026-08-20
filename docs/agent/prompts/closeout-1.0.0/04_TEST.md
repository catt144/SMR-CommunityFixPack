# Link 4 — ⭐ THE ATTENDED SITTING: the first and only eyes on both fixes

♻️ **SELF-CONSUMING.** `git rm` this file in your closing commit, naming its grave.
📋 Read `README.md` in this folder first — its binding rules govern you.

⭐⭐ **THIS LINK NEEDS THE OWNER, ONCE, FOR ABOUT HALF AN HOUR.** Everything
before it is *built, unobserved*. ⛔ Nothing in this chain may be called verified
until this sitting produces a log and a screen reading.

⚖️ **"Basic testing" is the owner's ruling (checklist 57) and it is the bar
here.** ⛔ No run B, no suite marathon, no multi-day leg. One launch, two screens,
one language switch, the logs archived.

## 0 · Read path + preparation you do BEFORE the owner sits down

```
git log --oneline -15 && git pull
python tools/doccheck.py --emit-counts
python tools/upload_preflight.py
```

Read both modules **as built**, and write your **predictions first** — what each
log line and each screen should say if the fixes work, and what it would look
like if they silently did not. ⛔ A sitting without written predictions measures
nothing; it just watches.

⚠️ **`EF-056` — pre-copy every autosave before any launch and keep the copies
outside the save dir.** Loading a copy of a campaign runs that campaign's autosave
rotation and **deletes the owner's autosaves**. Reconcile by name afterwards.

⚠️ The rig runs cheats and both mods are the normal config (owner rule): a cheat
is a confound only where a reading intersects what it changed. Neither fix here
is touched by any of them — say so rather than pretending the rig is clean.

## 1 · 🗒 Live todo list — one item per step of the script below

## 2 · The owner's script — write it as numbered steps they can follow without you

Build it around these readings. **Every step says what to expect and what to do
if it differs.**

1. **Boot.** Both new modules report `applied` in the log, and the pack still
   reports its full module count. ⛔ An `inactive` line on either is a stand-down
   with a reason — capture the reason verbatim; it is the fix telling you the
   game is not shaped the way we read it.
2. **`C50` — English.** Pre-game → sponsor selection → **SpaceY**. The
   description carries the new bullet, **with the number in it**. ⚠️ Read the
   **first** bullet too: it contains the rocket's cargo figure, and it is the
   thing route 2 would have broken. If that number is missing or shows as raw
   markup, ⛔ **stop the sitting and report** — that is the context-drop failure
   and the fix must come out.
3. **`C51` — English.** Terraforming overview panel; rocket → *Back to Earth*
   rollover. ⛔ **Expect NO visible change.** This step exists only to prove
   nothing broke, and the report must say that rather than dressing it up.
4. ⭐ **The language switch — the only step that can actually see `C51`.** Switch
   the game language (German is the one whose records were verified), restart if
   the game asks, and revisit **both** screens plus the SpaceY description.
   Expect: the terraforming heading and the *Back to Earth* rollover now in
   German, and the SpaceY bullet in German too — including its borrowed sentence.
   ⭐ **This is also the first time in this project's history that a shipped-id
   string has been watched rendering in another language** (`EF-039`'s standing
   unobserved note). Whatever it shows, it retires that gap — record it as a fact
   either way.
5. **Switch back to English**, confirm the screens return to normal.
6. **Suite, only if it is free** (`*r SMRTest.RunAll()`): a green-or-explained
   result, not a number to chase. ⛔ Do not turn this into a gate.

## 3 · After the sitting

- **Archive every log** to `docs/archive/` with a distinguishing prefix, and
  ⛔ **`git add -f`** — `.gitignore` carries `*.log`, and three evidence logs were
  found uncommitted on 2026-08-20 for exactly this reason. Then check
  `git ls-files docs/archive/ | wc -l` against the files on disk.
- Update `C50.md` / `C51.md` from `filed` to a **status word that matches what was
  actually seen** — `tested-attended` if a human watched it, never bare `tested`
  (closed to new work). ⚠️ If the language step did not happen, `C51` **does not**
  get an attended screen claim; say what was skipped, **by name**.
- Record the language reading in `EF-039` — it closes that entry's own open note.

## 4 · Scope fence

**IN:** the sitting · predictions · logs archived and tracked · status words ·
`EF-039`'s note · a defect entry for anything the sitting finds.

**OUT:** ⛔ code changes — ⚠️ **unless the sitting finds one of the two fixes
broken**, in which case fixing it is in scope and the audit is told loudly · ⛔
the tag · ⛔ `version` · ⛔ portals · ⛔ packing (the owner packs at the upload
sitting; the Ged route loads a scratch colony and is not free).

## 5 · ⛔ What you may not claim

- ⛔ **Any screen reading the owner did not report to you in their own words.**
- ⛔ **"Both fixes verified"** if only one was seen. ⛔ SKIPs by name, never a
  total.
- ⛔ A German rendering nobody looked at.
- ⛔ `tested` bare. ⛔ Any count you did not emit.
- ⛔ **"Nothing else in the log"** — read the whole log, and attribute every
  `[LUA ERROR]` or unexplained line rather than discounting it. *"Not caused by
  our leg"* is an attribution, not a dismissal.

## 6 · Close-out

One commit: the results · logs (`-f`) · entries · `EF-039` · `doccheck` GREEN ·
`git rm` this file · push.

**Owner report:** what was seen, screen by screen · what was skipped, by name ·
anything unexplained in the log · **the kickoff line for `05_AUDIT_fable.md`.**

## Notes from upstream

- **2026-08-20, link 3 (surfaces, consumed).** Counts are UNCHANGED by this link
  and re-emitted at its close: **77 registered modules · 78 `Code/*.lua` · 98
  probes**; `upload_preflight` **0 FAIL, 78 entries in order**; `pack_predict`
  **82 files**. ⛔ Re-emit anyway — never carry one of these forward by hand.
- ⭐⭐ **THE PLAYER-FACING PAGES NOW DESCRIBE CODE NOBODY HAS WATCHED, AND THAT IS
  THIS SITTING'S REAL STAKE.** Two entries went onto the site's fix list
  (`C:\Dev\SMR-CommunityMods`, **separate history, separate commit**) saying what
  both fixes do. ⇒ **if the sitting finds either fix broken, its site entry is a
  false promise and has to come out in the same breath** — say so loudly in the
  report, because the site repo is not in this repo's commit and is easy to
  forget. The audit (link 5) inherits that obligation.
- ⚠️ **What the `C51` entry promises, so step 3 can check exactly it:** *"if you
  play in English, this fix changes nothing you can see."* ⇒ step 3's expected
  reading is not merely "no crash" — it is **no visible difference**, and the
  German step is what the entry's other half rests on.
- ⚠️ **The `C50` entry is deliberately screen-agnostic** — *"while you are
  choosing a sponsor"*, no enumeration, and ⛔ **no number quoted**. ⇒ if the owner
  takes checklist 59's option to cut the challenge landing-spot site, **no site
  edit follows**. It also means the sitting cannot falsify the page by looking at
  only one of the two sponsor-screen readings.
- ⚖️ **One number is EMITTED BUT NOT MEASURED and it is on the store card:** the
  card now says *"an automated suite of **98** checks"* (was 96 — waves 12+13).
  The last A/B reading is `80/0/16/0` of 96, 08-15. ⇒ **§2 step 6 is the only
  thing that can close that gap.** Owner-facing as checklist **60** with a
  recommendation (run it if the sitting is smooth, skip it otherwise); if it runs,
  ⭐ **record the reading and tell link 5**, and if it does not, say so BY NAME.
- **The stale fingerprint is fixed and it did NOT become a number:**
  `RELEASE_PORTAL_PREP` §0.5(f) now carries an empty md5/bytes/entries row the
  owner fills **when they pack at the upload sitting** (not here — link 4 does not
  pack, `FIX_POLICY`/§4 fence). Expected entry count **82**; ⛔ a session that
  writes an md5 it did not compute from a real `.fpk` has broken the check.
- **Superseded chains were banner-fenced, not deleted** (`prompts/SMRCF_CHAIN_SET.md`,
  `prompts/smrcf-text/README.md`): they still told a session to *build* `C50` and
  `C51`. ⚠️ Their recorded readings are also wrong now — chain B says `C50` has
  two render sites; it has three.
- `mkdocs build --strict` **GREEN, zero warnings**, after the site edits; `site/`
  is not committed.

- *(links 1–2's notes were consumed with `03_SURFACES.md`; the survivors that
  matter here are above, plus: `Src` is under the install dir literally named
  `Project Spark` (`EF-014`), the TestKit is a SEPARATE REPO
  `C:\Dev\SMR-BugFixPack-TestKit` with waves **12 and 13** taken, and
  `python tools/split_bugs.py --write` ABORTS — regenerate `bugs/INDEX.md` with
  `sb.render_index(sb.load_from_dir())` instead, then expect one
  `warn <ID>: the frozen index-row cell says 'filed'…` per flipped entry, which is
  the house pattern and not a problem.)*
