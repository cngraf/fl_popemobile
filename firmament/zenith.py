import math
from enum import Enum, auto

from enums import *
import utils
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