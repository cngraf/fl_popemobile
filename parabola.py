from enums import *
from utils import *

def add_trades(active_player, config):
    trade = config.trade
    add = config.add

    # TODO
    add({
        Item.RootAction: -1,
        Item.ParabolaAction: 1
    })

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
    # lengths per wiki

    if (config.player.profession == Profession.MonsterHunter):
        trade(8, {
            Item.FinBonesCollected: 2,
            Item.FavDocks: 1,
            Item.RemainsOfAPinewoodShark: 1
        })
    else:    
        trade(12, {
            Item.FinBonesCollected: 2,
            Item.FavDocks: 1,
            Item.RemainsOfAPinewoodShark: 1
        })

    # Location in the Neath
    
    # depends on shadowy, ~4 actions @ 315
    # slightly less at high shadowy
    add({
        Item.ParabolaAction: -4,
        Item.Casing: 28
    })

    # Waswood Water => Particular Treaure
    # probably more like 4.5 actions.
    # DC is 180 + 20 * (Ferocity - Scouting)
    # 14 ferocity => DC 460 => 41% @ 315 shadowy
    # you get +2 scouting per sneak fail, +10 per advanced skill success
    # Stategy 1
    # + 10 Scouting, then attempt until success
    # first attempt is 0.72, then 0.86, then 1.0
    # so expected action cost is 2 + 1 + 1 + (0.28) + (0.28 * 0.14) = ~4.3
    # Strategy 2
    # YOLO it until success
    # first attempt is .41, second is 0.45, third is 0.5
    # works out to be about the same, ballbark to 1/0.43, ~4.3 actions total
    # just do the first one since it's lower variance?

    add({
        Item.ParabolaAction: -4,
        Item.FlaskOfWaswoodSpringWater: -1,
        Item.HidingPlaceOfAPeculiarItem: 1
    })

    # TODO: different file
    add({
        Item.RootAction: -1,
        Item.FlaskOfWaswoodSpringWater: -1,
        Item.DropOfPrisonersHoney: 650,
        Item.Scandal: 1
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