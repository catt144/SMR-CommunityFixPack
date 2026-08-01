# One-off prompt — adjudicate the two F86 positions

**Paste everything below into a fresh session.** This is a **one-off**: it is
consumed when the verdict is delivered. Model-neutral — nothing in it depends on
which model runs it.

---

You are auditing a **P1 defect and its proposed remedy** in the Surviving Mars:
Relaunched "Community Fix Pack" (`C:\Dev\SMR-BugFixPack`, git). **A build is
authorised but PAUSED, waiting on you.**

Two agents worked on the same defect, **independently**, and each wrote up its
own position. The owner wants them torn apart before a line of code is written.

- **`docs\reports\F86_DISCOVERY_POSITION.md`** — the session that *found* the defect
  (the PT-20 leg). It ran the game; its claims include real measurements.
- **`docs\reports\F86_SESSION_FINDINGS.md`** — the session that did the *design and
  sweep* work afterwards. It never launched the game; its claims are source
  reading and analysis.

## Your job

**Determine where the project actually stands.** Not "summarise both" — decide
what is true, what is unproven, what is wrong, and what must be measured before
anything is built.

**You may conclude that either document is wrong, that both are, or that the
important risk is something neither considered.** You are not refereeing a
contest between two agents and you owe neither any deference. If the right answer
is "do not build any of this yet", say so plainly.

## Rules of engagement

1. **Confidence labels are claims, not evidence.** Both documents label their
   findings (MEASURED / SOURCE-VERIFIED / REASONED / DERIVED / INFERRED). Treat
   a label as the author's *opinion of their own work*. Re-derive anything
   load-bearing from `ModTools\Src` or the repo yourself. A wrong claim labelled
   MEASURED is worse than one labelled REASONED, because it will be trusted.
2. **Verify against primary sources, not against the other document.** Src is at
   `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` (**read-only,
   NEVER modify**). Game logs are in
   `%AppData%\Surviving Mars Relaunched\logs` — the PT-20 evidence is in the
   2026-07-31 `16.28`, `17.14`, `17.55` files. The pack's code is `Code\`.
3. **`F86_DISCOVERY_POSITION.md` deliberately does NOT incorporate the later
   session's corrections.** That is by design, so the two could be compared as
   independent positions. Do not score it down for "staleness" — instead decide
   whether each correction is itself correct.
4. **Do not build, repair or refactor anything.** No `Code\` edits. Report only.
   If you find a new defect, file it in `BUGS.md` with evidence and stop.
5. **Beware this project's characteristic failure mode: source-plausible and
   false.** In the last two days it has falsified its own recorded "facts" about
   the save hook, class-table safety, `debug.getinfo`, and `Wakeup`. Reading
   source is necessary and not sufficient. Where a claim can only be settled by
   running the game, say so and mark it as owed rather than guessing.
6. **A test that cannot discriminate is worse than no test.** One proposed
   experiment was cancelled during discovery for exactly this reason (the
   tail-call probe). If you propose a measurement, state what each outcome would
   prove, and check that the outcomes actually differ.

## Read first

1. **`docs\agent\ENGINE_FACTS.md` — the whole file.** Several behaviours are the
   opposite of what the code suggests, and it carries the thread-stack
   persistence entry this whole defect rests on.
2. `docs\BUGS.md` — the **F86** entry, and **F02** (the fix under rewrite).
3. `docs\reports\SAVE_SAFETY_REDESIGN.md` — the remedy of record, including the owner
   decisions in §4 and the authorised build in §6.
4. `docs\agent\FIX_POLICY.md` — **§3a** is the newly adopted layer rule; **§4** bars
   gameplay changes; **§1.5** governs full-body replacements.
5. Then the two position documents.

## The claims that gate the build — attack these first

Ranked by how much rests on them. Both documents are represented; the order is
by consequence, not by author.

1. **"Synchronous mod code can never be captured by a save."**
   (`F86_DISCOVERY_POSITION` §3.) The *entire* scope rests on this — it is what
   makes 62 of 74 modules "safe by construction" with no work. Its own author
   flags it as never tested in the negative direction. **If it is wrong, the
   exposure list is meaningless and the build scope is wrong.** Can you prove or
   break it from `cthreads.lua` / `persist.lua`? Is there a cheap in-game test?
2. **The severity tiering** (`F86_SESSION_FINDINGS` §2.1) — "module adds a
   thread" vs "module replaces a vanilla body". **Layer 1 was barred on its
   strength**, so if the tiering is unsound, a barred layer may be needed after
   all. It is REASONED, never measured. Its author names the control that would
   settle it.
3. **The per-load restart** (`F86_SESSION_FINDINGS` §1.4) — that
   `Fix_MeteorFrequency` unconditionally restarts the meteor thread on **every**
   `LoadGame`, re-rolling a 35–115 h timer, so a player who loads frequently
   never gets a meteor. If true this is **currently shipped**, is player-facing,
   and is a defect in its own right. Verify it independently against
   `Code\Fix_MeteorFrequency.lua` and `_fixup.lua`. **Note it collides with a
   MEASURED claim in the other document** — that reinstalling the pack "repairs"
   a damaged save. Both cannot be the whole truth; work out how they fit, and
   whether "put the mod back" is still honest advice to a player. It is undecided
   whether this gets its own F-number.
4. **The exposure list.** `F86_DISCOVERY_POSITION` §4 admits it is a **lower
   bound** and that the transitive case defeats its grep method.
   `F86_SESSION_FINDINGS` §3.1/§4 claims to have closed that with
   `tools/blocking_analysis.py` (seeded from four engine primitives, propagating
   only through unambiguous callees, 633 of 15,106 direct yielders). **Audit that
   tool and its output.** Two membership changes are claimed
   (`Fix_DroneUnreachableForever` in, `Fix_TrainCargoDumping` out) — check both
   yourself. Is 12 right? Is *any* fixed number defensible?
5. **The F02 keying correction** (`F86_SESSION_FINDINGS` §1.1). The discovery
   session proposed keying the `GetDisasterWarningTime` wrapper on the meteor
   descriptor; the design session says that cannot separate the call sites
   because `MeteorStorm` passes the same descriptor, and proposes
   `CurrentThread() == rawget(_G, "Meteors")` instead. **Re-enumerate the callers
   yourself** and decide. Then check the *replacement* is sound: is
   `CurrentThread()` reachable in the mod sandbox, and does the global reliably
   hold that thread?
6. **The upgrade-path hazard** (`F86_SESSION_FINDINGS` §2.5) — saves already
   carry the current `Fix_MeteorFrequency` body *by value*, and it calls
   `SMRFixPack.*` helpers at eight points. Deleting those helpers in a layer-3
   rewrite would kill the resumed thread and stop meteors permanently — **the
   F86 harm delivered by the F86 repair.** Is the stated rule (keep the helpers,
   or guarantee a restart) sufficient? Does it interact with §1.4 and §2.3?
7. **The retroactive heal** (`F86_SESSION_FINDINGS` §2.3) and **command-thread
   self-cleaning** (§2.4). Both REASONED/UNVERIFIED, and §2.3's author calls the
   one-shot latched heal "the weakest link in this report". Decide whether either
   is safe to rely on.

## Also worth your attention

- **The layer-2 rule** — "no mod code after a call that can block". Both
  documents accept it; the discovery session explicitly weakened its
  justification so it no longer depends on Lua tail-call behaviour. Is the weaker
  form actually sufficient? What about a serialised-but-inert function sitting in
  a save — is "harmless dead weight" right?
- **The autosave path.** `SaveGameStart` reaching mods is MEASURED; that
  autosaves take the same path is source-only and was never observed. A temporary
  probe may still be armed in the Test Kit (`Code\97_SaveHookProbe.lua`) — if so,
  a single sol of play settles it.
- **Method review.** `F86_SESSION_FINDINGS` §4 documents two analysis approaches
  that produced garbage before the third worked. Check the surviving method as
  hard as the conclusions.
- **Both self-reported error lists** (`F86_DISCOVERY_POSITION` §8,
  `F86_SESSION_FINDINGS` §5). Use them to calibrate how much each document's
  unverified claims are worth — but verify rather than assume the lists are
  complete.

## Deliverable

Write **`docs\reports\F86_ADJUDICATION.md`** and commit it. Structure:

1. **Verdict up front** — is the authorised build safe to start as scoped? Yes,
   no, or yes-with-changes. One paragraph.
2. **Settled** — claims you independently confirmed, with your own file:line
   evidence. Note which document got there first only where it matters.
3. **Wrong** — claims you falsified, from either document, with proof. Say
   plainly what breaks downstream of each.
4. **Unproven and load-bearing** — claims that are neither confirmed nor
   falsified but which the build depends on. For each: what would settle it, and
   how expensive that is.
5. **Missed by both** — anything the two documents did not consider that you
   judge more important than what they argued about.
6. **What to do next** — an ordered list. If measurement must precede the build,
   say which measurement and why. If the scope should change, say how.
7. **Open decisions for the owner**, with your recommendation and reasoning.

Keep it dense and evidence-first. **A confident wrong answer here is the most
expensive thing you can produce** — this decides what gets built into a mod that
writes to players' savegames. Where you are unsure, be explicit about the
uncertainty and what would remove it.

## Standing project rules

- Update your todo list **as you go**, one item per verifiable unit — the owner
  reads it to decide when to step in.
- **Never modify the game directory.** Src is read-only.
- Commit with
  `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
  and push. Commit messages via `git commit -F <file>` — **no embedded double
  quotes** (PowerShell 5.1 splits them).
- Docs never lag findings: if you falsify something, fix the document that
  carries it in the same commit that records the falsification.
- `docs\FUTURE_IDEAS.md` is a **parking lot, not a backlog** — nothing in it is
  owed, and defects never go there.
- Start with `git log --oneline -10` + `git pull`; this prompt goes stale the
  moment another session commits.
