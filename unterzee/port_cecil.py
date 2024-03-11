from enums import *
from utils import *

def add_trades(active_player, trade):
    # --------------
    # Port Cecil
    # -------------

    # 7? actions to zail from london? 4 + 2 + 1
    # TODO: check round trip length
    trade(14, {
        Item.PortCecilCycles: 4, # arbitrary, how many times thru before home
        Item.ZailingDraws: 12
    })

    # ideal cycle w/ maxed stats
    # - 13 AotRS (reliable but less profitable w less)
    # - 334 Watchful (required to guarantee 50/50 split)
    # - 334 Persuasive  (required to guarantee 50/50 split)
    # 5x (red science miners => 7x map scrap, 1x knob scintillack)
    # 1x (instruct the cats => 5x scrap of i.g., 7x romantic notion)
    # 5x (prey on miners concerns => 6x journal ofinf)
    # 2x (deploy cat wrangling => 30x silvered cats claw)
    #   OR (distact w wildlife => 4x withered tentacle)

    trade(14, {
        Item.PortCecilCycles: -1,
        Item.MapScrap: 35,
        Item.KnobOfScintillack: 5,
        Item.ScrapOfIncendiaryGossip: 5,
        Item.RomanticNotion: 7,
        Item.JournalOfInfamy: 30,
        Item.WitheredTentacle: 8,
        Item.LostResearchAssistant: 1,
        Item.SegmentedRibcage: 3
    })

    # alternative in carousel
    trade(0, {
        Item.WitheredTentacle: -4,
        Item.SilveredCatsClaw: 30
    })

    # slightly less profitable but more achievable grind
    # 5x direct miners toward dig site
    # - doesn't derail on failure
    # - 90% success w 273 P, 100% w 300
    # 1x instruct cats in calc
    # 3x liberate raw scintillack
    # 3x bring refreshments
    # 1x distract cats w/ wildlife

    trade (14, {
        Item.PortCecilCycles: -1,
        Item.ZeeZtory: 6 * 5,
        Item.ScrapOfIncendiaryGossip: 5,
        Item.RomanticNotion: 7,
        Item.KnobOfScintillack: 3,
        Item.MemoryOfDistantShores: 4 * 3,
        Item.WitheredTentacle: 4,
        Item.LostResearchAssistant: 1, 
        Item.SegmentedRibcage: 3
    })
