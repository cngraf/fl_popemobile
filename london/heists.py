from enums import *
from helper.utils import *
from config import Config

# TODO: loop into card requirement

def add_trades(config: Config):
    add = config.add

    ##################################################
    #                   Casing...
    ##################################################

    # creating dummy items to represent all-or-nothing trade

    # 1. Find the weakness...
    # 2. reduce ferocity (GW or KT 7/12)
    # 3. Sneak forward (Sh 180/300)
    # 4. claim prize

    # When is YOLO sneak forward better?
    # success needs to be higher than 50%, failure adds +2 Nightmares, ~1/3 action
    # nightmare_reduction = 0
    # nightmare_reduction_per_action = 6
    # nightmare_on_fail = 2 * (0.85 ** nightmare_reduction)
    # pass_rate = shadowy/380 * 0.6
    # avg_failures = (1.0/pass_rate) - 1
    # failure_action_cost = avg_failures * (1 + )
    # failure_action_cost = 1
    # ignoring the fact that each failure makes next check ~2% easier
    # 0 nightmare reduction, need 57% pass rate AKA 361 shadowy, or:
    # 1 & 356 shadowy
    # 2 & 350 shadowy
    # 3 & 346 shadowy
    # my PC has full BiS in free slots and another 13 from locked slots, and that's only 334.
    # not achievable for most players even at full BiS, short of boons
    # Verdict: Not Feasible

    for infos in (0, 1):
        for keys in (0, 1):
            add({
                Item.Action: -4 - infos - keys,
                Item._ParabolaRoundTrip: -1,
                Item._Heist15Casing: 1,
                Item.InsideInformation: infos,
                Item.IntriguingKey: keys
            })

    # Big Rat
    if (config.player.qualities.get(Item._AllianceWithBigRat, 0) > 0):
        add({
            Item.Action: -2,
            Item.TalkativeRattusFaber: -6,
            Item._Heist15Casing: 1
        })

    # Well-Planned Villainy
    # or the Gang of Hoodlums one
    add({
        Item.Action: -5,
        Item._Heist15Casing: 1
    })

    # TODO update this, actually 1 action + 1 favour society
    # also move it to proper file
    add({
        Item.Action: -2,
        Item.ConnectedTheDuchess: 50
    })

    # 0 info, 0 keys, 0 escape routes
    # Complete: 99886 (99.89%)
    # Imprisoned: 61 (0.06%)
    # Escaped: 53 (0.05%)
    # avg 5.5 actions on cards, 1 to start, 1 to claim prize
    add({
        Item.Action: - 6.5 - 1,
        Item._Heist15Casing: -1,
        Item.HidingPlaceOfAPeculiarItem: -1,
        Item.ConnectedTheDuchess: -1.7,
        Item.Suspicion: 1,
        Item._WaswoodHeistCashOut: 0.999,
        Item._ImprisonedInNewNegate: 0.0005
    })

    # 1 info
    # Complete: 99989 (99.99%)
    # Imprisoned: 3 (0.00%)
    # Escaped: 8 (0.01%)
    add({
        Item.Action: -5.5 - 1,
        Item._Heist15Casing: -1,
        Item.HidingPlaceOfAPeculiarItem: -1,
        Item.InsideInformation: -1,

        Item.ConnectedTheDuchess: -1.25,
        Item.Suspicion: 1,
        Item._WaswoodHeistCashOut: 1
    })

    # 1 key
    add({
        Item.Action: -6.25 - 1,
        Item._Heist15Casing: -1,
        Item.HidingPlaceOfAPeculiarItem: -1,
        Item.IntriguingKey: -1,
        
        Item.ConnectedTheDuchess: -1.5,
        Item.OstentatiousDiamond: 1.5,
        Item.Suspicion: 1,
        Item._WaswoodHeistCashOut: 0.999,
        Item._ImprisonedInNewNegate: 0.0005
    })

    # 1 key, 1 info
    add({
        Item.Action: -5.35 - 1,
        Item._Heist15Casing: -1,
        Item.HidingPlaceOfAPeculiarItem: -1,        
        Item.IntriguingKey: -1,
        Item.InsideInformation: -1,

        Item.ConnectedTheDuchess: -1.2,
        Item.OstentatiousDiamond: 1.25,
        Item.Suspicion: 1,
        Item._WaswoodHeistCashOut: 1
    })

    # 2 info
    # Total Runs: 100000
    # Complete: 99999 (100.00%)
    # Escaped: 1 (0.00%)
    add({
        Item.Action: -5.2 - 1,
        Item.HidingPlaceOfAPeculiarItem: -1,
        Item.InsideInformation: -1,
        Item._Heist15Casing: -1,

        Item.ConnectedTheDuchess: -1.1,
        Item.Suspicion: 1,
        Item._WaswoodHeistCashOut: 1
    })

    add({
        Item._WaswoodHeistCashOut: -1,
        Item.FalseHagiotoponym: 1,
        Item.ApostatesPsalm: 16
    })

    # add({
    #     Item._WaswoodHeistCashOut: -1,
    #     Item.CaptivatingBallad: 1,
    #     Item.TouchingLoveStory: 16
    # })

    add({
        Item._WaswoodHeistCashOut: -1,
        Item.FragmentOfTheTragedyProcedures: 1,
        Item.SwornStatement: 16
    })

    add({
        Item._WaswoodHeistCashOut: -1,
        Item.ChimericalArchive: 1,
        Item.NicatoreanRelic: 16
    })