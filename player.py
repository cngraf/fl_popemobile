from enums import *


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
Watchful:   +92
Shadowy:    +73
Dangerous:  +83
Persuasive: +85

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

'''

class Player:

    def __init__(self,
                location = Location.NoLocation,
                ambition = Ambition.NoAmbition,
                profession = Profession.NoProfession,
                treasure = Treasure.NoTreasure,
                stats = {}):
        self.location = location
        self.ambition = ambition
        self.profession = profession
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
