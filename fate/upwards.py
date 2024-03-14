from enums import *
from utils import *

def add_trades(active_player, config):
    trade = config.trade
    # TODO: confirm all of this

    trade(9, {
        Item.CartographersHoard: -1,
        Item.FivePointedRibcage: 1
    })

    trade(7, {
        Item.FavourInHighPlaces: -1,
        Item.CartographersHoard: -1,
        Item.FivePointedRibcage: 1
    })

    trade(9, {
        Item.PentagrammicSkull: 1,
        Item.BoneFragments: 1900
    })

    trade(7, {
        Item.FavourInHighPlaces: -1,
        Item.PentagrammicSkull: 1,
        Item.BoneFragments: 1900
    })
