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

'''

class Player:
    '''
    TODO
    - get rid of Location prop
    - add Spouse
    - add Ship
    - add Destiny
    - add Club
    '''

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