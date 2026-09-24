--Game version 1.1.0.403908 needed a complete rewrite of the mod and was the end of ChoGGi´s original code of the mod

print("[Passage Network] Mod active")
print("[Passage Network] Mod version 1.38")

--Modify workplace and UI for modded behavior

function Dome:GetClusterDomes()
    return self.dome_network
end

function Dome:IsInClusterWith(other)
    return other == self or self.dome_network and self.dome_network[other] ~= nil
end



--make services share with the whole dome_network instead of just the connected_domes

--Check if ReassignServices was changed from what the mod was designed for and notify if it was

local function ToHex(str)
    local result = {}
    for i = 1, #str do
        result[i] = string.format("%02x", string.byte(str, i))
    end
    return table.concat(result)
end

local VANILLA_REASSIGN_SERVICES_HASH = "281802b04005f448b6641cfa23d91070cf3dc28453ac73a5a240a03d3ed7837e"

local VanillaReassignServices = ReassignServices

local actual_hash = ToHex(SHA256(string.dump(VanillaReassignServices)))

if actual_hash ~= VANILLA_REASSIGN_SERVICES_HASH then
    print("[Passage Network] WARNING: Unknown/Unsupported Vanilla ReassignServices!")
    print("[Passage Network] Mod may not work. Use at your own risk!")
	print("[Passage Network] Old vanilla hash: " .. VANILLA_REASSIGN_SERVICES_HASH .. " was the hash for 1.1.0.403908")
	print("[Passage Network] Current vanilla hash: " .. actual_hash)
end



function Dome()
	return self.dome_network
end

function Dome(other)
	return other == self or self.dome_network and self.dome_network[other] ~= nil
end


function ReassignServices(dome)
    --print("[Passage Network] Moded ReassignServices called")

    local network = dome and dome.dome_network

    if not network or #network <= 1 then
        return VanillaReassignServices(dome)
    end

    local original_connected = {}

    -- Create a connected_domes list for every dome with that dome itself guaranteed to be at index 1.
    for i = 1, #network do
        local d = network[i]

        original_connected[d] = d.connected_domes

        local list = { d }

        for j = 1, #network do
            local other = network[j]
            if other ~= d then
                list[#list + 1] = other
            end
        end

        d.connected_domes = list
    end

    local ok, err = pcall(VanillaReassignServices, dome)

    -- Restore the real passage connections.
    for i = 1, #network do
        local d = network[i]
        d.connected_domes = original_connected[d]
    end

    if not ok then
        error(err)
    end
end

