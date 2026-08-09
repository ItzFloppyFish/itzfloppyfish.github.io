local Core = {}
local SoundFolderName = "ASMRSounds" -- Change to whatever your ASMRSounds folder is called.
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")
local handlers, objects, unclaimed = {}, {}, {}
local cullDistance = 120 -- This helps with performance, but may need to be tuned for your game
local soundList, liveCount, pool = {}, {}, {}
local rng = Random.new()

task.spawn(function()
	local folder = ReplicatedStorage:WaitForChild(SoundFolderName, 20)
	if not folder then
		warn(("[ASMR] ReplicatedStorage.%s folder not found - sounds disabled."):format(SoundFolderName))
		return
	end
	local function add(s)
		if s:IsA("Sound") and s.SoundId ~= "" then table.insert(soundList, s) end
	end
	for _, s in ipairs(folder:GetChildren()) do add(s) end
	folder.ChildAdded:Connect(add)
end)

local function withPrefix(prefix)
	local out = {}
	for _, s in ipairs(soundList) do
		if string.sub(s.Name, 1, #prefix) == prefix then table.insert(out, s) end
	end
	return out
end

function Core.PlaySound(category, parent, cfg, subset)
	if #soundList == 0 or not parent or not parent.Parent then return end
	local n = liveCount[category] or 0
	if n >= (cfg.MaxConcurrent or 6) then return end

	local candidates
	if subset then
		candidates = withPrefix(category .. subset)
		if #candidates == 0 then candidates = withPrefix(category) end
	else
		candidates = withPrefix(category)
	end
	if #candidates == 0 then return end

	local snd = table.remove(pool)
	if not snd then
		snd = Instance.new("Sound")
		snd.Name = "ASMRSound"
	end
	snd.SoundId            = candidates[rng:NextInteger(1, #candidates)].SoundId
	snd.Volume             = math.max(0, (cfg.Volume or 1) + rng:NextNumber(-(cfg.VolumeJitter or 0), cfg.VolumeJitter or 0))
	snd.PlaybackSpeed      = math.max(0.1, (cfg.Pitch or 1) + rng:NextNumber(-(cfg.PitchJitter or 0), cfg.PitchJitter or 0))
	snd.RollOffMode        = Enum.RollOffMode.InverseTapered
	snd.RollOffMinDistance = cfg.RollOffMin or 8
	snd.RollOffMaxDistance = cfg.RollOffMax or 50
	snd.Parent             = parent
	liveCount[category] = n + 1

	local done = false
	local conn
	local function cleanup()
		if done then return end
		done = true
		if conn then conn:Disconnect() end
		liveCount[category] = math.max(0, (liveCount[category] or 1) - 1)
		snd:Stop()
		snd.SoundId = ""
		snd.Parent = nil
		if #pool < 48 then table.insert(pool, snd) else snd:Destroy() end
	end
	conn = snd.Ended:Connect(cleanup)
	snd:Play()
	task.delay(6, cleanup)
end

local character, humanoid
local contactParts = {}
local ContactNames = { LeftFoot = true, RightFoot = true, ["Left Leg"] = true, ["Right Leg"] = true, HumanoidRootPart = true }

local function bind(char)
	character = char
	humanoid = nil
	table.clear(contactParts)
	for _, c in ipairs(char:GetChildren()) do
		if ContactNames[c.Name] and c:IsA("BasePart") then table.insert(contactParts, c) end
	end
	char.ChildAdded:Connect(function(c)
		if character == char and ContactNames[c.Name] and c:IsA("BasePart") then
			table.insert(contactParts, c)
		end
	end)
	task.spawn(function()
		local hum = char:WaitForChild("Humanoid", 10)
		if character ~= char or not hum then return end
		humanoid = hum
		hum.Died:Once(function()
			for _, obj in pairs(objects) do
				if obj.Handler.Cleanup then obj.Handler.Cleanup(obj, hum) end
				if obj.Resolved and obj.Handler.Reset then obj.Handler.Reset(obj) end
			end
			if character == char then character, humanoid = nil, nil end
		end)
	end)
end

local player = Players.LocalPlayer
if player.Character then bind(player.Character) end
player.CharacterAdded:Connect(bind)

local function consider(inst)
	if not inst:IsA("Model") then return end
	local t = inst:GetAttribute("ASMRType")
	if type(t) ~= "string" or objects[inst] then return end
	local h = handlers[t]
	if not h then
		unclaimed[inst] = t
		return
	end
	unclaimed[inst] = nil
	objects[inst] = {
		Model = inst, Type = t, Handler = h, State = {},
		Resolved = false, Active = false, Occupied = false,
		NextResolve = 0, ResolveDeadline = os.clock() + 15,
		Warned = false, LastTrigger = 0,
	}
end

for _, d in ipairs(Workspace:GetDescendants()) do consider(d) end
Workspace.DescendantAdded:Connect(consider)
Workspace.DescendantRemoving:Connect(function(d)
	local obj = objects[d]
	if obj then
		if obj.Handler.Cleanup then obj.Handler.Cleanup(obj, humanoid) end
		objects[d] = nil
	end
	unclaimed[d] = nil
end)

function Core.RegisterHandler(handler)
	if handlers[handler.Type] then return end
	handlers[handler.Type] = handler
	for model, t in pairs(unclaimed) do
		if t == handler.Type then consider(model) end
	end
end

local overlap = OverlapParams.new()
overlap.FilterType = Enum.RaycastFilterType.Include
overlap.MaxParts = 4

local function deactivate(obj)
	if not obj.Active then return end
	obj.Active = false
	obj.Occupied = false
	if obj.Handler.Cleanup then obj.Handler.Cleanup(obj, humanoid) end
	if obj.Resolved and obj.Handler.Reset then obj.Handler.Reset(obj) end
end

RunService.Heartbeat:Connect(function(dt)
	if not (character and humanoid and humanoid.Health > 0) then return end
	local hrp = character:FindFirstChild("HumanoidRootPart")
	if not hrp or #contactParts == 0 then return end

	local origin = hrp.Position
	overlap.FilterDescendantsInstances = contactParts
	local now = os.clock()
	local cull2 = cullDistance * cullDistance

	for model, obj in pairs(objects) do
		local root = obj.Root
		if not (root and root.Parent) then
			deactivate(obj)
			obj.Resolved = false
			if now >= obj.NextResolve then
				obj.NextResolve = now + 0.5
				if obj.Handler.Resolve(obj, Core) then
					obj.Resolved = true
				elseif not obj.Warned and now > obj.ResolveDeadline then
					obj.Warned = true
					warn(("[ASMR] '%s' (%s) hasn't set up after 15s. %s"):format(model:GetFullName(), obj.Type, obj.Handler.Requirements or ""))
				end
			end
			if not obj.Resolved then continue end
			root = obj.Root
		end

		local delta = root.Position - origin
		if delta:Dot(delta) > cull2 then
			deactivate(obj)
			continue
		end

		obj.Active = true
		local parts = Workspace:GetPartBoundsInBox(obj.TriggerCF, obj.TriggerSize, overlap)
		obj.Occupied = #parts > 0
		obj.Handler.Update(obj, dt, Core, character, humanoid)
	end
end)

return Core
