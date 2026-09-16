# Applying the STATE admission tests

Owner-directed follow-up to [the admission audit](STATE_ADMISSION_AUDIT.md),
under `zz-owner/09_STATE_DOOR.md`. Baseline:
`19c695473474faafec194b55553646e60496a7d9`. The working tree was clean and
`python tools/doccheck.py` was GREEN. The complete admission and volatility
rulings in `.claude/DECISIONS.md` were read before changes.

This applies the owner's tests by hand. It does not install a new procedure or
machine check. A duplicate pointer can leave without retiring the ruling at
its destination. Uncertain or unique authority is not silently discarded.

## Measurements and changed judgments

Command: `python -` reading `git show 19c6954:docs/agent/STATE.md`, normalizing
CRLF to LF, slicing at `^#{1,3} ` after asserting no `### ` heading, and taking
the encoded byte length of each slice. Physical lines use `splitlines()`.

| Baseline slice | Lines | LF bytes |
|---|---|---:|
| Title | 1–2 | 87 |
| Header/navigation | 3–11 | 548 |
| Now | 12–93 | 8,885 |
| Hazard pointers | 94–100 | 586 |
| Governing pointers | 101–114 | 888 |
| Open decisions | 115–119 | 377 |
| Build state | 120–128 | 368 |
| Total | 1–128 | 11,739 |

Now occupies 75.7%. These measurements agree with the follow-up brief.

**27 of my 33 prior table dispositions are overturned.** Filter: the first
column of the leg-08 report's “Disposition of the header and Now” table;
count a row once when its formerly retained content is now refused and routed.
Members, using that report's original line ranges: 8, 9–10, 15–16, 17–22, 23,
26–27, 28–30, 31–33, 34–38, 39–42, 43–45, 46–47, 48–51, 52–58, 59–63,
64–65, 66–67, 68–72, 73–74, 75–83, 84–85, 86, 88–89, 90, 91–92, 93, 94.
The other six rows reconcile the total: 1–7 and 13–14 are structure; 11–12
were already cut; 24–25 retain the version pair in the owner's new wording;
87 is the protected generator dependency; 95 is a separator. The later
peer deletion of the decisions commentary is not counted as my work.

The probe-name verification also corrected an inherited measurement. Filter:
backtick-delimited identifiers matching `[A-Z][A-Za-z0-9]+` in STATE's
probe-maintenance paragraph, then exact-string membership in
`CK144A_CLOSEOUT_SITTING.md`. **10 of 10**, not eight: C47OpenFarmSeedBufferShape,
LanderCargoRatchet, DroneUnreachableForever, AutoExportPriority, LayoutTechLock,
AnomalyCaveInMap, DomeFreeSpaceMismatch, ClassicRockets, CohortHousing, NoHomeless.
The destination's “RunAll, by name” section contains all of them. Its preceding
table says `counts={ERROR:6,FAIL:4,PASS:69,SKIP:18}`. The source and destination
membership totals agree; no probe or task is silently dropped.

## Per-line decision and destination

Numbers below refer to the new baseline, not leg 08. All physical lines are
covered once. Tests are applied together: H names the potential victim (or
states that the harm is only a lookup); R gives job/knowledge audience; G
identifies an existing gate or says none; V says whether the described status
can change. A rejected reach or volatility result cannot be rescued by harm.
Headings, blanks and the required local header are structural scaffolding,
not admissions for the paragraphs that used to follow them.

“Existing” means the destination passage was opened and checked. “New passage”
means it must land in the same commit as the cut. “Protected” is an explicit
scope exception, not a claim that the paragraph passes the door.

| Lines | H: victim / R: job and audience / G / V | Decision and verified destination |
|---|---|---|
| 1–7 | Structural title, pull notice, local header | Keep the notice and header. They define the file, not a work queue. |
| 8 | Lookup only / STATE maintainer / doccheck size gate / settled procedure | Cut locator. Existing: STATE_EVICTION §Formatting says “if content doesn't fit, evict, don't compress”; prompts map has its task row. No procedure changed. |
| 9–10 | Historical lookup only / historian / git / settled | Cut grave navigation. Existing: SESSION_LOG is the history home; the prior states remain `git show 541e626:docs/agent/STATE.md`, `1aafdbf:...`, `3ef6fcb:...`. This report records the audit's own baseline above. |
| 11–12 | Structure | Keep a separator and Now heading. |
| 13–14 | Players if wrong release is prepared / release role / outbox+preflight / mutable release, settled receipt | Refuse reach. Existing release outbox “Released in v10” says “both portals ran” and records version 11, pdx_version 9 and Forty-nine. New passage: V10_RELEASE_RECORD, preserving the exact historical release receipt and portal IDs together. |
| 15–20 | Release reader could trust wrong artifact count / packaging role / FLPK SELFTEST / settled artifact, mutable next prediction | Refuse reach and historical content. Existing DOC_OVERHAUL_AUDIT §1: “371,327 bytes; md5 bef42a2d5405e06444b7e6efdf28cf38” and “extra ‘two entries’ are a reader defect.” New V10_RELEASE_RECORD passage preserves the repaired-reader qualification, next-pack exclusions and unread PDX size. |
| 21 | Owner's upload can fail / release role / upload_preflight / settled route | Cut. Existing UPLOAD_WORKFLOW §1: “Main menu → MOD EDITOR” then “File → Pack Mod.” |
| 22–23 | Any reader can use the wrong game's evidence / everyone/everyone / fingerprint command / current+previous can change | Admit only the owner's two-line version shape. EF-075 holds the dated update and “never renumber their citations in place”; EF-083 holds the archived source path. `--emit-fingerprint` confirms installed build 24995074, matching the 1.1.0 group. |
| 24–25 | Investigator can trust a source prediction or invalid fixture / fact user/playtest role / none / settled observations | Cut as owner decided. Existing EF-078: “Only a runtime read measures these. Ever”; EF-079: “THE WHOLE PLAYTEST SAVE LIBRARY IS BRANCH-LOCKED”; EF-080: “Triage only, NEVER a verdict, NEVER shipped to players.” |
| 26–28 | False play coverage could mislead a fix author / entry and test roles / none / status mutable | Cut duplicated entry summaries. F116: “F116 remains never reproduced/unplaytested”; F117 §Control: “nil ⇒ the branch never fired ⇒ the row is VACUOUS”; F118 retirement passage: repair “was never exercised, in play or at a desk” and “had no probe.” ck184(d) separately preserves the owner's later field-evidence closure; no entry status is promoted. |
| 29–31 | Owner could be asked to repeat discharged work / sitting role / none / settled | Cut as owner decided. Checklist ck184(b/d): “The owed first RunAll then RAN 09-15 under a same-day stamp”; “Nothing from ck144 (a) is owed to anyone.” |
| 32–36 | Tester might trust unhealthy probes / toolkit maintenance role / probe suite / maintenance mutable | Cut as owner decided. CK144A_CLOSEOUT_SITTING “RunAll, by name” holds every name and failure shape; SMRTK_08B_SURFACE findings 5–6 preserve “Cannot be proven pre-existing” and “there is no baseline to diff.” |
| 37–40 | Owner could be billed for declined legs / entry and sitting roles / none / settled ruling with conditional reopening | Cut duplicate, not ruling. C89 attended check: “ship it, and reopen this entry if a field report counters it”; C85: daily arm “not run” and “neither gates anything”; C88: comparison “structurally unavailable, not owed.” |
| 41–43 | Wrong evidence or scope could reach a fix / C90/C91/C92 roles / entry checks / candidate status mutable | Cut. C90: “Fixed; ships unexercised in play” and “Saint and Sinkhole only”; C91 title names the modifier surviving repeal; C92 entry names the hidden unresearched UndergroundExploitation and no award observed. The C92 placement report remains its placement evidence. |
| 44–45 | Unauthorized shipping / C92 build/release roles / owner hold / can change only by owner | Cut duplicate authority. Prompts map C92 row: “build + test authorised, shipping held until they lift it in words”; “Decision 171 stays the owner's.” Checklist 172/171 and the build brief remain unchanged. |
| 46–49 | False attribution or unsupported stand-down / C93 triage and D14 audit roles / bodycheck has stated blind spot / unresolved | Cut. C93 §Control: “Needed: the reporter's log and their mod list” and “if the owner chooses to ask”; D14's measured table records 21 nondelegating bodies of 45 and §The instrument gap names class c. Prompts map routes STANDDOWN_AUDIT. |
| 50–56 | Unauthorized or vacuous repair / C95/C96 build roles / play controls / mutable hold; facts settled | Cut duplicates. ck185 and C96 say “Don't author the fix yet”; C95 classification says “Ships in the MAIN pack with the judgment-call mark”; C94 retains the retired control. EF-103 holds habitat Community/Dome distinction; EF-104 holds colony-wide draft, teleport and the unexplained observation. No control or owner condition changes. |
| 57–61 | False normal-play claim / C97 triage role / no general gate / candidate mutable, completed audit settled | Cut. C97 opens “nothing here can reach a normal colony” and “not a GameVar”; its last section is “Engine facts worth promoting … if this entry is accepted.” Source-only limits and fact candidates remain there. |
| 62–63 | Vacuous coverage could mislead tester / Saint tester / probe can PASS vacuously / settled evidence | Cut. SESSION_LOG 2026-09-13 eviction passage: heal “fired in play 09-12”; probe “PASSes vacuously with no domed Saint and field reports are the detector.” This preserves the ck130 condition, not just the topic. |
| 64–65 | Release reader could misstate shipped history / release role / outbox / settled | New V10_RELEASE_RECORD history passage. Existing F107 §What this leg still does NOT establish says the field route “has never run”; F104 records “NOT OUR DEFECT AND NOTHING HERE IS OURS TO FIX.” History is not promoted into new coverage. |
| 66–70 | Owner publication could be mistaken for a commit / release/site role / deployment read procedure / historical receipt settled, decision 47 mutable | New V10_RELEASE_RECORD deployment passage holds exact prior receipt. Existing LIVE_SITE_READ: commit “is not public until the owner runs the workflow”; SESSION_LOG holds the two pared files under decision 47. Record them as the prior state, not a live external read. |
| 71–72 | Wrong Linux attribution / FR-1 role / none / resolved field report, release may change | New passage in FR1_LINUX_FINDINGS_2026-09-10 records the owner-resolved GTX 1070 result. Existing LINUX_DISPATCH gives the portal IDs; CLAUDE and prompts map keep the role route. Its stale tally is out of scope, not copied as current truth. |
| 73–81 | Reopening closed toolkit work / self-consuming chain, fails knowledge reach by construction / toolkit gates / closed | New closeout passage in SMRTK_AUDIT links the actual later results and ck184 ruling. Existing audit: “Ship means the owner uses it. The TestKit never uploads”; taint and eligibility limits remain in §§3–4. CK144A_CLOSEOUT_SITTING holds C-1/C-6 witnessed, C-3 refuted and C-5 unwitnessed. FUTURE_IDEAS §5 holds the parked Stamper. |
| 82–84 | Misrouted work / named prompt roles / PROMPT MAP / queue could change but freeze governs | Cut as owner decided. Prompts map rows route STANDDOWN, C92 and DLC; freeze says “until … the owner lifts this in words.” No new next-work order is created. |
| 85 | Owner loses ck151 from register / owner routing / WAITING generator / unresolved | Protected dependency: keep the exact `Owner OWES: ck151 (b) dev-report scope.` line, relocated next to the protected enumeration. |
| 86–87 | Wrong or tainted fixture / toolkit sitting role, chain knowledge / disk evidence / completed sitting | Cut. SMRTK_FULL_SITTING §Fixture names the Sol 490 copy and scalar CheatsUsed against a TABLE positive control; “never the other three byte-identical copies.” Later passage records the actual `SMRTK_490` save. No new fixture selection. |
| 88 | Owner-deferred work could refire / DLC and fixtoggles roles, chain knowledge / PROMPT MAP / held | Cut. Prompts map owns DLC_DEEP_CHECK; fixtoggles README names checklist 148 and its scope. Checklist 148 heading: “DEFERRED … you said skip; the chain is NOT started.” Deferral stays in force. |
| 89–90 | Wrong coverage or forced organic test / named test roles / per-entry controls / mixed | Cut. EF-066: “that half of checklist 74 stays unmeasured”; EF-039: “German alone was watched”; EF-051 retains the stray-save falsifier. C47 holds the unbuilt repair/hold, C48 the opt-in disposition, F02/F78/F81 organic records, C42/F99/F80/F96 the riders. Detailed quotes below; no playtest debt is created or closed. |
| 91–92 | Dormant reports could become unauthorized builds / entry/triage roles / none / parked/open status mutable | Cut. F60 retirement section preserves the ruling and loose ends; F109: “If a second report ever arrives” get the buildings list, mod list and save, and “Do not harden DestroyedRebuild”; C55 holds the pre-sort evidence; checklist 136 holds FR-2/FR-3. |
| 93–94 | Section structure | Remove empty separator/heading with the refused Hazard content. |
| 95 | Wrong module membership / pack/release role / MODULE SETS+upload_preflight / mutable | Cut as owner decided. Existing gates and RELEASE_SURFACES §4 require doccheck and upload_preflight; the tool detects membership/order. |
| 96 | Owner portal action / release role / owner-only rail / settled | Cut as owner decided. release_prompt opening: “The agent never packs, uploads, opens the Mod Editor, or calls a portal API.” UPLOAD_WORKFLOW holds the safe route. |
| 97 | Sweep contamination / sweep chain role, fails knowledge reach / none / historical chain | Cut as owner decided. Archived prelaunch spec §2 describes the blind-sweep problem and its fence; docs/README still says that H-05 fence “remains authoritative.” |
| 98–99 | Owner loses mod enable or measures wrong load / junction/playtest role / in-game verification / settled observations | Cut as owner decided. EF-055: every restoration must “verify the registry in-game before measuring”; its narrowed same-id packed-folder experiment preserves the exception. |
| 100–101 | Section structure | Remove empty Governing heading and separator. |
| 102–105 | Player/save or owner time could be harmed / release, fix and playtest roles / relevant tool gates / settled policies | Cut locators only. release_prompt owns H-04; FIX_POLICY §3a calls save safety a “design discipline”; §4 requires “file:line evidence … reachability tier … positive intent statement”; WORKFLOW's rig section says “BOTH mods enabled.” Their conditions remain untouched. |
| 106 | Owner interruption / communication role / none / settled policy | Cut locator. Existing WORKFLOW 5b: “Never draft one unasked, never put one on the owner's owed list.” No reply rule is authored here. |
| 107 | Misrepresented testing / playtest role / none / settled policy | Cut locator. WORKFLOW testing/release protocol preserves reporting the “SKIP set BY NAME”; this task does not change that protocol. |
| 108–109 | Broken identity or false ordering advice / release/integration role / module-order gate / settled | Cut locators. RELEASE_PORTAL_PREP opening preserves Relaunched Fix Pack display name and unchanged mod id/log tag/repo names. EF-054: visible list is a “COSMETIC sort”; FIX_POLICY §8 keeps the inter-mod/intra-mod distinction. |
| 110–111 | Bad format or branch guard / STATE maintainer and fix author / doccheck/probes / settled policies | Cut locators. STATE_EVICTION formatting remains; FIX_POLICY §2a keeps “the probe IS the guard.” This is not retirement of either rule. |
| 112 | Wrong legacy download / release/support role / release artifact / service may change | Cut. Checklist 169 legacy paragraph: “1.0.7 players keep the frozen v5-game-1.0.7 GitHub build (ck118)”; ck118 records the GitHub release/site tab/card route. |
| 113 | Stale portal body / release role / parity/preflight / settled procedure | Cut locator. RELEASE_SURFACES §3 lists card, metadata and UPLOAD_WORKFLOW backups that “must move together”; UPLOAD_WORKFLOW header requires byte matching. |
| 114–119 | Owner obligations / owner-routing role / WAITING generator / unresolved | Protected: leave the complete Open owner decisions section and STILL OPEN continuation unchanged. Retain its separator. |
| 120–127 | Next command can emit counts / build/release roles / mandatory generated-region gate / mutable | Refused by reach, but blocked by an existing gate. Proposed home is `python tools/doccheck.py --emit-counts`; see the concrete conflict below. No generated content is hand-edited. |
| 128 | Wrong historical citation branch / fact readers / fingerprint / settled qualifier | Cut duplicate. EF-075 explicitly distinguishes current installation from EF-014's historical stated version and forbids renumbering old citations. |

### Destination details that a topic match would miss

- F117's entry has the station recipe and the nil-cache falsifier. Its older
  “8/8” summary is not a fresh test claim; later controls have their own dated
  results. Checklist ck184(d), not a status promotion, closes the sitting debt.
- The probe list is instrument maintenance, not another owed sitting.
  CK144A_CLOSEOUT_SITTING says “nothing new regressed and nothing was cleared.”
  SMRTK_08B_SURFACE explicitly preserves the no-prior-baseline limitation.
- C47's `unrun` shorthand is not preserved as a claim about all C47 evidence:
  the entry records attended reproduction and says no fix separable from C48's
  issue is to be built. C48's behavioral remedy “lives in the OPT-IN pack.”
- The organic records in F02/F78/F81 remain dated to their game branch; their
  retirement passages say the original fixes were correct on 1.0.7. No new
  test campaign is inferred from the stale watch shorthand.
- C42 records the attended rider; F99 says “one organic throw reopens this as
  real work immediately”; F80 says its settling procedure moved from the
  checklist and gives “EITHER symptom” as trigger; F96 says “R2 stays owed and
  stays un-chased.” Removing the watch line changes none of those conditions.
- F109's exact reopening evidence remains in the entry, not merely its
  parked status. F60's retirement section separately preserves its loose ends.
- The SMRTK audit predates the later owner ruling. Its original recommendations
  will remain historical; the new dated closeout passage supplies the outcome,
  including the prohibition on refusing work over sweep age.

## Concrete gate conflict, not admission by default

`tools/doccheck.py:state_counts_bytes` raises `StateCountsError` unless STATE
contains exactly one `BUILD STATE (emitted by tools/doccheck.py)` marker.
`check_state_counts` treats that error as RED. The count block has a pull-only
home in the tool's `--emit-counts` output, but deleting it while retaining the
existing gate cannot pass the required check.

Proposed resolution for the owner: remove the mandatory STATE copy and its
requirement, preserving count derivation and the underlying membership checks.
That changes an existing machine obligation; this sweep does not silently
retire it. The block is recorded as refused/blocked, not as passing the door
and not as homeless. The owner-register source is a different, expressly
protected exception: the parser still needs ck53, ck133 and ck151.

## Execution and verification

Audit and destination review committed as `f5302ce`, with STATE unchanged.
The existing-home cut removes the verified duplicates in the table, including
the entire Hazard and Governing pointer sections, and rewrites the version
pair. The exact owner-debt sentence now sits beside the protected enumeration.
The release, site, FR-1 and toolkit blocks await their new destination passages.

At `f5302ce` plus that STATE patch, normalized STATE measures 4,038 B (command:
`len(Path('docs/agent/STATE.md').read_bytes().replace(b'\r\n', b'\n'))`).
This intermediate size is attribution only. doccheck is GREEN, WAITING is
byte-identical to `19c6954`, and its decision members remain exactly
53, 133, 151, 169, 171, 172, 173, 175, 178, 180, 181, 182, 183, 184, 185, 186.
The STATE parser still yields 47, 53, 133, 151, 152. Command/filter: import
`tools/doccheck.py`, call `state_owed_numbers()`, and select `classify_items`
rows where `status in MARKER_STATUSES` and `owner`, just as `render_waiting`
does. The enumerated sets reconcile to five parser IDs and sixteen rows.

The generated-block conflict was also falsified in memory before any cut:
remove its heading/fenced region from baseline input, call
`state_counts_bytes(candidate, {})`, and require the exact error
`expected exactly one BUILD STATE first line, found 0`. It fired. No file was
modified by that experiment; the intact block remains unchanged.

Verification plan: compare complete WAITING bytes and parsed owner-ID sets to
the baseline, preserve the exact STILL OPEN block, verify the version pair,
check every removed interval against the matrix, run doccheck and review the
diff for unique conditions. No new game, site or portal observation is claimed.

Departures: correct the probe membership from eight to ten; the baseline hazard
paths are already updated, though the content still fails the owner's test.
The checklist body and prompts remain out of scope. Missing later outcomes
are homed in task-specific reports, not a general intake or replacement STATE.

Suggestions: settle the mandatory generated-copy conflict separately; update
the stale FR-1 field tally in LINUX_DISPATCH/checklist 145 when those surfaces
are authorized. Installing the admission door in STATE_EVICTION or tooling
remains unadopted. Executed model: GPT-6, as exposed in this transcript.
