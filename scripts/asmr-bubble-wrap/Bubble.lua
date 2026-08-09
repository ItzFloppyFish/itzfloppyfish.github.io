local BubbleType = "Bubble" -- Must match the ASMRType attribute on your bubble models.
local SoundName = "Pop" -- Change to whatever your Sound is called.
local Config = {
	RespawnTime  = 3, -- The time between the bubble being popped and returning to default.
	PoppedHeight = 0.15, -- The deflated bubble height (0.15 = 15% of original, lower = flatter)
	Volume       = 1, -- Pop sound volume
	Pitch        = 1, -- Pop sound pitch
}
Config.SquashTime = 0.05 -- How fast the bubble flattens when popped (seconds).
Config.PoppedWidth = 1.25 -- How much the bubble bulges outwards as it flattens (1.25 = 25% wider).
Config.PoppedSink = 0.5 -- How the flat bubble sits on the ground (0.5 = flush, lower = floats, higher = sinks in).
Config.Cooldown = 0.12 -- Minimum time between pops, stops one step popping a whole row (seconds).
Config.RegrowTime = 0.35 -- How long the bubble takes to re-inflate (seconds).
Config.RegrowEasing = Enum.EasingStyle.Back -- The re-inflate motion. Back = slight overshoot so it looks like it's inflating.
Config.VolumeJitter = 0.12 -- Random volume variation per pop, so repeats don't sound identical.
Config.PitchJitter = 0.22 -- Random pitch variation per pop, so repeats don't sound identical.
Config.RollOffMin = 6 -- Distance (studs) the pop stays full volume before it starts fading.
Config.RollOffMax = 45 -- Distance (studs) at which the pop can no longer be heard.
Config.MaxConcurrent = 14 -- Max pop sounds playing at once, stops audio overload on big sheets.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService      = game:GetService("TweenService")
local coreModule = ReplicatedStorage:WaitForChild("ASMRCore", 10)
if not coreModule then
	warn("[ASMR] 'ASMRCore' ModuleScript not found in ReplicatedStorage - this pack does nothing without it.")
	return
end
local Core = require(coreModule)
local SquashInfo = TweenInfo.new(Config.SquashTime, Enum.EasingStyle.Quart, Enum.EasingDirection.Out)
local RegrowInfo = TweenInfo.new(Config.RegrowTime, Config.RegrowEasing, Enum.EasingDirection.Out)
local function pop(obj, animate)
	local s = obj.State
	if s.popped then return end
	s.popped = true
	s.poppedAt = os.clock()
	Core.PlaySound(SoundName, obj.Root, Config)
	for _, p in ipairs(s.parts) do
		if not p.Parent then continue end
		local b = s.baseSize[p]
		local base = s.baseCFrame[p]
		local flat = Vector3.new(b.X * Config.PoppedWidth, b.Y * Config.PoppedHeight, b.Z * Config.PoppedWidth)
		local drop = (b.Y - flat.Y) * Config.PoppedSink
		local target = base * CFrame.new(0, -drop, 0)
		if animate then
			TweenService:Create(p, SquashInfo, { Size = flat, CFrame = target }):Play()
		else
			p.Size = flat
			p.CFrame = target
		end
	end
end
local function regrow(obj, animate)
	local s = obj.State
	if not s.popped then return end
	s.popped = false
	s.poppedAt = nil
	for _, p in ipairs(s.parts) do
		if not p.Parent then continue end
		if animate then
			TweenService:Create(p, RegrowInfo, { Size = s.baseSize[p], CFrame = s.baseCFrame[p] }):Play()
		else
			p.Size = s.baseSize[p]
			p.CFrame = s.baseCFrame[p]
		end
	end
end
Core.RegisterHandler({
	Type = BubbleType,
	Requirements = "Bubbles need at least one BasePart inside the Model.",
	Resolve = function(obj)
		local model = obj.Model
		local root = model:FindFirstChildWhichIsA("BasePart", true)
		if not root then return false end
		local s = obj.State
		s.parts, s.baseSize, s.baseCFrame = {}, {}, {}
		for _, d in ipairs(model:GetDescendants()) do
			if d:IsA("BasePart") then
				table.insert(s.parts, d)
				s.baseSize[d] = d.Size
				s.baseCFrame[d] = d.CFrame
			end
		end
		s.popped = false
		s.poppedAt = nil
		obj.Root = root
		local ext = model:GetExtentsSize()
		local h = 1.6
		obj.TriggerCF = root.CFrame * CFrame.new(0, h * 0.35, 0)
		obj.TriggerSize = Vector3.new(ext.X * 0.95, h, ext.Z * 0.95)
		return true
	end,
	Update = function(obj, dt)
		local s = obj.State
		local now = os.clock()
		if s.popped then
			if now - s.poppedAt >= Config.RespawnTime then
				regrow(obj, true)
			end
			return
		end
		if obj.Occupied and (now - obj.LastTrigger) >= Config.Cooldown then
			obj.LastTrigger = now
			pop(obj, true)
		end
	end,
	Reset = function(obj)
		if obj.State.popped then regrow(obj, false) end
	end,
})
