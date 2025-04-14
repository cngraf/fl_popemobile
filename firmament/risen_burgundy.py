import math
from enum import Enum, auto

from enums import *
import helper.utils as utils
from config import Config
from player import Player

def add_trades(config: Config):
    add = config.add

    for i in range(0, 11):
        visit_length = 2 ** i
        add({
            Item._FirmamentRoundTrip: -1,
            Item.Action: -visit_length,
            Item._BurgundyAction: visit_length,
        })  

    add({
        Item._BurgundyAction: -38,
        Item._CardDraws: -100,

        Item.MakingWaves: 26,
        Item.TouchingLoveStory: 7,
        Item.ExtraordinaryImplication: 7,
        Item.CausticApocryphon: 5,
        Item.MortificationOfAGreatPower: 2.2,
        Item.MemoryOfAMuchStrangerSelf: 2.1,
        Item.CellarOfWine: 4,
        Item.MourningCandle: -14
    })

    # TODO: burgundy market, move to another file or sth
    add({
        Item.RatworkMechanism: -1,
        Item.MoonPearl: 1250
    })
