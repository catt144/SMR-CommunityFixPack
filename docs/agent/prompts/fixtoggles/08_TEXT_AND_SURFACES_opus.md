# fixtoggles 08 — text and every surface that must now agree

Link 08 of `fixtoggles`. README binding rules 1–18 are yours — **rule 8 (off is not an uninstall) and rule 9 (never
name the reference mod; never reuse its wording) govern every sentence**. Runs after 06b and 07.

## Job

1. **Row text for every registered module** — a player title and a one-paragraph description, each derived from the
   module's `agent/bugs/` entry (act on the ENTRY, not a brief), stating what the fix does in plain words. No "Fixed"
   beyond the entry's status (owner rule 09-08). Beta rows say what "Beta" means in one line. Restart-required and
   always-on parts are said where they apply. Replace 07's placeholders.
2. **Beta flags + per-fix defaults** as the owner ruled in ck148 (per fix) — each recorded where the spec §5 says, and
   checked by whatever tool the spec named.
3. **`items.lua` / `metadata.lua`** consistent with the final module and option set (H-10). ⛔ Never `version` (H-02).
4. **Store text** — the description gains the switches (how to reach them; that off stops a fix's behaviour but repairs
   already made stay). `metadata.lua` `description` + `UPLOAD_WORKFLOW.md` §3 backups + `STORE_CARD_LIVE` in ONE commit,
   proven identical **by script**, not by eye (memory `store-card-backups-required-not-polish`). `last_changes` drafted
   for the release sitting.
5. **Site source** (`C:\Dev\SMR-CommunityMods`): the fix list and FAQ ("how do I switch a fix off?", "is my save clean
   if I switch one off?" — answer honestly per `EF-002`). ⛔ Commit only; publishing is the release sitting's
   (`publish-site.yml` is workflow_dispatch).
6. **TestKit** (`C:\Dev\SMR-BugFixPack-TestKit`, local-only by design): a switched-off module's probes SKIP by name,
   never FAIL; the census reads the switch state.
7. **Docs:** `PLAYTEST_HELP.md` console recipes for reading/setting a switch; `FIX_POLICY` §5 final wording if 01 left
   anything; the `[FAQ]` tags; the opt-in repo's `FUTURE_IDEAS.md` #9 marked UN-PARKED (by this chain) and checklist 88
   marked overtaken.

## Scope fence

IN: text, `items.lua`/`metadata.lua`, the three store backups, site source, TestKit, docs above. OUT: code semantics,
publishing anything, uploading, version text of any kind.

## Stop conditions

An entry whose status cannot support its row's wording · a store string that cannot fit the portal limits.

## What may NOT be claimed

That a switched-off fix leaves a save as vanilla. That any fix is "Fixed" beyond its entry's status. That anything is
published.

## Close-out

Green gates. Outbox to 10 and 99 (every string surface you touched, and the script that proved them identical); strike
your row; `git rm` this file; push.

## Notes from upstream

- (links 01–07 append here)
