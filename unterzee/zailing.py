from enums import *
from utils import *

def add_trades(active_player, zailing_epa, config):
    trade = config.trade

    # ballparking EPA for zailing with piracy
    trade(0, {
        Item.ZailingDraws: -1,
        Item.Echo: zailing_epa
    })

    # rounding up for overflow
    trade(2, {
        Item.ChasingDownYourBounty: -120,
        Item.StashedTreasure: 5500
    })

    # amortizing travel cost
    trade(0, {
        Item.StashedTreasure: -1250,
        Item.MourningCandle: 5
    })

    trade(0, {
        Item.StashedTreasure: -1250,
        Item.CaveAgedCodeOfHonour: 1
    })

    trade(0, {
        Item.StashedTreasure: -6250,
        Item.RelativelySafeZeeLane: 1
    })

    trade(0, {
        Item.StashedTreasure: -6250,
        Item.SaltSteppeAtlas: 1
    })

    trade(0, {
        Item.StashedTreasure: -31250,
        Item.FabulousDiamond: 1
    })

    # # optimistic 100% draw rate of chasing cards
    # # pessimistic no rare success
    # trade(0, {
    #     Item.HomeWatersZeeDraw: -1,
    #     Item.ChasingDownYourBounty: 8
    # })

    # trade(0, {
    #     Item.ShephersWashZeeDraw: -1,
    #     Item.ChasingDownYourBounty: 8.5
    # })

    # trade(0, {
    #     Item.StormbonesZeeDraw: -1,
    #     Item.ChasingDownYourBounty: 8.5
    # })

    # trade(0, {
    #     Item.SeaOfVoicesZeeDraw: -1,
    #     Item.ChasingDownYourBounty: 9
    # })

    # trade(0, {
    #     Item.SaltSteppesZeeDraw: -1,
    #     Item.ChasingDownYourBounty: 13.5
    # })

    # trade(0, {
    #     Item.PillaredSeaZeeDraw: -1,
    #     Item.ChasingDownYourBounty: 14.5
    # })

    # trade(0, {
    #     Item.StormbonesZeeDraw: -1,
    #     Item.ChasingDownYourBounty: 15.5
    # })

