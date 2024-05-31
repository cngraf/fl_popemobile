from enums import *
import utils

'''
Defining the baseline endgame player
- excludes boons and moods
- excludes Ambition stuff
    - Treasure
    - ambition-exclusive items
- excludes SMEN & Retired items (irrelevant anyway?)
- excludes item slots that can't be easily swapped
    - Destiny
        - also excludes Mark of Acceptance
        - but allows Memory of Much Greater Self?
    - Ship
    - Spouse
    - Club
    - Profession item

TODO:
- double check these, just count programmatically
- numbers for "soft F2P"?
    - allow exceptional story, memory of a tale stuff
    - allow Ubergoat, other 1 FATE items

with FATE & Seasonal:
Watchful:   +92 => 322
Shadowy:    +73 => 303
Dangerous:  +83 => 313
Persuasive: +85 => 315

KT:     +10
MA:     +10
APoC:   +10
GW:     +11
SA:     +10
AotRS:  +10
Mith:   +10
SotD:   +1
Zee:    +10

without FATE and Seasonal:
Watchful:   +76
Shadowy:    +65
Dangerous:  +72
Persuasive: +71

KT:     +6
MA:     +4
APoC:   +3
GW:     +5
SA:     +2
AotRS:  +2
Mith:   +3
SotD:   +1
Zee:    +5

so to really get into the nitty gritty, are we gonna need some concept of outfits?
thinking of scandal multiplier

List of Mutually-Exclusive Item & Quality Groups (WIP)
- Treasures
- Destinies + Mark of Acceptance
- Tools of the Trade
- Ships
- Spouses
- Clubs
- Airships
- Tattoos

- Ambition-specific items
- notable branching choices WITHIN Ambitions
    - LF: Lyon Pursuivant vs. Tatterskin Shawl
    - Nem: Dream-Shadow vs. Dream-Shard
    - BAL: trapping 3CV in parabola vs. not
    - HD: none?
- rewards of ambition

- Unburdened Imp & Deviless variants
    - Imp is the only BiS option
- Salon & Orphanage
- Sacksmas Quest Rewards
    - not exclusive but takes several years to complete

- Lab staffing

- Khaganian Network configuration
    - Ties
    - Methods
    - was there a third thing?

- GHR board members
- GHR statues
- GHR station darkness 
- TLC stuff
    - Location
    - Founding Body
    - Currency
    - Leader
    - Political Alignment
- "Closest To" faction

- numerous ES branching choices
    - trade in souls
    - aunt
'''

def baseline_stats():
    return {
        Stat.Watchful:      230,
        Stat.Shadowy:       230,
        Stat.Dangerous:     230,
        Stat.Persuasive:    230,

        Stat.Respectable: 0,
        Stat.Dreaded: 0,
        Stat.Bizarre: 0,

        Stat.KatalepticToxicology: 7,
        Stat.MonstrousAnatomy: 7,
        Stat.APlayerOfChess: 7,
        Stat.Glasswork: 7,
        Stat.ShapelingArts: 7,
        Stat.ArtisanOfTheRedScience: 7,
        Stat.Mithridacy: 7,

        Stat.StewardOfTheDiscordance: 7, # 6?
        Stat.Zeefaring: 7,
        Stat.Chthonosophy: 2,

        Stat.Inerrant: 0,
        Stat.Insubstantial: 0,
        Stat.Neathproofed: 0,
    }

def min_endgame_f2p_bonuses():
    # Excludes
    # - anything FATE-locked
    # - Mr Chimes' Lost & Found
    # - hellworm
    # - ubergoat 
    # - annual seasonal items
    # - ambitions
    # - professions
    # - any slots with swap costs (ship, spouse, destiny, etc.)
    # - any items from a mutually exclusive set (eg. salon/orphanage, unburdened imp)
    # - mark of acceptance
    # - boons & moods
    # - SMEN
    # - retired items
    # - ubergoat (borderline?)

    # Includes
    # - faction renown items
    # - Sacroboscan calendar items
    # - Evolution
    # - Railway & TLC
    # - Firmanent
    # - non-seasonal HG items
    return {
        Stat.Watchful: 8 + 11 + 8 + 8 + 10 + 7 + 10 + 5 + 7, # 74
        Stat.Shadowy: 6 + 6 + 7 + 10 + 10 + 10 + 6 + 10 + 5 + 8, # 78
        Stat.Dangerous:  6 + 8 + 5 + 8 + 12 + 8 + 10 + 4 + 6 + 4, # 71
        Stat.Persuasive: 10 + 10 + 8 + 5 + 10 + 5 + 10 + 2 + 8 + 8, # 76

        Stat.Bizarre: 1 + 2 + 2 + 2 + 1 + 1 + 1 + 2 + 1 + 2 + 2, # 17
        Stat.Dreaded: 2 + 2 + 1 + 1 + 1 + 1 + 1 + 4 + 2 + 2, # 17
        Stat.Respectable: 1 + 1 + 2 + 1 + 1 + 1 + 1 + 4 + 2 + 2, # 16

        # Labcoat or Shell, Work Gloves, Butcher's Tool, Perfumer's Arts
        Stat.KatalepticToxicology: 4,

        # Illuminating Cap, Shell or Ribcage, Naturalist's Map
        Stat.MonstrousAnatomy: 3,

        # Director's Overcoat, Infiltrator's Footsteps, FFG's Address Book
        Stat.APlayerOfChess: 3,

        # Parabola Suit or Viric Frock, VC's Collar, Honey-Mazed Bear, OP Stave (+2)
        Stat.Glasswork: 5,

        # Tunip, Amber Vision
        Stat.ShapelingArts: 2,

        # Misplaced Ring, Flower from Hell, Lowell's Locks and Cages
        Stat.ArtisanOfTheRedScience: 3,

        # Viscount's Collar, Stalking Shadow, Memory of Much Greater Self
        Stat.Mithridacy: 3,

        # imp is from an exclusive set
        Stat.StewardOfTheDiscordance: 0,

        # Captain's or Admiral's Hat, Mostly-Cooperative Chart, Blue Prophet,
        # HMS Ramilies, Amber Vision
        Stat.Zeefaring: 5,

        # Glim Earring
        Stat.Chthonosophy: 1,

        # Glim Earring, Carpetbag, Cinnabar Compass
        Stat.Inerrant: 3,

        # Carryall or Suitcase, Nod from Mr Hearts
        Stat.Insubstantial: 2,

        # Illuminating Cap or Hymn, Ratskin Suit, Devil's Dictionary, Ratskin Boots,
        # Indestructible Trunk
        Stat.Neathproofed: 5,
    }


class Player:
    '''
    TODO
    - get rid of Location prop
    - add Spouse
    - add Ship
    - add Destiny
    - add Club
    '''

    location: Location
    ambition: Ambition
    treasure: Treasure
    profession: Profession
    specialization: Specialization

    baseline_watchful = 230 + 92
    baseline_shadowy = 230 + 73
    baseline_dangerous = 230 + 83
    baseline_persuasive = 230 + 85

    def __init__(self,
                location = Location.NoLocation,
                ambition = Ambition.NoAmbition,
                profession = Profession.NoProfession,
                treasure = Treasure.NoTreasure,
                stats = {}):
        
        self.location = location
        self.ambition = ambition
        self.profession = profession
        self.specialization = Specialization.NoSpecializaiton
        self.treasure = treasure

        advanced_value = 17

        self.stats = {
            Stat.Watchful:      230 + 92,
            Stat.Shadowy:       230 + 73,
            Stat.Dangerous:     230 + 83,
            Stat.Persuasive:    230 + 85,

            Stat.KatalepticToxicology: advanced_value,
            Stat.MonstrousAnatomy: advanced_value,
            Stat.APlayerOfChess: advanced_value,
            Stat.Glasswork: advanced_value,
            Stat.ShapelingArts: advanced_value,
            Stat.ArtisanOfTheRedScience: advanced_value,
            Stat.Mithridacy: advanced_value,
            Stat.StewardOfTheDiscordance: 8,
            Stat.Zeefaring: advanced_value
        }

        for key, value in stats.items():
            self.stats[key] = value

        self.wounds_reduction = 2
        self.scandal_reduction = 2
        self.suspicion_reduction = 2
        self.nightmares_reduction = 2
        self.troubled_waters_reduction = 2

    # TOOD: add a threshold to auto-use a second chance item?
    def pass_rate(self, stat, difficulty):
        player_level = self.stats[stat]
        if stat in (Stat.Watchful, Stat.Shadowy, Stat.Dangerous, Stat.Persuasive):
            return utils.broad_challenge_success_rate(player_level, difficulty)
        else:
            return utils.narrow_challenge_success_rate(player_level, difficulty)
        
    # def challenge_ev(self, stat, difficulty, on)

    def wounds_ev(self, int):
        blocked = min(2, int * utils.menace_multiplier(self.wounds_reduction))
        return max(0, int - blocked)

    def scandal_ev(self, int):
        blocked = min(2, int * utils.menace_multiplier(self.scandal_reduction))
        return max(0, int - blocked)

    def nightmares_ev(self, int):
        blocked = min(2, int * utils.menace_multiplier(self.nightmares_reduction))
        return max(0, int - blocked)                

    def suspicion_ev(self, int):
        blocked = min(2, int * utils.menace_multiplier(self.suspicion_reduction))
        return max(0, int - blocked)

    # suspicion_multiplier = menace_multiplier(player.suspicion_reduction)
    # scandal_multiplier = menace_multiplier(player.scandal_reduction)    
    # nightmares_multiplier = menace_multiplier(player.nightmares_reduction)


class Challenge:
    def __init__(self, stat: Stat, dc: int, on_pass: dict, on_fail: dict):
        self.stat = stat
        self.dc = dc
        self.on_pass = on_pass
        self.on_fail = on_fail

    # def get_trade(self, player: Player):
    #     pass_rate = player.pass_rate(self.stat, self.dc)
    #     return utils.weighted_exchange(
    #         ()
    #     )