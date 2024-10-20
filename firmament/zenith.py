import math
from enum import Enum, auto

from enums import *
import helper.utils as utils
from config import Config
from player import Player

def add_trades(config: Config):
    add = config.add

    for i in range(0, 11):
        visit_length = 2 ** i
        add({
            Item._FirmamentRoundTrip: -1,
            Item.Action: -visit_length,
            Item._ZenithAction: visit_length,
        })

    add({
        Item._ZenithAction: -1,
        Item.RoofChart: -2,
        Item.SurveyOfTheNeathsBones: 10
    })

    add({
        Item._ZenithAction: -1,
        Item.RoofChart: -5,
        Item.GlassGazette: 5
    })

    # TODO add to bone market
    add({
        Item._ZenithAction: -1,
        Item.EyelessSkull: -1,
        Item.PanopticalSkull: 1
    })

    add({
        Item._ZenithAction: -1,
        Item.RelicOfTheFifthCity: -10,
        Item.NightsoilOfTheBazaar: 25,
        Item.LondonStreetSign: 6
    })

    add({
        Item._ZenithAction: -1,
        Item.MemoryOfMoonlight: -1,
        Item.RumourOfTheUpperRiver: 1,
        Item.Hillmover: 1
    })

    # Stacks new route
    add({
        Item.Action: -23.2,
        Item.TantalisingPossibility: 171,
        Item.CracklingDevice: 0.95,
        Item.RatworkMechanism: 4 * 0.95,
        Item.DevilboneDie: 4 * 0.95,
        Item.GlimpseOfAnathema: 0.05,
        Item.Nightmares: 1,
    })

    ################################################
    #               High Santa
    ################################################

    # Odds per wiki
    fixed_actions = 3
    stage1_actions = sum(2 *  1 - i * 0.025 for i in range(0,4))
    stage2_actions = sum(2 *  1 - i * 0.025 for i in range(4,8))
    stage3_actions = sum(2 *  1 - i * 0.025 for i in range(8,12))

    stage1_cards = sum(1 - i * 0.025 for i in range(0,4))
    stage2_cards = sum(1 - i * 0.025 for i in range(4,8))
    stage3_cards = sum(1 - i * 0.025 for i in range(8,12))

    avg_counterlight_passes = sum(1 - i * 0.025 for i in range(0, 12))
    # Not exact but close enough
    avg_memories = (avg_counterlight_passes * (850 + 100 * (avg_counterlight_passes + 1)/2))/1250
    add({
        Item.ViolantSights: 1,
        Item.Anticandle: -avg_counterlight_passes,
        Item._ZenithAction: -(3 + avg_counterlight_passes * 2),
        Item._ApproximateEchoValue: 12.50 * avg_counterlight_passes,
        Item.MemoryOfAMuchStrangerSelf: avg_memories
    })

    # # Deck model adds too much bloat in report
    # # Also not sure this actually ties out
    # violant_sky = sum((850 + i * 250) * 1 - (i * 0.025) for i in range(0, 12))
    # add({
    #     Item.ViolantSights: 1,
    #     Item.Anticandle: -12,
    #     Item._ZenithAction: -(3+stage1_actions+stage2_actions+stage3_actions),
    #     Item._HighSanctaDraw_Stage1: stage1_cards,
    #     Item._HighSanctaDraw_Stage2: stage2_cards,
    #     Item._HighSanctaDraw_Stage3: stage3_cards,
    #     Item.MemoryOfAMuchStrangerSelf: violant_sky / 1250
    # })

    # add({
    #     Item._HighSanctaDraw_Stage1: -9,

    #     Item._HighSanctaPlay_Stage1: 9,
    #     Item.CF_BleedingIn: 3,
    #     Item.CF_BorrowedScripts: 3,
    #     Item.CF_DrowsyExile: 3,
    #     Item.CF_FamilyAndLaw: 3,
    #     Item.CF_LawsUnwritten: 3,
    #     Item.CF_MoltenForests: 3,
    #     Item.CF_PungentSorrows: 3,
    #     Item.CF_Statuary: 3,
    #     Item.CF_StolenMarble: 3,
    # })

    # add({
    #     Item._HighSanctaPlay_Stage1: -1,
    #     Item.CF_BleedingIn: -1,
    #     Item.UnprovenancedArtefact: 1,
    #     Item.ExtraordinaryImplication: 2,
    #     Item.AnIdentityUncovered: 2
    # })

    # add({
    #     Item._HighSanctaPlay_Stage1: -1,
    #     Item.CF_BorrowedScripts: -1,
    #     Item.CausticApocryphon: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage1: -1,
    #     Item.CF_DrowsyExile: -1,
    #     Item.BazaarPermit: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage1: -1,
    #     Item.CF_FamilyAndLaw: -1,
    #     Item.BlackmailMaterial: 1,
    # })

    # add({
    #     Item._HighSanctaPlay_Stage1: -1,
    #     Item.CF_LawsUnwritten: -1,
    #     Item.NevercoldBrassSliver: 1250
    # })

    # add({
    #     Item._HighSanctaPlay_Stage1: -1,
    #     Item.CF_MoltenForests: -1,
    #     Item.EmeticRevelation: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage1: -1,
    #     Item.CF_PungentSorrows: -1,
    #     Item.PuzzleDamaskScrap: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage1: -1,
    #     Item.CF_Statuary: -1,
    #     Item.TouchingLoveStory: 5,
    # })

    # add({
    #     Item._HighSanctaPlay_Stage1: -1,
    #     Item.CF_StolenMarble: -1,
    #     Item.MemoryOfDistantShores: 25
    # })

    # add({
    #     Item._HighSanctaDraw_Stage2: -9,

    #     Item._HighSanctaPlay_Stage2: 9,
    #     Item.CF_Chained: 1,
    #     Item.CF_Consortion: 1,
    #     Item.CF_Coronation: 1,
    #     Item.CF_ScarredMemories: 1,
    #     Item.CF_UndyingWish: 1,
    #     Item.CF_UnsignedInTriplicate: 1,
    #     Item.CF_VelvetDark: 1,
    #     Item.CF_VoidsBreath: 1,
    #     Item.CF_Waning: 1,    
    # })

    # add({
    #     Item._HighSanctaPlay_Stage2: -1,
    #     Item.CF_Chained: -1,
    #     Item.UnlawfulDevice: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage2: -1,        
    #     Item.CF_Consortion: -1,
    #     Item.ScrapOfIncendiaryGossip: 25
    # })

    # add({
    #     Item._HighSanctaPlay_Stage2: -1,
    #     Item.CF_Coronation: -1,
    #     Item.NoduleOfTremblingAmber: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage2: -1,
    #     Item.CF_ScarredMemories: -1,
    #     # Item.SkyglassKnife: 1,
    #     Item.Echo: 3.20,
    #     Item.AppallingSecret: 62
    # })

    # add({
    #     Item._HighSanctaPlay_Stage2: -1,
    #     Item.CF_UndyingWish: -1,
    #     Item.AnIdentityUncovered: 1,
    #     Item.MysteryOfTheElderContinent: 20
    # })

    # add({
    #     Item._HighSanctaPlay_Stage2: -1,
    #     Item.CF_UnsignedInTriplicate: -1,
    #     Item.InfernalContract: 63,
    # })

    # add({
    #     Item._HighSanctaPlay_Stage2: -1,
    #     Item.CF_VelvetDark: -1,
    #     Item.Hillmover: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage2: -1,
    #     Item.CF_VoidsBreath: -1,
    #     Item.RelicOfTheSecondCity: 80,
    #     Item.BoneFragments: 50
    # })

    # add({
    #     Item._HighSanctaPlay_Stage2: -1,
    #     Item.CF_Waning: -1,
    #     Item.MemoryOfMoonlight: 1
    # })

    # add({
    #     Item._HighSanctaDraw_Stage3: -9,

    #     Item._HighSanctaPlay_Stage3: 9,
    #     Item.CF_BlackIce: 1,
    #     Item.CF_DiscardedHearts: 1,
    #     Item.CF_DrownedWars: 1,
    #     Item.CF_HandsAndBlades: 1,
    #     Item.CF_LoveAndTombstones: 1,
    #     Item.CF_MonthsPassing: 1,
    #     Item.CF_Reliquaries: 1,
    #     Item.CF_RescuedHungers: 1,
    #     Item.CF_Sloughing: 1,    
    # })


    # add({
    #     Item._HighSanctaPlay_Stage3: -1,
    #     Item.CF_BlackIce: -1,
    #     Item.MagnificentDiamond: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage3: -1,
    #     Item.CF_DiscardedHearts: -1,
    #     Item.OstentatiousDiamond: 25
    # })

    # add({
    #     Item._HighSanctaPlay_Stage3: -1,
    #     Item.CF_DrownedWars: -1,
    #     Item.TempestuousTale: 12,
    #     Item.ZeeZtory: 13
    # })

    # add({
    #     Item._HighSanctaPlay_Stage3: -1,
    #     Item.CF_HandsAndBlades: -1,
    #     Item.RelicOfTheFifthCity: 5
    # })

    # add({
    #     Item._HighSanctaPlay_Stage3: -1,
    #     Item.CF_LoveAndTombstones: -1,
    #     Item.SilentSoul: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage3: -1,
    #     Item.CF_MonthsPassing: -1,
    #     Item.MourningCandle: 5
    # })

    # add({
    #     Item._HighSanctaPlay_Stage3: -1,
    #     Item.CF_Reliquaries: -1,
    #     Item.CaveAgedCodeOfHonour: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage3: -1,
    #     Item.CF_RescuedHungers: -1,
    #     Item.SausageAboutWhichNoOneComplains: 1
    # })

    # add({
    #     Item._HighSanctaPlay_Stage3: -1,
    #     Item.CF_Sloughing: -1,
    #     Item.JustificandeCoin: 5
    # })
