# 03b — seam presets and generated consumers: live plan

2026-09-10. Parent: Codex `/root`. Source-review agents are read-only; the
parent owns every repository write, sample, verdict, filing and handoff.

## Live todo — one commit-and-verify unit per item

- [x] Pin HEAD/build/manifests, size the exact 03b queue, and commit this plan;
  PROBE SWEEP: clean; chain gates GREEN.
- [x] Read the 560-row food/resource/UI preset batch; parent re-derives its
  surviving leads and sample, records exact coverage, then runs chain gates and
  commits the durable report.
- [x] Read the 548-row progression/politics preset batch; parent re-derives its
  surviving leads and sample, records exact coverage, then runs chain gates and
  commits the durable report.
- [>] Read the 510-row support/story preset batch; parent re-derives its
  surviving leads and sample, records exact coverage, then runs chain gates and
  commits the durable report.
- [ ] Read all 360 generated INVENTORY rows and six CALLERS items, enumerate
  generated/Data twins and actual consumers in both directions, reconcile the
  three preset reports, then run chain gates and commit the durable report.
- [ ] Falsify and file every surviving candidate in one or more race-safe
  batches; add only fresh-fixture/runtime decisions to the owner checklist;
  regenerate indexes, repeat applicable desk controls, run chain gates, commit
  and push each batch immediately.
- [ ] Close out: append 03b's named TRIAGE section and complete outboxes,
  preserve exact read/not-reached receipts and limits, update README/STATE,
  consume this one-shot prompt, run the clean probe sweep and all chain gates,
  commit with explicit paths, push, and verify HEAD plus worktree state.

Exactly one item is in progress. If a stage produces more than one reviewable
commit, this list is expanded before the extra work begins.

## Pin and exact queue

Start HEAD `7987b28`; `git pull` reported already up to date and the worktree was
clean. The prompt was added by `0683c48`; later drift through current HEAD only
records the resolved commit-hook environment cause. Installed Steam buildid is
still `24995074`, matching archived 1.1.0.403908. Pinned trees:

- `C:/Dev/SMR-SrcArchive/1.0.7.396349/Src` — manifest 4,448 files,
  `09d95e3448573dc378fa0bed5fc987fead3aafb70bf2ecf6a2cddef3f1ff9921`.
- `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src` — manifest 4,717 files,
  `a4577da25cb3fe8586bb7388b9b557d3dfd343938e453382e65d066f1945b3b2`.

`SEAM_COVERAGE.tsv` assigns 03b exactly 360 INVENTORY rows (119 removed,
121 body, 99 added, 21 body+sig), 1,618 PRESETS rows across 49 registries and
six CALLERS items; no NOROWS. The original tagged TSVs and dated coverage
snapshot remain unchanged.

## Read-only agent batches

Each agent returns every row under README §4's contract: key; preset/file and
consumer; class; both-tree locations; actual change; reach tier and player
action; falsifier; old×new seam; non-owner answer; and a cited `SMELL`/`PERF`
tell or `none`. Added presets compare the prior behavior path, not a fabricated
old file. Each batch identifies complete, hunk-only, malformed and not-reached
items. Agents do not write repository files or issue verdicts.

| batch | rows | exact registries |
|---|---:|---|
| food/resource/UI | 560 | CropPreset, ResourcePreset, Animal, BuildingTemplate, XDef, Resource, Vegetation, CargoResource, BuildMenuSubcategory, AmbientLife, Achievement, BugReportTag, Trigger, TutorialStep, ParticleSystemPreset |
| progression/politics | 548 | FactionDef, TechPreset, Tech, LawDef, PolicyDef, FlightPolicyDef, CommanderProfilePreset, SponsorGoals, MissionSponsorPreset, Challenge, GameRuleDef, EffectDef, TechFieldPreset, Milestone |
| support/story | 510 | PresetDef, StoryBit, SA_Exec, OnScreenHint, Label, SA_WaitMessage, SoundPreset, ClassDef, NotificationPreset, PopupNotificationPreset, EncyclopediaArticle, SA_GrantTechBoost, MsgDef, SA_WaitChoice, AppendClassDef, DumbAIDef, ScriptConditionList, StatsImpactRest, StatusEffectPreset, TraitPreset |

The parent reads the generated queue and caller contracts so it can establish
which definition is live, connect each field change to an actual Lua reader,
and distinguish generated twins from duplicate runtime effects. Priority seams
are Crop/Resource/recipes, Tech/TechPreset, Law/Policy/Faction, cargo,
BuildingTemplate and XDef/class twins. FR preset rows are read first: four
ParticleSystemPreset FR-1(c), one EffectDef FR-2 and one StoryBit FR-2.

## Controls, limits and stop conditions

There are no eligible F114–F117 seeds in this generated/preset queue; the score
will therefore be `0 eligible`, never 4/4. The parent draws and records a
reproducible random sample across all three preset batches plus generated rows,
before reading the agent verdicts for those sample keys. Surviving claims are
re-derived from the archived Lua and receive negative/counterfactual controls
where a real-Lua deskbench is suitable.

No game launches, modules, metadata/version fields, archives, installed files or
sibling-owned queues are in scope. Native consumers, anonymous/dynamic callers,
rendering/timing, actual execution, consoles, absent assets and incomplete old
DLC remain blind spots. A needed DLC interior beyond one directly called
function is routed to TRIAGE `For dlccheck` with `TAKEABLE WHEN`; it is not read
as 03b coverage. Runtime proof becomes a checklist rider, never an unattended
launch. If context cannot hold the remaining work, the parent first commits all
authorized filing and creates a first-class child with exact remaining keys,
README ownership and a 99 gate.
