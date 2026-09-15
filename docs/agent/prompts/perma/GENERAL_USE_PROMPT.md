# General-use standing prompt (minimal, model-agnostic) — rescoped 2026-09-13, owner ask

Paste this into a fresh Claude Code session for **anything that isn't a scripted
job** — a random question, a player report to triage, quick orientation. **Any
Claude model; the user picks per task. Start with `git log --oneline -10` +
`git pull`** — this file goes stale the moment another session commits.

> ⛔ **THIS PROMPT IS INSTRUCTIONS, NOT A LOGBOOK.** doccheck enforces a
> 220-line cap. A sitting's lesson goes to its proper home in the SAME
> close-out commit: engine behaviour → a new `agent/facts/EF-###.md` (+
> regenerate the INDEX) · result narrative → `agent/bugs/`. The only edits
> this file takes are corrections to its own instructions.

> 📁 **LAYOUT** — `docs/README.md` is the map (`CLAUDE.md`, auto-loaded,
> carries the contract). `agent/STATE.md` is the one mandatory read: current
> build, open gates, active holds. `FIX_POLICY.md` binds any code any session
> writes. `WORKFLOW.md` owns the full reading path, testing checklist and
> probe hygiene — read it before writing or testing a fix; this file does not
> duplicate it.

## Default mode: a player report about the GAME, no other instruction

A pasted screenshot, forum post, or complaint with **no other text** is a
request to investigate **vanilla game behaviour** for `docs/agent/bugs/`
candidate material — **not** an audit of our own mod. Multiple sessions have
burned context defaulting the other way; don't.

1. ⛔ **Do not open `Code/` top-to-bottom looking for whether we caused it.**
   One cheap check settles it: `grep -rl <keyword> Code/`. Empty result ⇒
   vanilla, and it stays vanilla for the rest of the session — the fix pack
   is small enough that this is a real negative, not a maybe.
2. **Cheap known-check, not a deep read:** grep `docs/agent/bugs/INDEX.md` +
   `docs/agent/facts/INDEX.md` for the topic (`smr-bug-library` skill). One
   command; it may already answer "is this known."
3. **Go straight to source.** Live tree:
   `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`. When a
   control is needed, the archived version trees under `C:\Dev\SMR-SrcArchive\`
   (`docs/README.md` "Path translation" for pre-move names). Trace the actual
   mechanism; cite `file:line`, not a paraphrase.
4. **Render a verdict, don't just describe.** DISMISS (no source-verified
   mechanism, or the design explains it) or `cand` (a real mechanism **and** a
   control — "the owner expects a control, not a plausible story"). Never
   file on testimony alone; corroboration is the owner's call, not something
   to chase unasked.
5. This is not a playtest sitting and doesn't touch `STATE.md` unless
   something is actually filed.

## Standing rules (always bind, whatever the task)

- **Never modify the game directory** (`A:\SteamLibrary\steamapps\common\
  Project Spark`); `ModTools\Src` is read-only truth for line numbers.
- **Check `Mars.exe` is NOT running before touching loadable code**
  (`tasklist`) — before, never in the same command as the edit.
- **Fix/file judgments are `FIX_POLICY.md`'s** (§4a who-benefits, §3a
  save-safety, §2 enable-path) — open it before writing any fix, and judge
  by enumeration, never by an entry's own words.
- **Account state: READ IT, NEVER ASSUME IT** — `SMRFixPack.ListFixes()` and
  a leg's own reading are the only valid source; this file never is.
- ⛔ **FUTURE_IDEAS.md is a parking lot** — nothing in it is work.

## Live playtest sitting

This file no longer scripts the sitting — **the agent authors that prompt at
sitting time** from `WORKFLOW.md` ("Probe hygiene", "Testing checklist per
fix"), the `prompt-authoring` skill's playtest instructions and
`docs/PLAYTEST_CHECKLIST.md` (the queue + protocol). Use `SMRTK_SLOTS.md` or
`CO_RUNS.md` when that mode applies. Standing non-sitting work:
`agent/STATE.md` names the active chain. Drone work is
`docs/agent/prompts/perma/DRONE_PROJECT_PROMPT.md`.

## End of session

If anything here changed `STATE.md`-worthy facts (a filed candidate, a lifted
gate), update it per `STATE_EVICTION.md`, commit, push, and say what you did.
Otherwise there is nothing to close out — a random-question session with no
finding needs no ceremony.
