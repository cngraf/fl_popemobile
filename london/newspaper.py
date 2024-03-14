from enums import *
from utils import *

def add_trades(active_player, config):
    trade = config.trade
    # Gossipy edition with maximum Salacious
    trade(13, {
        Item.WhirringContraption: -1,
        Item.ScrapOfIncendiaryGossip: -5,

        Item.Hedonist: 1,
        Item.JournalOfInfamy: 148,
        Item.SlightedAcquaintance: 1,
        Item.SulkyBat: 2
    })

    # Tawdry secrets without slighted 
    trade(13, {
        Item.WhirringContraption: -1,
        Item.JournalOfInfamy: 118,
        Item.SulkyBat: 2,
        Item.BottleOfBrokenGiant1844: 4
    })

    # Outlandish edition
    trade(13, {
        Item.WhirringContraption: -1,
        Item.JournalOfInfamy: 118,
        Item.ExtraordinaryImplication: 4
        # Item.Echo: 7.9 # 0.4 bats, 10 wine, -2.5 gossip
    })

    # Expose of Palaeontology
    # - 6 actions to get max RoaMF
    # - 13 actions base
    trade(6, {
        Item.CrypticClue: 100, # carpenter's granddaughter
        Item.FinBonesCollected: 3, # palaeo companion
        Item.WitheredTentacle: 3, # carnival
        Item.UnidentifiedThighbone: 2, # university
        Item.JetBlackStinger: 3, # ??? can also be tentacles?
        Item.PlasterTailBones: 1, # stalls
        Item.ResearchOnAMorbidFad: 6
    })

    trade(13, {
        Item.WhirringContraption: -1,
        Item.ResearchOnAMorbidFad: -6,

        Item.PieceOfRostygold: 500,
        Item.SurveyOfTheNeathsBones: 20 + 13 * 6,
        Item.HolyRelicOfTheThighOfStFiacre: 2
    })

    # Revenge cards -----------
    # Ignores cost to acquaintance
    trade(1, {
        Item.CardDraws: -1,
        Item.SlightedAcquaintance: -1,
        Item.PuzzleDamaskScrap: 1
    })

    trade(1, {
        Item.CardDraws: -1,
        Item.SlightedAcquaintance: -1,
        Item.NoduleOfTremblingAmber: 1
    })

    trade(1, {
        Item.CardDraws: -1,
        Item.SlightedAcquaintance: -1,
        Item.MagnificentDiamond: 1
    })

    # FATE Johnny Croak
    trade(1, {
        Item.CardDraws: -1,
        Item.SlightedAcquaintance: -1,
        Item.PuzzlingMap: 1
    })

    # FATE Johnny Croak
    trade(1, {
        Item.CardDraws: -1,
        Item.SlightedAcquaintance: -1,
        Item.AntiqueMystery: 1
    })
