import math
from enum import Enum, auto

from enums import *
import utils
from config import Config
from player import Player


def add_trades(config: Config):
    config.add({
        Item.VisitFromTimeTheHealer: -1,

        # Item.FavourableCircumstance: 1, # TODO
        # Item.FreeEvening: 5, # TODO
        # Item.AConsequenceOfYourAmbition: 1, # TODO
        # Item.FleetingRecollections: 1, # TODO
        # Item.AGiftFromBalmoral: 1, # TODO
        # # Item.ABeneficence: 1,

        # Item.Wounds: -2,
        # Item.Nightmares: -1,
        # # Item.Suspicion: -1,
        # Item.Scandal: -1,

        # # Item.BoneMarketExhaustion: -4, # done

        # Item.RavagesOfParabolanWarfare: -10, # TODO
        # Item.RecentParticipantInAStarvedCulturalExchange: -1, # TODO
        # Item.GlowingViric: -1, # TODO
        # Item.MiredInMail: -99,
        # Item.AReportFromTheKhagansPalace: -1,

        Item.DelayUntilTheNextBoardMeeting: -1,

        # Item._BoneMarketRotation: 1,
        
        # # 6 weeks, 2 demands per week => refresh 1/3 capacity per week
        # # 0 to 65k
        # Item.SoftRatMarketSaturation1: -65_000 / 3,
        # Item.SaintlyRatMarketSaturation1: -65_000 / 3,
        # Item.MaudlinRatMarketSaturation1: -65_000 / 3,
        # Item.InscrutableRatMarketSaturation1: -65_000 / 3,
        # Item.TempestuousRatMarketSaturation1: -65_000 / 3,
        # Item.IntricateRatMarketSaturation1: -65_000 / 3,

        # # 65k to 180k
        # Item.SoftRatMarketSaturation2: -115_000 / 3,
        # Item.SaintlyRatMarketSaturation2: -115_000 / 3,
        # Item.MaudlinRatMarketSaturation2: -115_000 / 3,
        # Item.InscrutableRatMarketSaturation2: -115_000 / 3,
        # Item.TempestuousRatMarketSaturation2: -115_000 / 3,
        # Item.IntricateRatMarketSaturation2: -115_000 / 3,        
   
    })

    # free source of constraining qualities
    # without this, model sees them as required costs for TtH
    for lockout_quality in (
        Item.RavagesOfParabolanWarfare,
        Item.GenericBoneMarketExhaustion,
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


