from enums import *
from helper.utils import *

def add_trades(config):
    trade = config.trade
    add = config.add

    # --------------
    # Port Cecil
    # -------------

    add({
        Item.Action: -11.5 - 40,
        Item.StashedTreasure: 2700,
        Item._PortCecilAction: 40,
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

    # trade(1, { Item._PortCecilAction: 1 })

    trade(0, {
        Item._PortCecilAction: -14,
        Item.MapScrap: 35,
        Item.KnobOfScintillack: 5,
        Item.ScrapOfIncendiaryGossip: 5,
        Item.RomanticNotion: 7,
        Item.JournalOfInfamy: 30,
        Item.WitheredTentacle: 8,
        Item.LostResearchAssistant: 1,
        Item.SegmentedRibcage: 3
    })

    trade(0, {
        Item._PortCecilAction: -14,
        Item.MapScrap: 35,
        Item.KnobOfScintillack: 5,
        Item.ScrapOfIncendiaryGossip: 5,
        Item.RomanticNotion: 7,
        Item.JournalOfInfamy: 30,
        Item.WitheredTentacle: 4,
        Item.SilveredCatsClaw: 30,
        Item.LostResearchAssistant: 1,
        Item.SegmentedRibcage: 3
    })

    trade(0, {
        Item._PortCecilAction: -14,
        Item.MapScrap: 35,
        Item.KnobOfScintillack: 5,
        Item.ScrapOfIncendiaryGossip: 5,
        Item.RomanticNotion: 7,
        Item.JournalOfInfamy: 30,
        Item.SilveredCatsClaw: 60,
        Item.LostResearchAssistant: 1,
        Item.SegmentedRibcage: 3
    })

    # slightly less profitable but more achievable grind
    # 5x direct miners toward dig site
    # - doesn't derail on failure
    # - 90% success w 273 P, 100% w 300
    # 1x instruct cats in calc
    # 3x liberate raw scintillack
    # 3x bring refreshments
    # 1x distract cats w/ wildlife

    trade(0, {
        Item._PortCecilAction: -14,
        Item.ZeeZtory: 6 * 5,
        Item.ScrapOfIncendiaryGossip: 5,
        Item.RomanticNotion: 7,
        Item.KnobOfScintillack: 3,
        Item.MemoryOfDistantShores: 4 * 3,
        Item.WitheredTentacle: 4,
        Item.LostResearchAssistant: 1, 
        Item.SegmentedRibcage: 3
    })
