from enums import *
from utils import *

def add_trades(active_player, trade):
    default_rare_success_rate = 0.05
    # Sets to 3
    # In practice probably slightly better w overcap
    trade(1, {
        Item.SeeingBanditryInTheUpperRiver: - (pyramid(8) - pyramid(3)),
        Item.Scandal: 12
    })

    # Card: Intervene in an Attack
    trade(1, {
        Item.SeeingBanditryInTheUpperRiver: -1,
        Item.InCorporateDebt: -1 * default_rare_success_rate,
        Item.PieceOfRostygold: 400
    })

    # -----
    # Board Member Stuff
    # -----

    # Tentacled Entrepreneur rotation
    trade(7, {
        Item.InCorporateDebt: -15,
        Item.HinterlandScrip: 10
    })

    # --------------
    # Shops
    # -------------

    trade(0, {
        Item.HinterlandScrip: -2,
        Item.UnidentifiedThighbone: 1,
    })

    trade(0, {
        Item.HinterlandScrip: -85,
        Item.FossilisedForelimb: 1
    })

    # ----- Selling
    trade(0, {
        Item.AmbiguousEolith: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.FinalBreath: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.HandPickedPeppercaps: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.MovesInTheGreatGame: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.NightsoilOfTheBazaar: -1,
        Item.HinterlandScrip: 1
    })


    trade(0, {
        Item.PotOfVenisonMarrow: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.RoyalBlueFeather: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.SolaceFruit: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.SurveyOfTheNeathsBones: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.UnidentifiedThighbone: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.PreservedSurfaceBlooms: -1,
        Item.HinterlandScrip: 3
    })

    trade(0, {
        Item.CarvedBallOfStygianIvory: -1,
        Item.HinterlandScrip: 5
    })

    trade(0, {
        Item.CrateOfIncorruptibleBiscuits: -1,
        Item.HinterlandScrip: 5
    })

    trade(0, {
        Item.KnobOfScintillack: -1,
        Item.HinterlandScrip: 5
    })

    trade(0, {
        Item.NicatoreanRelic: -1,
        Item.HinterlandScrip: 5
    })

    trade(0, {
        Item.TailfeatherBrilliantAsFlame: -1,
        Item.HinterlandScrip: 5
    })

    trade(0, {
        Item.ViennaOpening: -1,
        Item.HinterlandScrip: 5
    })

    trade(0, {
        Item.UnlawfulDevice: -1,
        Item.HinterlandScrip: 25
    })

    trade(0, {
        Item.VitalIntelligence: -1,
        Item.HinterlandScrip: 25
    })

    trade(0, {
        Item.QueenMate: -1,
        Item.HinterlandScrip: 50
    })


    trade(0, {
        Item.EpauletteMate: -1,
        Item.HinterlandScrip: 50
    })

    trade(0, {
        Item.SapOfTheCedarAtTheCrossroads: -1,
        Item.HinterlandScrip: 125
    })

    trade(0, {
        Item.Stalemate: -1,
        Item.HinterlandScrip: 125
    })

    trade(0, {
        Item.CartographersHoard: -1,
        Item.HinterlandScrip: 625
    })

