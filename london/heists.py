from enums import *
from utils import *
from config import Config

# TODO: loop into card requirement

def add_trades(config: Config):
    add = config.add

    # Casing is one of those qualities that's hard to model
    # it's zeroed out whenever you start the heist

    # # requires deal with big rat
    # add({
    #     Item.Action: -1,
    #     Item.Echo: -2.4,
    #     Item.Casing: 9
    # })

    # # slightly less at high shadowy?
    # # requires parabola
    # add({
    #     Item.Action: -4,
    #     Item.Casing: 28
    # })

    # # from Flit
    # # 1 action start heist, trades in Hiding Place
    # # 1 action per inside info, etc. you want to get
    # # want 12 GW, 12 MA
    # # 1 to begin the job
    # # N to build progress
    # # 1 to finish job
    # # that's it
    # # best case scenario is 1 + 3 + 1 = 5 actions

    # add({
    #     Item.Action: -7,
    #     Item.Casing: -15,
    #     Item.WaswoodHeistCashOut: 1
    # })

    # semi-conservative estimate of carousel
    # 5 actions + 100 honey => 28 Casing
    # 2 actions + 10 casing => 2 inside info
    # 7 actions + rest of casing => complete heist

    # add({
    #     Item.Action: -14,
    #     Item.DropOfPrisonersHoney: -100,
    #     Item.HidingPlaceOfAPeculiarItem: -1,
    #     Item.WaswoodHeistCashOut: 1
    # })

    # most aggressive strat w/ big rat
    # 1 action to start heist
    # 2 actions + 4.8 echoes => 18 casing
    # Per simulation
    # 6.8 actions to complete heist
    # 99.8 success rate
    # 0.6 cat bribes per run
    # ballpark cost of failure
    # 8.5 actions per failed run
    # additional 30 actions half the time for going to prison
    # 0.002 * (8 + 30 * 0.5)
    # that's about 0.05 addtl actions per run

    add({
        Item.Action: -(1 + 2 + 6.51 + (20 * 0.002)),
        Item.Echo: -4.8,
        Item.AppallingSecret: -6,
        Item.HidingPlaceOfAPeculiarItem: -1,
        Item.WaswoodHeistCashOut: 1 * 0.996
    })

    # parabolan casing with no big rat
    # 1 action to start heist
    # 4.65 actions => 28 casing (first parabola trip is free)
    # 1 action => buy key
    # 6.2 actions to complete heist

    # add({
    #     Item.Action: -12.85,
    #     Item.AppallingSecret: -3,
    #     Item.HidingPlaceOfAPeculiarItem: -1,
    #     Item.WaswoodHeistCashOut: 1
    # })

    # optimistic semi-aggro strat
    # 3 actions + 7.2 echoes => 27 casing
    # 1 action => inside info
    # 8 actions? => complete heist

    # add({
    #     Item.Action: -10.5,
    #     Item.Echo: -4.8,
    #     Item.HidingPlaceOfAPeculiarItem: -1,
    #     Item.WaswoodHeistCashOut: 1
    # })

    add({
        Item.WaswoodHeistCashOut: -1,
        Item.FalseHagiotoponym: 1,
        Item.ApostatesPsalm: 16
    })

    add({
        Item.WaswoodHeistCashOut: -1,
        Item.CaptivatingBallad: 1,
        Item.TouchingLoveStory: 16
    })

    add({
        Item.WaswoodHeistCashOut: -1,
        Item.FragmentOfTheTragedyProcedures: 1,
        Item.SwornStatement: 16
    })

    add({
        Item.WaswoodHeistCashOut: -1,
        Item.ChimericalArchive: 1,
        Item.NicatoreanRelic: 16
    })