from enums import *
from utils import *

def add_trades(active_player, config):
    trade = config.trade

    # Licensed by Mr Stones

    trade(1, {
        Item.FlawedDiamond: -100,
        Item.HinterlandScrip: 30
    })

    trade(1, {
        Item.OstentatiousDiamond: -25,
        Item.CrateOfIncorruptibleBiscuits: 6
    })

    trade(1, {
        Item.MagnificentDiamond: -1,
        Item.TouchingLoveStory: 5.5 # assumes uniform 5 or 6
    })

    trade(1, {
        Item.FabulousDiamond: -1,
        Item.HinterlandScrip: 625,
        Item.StolenKiss: 2
    })
