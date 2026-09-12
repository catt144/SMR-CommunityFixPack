# PayloadTemplateRefill - one-module review

Agent `/root`, 2026-09-12, anchor `2983fac`. Recommendation only.

## Disagreements first

No material disagreement with the current fix-list row.

| module | entry | applies? | consumer still reads it? | row true? | bullet true? | verdict | evidence file:line on 1.1.0.403908 | basis | what I did NOT check |
|---|---|---|---|---|---|---|---|---|---|
| Fix_PayloadTemplateRefill.lua | F70 | yes: direct final registry line 246 active | yes: RetrieveRequests populates GetCargoList, consumed by Apply and transporter CmdLoad; confirmed first-use stamp gates later template reuse | yes: ordinary confirmed payload reuse honors zero; destination picks and tutorial are explicit exceptions | n/a: no headline; judgment-call description agrees | KEEP | 1.1.0.403908 Lua/CargoRequestNew.lua:120; 1.1.0.403908 Lua/CargoRequestNew.lua:174; 1.1.0.403908 Lua/CargoRequestNew.lua:191; 1.1.0.403908 Lua/CargoRequestNew.lua:215; 1.1.0.403908 Lua/CargoRequestNew.lua:221; 1.1.0.403908 Lua/CargoRequestNew.lua:226; 1.1.0.403908 Lua/CargoRequestNew.lua:240; 1.1.0.403908 Lua/CargoRequestNew.lua:321; 1.1.0.403908 Lua/CargoRequestNew.lua:371; 1.1.0.403908 Lua/CargoRequestNew.lua:379; 1.1.0.403908 Lua/UniversalRocket.lua:491; 1.1.0.403908 Lua/UniversalRocket.lua:577 | SOURCE | Organic 1.1.0 payload zero/refill, confirmation/cancel and destination-pick/tutorial controls; Current save/load/uninstall of payload flag and real-time blocked Apply thread; Current behavior probe firing and 1.0.7 runtime |

Primary root: `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`.

- Current RetrieveRequests :215 identifies destination picks; :217 ignores prior requests on that route. On ordinary reuse, :220 reads stored requested amount, but :221 treats zero as missing and :226 refills from the policy CargoTemplate returned at :191. The extra CmdLoad gate at :174 prevents only that command; it is not a persistent configured-payload test. No vanilla replacement performs the first-use distinction.

- Init :120 calls RetrieveRequests; SetRequest :240 writes cargo_items. GetCargoList :321 reads item.requested and scales resources :323, producing the cargo_list supplied by Apply :371 to CmdLoad :379. UniversalRocket :491 calls SetCargoRequest with the dialog; CmdUnload :577 resets requested amounts, keeping the later reopen path relevant. These are primary consumers, not a retired UI estimate.

- Code/Fix_PayloadTemplateRefill.lua:229 gates the template after its preserved tutorial branches and only outside destination picks. The confirmed Apply path stamps SMRFixPack_payload_set at :247; cancellation :256 does not. The 1.1.0 asynchronous prompt, midflight policy updates and CmdLoad dispatch remain intact. Current F70 already records the hotfix-2 recopy and destination-pick exception.

- Site fix-list.md:437 and :445 describe intentional zeroes and first-use defaults. Read within ordinary payload reuse, the row remains true; destination picks intentionally obtain new suggestions. This is one of the three explicitly labelled judgment-call rows. No matching card headline exists.

Registry archive `docs/archive/logs/stillneeded_registry_Mars.exe-20260912-00.29.01-6a91a190.log:246` measures active. Installation is not cure verification.

Not checked:

- Organic 1.1.0 payload zero/refill, confirmation/cancel and destination-pick/tutorial controls
- Current save/load/uninstall of payload flag and real-time blocked Apply thread
- Current behavior probe firing and 1.0.7 runtime
