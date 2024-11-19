from enums import *
from helper.utils import *

def add_trades(config):
    trade = config.trade
    player = config.player
    add = config.add

    add({
        Item._ParabolaAction: -1,
        Item._DiscoAction: 1
    })

    # for i in (1, 5, 10, 20):
    # add({
    #     Item._ParabolaRoundTrip: -1,
    #     Item.Action: -i,
    #     Item._DiscoAction: i
    # })

    # add({
    #     Item.Echo: -54,
    #     Item.DiscordantSoul: 1
    # })

    # TODO check action costs
    # HACK Amortizing GW loss, assuming +13 from gear
    add({
        Item._ParabolaRoundTrip: -1,
        Item.Action: -1,
        Item.DiscordantSoul: -1,

        Item.ParabolanResearch: 5,
        Item.BrilliantSoul: 111,
        Item.Soul: 555,
        Item.MemoryOfAnAnchorhold: 1
    })

    # 17.75e payout
    add({
        Item._DiscoAction: -1,
        Item.MemoryOfDiscordance: -1,
        Item.MemoryOfAnAnchorhold: -1,
        Item.AppallingSecret: 111,
        Item.ManiacsPrayer: 11
    })

    # -3.50  +20.7
    add({
        Item._DiscoAction: -1,
        Item.MemoryOfDiscordance: -1,
        Item.MemoryOfAnAnchorhold: -1,
        Item.MemoryOfMuchLesserSelf: -1,
        Item.MemoryOfDistantShores: -1,
        Item.MemoryOfLight: -1,

        Item.AntiqueMystery: 1,
        Item.ApostatesPsalm: 3,
        Item.ManiacsPrayer: 7
    })
