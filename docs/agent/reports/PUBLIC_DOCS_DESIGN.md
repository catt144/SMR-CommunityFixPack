# Public-docs design — the player-facing surfaces

**Written 2026-08-13 by `agent/prompts/public-docs/01_DESIGN.md` (consumed).**
Chain rules and the exposure framing: `agent/prompts/public-docs/README.md`.
Reviewed next by that chain's `02_QA.md`; built by prompts 3 and 4.

> ⚠️ **This is a report, and reports are not authority** (`docs/README.md`).
> Where it disagrees with an `agent/bugs/` entry or an `agent/facts/` fact, the
> entry wins. Every count below was re-derived on 2026-08-13 with
> `--emit-counts` or by reading the source cited; none was copied from prose.

---

## 0 · What was re-derived, and what moved under me while I worked

**Counts, `python tools/doccheck.py --emit-counts`, both repos, 2026-08-13:**

| | fix pack | opt-in pack |
|---|---|---|
| registered modules | **74** (74 default-active, 0 optional-gated) | **8** (1 default-active, 7 optional-gated) |
| `Code/*.lua` files | 75 | 9 |
| index rows | 102 F + 12 D + 46 C = 160, in 125 entry files | 0 F + 9 D + 0 C = 9 |
| TestKit probes | 88 (one shared kit, serves both mods) | 88 (same kit) |

**F-row status distribution, counted off `agent/bugs/INDEX.md`:** 41 `fixed` ·
40 `tested` · 11 `wontfix` · 3 `filed` · 2 `open` · 2 `closed` · 1 `todo` ·
1 `investigating` · 1 `folded`. ⇒ **81 F-entries carry a shipping status,
delivered by 74 registered modules.** The two numbers differ because some
modules bundle several defects (`Fix_TrainMinors`, `Fix_DroneTransportMinors`,
`Fix_SequenceLatents`) and one module is the save-repair pass rather than a
fix. ⛔ **Neither number is the player-facing count yet** — the entry→module
mapping has never been derived, and §4 recommends the count stop being a
headline at all, which makes the derivation a nice-to-have rather than a gate.

**⚠️ Three staleness corrections to this chain's own brief**, found by reading
git rather than prose (`README.md` and `01_DESIGN.md` were authored earlier the
same day):

1. **The opt-in mod's display name is NOT open.** ✅ Decided by the owner
   2026-08-13 — **"Community Fix Pack: Opt-In Modules"** — and swept the same
   day across 15 sites in 11 files, pushed `e17586b`
   (`SMR-OptInPack/docs/agent/PROVENANCE.md` §3). `01_DESIGN.md` Job 8 lists it
   as owed; it is closed. **Prompts 3 and 4 use the decided name.**
2. **The `public-site/` specimens already carry the dead working title.**
   `content/index.md` says *"Community Opt-In Pack"* in its tabbed block, and
   `install.md` says the display name is "not yet chosen". Both are pre-sweep.
3. **`install.md` contradicts the frozen description on a factual point.** It
   says to turn opt-in modules on *"then restart"*; `MOD_DESCRIPTION.md:501`
   says *"Toggles take effect immediately — no restart needed."* The frozen file
   is the one written against measurement. ⚠️ Prompt 4 re-derives this from the
   opt-in pack's own code before either sentence ships — it is exactly the kind
   of claim a player checks.

**Concurrency.** The D13 chain ran beside this one in the same tree throughout.
Nothing under `agent/prompts/d13-rescue/`, `agent/bugs/D13.md`,
`agent/facts/EF-023.md` or `agent/reports/D13_EXPOSED_SET.md` was read for
content or touched; `docs/agent/STATE.md` was **not edited** (§10 carries the
line this chain wants added, as a request). `D13.md` was deliberately not quoted
— see §8.

---

## 1 · The audience split, and it is the whole design

Three readers, three doors, three different questions. The design follows from
deciding **which surface owes which reader**, and refusing to make any surface
serve all three.

| reader | arrives via | budget | wants |
|---|---|---|---|
| **the scroller** | the Paradox Mods / Steam card | ~15 seconds | *what is this · is it safe for my 300-sol save · does it change my balance* |
| **the searcher** | a search engine, or a link from the card, with a specific bug in mind | as long as it takes, but zero patience for scrolling | *is MY thing fixed* |
| **the evaluator** | a forum thread, another modder, a careful player | long | *why should I believe you · what breaks · what happens when I remove it* |

### What each surface owes each reader

| surface | scroller | searcher | evaluator |
|---|---|---|---|
| **store card ×2** | **owns them entirely.** All three of their questions answered above the fold, before any feature list | owes them **one link and nothing else** — a 74-item list on a store page serves nobody | owes the install-gating half: save safety, balance, dependencies, removal — each one sentence + a link |
| **the site** | owes them a landing page that repeats the card's three answers, because some scrollers arrive here first | **owns them.** Search box and categories; the list is a database with a query box, never a page to read | **owns them.** Reasoning, compatibility, the uninstall truth, the judgment calls, the honest limits |
| **the repo (`docs/`)** | nothing | nothing | owes them **receipts and nothing else** — reachable by one honest line, never linked as documentation |

⭐ **The one rule that falls out of the table:** *no surface tries to be two of
these.* The store card's job is to end in a decision (install / do not install)
in 15 seconds. The site's job is to answer a question someone already has. The
repo's job is to be checkable. Every failure mode of a mod page — the wall of
bullets, the 74-item list nobody reads, the FAQ that answers questions nobody
asked — is one surface trying to do a second surface's job.

### ⭐ Reframing the owner's question, deliberately

The owner asked: *"Do we need a separate FAQ, like the big mod creators?"*

**The FAQ is not the interesting surface, and copying the pattern would import
the wrong reason for it.** The big creators split docs off because a store
description is a single unformatted blob with a length limit and no search —
the split is forced by the **platform**, not by having many mods. Their driver
is *volume of text*; the FAQ is where the overflow goes.

**Our shape is different and our problem is different.** Two mods (three if the
rescue publishes), and the pressure is not text volume — it is that **the
searcher cannot be served by any linear document at all**. 81 repaired defects
is not a long list; it is a *database*, and the only usable entry point to a
database is a query. That is the problem to design around.

⇒ **The surface set is decided by the searcher, not by the FAQ.** The FAQ then
falls out as a small, cheap by-product: it is the page for questions that arise
*after* installing, which is a genuinely different job from the store card's
install-gating questions (§6 splits them). We build an FAQ because it is the
right home for ~10 real questions we already have — not because peer sites have
one.

---

## 2 · Site topology — recommendation, with the argument that changed

✅ **Platform is DECIDED (owner, 2026-08-13): GitHub Pages.** Not re-opened.
Scaffold at `public-site/` (MkDocs + Material), workflow
`.github/workflows/publish-site.yml`, `workflow_dispatch` only, Pages not
enabled. Both exposure guards stay: `docs_dir: content` in `mkdocs.yml`, and the
build step that fails if that line changes or any path escapes `public-site/`.

### ⛔ THE VERIFICATION THE PROMPT ASKED FOR — and it lands on the recommendation

`01_DESIGN.md` was right to separate two claims and right that only one was
proven. **The second is now measured, and the answer is the uncomfortable one.**

* **"Inert at load" — already proven.** Only files listed in `metadata.lua`'s
  `code` table execute (`Mod.lua:490-521`). Nothing else in the folder runs.
* **"Not in the upload" — FALSE as things stand.** The upload path is
  `CommonLua/Classes/GedModEditor.lua:678-741`. `CreatePackageForUpload` does
  `AsyncListFiles(content_path, nil, "recursive")` over **the whole mod folder**
  and packs every file that does not match a `metadata.lua` `ignore_files`
  wildcard (`:717-731`), then `AsyncPack`s that list (`:735`). It is the single
  packer — the upload flow at `:793` and both debug paths (`:749`, `:764`) all
  route through it.

**Our `ignore_files` (both repos, identical):** `*.git/*` · `*.svn/*` ·
`*/Source/*` · `*/SourceData/*` · `*/docs/*` · `*/.claude/*` · `*README.md` ·
`*.gitignore`.

⇒ **`public-site/` matches none of them.** If the site stays in the fix pack
repo, **the whole MkDocs tree ships inside every player's download** of the fix
pack — inert, invisible, and wrong.

⚠️ **A pre-existing finding on the way, and it is bigger than the site.** Under
the same rule, these fix-pack root entries are also unfiltered today:
`tools/` · `.github/` · `CLAUDE.md` · `LICENSE` · `.gitattributes`. The opt-in
repo has the same gap minus `.github`/`public-site`. **`CLAUDE.md` is
agent-facing instruction material and would ship inside a player's download**
— which is not an exposure hazard in the secrecy sense (§ the README's
correction: the repo is public on purpose) but *is* the "player lands in agent
workflow docs" failure the whole site design exists to prevent, delivered
straight to their disk. ⚠️ Whether `.github/` escapes `*.git/*` depends on
`MatchWildcard`'s exact semantics; that is an engine function with no Lua body
in `Src`, so it is **unverified in both directions** — `public-site/`,
`tools/`, `CLAUDE.md` and `LICENSE` match nothing under any reading and do not
depend on it. ⛔ **Not fixed here** — `metadata.lua` is code and this chain's
scope fence excludes it. Routed to the release checklist as item 23 (§9).

### ⚖️ THE RECOMMENDATION: its own repo

Already the owner's open question as checklist item 21. The recommendation
stands and is now stronger:

* **Its own repo** (e.g. `SMR-CommunityMods`) ← **recommended.** One site
  serving both shipped mods and the rescue artifact when it lands · a neutral
  URL rather than one mod's · **nothing ships inside either mod, structurally
  rather than by remembering to maintain an ignore list** · and a docs-only repo
  has no agent corpus to leak, so the exposure gate stops being configuration.
  It is also the peer pattern — "Dash's Vault" is one site with a mod tree under
  it, not a site per mod. **Cost: ~15 seconds of owner time**, and the scaffold
  moves with a `git mv` — it was built self-contained for exactly this.
* **Stay in the fix pack repo.** Zero new repos. But this repo *is* the mod (the
  game's Mods folder is a junction into it), so **the site ships in the
  download** unless `ignore_files` gains a `*/public-site/*` line and keeps it
  forever; and the URL reads `catt144.github.io/SMR-CommunityFixPack/` for a
  site that also documents the opt-in pack and later the rescue.

⭐ **The packaging finding does not decide it** — one `ignore_files` line closes
that hole — but it converts the choice from *aesthetic* (which URL reads better)
to *structural* (which arrangement cannot regress). Nothing in this chain is
blocked either way: prompts 3 and 4 write into `public-site/content/`, and the
folder moves whole afterwards.

---

## 3 · The honest content inventory

**What already exists, in the right voice:** `docs/archive/MOD_DESCRIPTION.md`
— 748 lines, FROZEN, and genuinely good raw material. Roughly **90 player-facing
fix bullets** already written in player language, plus a save-safety section, a
compatibility section, a "fixing your already-broken save" section, a
"looks like a bug, but isn't" essay, a reporting section and credits.

⛔ **But it is dated 2026-08-03 and pre-split, and three things in it are now
wrong**, which is the single largest hidden cost in this table:

1. **It describes a one-mod product.** Its entire "Optional modules" section
   documents 8 modules as living *inside* the fix pack, under
   *Options → Mod Options → **Community Fix Pack***. All eight moved to a second
   mod on 2026-08-12 with its own page and its own name. **Every occurrence of
   that Mod Options path in it is false**, and the file has to be *split*, not
   edited.
2. **Its counts are stale** — "an automated suite of 77 checks" (now 88 probes,
   both-mods read `78/0/10/0`), and its fix list predates ~20 entries.
3. **Its F76 explainer is VOID** (chain-12 QA ruling, 2026-08-03: F76 is CLOSED
   — REFUTED). Two stacked `[DRAFT NOTE]` blocks in it say so at length. ⛔ That
   text must never publish in any form; §5.6 makes it a standing rule.

**What holds the truth per fix:** `docs/agent/bugs/` — accurate, current, and in
agent language with file paths, function names and `F##` ids. Rule 4 bars all of
it from player text, so every entry needs a translation pass, not a copy.

### The inventory

| # | surface | exists? | what must be written | agent hours | owner cost |
|---|---|---|---|---|---|
| 1 | **Store description — fix pack** | ~70% (frozen file, minus the opt-in half, minus stale counts, plus tiering) | re-tier to §4's three tiers; strip the 8 modules; re-derive counts; add the judgment-calls section | 3–4 | wording sign-off (~15 min) |
| 2 | **Store description — opt-in pack** | ~50% (the 8 module blocks are written and good) | a whole new top: what this mod is, why it is separate, that neither mod needs the other | 2–3 | wording sign-off (~10 min) |
| 3 | **Site: landing** | specimen exists, 2 stale strings | the three scroller answers + the two-mods split + two buttons | 1 | — |
| 4 | **Site: installing** | specimen exists, 1 contradiction, 2 holes | real store links; load order answered rather than deferred; the restart truth re-derived | 1–2 | store links exist only after upload |
| 5 | **Site: "Is my bug fixed?"** | 3 of ~81 entries drafted | **the big one** — ~81 entries in `What you saw / What was wrong / After the fix`, categorised, searchable | **8–12** | — |
| 6 | **Site: FAQ** | specimen exists | ~12 questions, seeded in §6, each with an earned answer or a marked hole | 2 | — |
| 7 | **Site: save safety & uninstall** | nothing | skeleton now, holes marked; D13-gated (§8) | 1 now, 2 after D13 | — |
| 8 | **Site: "why trust this"** | material in the frozen file | the evidence bar in player words, the honest limits, the receipts link | 1–2 | — |
| 9 | **The judgment-calls section** | proposal adopted, wording owed since 08-04 | draft in §9 so the owner approves rather than composes | 0.5 (done) | **~15 min of owner prose** |
| 10 | **`metadata.lua` `short_description` ×2** | placeholder | one sentence each, matching tier 0 | 0.25 | — |
| 11 | **Screenshots** | none | §5's shot list | 0.5 to plan | **one 45–60 min sitting, in game** |
| 12 | **Preview image ×2** | none | ⛔ an ART problem, not a writing one | 0 | **owner or a commission; unbounded** |
| 13 | **Portal pass ×2** | none | — | 0 | **~1–2 h, owner-only** |

**Agent total: roughly 22–30 hours**, of which #5 alone is a third.
**Owner total: roughly 2–3 hours plus the preview art**, and every hour of it is
in exactly four places — the judgment-calls wording, one screenshot sitting, the
preview art, and the portal passes.

⭐ **The sizing's one real lever:** #5 is the largest agent item *and* the one
that decides whether the searcher is served at all. Everything else can be
trimmed; that cannot. ⚠️ And #12 is the only item with an unbounded tail — it is
not writing, it does not get better with agent hours, and it should be started
early rather than discovered at launch. It is on the checklist as item 24 (§9).

---

## 4 · The TL;DR problem, solved

### 4.1 Three tiers, each standing alone

**Tier 0 — one sentence.** Goes in `short_description`, the card's first line,
and the site's `<title>`-adjacent lede. Must contain *what it is* and *the
strongest install-gating fact*, and nothing else:

> Bug fixes for *Surviving Mars: Relaunched* — safe to add to a save you have
> already played, and it does not change how the game is balanced.

**Tier 1 — about ten lines.** The rest of the store card's first screen. §4.2
fixes its order. A reader who stops here must not be misled: that is why the
removal answer is *in* tier 1 rather than deferred, even though it is the
weakest of the four.

**Tier 2 — everything.** The site. Nothing on the card is a summary of tier 2
that changes meaning when expanded; tier 2 only ever *adds*.

⭐ **The standalone test, stated so prompt 5 can audit it:** for each tier, ask
*"if a reader stops here and acts on it, is anything they now believe false?"*
That is a sharper test than "is it complete", and it is the one that kills the
usual store-page failure — a confident summary whose caveats live three
paragraphs down.

### 4.2 Install-gating questions come first, above any feature list

The four questions that decide whether someone installs, in this order:

| # | question | our answer | strength |
|---|---|---|---|
| 1 | **Is it safe for my existing save?** | Yes, including a long one. The mod writes almost nothing into your save, and what it writes is inert without it — the footprint is enumerated, not summarised | ⭐ **strong, and unusual** — this is the project's single best claim and it is earned |
| 2 | **Does it change balance?** | No. Only defects verified in the game's own code. Preferences live in a separate mod you do not need | ⭐ **strong** — and it is the whole reason the split happened |
| 3 | **Do I need anything else?** | No. Neither mod needs the other; both work alone and together | ⭐ **strong** — measured both directions 2026-08-12 |
| 4 | **What happens if I remove it?** | Built to be removable at any time; the original bugs come back. **One real caveat** (a drone dial left off base) and a rescue tool for it | ⚠️ **the weak one, and D13 owns the detail** (§8) |

⛔ **Do not lead with the feature list.** The frozen file leads with two strong
paragraphs and then a 90-bullet list; the list is what a scroller sees when
they scan, and it answers none of the four. **Tier 1 answers all four before any
bullet, and replaces the bullet list with four or five category names plus one
link.**

⭐ **Answer #4 rather than hiding it.** Three strong answers and one silently
missing answer is the pattern that costs credibility with the evaluator — who
is the reader who writes the forum replies everyone else reads. One honest
sentence plus a link beats an omission.

### 4.3 The searcher never scrolls a list

**Decision: the fix list is a searchable page, and its entry point is the search
box, not the top of the list.** Concretely:

* MkDocs Material's built-in search (`Ctrl K`) is the primary entry point, and
  the page says so in its first line — *"search what went wrong"* with four
  worked examples (*meteor*, *colonists suffocate*, *train*, *drones stuck*).
* Entries are **collapsed by default** (`pymdownx.details`, already enabled).
  A collapsed entry shows only its title, which makes ~81 entries a scannable
  page rather than a wall — and search expands the match.
* ⭐ **Titles are written as the player's symptom, never as our diagnosis.**
  *"Sensor Towers made meteors MORE frequent instead of less"*, not *"Sensor
  Tower bonus applied with inverted sign"*. Search only works if the words in
  the title are the words in the player's head.
* **Categories are a secondary index for browsers**, not the primary structure.
  Proposed set, taken from the frozen file's own groupings because they have
  already survived a writing pass: *Disasters & weather · Colonists & domes ·
  Drones & logistics · Buildings & economy · Trains · Rockets & asteroids ·
  Story & mysteries · Interface & numbers*. ⚠️ Prompt 4 re-derives the bucket
  sizes and merges any category under ~4 entries.

### 4.4 ⛔ Kill the count as a headline

*"74 fixes"* impresses nobody, invites *"which ones?"*, and is the wrong unit —
a player cares whether **their** bug is in there, not how many other people's
are. It is also three different numbers depending on what you count (§0), which
means any headline version of it is a hostage.

**Decision: no count in tier 0 or tier 1.** The count may appear once, in a
neutral position on the fix-list page (*"this page lists every fix in the
pack"*), and in `last_changes` where it is genuinely informative. Where a
scroller would expect a count, the card gives **category names** instead —
which answer the real question (*is my kind of problem in scope*) that a count
only pretends to answer.

### 4.5 ⛔ The vocabulary the surfaces may and may not use

**Rule 6 applies to phrasing, not just facts.** The frozen evidence bar is
`fixed` + the automated suite + per-fix runtime self-checks + the verified
save-safety tier. Word choice can silently upgrade that bar, so the vocabulary
is a decision, not a style preference.

**✅ ALLOWED — each is exactly what the bar supports:**

| phrase | what earns it |
|---|---|
| "verified in the game's own code" / "verified against the game's code" | every entry is source-verified before a line is patched |
| "checks the game's code before it patches anything, and switches itself off if the game no longer looks the way that fix expects" | the per-fix runtime self-checks + fail-safe registry |
| "an automated suite of **N** checks, run against a modded and an unmodded build before release" | the shared TestKit — ⛔ **N is re-derived at write time**, never copied (88 probes as of 2026-08-13) |
| "built to be safe to add or remove at any time" | the frozen file's own wording; it says *built to be*, which is a design claim, not an outcome claim |
| "measured" | ⚠️ **only where the cited entry records a measurement.** Never as a synonym for "checked" |
| "we could not reproduce it on …" / "we have not seen …" | negative results, stated as negative results |
| "designed to" / "intended to" / "tries to" | the save-repair passes, which attempt and may fail |

**⛔ FORBIDDEN — every one of these upgrades the bar:**

*proven · guaranteed · fully tested · thoroughly tested · extensively tested ·
battle-tested · 100% · bug-free · risk-free · no risk · certified · safe*
(unqualified — always *"safe to add to an existing save"*, never bare *"safe"*)
*· compatible with all mods · will fix your save · never breaks · always works*

**⛔ Two forbidden moves that are not single words:**

1. **Never quote our internal status vocabulary.** `fixed` and `tested` are
   house words. In player English *"tested"* claims more than we mean and
   *"fixed"* claims less, and exposing the split (*"40 of them tested"*)
   invites *"and the other 41?"* about a distinction that the owner's own ship
   line (checklist 14) deliberately froze. **The public surfaces have one
   status: it ships or it is not mentioned.**
2. **Never compare against other mods.** See §7 for the standing rule.

⚠️ **Where the frozen file already breaks its own bar**, so prompt 3 catches it:
its *"as far as we can tell, no mod in either game's community has held itself
to this uninstall standard before"* sentence is a claim about the whole
community resting on a 471-mod survey. It ships whole or not at all by explicit
decision (`MOD_DESCRIPTION.md:117-123`) — that decision is not re-opened here,
but it is the one sentence in the file that a reviewer should look at twice, and
it is now entangled with D13 (§8).

---

## 5 · Five specimen fix blurbs — proving the format on the hardest cases

⛔ **Five specimens, not 81 blurbs.** Four hard cases and one control. The format
under test is the specimen page's *What you saw → What was wrong → After the
fix*.

**Verdict on the format: keep the three beats, add two things.**

* ⭐ **A fourth optional beat, "Worth knowing"**, for the cases with a real
  caveat. Without it, a caveat has nowhere to go except inside "After the fix",
  where it reads as a hedge on the fix rather than as information.
* ⭐ **A label on the title line** for the five judgment calls (§9), so they are
  not presented identically to a plain defect repair. The relabel package
  adopted 2026-08-04 asked for exactly this and has been waiting for a surface
  to live on; **this is that surface**, alongside the store section.

### 5.1 Hard case — a "fix" that gives some players MORE of a hazard (`F97`)

> **Dust devil waves were smaller than the map setting said** — *restores
> authored wave sizes*
>
> **What you saw:** on a map set to heavy dust devils, waves that were smaller
> than the setting promised — sometimes no devils at all when the setting said
> at least one.
>
> **What was wrong:** the game multiplied the *number* of devils in a wave by a
> *percentage* that was meant to be a separate roll. The top of the authored
> range could never occur, and the bottom could round down to zero.
>
> **After the fix:** waves come out in the range the map setting actually
> specifies.
>
> **⚠️ Worth knowing:** this one changes how the game feels, and upward. On the
> heaviest dust-devil settings you will see noticeably more devils than the game
> has ever delivered — in either the original or the remaster. The default
> setting is unaffected.

⭐ **Why this is the hardest case in the pack:** it is the only entry where the
honest description of a correct repair is *"you will get more of a bad thing"*.
The blurb refuses the word "restores" in the body (the entry proves no shipped
version ever delivered the gate — `F97`, OG disassembly) while keeping it in the
label, where it describes the *authored intent* rather than any player's past
experience. ⛔ **Prompt 3 must not soften "more devils" into "as intended".**

### 5.2 Hard case — a fix whose cure we cannot verify (`F102`)

> **Some machines froze when visiting an asteroid with Exotic Minerals
> underground**
>
> **What you saw:** the game hard-freezing on arrival at an asteroid that has
> subsurface Exotic Minerals. Reported on Linux with NVIDIA graphics.
>
> **What was wrong:** the deposit's marker sign uses the only piece of
> hand-edited art of its kind in the game. The remaster ships a clean,
> unused sign for the same resource.
>
> **After the fix:** the deposit uses the clean sign instead. Nothing about the
> deposit itself changes — same resource, same amount, same behaviour.
>
> **⚠️ Worth knowing:** we could not reproduce the freeze on our own hardware,
> so **we cannot tell you this cures it** — only that it removes the one thing
> that makes those deposits different from every other deposit in the game. If
> you have hit this freeze, we would genuinely like to know whether this helps.

⭐ **Why it is hard:** the project decided to ship a fix for a defect it has
never witnessed and cannot test (owner decision 2026-08-12: ships
*disclaimered*). The blurb has to be useful to an affected player without
claiming a cure — and it converts the weakness into the one thing that actually
helps us, an ask for a report. ⛔ **"Fixes the asteroid freeze" is forbidden
wording here** and the entry says so.

### 5.3 Hard case — a design judgment, not a defect (`F55`, relabel package)

> **A drone that failed to reach a building once ignored it for the rest of the
> game** — *behaviour change, and we will defend it*
>
> **What you saw:** buildings that drones simply would not service, for the rest
> of the colony's life, after one blocked approach.
>
> **What was wrong:** a failed approach was recorded as unreachable with a
> retry time so far in the future that the game's own five-sol "try again" could
> never fire.
>
> **After the fix:** the retry fires, and drones try the building again.
>
> **⚠️ Worth knowing:** this one is a judgment call rather than a plain repair.
> A comment in the game's own code says the permanent mark is deliberate — it is
> supposed to be cleared when the map's walkable routes change. In a real colony
> that clearing does not reliably happen, so a building gets written off for
> good. We think that effect is harmful enough to override the comment, and we
> would rather tell you so than present it as an obvious bug.

⭐ **Why it is hard:** the honest version has to say *the game's authors may have
meant this* — the comment at `Drone.lua:840` states the forever-mark is intended
and names its reset condition. That sentence is uncomfortable and it is exactly
what the relabel package was adopted for. ⛔ The label is not optional and is not
a footnote.

⚠️ **A trap prompt 3 must not fall into, and this draft nearly did.** `F55`'s
entry title reads *"Open domes: drone access lost + unreachable-forever cache"*
and the entry has **two halves — only the cache half shipped.** The open-air
dome-entrance half is explicitly **not actionable** and is engine-data, not ours.
A blurb written from the title alone describes a fix that does not exist.
⇒ **Write every blurb from the entry body and its status tag, never from the
index row's title.**

### 5.4 Hard case — a retroactive save repair (`F03`)

> **Salvaging an upgraded building left its bonuses behind forever**
>
> **What you saw:** nothing, which is the problem. Colony-wide and dome-wide
> upgrade bonuses that outlived the buildings that granted them — and stacked
> every time you rebuilt.
>
> **What was wrong:** salvaging removed the building but not the bonuses it had
> applied.
>
> **After the fix:** salvaging removes them. **And bonuses already leaked into
> your save are cleaned up the next time you load it.**
>
> **⚠️ Worth knowing:** the clean-up pass changes something only when it can
> positively identify what went wrong, does nothing when unsure, and does
> nothing at all the second time it runs. It is a genuine attempt at repairing
> existing damage, not a promise that it will repair *yours*.

⭐ **Why it is hard:** it is the pack's best selling point — *it can fix a save
you already broke* — and the one most likely to be over-promised. The last
paragraph is lifted almost intact from the frozen file, which already got this
right; the specimen's job is to prove the format has room for it.

### 5.5 Control — a plain repair (`F13`)

> **The Command Center's resource rows showed no numbers**
>
> **What you saw:** eleven rows of the Command Center resource panel rendering
> as blank space.
>
> **What was wrong:** the numbers were being drawn, but not where you could see
> them.
>
> **After the fix:** the rows show their numbers.

⭐ **Why the control matters:** it proves the format does not inflate a simple
fix. Three beats, four lines, no "Worth knowing", no label. **If every entry
needs four beats, the format is wrong.** Most of the ~81 will look like this
one.

### 5.6 ⛔ The negative specimen — the entry that must NOT exist (`F76`)

`F76` was **investigated, drafted for the mod page, and then REFUTED by
measurement** (chain-12 QA, 2026-08-03: the resource picker anchors exactly at
the cursor; the load failure did not reproduce). Its draft text survives
verbatim inside `MOD_DESCRIPTION.md:225-249` under two stacked ⛔ notes.

**Standing rule, and it is a rule about the fix list as a whole:**

> **The public fix list contains fixes we shipped. It never contains defects we
> investigated, and never contains a defect we could not demonstrate.**
> Publishing `F76` would tell players about a bug that does not exist — the
> exact opposite of the trust the surfaces are for. ⛔ The frozen file's draft
> blocks are **quarantined text**: prompt 3 splits that file and must carry
> neither block across in any form. If `C41` (the unrefuted residue) ever earns
> a shipping status, a **new** entry is written from `C41`'s evidence.

⚠️ **The near-miss is the point.** That text was written in good faith, in the
right voice, and sat in the file ready to publish for a week. Nothing about its
prose flags it. **Only the entry does** — which is why rule 3 (recorded facts
are claims; re-derive from entries) is load-bearing for prompts 3 and 4 and not
ceremony.

---

## 6 · The FAQ seed — mined, not invented

Sources: `PLAYTEST_CHECKLIST.md` (every question the owner actually asked is a
question a player will ask), the `[FAQ]`-tagged entries, `FUTURE_IDEAS.md`, and
the split's own consequences. ⛔ Nothing below was invented.

### 6.1 ⭐ The split that IS the deliverable

**The dividing line: does the answer change whether I install?**

| | **STORE CARD** — gates installation | **FAQ** — matters only afterwards |
|---|---|---|
| | Is it safe on my existing save? | Why did my dials/toggles reset? |
| | Does it change balance? | Load order, and other mods |
| | Do I need the other mod? | How do I turn one fix off? |
| | What happens if I remove it? | Will it fix my already-broken save? |
| | Console/gamepad — anything different? | Why isn't *X* fixed? |
| | Which game version? | Which fixes are judgment calls? |
| | | "Dismissed warnings come back" — not a bug |
| | | The Retirement-Dome hotel wrinkle |
| | | Classic rockets: the already-parked rocket |

⭐ **Two of these are not obvious and are worth defending:**

* **"Console/gamepad" is an install-gating question, not an FAQ question** — the
  achievements rule (below) changes whether a console player installs *at all*.
  Burying it in an FAQ would be the single most consequential omission on the
  card.
* **"Will it fix my already-broken save?" is an FAQ question, not a card
  question** — even though it is our most attractive claim. It is a *reason to
  install* rather than a *gate on installing*, and the honest answer needs more
  room than tier 1 has. The card gets one sentence; the FAQ gets the real
  answer.

### 6.2 The seeded questions, with what we can actually say

| question | answer status | source |
|---|---|---|
| **Is it safe on my existing save? Can I remove it mid-game?** | ✅ **earned** — enumerated footprint; "built to be safe to add or remove at any time" | `MOD_DESCRIPTION.md:26-40`; ⚠️ the *removal* half is D13-gated, §8 |
| **What is the opt-in pack — do I need it, does the fix pack need it?** | ✅ **earned, measured both directions 2026-08-12** — neither needs the other; both work alone and together | split chain prompt 4/5, checklist 15 |
| **Why did my drone dials / toggles reset?** | ✅ **earned** — the modules moved to a second mod on the split, and a new mod id means fresh toggle state. One visit to Mod Options restores them | checklist 15 |
| **⛔ If I remove the mod with a drone dial off base, does the boost stay?** | ⛔ **YES, permanently — and this is the single most important uninstall caveat.** Set both dials back to base before uninstalling. A rescue tool exists for people who already did | `MOD_DESCRIPTION.md:34-39`; opt-in `README.md`; ⚠️ the tool half is a **marked hole**, §8 |
| **Does this change balance?** | ✅ **earned** — no; preferences are a separate mod. ⚠️ **with two honest exceptions**: the five judgment calls (§9), and `F97`, which increases dust devils on heavy settings | §5.1, §9 |
| **Why isn't *X* fixed / why is *X* optional?** | ✅ **answerable in general terms** — we fix defects verified in the game's code; things we merely disagree with are opt-in. ⚠️ **per-fix "why not" answers are NOT drafted** and should not be attempted from `wontfix` entries without reading each one | 11 `wontfix` F-rows |
| **Load order, and does it work with other mods?** | ⚠️ **partial — this is the weakest FAQ answer we have.** "Built to coexist; every fix checks the game's code first and deactivates itself rather than fighting an official patch" is earned. **A specific load-order instruction is NOT** — the site specimen defers it and prompt 4 must either derive a real answer or say plainly that we have not measured it | `MOD_DESCRIPTION.md:482-485` |
| **Console / gamepad players — anything different?** | ✅ **earned, and now source-cited.** Two things: **(1)** while any mod is enabled, achievements/trophies do not unlock on **Xbox, PlayStation and the Microsoft Store** — Steam and other PC versions are unaffected; **(2)** the per-fix disable switch is PC-only (it needs the console), while the opt-in mod's toggles work on every platform including a controller | ⭐ **newly verified this session:** `DoModsBlockAchievements()` returns true on exactly `Platform.playstation or Platform.xbox or Platform.windows_store` — `CommonLua/Classes/Achievement.lua:61-63`, consumed at `:77` and `Lua/UI/SaveLoad.lua:102`. The frozen file made this claim with no citation on record; it is **correct** |
| **Which game version, and what about updates?** | ✅ **earned** — pinned `1.0.7.396349`; each fix self-checks and stands down if the game changes underneath it | `EF-014`; per-fix self-checks |
| **Dismissed "Building Not Working" warnings come back — is that your bug?** | ✅ **earned, and the essay is already written** — no; it is deliberate vanilla behaviour, an older real bug was already fixed by the developers, and the opt-in pack carries a module for the annoyance | `MOD_DESCRIPTION.md:691-723`, lifts nearly intact |
| **Classic rockets: I switched it on and my parked rocket did nothing** | ✅ **earned** — a rocket already parked picks the behaviour up on its next landing; deliberate, and land it once if it bothers you | `[FAQ]`-tagged: `FUTURE_IDEAS.md` §2 + D01 |
| **Will it fix my already-broken save?** | ✅ **earned, with its limits already honestly written** — conservative passes, does nothing when unsure, idempotent; "a genuine attempt, not a guarantee" | `[FAQ]`-tagged: `FUTURE_IDEAS.md` §4; `MOD_DESCRIPTION.md:441-479` |
| **My Retirement Dome's hotel is filling with jobseekers** | ✅ **earned** — leave the Hotel on "Tourists Only"; on "Any Colonist" it becomes ordinary housing | `MOD_DESCRIPTION.md:637-650` |

⭐ **One structural note for prompt 4:** every ✅ above is already written
somewhere in the frozen file or an entry. **The FAQ is a ~2-hour assembly job,
not a writing job** — which is precisely why it was the wrong thing for the
owner's question to focus on.

---

## 7 · How we talk about other people's mods — the standing rule

The public surfaces will touch compatibility, prior art and credits, so this
gets decided once here rather than per-page later.

**Proposed standing rule, four lines:**

1. **We name other people's mods only to credit them or to answer a
   compatibility question a player actually has.** Never to position ourselves.
2. **⛔ We never say what another mod does badly, does not do, or gets wrong.**
   *"This fixes what mod X doesn't"* is never something we say — not softened,
   not implied by juxtaposition, not in an FAQ answer.
3. **Where a comparison is unavoidable** (a player asks "do I need mod X too?"),
   we describe **our** scope and stop. The player can read the other page.
4. **Prior art is credited by name and generously**, which the frozen file
   already does (ChoGGi, LukeH, forum reporters) and which stays.

⚠️ **The rule has one live edge already**, and prompt 3 needs to see it: the
frozen file's community-standard sentence (§4.5) is a claim about what no other
mod has done. It survives rule 2 only because it is explicitly framed as *"not
because others fell short, but because the engine never made it cheap enough to
promise"* — the comparison is to the **engine**, not to authors. **That framing
is load-bearing and must not be trimmed for length.**

---

## 8 · The D13 seam — operational, item by item

⛔ **D13 is the priority chain and its work is in flight.** `agent/bugs/D13.md`
was deliberately **not read for content** while writing this: its status tag and
tables are changing. Everything below is drawn from this chain's `README.md` and
`PLAYTEST_CHECKLIST.md` items 17–19, both stable.

### ✅ Safe to write now — nothing here depends on D13

* Everything in §1–§7 above except where marked.
* The whole fix list (§5) — the ship line is frozen, the entries are not moving.
* The opt-in pack's copy — built, verified, audit-sustained 2026-08-12.
* The **first three** install-gating answers (§4.2 rows 1–3).
* The "safe to add" half of save safety, including the enumerated footprint.
* The console/achievements answer (§6.2) — now source-cited.
* The whole screenshot plan and its sitting (§8B).

### ⚠️ Write the skeleton, mark the hole

| item | write | leave as a marked hole |
|---|---|---|
| **"What happens if I remove it?"** (§4.2 row 4) | the shape: the pack is built to be removable; the original bugs come back; one caveat exists | the exact uninstall procedure's final wording |
| **The drone-dial caveat** | ⛔ **the caveat itself is NOT a hole — it is known, real and already published in the frozen file and the opt-in README.** Write it plainly | **the remedy sentence** — the rescue tool's name, link and whether it is published at all |
| **The rescue artifact** | that a tool exists for people who already uninstalled | ⛔ **its name, its link, and its existence in any store.** Checklist 17 decided the *shape* (option (c)) and recorded **"build ≠ publish"** in the same breath. A page that names an unpublished tool is a broken promise |
| **The uninstall-cleanliness sentence** (§4.5, §7) | nothing | ⛔ **do not place it.** Whether it ships under "Reading A" (pack alone) or "Reading B" (pack + cleaner, rewritten to say so) is an explicit owner decision deferred to launch, and D13's outcome is half of it |

### ⛔ Do not touch until D13 closes

* `agent/prompts/d13-rescue/` · `agent/bugs/D13.md` · `agent/facts/EF-023.md` ·
  `agent/reports/D13_EXPOSED_SET.md`.
* **Any exposed-set count.** ⛔ Every "13" / "≥13" / "12 exposed" is superseded,
  and **no player surface may ever contain an exposed-set count in any form.**
  The player-facing statement is the *enumerated footprint in player words*,
  which is a different artifact from the derivation.
* `docs/agent/STATE.md` — D13's while their chain runs (§10).

⭐ **The seam's one-line summary for prompts 3 and 4:** *write everything about
what the mod does; write the shape of what happens when it is gone; name no
tool and place no cleanliness claim.*

---

## 8B · The screenshot plan — for a mod that is invisible when it works

⚠️ **This is genuinely hard and the plan says so.** A bug fix looks like nothing
happening. Peer mods screenshot new buildings; we mostly cannot. What follows is
the capturable surface **derived from the entries**, with each shot's job named,
and each one flagged for whether it was verified against its entry.

### The candidates, assessed

| shot | mod | job | verdict |
|---|---|---|---|
| **Opt-in Mod Options page** — 7 toggles + 2 dials | opt-in | proves the product is configurable and controller-friendly; the single best shot the opt-in pack has | ✅ **take it.** Real, visual, verified — it is `D05` and the split's verification read it as `1/8` on fresh defaults |
| **Nursery/Retirement dome policy row** — showing `off (3 would move)` → `3 moving out` | opt-in | ⭐ **the best shot in the project.** A novel UI element that shows its own effect before you click it — the only screenshot we have that is genuinely *interesting* | ✅ **take it**, and give it the card's hero slot. `MOD_DESCRIPTION.md:616-618` describes the row; ⚠️ needs a dome that actually has jobseekers in it |
| **Residency control row** — "Closed to new residents" on a dome infopanel | opt-in | shows a policy the game never had | ✅ take it, likely in the same infopanel frame as the row above |
| **Two Artificial Suns on screen** | opt-in | the only shot that looks like a *feature* rather than a setting | ✅ take it — but ⚠️ it needs two suns built, which is a real colony state, not a quick pose |
| **Drone dials dropdown, open** | opt-in | one frame that explains the dials | ✅ cheap, take it while on the Options page |
| **`F13` Command Center rows** — blank vs numbers | fix pack | ⭐ the only clean **before/after** the fix pack has that a scroller understands instantly | ✅ take it — ⛔ but see the restart cost below |
| **`F14` Domes Overview** — red low-stat highlight | fix pack | second before/after, same panel family | ✅ take it in the same before/after pass |
| **`F19` graph caption** — "Consumed" including maintenance | fix pack | third before/after; appeals to the numbers-minded | ⚠️ **weak as an image** — the difference is a number in a caption. Take it, use it on the site, not the card |
| **`F102` asteroid deposit signs** — new art renders | fix pack | shows real art on screen | ⚠️ **take it, but it is not a before/after** — the "before" is a hard freeze on hardware we do not have. It shows *three deposit signs rendering correctly*, nothing more, and the caption must not imply we photographed a cure. ⭐ The owner's 2026-08-12 leg already rendered exactly this scene (`F102`, negative-repro leg) — **the recipe exists** |
| **`SMRFixPack.ListFixes()` console output** | fix pack | proves liveness to the evaluator | ⚖️ **SITE ONLY — never the store card.** See below |
| **Mod Manager entry** | both | "how do I know it installed" | ✅ cheap, take it |

### ⚖️ The console screenshot call

**Recommendation: it goes on the site's "how do I know it's working" page, and
never on a store card.**

* On a **store card** it is a first impression, and it says *"you will need a
  developer console"* to a scroller who was deciding in 15 seconds — and it says
  it to console players for whom the console does not exist. It reads as *this
  mod is for programmers*.
* On the **site**, the reader arrived with a question, and this is the answer to
  it. Here the same image reads as *technical and trustworthy*, which is exactly
  what the evaluator came for.
* ⚠️ The command name is verified current post-split: `SMRFixPack.ListFixes()`
  (`Code/00_Core.lua:519`) and `SMROptInPack.ListFixes()` in the opt-in pack.

### ⛔ The sitting — ordered so it costs ONE sitting

Every shot is owner time in game. The order below exists because **enabling or
disabling a mod needs a FULL game restart** (D13/Mod-Manager finding), so a
naive shot list costs one restart per before/after pair.

> **Before you start:** ⛔ **`EF-056` — loading a copy of a real campaign still
> runs that campaign's autosave, and its rotation deletes your autosaves.**
> **Byte-copy every autosave first** and list them by name at the end. This has
> already cost this project one unrecoverable save.
>
> ⚠️ **Cheats are enabled on the rig.** Any shot whose content depends on a
> cheated state must be named as such, and none of the shots below should need
> one — but if a colony has to be posed with a cheat, say so beside the image.

1. **Pass A — both mods OFF, one restart into it.** Capture only the "before"
   frames: `F13` Command Center rows (blank), `F14` Domes Overview (no red).
   Nothing else. ⭐ Keep the save loaded and untouched between the two.
2. **Restart once, both mods ON.**
3. **Pass B — the "after" frames**, same save, same camera: `F13`, `F14`, `F19`.
4. **Pass C — the opt-in surfaces**, same session: Mod Options page · dials
   dropdown open · a dome infopanel showing both policy rows · the
   Nursery/Retirement row in its `off (N would move)` state **and** its
   `N moving out` state.
5. **Pass D — the set pieces:** two Artificial Suns; the Mod Manager entry.
6. **Pass E — the asteroid:** three subsurface Exotic Minerals deposit signs
   rendering (`F102`'s existing leg recipe).
7. **Pass F — PC only, console open:** `SMRFixPack.ListFixes()` and
   `SMROptInPack.ListFixes()`.

**Estimated: 45–60 minutes, one sitting, two restarts.** ⚠️ Passes D and E need
colony state that may not exist on the chosen save — prompt 4 checks the save
fixtures **before** the sitting is scheduled, and drops or re-routes any shot
whose state is not already there rather than asking the owner to build it.

### ⛔ The preview image is an ART problem, and it is routed as one

Not a screenshot, not a writing task, and it does not improve with agent hours.
**Two are needed now** (fix pack, opt-in pack), **three if the rescue
publishes.** Constraints already on record: **Paradox Mods ≤ 2 MB, Steam ≤ 1 MB**
(`WORKFLOW.md` release steps). It is the only inventory item with an unbounded
tail, so it goes to the owner now rather than at launch — checklist item 24.

---

## 9 · The judgment-calls section — a draft, so the owner approves rather than composes

**Adopted 2026-08-04** (owner `--approved`); **the wording has been owed for
nine days** and blocks nothing except itself. Five shipped fixes are correct
repairs whose *bug-ness* is a design judgment, and the adopted proposal is that
they not be presented identically to a plain defect repair.

**Draft, for the store description and mirrored as labels on the five fix-list
entries (§5's label beat):**

> ### A few of these are judgment calls, and we would rather say so
>
> Almost everything in this pack is a plain repair: the game's code says one
> thing, does another, and we make it do what it says. **Five are not that
> simple.** They are still repairs we stand behind — but each one required us to
> decide what the game *meant*, and reasonable people could decide differently.
> They are marked in the list, and here is what each one is:
>
> * **Drones writing a building off after one blocked approach** — a comment in
>   the game's own code says that permanent mark is deliberate. In a real colony
>   the condition that clears it does not reliably happen, and we think that
>   effect is harmful enough to override the comment. *(behaviour change,
>   defended)*
> * **Biorobots and Dust Sickness** — there is no coding error here. A dust
>   illness that infects synthetic colonists is a thematic judgment, and we
>   made it. *(design judgment)*
> * **Colonists sheltering in vacuum** — we added a reflex the game does not
>   have, rather than repairing one it has. An absence, not a mistake.
>   *(added safety behaviour)*
> * **Edit Payload remembering what you told it** — treating the flight
>   policy's list as a *default* rather than a *refill* is arguably how it was
>   designed. We think a row you deliberately emptied should stay empty.
>   *(design judgment)*
> * **Dust devil wave sizes** — this restores the wave sizes the map settings
>   were written for. On the heaviest settings that means noticeably more dust
>   devils than the game has ever actually delivered, in either the original or
>   the remaster. *(restores authored settings — more devils on some maps)*
>
> If you disagree with any of these, they can each be switched off individually
> on PC. We would rather tell you they exist than have you find one.

⚠️ **The last line is conditional** — the per-fix switch is PC-only (it needs
the console or a companion mod). ⛔ Prompt 3 must either qualify it on the spot
or drop it, and must not let it stand unqualified where a console player reads
it. The five entries and their labels come from `CHAIN_QA_REPORT.md` §3
(F55, F40, F73(b), F70, F97); their player-facing descriptions above were
written from the entries, not from that table's shorthand.

**⇒ The owner's job here is 15 minutes of reading and either "yes" or edits.**
That is the whole point of drafting it: the item has been open nine days because
it asked for composition rather than approval.

---

## 10 · Decisions routed, and what this chain needs from STATE

### Routed to `PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"

| # | decision | status |
|---|---|---|
| 21 | **Site topology** — own repo vs fix-pack repo | ⚖️ **already open**; §2 adds the packaging finding and re-states the recommendation |
| 22 | **The judgment-calls wording** | ⚖️ **new** — draft in §9, owner approves or edits |
| 23 | **`ignore_files` packaging hygiene** | ⚖️ **new** — `public-site/`, `tools/`, `CLAUDE.md`, `LICENSE` currently pack into the upload (§2) |
| 24 | **Preview art ×2** | ⚖️ **new** — the only unbounded item; routed early on purpose |
| 25 | **The third-party roster wording** | ⚖️ **new** — §11 |

✅ **Closed, and this chain's brief was stale on it:** the opt-in mod's display
name. Decided and swept 2026-08-13 (§0).

### ⛔ The STATE line this chain wants — a REQUEST, not an edit

`docs/agent/STATE.md` was **not touched**: it is D13's while their chain runs,
it sits at 60/60 lines against a hard cap, and two editors means one silently
deletes the other's line.

> **Requested line** (release front, after ①): *"⑤ **public-docs chain** —
> design DONE 2026-08-13 (`reports/PUBLIC_DOCS_DESIGN.md`); next `02_QA.md`.
> Platform Pages ✅, topology ⚖️ck21. Feeds ③."*
>
> **What to drop for it, if the cap binds:** the `⛔ Pre-split 82/75/8 …
> ERA-STALE` sentence in "Build state" — it names three superseded number
> triples whose only job is to stop someone quoting them, and both surviving
> readers of those numbers (`--emit-counts` and this report §0) now re-derive
> instead.

**Landed by:** the next prompt in this chain, once D13's chain is quiet.

---

## 11 · The third-party roster — a wording call that belongs to the owner

`agent/reports/BUG_LIST_AUDIT.md:355-370` is a competitive-landscape roster
under a heading reading **"Rejected (with reasons):"**. It names real people:
`LukeH`, `Ayzo`, `Fizzle Fuze`, `Silva/Dash`, `Thorik`, `akarnokd`,
`FirestormMk3`, plus nine unnamed one-off authors.

**Read in full, and the assessment is fair.** In context "rejected" means
*rejected as a SOURCE of bug reports for our list* — the section is a research
provenance record, and the adjacent sections are generous (`Tremualin` accepted
with caveat; `fredware` singled out as *"the one to watch"*; `LukeH`'s own entry
credits a genuine fix mod and a useful vanilla-defect witness). **Nothing in it
is untrue and nothing in it is hostile.**

**Three things are still worth changing, and none of them is a factual
correction:**

1. **The header word is harsh out of context.** A reader who lands on
   `:355` without `:300-354` sees their name under "Rejected".
2. **"an aggregator repack"** (`Ayzo`) is a loaded term for a factual
   observation. *"aggregates other authors' fixes"* says the same thing.
3. ⭐ **`Silva/Dash` is the author of the GitBook site the owner cited as the
   model for this very chain.** The odds of one of these people reading this
   repo are not hypothetical — the repo is public on purpose, and we are about
   to point players at it.

⚠️ **The file is in `reports/`, not `archive/`, so it CAN be edited** — the
append-only rule does not protect it. The decision is live, not academic.

**⛔ Recommendation only — this is a wording call about other people's work and
it belongs to the owner:**

> Retitle **"Rejected (with reasons)"** → **"Not used as sources, and why"**,
> and replace **"an aggregator repack"** with **"aggregates other authors'
> fixes"**. Every assessment stays exactly as it is; only the verdict tone
> goes. Two edits, no facts touched.

Routed as checklist item 25. ⛔ Nothing is rewritten unasked.

---

## 12 · Every hole marked in this document

| # | hole | who closes it |
|---|---|---|
| 1 | The rescue artifact's **name, link and publish status** | D13 + a release-time owner call ("build ≠ publish") |
| 2 | The **uninstall-cleanliness sentence** — Reading A or B | owner, at launch, against the residual set that exists then |
| 3 | **Load order** — we have no measured answer | prompt 4: derive one or say plainly that we have not measured it |
| 4 | **The restart question** for opt-in toggles — the specimen and the frozen file disagree | prompt 4, from the opt-in pack's own code |
| 5 | **Per-fix "why isn't X fixed"** answers | not drafted; needs each `wontfix` entry read individually |
| 6 | **Entry→module mapping** (81 entries / 74 modules) | prompt 4 if a count is ever needed; §4.4 says it should not be |
| 7 | **`.github/` vs the `*.git/*` filter** | unverifiable from `Src` (`MatchWildcard` is an engine function); resolve empirically at packaging time |
| 8 | **Store links** for the install page | do not exist until the mods are uploaded |
| 9 | **Passes D and E screenshot state** (two suns, an asteroid with subsurface Exotic Minerals) | prompt 4 checks the save fixtures before the sitting is scheduled |
| 10 | **Preview art** | owner or a commission; unbounded |
