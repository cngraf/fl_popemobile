from enums import *
from helper.utils import *

def add_trades(config):
    trade = config.trade
    default_rare_success_rate = 0.05

    config.add({
        Item.Action: -2,
        Item._UpperRiverRoundTrip: 1,
        Item.RumourOfTheUpperRiver: 2
    })

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
        Item.UnidentifiedThighBone: 1,
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
        Item.UnidentifiedThighBone: -1,
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

    # Palaeontological Discoveries

    trade(0, {
        Item.PalaeontologicalDiscovery: -25,
        Item.LeviathanFrame: 1
    })

    trade(0, {
        Item.PalaeontologicalDiscovery: -5,
        Item.MammothRibcage: 1
    })

    trade(0, {
        Item.PalaeontologicalDiscovery: -5,
        Item.SabreToothedSkull: 1
    })

    trade(0, {
        Item.PalaeontologicalDiscovery: -4,
        Item.FossilisedForelimb: 2
    })
    
    trade(0, {
        Item.PalaeontologicalDiscovery: -3,
        Item.HumanRibcage: 2,
        Item.HumanArm: 4,
        Item.TraceOfTheFirstCity: 5
    })

    trade(0, {
        Item.PalaeontologicalDiscovery: -2,
        Item.HelicalThighbone: 6,
        Item.KnottedHumerus: 4
    })

    trade(0, {
        Item.PalaeontologicalDiscovery: -2,
        Item.ThornedRibcage: 2,
    })

    trade(0, {
        Item.PalaeontologicalDiscovery: -1,
        Item.HornedSkull: 1
    })

    trade(0, {
        Item.PalaeontologicalDiscovery: -1,
        Item.FemurOfAJurassicBeast: 5,
    })

    trade(0, {
        Item.PalaeontologicalDiscovery: -1,
        Item.BoneFragments: 1250,
    })