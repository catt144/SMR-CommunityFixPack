# Desk instrument repair + C90 reach — one run, two legs, sequenced

**For:** Astra (Codex), fan-out permitted. **Filed by:** orchestrator, 2026-09-12, owner-fired.
**Lifecycle:** root one-off — `git rm` this file in your landing commit and add its grave row to
`docs/agent/prompts/README.md` ("Root — live one-offs" table), same shape as the rows already there.

**Why one run:** both legs are desk-harness work against shipped Lua, both end in a runnable control, and
they are **ordered** — leg 2's verdict is read through the instrument leg 1 repairs. Do not invert them.

**⛔ Keep a todo list live from the first minute** and update it the moment each item changes state. The
owner reads that list to decide whether to step in. One item per numbered task below, minimum.

---

## 0 · Orient (mandatory, before any edit)

- `docs/agent/STATE.md` — build state, hazards, open gates. The whole file.
- `docs/agent/FIX_POLICY.md` §1, §2a, §3a — what a core change costs.
- `docs/agent/bugs/C90.md` — the defect leg 2 measures. Read **all** of it, including "Not opened".
- `tools/desk_migration_cluster.py` — the instrument leg 1 repairs.
- `tools/desk_c89_faction_gate.py` leg **(k2)** — the template leg 2 copies.

**Standing rule for this run:** anything else interesting you find, **file it as a `cand` entry, do not
fix it.** That rule is what produced C90 and C91 and it holds here.

---

## 1 · LEG 1 — repair `tools/desk_migration_cluster.py` (lands; do this first)

`deskbench` currently carries one REFUTED row, pre-existing since `9bc4360` (09-11) and confirmed by
running the harness at `59c8c47^`: `desk_migration_cluster.py` still loads
`Code/Fix_DomeFreeSpaceMismatch.lua`, which F60's retirement deleted. A real failure can hide behind it.

**⛔ Do not delete the F60 legs.** A fix — here, a retirement — invalidates its own tests; the harm legs
still have to demonstrate the harm on the body that carried it. The harness already supports this:
`module_text(name, rev=None)` and `module(rt, name, rev=None)` take a git revision. Re-base the F60 legs
(`desk_migration_cluster.py:231-242`) on the pre-retirement body from git.

**⛔ Do not disturb the F51 legs** (`:147`, `:153`, `:165`) or any other demand in the file. `F51.md:32`
and four separate `MIGRATION_DEV_REPORT.md` confidence lines cite this harness by name; every demand it
currently holds must still hold after your repair, at the same count.

Done when: `deskbench` is green with no REFUTED row, every pre-existing demand still passes, and the F60
legs still demonstrate F60's harm on F60's own body.

**This leg lands.** It is an instrument with no player surface and no decision attached.

---

## 2 · LEG 2 — measure C90's reach (does NOT land a fix)

C90: a `DataPatch` module whose `apply()` self-check DECLINED still patches shipped presets. `run()` never
reads the apply verdict. `Fix_FactionDomeSizeGate` carries a `self_check_passed` flag; `Fix_SaintBlessing`
and `Fix_SinkholeIndestructible` do not. The entry tiers reachability **U — unknown** and says so honestly.

Three questions, all of them from C90's own "Not opened" list. Fan these out if you like — the census (2c)
is the broad-enumeration half and is the natural one to split.

**(2a) What does each unguarded pass write before it reaches its missing target?**
For `Fix_SaintBlessing` and `Fix_SinkholeIndestructible`, with one `Require` target removed: list, in order,
every preset write the pass performs before the first use of the missing target. C90 says both were "NOT
traced line by line" and that "both need the same read before anyone calls them safe." Do that read.
`Fix_SinkholeIndestructible` may be benign because the pass re-checks what `Require` checks — confirm or
refute, do not assume.

**(2b) A control, built from the (k2) template.**
Point a (k2)-shaped leg at each unguarded module with a `Require` target removed. Expected: presets edited
while the entry reads `inactive`. New file `tools/desk_c90_datapatch.py`, or an added section to an existing
harness if that is cleaner — your call, say which and why.

**(2c) Census: does `OnDataReady` have the same gap, or a worse one?**
C90 notes `OnDataReady` "takes no id and does no veto or status check at all, so it may be worse, but no
site was enumerated." Enumerate every `OnDataReady` site and every `DataPatch` call site across `Code/`
(49 registered modules, 50 `Code/*.lua` files per `doccheck --emit-counts` — re-emit, do not trust that
number). For each: does a decline path exist, and is it guarded? A total is not a set — give the members,
not just a count.

**⛔ LANDING BOUNDARY — read this twice.** Leg 2 lands **an updated `docs/agent/bugs/C90.md` and the
control**. It does **not** land a code fix to any module or to `00_Core.lua`. The fix shape is an open owner
decision, still unruled: per-module `self_check_passed` (three lines each, no core change) versus capturing
the apply verdict in the core (one place, but a seam all 49 modules sit on — a §3a/§1 decision). Landing
either pre-empts the owner and puts an unruled change into v10. Update the entry with what you measured,
sharpen the recommendation if the measurement supports one, and stop.

**⛔ Also forbidden, from C90 itself:** do not gate the pass on `entry.status == "active"`. That breaks the
live re-apply path `00_Core.lua` deliberately supports.

---

## 3 · Verification pass — adversarial, and not your own switch

Re-verify your subagents' work yourself, treating each report as a **claim**, not a result. Two distinct
things are required and they catch different failures:

**(3a) Independent reading** — does the conclusion actually follow from the measurement? Most refuted
claims in this project sat on *correct* measurements and wrong inference.

**(3b) A falsifiable instrument — the part that is easy to skip.**
For every leg you add or repair, revert the guard in a **scratch copy** and require the leg to **FAIL**.
A control that passes both with and without the guard measured nothing, and it *looks like success* — no
reader downstream can catch it, because there is nothing to see. The builder's own control switch does not
count as independent; use scratch variants.

This is not hypothetical here. F59's harness passed three legs and a full audit while a stubbed
`GetResidenceComfort` had silently deleted a `destroyed` validity test and manufactured the harm it was
measuring. Everyone in that chain reasoned correctly over a control that could not fail.

**Desk-harness shims:** `lupa` runs of shipped bodies need the usual `ipairs`/`pairs`-on-false, `Min`/`Max`-
on-nil and `table.get` shims, and bodies must load under their real file name + line offset so error lines
match the game log. ⛔ A stub for a function that can **refuse** (validity/nil) is a behaviour change, not a
tolerance — that is precisely the F59 trap.

---

## 4 · Land + hand back

Coordination is git-visible: **the push is the claim.**

- Commit the harness repair and the C90 material; push.
- Commit your report **verbatim** to `docs/agent/reports/` so a Claude audit can read exactly what you
  wrote. Do not summarise it away.
- `git rm` this brief; add its grave row to `docs/agent/prompts/README.md`.
- ⚠️ **Sibling sessions edit this tree.** Check `git log` / `git status` before every shared-doc write; all
  sessions share one git identity, so `--author` attributes nothing — identify by sha + diff, and **list
  your own shas** in the handback. Commit with a pathspec (`git commit -F msg -- <paths>`) so you do not
  sweep up a peer's staged changes. If `docs/agent/bugs/` shows foreign ` M`/`??` rows, do not `--regen`
  the index over them.
- Run `python tools/doccheck.py` before committing docs; red blocks.

**Handback, in the report:** your shas; whether `deskbench` is green and at what demand count; the answer
to each of 2a/2b/2c; every scratch-variant falsifier you ran and that it FAILED as required; anything you
filed rather than fixed; and anything you could **not** settle, named — an unchecked-artefacts list is
where the next reader looks for the wrong conclusion, so write it even if it is empty.

**Next reviewer:** the orchestrator does a surface check only. If it fails that sniff test it escalates to
a dedicated cross-vendor Claude agent. Write the report so a fresh reader with no context can audit it.
