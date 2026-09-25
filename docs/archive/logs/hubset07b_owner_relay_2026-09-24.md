# hubset 07B owner relay (verbatim, in order)
- Pre-sitting: the owner ran segment A before the attending session's pre-sitting checks. Checked afterwards: junction on the main tree; fixture sha256 036e130d... equal to the saves/reporters backup; no new save written; hubset clean at 7f6e6bf; TestKit 4fd0275 slots loaded (SLOTS sitting=hubset07b).
- A (main), log Mars.exe-20260924-20.49.43-6aad2d75.log: owner sent a screenshot (hubset07b_A_slot2_owner.jpg: Caroline Amaury I, Brussels, "Going to work", Colonist(2000011092)) and said "Done".
  Scratch id=32 build=main, six absent, c114_hubs=4, c111_subjects=16.
  Slot 1 REFUSED "pause first" (id=33): C111 not read in A; 07 holds the main baseline.
  C114 id=54: subject 2000011092 on PassageHub(2692), exposed=true, booked=true ended=ready_for_pickup, verdict=HELD (defect reproduced).
  C117 id=79: Passage(2694), at_drain=68, hub_bound=43, hub_bound_unmarked=43, verdict=HELD (defect reproduced); entry NOT_SAMPLED by design. Screenshots SMRTK_0077, 0078.
- Between segments: owner "on desktop". Segment A log archived; junction -> B:\Dev\SMR\SMR-BugFixPack-hubset, read back.
- B (hubset), log Mars.exe-20260924-20.54.42-6aad2d75.log: six modules `applied`; Scratch id=32 build=hubset, six active, c114_hubs=4.
  Owner sent a screenshot (hubset07b_B_slot1_owner.jpg: Bogdan Bojidarov, Residence blank, Status "Returning to Dome: Brussels") and said "Done I fired on out of order though".
  Order in the log: 2 (pause id=44), 4 (busy pause id=56), 3 (fire id=65: subject 2000015083 still exposed=true at fire, id=62), 4 again (id=79), 5 (id=88).
  C111 id=35: text "Returning to Dome: Brussels", returning=true, emigration_dome=false, dreaming=false; the slot's verdict reads NOT_SAMPLED because the Untranslated text carries no T id (judge defect); the fields meet the prediction.
  C114 id=68: subject 2000015083 (Zenith Hubble) on PassageHub(2692), exposed=true, booked=false ended=safe in DomeMedium(3911), verdict=HELD. Auto-screenshot SMRTK_0079 shows it selected: Unemployed, "Visiting Amusement Park".
  C117 id=93: Passage(2694), at_drain=69, hub_bound=37, hub_bound_unmarked=0, verdict=HELD; entered_after=0, entry_verdict=HELD. Auto-screenshot SMRTK_0080 still shows the C114 subject (selection did not change before capture).
- After: owner "Done" (quit). Segment B log archived; junction -> B:\Dev\SMR\SMR-BugFixPack, read back; fixture sha256 036e130d... unchanged; no save written (account.dat, steam_autocloud.vdf touched by the boots).
