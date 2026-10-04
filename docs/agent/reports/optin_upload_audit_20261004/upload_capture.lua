-- TEMPORARY owner-run capture; desk verified only. No API calls at installation.
-- Target: Opt-In only. Use the generated one-line paste and report instructions.
do
  local target = "SMR_CommunityOptInPack"
  local G, old_upload = _G, UploadMod
  local pdx_prepare, pdx_upload = PDX_PrepareForUpload, PDX_Upload
  local names = {
    "AsyncPdxGetModDetails", "AsyncPdxSetupModForPublish",
    "AsyncPdxUploadModAsset", "AsyncPdxUploadModContent",
    "AsyncPdxPublishMod", "AsyncPublishNewModVersion",
  }
  local pack = function(...) return {n = select("#", ...), ...} end
  local unpackn = function(t, first) return table.unpack(t, first or 1, t.n) end
  local function log(s) pcall(ModLog, "%s", "[PDXCAP] " .. s) end
  local function scalar(v, is_error)
    local t = type(v)
    if v == nil then return "nil" end
    if t == "boolean" or t == "number" then return tostring(v) end
    if t == "string" then
      if is_error then return string.format("%q", v) end
      return "string(bytes=" .. #v .. ")"
    end
    return t
  end
  local function describe(r, error_index)
    local s = "arity=" .. r.n
    for i = 1, r.n do s = s .. " r" .. i .. "=" .. scalar(r[i], i == error_index) end
    return s
  end
  local function check()
    if type(old_upload) ~= "function" or type(pdx_prepare) ~= "function"
      or type(pdx_upload) ~= "function" or type(ModLog) ~= "function"
      or type(table.unpack) ~= "function" then return false end
    for _, name in ipairs(names) do
      if type(G[name]) ~= "function" then return false end
    end
    return true
  end
  -- The setter/readback control catches a sandbox that accepts a shadow write.
  if not check() then log("NOT_READY globals-or-logger-unavailable"); return end
  local sentinel = function() end
  UploadMod = sentinel
  local global_write_ok = G.UploadMod == sentinel
  UploadMod = old_upload
  if not global_write_ok then log("NOT_READY global-write"); return end
  -- Local stub positive control: calls no native/network function.
  local nils = pack((function() return nil, false, nil end)())
  if nils.n ~= 3 or nils[2] ~= false then log("NOT_READY arity-control"); return end
  log("CONTROL " .. describe(nils))
  local wrapped
  wrapped = function(socket, mod, params, prepare_fn, upload_fn)
    if mod.id ~= target or prepare_fn ~= pdx_prepare or upload_fn ~= pdx_upload then
      return old_upload(socket, mod, params, prepare_fn, upload_fn)
    end
    -- Remove the outer hook as soon as its one target attempt is dispatched.
    if G.UploadMod == wrapped then UploadMod = old_upload end
    log("DISPATCH branch=" .. ((mod.PdxMod and mod.PdxMod.ModID or mod.pdx_id) and "update" or "create"))
    local prep = function(...)
      log("BEGIN prepare")
      local r = pack(prepare_fn(...))
      log("END prepare " .. describe(r))
      return unpackn(r)
    end
    local after_pack = function(...)
      -- This closure is an argument of the live thread; packaging reloads Lua.
      local saved, installed = {}, {}
      for _, name in ipairs(names) do
        if type(G[name]) ~= "function" then
          log("NOT_READY after-pack missing=" .. name)
          return upload_fn(...)
        end
        saved[name] = G[name]
      end
      local asset_index = 0
      for _, name in ipairs(names) do
        local native = saved[name]
        local hook = function(...)
          local stage = name
          if name == "AsyncPdxUploadModAsset" then
            asset_index = asset_index + 1
            stage = stage .. "#" .. asset_index
          end
          log("BEGIN " .. stage)
          local r = pack(native(...))
          log("END " .. stage .. " " .. describe(r, 1))
          return unpackn(r)
        end
        G[name], installed[name] = hook, hook
      end
      for _, name in ipairs(names) do
        if G[name] ~= installed[name] then
          for _, restore_name in ipairs(names) do
            if G[restore_name] == installed[restore_name] then G[restore_name] = saved[restore_name] end
          end
          log("NOT_READY after-pack hook-readback=" .. name)
          return upload_fn(...)
        end
      end
      log("READY after-pack stages")
      local r = pack(pcall(upload_fn, ...))
      for _, name in ipairs(names) do
        if G[name] == installed[name] then G[name] = saved[name] end
      end
      log("END upload " .. describe(r, not r[1] and 2 or nil) .. " restored=true")
      if not r[1] then error(r[2], 0) end
      return unpackn(r, 2)
    end
    return old_upload(socket, mod, params, prep, after_pack)
  end
  UploadMod = wrapped
  if G.UploadMod == wrapped then
    log("READY armed target=" .. scalar(target))
  else
    log("NOT_READY final-readback")
  end
end
