# fixtoggles 01 — the spec (re-validate the cut, re-derive the routes, write the contract)

You are link 01 of the `fixtoggles` chain. Read `README.md` in this folder first: its binding rules 1–18 are yours.
**Staleness anchor:** the chain was authored on top of `dc31795` plus its own authoring commit; run `git log --oneline -10`
and `git pull`, and read everything that landed since before trusting any line below.

## Job 0 — re-validate the chain itself (CHAIN_METHOD §4.0)

This 13-prompt chain was cut by an Opus session. Before writing the spec, judge the decomposition and the model
placement against `CHAIN_METHOD.md` §2.10 and §4.0 (top tier where errors COMPOUND; ~15–20%; more than half on the top
tier means the specs aren't carrying the load). You may re-write, merge, split or re-order any **unconsumed** prompt and
the README table. Record every change and its reason in the spec's §0 and in 99's inbox. If you change nothing, say so.

## Job — write `docs/agent/reports/FIXTOGGLES_SPEC.md`

Sections, all required. Tag every load-bearing claim MEASURED / SOURCE (file:line) / INFERRED.

- **§0 Chain re-validation** (job 0's result).
- **§1 Routes, re-derived — never inherited from the research report.**
  (a) the Mod Options route (`ModItemOptionToggle`, `default_options`, `CurrentModOptions` load-before-code, Apply →
  `ApplyModOptions`, persistence) on 1.1.0, with the lines;
  (b) the Options-category route (`OptionsCategories` + `run`) and what window classes a panel may use;
  (c) the mod-persistent-storage route (`CurrentModStorageTable`, `WriteModPersistentStorageTable`, `MaxModDataSize`);
  (d) **every engine name the surface and the store will touch, checked against `ModEnvBlacklist`/`ModMsgBlacklist`**
  in the shipped `Mod.lua` — list them;
  (e) the gamepad focus model for the list/checkbox classes a panel would use (what makes a row reachable by D-pad, how
  the built-in Options pages do it) — SOURCE only; the proof is 03's.
  (f) spot-re-verify the research report's §3 table: open ALL nine non-trivial modules (SaveSanitizer, SaintBlessing,
  TrackTunnelPowerBridge, ExoticDepositSign, SilentHitMomentFX, DustSicknessBiorobots, SinkholeIndestructible,
  CrystalMysteryHang, ArrivalDeaths/ShelterReflex pair) and at least 10 of the rest; record each row CONFIRMED / CORRECTED.
- **§2 The framework contract.** Registry fields (stable id shown to players, `beta`, `default_on`, `restart_required`,
  link group, always-on parts); the ONE store and its schema (**deviations from default only**, README rule 11); the
  reconciler (generalise `ApplyModOptions`' reconciler or its equivalent to every module); the gate helper's shape and
  its call contract (inert for foreign objects first; captured original from the DECLARING class, F107 rule); what
  `SMRFixPack_Disabled` and the stand-down dialog (`UpdateSuspects`) do alongside a player switch; the log lines a
  switch writes (the sitting reads them); how a registered-but-not-yet-converted module is shown and refused (so a
  half-converted tree is never mistaken for switchable).
- **§3 The 45-row disposition table** — one row per registered module: live-gate / undo / next-load / split
  (always-on part named); what off→save→on does to the save (§7); link group; Beta candidate + proposed default; the
  player-facing title (a draft; 08 finalises). Assign each row to 02/04/05/06/06b exactly as the README splits them, or
  re-split with a reason.
- **§4 Linked buttons.** Define what "linked" means to a player (one switch for the group? turning A off forces B off
  with a shown reason?). Enumerate TRUE dependencies with evidence (a module whose correctness needs another active),
  and separately the shared-target clusters that are NOT dependencies under a per-call gate (prove the `Colonist:Idle`
  pair is independent, or that it is not). Owner's words: *"if we do we should make sure thier button is linked."*
- **§5 Beta.** Definition in the status vocabulary (e.g. "not `tested-attended`/`tested-unattended` on the current
  branch"); where the flag and the per-fix default live (entry front matter? the Register def? both, checked by a
  tool?); promotion semantics (a default change reaches untouched players by construction — rule 11); the UI tag; the
  CURRENT candidate list with each entry's status (F116, F117, F118, the Saint heal; F119 if built) → a proposed
  per-fix default for the owner (ck148 ruled *per fix*).
- **§6 The surface decision package** for ck148(a): built-in Mod Options page vs our own panel vs both-over-one-store;
  what each costs; console reach; 03's kill criteria written as numbered, falsifiable checks; the fallback. Plus an
  **original visual direction** for our panel (layout, what a row shows, how Beta/links/restart-required read) that owes
  nothing to the reference mod's constants or wording (rule 9).
- **§7 Save safety for runtime switching (`FIX_POLICY` §3a).** Per module: can switching it off mid-campaign, saving,
  and switching back on harm a save (stamps, persisted fields, threads, deletions already made)? The honesty rail for
  every player-visible sentence (rule 8). The TrackTunnelPowerBridge teardown (never switchable). Any module whose
  answer is "harmful" is routed to the owner with the reason — the owner accepts partial coverage only for a good reason.
- **§8 Policy text.** Draft the `FIX_POLICY` §5 rewording (toggles now exist for fixes; the section's real test —
  "a behaviour change a player wants to opt into is not a fix" — survives) and a new §2 install rule for the gate.
  **Land the §5 rewording yourself** (the owner's ask rules it; cite ck148). Leave §2a untouched.
- **§9 Test design.** The desk harness (`tools/desk_toggles.py`, run by `tools/deskbench.py`): both enable paths, gate
  on/off, undo, persistence round trip, deviation-only storage, a falsifier per assertion. TestKit impact (probes read
  the registry — an off module must SKIP by name, never FAIL). The attended legs for 03 and 11 with predictions.
- **§10 Owner decisions** — append to checklist **148** in the owner's plain language, each with a recommendation.

## Scope fence

IN: the spec, the README/queue edits job 0 makes, `FIX_POLICY` §5 rewording, checklist 148 appends, the spec's
research reads. OUT: any `Code/` edit (02 onward); any version work (09 only; rule 10); player text (08). An
interesting out-of-fence finding is FILED, not fixed.

## Stop conditions — reporting beats pushing through

- A route the contract needs (store, surface, gate) turns out blocked by the sandbox → stop, write what you proved,
  route the question.
- A module cannot be made safely switchable → record why, route it; do not quietly exclude it.
- The per-call-gate premise (rule 7) fails for some shape → stop; that is a design change the owner must see.

## What may NOT be claimed

Nothing works "in game" (no game has run). No module is "safe to switch" on source alone — say "source-derived".
"Off = vanilla" in any form (rule 8). A research `[R]` row as verified unless you opened it.

## Close-out

Live todo list throughout (README rule 13). Commit the spec + §5 + checklist appends + any queue edits; outbox to
02's and 99's inboxes (what 02 must build first, every CORRECTED row, every open question); strike your row; `git rm`
this file; push.

## Notes from upstream

- From the authoring session (`smr-bugfixpack-24`, 2026-09-11): the research is `reports/FIXTOGGLES_RESEARCH_2026-09-11.md`.
  Two tensions are yours to carry, not resolve silently: `FIX_POLICY` §5's "needs a toggle ⇒ not a fix" (overridden by
  the owner's ask — reword it) and §2a's "no version detector" (UNTOUCHED; B step). The reference mod's version
  dropdown is display-only and its "Reset" means all-off — do not inherit either. The peer session `smr-bugfixpack-0d`
  filed F119 (ck146): if the owner rules it built, it is the first real Beta fix — design §5 so it can ship as one.
