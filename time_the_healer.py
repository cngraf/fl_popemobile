import math
from enum import Enum, auto

from enums import *
import helper.utils as utils
from config import Config
from player import Player


def add_trades(config: Config):
    add = config.add

    config.add({
        Item._VisitFromTimeTheHealer: -1,

        Item.AnEarnestOfPayment: 1,
        Item.ProfessionalPerk: 1,

        Item.FavourableCircumstance: 1, # TODO
        Item.FreeEvening: 5,

        Item.Wounds: -2,
        Item.Nightmares: -1,
        Item.Suspicion: -1,
        Item.Scandal: -1,

        Item._RatNoLonger: 1,

        #####################
        # Weekly Carousels
        #####################
        Item.FleetingRecollections: 1, # TODO
        Item.DelayUntilTheNextBoardMeeting: -1,
        Item.ViolantSights: -1,

        # Living story, drift of 1 day
        Item.ReportFromTheKhagansPalace: -7/8,
        Item.GiftFromBalmoral: 7/8,        


        # Item.RavagesOfParabolanWarfare: -10, # TODO
        # Item.MiredInMail: -99,

        ##### Stuff that is not worth the bloat
        # Item.AConsequenceOfYourAmbition: 1,
        # Item.ABeneficence: 1,
        # Item.RecentParticipantInAStarvedCulturalExchange: -1,
        # Item.GlowingViric: -1,
    })

    # free source of constraining qualities
    # without this, model sees them as required costs for TtH
    for lockout_quality in (
        Item.RavagesOfParabolanWarfare,
        Item.GenericBoneMarketExhaustion,
        Item.RecentParticipantInAStarvedCulturalExchange,
        Item.GlowingViric,
        Item.MiredInMail,
        Item.ReportFromTheKhagansPalace
    ):
        config.add({
            lockout_quality: 1
        })


    add({
        Item.AnEarnestOfPayment: -1,
        Item.Echo: 70
    })

    ############################
    # Professional Perks


    # Ballpark "reduce menace by half"
    add({
        Item.Action: -1,
        Item.ProfessionalPerk: -2,
        Item.Nightmares: -15
    })

    add({
        Item.Action: -1,
        Item.ProfessionalPerk: -2,
        Item.Wounds: -12
    })

    add({
        Item.Action: -1,
        Item.ProfessionalPerk: -2,
        Item.Scandal: -12
    })

    add({
        Item.Action: -1,
        Item.ProfessionalPerk: -2,
        Item.Suspicion: -12
    })

    add({
        Item.Action: -1,
        Item.ProfessionalPerk: -4,
        Item.TradeSecret: -12
    })


    add({
        Item.Action: -1,
        Item.ProfessionalPerk: -1,
        Item.HardEarnedLesson: 1,
        Item.HastilyScrawledWarningNote: 1,
        Item.ConfidentSmile: 1,
        Item.SuddenInsight: 1,
    })

    add({
        Item.Action: -10,
        Item.TradeSecret: -1,
        Item.SearingEnigma: 1,
        Item.AntiqueMystery: 5
    })

    add({
        Item.TradeSecret: -1,
        Item.Echo: 60
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


