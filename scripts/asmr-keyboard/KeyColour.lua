local KeyName = "Key" -- Must match the KeyName used in your LocalScript.
local Saturation = 0.65 -- How vivid the colours are (0 = grey, 1 = full).
local Value = 0.9 -- How bright the colours are (0 = black, 1 = full).
local colored = {}

local function randomColor()
	return Color3.fromHSV(math.random(), Saturation, Value)
end

local function contrastText(bg)
	local _, _, v = Color3.toHSV(bg)
	return v > 0.6 and Color3.new(0, 0, 0) or Color3.new(1, 1, 1)
end

local function randomLetter()
	return string.char(math.random(65, 90)) -- A-Z, all caps.
end

local function colorKey(inst)
	if colored[inst] then return end
	if inst.Name ~= KeyName then return end

	local color = randomColor()
	local letter = randomLetter()
	local isModel = inst:IsA("Model")

	if isModel then
		for _, d in ipairs(inst:GetDescendants()) do
			if d:IsA("BasePart") then d.Color = color end
		end
	elseif inst:IsA("BasePart") then
		inst.Color = color
	else
		return
	end

	for _, d in ipairs(inst:GetDescendants()) do
		if d:IsA("TextLabel") then
			d.TextColor3 = contrastText(color)
			d.Text = letter
		end
	end

	colored[inst] = true
end

for _, inst in ipairs(workspace:GetDescendants()) do
	colorKey(inst)
end
workspace.DescendantAdded:Connect(colorKey)
