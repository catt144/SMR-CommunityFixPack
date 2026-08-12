-- F102: visiting an asteroid that carries subsurface Exotic Minerals deposits
-- hard-freezes the game on some systems (witnessed: Linux/Proton on NVIDIA
-- proprietary drivers — Steam forum, May 31 2026; still being hit as of
-- Aug 2026). The community's "Hotfix 1.0.7 asteroid freeze" mod (PDX 154761)
-- stops the freeze by swapping every subsurface PreciousMinerals deposit to
-- PreciousMetals at PlaceDeposit time — proof the trigger is the deposit
-- OBJECT, at the cost of removing subsurface Exotic Minerals from asteroids
-- entirely.
--
-- What actually differs about that object: `SubsurfaceDepositPreciousMinerals`
-- (Lua\Buildings\SubsurfaceDeposit.lua:496-507) has NO unique logic — its only
-- unique surface is its sign entity, `SignPreciousMineralsDeposit`, whose
-- shipped material (Materials.fpk: SignPreciousMineralsDeposit_mesh.sub_0.mtljson)
-- is the game's only sign with a `VertexNoise: "noiseTree"` vertex-animation
-- flag (7 of 2,455 materials carry VertexNoise; the other six are crops and a
-- rover part) and is a visible hand-edit: it points the old B&B sign at
-- remaster-era textures ("ResourceRareMinerals_BC.dds", used by nothing else;
-- an "...EM - Copy.dds" emissive). Meanwhile the remaster's own clean sign for
-- this resource, `SignRareMineralsDeposit`, ships fully (mesh + clean material
-- + entities.dat record) and is referenced NOWHERE — an orphaned asset.
--
-- The fix: point the class at the clean orphaned sign. Gameplay is untouched —
-- the deposit stays PreciousMinerals, extractable, correct UI/amounts; only
-- the billboard art changes. FIX_POLICY §1.1 (data patch on a class default,
-- written pre-flattening so ClassesBuilt bakes it), plus a LoadGame sweep that
-- converges already-placed deposits on the classdef the same way vanilla does
-- when a deep-exploitability const flips (SubsurfaceDeposit.lua:471-483 —
-- AllMapsForEach + UpdateEntity). Deposits placed after load (asteroid map
-- generation) take the classdef path via GameInit → UpdateEntity and need no
-- sweep. `disabled_entity` (SignUnexploitablePreciousMinerals) is deliberately
-- left vanilla: its material is clean, and §4 does not license touching what
-- no evidence implicates.
--
-- §3a layer statement: Layer 3. Data only — no wrapped bodies, no game-time
-- threads, no blocking calls; the one OnMsg.LoadGame handler is synchronous,
-- stores nothing, and OnMsg registrations are not persisted. Uninstall: the
-- class default reverts to vanilla with the mod gone, and whichever entity
-- name a save carries, BOTH sign entities ship in the vanilla packs
-- (entities.dat records verified this session), so a save made with the fix
-- loads clean without it. Nothing of ours enters the save.
--
-- ⚠️ VERIFICATION BOUNDARY (owner decision 2026-08-12 — ship with disclaimer):
-- the freeze does not reproduce on either of our machines (Windows/RTX 4080
-- and Steam Deck/RADV both ran a 3-deposit D-type clean, logs clean), so the
-- CURE is unverified — only an affected player (Linux + NVIDIA witnessed
-- class) can confirm it. What is verified locally: the retarget is safe — the
-- replacement entity is registered, gameplay identity is class-keyed (nothing
-- in Src keys on the deposit's entity string), and failure to cure leaves
-- players exactly where vanilla left them, minus one broken material on
-- screen. Mechanism attribution (VertexNoise shader permutation) is a
-- HYPOTHESIS; if an affected player reports the freeze survives this fix, the
-- defect is below Lua's reach and F102 records the community swap as the only
-- remaining lever.

SMRFixPack.Register("ExoticDepositSign", {
	title = "Subsurface Exotic Minerals deposits use the remaster's own sign — believed to stop the asteroid-visit freeze reported on Linux/NVIDIA systems",
	apply = function()
		local err = SMRFixPack.Require("ExoticDepositSign", {
			{ global = "IsValidEntity" },
			{ class = "SubsurfaceDepositPreciousMinerals" },
			{ test = function()
					local C = rawget(_G, "SubsurfaceDepositPreciousMinerals")
					return type(C) == "table"
						and rawget(C, "entity") == "SignPreciousMineralsDeposit"
				end,
				reason = "SubsurfaceDepositPreciousMinerals.entity is not the shipped sign (game update rewired it?)" },
			{ test = function() return IsValidEntity("SignRareMineralsDeposit") end,
				reason = "replacement entity SignRareMineralsDeposit is not registered in this build" },
		})
		if err then return err end

		SubsurfaceDepositPreciousMinerals.entity = "SignRareMineralsDeposit"
		if rawget(SubsurfaceDepositPreciousMinerals, "entity") ~= "SignRareMineralsDeposit" then
			return "class-default entity write did not land"
		end
	end,
})

-- Already-placed deposits (saves that visited an asteroid before the fix, or
-- were written mid-visit) may carry the old sign; converge them on the
-- classdef. UpdateEntity is vanilla's own method for exactly this, and the
-- sweep is idempotent — on a deposit already showing the right sign,
-- ChangeEntity to the same entity is a no-op.
OnMsg.LoadGame = SMRFixPack.WhenActive("ExoticDepositSign", function()
	local for_each = rawget(_G, "AllMapsForEach")
	if type(for_each) ~= "function" then return end
	local n = 0
	for_each("map", "SubsurfaceDepositPreciousMinerals", function(obj)
		n = n + 1
		obj:UpdateEntity()
	end)
	if n > 0 then
		SMRFixPack.Log("ExoticDepositSign: %d Exotic Minerals deposit(s) re-signed onto the clean entity", n)
	end
end)
