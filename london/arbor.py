from enums import *
from utils import *
from config import Config

# TODO: loop into card requirement

def add_trades(config: Config):
    trade = config.trade
    player = config.player

    trade(9, {
        Item.C_Arbor: -1,
        Item.Attar: 13
    })

    trade(0, {
        Item.Attar: -1,
        Item.PresbyteratePassphrase: 1
    })

    trade(0, {
        Item.Attar: -1,
        Item.SwornStatement: 1
    })

    trade(1, {
        Item.Attar: -7,
        Item.DirefulReflection: 1
    })

    trade(1, {
        Item.Attar: -4,
        Item.EmeticRevelation: 1
    })

    trade(0, {
        Item.Attar: -3,
        Item.FavourInHighPlaces: 1
    })

    trade(3, {
        Item.C_Arbor: -1,
        Item.PresbyteratePassphrase: 7
    })

    trade(3, {
        Item.C_Arbor: -1,
        Item.SwornStatement: 7
    })

    # trade(3, {
    #     Item.Attar: 7
    # })