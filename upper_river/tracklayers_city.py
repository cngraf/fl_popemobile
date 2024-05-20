import math
from enum import Enum, auto

from enums import *
import utils
from config import Config
from player import Player

def add_trades(config: Config):
    trade = config.trade

    # ballpark
    trade(1, {
        Item.HinterlandProsperity: 510
    })

    # Cashing in
    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.PuzzlingMap: 1
    })

    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.AmbiguousEolith: 15,
        Item.UnidentifiedThighbone: 5
    })

    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.NoduleOfTremblingAmber: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.LegalDocument: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.VitalIntelligence: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.NoduleOfTremblingAmber: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.CrystallizedEuphoria: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.VerseOfCounterCreed: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.LostResearchAssistant: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -1050,
        Item.BlackmailMaterial: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -6250,
        Item.HolyRelicOfTheThighOfStFiacre: 1,
        Item.VerseOfCounterCreed: 3,
        Item.ApostatesPsalm: 5
    })

    trade(1, {
        Item.HinterlandProsperity: -6250,
        Item.CaptivatingBallad: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -31250,
        Item.BottleOfFourthCityAirag: 5,
    })

    trade(1, {
        Item.HinterlandProsperity: -156000,
        Item.RumourmongersNetwork: 1,
    })

    trade(1, {
        Item.HinterlandProsperity: -156000,
        Item.VialOfMastersBlood: 1,
    })

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
    trade(11, {
        Item.SearingEnigma: 1
    })
    
    trade(11, {
        Item.PrimaevalHint: 1
    })

    