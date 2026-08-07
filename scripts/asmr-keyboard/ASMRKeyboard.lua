local RunService = game:GetService("RunService")
local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local Debris = game:GetService("Debris")
local Player = Players.LocalPlayer
local KeyName = "Key" -- The name of all the parts that will be treated as keys.
local DropDistance = 0.9 -- This is how far down your key drops down when its stood on.
local TweenTime = 0.2 -- How quickly a key returns to default.
local Detection = Vector3.new(0, 4, 0)
local SoundId = "rbxassetid://113108830240353" -- The sound that plays when a key is stood on.
local tweenInfo = TweenInfo.new(TweenTime, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
local keyData = {}
local function getRootPart(inst)
	if inst:IsA("Model") then return inst.PrimaryPart
	elseif inst:IsA("BasePart") then return inst end
	return nil
end
local function registerKey(inst)
	if keyData[inst] then return end
	if inst.Name ~= KeyName then return end
	local isModel = inst:IsA("Model")
	if not (isModel or inst:IsA("BasePart")) then return end
	local root = getRootPart(inst)
	if not root then return end
	local origin = isModel and inst:GetPivot() or root.CFrame
	local data = { origin = origin, isModel = isModel, pressed = false, tween = nil, proxy = nil }
	if isModel then
		local proxy = Instance.new("CFrameValue")
		proxy.Value = origin
		proxy.Changed:Connect(function(cf)
			if inst.Parent then inst:PivotTo(cf) end
		end)
		data.proxy = proxy
	end
	keyData[inst] = data
end
local function targetCFrame(data, pressed)
	if not pressed then return data.origin end
	return data.origin + (-data.origin.UpVector * DropDistance)
end
local function playSound(root)
	local sound = Instance.new("Sound")
	sound.SoundId = SoundId
	sound.Parent = root
	sound:Play()
	Debris:AddItem(sound, 5)
end
local function setPressed(inst, data, pressed)
	if data.pressed == pressed then return end
	data.pressed = pressed
	if pressed then
		local root = getRootPart(inst)
		if root then playSound(root) end
	end
	if data.tween then data.tween:Cancel() data.tween = nil end
	local goalCF = targetCFrame(data, pressed)
	if data.isModel then
		data.tween = TweenService:Create(data.proxy, tweenInfo, { Value = goalCF })
	else
		data.tween = TweenService:Create(inst, tweenInfo, { CFrame = goalCF })
	end
	data.tween:Play()
end
local overlapParams = OverlapParams.new()
overlapParams.FilterType = Enum.RaycastFilterType.Include
local currentCharacter
local function bindCharacter(char)
	currentCharacter = char
	overlapParams.FilterDescendantsInstances = { char }
end
if Player.Character then bindCharacter(Player.Character) end
Player.CharacterAdded:Connect(bindCharacter)
for _, inst in ipairs(workspace:GetDescendants()) do
	registerKey(inst)
end
workspace.DescendantAdded:Connect(registerKey)
RunService.Heartbeat:Connect(function()
	local char = currentCharacter
	if not char or not char.Parent then return end
	if not char:FindFirstChild("HumanoidRootPart") then return end
	for inst, data in pairs(keyData) do
		if not inst.Parent then
			if data.proxy then data.proxy:Destroy() end
			keyData[inst] = nil
		else
			local root = getRootPart(inst)
			if root then
				local hits = workspace:GetPartBoundsInBox(data.origin, root.Size + Detection, overlapParams)
				setPressed(inst, data, #hits > 0)
			end
		end
	end
end)
