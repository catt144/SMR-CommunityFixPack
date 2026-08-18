# Sweep findings — ⛔ NOT FOR THE NEXT LINK

⛔⛔ **IF YOU ARE RUNNING `01_LINK.md`, CLOSE THIS FILE NOW.** Reading it
contaminates you, and contamination is the one thing this chain is built to
prevent — the owner's whole design is that each session sweeps without knowing
what the last one found, so that a fresh pair of eyes stays fresh.

**Readers, and only these:** the **owner**, and the **terminal audit**
(`99_TERMINAL_AUDIT_fable.md`).

⚠️ If you opened this by accident, **say so in your report.** A contaminated link
is still useful. A contaminated link that hides it corrupts the chain's only
convergence signal.

---

## Format — append, never rewrite

```
### Link N · lens <name> · <commit>

| # | finding | severity | route | disposition |
|---|---|---|---|---|
| N.1 | one sentence | launch-blocking / real / cosmetic / unmeasured | where it went | fixed <sha> / recorded / routed to checklist NN |

**Evidence per finding** — the ROUTE re-derived, not citations inherited.
**What I could NOT reach** — mirrors this link's ledger row.
```

**Severity words, used strictly:**

| word | meaning |
|---|---|
| **launch-blocking** | a player would hit it, or it would ship something false. ⛔ Fixed immediately at any link |
| **real** | a genuine defect that is not launch-blocking |
| **cosmetic** | comments, naming, tidiness — ⚠️ two consecutive cosmetic-only links trip stopping-rule clause 2 |
| **unmeasured** | you found the question but could not answer it. ⛔ Legitimate, and it must ALSO appear in the ledger's *NOT reached* column |

---

## Pre-chain findings — 2026-08-17, before the chain existed

Recorded here so the terminal audit has the full body of work in one place.

### Seed · the upload sitting · `7824cbc`, `2f077e8`

| # | finding | severity | disposition |
|---|---|---|---|
| S.1 | `metadata.lua` had **no `image` field**; `PDX_PrepareForUpload` rejects on `mod.image == ""` before packing anything | **launch-blocking** | fixed `7824cbc`; `tools/upload_preflight.py` now guards it permanently |
| S.2 | Every Mod Editor save runs `version = version + 1`, and the upload forces a save when dirty ⇒ 1.0.1 against the ruled 1.0.0 | **launch-blocking** | fenced: `image` hand-written so the mod loads clean; `IsDirty()` measured **false** in game |
| S.3 | Paradox saves AFTER upload, Steam saves BEFORE packing ⇒ **Paradox must upload first** or it ships 1.0.1/1.0.2 | **launch-blocking** | recorded, `RELEASE_PORTAL_PREP.md` §0.5(c); Steam's own number routed to checklist 37 Q2 |
| S.4 | `update_suspect` never cleared on success, at **two** sites ⇒ a false *"the game code changed"* dialog on a brand-new release | **launch-blocking** | fixed `2f077e8`; ⛔ **unverified in a running game** |
| S.5 | `Register` appended to `order` unconditionally while state survives `ReloadLua` ⇒ every module double-listed | **real** | fixed `2f077e8`; ⛔ **unverified in a running game** |
| S.6 | ④ sheet claimed the sitting never opens the game; the upload route **is** the in-game Mod Editor ⇒ `EF-056` was live and unguarded | **real** | corrected; pre-copy taken |
| S.7 | ④ sheet's held-saves list named `Autosave Sol 311`, absent from disk (old rotation, ~100 sols back) | **cosmetic** | list corrected |
| S.8 | TestKit's own title still reads *"Community Fix Pack — Test Kit"* | **cosmetic** | ⛔ never player-visible, never uploaded; noted so it is not later mistaken for a rename miss |

**What the seed could NOT reach:** everything in the ledger's seed row — no module
was read, nothing was run in a game, and the mod has never been loaded packed.
