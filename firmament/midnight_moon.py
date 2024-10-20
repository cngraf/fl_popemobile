import math
from enum import Enum, auto

from enums import *
import helper.utils as utils
from config import Config
from player import Player

def add_trades(config: Config):
    add = config.add
    trade = config.trade

    add({
        Item._FirmamentRoundTrip: -1,
        Item.Action: -50,
        Item._MidnightMoonAction: 50
    })

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
