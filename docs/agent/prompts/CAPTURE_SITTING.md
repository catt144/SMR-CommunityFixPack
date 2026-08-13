# One-off brief — the capture sitting (screenshots + preview-art backdrops)

**Authored 2026-08-13. ⛔ DO NOT RUN WHILE THE D13 CHAIN IS LIVE** — it needs the
game, and so does D13's verification leg. Fire this when
`agent/prompts/d13-rescue/` is empty (or its remaining prompts need no game).

**Owner-attended, in game, ONE sitting.** Everything here is a capture; nothing
is a test and nothing has a pass/fail. Full reasoning and each shot's job:
`agent/reports/PUBLIC_DOCS_DESIGN.md` §8B.

⚠️ **Delete this file when consumed** (one-off convention), and record what was
captured — by file name — wherever the images land.

---

## ⛔ BEFORE THE GAME LAUNCHES — non-negotiable

1. ⛔ **`EF-056`. Byte-copy EVERY autosave first, and list them by name at
   close-out.** Loading a *copy* of a real campaign still runs that campaign's
   autosave, and its rotation deletes the owner's autosaves. **This has already
   cost this project `Autosave Sol 306`, unrecoverably.** "Use a designated
   copy" protects the file; it does not protect the folder.
2. ⚠️ **The rig has CHEATS ENABLED.** No shot below should depend on a cheated
   state — but if a colony has to be posed with one, **say so beside the image**
   so a caption never implies otherwise.
3. ⛔ **PT-00 stale-probe sweep** if the TestKit is loaded, per the standing rule.
4. ⭐ **Check the save fixtures FIRST and re-route anything whose state does not
   already exist.** Passes D, E and G need real colony state (two Artificial
   Suns; an asteroid with subsurface Exotic Minerals; a photogenic vista).
   ⛔ **Do not ask the owner to BUILD colony state for a screenshot** — drop or
   substitute the shot instead, and record which.

## ⚠️ Why the order matters

**A Mod-Manager toggle needs a FULL game restart.** A naive shot list costs one
restart per before/after pair. The order below costs **two, total**.

---

## Pass A — both mods OFF (first restart into it)

Capture ONLY the "before" frames. Keep the same save loaded and the camera
still between shots so the pair matches.

| shot | frame |
|---|---|
| `F13-before` | Command Center resource panel — the eleven rows rendering as **blank space** |
| `F14-before` | Domes Overview — low colonist stats **not** highlighted red |

## Pass B — restart with both mods ON, same save, same camera

| shot | frame |
|---|---|
| `F13-after` | the same rows, now showing their numbers |
| `F14-after` | the same overview, low stats now red |
| `F19-after` | a Command Center graph caption where "Consumed" now includes maintenance ⚠️ weak as an image; site only, not a store card |

## Pass C — the opt-in pack's surfaces (same session)

⭐ **The strongest material the project has.** Take your time here.

| shot | frame |
|---|---|
| `optin-modoptions` | Options → Mod Options → the opt-in pack: 7 toggles + 2 dials on one page |
| `optin-dials` | the drone speed (or carry) dropdown **open**, showing its options |
| `optin-domerows` | a Dome infopanel showing **both** policy rows at once |
| `optin-nohomeless-off` | ⭐⭐ **the best shot in the project** — the Nursery/Retirement row reading `off (N would move)` |
| `optin-nohomeless-on` | the same row reading `N moving out` ⚠️ needs a dome that actually has jobseekers in it |

## Pass D — set pieces

| shot | frame |
|---|---|
| `multiplesuns` | two Artificial Suns on screen — the only shot that looks like a *feature* |
| `modmanager` | the Mod Manager listing both mods enabled |

## Pass E — the asteroid

| shot | frame |
|---|---|
| `F102-signs` | three subsurface Exotic Minerals deposit signs rendering. ⭐ The owner's 2026-08-12 negative-repro leg already staged this exact scene — **reuse that recipe** (`agent/bugs/F102.md`) |

⛔ **This is NOT a before/after.** The "before" is a hard freeze on hardware we
do not own. The caption may say the signs render; it may **never** imply we
photographed a cure.

## Pass F — console, PC only

| shot | frame |
|---|---|
| `listfixes-pack` | `SMRFixPack.ListFixes()` output |
| `listfixes-optin` | `SMROptInPack.ListFixes()` output |

⚖️ **Site only — never a store card.** On a card this tells a 15-second scroller
"you will need a developer console", and tells console players about something
they cannot reach. On the site it is the answer to a question the reader arrived
with. (Design report §8B.)

## ⭐ Pass G — preview-art backdrops (NEW — this is checklist item 24)

The owner ruled a **plain text-on-image preview as a FLOOR**, so launch can never
be blocked on art. That needs backdrops, and backdrops need the game — which is
why this rides the same sitting rather than its own.

**Capture 4–6 wide, clean, uncluttered vistas.** Framing notes:

* **Leave dead space** — a third of the frame with nothing important in it, for
  the mod name to sit over. Off-centre compositions beat centred ones.
* **Highest resolution available**; downscaling is free, upscaling is not.
  ⚠️ The size limits (**Paradox Mods ≤ 2 MB · Steam ≤ 1 MB**) apply to the
  *finished* preview, not the capture — do not compress at capture time.
* **Two moods if the sitting allows:** one wide daylight colony vista, one
  night/dusk shot. Different mods can then get visibly different previews from
  one sitting.
* ⛔ **No UI, no cursor, no notifications** in frame. Hide the HUD.
* **Three previews are needed** (fix pack · opt-in pack · save rescue), so
  capture more than three — the floor is replaceable and the cheapest time to
  get options is while the game is already open.

---

## ⚖️ One scheduling question for whoever fires this

`STATE.md` already plans **② ONE combined sitting** — PT-20 redo + the D13
after-sweep + F102's minute. **This brief is a second sitting, and it probably
should not be.**

**Recommendation:** fold **Passes A–D, F** into that combined sitting — they are
UI shots that ride whatever colony is loaded and cost minutes. **Passes E and G**
may need their own save state and can be split off if the combined sitting is
already long. ⭐ Decide it when the combined sitting is scheduled, and say which
way it went. The owner's time is the scarce resource; two sittings where one
would do is the failure mode to avoid.

## Close

* Record every captured file **by name**, and every shot **dropped** and why.
  ⛔ A silently missing shot reads as "we got everything" when we did not.
* ⛔ **Re-list the autosave folder by name** and confirm nothing went missing
  (`EF-056`).
* Route the images to the public-docs chain (`03_BUILD_STORE` / `04_BUILD_SITE`)
  and strike the capture line in `PLAYTEST_CHECKLIST.md`.
* Delete this file in the same commit.
