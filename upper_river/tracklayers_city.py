import math
from enum import Enum, auto

from enums import *
import helper.utils as utils
from config import Config
from player import Player

def add_trades(config: Config):
    trade = config.trade
    add = config.add

    efficiency = 300

    # ballpark
    trade(1, {
        Item.HinterlandProsperity: 510
    })

    # TODO monte carlo how many actions it actually takes to get right card
    # # Cashing in
    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.PuzzlingMap: 1
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.AmbiguousEolith: 15,
    #     Item.UnidentifiedThighBone: 5
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.NoduleOfTremblingAmber: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.LegalDocument: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.VitalIntelligence: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.NoduleOfTremblingAmber: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.CrystallizedEuphoria: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.VerseOfCounterCreed: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.LostResearchAssistant: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -1050 + efficiency,
    #     Item.BlackmailMaterial: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -6250,
    #     Item.HolyRelicOfTheThighOfStFiacre: 1,
    #     Item.VerseOfCounterCreed: 3,
    #     Item.ApostatesPsalm: 5
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -6250,
    #     Item.CaptivatingBallad: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -31250,
    #     Item.BottleOfFourthCityAirag: 5,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -156000,
    #     Item.RumourmongersNetwork: 1,
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -156000,
    #     Item.VialOfMastersBlood: 1,
    # })

    # # amortized betray to crims
    # trade(1, {
    #     Item.HinterlandProsperity: -500_000,
    #     Item.JournalOfInfamy: 10_000
    # })

    # trade(1, {
    #     Item.HinterlandProsperity: -500_000,
    #     Item.DubiousTestimony: 10_000
    # })

    # Communing

    # Needs 15 in 3 advanced stats to 100%

    def commune(stat: Item, dc: int, reward: Item):
        config.challenge_trade(stat, dc,
            cost={
                Item.Action: -1
            },
            on_pass={
                reward: 1
            },
            on_fail={
                Item.Nightmares: 2
            }
        )

    commune(Item.MonstrousAnatomy, 10, Item.TheMindsAscent1)
    commune(Item.ShapelingArts, 10, Item.TheMindsAscent1)
    commune(Item.KatalepticToxicology, 10, Item.TheMindsAscent1)

    commune(Item.ArtisanOfTheRedScience, 10, Item.TheMindsAscent2)
    commune(Item.Zeefaring, 10, Item.TheMindsAscent2)
    commune(Item.StewardOfTheDiscordance, 4, Item.TheMindsAscent2)

    commune(Item.Mithridacy, 10, Item.TheMindsAscent3)
    commune(Item.Glasswork, 10, Item.TheMindsAscent3)
    commune(Item.APlayerOfChess, 10, Item.TheMindsAscent3)

    add({
        Item.Action: -2,
        Item.TheMindsAscent1: -2,
        Item.TheMindsAscent2: -3,     
        Item.TheMindsAscent3: -4,     
        Item.SearingEnigma: 1
    })
    
    add({
        Item.Action: -2,
        Item.TheMindsAscent1: -2,
        Item.TheMindsAscent2: -3,     
        Item.TheMindsAscent3: -4,     
        Item.PrimaevalHint: 1
    })
    