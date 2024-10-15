from enums import *
from config import *

def add_trades(config: Config):
    add = config.add
    trade = config.trade

    for item, buy_price, sale_value in (
        (Item.MagisterialLager, -1, 1),
        (Item.TinOfZzoup, -5, 2),
        (Item.CrateOfIncorruptibleBiscuits, -12, 5),
        (Item.TinnedHam, -125, 62),
        # (Item.PairOfBalmoralBoots, -250, 125)

        (Item.AmbiguousEolith, -2, 1),
        (Item.UnidentifiedThighBone, -2, 1),
        # (Item.LithificationLiquid, -25, 12),
        # (Item.PatentOsteologicalSandAndWax, -25, 12),
        (Item.FossilisedForelimb, -85, 25)
    ):
        trade(0, { item: 1, Item.HinterlandScrip: buy_price })
        trade(0, { item: -1, Item.HinterlandScrip: sale_value })

    for item, sale_value in (
        # (Item.AmbiguousEolith, 1),
        (Item.FinalBreath, 1),
        (Item.HandPickedPeppercaps, 1),
        (Item.MovesInTheGreatGame, 1),
        (Item.NightsoilOfTheBazaar, 1),
        (Item.PotOfVenisonMarrow, 1),
        (Item.RoyalBlueFeather, 1),
        (Item.SolaceFruit, 1),
        (Item.SurveyOfTheNeathsBones, 1),
        (Item.TraceOfViric, 1),
        # (Item.UnidentifiedThighbone, 1),
        (Item.FemurOfAJurassicBeast, 2),
        (Item.HelicalThighbone, 2),
        # (Item.TinOfZzoup, 2),
        (Item.PreservedSurfaceBlooms, 3),
        (Item.CarvedBallOfStygianIvory, 5),
        # (Item.CrateOfIncorruptibleBiscuits, 5),
        (Item.KnobOfScintillack, 5),
        (Item.NicatoreanRelic, 5),
        (Item.SausageAboutWhichNoOneComplains, 5),
        (Item.TailfeatherBrilliantAsFlame, 5),
        (Item.ViennaOpening, 5),
        (Item.RailwaySteel, 19),
        (Item.UnlawfulDevice, 25),
        (Item.VitalIntelligence, 25),
        (Item.QueenMate, 50),
        (Item.EpauletteMate, 50),
        (Item.SapOfTheCedarAtTheCrossroads, 125),
        (Item.Stalemate, 125),
        (Item.CartographersHoard, 625),
    ):
        trade(0, { item: -1, Item.HinterlandScrip: sale_value })


    add({
        Item.HinterlandScrip: -200_000,
        Item.YourVeryOwnMiniatureHellworm: 1
    })