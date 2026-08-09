local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local coreModule = ReplicatedStorage:WaitForChild("ASMRCore", 10)
if not coreModule then
	warn("[ASMR] 'ASMRCore' ModuleScript missing from ReplicatedStorage.")
	return { Register = function() end }
end
local Core = require(coreModule)

local Defaults = {
	DentFalloff = 2, DentOvershoot = 0, CrackSpread = 0,
	SinkSpeed = 10, RiseSpeed = 2,
	StepSpeedMin = 4, StepGap = 0.28,
	VolumeJitter = 0.08, Pitch = 1, PitchJitter = 0.06,
	MaxConcurrent = 6, RollOffMin = 10, RollOffMax = 70,
}

local CrustNames = { "Shell" }

local Deformable = {}
local RestX, RestY, RestZ = "_RestX", "_RestY", "_RestZ"

local Sink = { Claimed = false, Alpha = 0, Hum = nil, Base = nil, Tracked = nil, Holding = false }

local function claimSink(hum, alpha)
	if not hum then return end
	Sink.Hum = hum
	if not Sink.Claimed or alpha < Sink.Alpha then Sink.Alpha = alpha end
	Sink.Claimed = true
end

RunService.Heartbeat:Connect(function()
	local hum = Sink.Hum
	if not (hum and hum.Parent and hum.Health > 0) then
		Sink.Claimed, Sink.Alpha, Sink.Holding = false, 0, false
		return
	end
	if Sink.Tracked ~= hum then
		Sink.Tracked, Sink.Base = hum, hum.HipHeight
	end
	if Sink.Claimed then
		hum.HipHeight = Sink.Base + Sink.Alpha
		Sink.Holding = true
	elseif Sink.Holding then
		hum.HipHeight = Sink.Base
		Sink.Holding = false
	end
	Sink.Claimed, Sink.Alpha = false, 0
end)

local function dentAt(cfg, boneXZ, playerXZ)
	if not playerXZ then return 0 end
	local d = (boneXZ - playerXZ).Magnitude
	if d >= cfg.DentRadius then return 0 end
	local t = 1 - (d / cfg.DentRadius)
	return -cfg.DentDepth * (t ^ cfg.DentFalloff)
end

local function spreadAt(cfg, boneXZ, playerXZ)
	if cfg.CrackSpread <= 0 or not playerXZ then return Vector2.zero end
	local offset = boneXZ - playerXZ
	local d = offset.Magnitude
	if d < 0.05 or d >= cfg.DentRadius then return Vector2.zero end
	local t = d / cfg.DentRadius
	return offset.Unit * (cfg.CrackSpread * 4 * t * (1 - t))
end

local function updateBones(s, cfg, dt, playerXZ)
	local overshoot = cfg.DentOvershoot
	local spreads = cfg.CrackSpread > 0
	local moving = false

	for _, bone in ipairs(s.Bones) do
		if bone.Parent then
			local boneXZ = s.BoneWorld[bone]
			local target = dentAt(cfg, boneXZ, playerXZ)
			local cur = s.BoneY[bone]
			local nxt

			if overshoot > 0 and target > cur then
				local vel = s.BoneVel[bone]
				local k = cfg.DentReleaseSpeed * 6
				vel += ((target - cur) * k - vel * (2 * math.sqrt(k) * (1 - overshoot))) * dt
				nxt = cur + vel * dt
				s.BoneVel[bone] = vel
			else
				local rate = (target < cur) and cfg.DentPressSpeed or cfg.DentReleaseSpeed
				nxt = cur + (target - cur) * math.min(1, rate * dt)
				s.BoneVel[bone] = 0
			end
			if math.abs(nxt) < 0.002 and math.abs(target) < 0.002 then nxt = 0 end

			local prevOff = s.BoneOff[bone]
			local off = prevOff
			if spreads then
				local w = spreadAt(cfg, boneXZ, playerXZ)
				local want = Vector2.zero
				if w.Magnitude > 0 then
					local v = s.Surface.CFrame:VectorToObjectSpace(Vector3.new(w.X, 0, w.Y))
					want = Vector2.new(v.X, v.Z)
				end
				local rate = (want.Magnitude > off.Magnitude) and cfg.DentPressSpeed or cfg.DentReleaseSpeed
				off = off + (want - off) * math.min(1, rate * dt)
				if off.Magnitude < 0.002 then off = Vector2.zero end
			end

			if nxt ~= cur or off ~= prevOff then
				bone.Position = Vector3.new(
					(bone:GetAttribute(RestX) or 0) + off.X,
					(bone:GetAttribute(RestY) or 0) + nxt,
					(bone:GetAttribute(RestZ) or 0) + off.Y
				)
			end

			s.BoneY[bone], s.BoneOff[bone] = nxt, off
			if nxt ~= 0 or off ~= Vector2.zero then moving = true end
		end
	end
	return moving
end

local function sampleDent(s, xz)
	local b1, b2, b3, b4
	local d1, d2, d3, d4 = math.huge, math.huge, math.huge, math.huge
	for _, bone in ipairs(s.SinkBones) do
		local d = (s.BoneWorld[bone] - xz).Magnitude
		if d < d1 then
			b4, d4 = b3, d3; b3, d3 = b2, d2; b2, d2 = b1, d1; b1, d1 = bone, d
		elseif d < d2 then
			b4, d4 = b3, d3; b3, d3 = b2, d2; b2, d2 = bone, d
		elseif d < d3 then
			b4, d4 = b3, d3; b3, d3 = bone, d
		elseif d < d4 then
			b4, d4 = bone, d
		end
	end
	local sum, wsum = 0, 0
	for _, p in ipairs({ {b1,d1}, {b2,d2}, {b3,d3}, {b4,d4} }) do
		if p[1] then
			local w = 1 / math.max(p[2], 0.05)
			sum += s.BoneY[p[1]] * w
			wsum += w
		end
	end
	return wsum == 0 and 0 or sum / wsum
end

function Deformable.Register(typeName, cfg)
	for k, v in pairs(Defaults) do
		if cfg[k] == nil then cfg[k] = v end
	end
	local soundName = cfg.SoundName or typeName

	Core.RegisterHandler({
		Type = typeName,
		Requirements = "Needs a MeshPart named 'Surface' containing Bones.",

		Resolve = function(obj)
			local model = obj.Model
			local surface = model:FindFirstChild("Surface", true)
			if not (surface and surface:IsA("MeshPart")) then return false end

			local meshes = { surface }
			for _, n in ipairs(CrustNames) do
				local extra = model:FindFirstChild(n, true)
				if extra and extra:IsA("MeshPart") then table.insert(meshes, extra) end
			end

			local bones, sinkBones = {}, {}
			for i, mesh in ipairs(meshes) do
				for _, d in ipairs(mesh:GetDescendants()) do
					if d:IsA("Bone") and d.Name ~= "Root" then
						table.insert(bones, d)
						if i == 1 then table.insert(sinkBones, d) end
					end
				end
			end
			if #sinkBones == 0 then return false end

			local s = obj.State
			s.Surface, s.Bones, s.SinkBones = surface, bones, sinkBones
			s.BoneY, s.BoneVel, s.BoneOff, s.BoneWorld = {}, {}, {}, {}

			for _, bone in ipairs(bones) do
				if bone:GetAttribute(RestY) == nil then
					local p = bone.Position
					bone:SetAttribute(RestX, p.X)
					bone:SetAttribute(RestY, p.Y)
					bone:SetAttribute(RestZ, p.Z)
				end
				s.BoneY[bone], s.BoneVel[bone], s.BoneOff[bone] = 0, 0, Vector2.zero
				local wp = bone.WorldPosition
				s.BoneWorld[bone] = Vector2.new(wp.X, wp.Z)
			end

			s.SinkAlpha, s.LastStep = 0, 0
			s.Inside, s.WasInside, s.Settled = false, false, true
			obj.Root = surface

			local hitbox = model:FindFirstChild("Hitbox")
			if hitbox and hitbox:IsA("BasePart") then
				obj.TriggerCF, obj.TriggerSize = hitbox.CFrame, hitbox.Size
			else
				local sz = surface.Size
				local h = 5 + cfg.DentDepth
				obj.TriggerCF = surface.CFrame * CFrame.new(0, sz.Y / 2 + h / 2 - cfg.DentDepth - 0.5, 0)
				obj.TriggerSize = Vector3.new(sz.X * 0.98, h, sz.Z * 0.98)
			end
			return true
		end,

		Reset = function(obj)
			local s = obj.State
			if not s.Bones then return end
			for _, bone in ipairs(s.Bones) do
				if bone.Parent then
					s.BoneY[bone], s.BoneVel[bone], s.BoneOff[bone] = 0, 0, Vector2.zero
					bone.Position = Vector3.new(
						bone:GetAttribute(RestX) or 0,
						bone:GetAttribute(RestY) or 0,
						bone:GetAttribute(RestZ) or 0
					)
				end
			end
			s.SinkAlpha = 0
			s.Inside, s.WasInside, s.Settled = false, false, true
		end,

		Cleanup = function(obj)
			obj.State.Inside, obj.State.WasInside = false, false
		end,

		Update = function(obj, dt, core, char, hum)
			local s = obj.State
			if not s.Bones then return end

			local hrp = char:FindFirstChild("HumanoidRootPart")
			s.WasInside = s.Inside
			s.Inside = obj.Occupied and hrp ~= nil

			if s.Settled and not s.Inside and not s.WasInside then return end

			local playerXZ = s.Inside and Vector2.new(hrp.Position.X, hrp.Position.Z) or nil
			local moving = updateBones(s, cfg, dt, playerXZ)

			if s.Inside then
				local target = sampleDent(s, playerXZ)
				local rate = (target < s.SinkAlpha) and cfg.SinkSpeed or cfg.RiseSpeed
				s.SinkAlpha += (target - s.SinkAlpha) * math.min(1, rate * dt)
				claimSink(hum, s.SinkAlpha)
			elseif s.SinkAlpha ~= 0 then
				s.SinkAlpha += (0 - s.SinkAlpha) * math.min(1, cfg.RiseSpeed * dt)
				if math.abs(s.SinkAlpha) < 0.01 then s.SinkAlpha = 0 else claimSink(hum, s.SinkAlpha) end
			end

			s.Settled = (not moving) and s.SinkAlpha == 0

			if s.Inside and not s.WasInside then
				Core.PlaySound(soundName, s.Surface, cfg, "Enter")
			elseif s.WasInside and not s.Inside then
				Core.PlaySound(soundName, s.Surface, cfg, "Exit")
			end

			if s.Inside then
				local v = hrp.AssemblyLinearVelocity
				local now = os.clock()
				if Vector2.new(v.X, v.Z).Magnitude > cfg.StepSpeedMin and (now - s.LastStep) > cfg.StepGap then
					s.LastStep = now
					Core.PlaySound(soundName, s.Surface, cfg, "Step")
				end
			end
		end,
	})
end

return Deformable
