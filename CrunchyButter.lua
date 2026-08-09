local PackType = "CrunchyButter" -- Whatever this pack is called (Linked to the Attributes)
local Config = {}
Config.SoundName = "CrunchyButter" -- Change to whatever your Sound is called.
Config.CrackSpread = 0.3 -- How wide the cracks open up (0 = closed, 0.6 = dramatic).
Config.DentDepth = 2 -- How far you sink when on the butter.
Config.DentRadius = 12 -- How far away from the player the cracking reaches.
Config.DentPressSpeed = 11 -- How quick the butter cracks (Higher = sharper break).
Config.DentReleaseSpeed = 2 -- How long it takes for the cracks to close after being stood on.
Config.Volume = 0.9 -- The Audio volume.
Config.DentFalloff = 2 -- The shape of the dip (1 = pointy, 2 = soft bowl, 3 = narrow hole).
Config.StepGap = 2 -- The minimum gap between step sounds, stops them overlapping.
local mod = game:GetService("ReplicatedStorage"):WaitForChild("ASMRControls", 10)
if not mod then
	warn("[ASMR] 'ASMRControls' ModuleScript missing from ReplicatedStorage.")
	return
end
require(mod).Register(PackType, Config)
