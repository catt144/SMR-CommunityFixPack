# Site build — sweep and arbitration ledger

**Written 2026-08-13 by `agent/prompts/public-docs/05_BUILD_SITE.md`** (the site
build), in the pattern `STORE_BUILD_AUDIT.md` set for the store build. The
artifact this ledger is about lives in a different repo: the site is
`C:\Dev\SMR-CommunityMods` (`catt144/SMR-CommunityMods`, public, **nothing on the
web** — `workflow_dispatch` only, Pages OFF).

> ⚠️ **This is a report, and reports are not authority.** Where it disagrees with
> an `agent/bugs/` entry, an `agent/facts/` fact or the shipped code, they win.
> Every count was re-emitted with `--emit-counts` at the moment it was used.

## What was built

| page | what it is |
|---|---|
| `content/index.md` | the landing page — the three install-gating answers, then which mod is which |
| `content/install.md` | installing, the full-restart rule, what each mod puts in a save (by name), the optional pack's switches, load order, console/gamepad, "checking it is working" |
| `content/fix-list.md` | ⭐ **the searchable fix list** — 74 registered modules, nine sections, every entry folded, three beats each, the five judgment calls labelled |
| `content/faq.md` | the FAQ, opening with **job 4's hostile-reader section** (checklist 22c: *is it you · how do I get you out · where do I tell you*) |
| `content/for-modders.md` | ⭐ **new page** — the identifier-carrying per-fix disable instructions, and design hole 3 (load order) answered honestly |
| `mkdocs.yml` | nav extended for the new page; **one pre-existing defect fixed** (below) |

**Counts re-emitted at write time (2026-08-13):** fix pack 74 registered modules
(74 default-active), 75 `Code/*.lua`, 94 probes, 103 F + 12 D + 46 C rows;
opt-in 8 registered (1 default-active, 7 optional), 9 `Code/*.lua`, same 94-probe
shared kit. ⛔ No count appears in tier 0 or tier 1 of any page, and no
exposed-set count appears anywhere in any form.

---

## ⛔ Findings the WRITE caught, before any sweep ran

These are recorded first because all three are the same failure the `F76`
precedent exists to prevent — **a player-facing page describing a fix that does
not ship** — and all three came out of checking the frozen file's bullets against
the registered module list rather than against prose.

| # | finding | evidence | disposition |
|---|---|---|---|
| W1 | ⛔⛔ **`MOD_DESCRIPTION.md` promises a fix for dome plumbing that was DELETED.** Its bullet *"Domes clean up properly when they grow over a building… stale plumbing behind that a repair pass re-ran on every load"* describes `F24`, closed **wontfix 2026-07-30** with `Code/Fix_DomePipeMoveInside.lua` deleted and removed from `metadata.lua` | `docs/agent/bugs/F24.md:14`; no `Fix_DomePipe*` in `Code/`; `Register(` grep returns 74 modules, none of them this | **struck from the site before it was written down.** ⛔ The frozen file's bullet is a live false claim and is now on record as one |
| W2 | ⛔⛔ **The same file promises the research-counter fix, also DELETED.** *"swapping one researched technology for another keeps the research counters straight"* describes `F28`, closed **wontfix 2026-07-30** (reachable only from mod code, barred by `FIX_POLICY` §4a), `Code/Fix_ReplaceTechCount.lua` deleted | `docs/agent/bugs/F28.md:14` | **struck.** It had already been drafted into the site's "Under the hood" section and was removed; that section is three entries, not four |
| W3 | ⛔⛔ **The sensor-tower claim is BACKWARDS in every record that carries it.** The frozen file says *"Sensor Towers now genuinely delay strikes instead of accidentally making things worse"*; the site's own layout specimens said *"made meteors MORE frequent instead of less"*; `PUBLIC_DOCS_DESIGN.md` §4.3 uses that as its worked search example. **The code says the opposite:** the interval was `Min(spawn_time, warning_time)`, towers ADD warning time, so towers *lengthened* the interval — `F02.md:30-38` states it outright: *"towers **accidentally repair the cadence**… the players actually harmed are early colonies with no Sensor Towers"* | `Code/Fix_MeteorFrequency.lua:6-14`; `docs/agent/bugs/F02.md:30-38`, `:105-107` | **the site says the true thing**, in the meteor entry's *Worth knowing* beat: towers were accidentally papering over the fault, and after the fix the schedule is the same with towers or without. ⚠️ It never reached either store card (neither mentions Sensor Towers), so nothing shipped is wrong — but three of our own records still carry it |

⭐ **The pattern, stated for the next build:** all three were found the same way —
by refusing to write a player sentence from the frozen file's bullet and instead
asking *which registered module delivers this?* Two had no module at all. That
question is cheap and it is the one the six store sweeps did not ask.

## ⛔ A fourth finding — the site scaffold could never have built

`mkdocs.yml:33` read

```
site_description: Bug fixes and optional modules for Surviving Mars: Relaunched.
```

The unquoted value contains `: `, which is a YAML mapping delimiter. **Every
`mkdocs build` fails at the config parse**, so the scaffold committed on
2026-08-13 — and the CI workflow that builds it — had never been run and could
never have succeeded. Fixed by quoting the value. The whole site now builds under
`--strict`.

⚠️ **What that says about the specimens:** the four specimen pages were written,
reviewed and committed without anyone building them once. Local preview costs one
`pip install` and eleven seconds.

## ⭐ A measurement, taken because the design asserted it

`PUBLIC_DOCS_DESIGN.md` §4.3 says entries are collapsed *"and search expands the
match"*. **Measured on the real build** (`mkdocs build`, then reading
`site/search/search_index.json`):

* ✅ **The folded text IS indexed** — searching *Sensor Towers* or *suffocate*
  finds content that is inside a closed `???` block.
* ⛔ **Search does NOT expand the entry.** The index is sectioned by heading, so a
  hit resolves to `fix-list/#disasters-weather` — the reader lands on the category
  with every entry still folded.

⇒ The page now says exactly that: search takes you to the section, the titles are
all visible while folded, and the last click is the reader's. ⛔ No surface claims
the entry opens itself.

---

## The sweeps

Eight one-rule sweeps, each firewalled from the others and from this ledger, each
told to report evidence rather than opinions. Two of them were pointed at the
CODE rather than at the entries, which is where the terminal audit said the store
build's six sweeps under-swept.

| # | rule swept | scope |
|---|---|---|
| 1 | player language (rule 4) | all five pages |
| 2 | unearned claims / vocabulary (rule 6, §4.5), incl. every "you can X" route | all five pages |
| 3 | ⭐ fix-list entries **against the module code**, first three sections | `Code/Fix_*.lua` |
| 4 | ⭐ fix-list entries **against the module code**, remaining six sections | `Code/Fix_*.lua`, `90_SaveSanitizer.lua` |
| 5 | ⭐ every opt-in claim **against the opt-in mod's own code** | `SMR-OptInPack/Code/` |
| 6 | holes, unpublished state, broken anchors, the rescue artifact, exposed-set counts | site repo |
| 7 | site against the two store cards — contradiction, escalation, silent omission | both card texts |
| 8 | coverage both ways: 74 modules ↔ entries; retired work; exactly five judgment calls | `Code/`, `bugs/INDEX.md` |

*(Sweep verdicts and arbitration follow; every finding was re-derived by the
arbitrator from code or entries before being accepted or refused.)*
