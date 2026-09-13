# REPAIR_PASS — the six defects that need no owner ruling

**Fire with:** a fresh session rooted at `C:\Dev\SMR-BugFixPack`. Tool-neutral. Written 2026-09-13
by `smr-bugfixpack-da`, which **analysed these and is deliberately not implementing them** — the
owner separated implementor from judge, and that split already caught a defect in the previous
brief on its first firing. A different session adjudicates your **output**, not your report.
`git rm` this file when it has fired; its grave is the commit that lands group C.

**Every defect below was verified in the tree before it was written here** — each row says with
what. ⛔ They are still **claims**: re-derive before you act, and if one does not reproduce, that
is a finding worth more than the repair.

---

## 0 · Scope

**In:** six defects that are wrong under *any* answer to the open policy calls.
⛔ **OUT — the owner's, do not pre-empt:** checklist **170** (a) marker vocabulary / (b) normalised
byte accounting / (c) reading routes · **ck169 ➋**, **ck47**, **ck152(c)** statuses · **deleting**
`prompts/SELFCHECK_PILOT.md` (removal is recommended and still awaiting the owner) · **D4** and any
`archive_settled.py --apply` · where the fredware-naming rule and the every-upload-overwrite rule
should be **filed** · any **status** change to any checklist item or entry · `CLAUDE.md` (editing it
drifts `AGENTS.md` and turns doccheck RED for every peer).

## 1 · Anchor — run these; ⛔ quote no number from this file

```
git -C C:/Dev/SMR-BugFixPack status -sb | head -1
git log --oneline -1
python tools/doccheck.py | tail -1
python tools/doccheck.py | grep -E 'WAITING|PUSH SET|STATE \+ STUBS|FINGERPRINTS'
python tools/flpk_extract.py --selftest
python tools/pack_predict.py . | head -12
```

⚠️ **The tree is busy** — several interactive peers, at least one mid-flight on **C92**; the owner
register gained rows **170** and **171** during the last pass. All sessions commit under **one git
identity**, so `git log --author` attributes nothing: identify by **sha + diff**.
⛔ **A pathspec is only HALF a commit fence** — it takes the *working-tree* content of a path you
name, a peer's unstaged edits included. Re-check `git status` **immediately before every write**.
Rules: `agent/WORKFLOW.md` § "Writing in a shared tree".
⛔ The pre-commit hook can go RED on a peer's in-flight `TEMPORARY` probe — not yours to fix, and
never a reason for `--no-verify`. Wait, or report and stop.

## 2 · Group A — `tools/doccheck.py` (one commit)

### A1 · Marker integrity is unreported, so it fails silently

Three defects in one mechanism. **Verified 2026-09-13:** `grep -cE '<!-- ck:' docs/PLAYTEST_CHECKLIST.md`
emits **one more** than doccheck's `WAITING: … marked` count, and has for days.

| | defect | verify |
|---|---|---|
| (i) | `MARKER_RE` (`:382`) matches `status:([a-z]+)` — **no hyphen** — so the live `status:part-ruled` marker on checklist 169 matches *nothing* and is dropped with no warning | `grep -n "MARKER_RE" tools/doccheck.py` |
| (ii) | `MARKER_STATUSES` (`:383`) is **defined and never referenced** — the vocabulary is documented in a comment and enforced by nothing | `grep -c MARKER_STATUSES tools/doccheck.py` returns its own definition line only |
| (iii) | **Duplicate `ck` numbers are not rejected**, so item 169's superseded heading — collapsed inside a `<details>` block — wins its register row over the current one | `grep -oE "ck:[0-9]+" docs/PLAYTEST_CHECKLIST.md \| sort \| uniq -d` → `ck:144`, `ck:169` |

**The repair is DETECTION, not semantics.** Emit a `MARKER INTEGRITY` line reporting: markers found
on disk vs markers parsed · every `<!-- ck:`-shaped comment that fails `MARKER_RE`, with its line
number · every status word outside `MARKER_STATUSES` (which must now actually be referenced) · every
duplicated `ck` number and the lines it appears on.

⛔⛔ **IT MUST NOT GO RED.** `part-ruled` exists and `ck144`/`ck169` are duplicated **right now**, so
a RED gate would block every commit for five peers until the owner rules ck170(a). **Emit warns**,
and state in the line itself what would make it RED later. Put that reasoning in the code comment —
the next session must not have to rediscover why this is a warn.
⛔ **Do not change which marker wins a row, and do not touch any marker in the checklist.** Which of
169's two markers is right is ck170(a), the owner's. Your job is to make the discrepancy *visible*.

### A2 · The fingerprint verdict is decided by substring membership

`doccheck.py:713` reads `elif build in bare:` — so a build id is matched as a **substring** of the
group label. **Verified:** an installed build of `2499507` would report `HOLDS` against a group
pinned to `24995074`. Compare the build **exactly** (parse the id out of the label, or anchor the
match); leave the `MOVED` wording alone.

⚠️ This is consequential, not cosmetic: the audit **refuted** the "no live consumer" suspicion —
both skills tell a working session to emit fingerprints and *inherit behind HOLDS*. So a false
`HOLDS` is permission to skip evidence. While you are there, soften the verdict text so it reads as
a **routing aid** rather than permission: build identity is not the truth, scope or source
dependency of every sentence in a group (`reports/DOC_OVERHAUL_AUDIT.md`, the fingerprint finding).

### A3 · `prose_defer` is dead

`grep -c prose_defer tools/doccheck.py` returns its own definition only — a derived flag with no
consumer. **Remove it, or give it the consumer it was written for and say which you did.** ⛔ If
removing it changes any emitted line, that is not dead code — stop and report.

**Group A done when:** `doccheck` GREEN · the new `MARKER INTEGRITY` line emitted and quoted · the
marker-on-disk and marker-parsed numbers **both** appear and differ by exactly the known gap ·
`FINGERPRINTS` output quoted before and after · a **falsifier** for A1 and A2 proving each fires
(the worked precedent is `_selftest` in `tools/flpk_extract.py`: a fixture, plus a control that
passes either way, plus proven discrimination against a scratch copy with the fix reverted).

## 3 · Group B — the pack model (one commit)

### B1 · `.rgignore` ships to players

**Verified:** `python tools/pack_predict.py .` lists `.rgignore` among the 5 root files in the
predicted pack. It is an agent-tooling file with no player use. Add the ignore rule to
`metadata.lua`'s `ignore_files` **and** its mirror in `tools/pack_predict.py`, exactly as
`*/.agents/*` was added at `9726389`. ⛔ Comment-line and ignore-list edits to `metadata.lua` are
ordinary work; **no Lua logic**. Check `grep -c '^\s*--' metadata.lua items.lua` first — **0 means a
`POST_UPLOAD_CLOSE` restore is owed and you must stop.**

### B2 · The ignore list is duplicated in two places with no parity gate

`metadata.lua`'s `ignore_files` and `pack_predict.py`'s `IGNORE` are hand-kept copies. They agree
today; nothing makes them. **Add a parity check to doccheck** — the two lists equal, in order — and
make it **RED**, because a drift here silently changes what players download. ⇒ This is the same
class as A1's silence, and it is the cheapest gate in this brief.

**Group B done when:** `pack_predict` models one fewer file, and the number is emitted not typed ·
the parity gate fires RED on a deliberately drifted copy, then GREEN restored (prove it, don't
assert it) · `Code/` has no diff.

## 4 · Group C — the documentation repairs (one commit)

### C1 · The marker obligation is documented nowhere live

*"Changing an item's status ALSO means updating its marker"* lives only at
`prompts/perma/HANDOFF_ORCHESTRATOR.md:119`, a prompt whose own retirement trigger has fired.
⭐ **This is the previous pass's own miss** — `0c6fd1f` homed three rules out of that same file and
left this one. Home it at the **authoring entry point**, per the audit's recommendation: WORKFLOW's
owner-decision mirroring rule. The register banner already tells readers to change the source and
regenerate; what is missing is the **writer's** mandatory status-change rule.
Verify with: `grep -rn "updating its marker" --include=*.md . | grep -v docs/archive`.

### C2 · Three retired things have no retirement banner at their executable entry

Audit finding, verify each: `IMPLEMENT_PROMPT.md`'s own opening still says **"Fire with"** and it
carries no spent/do-not-fire banner (it is spent and was wrong four times) · `SELFCHECK_PILOT.md`'s
payload still instructs a real boot and prototype, and `reports/SELFCHECK_PROMISE_COMBINED.md:98`
still routes to it · `HANDOFF_ORCHESTRATOR.md` still holds sole-home content after its removal
condition fired. **Put the retirement at the executable entry and remove affirmative firing
routes.** ⛔ **Delete nothing** — the pilot's removal is the owner's call under ck133, and
`IMPLEMENT_PROMPT.md` is kept deliberately as a record.
⚠️ `IMPLEMENT_PROMPT.md` and `PLAN_TODO.md` are **gitignored** — real, on disk, not committed. Fix
them anyway and say so; a firing route in ignored material still fires.

### C3 · Three shipped comments read as machine output

The previous pass rewrote hazard ids to full paths, correctly but mechanically:
`metadata.lua:159` now breaks grammatically — *"and `editor/version rail (agent/prompts/perma/RELEASE.md
§ Release rails)` as reworded 2026-08-24 puts…"*, where the long parenthetical sits between subject
and verb · `:159` backticks the whole phrase and `:180` does not · all three lines, plus
`items.lua:203` at ~140 chars, break the files' ~78-char comment wrap.
**Shorten to a consistent short form** (`RELEASE.md § Release rails`) and re-wrap to match the
surrounding comments. ⛔ Meaning must not change, and the reference must still resolve.

**Group C done when:** every claim above re-verified or refuted in writing · the obligation
greppable from its new home and quoted · no file deleted · `doccheck` GREEN.

## 5 · Order, and the stop rule

**A → B → C, each its own commit.** ⛔ **If you cannot finish a group, STOP and report with the
previous groups complete and committed.** A half-done group is the failure this split exists to
prevent. Any group standing alone leaves the tree consistent.

## 6 · What may not be claimed

- **A count is not a fence, and a count is not a finding** — check where each hit LANDED. The
  previous brief said "two comment lines" off a sweep piped through `sort -u -t: -k1,1 -k3,3`, which
  collapses repeat hits of the same token in one file. The real figure was six. ⇒ Enumerate; never
  trust a deduped count, this file's included.
- **Never state an absence from a truncated grep.** `| head` is not an enumeration.
- **A fix invalidates its own tests** — re-base any harm leg on the pre-fix body and run the whole
  check, not the leg you changed.
- **A check scoped so it cannot fail is not a check.** Ask what would make each of yours pass for
  the wrong reason. ⇒ **Every gate you add here must be shown to FAIL on a deliberately broken
  copy**, then restored — `sha256sum` the restore. That is the standard the `flpk` fix met and it is
  the standard for this pass.
- **"Done" needs its diff-stat and its doccheck line.** No count hand-typed
  (`python tools/doccheck.py --emit-counts`).

## 7 · Handover — the adjudicator reads this against the diff, not your prose

Land it as `docs/agent/reports/REPAIR_PASS.md`. Per defect: **the claim as this brief stated it · did
it reproduce · what you changed · the command that proves the gate fires · the command that proves
it is green now**. Plus at the top: `doccheck` before/after, `MARKER INTEGRITY` and `FINGERPRINTS`
lines verbatim, `pack_predict` before/after, your shas with diff-stats, and ⭐ a **"not done"** list
with reasons — on a job this size an empty one reads as a missing list, not a clean sweep.

## 8 · Stop conditions — report, never push through

A file you are about to write is dirty or owned by a running peer · doccheck RED for a reason
outside your lane · a `POST_UPLOAD_CLOSE` restore is owed on `metadata.lua`/`items.lua` · a rewrite
would change a sentence's meaning · **anything that looks like an owner decision**, especially
marker semantics · a defect in §2-§4 does not reproduce · a group cannot complete.

Close-out: *"nothing load-bearing exists only in my conversation."* If false, write it down first.
