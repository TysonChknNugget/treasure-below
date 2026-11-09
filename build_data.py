"""
Builds data.js (window.GAME) for the wiki from gamedata.json (the export from the game's own
data modules in Studio) plus a few hand-written extras the modules don't hold: zones, where
each monster lives, and the boss fight notes.

Run:  python build_data.py
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
D = json.loads((HERE / "gamedata.json").read_text(encoding="utf-8"))

ZONES = [
    {"name": "Town", "unlock": "Open from the start", "color": "uncommon",
     "text": "The hub. Whiskers' Wares sells pickaxes, weapons, shields and armor. Here are the Enchanter's Altar, Grimbold's Forge, the Hatchery, Pip's Packs, the Raid Gate, the Elder Gate and the Hall of Fame leaderboards."},
    {"name": "The Deep Mines", "unlock": "Open from the start", "color": "common",
     "text": "The cave under town: the Hollow, the Grand Cavern, the Grotto and the Depths. Goblins and Goblin Brutes guard the richer chambers.",
     "monsters": ["Goblin", "Brute"]},
    {"name": "Eclipse Shrine", "unlock": "The Eclipse Prophecy", "color": "celestial",
     "text": "Selene the Oracle's shrine. Its three gates lead to the Trials of the Sun and Moon and, at the end, to Eclipsar."},
    {"name": "The Abyss", "unlock": "Whispers of the Void", "color": "abyssal",
     "text": "A void-touched cave in the far north-east: Glowcap, the Chasm and the Voidheart Sanctum. Old Tobias forges endgame gear at its edge. Vor'Thalax waits in the heart.",
     "monsters": ["Voidling", "VoidBrute"]},
    {"name": "Goblin Fort", "unlock": "Open (far south-west)", "color": "legendary",
     "text": "A palisade full of goblins with archers on every tower. The War Gong in the War Hall summons Kragmaw the Warchief. The Kingdom Gate leads below.",
     "monsters": ["Goblin", "Brute", "Archer"]},
    {"name": "Skyreach", "unlock": "The Skyward Path", "color": "rare",
     "text": "Floating islands high above the north-west, reached by climbing the Sky Ladder and then by Captain Gale's Sky Lift. Sky pirates, storm brutes and sky ores.",
     "monsters": ["SkyPirate", "StormBrute"]},
    {"name": "The Broodhollow", "unlock": "The Brood Awakens", "color": "primordial",
     "text": "A giant anthill in the far south-east: the Antwork, the Colony, the Silkweb and the Brood Heart, where Vesskar the Thousand-Leg sleeps.",
     "monsters": ["WorkerAnt", "SoldierAnt", "CaveSpider", "Broodwidow"]},
    {"name": "Rootdeep", "unlock": "The Withering Root", "color": "ancient",
     "text": "The roots of a dead world-tree in the far west: the Mossway, the Sap Pools, Glimmercap Grove and the Heartroot, home of Gnarlroot.",
     "monsters": ["Rootling", "Thornspitter", "MossGolem"]},
    {"name": "The Heartwood Hollow", "unlock": "The Waking Tree, step 2", "color": "ancient",
     "text": "Rootdeep, part 2. Oakhollow the Tree Keeper's quest makes the old stump grow back into a giant world-tree (your own tree, saved with your quest). Climb the living-root stair and go through the hole in the trunk into the great glowing room inside it. Barkbeetles, the huge Stagborer, five amber tears, and Heartamber ore.",
     "monsters": ["Barkbeetle", "Stagborer"]},
    {"name": "The Beehive", "unlock": "The Waking Tree, step 4", "color": "ancient",
     "text": "Once the tree towers up, a spiral walkway climbs round the outside of its trunk to a great branch with a giant wax hive hanging off it. Honey Drones and Hive Guards (Broodhollow kin) and Royal Honeycomb ore. Bumbleworth the Beekeeper sells the tree's four pickaxes at his Honeyworks by Oakhollow.",
     "monsters": ["HoneyDrone", "HiveGuard"]},
    {"name": "The Goblin Kingdom", "unlock": "Beat Kragmaw the Warchief", "color": "gold",
     "text": "An endless floor-by-floor raid under the Goblin Fort. Every 10th floor is a boss, and past floor 50 they come back stronger.",
     "monsters": ["KingdomGuard", "KingdomBerserker", "KingdomChampion", "WarRaider", "WarBrute"]},
]

MONSTER_WHERE = {
    "Goblin": "The Deep Mines, Goblin Fort",
    "Brute": "The Deep Mines, Goblin Fort",
    "Archer": "Goblin Fort towers",
    "BoneThrall": "Raised by Mordrath the Lich King",
    "SkyPirate": "Skyreach",
    "StormBrute": "Skyreach",
    "Voidling": "The Abyss",
    "VoidBrute": "The Abyss",
    "WorkerAnt": "The Broodhollow",
    "SoldierAnt": "The Broodhollow",
    "CaveSpider": "The Broodhollow",
    "Broodwidow": "The Broodhollow",
    "Rootling": "Rootdeep",
    "Thornspitter": "Rootdeep",
    "MossGolem": "Rootdeep",
    "Barkbeetle": "The Heartwood Hollow (Rootdeep, part 2)",
    "Stagborer": "The Heartwood Hollow (Rootdeep, part 2)",
    "HoneyDrone": "The Beehive (Rootdeep, part 2)",
    "HiveGuard": "The Beehive (Rootdeep, part 2)",
    "WarRaider": "Kragmaw's warband, the Goblin Kingdom",
    "WarBrute": "Kragmaw's warband, the Goblin Kingdom",
    "KingdomGuard": "The Goblin Kingdom",
    "KingdomBerserker": "The Goblin Kingdom",
    "KingdomChampion": "The Goblin Kingdom (floor 31+)",
    "HexShade": "Called by Nyxa the Hexblade",
}

BOSS_WHERE = {
    "Raid": "Raid Gate, Town",
    "Quest": "Eclipse Shrine",
    "Abyss": "Voidheart Sanctum, The Abyss",
    "Elder": "Elder Gate, Town",
    "Brood": "Heart Sac, Brood Heart",
    "Root": "The Heartroot, Rootdeep",
    "Fort": "War Gong, Goblin Fort War Hall",
    "Kingdom": "The Goblin Kingdom",
}
BOSS_GROUP_NAME = {
    "Raid": "Raid Gate", "Quest": "Eclipse Trials", "Abyss": "The Abyss", "Elder": "Elder Gate",
    "Brood": "The Broodhollow", "Root": "Rootdeep", "Fort": "Goblin Fort", "Kingdom": "Goblin Kingdom",
}

# Fight notes, from each boss module's own description (technical lines left out)
BOSS_NOTES = {
    "GoblinKing": ["Weak on his own, Grukk leans on his summons: while 3 or more of his goblins are alive a golden ward soaks most damage, so you have to cut through the horde.", "He keeps his distance, slams anyone who corners him and lobs bags of gold.", "Below half health he flies into a rage and starts calling in brutes."],
    "Golem": ["A slow blocky giant of quarry rock with a crystal heart.", "Hammers the ground in front of him with both fists, stomps out a shockwave when raiders crowd his feet, and hurls boulders at anyone who keeps their distance.", "Below half health his crystals awaken: he speeds up and makes crystal spikes erupt under every raider."],
    "Dragon": ["On the ground: claw swipes in front, a tail sweep for anyone behind, and a long fire breath.", "At 70% and 35% health he takes off, circles the peak raining fireballs, then dive-bombs along a marked line and lands.", "Below 35% he's enraged: faster, with shorter cooldowns."],
    "SunTrial": ["A floating knight of gold and ivory with a blazing sun for a head.", "Keeps his distance and fires Solar Lances down long lines, calls Sunfall onto every raider, and bursts into a Flare when crowded.", "Below half health: the Solar Storm, wave after wave of sunfall, and his lances split in three."],
    "MoonTrial": ["A hooded wraith in a midnight cloak with a crescent blade on each arm.", "Slips through shadow to strike from behind, scythes crescent waves of moonlight, rains moon shards and hides behind summoned shades (she can't be hurt until they fall).", "Below half health the moon goes dark: she blinks more often and the shards fall thicker."],
    "Eclipse": ["Phase 1 (Sun): Solar Lances (three at once), Sunfall, Flare.", "Phase 2 (Moon): Crescent Waves, Moonfall, Blink, and shades that veil him.", "Phase 3 (Eclipse): everything, faster, and Total Eclipse: the sky goes black and only one circle of light is safe.", "He can't be hurt while shifting between phases."],
    "Abyss": ["Phase 1, The Gaze: Void Beam, Tentacle Slam, Claw Swipe, Void Orbs.", "Phase 2, The Hunger: + Devour (drags everyone toward its maw, then bites), Crystal Eruption, and Voidlings and Void Brutes.", "Phase 3, The Abyss Opens: everything faster and harder, and Abyssal Collapse: the whole floor is death except three small circles."],
    "FrostWyrm": ["Phase 1: Frost Breath (a long line), Icicle Rain (circles under everyone), Tail Sweep (a ring around it when you get close).", "Phase 2 (below half): + Glacial Spikes (lines of ice bursting outward) and Avalanche (huge falling ice blocks), everything faster and 25% harder."],
    "Kraken": ["It never leaves the water: it reaches across the whole arena instead.", "Phase 1: Tentacle Slam (along lines), Ink Barrage (ink bombs on everyone), Whirlpool (drags everyone toward its beak, then the beak snaps).", "Phase 2 (below half): + Grasp (tentacles burst out of the floor under everyone) and Tidal Wave (a wall of water sweeps the arena; get into one of the gaps)."],
    "LichKing": ["Phase 1: Soul Bolts, Bone Spikes (circles under everyone), Death Nova when you get close. He blinks around the crypt between casts.", "Phase 2 (below 60%): + Raise Dead (Bone Thralls rise; he's warded while any stand) and Soul Drain (get out of his reach).", "Phase 3 (below 30%): + Necrotic Field: the whole floor rots except three circles of light."],
    "StormTitan": ["Phase 1: Thunder Slam, Chain Lightning (bolts on everyone, in two waves), Hammer Throw (a line), and a stomp if you're underfoot.", "Phase 2 (below 66%): + Charge (he barrels along a line) and Storm Surge (strikes cascade across the peak).", "Phase 3 (below 33%): + Eye of the Storm: the whole peak is struck except a ring right around him. Get close!"],
    "Centipede": ["It slithers round the burrow without stopping, and its whole body hurts to touch.", "Phase 1: Bite, Venom Spit (globs that leave poison pools), Rush (a charge along a line) and Tail Lash.", "Phase 2 (below 66%): + Burrow (it dives under the floor and erupts beneath raiders; it can only be hurt while out of the ground) and Brood Call (spiders and a soldier ant).", "Phase 3 (below 33%): + Constrict: everyone outside the middle takes 75% of their health. Get to the centre!"],
    "Gnarlroot": ["Phase 1: Root Slam, Thorn Volley (thorns rain on everyone, in two waves), and a Sweep if you're close.", "Phase 2 (below 66%): + Root Eruption (roots burst up under every raider, three times) and Call (Rootlings and a Thornspitter).", "Phase 3 (below 33%): + Strangle: roots crush the whole hollow except a ring right around him. Get close! Calls bring a Moss Golem."],
    "Warchief": ["Unlike Grukk he fights up front and calls his warband to help.", "Phase 1: Cleave (a wide chop in front), Leap Slam (he jumps onto whoever is far away) and War Horn (Warband Raiders charge in from the gates).", "Phase 2 (below 66%): + Cleaver Throw (the cleaver spins out along a line and back), and the horn brings a Warband Brute too.", "Phase 3 (below 33%): Bloodrage. Faster, harder, and Whirlwind: he spins after you with the cleaver out."],
    "Siegemaster": ["He fights from range and makes the floor explode.", "Phase 1: Bomb Toss, Mortar Barrage (shells rain over the floor) and Wrench Smash if you get close.", "Phase 2 (below 66%): + Powder Kegs (they blow up after a fuse) and two Kingdom Guards.", "Phase 3 (below 33%): + Carpet Bomb (a line of blasts walks toward you). Faster fuses."],
    "Hexblade": ["She never stands still for long.", "Phase 1: Shadow Step (vanishes, reappears behind you and stabs), Hex Bolts (three bolts fanned out) and Hex Sigils (a sigil burns under every raider).", "Phase 2 (below 66%): + Hex Shades. While two or more stand she takes 85% less damage.", "Phase 3 (below 33%): + Hexstorm (sigils cascade across the whole floor in three waves)."],
    "Juggernaut": ["A huge goblin sealed inside a riveted iron war-suit with a furnace in its chest.", "Phase 1: Ram Charge (a long line), Ground Pound (around him) and Furnace Blast (fire in a wide line).", "Phase 2 (below 66%): + Steam Vents (vents burst under raiders and across the floor).", "Phase 3 (below 33%): + Meltdown: a ring of fire rolls out. Stand right next to him or far away."],
    "Beastmistress": ["A goblin huntress riding a giant armoured war-boar.", "Phase 1: Boar Charge (a long, fast line), Gore (tusks in front), Spear Throw (a javelin line) and Trample.", "Phase 2 (below 66%): + Call of the Wild: Kingdom Berserkers answer her horn.", "Phase 3 (below 33%): + Stampede: three charges back to back."],
    "Emperor": ["The lord of the Kingdom, swinging the Kingsblade.", "Phase 1: Royal Cleave (a huge sweep), Golden Rain and Earthsplitter (he leaps onto a far raider).", "Phase 2 (below 66%): + Imperial Guard (while two or more stand he takes 75% less damage) and Kingsblade Wave (a golden wave down a long line).", "Phase 3 (below 33%): + Royal Decree: the whole floor is struck except three jade circles. Get into one! A Kingdom Champion joins the guard."],
}

STYLES = {
    "Flurry": "Fast stabs", "Blade": "Slashes", "Thrust": "Long thrust (hits a line)", "Smash": "Overhead smash (splash)",
    "Archery": "Bow (ranged)", "Whirlwind": "Spinning swings (splash)", "Bolt": "Crossbow (ranged, pierces)",
    "Cleave": "Wide cleave (hits an arc)", "Cast": "Fireballs (ranged, explode)", "Reap": "Scythe reap (pulls enemies in)",
    "Fang": "Venom fang (finisher burst)",
}

# Bosses: add where, group and notes
groups = D["bosses"]["groups"]
for g, keys in groups.items():
    for k in keys:
        b = D["bosses"]["items"][k]
        b["Group"] = BOSS_GROUP_NAME[g]
        b["Where"] = BOSS_WHERE[g] if g != "Kingdom" else f"The Goblin Kingdom, floor {b.get('Floor')}"
        b["Notes"] = BOSS_NOTES.get(k, [])
        b["Loot"] = D["loot"]["bosses"].get(k)
D["bosses"]["groupOrder"] = ["Raid Gate", "Eclipse Trials", "The Abyss", "Elder Gate", "The Broodhollow", "Rootdeep", "Goblin Fort", "Goblin Kingdom"]

for k, where in MONSTER_WHERE.items():
    if k in D["monsters"]:
        D["monsters"][k]["Where"] = where

D["zones"] = ZONES
D["styles"] = STYLES
D["kingdom"] = {
    "countdown": 8, "break": 5, "heal": 0.35,
    "floorGold": "1,500 + 500 × floor",
    "bossFloors": [{"floor": 10 * (i + 1), "key": k} for i, k in enumerate(groups["Kingdom"])],
}

out = "// Generated by build_data.py from gamedata.json. Don't edit by hand.\nwindow.GAME = " + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";\n"
(HERE / "data.js").write_text(out, encoding="utf-8")
print("data.js", len(out), "bytes")
