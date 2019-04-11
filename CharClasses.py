import random as rand

names=["en", "da", "fu", "tuk", "tikki", "raz", "pak", "thuri", "yol", "brok", "joj"]

class character(object):
    def __init__(self, _type, health, mana, attack, spells, specials, buffs, amount):
        self.name="".join([rand.choice(names) for x in range(3)])
        self.amount = amount
        self.type=_type
        self.health = health
        self.lvl = 1
        self.attack = attack
        self.mana = mana
        self.multiplier = 1
        self.spells = spells
        self.specials = specials
        self.buffs = buffs

    def __iter__(self):
        stats=(("Level: ", self.lvl), ("Health: ", self.health), ("Mana: ", self.mana),
               ("Attack: ", self.attack), ("Spells: ", ", ".join(sp[0] for sp in self.spells)),
               ("Specials: ", ", ".join((sp[0] for sp in self.specials))),
               ("Buffs: ", ", ".join((buff[0] for buff in self.buffs))))
        return iter(stats)
     
class Barbarian(character):
    def __init__(self):
        spells = (("Cutting Edge", 5, 4), ("Piercing Strike", 8, 10), ("Slash", 3, 2))
        specials = (("Twin Blade Strike", 10, 3), ("Grand power Strike", 15, 6))
        buffs = (("Cure Wounds", 5, 3, "Heal"), ("Quick March", 1, 7, "MultM"), ("Berzerk", 2, 15, "MultH"))
        super().__init__("Barbarian", 10, 10, 4, spells, specials, buffs, 10)
        
class Elf(character):
    def __init__(self):
        spells = (("Woodland Stride", 4, 2), ("Acid Javelin", 6, 3), ("Earth Bind", 8, 5))
        specials = (("Crystal Dagger", 10, 3), ("Earth Surge", 16, 5))
        buffs = (("Crystal Cloud", 20, 10, "Heal"), ("Silence", 1, 6, "MultM"), ("Gaia's Seed", 20, 10, "Mana")) 
        super().__init__("Elf", 20, 25, 1, spells, specials, buffs, 40)

class Wizard(character):
    def __init__(self):
        spells = (("Astral Smite", 8, 7), ("Dragon Lightning", 12, 8), ("Grand Flame", 6, 3))
        specials = (("Reality Slash", 10, 3), ("Electrosphere", 16, 6))
        buffs = (("Energy Drain", 25, 5, "Mana"), ("False Power", 10, 2, "Mana"), ("Force Sanctuary", 25, 20, "Heal"))
        super().__init__("Wizard", 25, 50, 1, spells, specials, buffs, 80)

class Manticore(character):
    def __init__(self):
        spells = (("Flamewing", 5, 10), ("Hell Flame", 8, 12), ("Word of Curse", 3, 4))
        specials = (("Napalm", 12, 4), ("Fire Pillar", 40, 10))
        buffs = (("Energy Immunity", 10, 5, "Mana"), ("Dominate", 2, 30, "MultH"), ("Soothing Rage", 30, 20, "Heal"))
        super().__init__("Manticore", 90, 25, 5, spells, specials, buffs, 350)

class CrimsonDrake(character):
    def __init__(self):
        spells = (("Meteor Fall", 30, 10), ("Implosion", 50, 20), ("Explosion", 70, 40))
        specials = (("Vermilion Nova", 80, 8), ("Nuclear Blast", 100, 10))
        buffs = (("Draconic Power", 50, 10, "Heal"), ("Greater Magic Boost", 20, 6, "Mana"), ("Fire Rain", 4, 100,"MultH"))
        super().__init__("Crimson Drake", 500, 100, 10, spells, specials, buffs, 3300)

class Knight(character):
    def __init__(self):
        spells = (("Silver Lance", 6, 6), ("Thunder Lance", 7, 7), ("Freeze Lance", 8, 8))
        specials = (("Crystal Lance", 8, 2), ("Chain Lightning", 12, 4))
        buffs = (("Heavy Recover", 20, 20, "Heal"), ("Counter Detect", 1, 7, "MultM"), ("Fortress", 10, 5, "Mana"))
        super().__init__("Knight", 50, 20, 4, spells, specials, buffs, 65)

class LichDragon(character):
    def __init__(self):
        spells = (("Hold Of Ribs", 6, 4), ("Hawk Eye", 7, 5), ("Greater Lethal", 8, 6))
        specials = (("Ice Pillar", 25, 5), ("Indomitability", 30, 10))
        buffs = (("Magic Boost", 5, 1, "Mana"), ("Mid Magic Boost", 10, 3, "Mana"), ("Greater Magic Boost", 20, 6, "Mana"))
        super().__init__("Lich Dragon", 100, 30, 0, spells, specials, buffs, 450)

class ChaoticShambler(character):
    def __init__(self):
        spells = (("Strong Assault", 50, 40), ("Greater Strength", 40, 30), ("Skeletal Spike", 10, 3))
        specials = (("Sense Weakness", 80, 10), ("Grand Catastrophe", 100, 15)) 
        buffs = (("Sacrifice", 10, 450, "MultH"), ("Limit Breaker", 200, 130, "Heal"), ("Limit Breaker: Mind", 80, 80, "Mana"))
        super().__init__("Chaotic Shambler", 500, 300, 0, spells, specials, buffs, 5000)

class CyanSpellcaster(character):
    def __init__(self):
        spells = (("Wind Talisman", 10, 3), ("Weak Counter", 3, 1), ("Poison", 5, 2))
        specials = (("Tornado", 20, 8), ("Air Blade", 25, 9))
        buffs = (("Mana Essence", 10, 2, "Mana"), ("Magic Shield", 10, 2, "Heal"), ("Magic Weapon", 1, 7, "MultM"))
        super().__init__("Cyan Spellcaster", 25, 60, 0, spells, specials, buffs, 90)

class DreamWyrm(character):
    def __init__(self):
        spells = (("Night Talisman", 5, 4),)
        specials = (("Distant Vision", 2, 1),)
        buffs = (("Dream", 10, 30, "MultM"), ("Sanctuary", 15, 10, "Heal"), ("Melody", 10, 2, "Mana"))
        super().__init__("Dream Wyrm", 30, 30, 1, spells, specials, buffs, 100)

class HauntedLog(character):
    def __init__(self):
        spells = ()
        specials = ()
        buffs = (("Growth", 20, 5, "Heal"), ("Bloom", 10, 1, "Mana"), ("Rooted", 30, 8, "Heal")) 
        super().__init__("Haunted Log", 80, 10, 4, spells, specials, buffs, 85)

class HeroKing(character):
    def __init__(self):
        spells = (("Commandment", 30, 15), ("Heavy Strike", 20, 10))
        specials = (("Under Divine Rule", 30, 6),)
        buffs = (("Create Fortress", 30, 20, "Heal"), ("Pray", 30, 15, "Mana"), ("Lion's Heart", 1, 15, "MultM"))
        super().__init__("Hero King", 150, 70, 7, spells, specials, buffs, 550)

class LampStalker(character):
    def __init__(self):
        spells = (("Distort Shadows", 3, 2), ("Quick Pace", 4, 3), ("Paranoia", 2, 1))
        specials = (("Illuminate", 5, 3), ("Lights Out!", 30, 10))
        buffs = (("Strike Match", 1, 10, "MultH"), ("Raise Lamp", 2, 20, "MultH"), ("Light Candle", 3, 30, "MultH"))
        super().__init__("Lamp Stalker", 90, 10, 0, spells, specials, buffs, 350)

class Mercenary(character):
    def __init__(self):
        spells = (("Slash", 3, 2), ("Cutting Edge", 7, 5), ("Fatal Edge", 15, 10))
        specials = (("Full Throttle", 20, 10), ("Grand Power Strike", 30, 15))
        buffs = (("Ability Boost", 1, 10, "MultM"), ("Focus Battle Aura", 2, 20, "MultH"), ("Cure Wounds", 5, 3, "Heal"))
        super().__init__("Mercenary", 60, 10, 4, spells, specials, buffs, 80)

class Necromancer(character):
    def __init__(self):
        spells = (("Animate Dead", 20, 10), ("Detect Life", 15, 8), ("Fear", 10, 5))
        specials = (("Death March", 50, 10), ("True Dark", 80, 20))
        buffs = (("Dark Vision", 30, 10, "Mana"), ("Negative Burst", 20, 10, "Heal"), ("Undead Flame", 10, 5, "Heal"))
        super().__init__("Necromancer", 100, 150, 0, spells, specials, buffs, 750)

class ObsidianGolem(character):
    def __init__(self):
        spells = ()
        specials = (("Iron Fist", 40, 10), ("Power Claw", 60, 20), ("Arm Of The Demon", 90, 30))
        buffs = ()
        super().__init__("Obsidian Golem", 200, -100, 15, spells, specials, buffs, 800)

class PlagueRogue(character):
    def __init__(self):
        spells = (("Vermin Bane", 10, 6), ("Twine Plant", 20, 10), ("Fox Sleep", 30, 20))
        specials = (("Knife Storm", 30, 10), ("Greater Luck", 40, 15))
        buffs = (("Dull Pain", 30, 20, "Heal"), ("Strengthen Perception", 40, 25, "Mana"), ("Sharpen Dagger", 1, 15, "MultM"))
        super().__init__("Plague Rogue", 90, 90, 6, spells, specials, buffs, 700)

class PyroHarvester(character):
    def __init__(self):
        spells = (("Wickerman", 20, 10), ("Primal Fire", 30, 20), ("Unholy Flame", 50, 30))
        specials = (("True Dark", 80, 20), ("Pure Flame", 50, 10), ("Reap", 60, 15))
        buffs = (("Magic Boost", 10, 2, "Mana"), ("Effigy", 20, 6, "Heal"))
        super().__init__("Pyro Harvester", 300, 80, 8, spells, specials, buffs, 900)

class  SentryBot(character):
    def __init__(self):
        spells = (("Gattling Gun", 10, 3), ("Instant Counter", 30, 15))
        specials = (("Lazer Vision", 40, 10), ("Metal Enhancement", 50, 15))
        buffs = (("Electric Barrier", 20, 10, "Heal"), ("Short Circuit", 20, 7, "Mana"))
        super().__init__("Sentry Bot", 350, 60, 8, spells, specials, buffs, 780)

class SeraphicKnight(character):
    def __init__(self):
        spells = (("Valor", 20, 10), ("Holy Fire", 30, 20), ("Greater Light", 40, 30))
        specials = (("God Flash", 100, 20), ("Sixfold Slash of Light", 30, 8), ("Heavenly Aura", 50, 15)) 
        buffs = (("Uriel", 100, 50, "Heal"), ("Greater Spirit Boost", 30, 30, "Mana"), ("Spirit Boost", 20, 20, "Mana"))
        super().__init__("Seraphic Knight", 400, 200, 4, spells, specials, buffs, 1800)

class ShrubParasite(character):
    def __init__(self):
        spells = ()
        specials = (("Steal Life Essence", 5, 5),)
        buffs = (("Detect Life", 1, 5, "MultH"), ("Hunger", 2, 10, "MultH"), ("Starvation", 3, 20, "MultH"),
                 ("Depraved", 5, 30, "MultH"))
        super().__init__("Shrub Parasite", 350, 0, 1, spells, specials, buffs, 670)

class WaterGuardian(character):
    def __init__(self):
        spells = (("Repel Undeath", 20, 10), ("Monsoon", 50, 30), ("Open Wounds", 30, 20))
        specials = (("Shark Cyclone", 80, 15), ("Tsunami", 100, 20))
        buffs = (("Ocean Ruler", 100, 40, "Mana"), ("Calm Waves", 15, 10, "Heal"), ("Tidal Surge", 1, 15, "MultM"))
        super().__init__("Water Guardian", 350, 150, 0, spells, specials, buffs, 1500)

class EliteGunman(character):
    def __init__(self):
        spells = (("Twin Rifle Assault", 15, 8), ("Gale Acceleration", 30, 16), ("Vertical Strike", 40, 25))
        specials = (("High Vertical Strike", 50, 10), ("Overdrive!", 90, 20), ("Thunderball", 30, 6))
        buffs = (("Physical Boost", 2, 30, "MultM"), ("Strengthen Perception", 3, 40, "MultM"), ("Flow Acceleration", 30, 15, "Mana"))
        super().__init__("Elite Gunman", 400, 200, 8, spells, specials, buffs, 2500)

class GoldenHydra(character):
    def __init__(self):
        spells = (("Continual Light", 30, 15), ("Turn Undead", 40, 20), ("True Light", 20, 10))
        specials = (("God Flash", 100, 20), ("Vision Of The Oracle", 70, 12))
        buffs = (("1st Head Heal", 50, 20, "Heal"), ("2nd Head Mana", 50, 30, "Mana"), ("3rd Head Multiplier", 8, 150, "MultH"))
        super().__init__("Golden Hydra", 450, 150, 6, spells, specials, buffs, 4000)

class FesteringHydra(character):
    def __init__(self):
        spells = (("Petrification", 30, 15), ("Gravity Maelstrom", 60, 30), ("Dance Of Death", 70, 40))
        specials = (("Mantle Of Chaos", 80, 15), ("Thousand Bone Lance", 90, 20))
        buffs = (("Skeletal Wall", 40, 20, "Heal"), ("False Data: Mana", 40, 20, "Mana"), ("Dark Vision", 2, 45, "MultM"))
        super().__init__("Festering Hydra", 350, 130, 5, spells, specials, buffs, 3000)

chars=[Barbarian, Elf, Knight, Wizard, LichDragon, Manticore, WaterGuardian, ShrubParasite, SeraphicKnight, SentryBot,
       PyroHarvester, PlagueRogue, ObsidianGolem, Necromancer, Mercenary, LampStalker, HeroKing, HauntedLog, DreamWyrm,
       CyanSpellcaster, ChaoticShambler, CrimsonDrake, EliteGunman, FesteringHydra, GoldenHydra]
image_chars=[char() for char in chars]
