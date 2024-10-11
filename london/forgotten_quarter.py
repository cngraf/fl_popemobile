import math
from enum import Enum, auto

from enums import *
import helper.utils as utils
from config import Config
from player import Player

def add_trades(config: Config):
    add = config.add

    add({
        Item.Action: -1,
        Item._ForgottenQuarterAction: 1
    })

    ########################################################
    #               Expedition Supplies
    ########################################################

    add({
        Item._ForgottenQuarterAction: -1,
        Item.WhisperedHint: -200,
        Item.CrateOfExpeditionSupplies: 1.4,
        Item.MapScrap: 0.6
    })

    add({
        Item._ForgottenQuarterAction: -1,
        Item.AppallingSecret: -10,
        Item.CrateOfExpeditionSupplies: 1,
    })

    add({
        Item._ForgottenQuarterAction: -1,
        Item.PageOfPrelapsarianArchaeologicalNotes: -10,
        Item.CrateOfExpeditionSupplies: 1,
    })

    add({
        Item._ForgottenQuarterAction: -4,
        Item.Echo: -10,
        Item.CrateOfExpeditionSupplies: 4,
    })

    add({
        Item._ForgottenQuarterAction: -1,
        Item.BottleOfStranglingWillowAbsinthe: -3,
        Item.CrateOfExpeditionSupplies: 1,
    })

    add({
        Item._ForgottenQuarterAction: -1,
        Item.PieceOfRostygold: -160,
        Item.CrateOfExpeditionSupplies: 1,
    })

    add({
        Item._ForgottenQuarterAction: -1,
        Item.MoonPearl: -160,
        Item.CrateOfExpeditionSupplies: 1,
    })

    add({
        Item._ForgottenQuarterAction: -1,
        Item.FavDocks: -3,
        Item.PieceOfRostygold: -50,
        Item.CrateOfExpeditionSupplies: 7,
    })

    add({
        Item._ForgottenQuarterAction: -3,
        Item.StrongBackedLabour: -1,
        Item.CrateOfExpeditionSupplies: 3
    })

    '''
    All expeditions take 1 action to begin, adds 1 own progress & 1 rivals progress
    Some take 1 action to finish, some take 2? unclear

    TODO: random events
    - Shrine of Deep Blue Heaven has rare success when starting
        - +2 additional progress => saves 1 action & 2 supplies

    - Airs 96+ for 4 progress / 1 supply
        - 0.05 rate
        - (24 + 1) actions + (24 * 3 + 1) supply = (24 * 3 + 4) progress
        - 25 actions + 73 supply = 76 progress
        - 1 action + 2.92 supply = 3.04 progress
        - nvm this is the wrong way to calculate it

    - Possibility of low-roll on Rivals Progress (min 9 actions)
    '''

    # Length 10
    # +3 three times
    # Good Airs in 3 rolls (aka get 96+ for "A Sign?" at least once):
    # for simplicity assume you always play -3/+3 option otherwise
    # 0.95 ** 3 = 0.86
    # 86% of the time:
    #   3x (-1/-3/3) = -3/-9/9
    # 14% of the time:
    #   1x (-1/-1/4) + 2x (-1/-3/3) = -3/-7/10

    add({
        Item._ForgottenQuarterAction: -3,
        Item.CrateOfExpeditionSupplies: -8.7,
        
        Item.FavCriminals: -1,
        Item.CrypticClue: 100,

        Item._ThievesCacheReward: 1
    })

    add({
        Item._ForgottenQuarterAction: -2,
        Item._ThievesCacheReward: -1,

        # TODO alterante reward rate + unpredictable treasure
        Item.Echo: 35
    })

    # Length 20
    # +3 six times, +1 once
    # 0.95 ** 7 = 0.70
    # actually only 6 chances, getting it on final roll doesn't save action
    # 78% of the time:
    #   6x (-1/-3/3) + 1x (-1/-1/1) = -7/-19/19
    # 22% of the time:
    #    1x (-1/-1/4) + 5x (-1/-3/3) = -6/-16/19
    # 23% chance:
    #
    add({
        Item._ForgottenQuarterAction: -6.8,
        Item.CrateOfExpeditionSupplies: -18.4,

        Item._ShrineOfDeepBlueHeavenReward: 1
    })

    add({
        Item._ForgottenQuarterAction: -2,
        Item._ShrineOfDeepBlueHeavenReward: -1,

        # TODO unpredicatable treasure
        Item.Echo: 70
    })

    add({
        Item._ForgottenQuarterAction: -2,
        Item._ShrineOfDeepBlueHeavenReward: -1,

        # TODO rare success, combine with other result
        Item.EyelessSkull: 1,
        Item.ExtraordinaryImplication: 1,
        Item.WhisperedHint: 100
    })

    # Chacolite Pagoda

    add({
        Item._ForgottenQuarterAction: -6.8,
        Item.CrateOfExpeditionSupplies: -18.4,

        Item._ChacolitePagodaReward: 1
    })

    add({
        Item._ForgottenQuarterAction: -2,
        Item._ChacolitePagodaReward: -1,

        Item.SearingEnigma: 1
    })

    # Stonefall Copse

    add({
        Item._ForgottenQuarterAction: -6.8,
        Item.CrateOfExpeditionSupplies: -18.4,

        Item._StonefallCopseReward: 1
    })

    add({
        Item._ForgottenQuarterAction: -2,
        Item._StonefallCopseReward: -1,

        Item.PuzzlingMap: 2,
        Item.DirefulReflection: 1,
        Item.NoduleOfWarmAmber: 250
    })

    # Length 30
    # 0.95 ** 9 = 0.6
    # +3 nine times, +2 once    
    # 63% of the time:
    #   9x (-1/-3/3) + 1x (-1/-2/2) = -10/-29/29
    # 37% of the time:
    #   1x (-1/-1/4) + 8x (-1/-3/3) + 1x (-1/-1/1) = -10/-26/29
    # need at least 2 airs to save an action.
    # simulation says 9.93, not gonna bother with that.

    # Tomb of the Silken Thread
    add({
        Item._ForgottenQuarterAction: -10,
        Item.CrateOfExpeditionSupplies: -27.9,

        Item._TombOfSilkenThreadReward: 1
    })

    add({
        Item._ForgottenQuarterAction: -2,
        Item._TombOfSilkenThreadReward: -1,

        Item.JudgementsEgg: 1,
        Item.ParabolaLinenScrap: 1
    })

    # Length 40
    # +3 thirteen times
    # 0.95 ** 12 = 0.54
    # 54% no airs:
    #   13x (-1/-3/3) = -13/-39/39
    # 46% 1 airs:
    #   1x (-1/-1/4) + 11x (-1/-3/3) + 1x (-1/-2/2) = -13/-36/39
    add({
        Item._ForgottenQuarterAction: -13,
        Item.CrateOfExpeditionSupplies: -37.6,

        Item.Nightmares: 1,
        Item._SanctuaryOfCrimsonPetalsReward: 1
    })

    # 17% rare success rate per wiki
    crimson_rare_success_rate = 0.17
    add({
        Item._ForgottenQuarterAction: -2,
        Item._SanctuaryOfCrimsonPetalsReward: -1,

        Item.PortfolioOfSouls: 1 * (1 - crimson_rare_success_rate),
        Item.BrightBrassSkull: 2 * (1 - crimson_rare_success_rate),
        Item.NightWhisper: 3 * crimson_rare_success_rate
    })    