# Public-surface sweep — every place a shipped fix must appear

**Run this whenever a fix is added, retired, or materially re-scoped.** It is the
post-release counterpart to `reports/RELEASE_PORTAL_PREP.md`: that sheet covers
*uploading*, this one covers *what the words say*. Written 2026-08-24 during the
F105 sweep, from the surfaces that actually existed rather than from memory.

⛔ **A fix is not shipped when the code is written. It is shipped when a player
can find out that it exists.** Every surface below is one a player or a reporter
reads, and a fix missing from any of them is a fix nobody knows about.

## 0 · Before you touch anything

1. `python tools/doccheck.py --emit-counts` — never hand-type a count anywhere.
2. Read the entry in `agent/bugs/<ID>.md`. The **entry is authority**; store and
   site copy are derived from it, never the other way round.
3. Decide the **player-facing symptom sentence** first — the words the player
   would use, not ours. Everything else on this list is downstream of it.

---

## 1 · The site — `C:\Dev\SMR-CommunityMods` (the fix list is the spine)

`content/fix-list.md` is the canonical player-readable list, and **the store
cards' count is derived from it**, so it goes first.

* Add one entry, in the section a player would look in — not the section that
  matches our internal cause. (F105 is a landscaping bug to a player, so it sits
  with the landscaping entries in *Drones & logistics*, not in *Buildings &
  economy* where "construction costs" would put it.)
* House format, exactly:
  ```
  ??? success "<the symptom, in the player's words>"
      **What you saw:** …

      **What was wrong:** …

      **After the fix:** …

      **⚠️ Worth knowing:** …            <- only if there is a real caveat
  ```
* ⛔ **Never say "crash" for a Lua error.** Surviving Mars catches Lua errors; the
  player sees a message box or a log line, not a CTD (`EF-065`). Say *error*.
* Mark **judgment call** only if the entry required deciding what the game
  *meant*. A plain repair is not one, and the card states how many exist.
* Fixes that repair a save already in a bad state say so — that is the sentence
  players search for.

Then re-derive, do not count by hand:
```bash
grep -c '^??? ' content/fix-list.md
awk '/^## /{s=$0;order[++n]=s} /^\?\?\? /{c[s]++} END{for(i=1;i<=n;i++) if(c[order[i]]) printf "%-45s %d\n", order[i], c[order[i]]}' content/fix-list.md
```
The section tally **must** sum to the total. If it does not, an entry is
orphaned above the first `## `.

⚠️ Also check `content/index.md`, `content/faq.md`, `content/install.md`,
`content/for-modders.md` for any claim the new fix falsifies. As of 2026-08-24
**none of them states a count** — that is deliberate, keep it that way.

---

## 2 · The store cards — `reports/STORE_CARD_LIVE.md`

⛔ **This file has TWO blocks and they drift apart if you edit one.**

| block | line marker | format |
|---|---|---|
| Paradox Mods | `═══ PARADOX MODS — plain text` | plain |
| Steam Workshop | `═══ STEAM WORKSHOP — BBCode` | BBCode |

Both carry the same claims. Edit **both**, then diff them by eye.

**The count is a WORD, not a numeral** — *"Seventy-nine repairs"* — and it is
derived from §1's `grep -c`. Update it in both blocks. ⭐ The count is only safe
because the reader can check it on the page the card links to; if that link ever
breaks, the count must come out.

Also check, in both blocks:
* the **headliner list** — does this fix belong in it? The bar is *player-facing
  and recognisable*, not *most work*. A fix nobody could notice stays in the
  "… and a good deal more" tail.
* the **judgment-call sentence** — the count of those is stated separately.
* ⛔ **The card must not imply the pack fixes a client crash.** Recorded ruling;
  re-read §"What this pays off" before touching claim wording.

⚠️ These are our *record* of what is pasted. Changing this file does not change
the live pages — **the owner pastes them at a sitting.** Say so in the report;
never write as though the page is updated.

---

## 3 · `metadata.lua` — the strings that ship INSIDE the mod

* **`last_changes`** — this is the changelog a player reads on the store. It must
  name what changed **in this version**, in a player's words. ⛔ Do not let it
  keep saying `"Initial release."` after the first patch.
* **`description` / `short_description`** — only if the fix changes a *claim*
  (e.g. the judgment-call count, or a promise about save safety). Most fixes do
  not touch these.
* **`code` list** — `H-10`: a module absent from `items.lua` **ships absent**.
  `python tools/upload_preflight.py` proves the two lists match, in order.

⛔ **Version numbers are the sitting's, never yours** (`H-02`). Hand-editing these
strings is ordinary agent work; hand-editing `version` is not.

---

## 4 · The reporter — `reports/FIELD_REPORT_REPLIES.md`

If the fix answers an open field report, the reply is part of shipping it.

* ⛔ **Promise "the next update", never a date** — the tree runs ahead of the live
  listings and the upload is the owner's.
* ⛔ **Only assert what has been observed.** Each draft carries its own list of
  derived-not-witnessed sentences; when a leg witnesses one, strike the caveat
  and say so with the log name. When nothing has witnessed it, cut the sentence
  rather than soften it.
* Name the other mod plainly if one is the cause — owner ruling 2026-08-23.
  `FIX_POLICY` §8 binds store pages and load-order advice, not issue replies.
* ⚠️ Put the **issue number** in the entry's front matter when you have it. F104
  and F105 both went days without one, so neither could be found from the issue.

---

## 5 · Close the loop

1. `python tools/doccheck.py` — GREEN, and re-emit counts if modules changed.
2. `python tools/upload_preflight.py` — 0 FAIL.
3. Commit **both repos**. ⛔ The site repo is `C:\Dev\SMR-CommunityMods`; the
   TestKit repo is local-only by design and is not part of this sweep.
4. In the owner report, separate **what is now true in the tree** from **what
   still needs the owner's hands** (pasting cards, posting the reply, uploading).

## 6 · The checklist, condensed

```
[ ] fix-list.md entry added, in the player's section
[ ] grep -c '^??? ' re-derived; section tally sums
[ ] other site pages checked for falsified claims
[ ] STORE_CARD_LIVE.md — Paradox block: count word, headliners, judgment count
[ ] STORE_CARD_LIVE.md — Steam BBCode block: same, edited separately
[ ] metadata.lua last_changes rewritten for THIS version
[ ] metadata.lua description/short_description checked (usually untouched)
[ ] items.lua / code list — upload_preflight 0 FAIL
[ ] field-report reply updated; caveats struck only where a leg witnessed them
[ ] issue number recorded in the bug entry's front matter
[ ] doccheck GREEN, both repos committed
[ ] owner report separates "true in the tree" from "needs your hands"
```
