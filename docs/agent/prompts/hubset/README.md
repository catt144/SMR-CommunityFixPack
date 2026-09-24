# hubset: the chain manifest

Effort: build, verify and audit the hub release set as one release. The set is eight vanilla and pack
repairs on the hub, passage and migration surface: [C114](../../bugs/C114.md), [C115](../../bugs/C115.md),
[C116](../../bugs/C116.md), [C117](../../bugs/C117.md), [C42](../../bugs/C42.md),
[C111](../../bugs/C111.md), [F127](../../bugs/F127.md), and P3, two missing `SRC:` pins in
`Code/Fix_VacuumWalks.lua`. Authored 2026-09-24 at the owner's ask, on `main` at `e11a131`.
Method: `docs/agent/support/CHAIN_METHOD.md`. Evidence base, in reading order:
[HUB_FIELD_FINDINGS_2026-09-24.md](../../reports/HUB_FIELD_FINDINGS_2026-09-24.md) (read its §7
corrections), [MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md](../../reports/MIGRATION_CROSSCHECK_HUB_RESWEEP_2026-09-24.md),
then [MIGRATION_AUDIT_2026-09-24_D_hubs.md](../../reports/MIGRATION_AUDIT_2026-09-24_D_hubs.md). Each
entry is the authority for its own fix. Where the entry and a brief disagree, act on the entry and
report the disagreement.

## Owner rulings this chain obeys (2026-09-24, verbatim)

- **One release:** "If possible and we are going to fix them all I would like to do the fixes and get
  them out all at once. They all touch surfaces near the same thing so if we push one part people read
  that as fixed, and then if they hit the surface of one of the other parts then they say 'well you
  said it was fixed but X is still borken'".
- **Membership:** "if p3 is just makeing something better we already ship or correcting it and its
  ready to go we shoul,d just add it same with p2." C99 is out of the set; the owner has never
  reproduced it.
- **A member refuted by its sitting:** "it depends on the circumstances and information". There is no
  standing drop-or-hold rule. Stop and bring the owner the facts.
- **Order:** "making the one that you need measurements last right before the audit."
- **Routing:** "Codex will build fable will audit." The owner chooses every model; no link body names
  one.
- **Out of scope:** "For the load order we will decide how and what we implement after the fixes are
  done." No link changes load order or the VacuumWalks load-time guard.

## The queue

| # | file | tag | owner needed? | what it drains |
|---|---|---|---|---|
| ~~01~~ | ~~`01_WORKTREE_AND_SMALL_FIXES_fanout_level_3.md`~~ | ~~fan-out 3~~ | ~~may route C111 text~~ | ~~the `hubset` branch and worktree; P3 pins; C42; F127 (desk check first); C111~~ |
| ~~02~~ | ~~`02_C115_RESCUE_REVALIDATION_high.md`~~ | ~~high~~ | ~~no~~ | ~~C115: an obsolete own-home rescue stops at the start of `Transport`~~ |
| ~~03~~ | ~~`03_C117_SALVAGE_DRAIN_high.md`~~ | ~~high~~ | ~~no~~ | ~~C117: a busy hub passage's in-flight colonists keep their hub endpoint through a disconnect~~ |
| ~~04~~ | ~~`04_MEASURE_SITTING_owner.md`~~ | ~~attended~~ | ~~✅ keyboard, the reporter's save~~ | ~~hub footprint, marker and rescue-anchor readings (four console lines)~~ |
| 05 | `05_C114_C116_HUB_ACCESS_high.md` | high | no | C114 access fallback and C116 marker lifetime, sharing one physical on-hub test |
| 06 | `06_SITTING_PREP_medium.md` | medium | no | predictions, fixtures and the script for 07 |
| 07 | `07_VERIFY_SITTING_owner.md` | attended | ✅ keyboard | every member in the real game, fix on and off |
| 99 | `99_AUDIT_high.md` | high | ✅ raises | adversarial audit of the branch; SHIP / SHIP WITH CHANGES / NO SHIP; on SHIP and the owner's go, the merge and the records |

## Ordering

- **01 first.** It creates the branch and worktree every build uses.
- **02 and 03 after 01**, in either order, **never at the same time**: both register a module in
  `metadata.lua` and `items.lua`.
- **04 can fire any time**, even before 01. It builds nothing and runs on the owner's copy of
  TheGodUncle's save.
- **05 after 04 and after 02 and 03.** It is last among the builds because its design needs 04's
  measurements (owner's order).
- **06 after 05; 07 after 06; 99 last**, on a folder holding only 99 and this README.
- If a link finds a member cannot be built safely, it stops and routes the facts to the owner, per the
  ruling above. The chain continues with the other members only on the owner's word.

## Binding chain rules

1. **Staleness first.** Run `git log --oneline -10`, `git pull`, `git status --short` in the main tree,
   and `git -C ../SMR-BugFixPack-hubset log --oneline -5` once the worktree exists. Compare each input
   you are given from `e11a131` to HEAD. Re-derive every cited game line with `grep -n` on the archived
   `1.1.1.405907` tree before relying on it. Claude and Codex seats share this tree; Codex is invisible
   to `ListAgents`. Never touch a file you did not change; commit by explicit pathspec
   (`git commit -F <msg> -- <paths>`), never `-a`.
2. **Where things go.** Code (`Code/`, `metadata.lua`, `items.lua`) and desk harnesses (`tools/desk_*.py`)
   go on the `hubset` branch, in the worktree `B:\Dev\SMR\SMR-BugFixPack-hubset`. Everything under
   `docs/` goes to `main` in the main tree. Nothing from the set reaches `Code/`, `metadata.lua` or
   `items.lua` on `main` before 99's merge. The rig loads whatever the junction points at (WORKFLOW
   "Release marking"); only the attended links repoint it, and they hand it back.
3. **Inbox / outbox.** Read `## Notes from upstream` at the bottom of your link first. On close-out,
   append your outbox to the next link's inbox and to `99_AUDIT_high.md`'s, strike your row in the
   table above, `git rm` your own link, and commit those docs together on `main`.
4. **Route, never drop.** A finding outside your fence is filed (`smr-bug-library`) or routed to the
   owner; a drift instance, however small, goes into 99's inbox. Never silently correct one.
5. **Every fix follows `docs/agent/FIX_POLICY.md`:** its §1 technique ranking, §2 `Require` checks and
   manifest pins, §3a save and blocking-frame disposition, §4 intent tells. Each module states its
   MANIFEST and a per-module stand-down on an unknown shape.
6. **Evidence.** Any log a verdict cites is archived in the citing commit under `docs/archive/logs/`.
   Tag design claims MEASURED / SOURCE / INFERRED.
7. **Self-split** at a clean commit boundary into a continuation link that is a full chain member,
   rather than running to the edge of a context window.
8. **No status flip** on an entry except by evidence: desk results make a fix `fixed`-pending-play at
   most; `tested-attended` needs the owner's eyes in 07.

## Terminal lifecycle

After 99 closes, in either form, archive this README to `docs/archive/prompts/hubset/README.md` (a
new file; never overwrite an archived one), remove the `hubset/` row from `docs/agent/prompts/README.md`,
and leave no live `docs/agent/prompts/hubset/` directory.
