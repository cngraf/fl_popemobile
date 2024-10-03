from enums import *
from helper.utils import *
from config import Config

# TODO: loop into card requirement

def add_trades(config: Config):
    add = config.add

    # slightly less at high shadowy?
    add({
        Item.Action: -4,
        Item._ParabolaRoundTrip: -1,
        Item._Parabolan28Casing: 1
    })

    # TODO update this, actually 1 action + 1 favour society
    add({
        Item.Action: -2,
        Item.ConnectedTheDuchess: 50
    })

    add({
        Item.Action: -1,
        Item.Echo: -2.4,
        Item._BigRat9Casing: 1
    })

    add({
        Item.Action: -1,
        Item._BigRat9Casing: -2,
        Item._BeginYourHeist: 1
    })

    add({
        Item.Action: -1,
        Item._Parabolan28Casing: -1,
        Item._BeginYourHeist: 1
    })

    add({
        Item.Action: -2,
        Item._Parabolan28Casing: -1,
        Item.InsideInformation: 1,
        Item._BeginYourHeist: 1
    })

    add({
        Item.Action: -2,
        Item._Parabolan28Casing: -1,
        Item.IntriguingKey: 1,
        Item._BeginYourHeist: 1
    })

    # 0 info, 0 keys, 0 escape routes
    # Complete: 99886 (99.89%)
    # Imprisoned: 61 (0.06%)
    # Escaped: 53 (0.05%)    
    add({
        Item.Action: -6.5 - 1,
        Item._BeginYourHeist: -1,
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
        Item._BeginYourHeist: -1,
        Item.HidingPlaceOfAPeculiarItem: -1,
        Item.InsideInformation: -1,

        Item.ConnectedTheDuchess: -1.25,
        Item.Suspicion: 1,
        Item._WaswoodHeistCashOut: 1
    })

    # 1 key
    add({
        Item.Action: -6.25 - 1,
        Item._BeginYourHeist: -1,
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
        Item._BeginYourHeist: -1,
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
        Item._BeginYourHeist: -1,

        Item.ConnectedTheDuchess: -1.1,
        Item.Suspicion: 1,
        Item._WaswoodHeistCashOut: 1
    })

    add({
        Item._WaswoodHeistCashOut: -1,
        Item.FalseHagiotoponym: 1,
        Item.ApostatesPsalm: 16
    })

    add({
        Item._WaswoodHeistCashOut: -1,
        Item.CaptivatingBallad: 1,
        Item.TouchingLoveStory: 16
    })

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