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
            Item._ZenithAction: visit_length,
        })

    add({
        Item._ZenithAction: -1,
        Item.RoofChart: -2,
        Item.SurveyOfTheNeathsBones: 10
    })

    add({
        Item._ZenithAction: -1,
        Item.RoofChart: -5,
        Item.GlassGazette: 5
    })

    # TODO add to bone market
    add({
        Item._ZenithAction: -1,
        Item.EyelessSkull: -1,
        Item.PanopticalSkull: 1
    })

    add({
        Item._ZenithAction: -1,
        Item.RelicOfTheFifthCity: -10,
        Item.NightsoilOfTheBazaar: 25,
        Item.LondonStreetSign: 6
    })

    add({
        Item._ZenithAction: -1,
        Item.MemoryOfMoonlight: -1,
        Item.RumourOfTheUpperRiver: 1,
        Item.Hillmover: 1
    })

    # Stacks new route
    add({
        Item.Action: -23.2,
        Item.TantalisingPossibility: 171,
        Item.CracklingDevice: 0.95,
        Item.RatworkMechanism: 4 * 0.95,
        Item.DevilboneDie: 4 * 0.95,
        Item.GlimpseOfAnathema: 0.05,
        Item.Nightmares: 1,
    })