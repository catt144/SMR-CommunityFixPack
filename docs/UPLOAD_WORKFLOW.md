# Upload workflow — owner

Everything you do to put an update live, in order, and nothing else.

**The order is: mod → store pages → site.** The store pages are what players
actually see; the site is a place people have to choose to visit.

---

## Before you start

Nothing. The agent does the words — fix list, change note, descriptions — and
tells you when it is ready. If nobody has said "ready to upload", ask.

---

## 1 · Pack

1. Main menu → **MOD EDITOR**.
2. It asks to restart the game. **Yes.** It reopens into the editor.
3. On the right, read the **Last changes** box. That text is the change note
   players will see on both stores. If it is wrong or still describes the last
   release, stop and say so.
4. **File → Pack Mod.**

⛔ Do not press the Save (floppy) button. It bumps the version for nothing.

---

## 2 · Upload

**Paradox Mods first. Steam second.** Always this order — doing it backwards
pushes the two stores' version numbers further apart, and that cannot be undone.

These are **meant** to upload by themselves, with nothing pasted:

- the page description
- the short summary
- the title and tags
- the change note

⚠️ **This is untested.** It was changed on 2026-08-24, after the last upload, so
no upload has ever actually used it. Step 3 tells you how to check and what to
paste if it did not work. Assume you may need to paste until it has worked once.

**Two things that look wrong and are not:**

- The version number goes up. That is the upload doing its job.
- **The two stores show different version numbers.** They always have. It is how
  the two portals work, not a mistake. ⛔ Never re-upload to make them match —
  that bumps again and makes the gap bigger.

---

## 3 · Check the store pages — and paste if you need to

Open both pages and read the **description**.

**Does it start with "Bug fixes for Surviving Mars: Relaunched." and run all the
way down to the modder section?**

### ✅ Yes — the automatic fill worked

Nothing to paste. **Tell the agent it worked** — that is the thing we are waiting
to find out. Go to step 4, unless you want the styling below.

### ❌ No — it is short, stale, or missing

The automatic fill did not work. Paste it by hand, from
`docs/agent/reports/STORE_CARD_LIVE.md`:

| store | the block to use |
|---|---|
| **Paradox Mods** | the one headed `═══ PARADOX MODS — plain text, paste as-is ═══` |
| **Steam Workshop** | the one headed `═══ STEAM WORKSHOP — BBCode ═══` |

Then **tell the agent it did not work**, and what the page showed instead.

Also check the change note is there, under **CHANGELOG** (Paradox) or
**Change Notes** (Steam). If it is missing, say so.

### Optional either way: make it pretty

Even when the automatic fill works, the page comes out as plain text — correct,
but no headings or bold. The two blocks above are the styled versions; paste one
and apply the headings with the editor buttons.

⚠️ Cosmetic only, and **it does not survive the next upload.** Skip it whenever
you like; the page is still correct without it.

---

## 4 · Publish the site

The site does **not** update when the agent commits. It only updates when you
run this:

1. Go to **github.com/catt144/SMR-CommunityMods**
2. **Actions** tab
3. **Publish docs site** in the left-hand list
4. **Run workflow** → **Run workflow**

Give it a minute, then check the fix list page shows the new entry.

---

## 5 · Tell the agent

Four things, and then you are done:

1. The **version number each store shows**.
2. **Whether the descriptions filled themselves**, or you had to paste. This is
   the one we do not know yet.
3. Anything else that **looked wrong** on either page.
4. Whether the **site published**.

The agent writes the rest down.

---

## If something goes wrong

| what you see | what to do |
|---|---|
| The mod editor asks to save before uploading | Stop. Tell the agent. Something changed that should not have. |
| An upload is rejected | Stop. Tell the agent what it said, word for word. |
| The description came out short | Paste it by hand (step 3), then tell the agent it did not fill itself. |
| You uploaded Steam before Paradox | Not fixable, and not worth chasing. Say so, carry on. |
