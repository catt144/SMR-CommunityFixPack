# fixtoggles — the chain manifest

Effort: give players an **on/off button for every fix** in the Relaunched Fix Pack, a **Beta** label for fixes
shipped before full testing, and **linked buttons** where fixes depend on each other. Authored 2026-09-11 by
`smr-bugfixpack-24` at the owner's ask. Method: `agent/reports/CHAIN_METHOD.md`. Authoring mechanics:
`agent/WORKFLOW.md` "Authoring a prompt" elements 1–8. Evidence base: **`agent/reports/FIXTOGGLES_RESEARCH_2026-09-11.md`**
(read its provenance tags first). Owner decisions: checklist **148**.

> ⚖️ **WHY, in the owner's words:** *"we had over 24 hours of a broken mod that did cause defects and could have caused
> crashes in certain circumstances because some of our fixes are not as safe as we thought."* The F114 reporter could not
> bisect because nothing could be switched off individually (`bugs/F114.md:27-30`). Every prompt is written against that.
>
> ⚖️ **THE SCOPE, in the owner's words:** *"focus on the buttons first, and then we can swing back around to the
> versioning as a B step if we proceed with that."* ⇒ **No link in this chain builds a version selector, a version
> detector, or re-imports 1.0.7 modules.** Link 09 RESEARCHES them for the B decision and builds nothing.
> `FIX_POLICY` §2a stays in force.
>
> ⚖️ **THE BAR:** *"all is preferable"* — every fix switchable. A module may be excluded only with a good reason written
> down and routed to the owner (ck148), never silently.

## The queue

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| 01 | `01_SPEC_fable.md` | Fable | routes decisions | re-validates this cut + placement; re-derives the routes; the framework contract; 45-row disposition; links; Beta model; surface package; §3a for runtime switching; policy text |
| 02 | `02_SKELETON_BUILD_opus.md` | Opus | no | core registry/store/reconciler/gate helper + ONE module converted end to end + the surface stub + desk harness + predictions for 03 |
| 03 | `03_SKELETON_SITTING_owner.md` | any (attended) | ✅ **keyboard (+ a controller if you have one)** | ⛔ KILL GATE: the skeleton in the real game — cold boot + enable path, live toggle, persistence across restart, the surface on mouse and gamepad |
| 04 | `04_CONVERT_WRAPPERS_opus.md` | Opus | no | the 24 wrapper/handler modules (minus the one 02 did): per-call gate |
| 05 | `05_CONVERT_BODIES_opus.md` | Opus | no | the 13 full-body replacements: capture the shipped original, gate to it |
| 06 | `06_CONVERT_STATEFUL_fable.md` | Fable | may route one | the save-state four: SaintBlessing, TrackTunnelPowerBridge (split), ExoticDepositSign (next-load), SaveSanitizer |
| 06b | `06b_CONVERT_DATA_AND_LINKS_opus.md` | Opus | no | the data-undo four (SilentHitMomentFX, DustSicknessBiorobots, SinkholeIndestructible, CrystalMysteryHang) + every linked-button declaration |
| 07 | `07_PANEL_opus.md` | Opus | no | the full surface, our own look, per spec + ck148(a) |
| 08 | `08_TEXT_AND_SURFACES_opus.md` | Opus | no | player titles/descriptions for every row; `items.lua`/`metadata.lua`; store backups; site + FAQ source; TestKit + PLAYTEST_HELP; policy text landed |
| 09 | `09_VERSION_RESEARCH_opus.md` | Opus | routes the B decision | RESEARCH ONLY: version model + 1.0.7 re-import cost → a decision package for the B step |
| 10 | `10_SITTING_PREP_opus.md` | Opus | no | predictions, recipes, fixture re-confirm; writes 11's script |
| 11 | `11_SITTING_owner.md` | any (attended) | ✅ keyboard | the full attended leg: every switch, the risky modules A/B, save/load with switches off, the panel |
| 99 | `99_AUDIT_fable.md` | Fable | ✅ raises | terminal adversarial audit; folder-empty gate; SHIP / SHIP WITH CHANGES / NO SHIP; the kickoff lines |

Model placement: the top tier sits on 01 (the spec — a wrong contract poisons 45 conversions), 06 (save-state code, the
worst failure mode) and 99 (the adversary) — 3 of 13. ⚠️ `CHAIN_METHOD` §4.0 says a chain of 6+ prompts should have its
decomposition and placement done by a top-tier session; this one was cut by an Opus session, so **01's first job is to
re-validate the cut and the placement**, with authority to re-write any unconsumed prompt (ck148(c) asks the owner to
accept that instead of a separate authoring session).

**Owner time:** two attended sittings (03 short, ~30 min; 11 longer, 10 prices it) plus ck148's rulings.

## Ordering

- **01 → 02 → 03, strictly.** 03 is a kill gate: nothing converts until the skeleton is proven in the game.
- **After a 03 PASS:** 04, 05 and 06 are independent of each other (disjoint module files; the core is 02's and frozen
  unless a link routes a change back through the README) — any order, or in parallel by separate sessions.
- **06b after 04, 05 and 06** (its link declarations span modules those three convert).
- **07 after 03**, independent of 04–06b (it renders registry data generically); its final check reads 06b's links.
- **08 after 06b and 07** (it needs the final set, ids, defaults and the surface).
- **09 is independent of everything** — fire it any time, even before 01. It builds nothing.
- **10 after 08; 11 after 10; 99 last, on a folder holding only 99 + this README.**
- **If 03 KILLS:** 99 runs in its pre-written reduced form (post-mortem into `CHAIN_METHOD.md`, the respec/abandon
  decision routed, every unconsumed prompt `git rm`'d with its grave named). A clean abort is the gate working.

## Binding chain rules — every prompt inherits these

1. **Staleness check first.** `git log --oneline -10`, `git pull`, `git status --short`, `ListAgents`. Several sessions
   (Claude and Codex — Codex is invisible to `ListAgents`) edit this tree; message any peer whose lane you enter; never
   touch a stranger's unstaged file; commit by explicit pathspec (`git commit -F <msg> -- <paths>`).
2. **Inbox / outbox.** Read `## Notes from upstream` at the bottom of your prompt first. On close-out append your outbox
   to the NEXT prompt's inbox **and** `99_AUDIT_fable.md`'s, strike your row here, `git rm` your own prompt, and commit
   all of it together.
3. **Route, do not drop.** Out-of-fence findings get FILED (a bug entry, a fact, a checklist item). Unsure? **STOP AND ASK.**
4. **Self-split at a clean commit boundary** into `NNb_*.md` with a full inbox and its own row here. A link cannot see
   its own context budget — split early rather than late.
5. **Capture drift as evidence** — every mistake you catch (yours or upstream's) goes into 99's inbox. A silently
   corrected instance is destroyed evidence.
6. **Re-derive the ROUTE.** The research report's `[R]` rows and the spec are design, not permission to skip the read.
   Open the module and the shipped body before editing against them.
7. **⛔ THE MECHANISM IS THE PER-CALL GATE, NEVER A RESTORE.** An installed hook stays installed; while its fix is off it
   hands the call to the captured original untouched. Never re-assign an original back (`EF-058` subclass copies; the
   `Colonist:Idle` pair). A gate must be inert for a foreign object before touching one (`FIX_POLICY` §2).
8. **⛔ "OFF" IS NOT AN UNINSTALL** (`EF-002`). No code comment, log line, player text or verdict may say a switched-off
   fix leaves the save as vanilla, or that it is "exactly as without this mod". Say the narrower true thing: *its
   behaviour stops; repairs already made stay.*
9. **⛔ NO COPYING THE REFERENCE MOD.** `C:\Dev\_ref\smr-community-fixes` has no licence. Read it for how, never lift
   code, identifiers, layout constants or wording. Never name it (or fredware) on any player surface (`FIX_POLICY` §8).
10. **⛔ NO VERSION WORK outside link 09.** No `LuaRevision` gate, no version dropdown, no 1.0.7 module. `FIX_POLICY` §2a
    and the per-module probes stay exactly as they are.
11. **ONE settings store.** Whatever surface 01/ck148 chooses, exactly one place holds the player's choices, and it
    stores **deviations from the default only**, so a changed default (a Beta promotion) reaches players who never
    touched that switch.
12. **Both enable paths** (`FIX_POLICY` §2 F87): every change is correct on a cold boot AND on the enable-from-menu
    in-place reload. The desk harness exercises both.
13. **Live todo list, one item per commit-and-verify unit**, marked done the moment it is done. The owner reads it.
14. **Green gates before every commit:** `python tools/doccheck.py` GREEN, `python tools/sigcheck.py`,
    `python tools/bodycheck.py`, `python tools/harvest_wrap_targets.py --check`, `python tools/deskbench.py`, and a parse
    sweep of every `.lua` you touched. `git commit -F <file>`; push after every commit.
15. **⛔ `Code/` edits only with `Mars.exe` closed** (`tasklist` first, never in the same command). Never stage a packed
    folder beside a live junction (`H-09`).
16. **⛔ Never move a status you did not witness.** A desk harness is not the game; a source read is never `tested`.
17. **Bindings in force:** `H-02` (no Mod Editor, no `version` edit, no upload), `H-03`, `H-04`, `H-08`, `H-09`,
    `H-10` (every module or option item change updates `items.lua`). Owner decisions go to `docs/PLAYTEST_CHECKLIST.md`
    → "Decisions waiting on you" (append to **148** or take the next free number AT THAT MOMENT), never only here.
18. **A doccheck WARN goes verbatim into your summary.** STATE.md is byte-capped; measure it (`STATE + STUBS` line),
    never quote a stored number, and evict per `prompts/perma/STATE_EVICTION.md` when adding.

## Read path — declared

`docs/agent/STATE.md` (mandatory) · `agent/reports/FIXTOGGLES_RESEARCH_2026-09-11.md` · `agent/reports/FIXTOGGLES_SPEC.md`
(from 02 onward; 01 writes it) · `Code/00_Core.lua` · `agent/FIX_POLICY.md` §2, §3a, §5, §7, §8 · `agent/facts/EF-002.md`,
`EF-004.md`, `EF-058.md` · `docs/PLAYTEST_CHECKLIST.md` item 148 · your own prompt's inbox. Game source: 1.1.0 at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` (read-only); 1.0.7 archive at
`C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`. Working model of the Mod Options route: `C:\Dev\SMR-OptInPack` (`items.lua`,
`metadata.lua`, `Code/00_Core.lua`).
