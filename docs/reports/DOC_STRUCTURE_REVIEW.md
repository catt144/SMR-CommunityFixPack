# Documentation Structure Review — recommendations only (chain prompt 12, job 7, 2026-08-03)

**Commissioned by the owner 2026-08-01 after one session surfaced four drift
instances; the chain then deliberately accumulated a corpus (chain rule 4b)
through prompts 7–12. This review diagnoses structural causes and recommends —
it restructures nothing. The owner picks what happens.** Recommendations that
would change how prompts/sessions are authored are flagged **[WORKFLOW]**, since
they touch `WORKFLOW.md` and the chain conventions.

The corpus: the seed list in the job-7 notes (prompts 4b–11), the blind audit's
two structural observations (ANNEX §3), and this QA's own findings (the F29/F57
banners, the D12 tag, C40's frozen note, F68's lead paragraph, F97's silent
wave exclusion, the rotated logs). Roughly forty recorded instances.

---

## 1 · The document inventory (who writes it, who must update it, how staleness shows)

| doc | written by | must update, when | duplicates | how a session learns it is stale |
|---|---|---|---|---|
| `BUGS.md` | every session | any status/evidence change — **row AND tag** | statuses ×2 (row/tag); mechanisms restated in module headers, STATUS, prompts | nothing mechanical; the row↔tag protocol exists *because* nothing does |
| `STATUS.md` | any session changing counts/state (chain rule 7) | same session | counts (re-derivable from `Code/`/TestKit); narrative restates BUGS | counts went stale within their own day twice; only re-derivation catches it |
| `PLAYTEST_CHECKLIST.md` | build sessions add, owner fills results | on run/retire/absorb | predictions restate entry mechanisms | retired tests found referenced; caught by hand |
| `PLAYTEST_ARCHIVE.md` | on completion | never (append-only record) | results restated in BUGS tags | archived toggle-method "uninstall" survived 3 days past the doctrine |
| `MOD_DESCRIPTION.md` | fix sessions | when player-facing behavior changes | claims restate entries | the expired-gate note (F86) and the F76 draft note both went wrong *as instructions* |
| `agent/FIX_POLICY.md` | policy decisions only | rare | cites ENGINE_FACTS | stable — least-bitten doc in the corpus |
| `agent/ENGINE_FACTS.md` | any session proving an engine fact | on correction | none (it IS the single source) | **corrects itself in place and its corrections also go stale** (blind audit §11.3: a warning outlived its subject within a day) |
| `PLAYTEST_HELP.md` | procedure discoveries | on procedure change | recipes restate TestKit reality | the "67 default fixes" count was stale; found by audit |
| standing prompts (`FABLE_NEXT_PROMPT.md`, `DRONE_PROJECT_PROMPT.md`) | chain/owner | whenever referenced state moves | restate BUGS/STATUS heavily | the standing lesson: goes stale whenever playtest commits land after its last edit |
| chain `README.md` (ending) | chain author | each prompt close | chain state ×(rows + prompt bodies) | row 8b2 stayed un-struck; "the index the chain uses is the doc no prompt owns" |
| `reports/*` | one-off sessions | never (records) | conclusions restated forward | §5.4's "verified feasible" column asserted verification a row didn't have |
| module headers (`Code/`) | fix sessions | when behavior/rationale changes | summarize entries; advertise properties | a header asserted a withdrawn reason for 8 days; F94's property was in 4 places |

Two observations fall straight out of the table: **the only documents that never
bit anyone are the ones with a single writer and no duplication**
(FIX_POLICY, the report set as records), and **every recurring protocol the
project has added ("update both places", "re-derive counts", "re-read the entry
before acting on the brief") is compensation for duplication or provenance
blindness rather than a fix for it.**

## 2 · The failure taxonomy (by structural cause, not incident)

**T1 — Hand-synced duplication.** The same fact lives in N places and a human
must remember every copy. Instances: row↔tag (≥6: F18, F86 ×2, F42, D12 today);
counts in STATUS vs per-module tables (the `12` denominators, the 79/74
unwritten-exception line); dangling pointers to self-consumed files (×4);
prompt briefs vs entries (C33); module summary vs its own corrected body
(DroneTransportMinors, **F68's lead paragraph vs its own forensics — found
again today**); F94's property in 4 places; the F29/F57 banners vs the ✅
blocks below them (today); C40's note freezing a superseded design (today).
*The seed hypothesis is confirmed for this class — and it is only one class.*

**T2 — Provenance blindness.** A measured fact, an inherited fact, a
derivation, and a guess are written in the same voice, so downstream sessions
cannot weight them. Instances: the C33 "raises" claim; F82's inert-flag
inference; the Saint "R2-ish?" guess hardening; §5.4's blanket "verified
feasible" laundering six rows to the standard of the best one; **hedges not
surviving quotation** (F76's "Suspected" → four documents assert it); the
**route-above-citations** family (three in one week: a route recorded feasible
that did not exist, a route recorded impossible that did, a false citation
under a true conclusion — plus its mirror). The blind audit's closing
observation is the same fact from outside: *evidence tier tracks argument
type* — and our docs do not record the tier.

**T3 — Claims only a state transition can falsify.** Idempotence of load-time
heals, migrations, latches — invisible to source review, code review, and
same-session probes; falsifiable only by a human loading twice. Two-for-two
defective on the heals actually round-tripped; the rest have never been.

**T4 — Cross-artifact collisions.** Two artifacts each correct in isolation
sharing a field, a seam, or an ordering: the probe's `forbidden` scaffolding vs
8c's real guard; D12's wrapper vs D07's probe stand-ins; `TitleRight` vs
`Init`'s ordering; the push/accept asymmetry. Not findable by reading either
side; only a suite run or a leg catches them.

**T5 — Ran-vs-worked indistinguishable.** F98/F25: `fixed` was true (code
written, assignment performed, verdict "patched") and the fix had never worked
in retail. No surface distinguishes "this executed" from "this had its
effect".

**T6 — Written-but-never-executed instructions that look like answers.** The
`rawget(_G, ...)` console gate that cannot run in the sandbox (its failure
would have *looked like an answer*); the silently-dead A/B lever
(`SMRFixPack_Disabled.NoHomeless`); the F97 probe asserting an input the
engine cannot produce. A snippet that has only been written is a different
artifact from one that has been run, and today they are indistinguishable.

**T7 — Routing without preconditions.** Items routed to *prompts* when they
needed a *situation*: `DustDevilSpawnGate`'s suite-run debt (3 hops), C40's
enacted-law need (3 hops), prompt 11's owner-dependency. Each forward looked
like diligence.

**T8 — Append-only decay + evidence rotation.** ENGINE_FACTS' corrections
churn (a correction went stale in a day); and — new this session — **the
primary logs behind the founding measurements rotated off disk** (~20-file
cap), so "go to the primary evidence" now bottoms out at transcriptions.

**One anti-instance, kept so the corpus doesn't over-count** (prompt 10's
point): a session *deliberately amending* a spec it was authorized to amend,
with the departure recorded in the same commit, is the process working — the
tell that separates amendment from drift is exactly that contemporaneous
record.

## 3 · Recommendations, cheapest-highest-value first

**R1 — A mechanical `bugsync` check (T1's worst pair).** ~50 lines of Python:
parse BUGS.md, compare every index row's status word against its heading tag,
plus recount rows/files/probes and diff against STATUS's stated counts; run it
before any commit that touches BUGS/STATUS (this QA effectively ran it by hand
and it caught the D12 tag). *Worth it unambiguously* — the class has bitten
more than any other and the check costs one script forever. **[WORKFLOW]** one
line: "run `tools/bugsync.py` before committing a status flip".

**R2 — Execution markers on console snippets and A/B levers (T6).** Convention:
any console line or lever in a doc carries `[RAN <date>, log <name>]` or
`[NEVER RUN]`. Free at write time; the PT-61 near-miss (a gate that would have
parked the whole sitting's subject) is the bite it prevents. **[WORKFLOW]**

**R3 — Provenance tags on load-bearing claims (T2).** Adopt the discovery
position paper's own vocabulary — **MEASURED / SOURCE / INFERRED / INHERITED /
GUESS** — as a required prefix on load-bearing claims in entries, specs, and
briefs; and require the *route* sentence ("therefore the only way is…") to be
tagged separately from its citations. The corpus shows citation-checking
missed both route failures; a tagged INFERRED on the route sentence is what
would have invited the re-derivation. Costs writing discipline only; the F76
hedge-laundering and §5.4's blanket header are exactly what it prevents. Also:
**a blanket verification claim over a table is banned — the tag goes per
row.** **[WORKFLOW]**

**R4 — The round-trip step for state-transition claims (T3).** Standing
playtest rule: any load-time heal, migration, or latch that ships gets one
save→load→load reading of its number before its entry may say more than
`fixed`. The campaign already owes one sweep of the untested backlog (QA
report §9.2). Cheap per instance (minutes at the keyboard); the class is 2-for-2
when actually tested. **[WORKFLOW]**

**R5 — Routed items carry a TAKEABLE-WHEN line (T7).** Routing writes down the
owner prompt; it should also write the precondition ("needs: a suite run", "a
colony with the law enacted", "the owner at the keyboard"). Items whose
precondition is a *situation* go to the checklist as riders immediately —
which is where both three-hop items eventually landed anyway. One line per
route; prevents the diligence-shaped forwarding loop. **[WORKFLOW]**

**R6 — Generate the BUGS index from the heading tags (T1, structural half).**
The row↔tag pair stops being hand-synced when one side is derived: keep the
tags as the source of truth, generate the index table by script (R1's parser
is 80% of it). Medium cost (one session), permanently deletes the
most-protocolized duplication in the project. Do R1 first; promote to R6 when
the script has earned trust.

**R7 — "Effect-evidencing" verdicts for non-self-evidencing fixes (T5).** Rule
of thumb: a module's verdict function should test the *effect* where one is
readable (F98's `type(T(...))` control was one console line); where none is
readable in-session, the entry says so and the fix stays behind a live reading.
Don't add a new status — the existing `fixed`/`tested` split is right; the gap
was that nobody asked what `fixed` was resting on for a text change. Modest
cost, applies to few modules.

**R8 — Archive load-bearing logs (T8).** When a leg's numbers will be cited by
a status flip, copy the log file into `docs/logs/` (or a sibling folder) in
the same commit. The rotation cap is ~20 files and it has already eaten the
founding measurements. Nearly free going forward; cannot be applied
retroactively — which is the argument for starting now.

**R9 — ENGINE_FACTS review cadence (T8).** The blind audit's diagnosis is
adopted: the doc has outgrown append-only. Cheapest workable form: each entry
gets a `[verified <date>]` stamp when re-confirmed, and any session that
*uses* an entry re-stamps it; a periodic pass (release prep is the natural
moment) reviews the oldest stamps. Skip the full restructure — the doc's
content is good; only its freshness signal is missing.

**Live with it (honest column):** prompt-brief staleness against entries (the
re-read-the-entry rule already exists and briefs are consumed — T1's cheapest
instances die with the chain format); the chain README (the chain is over; if
another chain runs, give the README an owner the way prompts own their
successors); T4 collisions (no convention prevents them — the suite is the
instrument, and the one rule worth writing down is the one prompt 10 already
extracted: **every wrapper must be inert for a foreign object before it
touches one**, which belongs in FIX_POLICY §2 as a hardening rule
**[WORKFLOW]**); module-header restatement (R3's tags + the existing
same-commit discipline are enough — a header ban would cost more than it
buys).

## 4 · What this does NOT recommend

No doc splits, no doc merges, no new documents, no retirement of existing ones
— the inventory shows the bitten docs are bitten for reasons (duplication,
provenance, freshness) that the targeted mechanisms above address without
moving content. The one structural change worth real consideration is R6, and
it should be earned via R1 rather than adopted on faith.

---

## 5 · Addendum (2026-08-03, same session) — the audience map, and what it changes

The owner supplied the actual readership per document: **human-used** =
`PLAYTEST_CHECKLIST.md` (heaviest), `PLAYTEST_HELP.md`; **historical reference
only** = `PLAYTEST_ARCHIVE.md`; **launch-time, not used for work today** =
`MOD_DESCRIPTION.md`, the public-facing README; **agent-only** = `STATUS.md`,
`BUGS.md` (near-only — consulted by the owner just when an agent explains
poorly), `FIX_POLICY.md`, `ENGINE_FACTS.md`, the `reports/` set (agent-tasked,
agent-read), the `prompts/` folder (owner-invoked, agent-executed).

That map changes four things and leaves the rest standing:

**A — NEW, and the biggest delta: owner decisions must surface where the owner
actually reads.** Several "ask the owner" items have historically lived in
BUGS entries and report sections (`BUG_LIST_AUDIT.md` §7.1's web-checks are
the worked example — they "kept surviving prompts" partly because their home
was a document the owner does not read). Under the audience map that is a
structural mis-routing, not owner inattention. **Recommendation R10: a short
"Decisions waiting on you" section at the top of `PLAYTEST_CHECKLIST.md`** —
the owner's heaviest document — which agents must mirror every owner-decision
item into (one line + pointer) and strike when decided. No new document; one
section; **[WORKFLOW]** one authoring rule ("an owner decision recorded only
in BUGS/reports is not considered asked"). Today's pending entries would be:
the mod-page relabel package, the D03/D07 dead-veto choice, the F46 group
C→B adoption, the C36-adjacent mysteries grep, and this review itself.

**B — `MOD_DESCRIPTION.md`: stop maintaining it continuously; rebuild it at
launch prep.** Its whole drift class (the expired F86 gate note, the voided
F76 note — instructions that went wrong *as instructions*) exists because a
launch-time document is being hand-synced through development it does not
serve. **Recommendation R11: freeze it under a top banner ("NOT AUTHORITATIVE
during development — every claim must be re-verified against BUGS at launch
prep"), move any decision content it uniquely holds into the relevant entries,
and make "rebuild MOD_DESCRIPTION from entries" an explicit release-gate item**
(where the §3 relabel package lands anyway). This *deletes* a duplication
surface for the whole development period at zero ongoing cost. The public
README gets the same treatment at lower priority.

**C — release BUGS/STATUS from human-readability duty; push harder on machine
structure.** The owner confirms BUGS is not written for humans and that is
acceptable — agents translate on demand. So the one objection to aggressive
structure (tag clutter, generated tables reading poorly) is void. **R6
(generate the index from the heading tags) upgrades from "earn it via R1" to
"do it when convenient"** — R1's parser is still the first step, but there is
no audience reason left to keep the hand-synced pair. R3's provenance tags
likewise cost nothing socially in agent-only documents.

**D — R2 (execution markers) is re-ranked as a human-safety feature and moves
to the top with R1.** The written-but-never-run class is most dangerous
precisely in the two documents the owner acts on at the keyboard without the
re-derivation discipline agents are bound to (the PT-61 sandboxed console gate
sat in the checklist; the dead A/B lever was a checklist instruction). The
limited "write for humans" budget this project has should be concentrated on
`PLAYTEST_CHECKLIST.md` and `PLAYTEST_HELP.md` — markers, plain-language
"what a pass means" lines, and the uptime convention — and nowhere else.

Unchanged by the map: R4 (round-trip step — a keyboard fact, audience-neutral),
R5 (routing preconditions), R7 (effect-evidencing verdicts), R8 (log
archiving), R9 (ENGINE_FACTS cadence), and the live-with-it column.
**Revised order: R1 + R2 first, then R10 and R11 (both one-sitting, both
delete a failure surface outright), then R3/R4/R5, then R6, then R7/R8/R9.**

---

*Recommendations only — the owner decides. Items marked [WORKFLOW] change how
sessions are authored and therefore need explicit adoption into `WORKFLOW.md` /
`FIX_POLICY.md` rather than silent practice.*
