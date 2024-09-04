import math
from enum import Enum, auto

from enums import *
import utils
from config import Config
from player import Player


def add_trades(config: Config):
    trade = config.trade

    # trade(0, {
    #     Item.NoduleOfWarmAmber: -1,
    #     Item.Stuiver: 1
    # })


    # for item, buy_price in (
    #     # The Flexile Peddler
    #     (Item.SampleOfRoofDrip, -4),
    #     (Item.StarvedExpression, -20),
    #     (Item.GlimEncrustedCarapace, -3000),

    #     # The Cenobitic Outfitter
    #     (Item.RoofChart, -100),
    # ):
    #     trade(0, { item: 1, Item.HinterlandScrip: buy_price })

    for item, sale_value in (
        (Item.SampleOfRoofDrip, 2),
        (Item.TantalisingPossibility, 2),
        (Item.StarvedExpression, 10),
        (Item.TempestuousTale, 10),
        (Item.AscendedAmbergris, 50),
        (Item.RelicOfTheFifthCity, 50),
        (Item.CausticApocryphon, 250),
        (Item.MemoryOfAMuchStrangerSelf, 250),
        (Item.MemoryOfMoonlight, 250),
        (Item.GlimEncrustedCarapace, 1250),
        (Item.GlimpseOfAnathema, 6250)

    ):
        trade(0, { item: -1, Item.Stuiver: sale_value })

    trade(0, {
        Item.RoofChart: -1,
        Item.MoonPearl: 253
    })
    
    # Stacks results per simulation
    trade(11, {
        Item.MemoryOfAMuchStrangerSelf: 1,
        Item.DirefulReflection: 1,
        Item.EmeticRevelation: 1,
        Item.AntiqueMystery: 1,
        Item.TempestuousTale: 7,
        Item.Wounds: -1,
        Item.Nightmares: 1 * utils.menace_multiplier(config.player.nightmares_reduction)
    })

    # w/o Cartographer, avg run is 22 actions
    # bonus of 170 TPs, 0.17 office failures, 1.3 wounds, 0.54 anathema

    trade(22, {
        Item.CausticApocryphon: 9,
        Item.TantalisingPossibility: 170 + 35,
        Item.FinBonesCollected: 1,
        Item.DeepZeeCatch: 1,
        Item.Wounds: 1.3,
        Item.GlimpseOfAnathema: 0.054
    })

    trade(22, {
        Item.GlimEncrustedCarapace: 1,
        Item.TantalisingPossibility: 170 + 495,
        Item.ShardOfGlim: 400,
        Item.FinBonesCollected: 1,
        Item.DeepZeeCatch: 1,
        Item.Wounds: 1.3,
        Item.GlimpseOfAnathema: 0.054
    })    

    trade(22, {
        Item.RoofChart: 40,
        Item.TantalisingPossibility: 170,
        Item.FinBonesCollected: 1,
        Item.DeepZeeCatch: 1,
        Item.Wounds: 1.3,
        Item.GlimpseOfAnathema: 0.054
    })

    trade(22, {
        Item.Anticandle: 10,
        Item.FragmentOfTheTragedyProcedures: 1,
        Item.RelicOfTheFifthCity: 10,
        Item.TantalisingPossibility: 170 + 35,
        Item.FinBonesCollected: 1,
        Item.DeepZeeCatch: 1,
        Item.Wounds: 1,
        Item.GlimpseOfAnathema: 0.054
    })
    
    trade(22, {
        Item.Anticandle: 10,
        Item.TempestuousTale: 10,
        Item.MagnificentDiamond: 5,
        Item.RelicOfTheFifthCity: 6,
        Item.TantalisingPossibility: 170 + 10,
        Item.FinBonesCollected: 1,
        Item.DeepZeeCatch: 1,
        Item.Wounds: 1,
        Item.GlimpseOfAnathema: 0.054
    })

    # Cartographer
    trade(22.3, {
        Item.OneiromanticRevelation: 1,
        Item.StormThrenody: 2,
        Item.PuzzlingMap: 1,
        Item.VolumeOfCollatedResearch: 6,

        # Office failures
        Item.FinBonesCollected: 1,
        Item.DeepZeeCatch: 1,

        Item.GlimpseOfAnathema: 0.05,
        Item.TantalisingPossibility: 152 + 10,
        Item.Wounds: 1.2
    })