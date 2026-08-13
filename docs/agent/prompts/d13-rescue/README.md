# Chain — d13-rescue (the save-rescue artifact + the disposition table; 5 prompts, self-consuming)

**Why this chain exists.** D13 is a HARD LAUNCH DEPENDENCY (owner, 2026-08-01:
*"the pack does not ship until this ships alongside it"* — "we won't launch
till it does"). Its spec gate is OPEN: F86 Tiers 1+2 landed and verified, and
the opt-in split closed 2026-08-12 with both post-split trees audit-sustained —
so the residual set the cleaner targets is finally the FINAL one. Owner
sequencing rule (checklist 15): D13's exposed-set derivation must see the
final module sets of BOTH mods, which now exist.

Three deliverables, each first-class (`agent/bugs/D13.md` is the requirement
record — read it WHOLE in every prompt):

1. **The authoritative exposed-set derivation over BOTH shipped trees** —
   `C:\Dev\SMR-BugFixPack\Code\` (75 files) and `C:\Dev\SMR-OptInPack\Code\`
   (9 files). ⛔ **NO INHERITED COUNT** (owner, 2026-08-01): every recorded
   number ("≥13", "12 exposed") is an open lower bound from a grep proven
   blind to slot/global/preset assignments, and the builds have changed the
   set since. If this chain's derivation disagrees with a recorded count, the
   record is wrong. The derivation then **corrects every doc that states a
   count** (the entry's location table is a 2026-08-01 starting point with
   PRE-restructure paths — re-sweep, translate, never trust it as complete).
2. **The complete per-site disposition table** (FIX_POLICY §3a release gate):
   every exposed site gets its own recorded call — repaired-in-pack /
   inert-accepted / cleaner-target / **KEEP (the residue IS the repair)** —
   with the reason. A site with no disposition blocks release by default.
3. **The standalone save-rescue artifact**, built against the table's
   cleaner-target column and verified in game. Plus the player-facing
   uninstall procedure text (drafted, frozen for MOD_DESCRIPTION at prep).

## Binding chain rules

1. **Staleness check first, every prompt**: `git log --oneline -10` +
   `git pull` in THIS repo; same in `C:\Dev\SMR-OptInPack` and the TestKit;
   this chain was authored at fix-pack `ada5cbb` / opt-pack `a90d128` /
   TestKit `62f03da`. A live todo list, one item per commit-and-verify unit,
   updated per item — the owner reads it to decide when to step in.
2. **Inbox/outbox in writing**; each prompt appends to the next prompt's
   `## Notes from upstream`, commits, deletes its own file in the same
   commit. Folder emptiness is prompt 5's done-condition. Deliverables that
   outlive the chain land in PERMANENT homes (`agent/reports/`, the artifact
   repo, entries) — never only here.
3. **Recorded facts are claims** — including everything in this README, the
   D13 entry's tables, and every number in the F86 reports. Re-derive the
   ROUTE from Src/code, not just the citations (the project has been wrong
   about a route twice while every cited line was right).
4. **Self-split at a clean commit boundary** if context runs short. Route,
   don't drop; unsure who owns a discovery (fix pack vs opt pack vs artifact
   vs TestKit) → STOP AND ASK.
5. **WORKFLOW binds in full** — probe hygiene (parked `.txt` instruments, ARM
   gate, `PROBE SWEEP:` line, R8 `git add -f` for archived logs), EF-047
   (absence only from archived logs) · EF-048 (truthiness/type) · EF-049
   (save witness = disk bytes + load-back) · EF-050 (savename VERBATIM) ·
   ⚠️ **EF-051 HOLD** (Steam Cloud ON: "deleted, listing verified", NEVER
   "gone") · ⭐ **EF-055** (a junction pull is a REAL uninstall, agent-side,
   account untouched — this chain's uninstall primitive) · ⛔ **EF-056**
   (loading a COPY of a real campaign still runs its autosave: byte-copy
   EVERY autosave by name before any launch that loads one). PS 5.1 hazards
   (no-BOM UTF-8 via Edit tool / `[System.IO.File]`; commits via
   `git commit -F <file>`); parse sweep before any commit touching Lua;
   doccheck GREEN in EVERY repo it exists in before any doc commit; push
   what has a remote. ⭐ The rig's NORMAL config is BOTH mods loaded
   (baseline `74/74` + `8/8` · `78/0/10/0` of 88, SKIPs by name in STATE);
   ⚠️ cheats enabled — name it beside any "retail" claim.
6. **⛔⛔ THE DERIVATION INVARIANTS (this chain's constitution):**
   * **(a) No inherited count, anywhere.** The enumeration runs from the
     shipped `Code/` of BOTH mods, over ALL FIVE SHAPES (class-method wrap /
     table-slot / global assignment / preset-field / own-thread — the
     WORKFLOW release-gate list) UNION FIX_POLICY §3a's three capture routes
     ((a) blocked game-time-thread frames, (b) captured locals/upvalues of
     ANY frame, (c) persisted state: object fields, GameVar contents,
     notification closures). `tools/blocking_analysis.py` is an INSTRUMENT,
     never an oracle — static sweeps over-claim (corun-batch-1 rule 6:
     only per-candidate source reading may file). Every table row carries
     its own provenance tag (MEASURED / SOURCE / INFERRED); a blanket claim
     over the table is banned (R3).
   * **(b) Curated lists, never pattern-guess.** The 2026-07-31 `rawget`
     sweep false-positived on 192 buildings TWICE. The cleaner detects by
     enumerated name/site list only.
   * **(c) ⛔⛔ SOME RESIDUE IS THE REPAIR.** `90_SaveSanitizer`'s
     `SMRFixPack_F35_<label>` modifiers repair the save; a delete-everything
     cleaner re-breaks it. Every REMOVE entry carries why-safe; every KEEP
     entry carries why-kept; a name on neither list is a derivation gap, not
     a judgment call. Persisted names are SAVE CONTRACT in both packs — the
     cleaner may REMOVE per list, never rename, never rewrite.
   * **(d) The artifact is residue-zero BY CONSTRUCTION**: purely
     synchronous, no threads, no GameVars, no persisted names of its own, no
     `optional` machinery. Thread restarts are ONE-SHOT and bounded
     (restarting `Meteors` resets a 35–115 h interval — trap 2), never
     blanket-repeated. It states which pack versions' residue it handles.
   * **(e) THE FOUR OFF-STATES DOCTRINE binds every reading** (D13 entry,
     measured 2026-08-10): (1) per-module toggle off · (2) Mod-Manager
     disable without restart — permanent GONE, code LIVE · (3) disable +
     full restart · (4) real uninstall. Every uninstall-flavored claim
     carries its `pack=n/n` gate line BESIDE it; `Unpersist missing
     permanent` is NOT diagnostic (it fires in state 2). EF-055's junction
     pull produces state (4) unattended and is the preferred primitive.
   * **(f) BUILD FIRST, DISPOSITION AFTER (FIX_POLICY §3a, owner verbatim).**
     A newly derived site with an apparently reachable in-pack repair may
     NOT be dispositioned to the cleaner in advance — the discovering prompt
     STOPS on that site, routes it to the owner with the in-pack repair
     recommended and costed (offering an inserted build prompt before the
     terminal audit, per the escalation convention). The cleaner hand-off is
     valid only after the in-pack attempt is made or the route proven absent.
7. **Owner decisions routed, nothing else blocked on them — but prompt 3 IS
   gated on the answers:** prompt 1 packages the two reserved questions on
   the checklist ("Decisions waiting on you"), each with a recommendation
   and costs: **Q-A, the player story** (run-after-removal / keep-installed /
   pack-is-own-cleaner + artifact-for-the-already-removed) — deliberately
   reserved by the owner, asked NOW because the spec gate is open; **Q-B,
   the channel shape** — prompt 1 verifies the dissolving argument (an
   artifact built AS A MOD is channel-independent: Paradox Mods reaches
   Xbox/PS5 where no console exists, so only a mod-shaped cleaner reaches
   console players at all) and asks the owner to confirm rather than decide
   from scratch. ⛔ Prompt 3 checks both answers at its staleness check and
   **STOPS if either is missing** — it reports, and the chain resumes when
   the owner answers. Prompts 1–2 run without them.
8. **Evidence rules:** R2 execution markers on every console line; R4
   round-trip on every state-transition claim; R7 effect-not-execution on
   every verdict; R8 log archiving in the SAME commit as the claim it backs
   (owner-produced logs included — the split audit's lesson).
9. **Model placement:** prompts 1/3/4 = Opus executes; prompts 2/5 = Fable
   (fresh-context QA gate; terminal audit). Bodies are model-neutral
   (placement lives in filenames only). 5-prompt chain: the owner may
   reassign placement at will (CHAIN_METHOD §4.0).

## Scope fence — the whole chain

**In:** the exposed-set derivation over both shipped trees; the complete
per-site disposition table; correcting every doc that states a count or
denominator; the two owner questions packaged and answered; the artifact's
spec, repo scaffolding, build, and TestKit probes; the unattended
verification matrix (junction-pull configs, damaged-fixture legs, artifact
self-cleanliness); the player-facing uninstall-procedure DRAFT; records in
all repos it touches.
**Out:** ANY behaviour change to either shipped pack (a reachable in-pack
repair found by the derivation ROUTES per rule 6f — it is not built silently
mid-chain); renaming ANY persisted string; publishing/remotes/portal work
(release checklist owns it); MOD_DESCRIPTION's rebuild (step ③, after this
chain); the ATTENDED after-sweep and PT-20 redo (they ride the owner's ONE
combined sitting — prompt 5 preps and routes, never runs them);
`unattended-3`'s content; the F102 minute.

## Stop conditions (chain-wide)

- The derivation meets a persistence shape the taxonomy cannot classify →
  record it verbatim with its site, STOP that job, route.
- Prompt 2's verdict is not BUILD → back to prompt 1's owner; prompt 3 may
  not run on an unsustained derivation.
- Prompt 3 finds either owner answer missing → STOP and report (rule 7).
- Any verification leg shows the artifact violating its own residue-zero
  bar, a KEEP-list name missing after a clean, or a REMOVE-list name
  surviving → stop that leg, record verbatim, keep independent legs, route.
- Any `[LUA ERROR]` naming the artifact or either pack → stop that leg,
  record, route.
- Context runs short → self-split at a clean commit boundary (rule 4).

## Manifest

| # | file | owner needed? | what it does |
|---|------|---------------|--------------|
| 1 | `01_OPUS_DERIVE.md` | No — game closed (routes 2 questions) | authoritative five-shape derivation over BOTH trees · reconciliation vs every historical count · curated KEEP/REMOVE draft · disposition-table draft · artifact design sketch + repo proposal · Q-A/Q-B packaged to the checklist. Outbox = prompt 2's Notes |
| 2 | `02_FABLE_QA.md` | No | fresh-context ADVERSARIAL re-derivation of the set, the keep-list and the traps; verdict gates the build |
| 3 | `03_OPUS_BUILD.md` | ⛔ gated on Q-A/Q-B answers (game closed) | freeze spec → scaffold artifact repo → build cleaner + TestKit probes → correct every count-stating doc → doccheck GREEN everywhere; NO launch |
| 4 | `04_OPUS_VERIFY.md` | No at keyboard (game/Steam must be free) | unattended matrix: junction-pull configs, damaged-fixture clean, keep/remove verification, artifact-removed load-back, restore control; logs archived |
| 5 | `05_FABLE_AUDIT.md` | No (routes decisions) | byte-compare + whole-log read · re-derive every verdict AND the set membership once more · doc-sweep audit · ledger · integrate · folder EMPTY · kickoff = the combined sitting |
