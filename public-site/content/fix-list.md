# Is my bug fixed?

!!! warning "LAYOUT SPECIMEN — three real entries out of 74"
    This page exists to test the format on the hardest cases, not to be the
    finished list. Building the real one is the `public-docs` chain's job.

**Use the search box** (or ++ctrl+k++) rather than scrolling — that is what it is
there for. Search the thing that went wrong: *"meteor"*, *"colonists suffocate"*,
*"train"*, *"drones stuck"*.

---

## Disasters

??? success "Sensor Towers made meteors MORE frequent instead of less"
    **What you saw:** you built Sensor Towers expecting fewer meteor strikes,
    and got more of them.

    **What was wrong:** the game applied the tower's bonus in the wrong
    direction.

    **After the fix:** towers reduce meteor frequency, the way the building's
    own description says they do.

??? success "A cave-in could fire on a map with disasters turned off"
    **What you saw:** you started a game with disasters disabled and a cave-in
    happened anyway.

    **What was wrong:** one disaster path did not check the map's disaster
    setting.

    **After the fix:** it checks. A no-disasters map stays a no-disasters map.

---

## Colonists

??? success "Colonists idled outdoors and suffocated after a life-support blip"
    **What you saw:** a brief life-support interruption, and then colonists
    standing outside dying instead of going indoors.

    **What was wrong:** colonists who were idle when the interruption cleared had
    no instruction to seek shelter.

    **After the fix:** they head for shelter.

---

!!! note "Format questions this specimen is meant to settle"
    - Do collapsed entries (click to expand) beat a flat list for 74 items?
    - Is *What you saw → What was wrong → After the fix* the right three beats?
      It leads with the player's experience rather than ours.
    - Are these the right categories, and how many should there be?
    - Should each entry link to anything deeper, or is this the bottom?
