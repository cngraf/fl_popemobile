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

        Item.BoneMarketExhaustion: -4, # done

        Item.RavagesOfParabolanWarfare: -10, # TODO
        Item.RecentParticipantInAStarvedCulturalExchange: -1, # TODO
        Item.GlowingViric: -1, # TODO
        Item.MiredInMail: -99,
        Item.AReportFromTheKhagansPalace: -1
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


