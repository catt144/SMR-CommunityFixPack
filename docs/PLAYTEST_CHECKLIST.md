# Playtest checklist — the owner's list

## Must_Read_Header
<!-- RULES -->
Rule: Admit an item only when its next action is the owner's: a ruling in words, or a test only the owner can run. [A3: pass]
Rule: Hold the ask in at most eight lines and link its evidence, recipe and reasoning in a pull-only home. [A3: pass]
Rule: Delete an item in the commit that records the owner's action; keep no closed stubs, rulings or history here. [A3: pass]
Rule: Record the owner's ruling where the role that obeys it reads it, and its evidence in `docs/archive/`. [A3: pass]
<!-- /RULES -->

What is waiting on your word or your hands, and nothing else. doccheck enforces the shape: 600 lines,
120 characters a line, only the sections below, eight lines an item. Old bodies are in
`docs/archive/PLAYTEST_ARCHIVE.md` under `## ck<number>`; where each old item went is
`docs/archive/CHECKLIST_PURGE_LEDGER.md`.

## Decide

### 188 — Wildfire: whose report was it, and take the live look or drop it
- F120, the Wildfire report and the handoff name Jäger, but his comment #8 is C99's tunnel bug and
  you said "jager was completely different". Say who reported Wildfire; the agent then corrects or
  confirms the name in F120, the report and the handoff.
- The live look is the only route left to that report: on a 1.1.0 colony, does SPECIAL in the tech
  tree show the cure node without panning, and does Ctrl-F "Wildfire" find it? Five minutes, any
  save, on a scratch copy. Recipe: archive `## ck188`, Leg A. Take it at a sitting, or say drop and
  the report closes as unexplained.

### 188 — Habitat residents walk out on their own: defect, or the price of the building?
- Your C95 sitting: Dermot rode back into the Naturalist Habitat, then left for Fuller #1 once he
  had a job and an apartment there. Source says the jobless-override in the emigration scorer is
  what empties a habitat, because habitats forbid connected work by design.
- Before ruling, one cheap watch next time you are in that colony: does a habitat resident WITH a
  job stay put while a jobless one leaves? If a working resident also leaves, C100's mechanism is
  wrong. Nothing is authored or classified until you say. Entry: `docs/agent/bugs/C100.md`.

### 186 — Skill caps: pick the numbers
- Proposed, not set: warn 3,072 B, hard 5,120 B. Sizes move; read them from
  `python tools/doccheck.py` (SKILLS section), never from here. Caps stay down until you pick.
  Note the largest skill would sit close to the proposed hard cap.

### 181 — The attended monolith audit is the last gate of the doc overhaul
- Your ruling 09-14: automate the monoliths as far as it goes, then a you-and-me second pass over
  all of them. Left to sit over: `docs/agent/WORKFLOW.md` and `docs/agent/FIX_POLICY.md`
  (PLAYTEST_HELP was dissolved; this checklist was rebuilt 09-16). No agent closes the overhaul alone.
- 178 rides on it: STATE's warn cap is +25% until you say the overhaul is done. Then an agent sets
  `STATE_WARN_TEMPORARY = False` in `tools/doccheck.py`; nothing else changes.

### 173 — FIX_POLICY §2a's version-detector ban is wrong in one half
- Reason 2 ("unbuildable from the mod's own fields") is false: the runtime `LuaRevision` is 403908
  on 1.1.0, and the shipped FR-1 temporary mod already guards on it (EF-094).
- Your call: narrow §2a to "behaviour-test whenever the guarded thing is inspectable; a version
  label only where it is not", record FR-1 as a named exception, or leave it as is.

### 172 and 171 — C92 (restore the technology): shipping is HELD until you lift it in words
- Build option B proceeds (`docs/agent/prompts/C92_ACHIEVEMENT_BUILD.md`); no release, no outbox
  entry, no public row until you say so. Knowledge is an accepted deliverable even if it never ships.
- The test route needs your hands: move `account.dat` aside, test, move it back (EF-094). It resets
  your account options until restored, which is why it is your call.
- 171's scope question is overtaken by B; the only residual is whether it ever ships.

### 136 — FR-3 (frame skip and stutter): spend a profiling sitting, or not?
- Its own gate ("decide after link 99") has fired. A profiler session on a large colony would settle
  FR-3 and decide C60 and C81 in the same sitting; a source read cannot measure frame time.

### 148 — Fix toggles: deferred on your "skip"
- Nothing runs until you say start: fire `docs/agent/prompts/fixtoggles/01_SPEC_fable.md`. Two
  sittings are yours (link 03 about 30 minutes; link 11 longer). The three calls, (a) console
  players, (b) release gate, (c) who cut the chain, stay open as written in archive `## ck148`.

### 183 — SMR Tool Kit design calls still yours
- Where the slot engine lives once triggers move to Run: its own page, or riding with Probes.
- Defect 20's remedy: a cursor change, or a persistent banner.
- The cut Stamper is un-parked only in your words; it sits in FUTURE_IDEAS, on no list.

### 169 — The site deploy is your act
- Firing `workflow_dispatch` on the site repo is yours whenever its content changes.

## Run

- SMRTK: confirm 09's new menu layout and positioning in play once; one boot to confirm the
  `MechanizedDepotFood` before/after numbers print (archive `## ck183`).
- F80 (trains): the moment colonists queue at a platform forever or walk past a working station,
  open the agent session BEFORE adding trains; adding trains destroys the evidence.
  `docs/agent/bugs/F80.md`.
- F21 (trains, optional): two reads on any working line re-earn `tested`; skipping costs nothing.
- C40, C42, F99 (colonists and domes): each entry carries its own recipe and takeable condition.
- F16 (PT-30) and F06 (mysteries): procedures live in the entries.
- F76 / C41: the workaround command is in `docs/agent/bugs/F76.md`.
- C56 to C61 (food seams): each entry carries a TAKEABLE line.
- Both-packs stacked leg: information only, never a release gate (your ruling 08-19); after 53 pared
  the compatibility surface it may be vacuous. Take it only if you want the number.
