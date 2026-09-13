# The ck158 sitting — the v10 gate (one-off, model-agnostic)

⛔ **This is a LIVE PLAYTEST prompt. The owner is at the keyboard and you are not.** Your job is to set up,
read back, and record — never to claim a result the owner did not see. `tested-attended` is **the owner's
word to grant and nothing else grants it** (status-word rule, 2026-08-15).

⏳ **One-off.** `git rm` this file in the commit that lands the sitting's result, and grave its row in
`prompts/README.md`. If the sitting only partly ran, leave the file and record which legs are outstanding.

**What this gates:** v10. Three modules are built, desk-checked and have **never run in a game**. Nothing
ships until the owner has seen them. Full owner-facing text: `docs/PLAYTEST_CHECKLIST.md` item **158** —
⚠️ read it, do not re-derive the recipes from the modules.

---

## 0 · Orient, then the gate that binds this one

1. `git pull` · `git log --oneline -10` · `git status --short` · `ListAgents` (several sessions edit this
   tree; **Codex is invisible to `ListAgents`**) · read `docs/agent/STATE.md`.
2. ⛔ **THE STALE-PROBE GATE BINDS — this task launches the retail game.**
   `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` · **CLEAN = zero hits**, or every hit is
   declared by this session's own design. Put it in your todo list. A dirty tree means the owner is testing
   something other than what ships.
3. Confirm the build the owner will run is the tree's: `python tools/doccheck.py --emit-counts`. Expect
   **49 registered modules / 50 `Code/*.lua` files / 97 probes**. If those moved, say so before the boot.
4. ⚠️ **`Fix_GhostFarmOxygen` is STILL SHIPPING.** Checklist 156 ruled it retires, but the retirement is
   staged for v10 and has **not landed** — it is in `Code/` and in `items.lua`. It is live in whatever the
   owner boots. Do not tell them it is gone.

**Hazards that apply to this sitting specifically** (`STATE.md` carries the full list):
- **H-02** ⛔ An agent **never opens the Mod Editor** — every save bumps `version`. The owner's sitting sets
  the version, never you, and never by hand.
- **H-09** ⛔ Never stage a packed folder beside a live junction — at equal version the unpacked one wins
  **silently** and the leg measures nothing.
- **H-06** ⛔ Loading a COPY of a campaign runs that campaign's autosave rotation and **deletes the owner's
  autosaves**. Pre-copy every autosave before any load-a-copy step.
- **Both mods loaded is the rig's normal config** (2026-08-12). Do not ask for a clean profile.
- **Cheats are normal on the owner's playtest saves** (owner rule 2026-08-12) — the colonies are oversized
  and underindustrialized and cheats are life support. A cheat is a confound **only** where a reading
  intersects what it changed. Do not ask why.

---

## 1 · How to run it — the shape, not the steps

**ONE boot does all three legs.** The steps themselves live in checklist 158 and are written for the owner;
paste them from there rather than rewriting them, so what they read matches what is recorded.

- **A · C85** — minutes, any 1.1.0 colony.
- **B1 · C89** — two seconds, any dome. ⭐ **This is the real falsifier.** If time is short this is the one
  leg of B worth having.
- **B2 · C89** — a **fresh one-shot colony, 20–30 minutes of ordinary play**. Real play time, not a loadable
  fixture. This is the leg the owner asked to observe personally.
- **C · C88** — minutes, needs **Building Codes → Strict** and the Martian Assembly.

**If the owner has ten minutes: A, B1, C.** Say so up front rather than letting them start B2 and stop.

⚠️ **The console needs its prefix.** Lines starting `*r ` or `*g ` must be typed **with** the prefix: this
console requires it for anything longer than one statement (`PLAYTEST_HELP.md`, "Console input forms").
`*r` runs immediately; `*g` runs on the game's own clock, which is what anything that *changes* the colony
needs. **A line pasted without its prefix looks like it did nothing** — and 2 of 3 FR-1 sittings lost a leg
to a mistyped marker, so give copy-paste blocks, never descriptions.

**`FlushLogFile()` before the first leg and after each one.** The owner reads results from the log; an
unflushed log is an unread one.

---

## 2 · What each leg has to produce before it counts

⛔ **A working building is not a result. The log line is the result.** Each leg below names the artefact that
makes it a pass; without that artefact the leg is **unrun**, not a pass.

| leg | the artefact that makes it a pass | what a MISS looks like |
|---|---|---|
| **A · C85** | `CloggedBuildingRelease: released 1 building(s) stuck 'Clogged after a Dust Storm.' (load)` | no line ⇒ **the fix did not do it**; the building may have come back for another reason |
| **B1 · C89** | a `C89-AB` block ending `GATE ACTIVE on this dome`, with rows reading `shipped=true live=false` | `GATE-ABSENT` or `shipped=not-wrapped` ⇒ **the fix is not applied**; stop, nothing below is worth doing |
| **B1 control** | on a dome of **ten or more**, every row reads `shipped=true live=true` | if it still reads `live=false`, the gate is not a ten-colonist rule and that is a **defect in our fix** |
| **B2** | `C89-PANEL total=0` with the small dome at 3 colonists, **then the dislike APPEARS** at 10 | the dislike never appearing at 10 ⇒ we switched it off rather than gated it |
| **C · C88** | `BuildingCodesPrefab: Building Codes applied to a prefab-deployed <building>` **and** `modifier id=Policy_BuildingCodesStrict percent=-30` | `NO Building Codes modifier on this building` ⇒ the fix did not work; the line says so **on purpose** so a quiet log cannot read as a pass |

⭐ **B1's `shipped=` / `live=` pair is the A/B, in one boot, on the owner's real dome.** `shipped=` is the
game's own rule kept aside so it can be asked. There is **no pack-off leg** here because this module edits
faction data once at load, so isolating it needs a restart with the whole pack disabled. If the owner wants
that leg, it becomes **its own checklist item** — do not improvise it mid-sitting.

⚠️ **B2 can legitimately fail to run.** It needs one of `ProsperityForMars`, `MarsDemocraticParty`,
`WorkersParty`, `NewSol` seated, and **there is no cheat that seats a faction** — it was looked for and the
game has none. If none is seated after a sol or two: **record that the leg could not run and say so.** ⛔ Do
not force it, and do not bank A/B1/C as if B2 had passed.

---

## 3 · Recording the result

1. **Ask for the owner's word per leg, by name.** `tested-attended` for C89 is theirs to grant; A and C are
   theirs to confirm too. ⛔ SKIPs by name, never a total.
2. **Copy the actual log lines into the record**, not a paraphrase — the owner's sign-off should match what
   they can see (a log-only sign-off with no raw lines is ceremony).
3. Update, in this order: the three entries (`bugs/C85.md`, `bugs/C89.md`, `bugs/C88.md`) with an
   **§Attended check** section · their `status` **and** the heading tag (⛔ **doccheck goes RED if you flip
   one and not the other** — this has already happened once) · `docs/PLAYTEST_CHECKLIST.md` item 158 ·
   `docs/agent/STATE.md` · a `SESSION_LOG.md` entry.
3a. ⭐⭐ **AND ITEM 158's STATUS MARKER.** ⛔ **First, the boundary, because it is easy to trip over
   here:** the checklist-marker system arrived from **an ongoing multi-agent, mixed-model effort in a
   SEPARATE TREE**, and what is visible in this tree is a **deliberate partial** landing — that part had to
   be in before this tree moved again, and **the rest lands only after v10 ships.** ⛔ **It is NOT this
   sitting's job to re-derive, re-check, audit or complete it** (owner, 2026-09-12). **Partial is not
   unfinished.** Use the marker; do not investigate it. If something about it looks wrong, **tell the owner
   and carry on with the sitting** — do not stop to prove it.

   **What you actually have to do:** Checklist items
   carry a marker like `<!-- ck:162 status:ruled owner:no -->`, and a register (`docs/WAITING_ON_YOU.md`)
   is built from them. **Changing an item's status means updating its marker in the same edit** — nothing
   in `WORKFLOW.md`, `CLAUDE.md` or `README.md` says so yet, which is exactly why it is said here.
   ⚠️ **Item 158 has NO marker yet** (it is one of ~28 unmarked), so this sitting **ADDS** one rather than
   updating it. ⛔ Match the vocabulary neighbouring items use — do not invent a status word. An item that
   moves without its marker makes the register quietly wrong, and v10 moves several.
4. **Regenerate with the RIGHT flag.** This sitting edits **entries as well as the checklist**, so it needs
   the full `python tools/doccheck.py --regen` — ⚠️ **check `git status docs/agent/bugs/` for foreign
   ` M`/`??` first**, because regen builds the index from every entry **on disk**, a peer's uncommitted
   ones included. ⛔ **If you end up making a CHECKLIST-ONLY edit, use `--regen-waiting` instead** — it
   rewrites only `WAITING_ON_YOU.md` and cannot sweep in a peer's entries.
5. Commit with an explicit pathspec: `git commit -F <msg> -- <paths>`. ⛔ **A pathspec is only half a fence** —
   for a path you *name*, git commits that path's **working-tree** content, including a peer's unstaged edits
   to that same file. On a file another session is also in, stage your own hunks and commit **without** a
   pathspec. Then push.

---

## 4 · What happens next, so the owner is not left holding it

⭐ **`tested-attended` on all three is the last thing standing between the tree and v10.** When the sitting
lands, the next step is `prompts/perma/RELEASE.md` over the outbox's **Held** batch plus the **3 Pending**
entries. Say that to the owner at the end of the sitting; do not start it inside this one.

⛔ **Carry no counts into the release pass.** Re-derive every one: modules ± the retirements, the card count
word, the card headlines, "real defects you cannot see today", **judgment calls three → four (C89)**, and the
six `README.md` claims staged in `RELEASE_OUTBOX.md`'s batch notes. Text comes from
`reports/still-needed/WORDING_RULED.md` under the ⚖️ **VOICE RULE** — plain for players, precise for the two
Paradox developers who plan their hotfixes from our fix list, **no "no guarantees" / "unverified" hedging**.

## 5 · Two things already known, so they are not re-discovered mid-sitting

- **C85's one untested claim:** that *nothing in the game itself* ever clears the clogged state. Seeing that
  needs the whole pack switched off, a restart, and a sol of watching. **It is a separate boot and it is not
  being asked for here.** If the owner offers, it becomes its own item.
- **C88 cannot fix buildings already standing**, and that is not a gap in the test — the game does not record
  that a finished building came from a prefab, so there is nothing to find. The fix reaches buildings
  completed after it is installed, which is why the leg deploys a fresh one.
