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

    # Results from simulations/stacks2 using my own stats, mostly ~330/15
    # W/o cartographer unless required
    # ignoring items less than +/- 0.01 EPA i.e. bones and rats

    # Banned Works
    trade(24.2, {
        Item.CausticApocryphon: 8.5,
        Item.TantalisingPossibility: 230,
        Item.Nightmares: 1,
        Item.GlimpseOfAnathema: 0.05
    })

    # Dead Stars 1
    trade(24.1, {
        Item.GlimEncrustedCarapace: 0.95,
        Item.TantalisingPossibility: 650,
        Item.ShardOfGlim: 400,
        Item.Nightmares: 1,
        Item.GlimpseOfAnathema: 0.05
    })    

    # Dead Stars 2
    trade(24.1, {
        Item.RoofChart: 40,
        Item.TantalisingPossibility: 170,
        Item.GlimpseOfAnathema: 0.05
    })

    # Precipice 1
    trade(23.2, {
        Item.Anticandle: 9.4,
        Item.FragmentOfTheTragedyProcedures: 0.94,
        Item.RelicOfTheFifthCity: 9.4,
        Item.TantalisingPossibility: 200,
        Item.Nightmares: 0.5,
        Item.GlimpseOfAnathema: 0.06
    })
    
    # Precipice 2
    trade(23.2, {
        Item.Anticandle: 9.4,
        Item.TempestuousTale: 9.4,
        Item.TantalisingPossibility: 175,
        Item.RelicOfTheFifthCity: 5.6,
        Item.MagnificentDiamond: 4.7,
        Item.Nightmares: 0.5,
        Item.GlimpseOfAnathema: 0.06
    })

    # Cartographer
    trade(23.5, {
        Item.TantalisingPossibility: 205,
        Item.PuzzlingMap: 0.94,
        Item.OneiromanticRevelation: 0.94,
        Item.StormThrenody: 1.88,
        Item.VolumeOfCollatedResearch: 5.65,
        Item.GlimpseOfAnathema: 0.06,
        Item.Nightmares: 1
    })