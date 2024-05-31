import math
from enum import Enum, auto

from enums import *
import utils
from config import Config
from player import Player


def add_trades(config: Config):
    config.add({
        Item.VisitFromTimeTheHealer: -1,

        Item.FavourableCircumstance: 1, # TODO
        Item.FreeEvening: 5, # TODO
        Item.AConsequenceOfYourAmbition: 1, # TODO
        Item.FleetingRecollections: 1, # TODO
        Item.AGiftFromBalmoral: 1, # TODO
        # Item.ABeneficence: 1,

        Item.Wounds: -2,
        Item.Nightmares: -1,
        Item.Suspicion: -1,
        Item.Scandal: -1,

        # Item.BoneMarketExhaustion: -4, # done

        Item.RavagesOfParabolanWarfare: -10, # TODO
        Item.RecentParticipantInAStarvedCulturalExchange: -1, # TODO
        Item.GlowingViric: -1, # TODO
        Item.MiredInMail: -99,
        Item.AReportFromTheKhagansPalace: -1,

        # 0 to 50k
        Item.RatMarketWeek1ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek2ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek3ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek4ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek5ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek6ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek7ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek8ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek9ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek10ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek11ExhaustionStage1: -50_000 / 12,
        Item.RatMarketWeek12ExhaustionStage1: -50_000 / 12,

        # 50k to 80k
        Item.RatMarketWeek1ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek2ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek3ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek4ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek5ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek6ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek7ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek8ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek9ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek10ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek11ExhaustionStage2: -30_000 / 12,
        Item.RatMarketWeek12ExhaustionStage2: -30_000 / 12,

        # 80k to 170k
        Item.RatMarketWeek1ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek2ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek3ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek4ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek5ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek6ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek7ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek8ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek9ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek10ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek11ExhaustionStage3: -90_000 / 12,
        Item.RatMarketWeek12ExhaustionStage3: -90_000 / 12,          
    })

    # free source of constraining qualities
    # without this, model sees them as required costs for TtH
    for lockout_quality in (
        Item.RavagesOfParabolanWarfare,
        Item.BoneMarketExhaustion,
        Item.RecentParticipantInAStarvedCulturalExchange,
        Item.GlowingViric,
        Item.MiredInMail,
        Item.AReportFromTheKhagansPalace
    ):
        config.add({
            lockout_quality: 1
        })

# Time-gated stuff
# Lots missing

# # Just gonna comment this out for now
# # it will only confuse things until the non-exlusive options are settled

# def rewards_of_ambition(treasure):
#     if treasure == Treasure.NoTreasure:
#         return {}
#     # Bag a Legend
#     elif treasure == Treasure.VastNetworkOfConnections:
#         return {
#             Item.ParabolaLinenScrap: 1,
#             Item.HinterlandScrip: 5,
#             Item.Nightmares: -5,
#             Item.BraggingRightsAtTheMedusasHead: 5
#         }
#     elif treasure == Treasure.SocietyOfTheThreeFingeredHand:
#         return {
#             Item.SearingEnigma: 1,
#             Item.Nightmares: -5,
#             Item.BraggingRightsAtTheMedusasHead: 5
#         }
#     elif treasure == Treasure.WingedAndTalonedSteed:
#         return {
#             Item.NightWhisper: 1,
#             Item.Wounds: -5,
#             Item.BraggingRightsAtTheMedusasHead: 5
#         }
#     elif treasure == Treasure.LongDeadPriestsOfTheRedBird:
#         return {
#             Item.PrimaevalHint: 1,
#             Item.Wounds: -5,
#             Item.BraggingRightsAtTheMedusasHead: 5
#         }
#     # Hearts Desire
#     elif treasure == Treasure.TheRobeOfMrCards:
#         return {
#             Item.FragmentOfTheTragedyProcedures: 1,
#             Item.Suspicion: -5
#         }
#     elif treasure == Treasure.NewlyCastCrownOfTheCityOfLondon:
#         return {
#             Item.BottleOfFourthCityAirag: 1,
#             Item.Scandal: -5
#         }
#     elif treasure == Treasure.LeaseholdOnAllOfLondon:
#         return {
#             Item.SearingEnigma: 1,
#             Item.Wounds: -5
#         }    
#     elif treasure == Treasure.PalatialHomeInTheArcticCircle:
#         return {
#             Item.NightWhisper: 1,
#             Item.Nightmares: -5
#         }
#     elif treasure == Treasure.TheRobeOfMrCards:
#         return {
#             Item.PrimaevalHint: 1,
#             Item.Nightmares: -5
#         }
#     elif treasure == Treasure.FalseStartOfYourOwn:
#         return {
#             Item.SearingEnigma: 1,
#             Item.Nightmares: -5
#         }
#     elif treasure == Treasure.KittenSizedDiamond:
#         return {
#             Item.PrimaevalHint: 1,
#             Item.Wounds: -5,
#             # ???
#             Item.OstentatiousDiamond: -1,
#             Item.MagnificentDiamond: 1
#         }
#     elif treasure == Treasure.BloodiedTravellingCoatOfMrCups:
#         return {
#             Item.BlackmailMaterial: 1,
#             Item.Nightmares: -5
#         }
#     elif treasure == Treasure.YourLovedOneReturned:
#         return {
#             Item.PrimaevalHint: 1,
#             Item.Nightmares: -5
#         }


