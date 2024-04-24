import math
from enum import Enum, auto

from enums import *
import utils
from config import Config
from player import Player


def add_trades(config: Config):
    trade = config.trade

    # Hallow's Exchange

    trade(0, {
        Item.NoduleOfWarmAmber: -1,
        Item.Stuiver: 1
    })


    for item, buy_price in (
        # The Flexile Peddler
        (Item.SampleOfRoofDrip, -4),
        (Item.StarvedExpression, -20),
        (Item.GlimEncrustedCarapace, -3000),

        # The Cenobitic Outfitter
        (Item.RoofChart, -100),
    ):
        trade(0, { item: 1, Item.HinterlandScrip: buy_price })

    for item, sale_value in (
        (Item.NoduleOfWarmAmber, 1),
        (Item.SampleOfRoofDrip, 2),
        (Item.StarvedExpression, 10),
        (Item.TempestuousTale, 10),
        (Item.RoofChart, 50),
        (Item.AscendedAmbergris, 51),
        (Item.CausticApocryphon, 250),
        (Item.MemoryOfAMuchStrangerSelf, 250),
        # (Item.MemoryOfMoonlight, 250),
    ):
        trade(0, { item: -1, Item.Stuiver: sale_value })

    
    # Ecdysis
    trade(11, {
        Item.MemoryOfAMuchStrangerSelf: 1,
        Item.DirefulReflection: 1,
        Item.EmeticRevelation: 1,
        Item.AntiqueMystery: 1,
        Item.TempestuousTale: 7,
        Item.Wounds: -1,
        Item.Nightmares: 1 * utils.menace_multiplier(config.player.nightmares_reduction)
    })

