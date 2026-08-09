local PackType = "Butter" -- Whatever this pack is called (Linked to the Attributes)
local Config = {}
Config.SoundName = "Butter" -- Change to whatever your Sound is called.
Config.DentDepth = 2 -- How far you sink when on the butter.
Config.DentRadius = 15 -- How far away from the player the butter is effected.
Config.DentPressSpeed = 9 -- How quick the butter moves (Higher = quicker).
Config.DentReleaseSpeed = 1.2 -- How long it takes for the butter to bounce back after being stood on.
Config.Volume = 2 -- The Audio volume.
Config.DentFalloff = 2 -- The shape of the dip (1 = pointy, 2 = soft bowl, 3 = narrow hole).
Config.StepGap = 0.65 -- The minimum gap between step sounds, stops them overlapping.
local mod = game:GetService("ReplicatedStorage"):WaitForChild("ASMRControls", 10)
if not mod then
	warn("[ASMR] 'ASMRControls' ModuleScript missing from ReplicatedStorage.")
	return
end
require(mod).Register(PackType, Config)
