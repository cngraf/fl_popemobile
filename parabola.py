from enums import *
from utils import *

def add_trades(active_player, trade):
    trade(1, {
        Item.DropOfPrisonersHoney: 0 if active_player.profession == Profession.Silverer else -100,
        Item.ParabolaRoundTrip: 1
    })

    trade(2, {
        Item.BoneFragments: -1100,
        Item.ParabolanOrangeApple: 1
    })

    # with specific BaL ending
    # trade(2, {
    #     Item.BoneFragments: -500,
    #     Item.ParabolanOrangeApple: 1
    # })

    trade(2, {
        Item.BoneFragments: -100,
        Item.Hedonist: -21,
        Item.ParabolanOrangeApple: 2
    })

    # Hunting Pinewood Shark
    # TODO: check actual length of carousel

    # just stay there, ignore travel cost
    trade(6, {
        # Item.CardDraws: 6 * lost_draw_cost,
        Item.FinBonesCollected: 2,
        Item.FavDocks: 1,
        Item.RemainsOfAPinewoodShark: 1
    })

    # short trip, no cards missed
    trade(6, {
        Item.ParabolaRoundTrip: -1,
        Item.FinBonesCollected: 2,
        Item.FavDocks: 1,
        Item.RemainsOfAPinewoodShark: 1
    })

    # ------------------
    # Parabolan War
    # ------------------

    # Ballparked via wiki calculator @ 320 base stats and default values

    trade(72, {
        Item.ParabolanParable: 1
    })

    trade(72, {
        Item.RayDrenchedCinder: 1
    })

    trade(72, {
        Item.EdictsOfTheFirstCity: 1
    })

    trade(72, {
        Item.WaswoodAlmanac: 1
    })

    trade(72, {
        Item.ConcentrateOfSelf: 1
    })

    # --- The Waswood

    trade(0, {
        Item.AnIdentityUncovered: -4,
        Item.IncisiveObservation: -1,
        Item.CorrectiveHistorialNarrative: 1
    })

    trade(0, {
        Item.ExtraordinaryImplication: -4,
        Item.IncisiveObservation: -1,
        Item.RevisionistHistoricalNarrative: 1
    })