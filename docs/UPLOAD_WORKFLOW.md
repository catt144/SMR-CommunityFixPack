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

These upload by themselves. **You paste nothing:**

- the page description
- the short summary
- the title and tags
- the change note

**Two things that look wrong and are not:**

- The version number goes up. That is the upload doing its job.
- **The two stores show different version numbers.** They always have. It is how
  the two portals work, not a mistake. ⛔ Never re-upload to make them match —
  that bumps again and makes the gap bigger.

---

## 3 · Check the store pages

Open both pages and look at them.

- The description should be the full page text, not a short paragraph.
- The change note should be there, under **CHANGELOG** (Paradox) or
  **Change Notes** (Steam).

If the description looks short or stale, tell the agent — don't fix it by hand,
because the cause is in the mod and will happen again next time.

### Optional: make it pretty

The pages come out as plain text — correct, but no headings or bold. If you want
the styling, the formatted versions are in
`docs/agent/reports/STORE_CARD_LIVE.md`: one block for Paradox, one for Steam.
Paste and apply the headings with the editor buttons.

⚠️ This is cosmetic only, and **it does not survive the next upload.** Skip it
whenever you like; the page is still correct without it.

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

Three things, and then you are done:

1. The **version number each store shows**.
2. Anything that **looked wrong** on either page.
3. Whether the **site published**.

The agent writes the rest down.

---

## If something goes wrong

| what you see | what to do |
|---|---|
| The mod editor asks to save before uploading | Stop. Tell the agent. Something changed that should not have. |
| An upload is rejected | Stop. Tell the agent what it said, word for word. |
| The description came out short | Finish the upload, then tell the agent. Do not hand-fix it. |
| You uploaded Steam before Paradox | Not fixable, and not worth chasing. Say so, carry on. |
