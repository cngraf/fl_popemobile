import math
from enum import Enum, auto

from enums import *
import utils
from config import Config
from player import Player


def add_trades(config: Config):
    add = config.add
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

    add({
        Item.RoofChart: -1,
        Item.MoonPearl: 253
    })

    # TODO organize echo sales
    add({
        Item.TantalisingPossibility: -1,
        Item.Echo: 0.1
    })

    add({
        Item.GlimpseOfAnathema: -1,
        Item.Echo: 312.5
    })

    add({
        Item.RelicOfTheFifthCity: -1,
        Item.Echo: 2.5
    })

    # Results from simulations/stacks2 using my own stats, mostly ~330/15
    # W/o cartographer unless required
    # ignoring items less than +/- 0.01 EPA i.e. bones and rats
    # also ignored menaces when they were less than 2 per run

    # TODO double check these. ran again and got somewhat diff results

    # Banned Works
    trade(23.2, {
        Item.CausticApocryphon: 8.55,
        Item.TantalisingPossibility: 210,
        Item.GlimpseOfAnathema: 0.045,
        Item.Wounds: 1,
        Item.Nightmares: 1
    })

    # Dead Stars 1
    trade(23, {
        Item.GlimEncrustedCarapace: 0.95,
        Item.TantalisingPossibility: 655,
        Item.ShardOfGlim: 380,
        Item.GlimpseOfAnathema: 0.045,
        Item.Wounds: 1,
        Item.Nightmares: 1,        
    })    

    # Dead Stars 2
    trade(23, {
        Item.RoofChart: 38,
        Item.TantalisingPossibility: 180,
        Item.GlimpseOfAnathema: 0.045,
        Item.Wounds: 1,
        Item.Nightmares: 1,        
    })

    # Precipice 1
    trade(23, {
        Item.Anticandle: 9.5,
        Item.FragmentOfTheTragedyProcedures: 0.95,
        Item.RelicOfTheFifthCity: 9.5,
        Item.TantalisingPossibility: 215,
        Item.GlimpseOfAnathema: 0.05,
        Item.Nightmares: 1,
    })
    
    # Precipice 2
    trade(23, {
        Item.Anticandle: 9.5,
        Item.TempestuousTale: 9.5,
        Item.TantalisingPossibility: 190,
        Item.RelicOfTheFifthCity: 5.7,
        Item.MagnificentDiamond: 4.7,
        Item.GlimpseOfAnathema: 0.05,
        Item.Nightmares: 1,  
    })

    # Cartographer
    trade(23.5, {
        Item.TantalisingPossibility: 171,
        Item.PuzzlingMap: 0.95,
        Item.OneiromanticRevelation: 0.95,
        Item.StormThrenody: 1.9,
        Item.VolumeOfCollatedResearch: 5.7,
        Item.GlimpseOfAnathema: 0.05,
        Item.Nightmares: 1,
    })

    # add({
    #     Item.Anticandle: -1,
    #     Item.Echo: 2.5
    # })