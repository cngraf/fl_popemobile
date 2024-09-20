from enums import *
from utils import *
from config import Config

def add_trades(config: Config):
    add = config.add
    # return

    add({
        Item.Action: -1,
        Item.VerseOfCounterCreed: -3,
        Item.PalimpsestScrap: -10,
        Item.ApostatesPsalm: -7,

        Item.FalseHagiotoponym: 1
    })
    