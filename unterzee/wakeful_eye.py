from enums import *
from utils import *

def add_trades(active_player, config):
    trade = config.trade

    # trade(1, {
    #     Item.Echo: -25,
    #     Item.Tribute: 10
    # })

    # trade(1, {
    #     Item.MagnificentDiamond: -1,
    #     Item.Tribute: 5
    # })

    # trade(1, {
    #     Item.PuzzleDamaskScrap: -1,
    #     Item.Tribute: 5
    # })

    # trade(1, {
    #     Item.CellarOfWine: -1,
    #     Item.Tribute: 5
    # })

    trade(1, {
        Item.FavBohemians: -7,
        Item.Tribute: 11
    })

    trade(1, {
        Item.FavChurch: -7,
        Item.Tribute: 11
    })

    trade(1, {
        Item.FavCriminals: -7,
        Item.Tribute: 11
    })

    trade(1, {
        Item.FavDocks: -7,
        Item.Tribute: 11
    })

    trade(1, {
        Item.FavSociety: -7,
        Item.Tribute: 11
    })

    # trade(1, {
    #     Item.MemoryOfLight: -50,
    #     Item.Tribute: 10
    # })

    # trade(1, {
    #     Item.MountainSherd: -1,
    #     Item.Tribute: 35
    # })

    # trade(1, {
    #     Item.RoyalBlueFeather: -16,
    #     Item.Tribute: 4
    # })

    # trade(1, {
    #     Item.CorrespondencePlaque: -50,
    #     Item.Tribute: 10
    # })

    # trade(1, {
    #     Item.StrongBackedLabour: -1,
    #     Item.Tribute: 2
    # })

    ## ------------
    ## Court of the Wakeful Eye Grind
    ## ------------

    # Just make it one big blob
    # Can't be arsed to figure out the 240/260 leftovers thing
    # 14 actions = 2x the following
    # - 1 action to dock
    # - 2 actions in home waters
    # - 4 actions in shephers wash

    trade(14 + 12.65, {
        Item.HomeWatersZeeDraw: 4,
        Item.ShephersWashZeeDraw: 8,
        # Psuedo item represents tribute cap of 260
        Item.Tribute: -253,
        Item.NightWhisper: 12.65
    })