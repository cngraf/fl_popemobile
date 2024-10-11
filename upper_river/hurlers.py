from enums import *
from helper.utils import *

def add_trades(config):
    add = config.add
    trade = config.trade

    for i in range(0, 7):
        visit_length = 2 ** i
        add({
            Item._UpperRiverRoundTrip: -1,
            Item.Action: -1 * visit_length,
            Item._HurlersAction: visit_length,
        })


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

    # TODO get actual costs & rates
    add({
        Item._HurlersAction: -4,
        Item.FoxfireCandleStub: -100,

        Item.Wounds: 4,
        Item.Nightmares: 4,
        Item.UnidentifiedThighBone: 2,
        Item.DiscordantLaw: 1
    })
