# HAZARD_KERNEL_PASS — execute the owner's 2026-09-13 rulings on STATE's kernel

**Fire with:** a fresh session rooted at `C:\Dev\SMR-BugFixPack`. Tool-neutral. Docs plus
**comment lines only, no shipped Lua logic** — that is the fence, and it is behavioural.
Written 2026-09-13 by `smr-bugfixpack-da`, which analysed this and is **deliberately not
implementing it** — the owner separated implementor from judge after being bitten by
half-finished work that added more work than it removed.
⚠️ **CORRECTED 2026-09-13, first firing:** the fence first read "two comment lines", which
turned an arithmetic slip into a rule. A Codex run found a third shipped citation and
correctly STOPPED rather than cross it. The fence is behavioural; the count is whatever the
sweep finds. See §3's citation block — the real figure is six, and why it was wrong matters.
`git rm` this file when it has fired; its grave is the commit that lands phase 2.

⚖️ **You implement. A different session adjudicates your OUTPUT, not your report.** Write the
§6 handover table as you go, not at the end.

---

## 0 · Authority — these are the owner's rulings, not proposals

Ruled 2026-09-13 in conversation, recorded here because agent docs are the only place they exist:

1. **The harm floor is MODERATE.** *"Anything before that is low risk and probably not worth the
   space."* Below the floor a rail leaves the kernel — it is **not deleted**, it moves to its gate.
2. **The three-part admission test in §2 is ADOPTED** (owner: "Yes").
3. **H-04 MOVES** out of Hazards into the rules/claims section (owner: "Move") — it passes the
   test but is a rule about claims, not an action.
4. **H-10 is DROPPED** from the kernel (owner: "agreed"), because it is double-gated — see §3.

⛔ **NOT in scope, do not touch:** checklist **170**'s three policy calls (marker vocabulary,
normalised byte accounting, reading routes) are the owner's and still open · **D4** / any
`archive_settled.py` run · any **status** change to any checklist item or entry · the marker
vocabulary in `tools/doccheck.py` · `CLAUDE.md` (editing it drifts `AGENTS.md` and turns doccheck
RED for everyone).

## 1 · Anchor — run these; ⛔ quote no number from this file

```
git -C C:/Dev/SMR-BugFixPack status -sb | head -1
git log --oneline -1
python tools/doccheck.py | tail -1
python tools/doccheck.py | grep -E 'STATE \+ STUBS|WAITING|PUSH SET'
```

⚠️ **The tree is busy** — several interactive peers share this checkout, and at least one is
mid-flight on **C92** (`bugs/C92.md`, `reports/C92_INVESTIGATION.md`, `prompts/C92_PLACEMENT.md`).
All sessions commit under **one git identity**, so `git log --author` attributes nothing; identify
by **sha + diff** and list your own shas.
⛔ **A pathspec is only HALF a commit fence** — `git commit -- <paths>` takes the *working-tree*
content of a path you name, a peer's unstaged edits included. Re-check `git status` **immediately
before every write**, not once at the top. On a file two sessions are inside, stage your own hunks
(`git add -p`) and commit without a pathspec. Rules: `agent/WORKFLOW.md` § "Writing in a shared tree".
⛔ The pre-commit hook can go RED on a peer's in-flight `TEMPORARY` probe. That is not yours to fix
and **never** a reason for `--no-verify`. Wait, or report and stop.

## 2 · The admission test — adopted wording, install it verbatim

Install in `agent/prompts/perma/STATE_EVICTION.md`, replacing the one-line Hazards admission test
in its "The boundary" section, **and** reflect its short form in `STATE.md`'s `## Hazards` heading.
⛔ **Those two move as a pair** — the heading carries the short form and must not contradict the long.

> **1 · HARM — name the victim.** Who is worse off, and can they be made whole by the next command?
> A mechanism is not a victim: *"files get deleted"* is not harm if nobody wanted them. **Floor:
> moderate.** Below it, low risk, not worth kernel space.
> ⛔ **A silent harm outranks a loud one of the same size.** A loud failure self-corrects; a leg that
> measures nothing and hands you a number you trust does not.
>
> **2 · UNIVERSALITY — every agent, or one role?** STATE is read by every session, including a
> read-only QA pass. If only a release, playtest, junction or triage session can reach it, the rail
> belongs in **that role's entry doc**, not the kernel. Destructive rails are role-gated by
> construction; the **epistemic** ones — what you may not read-and-conclude, what you may not claim
> — are the universal ones.
>
> **3 · GATE — can a machine catch it?** If a hook or tool already hard-fails on it, the kernel line
> is belt-and-braces: **cite the gate instead.** If a machine *could* catch it and nothing does, the
> entry is a **placeholder** and the real deliverable is the check — the entry leaves when the check
> lands.
>
> ⇒ **A hazard is a failure that has not yet been converted into a gate.** Graduating is the normal
> end of a hazard's life. That is the list's outflow, and without one the list only grows: every
> entry was admitted for a real reason, so strictness at the door can never be enough.

## 3 · Phase 1 — the hazard pass (commit this on its own)

**Stays, untouched:** H-03, H-05, H-08, H-09. ⛔ Do not reword them.
⚠️ **H-08 and H-09 are the silent class** and H-09 is documented in **no other live file** — if you
touch either by accident, that is a stop.

| # | ruling | where its rail goes | notes you must verify, not trust |
|---|---|---|---|
| **H-10** | OUT — double-gated | cite the two gates in ~one clause (put it in the Hazards preamble or H-09's line) | `doccheck.py`'s `MODULE SETS` compares `Code/*.lua` ↔ `items.lua` ↔ `metadata.lua` code list by **symmetric difference**, RED, every commit. `tools/upload_preflight.py:174` + `:200` re-check it at **pack** time and also check **order**. Confirm both still do before you delete the prose. |
| **H-01** | OUT — weak harm (git holds the record) | **author** the tag rail into `perma/RELEASE.md` | ⛔ `RELEASE.md` currently contains **no mention of the tag at all** — this is authoring, not a move. Also **add `python tools/upload_preflight.py` to `RELEASE.md`**: it is mandated in `PUBLIC_SURFACE_SWEEP.md` but NOT in the release prompt, which is a real gap. |
| **H-02** | OUT — weak harm (next upload supersedes a double-bump) | `perma/RELEASE.md`, which already cites H-02 twice | Heaviest citation web. Keep the `metadata.lua` hand-edit exception (the ✅ clause) with the rail — it is what makes ordinary work legal. |
| **H-07** | OUT — weak harm | `reports/PARKED_OPTIN_REFERENCES.md` | That report is the restore record; the rail belongs at its head. |
| **H-06** | **FAILS** the harm test — no victim | `facts/EF-056.md` already holds it in full | Measured 2026-09-13: the owner's manual labelled saves carry **no `autosave` tag**; only autosaves carry `autosave=true`, and the rotation enumerates by that tag, so their saves cannot be enumerated. ⛔ **EF-056 STAYS as a fact** — the engine behaviour is real and measured. Only the kernel hazard goes. ⛔ The live rider *"never stage a fixture FROM an autosave"* (a byte copy carries the tag) must survive — it is already at its gate in `PLAYTEST_CHECKLIST.md`; confirm that, do not move it. |
| **H-04** | **MOVE**, do not delete | STATE's `## Rules in force` | Passes the test; it is a claim rule, not an action. |

### Citations — ⛔ the count is not the job, the landing is

Emit each, do not trust these numbers (measured 09-13, already drifted once):

```
for h in H-01 H-02 H-04 H-06 H-07 H-10; do
  echo "$h"; grep -rn "\b$h\b" --include=*.md docs/ | grep -v docs/archive | grep -v STATE.md
done
```
Cross-check only — a wild divergence means re-derive, not proceed: H-02 ≈ 24, H-10 ≈ 26,
H-04 ≈ 10, H-06 ≈ 7, H-01 ≈ 1, H-07 ≈ 1.

⛔ **SIX citations are NOT in markdown and a `--include=*.md` sweep misses every one.** Three are
in shipped files — `items.lua:203` (H-10), `metadata.lua:159` **and `:180`** (H-02) — and three in
`tools/doccheck.py` (`:1396`, `:1437`, `:1471`, all H-10). Enumerate them yourself with **no dedupe**:
`grep -rno "H-0[1-9]\|H-10" --include=*.py --include=*.lua tools/ Code/ metadata.lua items.lua`
⚠️ The first version of this brief listed three, because its own sweep piped through
`sort -u -t: -k1,1 -k3,3` — one line per file-and-token pair, which silently collapses repeat hits of
the same id in the same file. ⭐ That is §5's *"a grep count is not a finding"* committed by the
brief's own author, through a flag added for tidiness. Trust the enumeration, never the count.
`items.lua` and `metadata.lua` are **shipped files**; these are comment lines only, which is
ordinary work under H-02's own exception, but ⚠️ the Mod Editor writeback strips every comment from
both on upload, so never commit either while a `POST_UPLOAD_CLOSE` restore is owed
(`grep -c '^\s*--' metadata.lua items.lua`; **0 means the restore is owed** — then stop).

**Rules for a rewrite:** a citation to a moved hazard points at its **new home**, not at a deleted
label. `H-06` → `EF-056`. ⛔ **`docs/archive/` is never edited** — archive hits stay as they are and
are not counted as work. Two hits are in `reports/DOC_OVERHAUL_AUDIT.md`'s own verdict table: that
is a **record of an audit run under the old criterion** — leave it, do not "correct" it.
⛔ A rewrite that changes a sentence's meaning is a stop, not a judgement call.

**Phase 1 definition of done** — all five must hold:
1. `doccheck` GREEN, and `STATE + STUBS` emitted before and after.
2. Every removed rail is **quotable from its new home** — paste the line in §6.
3. **Zero** live-doc references to a hazard id that no longer exists (`docs/archive/` excluded).
4. H-03, H-05, H-08, H-09 **byte-identical** to their pre-pass text (`git diff` proves it).
5. STATE's `## Hazards` heading and `STATE_EVICTION.md`'s test do not contradict each other.

## 4 · Phase 2 — the redundancy pass (a SEPARATE commit)

⛔ **If you cannot finish phase 2, STOP and report with phase 1 committed and complete.** A
half-done phase 2 is the exact failure the owner split this job to avoid. Phase 1 standing alone
leaves the tree consistent; phase 2 half-done does not.

**(a) `## Rules in force` — seven lines restate a rule that has a canonical home, and SIX already
carry the pointer and then restate it anyway.** Verify each landing before collapsing it to a
pointer; if a target does not hold the rule in full, that line **stays** and you say so.

| STATE rule | canonical home to verify |
|---|---|
| Both-mods-loaded is normal | `agent/WORKFLOW.md:510` — a whole section |
| Status words (`tested-attended`/`-unattended`, bare `tested`) | `agent/WORKFLOW.md:411` |
| Replies are PULL-ONLY | `agent/WORKFLOW.md:76` rule 5b |
| fredware / no player load-order advice | `agent/FIX_POLICY.md` §8, lines 767-778 |
| ck118 decline-by-behaviour | `agent/FIX_POLICY.md` §2a, lines 203-235 |
| Every upload overwrites both page bodies | `docs/UPLOAD_WORKFLOW.md:375` |
| **STATE.md's own format rule** | `perma/STATE_EVICTION.md:14` — STATE spends bytes telling the eviction prompt a rule that prompt already states |

⚠️ Those line numbers are from 09-13 and **will drift** — re-derive every one. An empty
`git diff <sha>..HEAD -- <path>` does **not** prove a line number holds: a file's last write can be
an *ancestor* of your anchor. That mistake is on record (`.claude/PLAN_TODO.md`, defect 1).

**(b) `## Open owner decisions` → one line plus a pointer to `docs/WAITING_ON_YOU.md`.**
Why it is safe: `doccheck.py`'s own comment says *"Until an item carries a marker its row is
INFERRED from the header's prose plus STATE's open-decisions section."* Markers are the real source;
STATE's prose serves only the items still unmarked. ⛔ **So this is NOT a free delete** — emit
`python tools/doccheck.py | grep WAITING` **before and after**, and the owner-row count and every
`ck` number must be **unchanged**:
`sed -n 's/^| \([0-9]*\) .*/\1/p' docs/WAITING_ON_YOU.md | sort -n`.
⛔ **The literal idioms `Owner OWES: ck##` and `STILL OPEN: <n> <word>` are what the parser reads.**
Reword either and an owner row vanishes silently — that happened on 09-13 and cost checklist 53.
If collapsing the section would drop any row, **keep the enumeration** and report that the collapse
is blocked on markers landing. That is a finding, not a failure.
⚠️ Found 09-13, **report it, do not fix it**: STATE's `STILL OPEN:` names **47** and **152 c**, both
of which carry `status:ruled owner:no` markers and headers reading *"Nothing is owed from you."*
Whether STATE or the marker is right is the **owner's** call.

**Phase 2 definition of done:** `doccheck` GREEN · the `WAITING` line and the full `ck` list
unchanged before/after · every collapsed rule quotable from its named home · each line you left
uncollapsed listed in §6 with the reason.

## 5 · What may not be claimed

- **"Moved" needs the destination quoted.** A rail nobody can read at its new home was deleted.
- **No count is hand-typed** — `python tools/doccheck.py --emit-counts`, and every count carries the
  command *and the filter* that produced it.
- **Never state an absence from a truncated grep.** `| head` is not an enumeration; a claim that
  something is *nowhere* needs the presence side counted.
- **A grep count is not a finding** — check where each hit LANDED. A `--include=*.md` sweep here
  misses three real citations; that is the shape of the mistake.
- **"Done" needs its diff-stat and its doccheck line.**
- ⛔ **A check scoped so it cannot fail is not a check.** Ask what would make each of yours pass for
  the wrong reason before you rely on it.

## 6 · Handover table — the adjudicator reads this against the diff, not your prose

Land it as `docs/agent/reports/HAZARD_KERNEL_PASS.md`. One row per item in §3 and §4:

| item | ruling | new home (file + heading) | the rail, quoted from its new home | citations rewritten (count + the command) | left alone, and why |

Plus, at the top:
- `STATE + STUBS` emitted **before** and **after**, and the Hazards-section byte delta.
- The `WAITING` line and full `ck` list, before and after.
- Your own shas, each with its diff-stat.
- ⭐ **A "not done" list.** Anything you skipped, could not settle, or judged out of scope — with
  the reason. This list is where your work is most likely to be wrong, so make it explicit; an
  empty one on a job this size will be read as a missing list, not a clean sweep.

## 7 · Stop conditions — report, never push through

A file you are about to write is dirty or owned by a running peer · doccheck RED for a reason
outside your lane · a rewrite would change a sentence's meaning · **anything that looks like an
owner decision** (a status, a hazard's wording beyond §2's adopted text, where a rule is filed
beyond §3's table) · a `POST_UPLOAD_CLOSE` restore is owed on `metadata.lua`/`items.lua` · phase 2
cannot complete.

Close-out: *"nothing load-bearing exists only in my conversation."* If false, write it down first.
