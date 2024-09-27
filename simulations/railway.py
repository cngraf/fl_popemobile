import random
import sys
import math
from collections import defaultdict
from enum import Enum, auto
import utils
from enums import *
from simulations.item_conversions import conversion_rate, estimated_conversion_rate
from simulations.models import *
from simulations.models import GameState

default_alt_pass_rate = 0.05
default_alt_fail_rate = 0.05

class RailwayState(GameState):
    def __init__(self, location: Location):
        super().__init__(max_hand_size=5)
        self.location = location
        self.ev_threshold = 5.68
        self.scrip_threshold_multiplier = 1.2

        self.skip_favour_inputs = False
        self.skip_econ_inputs = False

    def ev_from_item(self, item, val: int):
        # if item == Item.SeeingBanditryInTheUpperRiver:
        #     if self.banditry_level() > 5:
        #         return val * -3

        scrip_value = conversion_rate(item, Item.HinterlandScrip)
        echo_value = conversion_rate(item, Item.Echo)

        # if item == Item.FavCriminals:
        #     scrip_value = 10

        if item == Item.DispositionOfYourHellworm:
            return val * 7

        if item == Item.SeeingBanditryInTheUpperRiver:
            return val * -2

        if item == Item.HinterlandScrip:
            scrip_value = 1

        scrip_value *= self.scrip_threshold_multiplier

        if item == Item.Echo:
            echo_value = 1

        scrip_to_echo_value = scrip_value * 63.5/125

        echo_value = max(echo_value, scrip_to_echo_value)
        if echo_value != 0:
            return val * echo_value
        else:
            return val * conversion_rate(item, Item._ApproximateEchoValue)
    
    def banditry_level(self):
        return self.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver)

    def step(self):
        # TODO implement refill as a general action w/ discard logic
        if len(self.hand) == 0:
            while len(self.hand) < self.max_hand_size:
                self.draw_card()

        best_card, best_action, best_action_ev = self.find_best_action()

        if best_action:
            if best_action_ev >= self.ev_threshold or best_card.autofire:
                result = best_action.perform(self)
                self.actions += best_action.action_cost
                self.action_result_counts[best_action][result] += 1

                if best_card is not None:
                    self.card_play_counts[best_card] += 1
                    if best_card in self.hand:
                        self.hand.remove(best_card)  
            else:
                if len(self.hand) == self.max_hand_size:
                    card_to_discard = min(self.hand, key=lambda card: card.weight)
                    self.hand.remove(card_to_discard)
                while len(self.hand) < self.max_hand_size:
                    self.draw_card()

        self.hand = [card for card in self.hand if card.can_draw(self)]

        if self.actions >= 100:
            self.status = "Complete"


'''
TODO
- Hellworm

# Skip cards and actions that are avoidable or non-repeatable

# Part of external carousels/storylines
    An Alteration
    An Opulent Railway Carriage
    Find a quiet corner to eat your (dish)
    Is he here too? Even here?
    Stop That Stove!
    Tending to the Allotment
    That Which was Taken (Upper River)
    The Clay Highwayman's Gang 2 (implement eventually)
    The Return of the Gondolier
    Who is the Clay Highwayman?
    The Incident of the Honey-Mazed Bear
    The Bear, Again
    Something is Landing
        technically not avoidable, -1 action/day

# Bad? cards added by non-essential item
    Tomb Colonist Tour
    Canal Workers on the Upper River
    God's Editors at Burrow-Infra-Mump
        might be worthwhile still, check back
    Upper River Artistry

# Replaceable with better cards
    Cells outside the City
    Listen to Rumours of Smuggling

# Retired or require WQ
    Tucked at the Back of a Freight Car
    An Embarrassment of Snitches
    At the Bottom of a Pit that Used to be a Hill
    Atop the Railway Shed
    Lines of Communication
    Steel and sabotage

# Any actions that meet the above critera, too many to list
# Anything involving cabinet noir cash-outs

'''

class UpperRiverCard(OpportunityCard):
    def __init__(self, name):
        super().__init__(name)
        self.free_discard = True



################################################################################
###                        A Disillusioned Fungiculturalist                  ###
################################################################################

class DisillusionedFungiculturalist(UpperRiverCard):
    def __init__(self):
        super().__init__("A Disillusioned Fungiculturalist")
        self.actions = [
            BuyMushroomsWithNightsoil(),
            HelpBringInHisCrop(),
            InquireAboutSpecialHarvest()
        ]
        self.weight = 0.8  # Infrequent Frequency
    
    def can_draw(self, state: RailwayState):
        return True  # This card is available in Upper River


class BuyMushroomsWithNightsoil(Action):
    def __init__(self):
        super().__init__("Buy already-picked mushrooms with Nightsoil")
    
    def can_perform(self, state: RailwayState):
        return state.skip_econ_inputs or state.get(Item.NightsoilOfTheBazaar) >= 10
    
    def pass_items(self, state: RailwayState):
        return {
            Item.HandPickedPeppercaps: 21,
            Item.NightsoilOfTheBazaar: -10
        }

class HelpBringInHisCrop(Action):
    def __init__(self):
        super().__init__("Help bring in his crop")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.Respectable, 0) > 0
    
    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(1, state.outfit.kataleptic_toxicology)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.HandPickedPeppercaps: 10
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.HandPickedPeppercaps: 1,
            Item.Wounds: 1  # Wounds increase on failure
        }

class InquireAboutSpecialHarvest(Action):
    def __init__(self):
        super().__init__("Inquire about a 'special harvest'")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.FavoursCriminals, 0) >= 1
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavCriminals) >= 1
    
    def pass_items(self, state: RailwayState):
        return {
            Item.KnobOfScintillack: 4,
            Item.FavCriminals: -1,
            Item.SeeingBanditryInTheUpperRiver: 2  # CP increase for seeing banditry
        }


################################################################################
###                          A Jurisdictional Dispute                        ###
################################################################################

class JurisdictionalDispute(UpperRiverCard):
    def __init__(self):
        super().__init__("A Jurisdictional Dispute")
        self.actions = [
            AttemptFairCompromise(),
            SideWithBishopSouthwark(),
            SideWithBishopFiacres(),
            NoisilySubvertProcess(),
            ArrangeTitledSurveyor(),
            StakeOwnPosition()
        ]
        self.weight = 1.0  # Standard Frequency
    
    # def can_draw(self, state: RailwayState):
    #     return state.items.get(Item.InvolvedInRailwayVenture, 0) >= 70


class AttemptFairCompromise(Action):
    def __init__(self):
        super().__init__("Attempt a fair compromise")
    
    # def can_perform(self, state: RailwayState):
    #     return (state.items.get(Item.TheVeryTeethOfStGeorge, 0) > 0 and 
    #             state.items.get(Item.FavoursChurch, 0) >= 7)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavChurch: 1  # Gain 1 Favor with the Church
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2  # Gain 2 CP Scandal on failure
        }
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)


class SideWithBishopSouthwark(Action):
    def __init__(self):
        super().__init__("Side with the Bishop of Southwark")
    
    # def can_perform(self, state: RailwayState):
    #     return (state.items.get(Item.BoardMemberBishopSouthwark, 0) > 0 and 
    #             state.items.get(Item.TheVeryTeethOfStGeorge, 0) > 0 and 
    #             state.items.get(Item.FavoursChurch, 0) >= 7)
    
    def pass_items(self, state: RailwayState):
        return {
            # Item.BoardMembersFavourSouthwark: 1,  # Gain 1 Favour with the Bishop of Southwark
            Item.FavChurch: 1  # Gain 1 Favor with the Church
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2  # Gain 2 CP Scandal on failure
        }
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)


class SideWithBishopFiacres(Action):
    def __init__(self):
        super().__init__("Side with the Bishop of St Fiacre's")
    
    # def can_perform(self, state: RailwayState):
    #     return (state.items.get(Item.BoardMemberBishopFiacres, 0) > 0 and 
    #             state.items.get(Item.TheVeryTeethOfStGeorge, 0) > 0 and 
    #             state.items.get(Item.FavoursChurch, 0) >= 7)
    
    def pass_items(self, state: RailwayState):
        return {
            # Item.BoardMembersFavourFiacres: 1,  # Gain 1 Favour with the Bishop of St Fiacre's
            Item.FavChurch: 1  # Gain 1 Favor with the Church
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2  # Gain 2 CP Scandal on failure
        }
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)


class NoisilySubvertProcess(Action):
    def __init__(self):
        super().__init__("Noisily subvert the entire process")
    
    def can_perform(self, state: RailwayState):
        return state.skip_econ_inputs or state.get(Item.VerseOfCounterCreed) > 0
        # state.items.get(Item.ASubmergedRector, 0) > 0)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.VerseOfCounterCreed: -1,  # Lose 1 Verse of Counter-Creed
            Item.HinterlandScrip: 36  # Gain 36 Hinterland Scrip
        }


class ArrangeTitledSurveyor(Action):
    def __init__(self):
        super().__init__("Arrange the services of a Titled Surveyor")
    
    def can_perform(self, state: RailwayState):
        # return (state.items.get(Item.InCorporateDebt, 0) > 0 and 
        return state.skip_favour_inputs or state.get(Item.FavSociety) >= 3

    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavSociety: -3,  # Lose 3 Favours: Society
            Item.InCorporateDebt: -2  # Lose 2 CP Corporate Debt
        }


class StakeOwnPosition(Action):
    def __init__(self):
        super().__init__("Stake your own position")
    
    # def can_perform(self, state: RailwayState):
    #     return (state.items.get(Item.GenesisOfDiocese, 0) >= 400 and 
    #             state.items.get(Item.FavoursChurch, 0) >= 7)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavChurch: 1,  # Gain 1 Favor with the Church
            Item.ProscribedMaterial: 75  # Gain 75 Proscribed Materials
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 1  # Gain 1 CP Scandal on failure
        }
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)


################################################################################
###                          An Unattended Mirror                            ###
################################################################################

# TODO can't really model this properly but w/e
class UnattendedMirror(UpperRiverCard):
    def __init__(self):
        super().__init__("An Unattended Mirror")
        self.actions = [
            UnattendedMirrorDummyCard()
            # VisitParabolanBaseCampNonSilverer(),
            # VisitParabolanBaseCampSilverer(),
            # GoToMoonlitChessboard(),
            # GoToReflectionOfLaboratory(),
            # GoToDomeOfScales(),
            # GoToViricJungle()
        ]
        self.weight = 0.5  # Very Infrequent Frequency

    # def can_draw(self, state: RailwayState):
    #     return state.items.get(Item.AccessParabolanBaseCamp, 0) > 0

class UnattendedMirrorDummyCard(Action):
    def __init__(self):
        super().__init__("(Placeholder card)")
    
    def pass_items(self, state: RailwayState):
        return {
            Item.DropOfPrisonersHoney: -100
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2
        }

# class VisitParabolanBaseCampNonSilverer(Action):
#     def __init__(self):
#         super().__init__("Visit your Parabolan Base-Camp (non-Silverer)")
    
#     def can_perform(self, state: RailwayState):
#         return state.items.get(Item.DropOfPrisonersHoney, 0) >= 100 and \
#                state.items.get(Item.SetOfCosmogoneSpectacles, 0) == 0

#     def pass_items(self, state: RailwayState):
#         return {
#             Item.DropOfPrisonersHoney: -100  # Lose 100 x Drop of Prisoner's Honey
#         }
    
#     def fail_items(self, state: RailwayState):
#         return {
#             Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
#         }

#     def pass_rate(self, state: RailwayState):
#         return self.narrow_pass_rate(2, state.outfit.glasswork)

#     def on_success(self, state: RailwayState):
#         state.move_to_location(Location.ParabolanBaseCamp)


# class VisitParabolanBaseCampSilverer(Action):
#     def __init__(self):
#         super().__init__("Visit your Parabolan Base-Camp (Silverer)")

#     def can_perform(self, state: RailwayState):
#         return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
#                state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0

#     def pass_items(self, state: RailwayState):
#         return {
#             Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
#         }
    
#     def fail_items(self, state: RailwayState):
#         return {
#             Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
#         }

#     def pass_rate(self, state: RailwayState):
#         return self.narrow_pass_rate(2, state.outfit.glasswork)

#     def on_success(self, state: RailwayState):
#         state.move_to_location(Location.ParabolanBaseCamp)


# class GoToMoonlitChessboard(Action):
#     def __init__(self):
#         super().__init__("Go straight to the Moonlit Chessboard")

#     def can_perform(self, state: RailwayState):
#         return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
#                state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0 and \
#                state.items.get(Item.RouteChessboard, 0) > 0

#     def pass_items(self, state: RailwayState):
#         return {
#             Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
#         }
    
#     def fail_items(self, state: RailwayState):
#         return {
#             Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
#         }

#     def pass_rate(self, state: RailwayState):
#         return self.narrow_pass_rate(2, state.outfit.glasswork)

#     def on_success(self, state: RailwayState):
#         state.move_to_location(Location.MoonlitChessboard)


# class GoToReflectionOfLaboratory(Action):
#     def __init__(self):
#         super().__init__("Go straight to the Reflection of Your Laboratory")

#     def can_perform(self, state: RailwayState):
#         return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
#                state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0 and \
#                state.items.get(Item.RouteReflectionLaboratory, 0) > 0

#     def pass_items(self, state: RailwayState):
#         return {
#             Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
#         }
    
#     def fail_items(self, state: RailwayState):
#         return {
#             Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
#         }

#     def pass_rate(self, state: RailwayState):
#         return self.narrow_pass_rate(2, state.outfit.glasswork)

#     def on_success(self, state: RailwayState):
#         state.move_to_location(Location.ReflectionLaboratory)


# class GoToDomeOfScales(Action):
#     def __init__(self):
#         super().__init__("Go straight to the Dome of Scales")

#     def can_perform(self, state: RailwayState):
#         return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
#                state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0 and \
#                state.items.get(Item.RouteDomeOfScales, 0) > 0

#     def pass_items(self, state: RailwayState):
#         return {
#             Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
#         }
    
#     def fail_items(self, state: RailwayState):
#         return {
#             Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
#         }

#     def pass_rate(self, state: RailwayState):
#         return self.narrow_pass_rate(2, state.outfit.glasswork)

#     def on_success(self, state: RailwayState):
#         state.move_to_location(Location.DomeOfScales)


# class GoToViricJungle(Action):
#     def __init__(self):
#         super().__init__("Go straight to the Viric Jungle")

#     def can_perform(self, state: RailwayState):
#         return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
#                state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0 and \
#                state.items.get(Item.RouteViricJungle, 0) > 0

#     def pass_items(self, state: RailwayState):
#         return {
#             Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
#         }
    
#     def fail_items(self, state: RailwayState):
#         return {
#             Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
#         }

#     def pass_rate(self, state: RailwayState):
#         return self.narrow_pass_rate(2, state.outfit.glasswork)

#     def on_success(self, state: RailwayState):
#         state.move_to_location(Location.ViricJungle)

################################################################################
###                            EngageInSomeMinorSmuggling                    ###
################################################################################

class EngageInSomeMinorSmuggling(UpperRiverCard):
    def __init__(self):
        super().__init__("Engage in Some Minor Smuggling")
        self.actions = [
            SmuggleUnlicensedSouls(),
            SmuggleUnlicensedBrilliantSouls(),
            OfferScintillackSnuff(),
            OfferJasmineLeaves(),
            StudySmugglingRings(),
            SellJasmineLeavesWidow(),
            SmuggleIndustrialMaterials()
        ]
        self.weight = 1.0  # Standard Frequency

class SmuggleUnlicensedSouls(Action):
    def __init__(self):
        super().__init__("Smuggle unlicensed souls up the river")
    
    def pass_items(self, state: GameState):
        return {
            Item.Soul: -50,
            Item.PreservedSurfaceBlooms: 2,
            Item.SeeingBanditryInTheUpperRiver: 1
        }

    def fail_items(self, state: GameState):
        return {
            Item.Suspicion: 2
        }

    def pass_rate(self, state: GameState):
        base = 400
        seeing_banditry = state.banditry_level()
        return self.broad_pass_rate(base - seeing_banditry * 50, state.outfit.shadowy)

class SmuggleUnlicensedBrilliantSouls(Action):
    def __init__(self):
        super().__init__("Smuggle unlicensed Brilliant Souls up the river")

    def pass_items(self, state: GameState):
        return {
            Item.BrilliantSoul: -10,
            Item.PreservedSurfaceBlooms: 3,
            Item.SeeingBanditryInTheUpperRiver: 1,
            Item.NevercoldBrassSliver: 70
            # Item.NevercoldBrassSliver: random.randint(60, 80)
        }

    def fail_items(self, state: GameState):
        return {
            Item.Suspicion: 2
        }

    def pass_rate(self, state: GameState):
        base = 480
        seeing_banditry = state.banditry_level()
        return self.broad_pass_rate(base - seeing_banditry * 60, state.outfit.shadowy)

class OfferScintillackSnuff(Action):
    def __init__(self):
        super().__init__("Offer a well-packed keg of scintillack snuff")

    # TODO: minor unlock conditions
    
    def pass_items(self, state: GameState):
        return {
            Item.ConsignmentOfScintillackSnuff: -1,
            Item.PreservedSurfaceBlooms: 7,
            Item.SeeingBanditryInTheUpperRiver: 1
        }

    def fail_items(self, state: GameState):
        return {
            Item.Suspicion: 2
        }

    def pass_rate(self, state: GameState):
        base = 400
        seeing_banditry = state.banditry_level()
        return self.broad_pass_rate(base - seeing_banditry * 50, state.outfit.shadowy)

class OfferJasmineLeaves(Action):
    def __init__(self):
        super().__init__("Offer a supply of Jasmine Leaves")
    
    def pass_items(self, state: GameState):
        return {
            Item.JasmineLeaves: -40,
            Item.PreservedSurfaceBlooms: 3,
            Item.SeeingBanditryInTheUpperRiver: 1
        }

    def fail_items(self, state: GameState):
        return {
            Item.Suspicion: 2
        }

    def pass_rate(self, state: GameState):
        base = 400
        seeing_banditry = state.banditry_level()
        return self.broad_pass_rate(base - seeing_banditry * 50, state.outfit.shadowy)

class StudySmugglingRings(Action):
    def __init__(self):
        super().__init__("Make a study of the local smuggling rings")
    
    def pass_items(self, state: GameState):
        return {
            Item.RumourOfTheUpperRiver: 1
        }

    def fail_items(self, state: GameState):
        return {
            Item.Nightmares: 2
        }

    def pass_rate(self, state: GameState):
        base = 400
        seeing_banditry = state.banditry_level()
        return self.broad_pass_rate(base - seeing_banditry * 50, state.outfit.watchful)

class SellJasmineLeavesWidow(Action):
    def __init__(self):
        super().__init__("Sell all your Jasmine Leaves via the contacts of the Gracious Widow")

    def pass_items(self, state: GameState):
        return {
            Item.JasmineLeaves: -state.items.get(Item.JasmineLeaves, 0),  # All leaves
            Item.JadeFragment: state.items.get(Item.JasmineLeaves, 0) * 13
        }

    def fail_items(self, state: GameState):
        return {
            Item.Suspicion: 2
        }

    def pass_rate(self, state: GameState):
        base = 400
        seeing_banditry = state.banditry_level()
        return self.broad_pass_rate(base - seeing_banditry * 50, state.outfit.shadowy)

class SmuggleIndustrialMaterials(Action):
    def __init__(self):
        super().__init__("Smuggle in industrial materials")

    def pass_items(self, state: GameState):
        return {
            Item.PreservedSurfaceBlooms: -24,
            Item.BessemerSteelIngot: 130
        }

    def fail_items(self, state: GameState):
        return {
            Item.Suspicion: 4
        }

    def pass_rate(self, state: GameState):
        base = 420
        seeing_banditry = state.banditry_level()
        return self.broad_pass_rate(base - seeing_banditry * 50, state.outfit.shadowy)

################################################################################
###                               HalfwayToHell                              ###
################################################################################

class HalfwayToHell(UpperRiverCard):
    def __init__(self):
        super().__init__("Halfway to Hell")
        self.actions = [
            KeepAnEyeOnDevilishActivities(),
            AskAboutFurnaceAndDevils(),
            SellInfernalMachine(),
            ExchangeEversmoulderKnowledge(),
            # SellPlausibleCoverIdentity(),
            # SellAdvancedIdentity()
        ]
        self.weight = 1.0  # Standard Frequency

class KeepAnEyeOnDevilishActivities(Action):
    def __init__(self):
        super().__init__("Keep an eye on the Devilish activities")

    def pass_items(self, state: GameState):
        return {
            Item.RumourOfTheUpperRiver: 1,
            Item.Investigating: 2  # +2 CP
        }

    def fail_items(self, state: GameState):
        return {
            Item.Nightmares: 2  # +2 CP
        }

    def pass_rate(self, state: GameState):
        return self.broad_pass_rate(200, state.outfit.watchful)

class AskAboutFurnaceAndDevils(Action):
    def __init__(self):
        super().__init__("Ask questions about the history between Furnace and the Devils")

    def pass_items(self, state: GameState):
        return {
            Item.AnIdentityUncovered: 1
        }

    def fail_items(self, state: GameState):
        return {
            Item.Scandal: 3  # +3 CP
        }

    def pass_rate(self, state: GameState):
        return self.broad_pass_rate(200, state.outfit.persuasive)

class SellInfernalMachine(Action):
    def __init__(self):
        super().__init__("Sell an Infernal Machine to devils")

    def pass_items(self, state: GameState):
        return {
            Item.InfernalMachine: -1,
            Item.NevercoldBrassSliver: 6600
        }

    def fail_items(self, state: GameState):
        return {}  # No failure state specified

    def pass_rate(self, state: GameState):
        return 1.0  # Guaranteed success

# huh this one isn't that bad. 10 scrip for 1 action
class ExchangeEversmoulderKnowledge(Action):
    def __init__(self):
        super().__init__("Exchange some knowledge of the Eversmoulder")

    def pass_items(self, state: GameState):
        return {
            Item.MovesInTheGreatGame: 10
        }

    def fail_items(self, state: GameState):
        return {
            Item.Nightmares: 3  # +3 CP
        }

    def pass_rate(self, state: GameState):
        return self.broad_pass_rate(210, state.outfit.watchful)

# class SellPlausibleCoverIdentity(Action):
#     def __init__(self):
#         super().__init__("Sell a socially plausible cover identity to a Devil")

#     def pass_items(self, state: GameState):
#         return {
#             Item.FavoursHell: 2,  # Up to 7
#             Item.CoverIdentityTies: 0,  # Remove Cover Identity: Ties
#             Item.FabricatorOfPastLives: 1
#         }

#     def fail_items(self, state: GameState):
#         return {}  # No failure state specified

#     def pass_rate(self, state: GameState):
#         return 1.0  # Guaranteed success

# class SellAdvancedIdentity(Action):
#     def __init__(self):
#         super().__init__("Sell a very advanced identity to Devils")

#     def pass_items(self, state: GameState):
#         return {
#             Item.FavoursHell: randint(0, 4),  # Lose 0-4 Favours: Hell
#             Item.InterceptedDocument: 21,  # Set Intercepted Document to 21
#             Item.CoverIdentityTies: 0,  # Remove Cover Identity: Ties
#             Item.FabricatorOfPastLives: 1
#         }

#     def fail_items(self, state: GameState):
#         return {}  # No failure state specified

#     def pass_rate(self, state: GameState):
#         return 100  # Guaranteed success


################################################################################
###                       Intervene in an Attack                             ###
################################################################################

class InterveneInAnAttack(UpperRiverCard):
    def __init__(self):
        super().__init__("Intervene in an Attack")
        self.actions = [
            AssistOldMan(),
            AssistRobber()
        ]
        self.weight = 0.8  # Infrequent Frequency
    
    def can_draw(self, state: RailwayState):
        return True  # This card is available in Upper River


class AssistOldMan(Action):
    def __init__(self):
        super().__init__("Assist the old man")
        self.alt_pass_rate = 0.05 # TODO Wild guess

    def pass_rate(self, state: RailwayState):
        seeing_banditry = state.banditry_level()
        return self.broad_pass_rate(50 * seeing_banditry, state.outfit.dangerous)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.SeeingBanditryInTheUpperRiver: -1 if state.banditry_level() > 0 else 0,
            Item.PieceOfRostygold: 400,
        }
    
    def alt_pass_items(self, state: RailwayState):
        return {
            Item.SeeingBanditryInTheUpperRiver: -1 if state.banditry_level() > 0 else 0,
            Item.PieceOfRostygold: 400,
            Item.InCorporateDebt: -1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2
        }


class AssistRobber(Action):
    def __init__(self):
        super().__init__("Assist the robber")
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(400 - (50 * state.banditry_level()), state.outfit.dangerous)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.SeeingBanditryInTheUpperRiver: 1,
            Item.PieceOfRostygold: 450,
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2,
        }


################################################################################
###                            A Meeting in a Dark Alley                     
################################################################################

class MeetingInADarkAlley(UpperRiverCard):
    def __init__(self):
        super().__init__("Meeting in a Dark Alley")
        self.actions = [
            IdentifyYourself(),
            DefendYourself(),
            PayTheMan()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.banditry_level() >= 6


class IdentifyYourself(Action):
    def __init__(self):
        super().__init__("Identify yourself")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.OneWhoPullsTheStrings, 0) > 0 
        
    def pass_items(self, state: RailwayState):
        return {
            Item.FlawedDiamond: 10,
            Item.HinterlandScrip: 6.5,
            Item.SeeingBanditryInTheUpperRiver: 1 if state.banditry_level() < 36 else 0,
        }


class DefendYourself(Action):
    def __init__(self):
        super().__init__("Defend yourself")
    
    def pass_rate(self, state: RailwayState):
        dc = 100 + (25 * state.banditry_level())
        return self.broad_pass_rate(dc, state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.FlawedDiamond: 5,
            Item.HandPickedPeppercaps: 10,
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 3,
            Item.HinterlandScrip: -5,
        }


class PayTheMan(Action):
    def __init__(self):
        super().__init__("Pay the man")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.HinterlandScrip, 0) >= 5
    
    def pass_items(self, state: RailwayState):
        return {
            Item.HinterlandScrip: -5,
            Item.SeeingBanditryInTheUpperRiver: 1 if state.banditry_level() < 36 else 0,
        }
    
################################################################################
###                            Respectable Passengers                    
################################################################################
   

class RespectablePassengers(UpperRiverCard):
    def __init__(self):
        super().__init__("Respectable Passengers")
        self.actions = [
            # ContributeEvidenceWithJudge(),
            # ContributeEvidenceWithoutJudge(),
            DiscussOngoingCasesWithAssumingJudge(),
            DiscussOngoingCasesWithLenientJudge(),
            SnoopOnLegalArgument(),
            # ProvideCoverToScholar(),
            # RestoreHopeToProfessor(),
            MakeNoteOfComingsAndGoings()
        ]
        self.weight = 1.0  # Standard Frequency
    
    # def can_draw(self, state: RailwayState):
    #     return state.items.get(Item.InvolvedInRailwayVenture, 0) >= 70


class ContributeEvidenceWithJudge(Action):
    def __init__(self):
        super().__init__("Contribute evidence to a case (with an Unassuming Judge)")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.UnassumingJudge, 0) > 0
    
    def pass_items(self, state: RailwayState):
        return {
            Item.SwornStatement: -5,
            Item.FavSociety: 1,
            Item.CompromisingDocument: 25
        }


class ContributeEvidenceWithoutJudge(Action):
    def __init__(self):
        super().__init__("Contribute evidence to a case (without an Unassuming Judge)")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.UnassumingJudge, 0) == 0
    
    def pass_items(self, state: RailwayState):
        return {
            Item.SwornStatement: -5,
            Item.CompromisingDocument: 30
        }


class DiscussOngoingCasesWithAssumingJudge(Action):
    def __init__(self):
        super().__init__("Discuss ongoing cases with an Assuming Judge")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.AssumingJudge, 0) > 0
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RumourOfTheUpperRiver: 1
        }


class DiscussOngoingCasesWithLenientJudge(Action):
    def __init__(self):
        super().__init__("Discuss ongoing cases with a Very Lenient Judge")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.VeryLenientJudge, 0) > 0
    
    def pass_items(self, state: RailwayState):
        return {
            Item.AnIdentityUncovered: 1
        }


class SnoopOnLegalArgument(Action):
    def __init__(self):
        super().__init__("Snoop on a legal argument")
    
    # def can_perform(self, state: RailwayState):
    #     requires all 3 judges
        
    def pass_items(self, state: RailwayState):
        return {
            Item.DubiousTestimony: 5
        }

class MakeNoteOfComingsAndGoings(Action):
    def __init__(self):
        super().__init__("Make note of their comings and goings")
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavCriminals: 1,
            Item.SeeingBanditryInTheUpperRiver: 1
        }
    
################################################################################
###                          Rising Reports of Banditry                   
################################################################################


class RisingReportsOfBanditry(UpperRiverCard):
    def __init__(self):
        super().__init__("Rising Reports of Banditry")
        self.actions = [
            TicketSalesAreGoingDown(),
            YourReputationIsTarnished(),
            GHRWarehousesAreBeingTargeted()
        ]
        self.weight = 0.8  # Infrequent Frequency
        self.autofire = True
    
    def can_draw(self, state: RailwayState):
        return state.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver) >= 8


class TicketSalesAreGoingDown(Action):
    def __init__(self):
        super().__init__("Ticket sales are going down")
    
    def pass_items(self, state: RailwayState):
        return {
            Item.InCorporateDebt: 4,  # Increases Corporate Debt by 4 CP
            Item.SeeingBanditryInTheUpperRiver: 6 - state.items.get(Item.SeeingBanditryInTheUpperRiver, 0)
        }


class YourReputationIsTarnished(Action):
    def __init__(self):
        super().__init__("Your reputation is tarnished")
    
    def pass_items(self, state: RailwayState):
        return {
            Item.Scandal: 12,  # Increases Scandal by 12 CP
            Item.SeeingBanditryInTheUpperRiver: 6 - state.items.get(Item.SeeingBanditryInTheUpperRiver, 0)
        }


class GHRWarehousesAreBeingTargeted(Action):
    def __init__(self):
        super().__init__("GHR warehouses are being targeted")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.RailwaySteel, 0) >= 4 
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RailwaySteel: -4,  # Removes 4 Railway Steel
            Item.SeeingBanditryInTheUpperRiver: 6 - state.items.get(Item.SeeingBanditryInTheUpperRiver, 0)
        }
    
################################################################################
###                     The Railway and the Great Game                   
################################################################################


class RailwayAndTheGreatGame(UpperRiverCard):
    def __init__(self):
        super().__init__("The Railway and the Great Game")
        self.actions = [
            WatchComingsAndGoingsBeforeManufacture(),
            WatchComingsAndGoingsAfterManufacture()
            # Skipping the various lengthy item conversions
        ]
        self.weight = 1.0  # Standard Frequency
    
    # def can_draw(self, state: RailwayState):
    #     return state.items.get(Item.InvolvedInRailwayVenture, 0) >= 90  # Unlocked with Railway Venture 90


class WatchComingsAndGoingsBeforeManufacture(Action):
    def __init__(self):
        super().__init__("Watch the comings and goings on the Upper River 1")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.BusinessOfManufacture, 0) < 6  # Locked with Business of Manufacture 6
    
    def pass_rate(self, state: RailwayState):
        dc = 210 - state.outfit.player_of_chess
        return self.broad_pass_rate(dc, state.outfit.watchful)
        
    def pass_items(self, state: RailwayState):
        return {
            Item.IntriguingSnippet: 10,  # Gains Intriguing Snippet x10
            Item.Casing: 1  # Casing increases by 1 CP
        }

class WatchComingsAndGoingsAfterManufacture(Action):
    def __init__(self):
        super().__init__("Watch the comings and goings on the Upper River 2")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.BusinessOfManufacture, 0) >= 6  # Requires Business of Manufacture 6 or higher
    
    def pass_rate(self, state: RailwayState):
        dc = 210 - state.outfit.player_of_chess
        return self.broad_pass_rate(dc, state.outfit.watchful)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.IntriguingSnippet: 11,  # Gains Intriguing Snippet x11
            Item.Casing: 1  # Casing increases by 1 CP
        }

################################################################################
###                         Urchins Games                   
################################################################################

class UrchinsGames(UpperRiverCard):
    def __init__(self):
        super().__init__("The Urchins' Games")
        self.actions = [
            WagerOnSpiteDrBlemmigan(),
            WagerWithConstantCufflinks(),
            WagerWithMrCards(),
            WagerWithTheMarvellous()
        ]
        self.weight = 1.0  # Standard Frequency
    
    # def can_draw(self, state: RailwayState):
    #     return state.items.get(Item.InvolvedInRailwayVenture, 0) >= 70  # Unlocked with Railway Venture 70


class WagerOnSpiteDrBlemmigan(Action):
    def __init__(self):
        super().__init__("Wager a penny on a hand of Spite Dr. Blemmigan")

    # def can_perform(self, state: RailwayState):
    #     return not state.items.get(Item.ConstantCufflinks, 0)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.CrypticClue: 120,
            Item.Echo: -0.01
        }


class WagerWithConstantCufflinks(Action):
    def __init__(self):
        super().__init__("Wager a penny on a hand of Spite Dr. Blemmigan (with Constant Cufflinks)")

    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.ConstantCufflinks, 0)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.IntriguingSnippet: 1,
            Item.Echo: 0.01,
            Item.AnIdentityUncovered: 2
        }


class WagerWithMrCards(Action):
    def __init__(self):
        super().__init__("Wager a penny on a hand of Spite Dr. Blemmigan (with The Robe of Mr Cards)")

    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.TheRobeOfMrCards, 0) > 0
    
    def pass_items(self, state: RailwayState):
        return {
            Item.IntriguingSnippet: 2,
            Item.Echo: 0.01,
            Item.AnIdentityUncovered: 2
        }


class WagerWithTheMarvellous(Action):
    def __init__(self):
        super().__init__("Wager a penny on a hand of Spite Dr. Blemmigan (with The Marvellous)")

    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.TheMarvellous, 0) > 0
    
    def pass_items(self, state: RailwayState):
        return {
            Item.IntriguingSnippet: 2,
            Item.Echo: 0.01,
            Item.AnIdentityUncovered: 2
        }

################################################################################
###                          Which Meeting?                 
################################################################################


class WhichMeeting(UpperRiverCard):
    def __init__(self):
        super().__init__("Which Meeting?")
        self.actions = [
            SellPerfumedGunpowder(),
            DonateHillmover(),
            SellPropaganda(),
            # DonateSpecialDispensation()
        ]
        self.weight = 1.0  # Standard Frequency
    
    # def can_draw(self, state: RailwayState):
    #     return state.items.get(Item.LanguageOfLaces, 0) > 0  # Requires Language of Laces


class SellPerfumedGunpowder(Action):
    def __init__(self):
        super().__init__("Sell Perfumed Gunpowder to Liberationist Revolutionaries")

    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.PerfumedGunpowder, 0) >= 4
    
    def pass_rate(self, state: RailwayState):
        support = state.items.get(Item.SupportingTheLiberationistTracklayers, 0)
        return self.broad_pass_rate(300 - support * 20, state.outfit.shadowy)

    def pass_items(self, state: RailwayState):
        return {
            Item.VitalIntelligence: 1,
            Item.WellPlacedPawn: 2, # random.randint(1, 3),
            Item.PerfumedGunpowder: -4,  # Lose 4 Perfumed Gunpowder
            Item.AdvancingTheLiberationOfNight: 1  # Increase Liberation of Night by 1 CP
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2  # Increase Suspicion by 2 CP
        }


class DonateHillmover(Action):
    def __init__(self):
        super().__init__("Donate a Hillmover to Liberationist Revolutionaries")

    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.FavoursRevolutionaries, 0) < 7
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavRevolutionaries: 1,  # Gain 1 Favour: Revolutionaries
            Item.Hillmover: -1,  # Lose 1 Hillmover
            Item.AdvancingTheLiberationOfNight: 3  # Increase Liberation of Night by 3 CP
        }


class SellPropaganda(Action):
    def __init__(self):
        super().__init__("Sell valuable propaganda to the Veteran Revolutionary, an anti-Liberationist")

    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.CorrectiveHistoricalNarrative, 0) > 0
    
    def pass_rate(self, state: RailwayState):
        support = state.items.get(Item.SupportingTheEmancipationistTracklayers, 0)
        return self.broad_pass_rate(300 - support * 20, state.outfit.shadowy)

    def pass_items(self, state: RailwayState):
        return {
            Item.ForgedJustificandeCoin: 2, #(1, 3),  # Gain 1 to 3 Forged Justificande Coins
            Item.JustificandeCoin: 2, # (1, 3),  # Gain 1 to 3 Justificande Coins
            Item.CorrectiveHistoricalNarrative: -1,  # Lose 1 Corrective Historical Narrative
            Item.AdvancingTheLiberationOfNight: -2  # Decrease Liberation of Night by 2 CP
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2  # Increase Suspicion by 2 CP
        }

# class DonateSpecialDispensation(Action):
#     def __init__(self):
#         super().__init__("Donate a Special Dispensation to the Veteran Revolutionary")

#     # def can_perform(self, state: RailwayState):
#     #     return state.items.get(Item.SpecialDispensation, 0) > 0 and state.items.get(Item.FavoursRevolutionaries, 0) <= 6
    
#     def pass_items(self, state: RailwayState):
#         return {
#             Item.FavoursRevolutionaries: 2,  # Gain 2 Favours: Revolutionaries
#             Item.SpecialDispensation: -1,  # Lose 1 Special Dispensation
#             Item.ForgedJustificandeCoin: (1, 3),  # Gain 1 to 3 Forged Justificande Coins
#             Item.JustificandeCoin: (1, 5)  # Gain 1 to 5 Justificande Coins
#         }

# ==============================================================
#                   Your Very Own Hellworm
# ==============================================================

class YourVeryOwnHellworm(UpperRiverCard):
    def __init__(self):
        super().__init__("Your Very Own Hellworm")
        self.actions = [
            PlayWithYourHellworm(),
            RideYourHellworm(),
            MilkYourHellworm()
        ]
        self.weight = 2.0  # Frequent Frequency
    
    def can_draw(self, state: RailwayState):
        return state.get(Item.InTheCompanyOfAHellworm) > 0


class PlayWithYourHellworm(Action):
    def __init__(self):
        super().__init__("Play with your hellworm")

    def pass_items(self, state: RailwayState):
        return {
            Item.Nightmares: -4.5, #-self.random_cp(1, 8),
            Item.DispositionOfYourHellworm: 1
        }

class RideYourHellworm(Action):
    def __init__(self):
        super().__init__("Ride your hellworm")

    def can_perform(self, state: RailwayState):
        return state.get(Item.HellwormSaddle) > 0

    def pass_items(self, state: RailwayState):
        return {
            Item.Scandal: 1,
            # Item.NotToBeTrifledWith: 1,
            Item.AeolianScream: 2,
            Item.DispositionOfYourHellworm: 1.5 #self.random_cp(1, 2)
        }

class MilkYourHellworm(Action):
    def __init__(self):
        super().__init__("Milk your hellworm")

    def can_perform(self, state: RailwayState):
        return state.get(Item.DispositionOfYourHellworm) >= 7

    def pass_items(self, state: RailwayState):
        # avg per wiki
        return {
            Item.Echo: 73, #self.random_cp(1, 33),
            Item.DispositionOfYourHellworm: -7
        }


################################################################################
###                   Adjust the Lighting in Ealing Gardens      
################################################################################

class AdjustLightingInEalingGardens(UpperRiverCard):
    def __init__(self):
        super().__init__("Adjust the Lighting in Ealing Gardens")
        self.actions = [
            RefreshWatchtowerEaling(),
            BreakLampEaling(),
            ImpassionedSpeechForLightAndBeautyEaling(),
            ImpassionedSpeechOnFreedomAndDarknessEaling(),
            CalculatedSpeechOnFreedomAndDarknessEaling(),
            LeaveLightAsIsEaling()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        # Check specific conditions for drawing this card
        return state.location == Location.EalingGardens and \
            state.get(Item.EalingGardensDarkness) < utils.pyramid(7) and \
            state.get(Item.ColourAtTheChessboard) < 3


class RefreshWatchtowerEaling(Action):
    def __init__(self):
        super().__init__("Refresh the Watchtower")
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(100, state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.EalingGardensDarkness: -1,  # CP drop
            Item.AdvancingTheLiberationOfNight: -1,  # CP drop
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2  # Wounds increase on failure
        }


class BreakLampEaling(Action):
    def __init__(self):
        super().__init__("Break a lamp")
    
    def pass_rate(self, state: RailwayState):
        banditry_level = state.banditry_level()
        return self.broad_pass_rate(400 - (50 * banditry_level), state.outfit.shadowy)

    def pass_items(self, state: RailwayState):
        return {
            Item.EalingGardensDarkness: 2,  # CP increase
            Item.AdvancingTheLiberationOfNight: 2  # CP increase
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2  # Suspicion increase on failure
        }

class ImpassionedSpeechForLightAndBeautyEaling(Action):
    def __init__(self):
        super().__init__("Make an impassioned speech for Light and Beauty")
        self.alt_pass_rate = 0.05 # TODO

    def can_perform(self, state: GameState):
        return state.get(Item.ColourAtTheChessboard) != 2

    def pass_rate(self, state: RailwayState):
        dc = 150 + state.get(Item.SupportingTheLiberationistTracklayers) * 25
        return self.broad_pass_rate(dc, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.AdvancingTheLiberationOfNight: -3,
            Item.WhisperedHint: 200
        }

    def alt_pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.AdvancingTheLiberationOfNight: -3,
            Item.WhisperedHint: 200,
            Item.MirrorcatchBox: 1  # Rare success
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2  # Scandal increase on failure
        }

class ImpassionedSpeechOnFreedomAndDarknessEaling(Action):
    def __init__(self):
        super().__init__("Give an impassioned speech on Freedom and Darkness")

    def pass_rate(self, state: RailwayState):
        dc = 400 - 50 * state.get(Item.SupportingTheLiberationistTracklayers)
        return self.broad_pass_rate(dc, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.AdvancingTheLiberationOfNight: 3,
            Item.WhisperedHint: 200
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2  # Scandal increase on failure
        }


class CalculatedSpeechOnFreedomAndDarknessEaling(Action):
    def __init__(self):
        super().__init__("Give a calculated speech on Freedom and Darkness")

    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(5, state.outfit.mithridacy)

    def pass_items(self, state: RailwayState):
        return {
            Item.AdvancingTheLiberationOfNight: 2
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2,
            Item.Wounds: 1
        }

class LeaveLightAsIsEaling(Action):
    def __init__(self):
        super().__init__("Leave the light as it is")

    def pass_items(self, state: RailwayState):
        return {
            Item.RumourOfTheUpperRiver: 1
        }
    
################################################################################
###                        Under the Statue (Ealing)                
################################################################################

class UnderTheStatueEaling(UpperRiverCard):
    def __init__(self):
        super().__init__("Under the Statue")
        self.actions = [
            PracticeSketchingTheStatueEaling(),
            CallInFavoursFromUrchinsEaling(),
            CallInFavoursFromTombColonistsEaling(),
            CallInFavoursFromRevolutionariesEaling(),
            CallInFavoursFromHellEaling(),
            CallInFavoursFromRubberyMenEaling(),
            CallInFavoursFromBohemiansEaling()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.EalingGardens and \
            state.items.get(Item.EalingGardensCommemorativeDevelopment, 0) > 0


class PracticeSketchingTheStatueEaling(Action):
    def __init__(self):
        super().__init__("Practice sketching the Statue")
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.DropOfPrisonersHoney: 100
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }


class CallInFavoursFromUrchinsEaling(Action):
    def __init__(self):
        super().__init__("Call in favours from Urchins")
    
    # def can_perform(self, state: RailwayState):
    #     return state.get(Item.EalingGardensCommemorativeDevelopment) == 1
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavUrchins) >= 4


    def pass_items(self, state: RailwayState):
        return {
            Item.FavUrchins: -4,
            Item.PuzzleDamaskScrap: 1,
            Item.ThirstyBombazineScrap: 5,
            # Item.BundleOfOddities: 1  # This can contain various rewards
            Item.Echo: 3.5 # estimated
        }


class CallInFavoursFromTombColonistsEaling(Action):
    def __init__(self):
        super().__init__("Call in favours from Tomb Colonists")

    # def can_perform(self, state: RailwayState):
    #     return state.get(Item.EalingGardensCommemorativeDevelopment) == 2
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavTombColonies) >= 2


    def pass_items(self, state: RailwayState):
        return {
            Item.FavTombColonies: -2,
            Item.Sapphire: 5,
            Item.VenomRuby: 49,
            Item.MagnificentDiamond: 1
        }


class CallInFavoursFromRevolutionariesEaling(Action):
    def __init__(self):
        super().__init__("Call in favours from Revolutionaries")

    # def can_perform(self, state: RailwayState):
    #     return state.get(Item.EalingGardensCommemorativeDevelopment) == 3
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavRevolutionaries) >= 4


    def pass_items(self, state: RailwayState):
        return {
            Item.FavRevolutionaries: -4,
            Item.ProscribedMaterial: 750
        }


class CallInFavoursFromHellEaling(Action):
    def __init__(self):
        super().__init__("Call in favours from Hell")
        self.alt_pass_rate = 0.05

    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavHell) >= 2

    # def can_perform(self, state: RailwayState):
    #     return state.get(Item.EalingGardensCommemorativeDevelopment) == 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavHell: -2,
            Item.MuscariaBrandy: 8
        }

    # This is worse than normal success?
    def alt_pass_items(self, state: RailwayState):
        return {
            Item.FavHell: -2,
            Item.BrassRing: 1
        }

class CallInFavoursFromRubberyMenEaling(Action):
    def __init__(self):
        super().__init__("Call in favours from Rubbery Men")

    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.EalingGardensCommemorativeDevelopment, 0) == 10
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavRubberyMen) >= 2

    def pass_items(self, state: RailwayState):
        return {
            Item.FavRubberyMen: -2,
            Item.NoduleOfTremblingAmber: 1,
            Item.NoduleOfWarmAmber: 55
        }


class CallInFavoursFromBohemiansEaling(Action):
    def __init__(self):
        super().__init__("Call in favours from Bohemians")

    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.EalingGardensCommemorativeDevelopment, 0) == 20

    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavBohemians) >= 4


    def pass_items(self, state: RailwayState):
        return {
            Item.FavBohemians: -4,
            Item.IvoryHumerus: 2,
            Item.RomanticNotion: 50
        }

# ==============================================================
#                           Constellations
# ==============================================================

class Constellations(UpperRiverCard):
    def __init__(self):
        super().__init__("Constellations")
        self.actions = [
            TimeAppearancesOfHillchangerTower(),
            MapTheConstellations()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.EalingGardens and \
            state.get(Item.EalingGardensDarkness) >= utils.pyramid(6)


class TimeAppearancesOfHillchangerTower(Action):
    def __init__(self):
        super().__init__("Time the appearances of Hillchanger Tower")
    
    # def can_perform(self, state: RailwayState):
    #     return state.get(Item.NuncianPocketWatch) > 0

    def pass_items(self, state: RailwayState):
        return {
            Item.ExtraordinaryImplication: 2,
            Item.WhisperedHint: 8.5  # random.randint(2, 15)
        }

class MapTheConstellations(Action):
    def __init__(self):
        super().__init__("Map the constellations")
    
    def pass_items(self, state: RailwayState):
        darkness_level = utils.cp_to_level(state.get(Item.EalingGardensDarkness))
        return {
            Item.MapScrap: 5,
            Item.WhisperedHint: 30 * darkness_level,
            # Item.AirsOfEalingGardens: 1  # Simulate air change in Ealing Gardens
        }

# ==============================================================
#                       Engage in Excavation
# ==============================================================

class EngageInExcavation(UpperRiverCard):
    def __init__(self):
        super().__init__("Engage in Excavation")
        self.actions = [
            ExploreRiverbankLowTide(),
            SiftRiverbankMud(),
            SearchRiversEdgeFallingTide(),
            ExploreRiversEdgeHighTide(),
            DigAwayFromRiver()
        ]
        self.weight = 2.0  # Frequent Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.EalingGardens

class ExploreRiverbankLowTide(Action):
    def __init__(self):
        super().__init__("Explore the riverbank in low tide")
        self.alt_pass_rate = default_alt_pass_rate 
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.AirsOfEalingGardens, 0) <= 25

    def pass_rate(self, state: RailwayState):
        darkness_level = utils.cp_to_level(state.get(Item.EalingGardensDarkness))
        return self.broad_pass_rate(50 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.UnidentifiedThighBone: 1,
            # Item.AirsOfEalingGardens: 1  # Simulate air change in Ealing Gardens
        }
    
    def alt_pass_items(self, state: RailwayState):
        return {
            Item.UnidentifiedThighBone: 1,
            Item.HeadlessSkeleton: 1,
            # Item.AirsOfEalingGardens: 1  # Simulate air change in Ealing Gardens
        }    

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2  # Nightmares increase on failure
        }

class SiftRiverbankMud(Action):
    def __init__(self):
        super().__init__("Sift the riverbank mud in the rising tide")
        self.alt_pass_rate = default_alt_pass_rate

    # def can_perform(self, state: RailwayState):
    #     return 26 <= state.items.get(Item.AirsOfEalingGardens, 0) <= 50

    def pass_rate(self, state: RailwayState):
        darkness_level = utils.cp_to_level(state.get(Item.EalingGardensDarkness))
        return self.broad_pass_rate(50 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.HelicalThighbone: 1,
            # Item.AirsOfEalingGardens: 1  # Simulate air change in Ealing Gardens
        }

    def alt_pass_items(self, state: RailwayState):
        return {
            Item.HelicalThighbone: 2,
            # Item.AirsOfEalingGardens: 1  # Simulate air change in Ealing Gardens
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2
        }


class SearchRiversEdgeFallingTide(Action):
    def __init__(self):
        super().__init__("Search the river's edge as the tide falls")
    
    # def can_perform(self, state: RailwayState):
    #     return 51 <= state.items.get(Item.AirsOfEalingGardens, 0) <= 75

    def pass_rate(self, state: RailwayState):
        darkness_level = utils.cp_to_level(state.get(Item.EalingGardensDarkness))
        return self.broad_pass_rate(50 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.KnottedHumerus: 1,
            Item.NoduleOfWarmAmber: 2, #random.randint(1, 3),
            # Item.AirsOfEalingGardens: 1  # Simulate air change in Ealing Gardens
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2
        }


class ExploreRiversEdgeHighTide(Action):
    def __init__(self):
        super().__init__("Explore the river's edge at high tide")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.AirsOfEalingGardens, 0) >= 76

    def pass_rate(self, state: RailwayState):
        darkness_level = utils.cp_to_level(state.get(Item.EalingGardensDarkness))
        return self.broad_pass_rate(50 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.KnobOfScintillack: 1,
            # Item.AirsOfEalingGardens: 1  # Simulate air change in Ealing Gardens
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2
        }


class DigAwayFromRiver(Action):
    def __init__(self):
        super().__init__("Dig a little distance from the river")
        self.alt_pass_rate = default_alt_pass_rate
        self.alt_fail_rate = default_alt_fail_rate
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.SurveyOfTheNeathsBones, 0) >= 15

    def pass_rate(self, state: RailwayState):
        darkness_level = utils.cp_to_level(state.get(Item.EalingGardensDarkness))
        return self.broad_pass_rate(40 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.HumanRibcage: 1,
            Item.SurveyOfTheNeathsBones: -15
        }

    def alt_pass_items(self, state: RailwayState):
        return {
            Item.ThornedRibcage: 1,
            Item.HumanArm: 1,
            Item.SurveyOfTheNeathsBones: -15
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.FemurOfASurfaceDeer: 10,
            Item.HeadlessSkeleton: 1,
            Item.HumanArm: 2,
            Item.Nightmares: 2,
            Item.SurveyOfTheNeathsBones: -15
        }

    def alt_fail_items(self, state: RailwayState):
        return {
            Item.ShrivelledBall: 1,
            Item.HumanArm: 3,
            Item.SurveyOfTheNeathsBones: -15
        }


# ==============================================================
#                           Engage in Unobserved Charity
# ==============================================================

class EngageInUnobservedCharity(UpperRiverCard):
    def __init__(self):
        super().__init__("Engage in Unobserved Charity")
        self.actions = [
            FillAStomachEaling(),
            ComfortASuffererEaling()
        ]
        self.weight = 0.8  # Infrequent Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.EalingGardens

class FillAStomachEaling(Action):
    def __init__(self):
        super().__init__("Fill a stomach")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.CrateOfIncorruptibleBiscuits, 0) >= 1

    def pass_rate(self, state: RailwayState):
        darkness_level = utils.cp_to_level(state.get(Item.EalingGardensDarkness))
        return self.broad_pass_rate(400 - (50 * darkness_level), state.outfit.shadowy)

    def pass_items(self, state: RailwayState):
        return {
            Item.CrateOfIncorruptibleBiscuits: -1,
            Item.FavUrchins: 1,
            # Item.AdriftOnASeaOfMisery: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2
        }


class ComfortASuffererEaling(Action):
    def __init__(self):
        super().__init__("Comfort a sufferer")

    def pass_rate(self, state: RailwayState):
        darkness_level = max(state.items.get(Item.EalingGardensDarkness, 0), 
                             state.items.get(Item.JerichoLocksDarkness, 0))
        return self.broad_pass_rate(400 - (50 * darkness_level), state.outfit.shadowy)

    def pass_items(self, state: RailwayState):
        return {
            Item.WhisperedHint: 250, #random.randint(226, 274),
            # Item.AdriftOnASeaOfMisery: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2
        }


# ==============================================================
#                           Ministry Enforcement
# ==============================================================

class MinistryEnforcement(UpperRiverCard):
    def __init__(self):
        super().__init__("Ministry Enforcement")
        self.actions = [
            SearchAroundBack(),
            OutflankTheMinistrysServant(),
            JoinTheEnforcementTeam()
        ]
        self.weight = 0.8  # Infrequent Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.EalingGardens

class SearchAroundBack(Action):
    def __init__(self):
        super().__init__("Search around back")
    
    def pass_rate(self, state: RailwayState):
        # TODO wiki unclear on whether darkness affects DC
        darkness_level = state.get_pyramidal_level(Item.EalingGardensDarkness)
        return self.broad_pass_rate(115, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.NoduleOfWarmAmber: 15,
            Item.NoduleOfDeepAmber: 100
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.NoduleOfDeepAmber: 100
        }

class OutflankTheMinistrysServant(Action):
    def __init__(self):
        super().__init__("Outflank the Ministry's servant")
    
    # def can_perform(self, state: RailwayState):
    #     return (state.outfit.bizarre and state.items.get(Item.FavoursRubberyMen, 0) >= 7)

    def pass_rate(self, state: RailwayState):
        dc = state.items.get(Item.Suspicion)
        return self.narrow_pass_rate(dc, state.outfit.player_of_chess)

    def pass_items(self, state: RailwayState):
        return {
            Item.FavRubberyMen: 1,
            Item.Suspicion: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2
        }

class JoinTheEnforcementTeam(Action):
    def __init__(self):
        super().__init__("Join the enforcement team")
    
    # def can_perform(self, state: RailwayState):
    #     return (state.items.get(Item.TheChapOnTheCorner, 0) > 0 and 
    #             state.outfit.renown_rubbery_men >= 16)

    def pass_rate(self, state: RailwayState):
        banditry_level = state.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver)
        return self.broad_pass_rate(50 * banditry_level, state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.HinterlandScrip: 5
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 1
        }

# ==============================================================
#                           Rubbery Observances
# ==============================================================

class RubberyObservances(UpperRiverCard):
    def __init__(self):
        super().__init__("Rubbery Observances")
        self.actions = [
            SneakIntoFactories(),
            VisitFactoriesAsGuest(),
            # MeetRubberyStranger(),
            ConstrueSignificantBurble()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        state.location == Location.EalingGardens

class SneakIntoFactories(Action):
    def __init__(self):
        super().__init__("Sneak into the Factories of the Tentacled Entrepreneur")
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.shadowy)

    def pass_items(self, state: RailwayState):
        return {
            Item.WhisperedHint: 250,
            # Item.AirsOfEalingGardens: 1  # Random change in Airs
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2
        }


class VisitFactoriesAsGuest(Action):
    def __init__(self):
        super().__init__("Visit the Factories of the Tentacled Entrepreneur as an invited guest")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.BoardMemberTentacledEntrepreneur, 0) > 0
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.WhisperedHint: 250,
            # Item.AirsOfEalingGardens: 1  # Random change in Airs
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }

# class MeetRubberyStranger(Action):
#     def __init__(self):
#         super().__init__("Meet a Rubbery Stranger")
    
#     def can_perform(self, state: RailwayState):
#         return state.items.get(Item.PeculiarPersonalEnhancement, 0) > 0
    
#     def pass_items(self, state: RailwayState):
#         return {
#             Item.NoduleOfWarmAmber: 30,
#             Item.JasmineLeaves: 1,
#             Item.PeculiarPersonalEnhancement: -1
#         }

class ConstrueSignificantBurble(Action):
    def __init__(self):
        super().__init__("Construe a significant burble")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.RubberyBellringer, 0) > 0

    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(220, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.RumourOfTheUpperRiver: 1,
            # Item.AcquaintanceWithHeliconHouse: 1  # Raise acquaintance with Helicon House
        }


# ==============================================================
#                           Set up your own Bear Show
# ==============================================================

class SetUpYourOwnBearShow(UpperRiverCard):
    def __init__(self):
        super().__init__("Set up your own Bear Show")
        self.actions = [
            TakeCareOfPerformer(),
            DesignBearShowRomanTheme(),
            DesignBearShowNavyTheme()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        state.location == Location.EalingGardens
        # return state.items.get(Item.HoneyMazedBear, 0) > 0 and \
        #     state.items.get(Item.Gazebo, 0) > 0

class TakeCareOfPerformer(Action):
    def __init__(self):
        super().__init__("Take good care of your performer")
    
    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(3, state.outfit.kataleptic_toxicology)

    def pass_items(self, state: RailwayState):
        return {
            Item.MagisterialLager: 5,
            Item.TracklayersDispleasure: -1
        }

    def fail_items(self, state: RailwayState):
        return {
            # No penalties beyond possible failure
        }

class DesignBearShowRomanTheme(Action):
    def __init__(self):
        super().__init__("Design a bear show on the Theme of the Roman Empire")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.FinalBreath, 0) >= 5 and \
    #         state.items.get(Item.HandPickedPeppercaps, 0) >= 5
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.FinalBreath: -5,
            Item.HandPickedPeppercaps: -5,
            Item.RumourOfTheUpperRiver: 1,
            Item.FlawedDiamond: 4,
            Item.HinterlandScrip: 10
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 3
        }

class DesignBearShowNavyTheme(Action):
    def __init__(self):
        super().__init__("Design a bear show on the Theme of the Surface Navy")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.UrsineHoneyConnoisseur, 0) > 0 and \
    #         state.items.get(Item.MoonPearl, 0) >= 500
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.MoonPearl: -500,
            Item.HinterlandScrip: 15
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 3
        }


# ==============================================================
#                           Adjust the Lighting in Jericho Locks
# ==============================================================

class AdjustLightingJerichoLocks(UpperRiverCard):
    def __init__(self):
        super().__init__("Adjust the Lighting in Jericho Locks")
        self.actions = [
            BreakALampJericho(),
            RepairALampJericho(),
            GiveImpassionedSpeechJericho(),
            LeaveLightAsIsJericho()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.JerichoLocks and \
            state.get_pyramidal_level(Item.JerichoLocksDarkness) < 7 and \
            state.get(Item.ColourAtTheChessboard) != 3

class BreakALampJericho(Action):
    def __init__(self):
        super().__init__("Break a lamp")
    
    def pass_rate(self, state: RailwayState):
        banditry_level = state.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver)
        return self.broad_pass_rate(400 - 50 * banditry_level, state.outfit.shadowy)
    
    def pass_items(self, state: RailwayState):
        return {
            # Item.Shadowy: 1,
            Item.AdvancingTheLiberationOfNight: 2,
            Item.JerichoLocksDarkness: 2
        }

    def fail_items(self, state: RailwayState):
        return {
            # Item.Shadowy: 1,
            Item.Suspicion: 2
        }

class RepairALampJericho(Action):
    def __init__(self):
        super().__init__("Repair a lamp")
    
    def can_perform(self, state: RailwayState):
        return state.get(Item.ColourAtTheChessboard) != 2
    
    def pass_rate(self, state: RailwayState):
        banditry_level = state.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver)
        return self.broad_pass_rate(50 * banditry_level, state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.JerichoLocksDarkness: -2
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2
        }

class GiveImpassionedSpeechJericho(Action):
    def __init__(self):
        super().__init__("Give an impassioned speech on Light and Beauty")
        self.alt_pass_rate = default_alt_pass_rate

    def can_perform(self, state: RailwayState):
        return state.get(Item.ColourAtTheChessboard) != 2
    
    def pass_rate(self, state: RailwayState):
        dc = 150 + 25 * state.get(Item.SupportingTheLiberationistTracklayers)
        return self.broad_pass_rate(dc, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.AdvancingTheLiberationOfNight: -3,
            Item.WhisperedHint: 200
        }

    def rare_success_items(self, state: RailwayState):
        return {
            Item.MirrorcatchBox: 1,
            Item.RomanticNotion: 5,
            Item.AdvancingTheLiberationOfNight: -3,
            Item.WhisperedHint: 200
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }

class LeaveLightAsIsJericho(Action):
    def __init__(self):
        super().__init__("Leave the light as it is")
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RumourOfTheUpperRiver: 1
        }

# ==============================================================
#                           Dredge the River
# ==============================================================

class DredgeTheRiverJericho(UpperRiverCard):
    def __init__(self):
        super().__init__("Dredge the river")
        self.actions = [
            DredgeLowTide(),
            NetRiver(),
            DigAwayFromRiver()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.JerichoLocks
    

class DredgeLowTide(Action):
    def __init__(self):
        super().__init__("Dredge the bottom of the river at low tide")
        self.alt_pass_rate = default_alt_pass_rate
    # def can_perform(self, state: RailwayState):
    #     return 0 <= state.items.get(Item.AirsOfJerichoLocks, 0) <= 25
    
    def pass_rate(self, state: RailwayState):
        darkness_level = state.get_pyramidal_level(Item.JerichoLocksDarkness)  # Base difficulty = 50 * Darkness level
        return self.broad_pass_rate(50 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.FemurOfAJurassicBeast: 1,
            Item.UnidentifiedThighBone: 1
        }

    def alt_pass_items(self, state: RailwayState):
        return {
            Item.FemurOfAJurassicBeast: 1,
            Item.HumanArm: 0.5,
            Item.FemurOfASurfaceDeer: 1.5,
            Item.JetBlackStinger: 0.5
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2,
            Item.HeadlessSkeleton: 1
        }


class NetRiver(Action):
    def __init__(self):
        super().__init__("Net whatever is in the river")
        self.alt_pass_rate = default_alt_pass_rate

    # def can_perform(self, state: RailwayState):
    #     return 26 <= state.items.get(Item.AirsOfJerichoLocks, 0) <= 100
    
    def pass_rate(self, state: RailwayState):
        darkness_level = state.get_pyramidal_level(Item.JerichoLocksDarkness)  # Base difficulty = 50 * Darkness level
        return self.broad_pass_rate(50 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.DeepZeeCatch: 1,
            Item.CarvedBallOfStygianIvory: 1
        }

    def alt_pass_items(self, state: RailwayState):
        return {
            Item.WitheredTentacle: 2,
            Item.DeepZeeCatch: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2
        }

class DigAwayFromRiver(Action):
    def __init__(self):
        super().__init__("Dig a little distance from the river")
        self.alt_pass_items = 0.05

    def can_perform(self, state: RailwayState):
        return state.items.get(Item.SurveyOfTheNeathsBones, 0) >= 2
    
    def pass_rate(self, state: RailwayState):
        darkness_level = state.get_pyramidal_level(Item.JerichoLocksDarkness)  # Base difficulty = 50 * Darkness level
        return self.broad_pass_rate(40 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.SurveyOfTheNeathsBones: -2,
            Item.RelicOfTheSecondCity: 10,
            Item.UnprovenancedArtefact: 2
        }

    def alt_pass_items(self, state: RailwayState):
        return {
            Item.SurveyOfTheNeathsBones: -2,
            Item.DoveMaskShard: 1,
            Item.RelicOfTheSecondCity: 10,
            Item.UnprovenancedArtefact: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 1,
            Item.RelicOfTheSecondCity: 6,
            Item.SurveyOfTheNeathsBones: -2
        }

# ==============================================================
#                           Enlighten Jericho Locks
# ==============================================================

class EnlightenJerichoLocks(UpperRiverCard):
    def __init__(self):
        super().__init__("Enlighten Jericho Locks")
        self.actions = [
            RepairLampJericho(),
            SpeechLightAndBeautyJericho(),
            LeaveLightJericho()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.JerichoLocks and \
            state.items.get(Item.ColourAtTheChessboard) >= 3

class RepairLampJericho(Action):
    def __init__(self):
        super().__init__("Repair a Lamp")
    
    def can_perform(self, state: RailwayState):
        return state.get(Item.ColourAtTheChessboard) != 2
    
    def pass_rate(self, state: RailwayState):
        banditry_level = state.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver)
        return self.broad_pass_rate(50 * banditry_level, state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.JerichoLocksDarkness: -2
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2
        }

class SpeechLightAndBeautyJericho(Action):
    def __init__(self):
        super().__init__("Give an impassioned speech on Light and Beauty")
        self.alt_pass_rate = default_alt_pass_rate

    def can_perform(self, state: RailwayState):
        return state.get(Item.ColourAtTheChessboard) != 2
    
    def pass_rate(self, state: RailwayState):
        dc = 150 + 25 * state.get(Item.SupportingTheLiberationistTracklayers)
        return self.broad_pass_rate(dc, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.LiberationOfNight: -3,
            Item.WhisperedHint: 200
        }

    def alt_success_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.LiberationOfNight: -3,
            Item.MirrorcatchBox: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }

class LeaveLightJericho(Action):
    def __init__(self):
        super().__init__("Leave the light as it is")
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RumourOfTheUpperRiver: 1
        }


# ==============================================================
#                           Indulge in Illicit Charity
# ==============================================================

class IndulgeInIllicitCharity(UpperRiverCard):
    def __init__(self):
        super().__init__("Indulge in Illicit Charity")
        self.actions = [
            FillAStomachJericho(),
            ComfortASuffererJericho(),
            AdoptWinsomeOrphans()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.JerichoLocks

class FillAStomachJericho(Action):
    def __init__(self):
        super().__init__("Fill a stomach")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.CrateOfIncorruptibleBiscuits, 0) >= 1
    
    def pass_rate(self, state: RailwayState):
        darkness_level = state.get_pyramidal_level(Item.JerichoLocksDarkness)
        return self.broad_pass_rate(400 - 50 * darkness_level, state.outfit.shadowy)

    def pass_items(self, state: RailwayState):
        return {
            Item.CrateOfIncorruptibleBiscuits: -1,
            Item.FavUrchins: 1,
            # Item.AdriftOnASeaOfMisery: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2
        }

class ComfortASuffererJericho(Action):
    def __init__(self):
        super().__init__("Comfort a sufferer")
    
    def pass_rate(self, state: RailwayState):
        darkness_level = state.get_pyramidal_level(Item.JerichoLocksDarkness)
        return self.broad_pass_rate(400 - 50 * darkness_level, state.outfit.shadowy)

    def pass_items(self, state: RailwayState):
        return {
            Item.WhisperedHint: 250,
            # Item.AdriftOnASeaOfMisery: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2
        }

# TODO this might be good depending on new tribute tapering
class AdoptWinsomeOrphans(Action):
    def __init__(self):
        super().__init__("Adopt a pair of Winsome Dispossessed Orphans")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.BasketOfRubberyPies, 0) >= 20 and \
    #           state.items.get(Item.TinnedHam, 0) >= 1
    
    def pass_items(self, state: RailwayState):
        return {
            Item.WinsomeDispossessedOrphan: 2,
            Item.BasketOfRubberyPies: -20,
            Item.TinnedHam: -1
        }

# ==============================================================
# Under the Statue at Jericho Locks Card and Actions
# ==============================================================

class UnderTheStatueAtJerichoLocks(UpperRiverCard):
    def __init__(self):
        super().__init__("Under the Statue at Jericho Locks")
        self.actions = [
            PracticeSketchingJericho(),
            TradeOnConnectionsJericho(),
            CallFavoursBishopSouthwarkJericho(),
            CallFavoursBishopStFiacresJericho(),
            ConverseWithScholarsJericho()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.JerichoLocks and \
            state.get(Item.JerichoLocksCommemorativeDevelopment) > 0


class PracticeSketchingJericho(Action):
    def __init__(self):
        super().__init__("Practice sketching the Statue to (subject)")
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.DropOfPrisonersHoney: 100
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }


class TradeOnConnectionsJericho(Action):
    def __init__(self):
        super().__init__("Trade on your academic and theological connections (Statue to the Dean of Xenotheology)")
    
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavChurch) >= 2
 
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavChurch: -2,
            Item.NoduleOfWarmAmber: 180
        }


class CallFavoursBishopSouthwarkJericho(Action):
    def __init__(self):
        super().__init__("Call in favours from the Church (Statue to the Bishop of Southwark)")
    
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavChurch) >= 1

        
    def pass_items(self, state: RailwayState):
        return {
            Item.FavChurch: -1,
            Item.StrongBackedLabour: 5
        }

class CallFavoursBishopStFiacresJericho(Action):
    def __init__(self):
        super().__init__("Call in favours from the Church (Statue to the Bishop of Saint Fiacre's)")
    
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavChurch) >= 4
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavChurch: -4,
            Item.HolyRelicOfTheThighOfStFiacre: 2,
            Item.BoneFragments: 500
        }

class ConverseWithScholarsJericho(Action):
    def __init__(self):
        super().__init__("Converse with a few retired scholars (Statue to Yourself, Preeminent Scholar of the Correspondence)")
    
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.get(Item.FavChurch) >= 1
        
    def pass_items(self, state: RailwayState):
        return {
            Item.FavChurch: -1,
            Item.WhisperedHint: 1200,
            Item.ExpertiseOfTheThirdCity: 5
        }



# ==============================================================
#                           Adjust the Lighting in Evenlode
# ==============================================================

class AdjustLightingEvenlode(UpperRiverCard):
    def __init__(self):
        super().__init__("Adjust the Lighting in Jericho Locks")
        self.actions = [
            BreakALampEvenlode(),
            RepairALampEvenlode(),
            GiveImpassionedSpeechEvenlode(),
            LeaveLightAsIsEvenlode()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.MagistracyOfTheEvenlode and \
            state.get_pyramidal_level(Item.MagistracyOfEvenlodeDarkness) < 7 and \
            state.get(Item.ColourAtTheChessboard) != 3

class BreakALampEvenlode(Action):
    def __init__(self):
        super().__init__("Break a lamp")
    
    def pass_rate(self, state: RailwayState):
        banditry_level = state.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver)
        return self.broad_pass_rate(400 - 50 * banditry_level, state.outfit.shadowy)
    
    def pass_items(self, state: RailwayState):
        return {
            # Item.Shadowy: 1,
            Item.AdvancingTheLiberationOfNight: 2,
            Item.MagistracyOfEvenlodeDarkness: 2
        }

    def fail_items(self, state: RailwayState):
        return {
            # Item.Shadowy: 1,
            Item.Suspicion: 2
        }

class RepairALampEvenlode(Action):
    def __init__(self):
        super().__init__("Repair a lamp")
    
    def can_perform(self, state: RailwayState):
        return state.get(Item.ColourAtTheChessboard) != 2
    
    def pass_rate(self, state: RailwayState):
        banditry_level = state.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver)
        return self.broad_pass_rate(50 * banditry_level, state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.Dangerous: 1,
            Item.MagistracyOfEvenlodeDarkness: -2
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2
        }

class GiveImpassionedSpeechEvenlode(Action):
    def __init__(self):
        super().__init__("Give an impassioned speech on Light and Beauty")
        self.alt_pass_rate = default_alt_pass_rate

    def can_perform(self, state: RailwayState):
        return state.get(Item.ColourAtTheChessboard) != 2
    
    def pass_rate(self, state: RailwayState):
        dc = 150 + 25 * state.get(Item.SupportingTheLiberationistTracklayers)
        return self.broad_pass_rate(dc, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.AdvancingTheLiberationOfNight: -3,
            Item.WhisperedHint: 200
        }

    def rare_success_items(self, state: RailwayState):
        return {
            Item.MirrorcatchBox: 1,
            Item.RomanticNotion: 5,
            Item.AdvancingTheLiberationOfNight: -3,
            Item.WhisperedHint: 200
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }

class LeaveLightAsIsEvenlode(Action):
    def __init__(self):
        super().__init__("Leave the light as it is")
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RumourOfTheUpperRiver: 1
        }
    
# ==============================================================
#                   Digs in the Magistracy of the Evenlode
# ==============================================================

class DigsInTheMagistracyOfTheEvenlode(UpperRiverCard):
    def __init__(self):
        super().__init__("Digs in the Magistracy of the Evenlode")
        self.actions = [
            SearchWhereWaterFlowsOut(),
            DigAtCrossroads(),
            HeadUphillEvenlode(),
            MakeTrainStopInHills(),
            MakeTrainStopPlainOfThirstyGrasses(),
            FlyOutToDigSite()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.MagistracyOfTheEvenlode


class SearchWhereWaterFlowsOut(Action):
    def __init__(self):
        super().__init__("Search where the water flows out")
    
    def pass_rate(self, state: RailwayState):
        darkness_level = state.items.get(Item.MagistracyOfEvenlodeDarkness, 0)
        return self.broad_pass_rate(50 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.FinBonesCollected: 2.5, # self.random_amount(1, 4),
            Item.AmbiguousEolith: 2.5, # self.random_amount(1, 4),
            Item.JadeFragment: 2.5 # self.random_amount(1, 4)
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.DeepZeeCatch: 1
        }


class DigAtCrossroads(Action):
    def __init__(self):
        super().__init__("Dig at the crossroads")
    
    def can_perform(self, state: RailwayState):
        return state.items.get(Item.SurveyOfTheNeathsBones, 0) >= 1
    
    def pass_rate(self, state: RailwayState):
        darkness_level = state.items.get(Item.MagistracyOfTheEvenlodeDarkness, 0)
        return self.broad_pass_rate(40 * darkness_level, state.outfit.watchful)

    def pass_items(self, state: RailwayState):
        return {
            Item.SurveyOfTheNeathsBones: -1,
            Item.TraceOfTheFirstCity: 10, #self.random_amount(4, 16),
            Item.ExpertiseOfTheFirstCity: 1
        }
    
    def alt_pass_items(self, state: GameState):
        return {
            Item.SurveyOfTheNeathsBones: -1,
            Item.FragmentOfWhiteGold: 1,
            Item.TraceOfTheFirstCity: 1,
            Item.ExpertiseOfTheFirstCity: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.SurveyOfTheNeathsBones: -1,
            Item.FirstCityCoin: 1
        }


class HeadUphillEvenlode(Action):
    def __init__(self):
        super().__init__("Head uphill")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.SurveyOfTheNeathsBones, 0) >= 15
    
    def pass_items(self, state: RailwayState):
        return {
            Item.SurveyOfTheNeathsBones: -15,
            Item.PalaeontologicalDiscovery: 1
        }


class MakeTrainStopInHills(Action):
    def __init__(self):
        super().__init__("Make the train take you to a designated stop in the hills")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.SurveyOfTheNeathsBones, 0) >= 120 \
    #         and state.items.get(Item.RouteTakenToEvenlode, 0) in {4, 5, 6}
    
    def pass_rate(self, state: RailwayState):
        banditry = state.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver)
        train_defense = state.items.get(Item.TrainDefences, 0)
        return self.broad_pass_rate(150 + 50 * (banditry - train_defense), state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.SurveyOfTheNeathsBones: -120,
            Item.PalaeontologicalDiscovery: 5
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2
        }

class MakeTrainStopPlainOfThirstyGrasses(Action):
    def __init__(self):
        super().__init__("Make the train stop in the Plain of Thirsty Grasses")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.SurveyOfTheNeathsBones, 0) >= 140 and \
    #         state.items.get(Item.RouteTakenToEvenlode, 0) in {3, 4, 5}
    
    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(5, state.outfit.kataleptic_toxicology)

    def pass_items(self, state: RailwayState):
        return {
            Item.SurveyOfTheNeathsBones: -140,
            Item.PalaeontologicalDiscovery: 6
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2
        }

class FlyOutToDigSite(Action):
    def __init__(self):
        super().__init__("Fly out to a dig site of your choosing")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.SurveyOfTheNeathsBones, 0) >= 240 and \
    #         state.items.get(Item.WingedAndTalonedSteed, 0) > 0
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(185, state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.SurveyOfTheNeathsBones: -240,
            Item.PalaeontologicalDiscovery: 10
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2 # TODO unknown number
        }


# ==============================================================
# Enlighten the Magistracy of the Evenlode Card and Actions
# ==============================================================

class EnlightenMagistracyEvenlode(UpperRiverCard):
    def __init__(self):
        super().__init__("Enlighten the Magistracy of the Evenlode")
        self.actions = [
            RepairLampEvenlode(),
            MakeImpassionedArgumentEvenlode(),
            LeaveLightAsIsEvenlode()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.MagistracyOfTheEvenlode


class RepairLampEvenlode(Action):
    def __init__(self):
        super().__init__("Repair a Lamp")
    
    def can_perform(self, state: RailwayState):
        return state.items.get(Item.ColourAtTheChessboard) in (1, 3)
    
    def pass_rate(self, state: RailwayState):
        banditry_level = state.get_pyramidal_level(Item.SeeingBanditryInTheUpperRiver)
        return self.broad_pass_rate(50 * banditry_level, state.outfit.dangerous)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.MagistracyOfTheEvenlodeDarkness: -2
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2
        }


class MakeImpassionedArgumentEvenlode(Action):
    def __init__(self):
        super().__init__("Make an Impassioned Argument for Light and Beauty")
        self.alt_pass_rate = 0.05

    def can_perform(self, state: RailwayState):
        return state.items.get(Item.ColourAtTheChessboard, 0) != 2
    
    def pass_rate(self, state: RailwayState):
        tracklayers_support = state.get(Item.SupportingTheLiberationistTracklayers)
        return self.broad_pass_rate(150 + 25 * tracklayers_support, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.WhisperedHint: 200,
            Item.AdvancingTheLiberationOfNight: -3
        }
    
    def rare_success_items(self, state: RailwayState):
        return {
            Item.MirrorcatchBox: 1,
            Item.RomanticNotion: 5,
            Item.AdvancingTheLiberationOfNight: -3
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }


class LeaveLightAsIsEvenlode(Action):
    def __init__(self):
        super().__init__("Leave the light as it is")
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RumourOfTheUpperRiver: 1
        }

# ==============================================================
#                       Under the Statue at the Magistracy
# ==============================================================

class UnderTheStatueMagistracy(UpperRiverCard):
    def __init__(self):
        super().__init__("Under the Statue at the Magistracy")
        self.actions = [
            PracticeSketchingStatueEvenlode(),
            CallInFavoursWithWidow(),
            ReceiveOfferingFromClayHighwayman(),
            SetWatchBesideStatueOfYourself()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.MagistracyOfTheEvenlode and \
            state.get(Item.MagistracyOfEvenlodeCommemorativeDevelopment) > 0


class PracticeSketchingStatueEvenlode(Action):
    def __init__(self):
        super().__init__("Practice sketching the Statue")
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.DropOfPrisonersHoney: 100
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }


class CallInFavoursWithWidow(Action):
    def __init__(self):
        super().__init__("Call in favours with the Gracious Widow")
    
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.items.get(Item.FavUrchins) >= 4
        
    def pass_items(self, state: RailwayState):
        return {
            Item.FavUrchins: -4,
            Item.PuzzleDamaskScrap: 1,
            Item.ThirstyBombazineScrap: 5,
            Item.Echo: 4.9 # Bundle of Oddities 1-659?, ballpark from wiki
        }


class ReceiveOfferingFromClayHighwayman(Action):
    def __init__(self):
        super().__init__("Receive an offering from the Clay Highwayman")
    
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.items.get(Item.FavCriminals) >= 2
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavCriminals: -2,
            Item.CertifiableScrap: 1,
            Item.MagnificentDiamond: 1,
            Item.FlawedDiamond: 42,
            # TODO: bundle of oddities, range varies with banditry
            Item.Echo: 4
        }

    def rare_success_items(self, state: RailwayState):
        return {
            Item.BundleOfOddities: (150, 450, 10 * state.items.get(Item.Banditry, 0))
        }


class SetWatchBesideStatueOfYourself(Action):
    def __init__(self):
        super().__init__("Set a Watch beside the Statue of Yourself")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.MagistracyCommemorativeDevelopment, 0) == 20
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.dangerous)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavConstables: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 1,
            Item.CertifiableScrap: 3
        }
    
# ==============================================================
#                   Balmoral in Gaslight
# ==============================================================

class BalmoralInGaslight(UpperRiverCard):
    def __init__(self):
        super().__init__("Balmoral in Gaslight")
        self.actions = [
            EnlightenBalmoral(),
            DarkenBalmoral(),
            BringInTombColonistTour(),
            EngageInSmuggling()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.Balmoral

class EnlightenBalmoral(Action):
    def __init__(self):
        super().__init__("Enlighten Balmoral")
    
    def can_perform(self, state: RailwayState):
        return state.get(Item.ColourAtTheChessboard) in [1, 3]  # White or Red Pieces
    
    def pass_rate(self, state: RailwayState):
        supporting_sum = sum([state.get(Item.SupportingTheLiberationistTracklayers),
                              state.get(Item.SupportingTheEmancipationistTracklayers),
                              state.get(Item.SupportingThePrehistoricistTracklayers)])
        base_difficulty = 220 + (50 * state.get(Item.SupportingTheLiberationistTracklayers) / (supporting_sum or 1))
        return self.broad_pass_rate(base_difficulty, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.AdvancingTheLiberationOfNight: -2,
            Item.BalmoralDarkness: -3
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 1
        }

class DarkenBalmoral(Action):
    def __init__(self):
        super().__init__("Darken Balmoral")
    
    def can_perform(self, state: RailwayState):
        return state.get_pyramidal_level(Item.BalmoralDarkness) < 8 and \
               state.items.get(Item.ColourAtTheChessboard, 0) in [1, 2]  # Black or Red Pieces
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(220, state.outfit.shadowy)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.AdvancingTheLiberationOfNight: 2,
            Item.BalmoralDarkness: 3
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 1
        }

class BringInTombColonistTour(Action):
    def __init__(self):
        super().__init__("Bring in a tomb-colonist tour")
    
    def pass_rate(self, state: RailwayState):
        dc = 180 + (10 * state.get_pyramidal_level(Item.BalmoralDarkness))
        return self.broad_pass_rate(dc, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.HinterlandScrip: (5 + state.get(Item.TrainLuxuries))
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.SeeingBanditryInTheUpperRiver: 1
        }


class EngageInSmuggling(Action):
    def __init__(self):
        super().__init__("Engage in a bit of smuggling")
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.ConsignmentOfScintillackSnuff, 0) > 0 and \
    #            state.items.get(Item.DiscoveredBalmoralDumbwaiter, 0) > 0
    
    def pass_rate(self, state: RailwayState):
        base_difficulty = 240 - (3 * state.items.get(Item.BalmoralDarkness, 0))
        return self.broad_pass_rate(base_difficulty, state.outfit.shadowy)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.ConsignmentOfScintillackSnuff: -1,
            Item.HinterlandScrip: (30 + state.banditry_level()),
            Item.SeeingBanditryInTheUpperRiver: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 1
        }
    
# ==============================================================
#                    Lead a Dig
# ==============================================================

class LeadADig(UpperRiverCard):
    def __init__(self):
        super().__init__("Lead a Dig")
        self.actions = [
            HeadUphillS8(),
            LeadExpeditionToHorizon()
        ]
        self.weight = 1.0  # Standard Frequency

    def can_draw(self, state: RailwayState):
        return state.location == Location.StationVIII

class HeadUphillS8(Action):
    def __init__(self):
        super().__init__("Head uphill")
    
    def can_perform(self, state: RailwayState):
        return state.skip_econ_inputs or state.get(Item.SurveyOfTheNeathBones) >= 40
    
    def pass_rate(self, state: RailwayState):
        base_difficulty = 175 + (25 * state.get(Item.StationVIIIDarkness))
        return self.broad_pass_rate(base_difficulty, state.outfit.watchful)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.SurveyOfTheNeathBones: -40,
            Item.PalaeontologicalDiscovery: 2
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2
        }

class LeadExpeditionToHorizon(Action):
    def __init__(self):
        super().__init__("Lead an expedition to the strangest point on the horizon")
    
    def can_perform(self, state: RailwayState):
        return state.skip_econ_inputs or \
            (state.items.get(Item.OilOfCompanionship, 0) >= 1 and \
               state.items.get(Item.RumourOfTheUpperRiver, 0) >= 98)
    
    def pass_rate(self, state: RailwayState):
        base_difficulty = 40 * state.get(Item.StationVIIIDarkness)
        # A False-Star of your Own reduces difficulty by 40
        if state.items.get(Item.FalseStarOfYourOwn, 0) > 0:
            base_difficulty -= 40
        return self.broad_pass_rate(base_difficulty, state.outfit.watchful)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.OilOfCompanionship: -1,
            Item.PrismaticFrame: 1,
            Item.RumourOfTheUpperRiver: -98
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2
        }
    
# ==============================================================
#                Under the Statue at Station VIII
# ==============================================================

class UnderTheStatueAtStationVIII(UpperRiverCard):
    def __init__(self):
        super().__init__("Under the Statue at Station VIII")
        self.actions = [
            PracticeSketchingStatueS8(),
            ReadTheGraffitiS8(),
            WriteSearingMessageS8()
        ]
        self.weight = 1.0  # Standard Frequency

    def can_draw(self, state: RailwayState):
        return state.location == Location.StationVIII and state.items.get(Item.StationVIIICommemorativeDevelopment, 0) > 0

class PracticeSketchingStatueS8(Action):
    def __init__(self):
        super().__init__("Practice sketching the Statue to (subject)")
    
    def pass_rate(self, state: RailwayState):
        base_difficulty = 250 - (10 * state.get(Item.StationVIIIDarkness))
        return self.broad_pass_rate(base_difficulty, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.DropOfPrisonersHoney: 110, # state.random.randint(100, 120)
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }

class ReadTheGraffitiS8(Action):
    def __init__(self):
        super().__init__("Read the graffiti on the Statue to (subject)")
    
    def pass_rate(self, state: RailwayState):
        correspondence_level = state.get(Item.AScholarOfTheCorrespondence)
        watchful_dc = 125 + (25 * state.get(Item.StationVIIIDarkness))
        # Either pass based on Watchful or A Scholar of the Correspondence
        return self.broad_pass_rate(watchful_dc, state.outfit.watchful) * \
               self.narrow_pass_rate(5, correspondence_level)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.UnusualLoveStory: 6 # state.random.randint(5, 7)
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2
        }

class WriteSearingMessageS8(Action):
    def __init__(self):
        super().__init__("Write something to sear the eyes of fools and lift up the great powers")
    
    def can_perform(self, state: RailwayState):
        # return state.items.get(Item.PotOfViolantInk, 0) > 0 and \
        return state.skip_econ_inputs or (
               state.items.get(Item.CorrespondencePlaques, 0) >= 4 and \
               state.items.get(Item.AeolianScream, 0) >= 3)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.CorrespondencePlaques: -4,
            Item.AeolianScream: -3,
            Item.StormThrenody: 1
        }


# ==============================================================
#                   Burrow in Heavenly Light
# ==============================================================

class BurrowInHeavenlyLight(UpperRiverCard):
    def __init__(self):
        super().__init__("Burrow in Heavenly Light")
        self.actions = [
            EnlightenBurrowInfraMump(),
            DarkenBurrowInfraMump(),
            PurchaseHereticalText(),
            EntertainBurnishedVicar()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        # TODO removable if church storyline unfinished
        return state.location == Location.BurrowInfraMump #and state.get(Item.ChurchInTheWild) >= 50

class EnlightenBurrowInfraMump(Action):
    def __init__(self):
        super().__init__("Enlighten Burrow-Infra-Mump")
    
    def can_perform(self, state: RailwayState):
        return state.get(Item.ColourAtTheChessboard) in [1, 3]  # White or Red Pieces
    
    def pass_rate(self, state: RailwayState):
        base_difficulty = 240
        return self.broad_pass_rate(base_difficulty, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.AdvancingTheLiberationOfNight: -2,
            Item.BurrowInfraMumpDarkness: -4
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 1
        }

class DarkenBurrowInfraMump(Action):
    def __init__(self):
        super().__init__("Darken Burrow-Infra-Mump")
    
    def can_perform(self, state: RailwayState):
        return state.get_pyramidal_level(Item.BurrowInfraMumpDarkness) < 8 and \
               state.items.get(Item.ColourAtTheChessboard, 0) in [1, 2]  # Black or Red Pieces
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(220, state.outfit.shadowy)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.AdvancingTheLiberationOfNight: 2,
            Item.BurrowInfraMumpDarkness: 3
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 1
        }

class PurchaseHereticalText(Action):
    def __init__(self):
        super().__init__("Purchase a heretical text")
    
    def can_perform(self, state: RailwayState):
        return state.get_pyramidal_level(Item.BurrowInfraMumpDarkness) >= 5 and \
            (state.skip_econ_inputs or state.get(Item.MoonPearl) >= 650)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.VerseOfCounterCreed: 1,
            Item.MoonPearl: -650
        }

class EntertainBurnishedVicar(Action):
    def __init__(self):
        super().__init__("Entertain a Burnished Vicar")
    
    def can_perform(self, state: RailwayState):
        return state.get_pyramidal_level(Item.BurrowInfraMumpDarkness) < 5 and \
            (state.skip_econ_inputs or state.get(Item.JasmineLeaves) >= 65)
     
    def pass_items(self, state: RailwayState):
        return {
            Item.VitalIntelligence: 1,
            Item.JasmineLeaves: -65
        }
    
# ==============================================================
#        Under the Statue at Burrow-Infra-Mump
# ==============================================================

class UnderTheStatueAtBurrowInfraMump(UpperRiverCard):
    def __init__(self):
        super().__init__("Under the Statue at Burrow-Infra-Mump")
        self.actions = [
            PracticeSketchingTheStatueBurrow(),
            DinnerWithCurate(),
            # PaleontologicalDiscussion(),
            TradeFavoursForBones(),
            SupplyHoneyForTheologicalSalon(),
            MeditateOnDeath(),
            MakeAddendumToTheology()
        ]
        self.weight = 1.0  # Standard Frequency

    def can_draw(self, state: RailwayState):
        return state.location == Location.BurrowInfraMump and \
            state.get(Item.BurrowInfraMumpCommemorativeDevelopment) >= 1

class PracticeSketchingTheStatueBurrow(Action):
    def __init__(self):
        super().__init__("Practice sketching the Statue")
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.DropOfPrisonersHoney: 100
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }

class DinnerWithCurate(Action):
    def __init__(self):
        super().__init__("Dinner with a Curate")
    
    def can_perform(self, state: RailwayState):
        has_econ = state.skip_econ_inputs or \
            state.get(Item.BottleOfGreyfields1868FirstSporing) >= 10
        has_fav = state.skip_favour_inputs or state.get(Item.FavChurch) >= 1
        return has_econ and has_fav
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavoursSociety: 1,
            Item.BottleOfGreyfields1868FirstSporing: -1,
            Item.FavoursTheChurch: -1
        }

# # TODO spicy but complicated
# class PaleontologicalDiscussion(Action):
#     def __init__(self):
#         super().__init__("An Evening of Palaeontological Discussion")
    
#     def can_perform(self, state: RailwayState):
#         return state.items.get(Item.SkeletonInProgress, 0) > 0 and \
#                state.items.get(Item.BurrowInfraMumpCommemorativeDevelopment) == 2 and \
#                state.items.get(Item.ConnectedBenthic, 0) >= 41
    
#     def pass_items(self, state: RailwayState):
#         skeleton_support = state.get(Item.SkeletonSupportCounterChurchTheology)
#         skeleton_value = state.get(Item.SkeletonValue)
#         return {
#             Item.RumourOfTheUpperRiver: 1,
#             Item.ConnectedBenthic: (2 * skeleton_support) + (skeleton_value // 1000)
#         }

class TradeFavoursForBones(Action):
    def __init__(self):
        super().__init__("Trade Favours for Bones")
        self.alt_pass_rate = default_alt_fail_rate
    
    # def can_perform(self, state: RailwayState):
    #     return state.get_pyramidal_level(Item.ConnectedBenthic) >= 20
    
    def pass_rate(self, state: RailwayState):
        return 0.5
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FlourishingRibcage: 1,
            Item.ConnectedBenthic: -70
        }
    
    def alt_pass_items(self, state: RailwayState):
        return {
            Item.PrismaticFrame: 1,
            Item.ConnectedBenthic: -200
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.FemurOfAJurassicBeast: 1,
            Item.HelicalThighbone: 1,
            Item.ConnectedBenthic: -60
        }

class SupplyHoneyForTheologicalSalon(Action):
    def __init__(self):
        super().__init__("Supply Honey for a Theological Salon")
    
    def can_perform(self, state: RailwayState):
        has_econ = state.skip_econ_inputs or state.get(Item.DropOfPrisonersHoney) >= 10
        has_fav = state.skip_favour_inputs or state.get(Item.FavBohemians) >= 1
        return has_econ and has_fav
    
    def pass_items(self, state: RailwayState):
        return {
            Item.FavRevolutionaries: 1,
            Item.DropOfPrisonersHoney: -10,
            Item.FavBohemians: -1
        }

class MeditateOnDeath(Action):
    def __init__(self):
        super().__init__("Meditate on Death")
        self.alt_pass_rate = default_alt_pass_rate
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.BurrowInfraMumpCommemorativeDevelopment) == 21
    
    # TODO: wild, never seen a challenge like this
    # def pass_rate(self, state: RailwayState):
    #     return self.broad_pass_rate(50, state.outfit.approaching_the_gates_of_the_garden)
    
    def pass_items(self, state: RailwayState):
        return {
            # Item.ApproachingTheGatesOfTheGarden: 5,
            Item.MemoryOfMuchLesserSelf: 1,
            Item.IncisiveObservation: 1
        }
    
    def alt_pass_items(self, state: RailwayState):
        return {
            # Item.ApproachingTheGatesOfTheGarden: 5,
            Item.MemoryOfMuchLesserSelf: 1,
            Item.HorseheadAmulet: 1
        }
    
    def fail_items(self, state: GameState):
        return {
            Item.MemoryOfMuchLesserSelf: 1
        }

class MakeAddendumToTheology(Action):
    def __init__(self):
        super().__init__("Make an addendum to the Church in the Wild's Theology")
    
    def can_perform(self, state: RailwayState):
        return state.skip_econ_inputs or (
               state.items.get(Item.ExtraordinaryImplication, 0) >= 2 and \
               state.items.get(Item.MemoryOfMuchLesserSelf, 0) >= 2
        )
    
    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(5, state.outfit.mithridacy)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.ExtraordinaryImplication: -2,
            Item.MemoryOfMuchLesserSelf: -2,
            Item.VerseOfCounterCreed: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 1,
            Item.Suspicion: 1
        }
    
# ==============================================================
#                   Moulin in Gaslight
# ==============================================================

class MoulinInGaslight(UpperRiverCard):
    def __init__(self):
        super().__init__("Moulin in Gaslight")
        self.actions = [
            EnlightenMoulin(),
            DarkenMoulin(),
            BringInHistoricalTour(),
            EngageInLarceny()
        ]
        self.weight = 1.0  # Standard Frequency

    def can_draw(self, state: RailwayState):
        return state.location == Location.Moulin

class EnlightenMoulin(Action):
    def __init__(self):
        super().__init__("Enlighten Moulin")
    
    def can_perform(self, state: RailwayState):
        return state.get(Item.MoulinDarkness) > 0 and \
               state.get(Item.ColourAtTheChessboard) in [2, 3]  # Red or White Pieces
    
    def pass_rate(self, state: RailwayState):
        supporting_sum = sum([state.get(Item.SupportingTheLiberationistTracklayers),
                              state.get(Item.SupportingTheEmancipationistTracklayers),
                              state.get(Item.SupportingThePrehistoricistTracklayers)])
        base_difficulty = 220 + (50 * state.get(Item.SupportingTheLiberationistTracklayers) / (supporting_sum or 1))
        return self.broad_pass_rate(base_difficulty, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.AdvancingTheLiberationOfNight: -4,
            Item.MoulinDarkness: -2
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 1
        }

class DarkenMoulin(Action):
    def __init__(self):
        super().__init__("Darken Moulin")
    
    def can_perform(self, state: RailwayState):
        return state.get(Item.MoulinDarkness) < 8 and \
               state.get(Item.ColourAtTheChessboard) in [1, 2]  # Black or Red Pieces
    
    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(220, state.outfit.shadowy)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.AdvancingTheLiberationOfNight: 3,
            Item.MoulinDarkness: 2
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 1
        }

class BringInHistoricalTour(Action):
    def __init__(self):
        super().__init__("Bring in a historical tour")
    
    def pass_rate(self, state: RailwayState):
        base_difficulty = 180 + (10 * state.get(Item.MoulinDarkness))
        return self.broad_pass_rate(base_difficulty, state.outfit.persuasive)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.HinterlandScrip: (4 + state.get(Item.TrainLuxuries))
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.SeeingBanditryInTheUpperRiver: 1,
            Item.MoonPearl: 50
        }

class EngageInLarceny(Action):
    def __init__(self):
        super().__init__("Engage in a spot of larceny")
        self.alt_pass_rate = default_alt_pass_rate
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.SetOfIntricateKifers, 0) > 0
    
    def pass_rate(self, state: RailwayState):
        base_difficulty = 240 - (10 * state.get(Item.MoulinDarkness))
        return self.broad_pass_rate(base_difficulty, state.outfit.shadowy)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.JustificandeCoin: 1,
            Item.FirstCityCoin: (1 + state.banditry_level())
        }
    
    def alt_pass_items(self, state: GameState):
        return {
            # Item.AncientHuntingRifle # TODO
            Item.Echo: 12.50
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Suspicion: 2
        }
    
# ==============================================================
#                   Under the Statue at Moulin
# ==============================================================

class UnderTheStatueAtMoulin(UpperRiverCard):
    def __init__(self):
        super().__init__("Under the Statue at Moulin")
        self.actions = [
            PracticeSketchingMoulinStatue(),
            ShareDrinkWithZailor(),
            ShareTaleOfTravels(),
            MakeContactWithAgent(),
            DrawInspirationForMonograph(),
            DeliverLectureOnParabolanHistoriography(),
            DeliverLectureOnLondonsHistory(),
            DeliverLectureOnNeathyHistory(),
            DeliverLectureOnHellsHistory()
        ]
        self.weight = 1.0  # Standard Frequency

    def can_draw(self, state: RailwayState):
        return state.location == Location.Moulin and state.get(Item.MoulinCommemorativeDevelopment) > 0

class PracticeSketchingMoulinStatue(Action):
    def __init__(self):
        super().__init__("Practice sketching the Statue")

    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.persuasive)

    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.DropOfPrisonersHoney: 100
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Scandal: 2
        }

class ShareDrinkWithZailor(Action):
    def __init__(self):
        super().__init__("Share a drink with a Zailor")
        self.alt_pass_rate = default_alt_pass_rate

    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.items.get(Item.FavDocks, 0) >= 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavDocks: -4,
            Item.PuzzlingMap: 2,
            Item.MapScrap: 50
        }

    def alt_pass_items(self, state: RailwayState):
        return {
            Item.FavDocks: -4,
            Item.SaltSteppeAtlas: 1
        }

class ShareTaleOfTravels(Action):
    def __init__(self):
        super().__init__("Share a tale of your travels")

    def can_perform(self, state: RailwayState):
        has_econ = state.skip_econ_inputs or state.items.get(Item.ZeeZtory, 0)
        
    def pass_items(self, state: RailwayState):
        return {
            Item.FavDocks: 1,
            Item.MagisterialLager: 1,
            Item.ZeeZtory: -1
        }

class MakeContactWithAgent(Action):
    def __init__(self):
        super().__init__("Make contact with an agent")

    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.items.get(Item.FavGreatGame, 0) >= 2

    def pass_items(self, state: RailwayState):
        return {
            Item.FavGreatGame: -2,
            Item.VitalIntelligence: 1,
            Item.MovesInTheGreatGame: 11
        }

class DrawInspirationForMonograph(Action):
    def __init__(self):
        super().__init__("Draw inspiration for a Monograph")

    # def can_perform(self, state: RailwayState):
    #     return 10 <= state.get(Item.MoulinCommemorativeDevelopment) <= 20 and \
    #            state.items.get(Item.ObjectOfHistoricalStudy, 0) > 0

    def pass_items(self, state: RailwayState):
        return {
            Item.CrypticClue: 175
        }

class DeliverLectureOnParabolanHistoriography(Action):
    def __init__(self):
        super().__init__("Deliver a lecture on Parabolan Historiography")

    # def can_perform(self, state: RailwayState):
    #     return 10 <= state.get(Item.MoulinCommemorativeDevelopment) <= 20 and \
    #            state.items.get(Item.RenownBohemians, 0) >= 10 and \
    #            100 <= state.items.get(Item.ObjectOfHistoricalStudy, 0) <= 130 and \
    #            state.items.get(Item.FavoursBohemians, 0) < 7

    def pass_items(self, state: RailwayState):
        return {
            Item.FavBohemians: 1
        }

class DeliverLectureOnLondonsHistory(Action):
    def __init__(self):
        super().__init__("Deliver a lecture on London's History")

    # def can_perform(self, state: RailwayState):
    #     return 10 <= state.get(Item.MoulinCommemorativeDevelopment) <= 20 and \
    #            state.items.get(Item.RenownTheChurch, 0) >= 10 and \
    #            210 <= state.items.get(Item.ObjectOfHistoricalStudy, 0) <= 240 and \
    #            state.items.get(Item.FavoursTheChurch, 0) < 7

    def pass_items(self, state: RailwayState):
        return {
            Item.FavChurch: 1
        }

class DeliverLectureOnNeathyHistory(Action):
    def __init__(self):
        super().__init__("Deliver a lecture on Neathy History")

    # def can_perform(self, state: RailwayState):
    #     return 10 <= state.get(Item.MoulinCommemorativeDevelopment) <= 20 and \
    #            state.items.get(Item.RenownTheGreatGame, 0) >= 10 and \
    #            300 <= state.items.get(Item.ObjectOfHistoricalStudy, 0) <= 400 and \
    #            state.items.get(Item.FavoursTheGreatGame, 0) < 7

    def pass_items(self, state: RailwayState):
        return {
            Item.FavGreatGame: 1
        }

class DeliverLectureOnHellsHistory(Action):
    def __init__(self):
        super().__init__("Deliver a lecture on Hell's History")

    # def can_perform(self, state: RailwayState):
    #     return 10 <= state.get(Item.MoulinCommemorativeDevelopment) <= 20 and \
    #            state.items.get(Item.RenownHell, 0) >= 10 and \
    #            state.items.get(Item.ObjectOfHistoricalStudy, 0) >= 500 and \
    #            state.items.get(Item.FavoursHell, 0) < 7

    def pass_items(self, state: RailwayState):
        return {
            Item.FavHell: 1
        }


# ==============================================================
#                   Grazing Goat-Demons
# ==============================================================

class GrazingGoatDemons(UpperRiverCard):
    def __init__(self):
        super().__init__("Grazing Goat-Demons")
        self.actions = [
            FeedPeppercapsToGoatDemons(),
            TryToPetGoatDemon(),
            # FindCaprineVagabond()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.Hurlers


class FeedPeppercapsToGoatDemons(Action):
    def __init__(self):
        super().__init__("Feed them some peppercaps")
    
    def can_perform(self, state: RailwayState):
        has_econ = state.skip_econ_inputs or state.get(Item.HandPickedPeppercaps) >= 5

    def pass_items(self, state: RailwayState):
        return {
            Item.HandPickedPeppercaps: -5,
            Item.FavoursHell: 1
        }


class TryToPetGoatDemon(Action):
    def __init__(self):
        super().__init__("Try to pet one")

    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(250, state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.Wounds: 1,
            Item.FemurOfAJurassicBeast: 1,
            Item.HardEarnedLesson: 1
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2
        }


# class FindCaprineVagabond(Action):
#     def __init__(self):
#         super().__init__("Find the Caprine Vagabond in the herd")
    
#     def can_perform(self, state: RailwayState):
#         return state.items.get(Item.GoneGrazing, 0) > 0

#     def pass_rate(self, state: RailwayState):
#         discordant_law = state.items.get(Item.DiscordantLaw, 0)
#         return self.broad_pass_rate(220 - (20 * discordant_law), state.outfit.watchful)

#     def pass_items(self, state: RailwayState):
#         discordant_law = state.items.get(Item.DiscordantLaw, 0)
#         state.items[Item.GoneGrazing] = 0  # Removes all Gone Grazing

#         if discordant_law == 0:
#             return {
#                 Item.ExtraordinaryImplication: 1,
#                 Item.CrypticClue: 44
#             }
#         elif discordant_law <= 2:
#             return {
#                 Item.AnIdentityUncovered: 1,
#                 Item.CrypticClue: 44
#             }
#         elif discordant_law <= 4:
#             return {
#                 Item.VolumeOfCollatedResearch: 1,
#                 Item.CrypticClue: 44
#             }
#         else:
#             return {
#                 Item.ViennaOpening: 1,
#                 Item.CrypticClue: 44
#             }

# ==============================================================
#                   Under the Statue at the Hurlers
# ==============================================================

class UnderTheStatueAtTheHurlers(UpperRiverCard):
    def __init__(self):
        super().__init__("Under the Statue at the Hurlers")
        self.actions = [
            PracticeSketchingStatueHurlers(),
            CallInFavoursFromRevolutionariesHurlers(),
            SleepBesideStatueFingerkings(),
            CallInFavoursFromTheChurchHurlers(),
            CallInFavoursFromHellGoatDemons(),
            AskOvergoatToPerformTrick(),
            AskUbergoatToPerformTrick(),
            AskHeptagoatToPerformTrick(),
            MeditateInStatueShadow()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.Hurlers and state.get(Item.HurlersCommemorativeDevelopment)


class PracticeSketchingStatueHurlers(Action):
    def __init__(self):
        super().__init__("Practice sketching the Statue")

    def pass_rate(self, state: RailwayState):
        return self.broad_pass_rate(200, state.outfit.dangerous)

    def pass_items(self, state: RailwayState):
        return {
            Item.RomanticNotion: 5,
            Item.DropOfPrisonersHoney: 100
        }

    def fail_items(self, state: RailwayState):
        return {
            Item.Wounds: 2
        }


class CallInFavoursFromRevolutionariesHurlers(Action):
    def __init__(self):
        super().__init__("Call in favours from Revolutionaries")
    
    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.items.get(Item.FavRevolutionaries, 0) >= 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavRevolutionaries: -4,
            Item.NightOnTheTown: 12,
            Item.AdvancingTheLiberationOfNight: 1
        }


class SleepBesideStatueFingerkings(Action):
    def __init__(self):
        super().__init__("Sleep beside the statue (Fingerkings)")
    
    def pass_items(self, state: RailwayState):
        # TODO unclear scaling
        # connected_fingerkings = state.get_pyramidal_level(Item.ConnectedFingerkings, 0)
        return {
            Item.SightingOfAParabolanLandmark: 55
        }


class CallInFavoursFromTheChurchHurlers(Action):
    def __init__(self):
        super().__init__("Call in favours from The Church")

    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.items.get(Item.FavChurch, 0) >= 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavChurch: -4,
            Item.VolumeOfCollatedResearch: 12
        }


class CallInFavoursFromHellGoatDemons(Action):
    def __init__(self):
        super().__init__("Call in favours from Hell (Goat-Demons)")

    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.items.get(Item.FavHell, 0) >= 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavHell: -4,
            Item.NightsoilOfTheBazaar: 60
        }


class AskOvergoatToPerformTrick(Action):
    def __init__(self):
        super().__init__("Ask your Overgoat to perform a trick")

    def can_perform(self, state: RailwayState):
        # return state.items.get(Item.Overgoat, 0) > 0 an
        return state.skip_favour_inputs or state.items.get(Item.FavHell, 0) >= 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavHell: -4,
            Item.AeolianScream: 12
        }


class AskUbergoatToPerformTrick(Action):
    def __init__(self):
        super().__init__("Ask your Übergoat to perform a trick")

    def can_perform(self, state: RailwayState):
        # return state.items.get(Item.Ubergoat, 0) > 0 and
        return state.skip_favour_inputs or state.items.get(Item.FavHell, 0) >= 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavHell: -4,
            Item.VolumeOfCollatedResearch: 12
        }


class AskHeptagoatToPerformTrick(Action):
    def __init__(self):
        super().__init__("Ask your Heptagoat to perform a trick")

    def can_perform(self, state: RailwayState):
        # return state.items.get(Item.Heptagoat, 0) > 0 and 
        return state.skip_favour_inputs or state.items.get(Item.FavHell, 0) >= 7

    def pass_items(self, state: RailwayState):
        return {
            Item.TracklayersDispleasure: -1,  # TODO unknown value
            Item.FavoursHell: -7,
            Item.PrimordialShriek: 777
        }

class MeditateInStatueShadow(Action):
    def __init__(self):
        super().__init__("Meditate in your statue's shadow")

    def can_perform(self, state: RailwayState):
        return state.skip_econ_inputs or state.items.get(Item.MemoryOfDiscordance, 0) >= 2

    def pass_items(self, state: RailwayState):
        return {
            Item.MemoryOfDiscordance: -2,
            Item.CorrespondencePlaque: 60
        }

# ==============================================================
#                   Under the Statue at Marigold Station
# ==============================================================

class UnderTheStatueAtMarigoldStation(UpperRiverCard):
    def __init__(self):
        super().__init__("Under the Statue at Marigold Station")
        self.actions = [
            SellSurplusRailwaySteel(),
            CallInFavoursWithTracklayersUnion(),
            SitByYourStatue(),
            AdmireTheStatue()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: RailwayState):
        return state.location == Location.MarigoldStation and state.get(Item.MarigoldCommemorativeDevelopment)


class SellSurplusRailwaySteel(Action):
    def __init__(self):
        super().__init__("Sell surplus Railway Steel to the Moloch Line")

    def can_perform(self, state: RailwayState):
        has_econ = state.skip_econ_inputs or state.items.get(Item.RailwaySteel, 0) > 0

    def pass_items(self, state: RailwayState):
        return {
            Item.RailwaySteel: -1,
            Item.SilentSoul: 1,
            Item.FavHell: 1
        }


class CallInFavoursWithTracklayersUnion(Action):
    def __init__(self):
        super().__init__("Call in favours with the Tracklayer's Union")

    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.items.get(Item.FavRevolutionaries, 0) >= 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavRevolutionaries: -4,
            Item.VitalIntelligence: 2,
            Item.ViennaOpening: 2
        }

    # def pass_items_january(self, state: RailwayState):
    #     return {
    #         Item.FavoursRevolutionaries: -4,
    #         Item.VitalIntelligence: 2,
    #         Item.ViennaOpening: 2,
    #         Item.AdvancingTheLiberationOfNight: 1  # Specific to the January Statue
    #     }

class SitByYourStatue(Action):
    def __init__(self):
        super().__init__("Sit by your statue")

    def can_perform(self, state: RailwayState):
        return state.skip_favour_inputs or state.items.get(Item.FavCriminals, 0) >= 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavCriminals: -4,
            Item.UnlawfulDevice: 1,
            Item.CaveAgedCodeOfHonour: 1,
            Item.CompromisingDocument: 10
        }

class AdmireTheStatue(Action):
    def __init__(self):
        super().__init__("Admire the statue")

    def can_perform(self, state: RailwayState):
        return state.items.get(Item.FavSociety, 0) >= 4

    def pass_items(self, state: RailwayState):
        return {
            Item.FavSociety: -4,
            Item.MagnificentDiamond: 2,
            Item.FlawedDiamond: 45
        }


class RailwaySimulationRunner(SimulationRunner):
    def __init__(self, runs: int, initial_values: dict, location: Location):
        super().__init__(runs, initial_values)

        self.location = location
        self.storylets = [
            # AlwaysAvailable()
        ]

        self.cards = [
            # All locations
            DisillusionedFungiculturalist(),
            JurisdictionalDispute(),
            UnattendedMirror(),
            EngageInSomeMinorSmuggling(),
            HalfwayToHell(),
            InterveneInAnAttack(),
            MeetingInADarkAlley(),
            RespectablePassengers(),
            RisingReportsOfBanditry(),
            RailwayAndTheGreatGame(),
            UrchinsGames(),
            WhichMeeting(),
            YourVeryOwnHellworm(),

            # Ealing
            AdjustLightingInEalingGardens(),
            UnderTheStatueEaling(),
            Constellations(),
            EngageInExcavation(),
            EngageInUnobservedCharity(),
            MinistryEnforcement(),
            RubberyObservances(),
            # SetUpYourOwnBearShow()

            # Jericho
            AdjustLightingJerichoLocks(),
            DredgeTheRiverJericho(),
            EnlightenJerichoLocks(),
            IndulgeInIllicitCharity(),
            UnderTheStatueAtJerichoLocks(),

            # Evenlode
            AdjustLightingEvenlode(),
            DigsInTheMagistracyOfTheEvenlode(),
            EnlightenMagistracyEvenlode(),
            UnderTheStatueMagistracy(),

            # Balmoral
            BalmoralInGaslight(),

            # Station VIII
            LeadADig(),
            UnderTheStatueAtStationVIII(),

            # Burrow
            BurrowInHeavenlyLight(),
            UnderTheStatueAtBurrowInfraMump(),

            # Moulin
            MoulinInGaslight(),
            UnderTheStatueAtMoulin(),

            # Hurlers
            GrazingGoatDemons(),
            UnderTheStatueAtTheHurlers(),

            # Marigold
            UnderTheStatueAtMarigoldStation()
        ]

    def create_state(self) -> GameState:
        return RailwayState(self.location)
    
    def print_item_summary(self):
        print(f"Location: {self.location.name}")
        max_name_length = 35
        print(f"\n{'Item':<35}{'Per Run':>15}{'Echo':>10}{'EPA':>10}{'Scrip':>10}{'SPA':>10}")
        print("-" * 85)

        total_echo_value = 0.0
        total_scrip_value = 0.0
        item_summaries = []

        for item, total_change in self.total_item_changes.items():
            initial_qty = self.initial_values.get(item, 0) * self.runs
            net_change = total_change - initial_qty

            avg_change = net_change / self.runs
            echo_value = simulations.item_conversions.conversion_rate(item, Item.Echo)
            scrip_value = simulations.item_conversions.conversion_rate(item, Item.HinterlandScrip)

            estimated = False
            if echo_value == 0:
                if scrip_value != 0:
                    echo_value = scrip_value * simulations.item_conversions.conversion_rate(Item.HinterlandScrip, Item.Echo)
                else:
                    echo_value = simulations.item_conversions.conversion_rate(item, Item._ApproximateEchoValue)
                    estimated = True

            item_total_echo_value = echo_value * net_change
            item_total_scrip_value = scrip_value * net_change

            total_echo_value += item_total_echo_value
            total_scrip_value += item_total_scrip_value
            truncated_item_name = item.name if len(item.name) <= max_name_length else item.name[:max_name_length - 3] + "..."

            # HACK was acting odd with some initial values
            if abs(avg_change) > 0.0001:
                item_summaries.append((
                    truncated_item_name,
                    avg_change,
                    echo_value,
                    item_total_echo_value / self.total_actions,
                    scrip_value,
                    item_total_scrip_value / self.total_actions,
                    estimated))

        item_summaries.sort(key=lambda x: x[1], reverse=True)

        for item_name, avg_change, echo_value, echo_per_action, scrip_value, scrip_per_action, estimated in item_summaries:
            table_row = f"{item_name:<35}{avg_change:>15.2f}{echo_value:>10.2f}{'*' if estimated else ' '}{echo_per_action:>9.2f}"
            table_row += f"{scrip_value:>10.2f}{scrip_per_action:>10.2f}"
            print(table_row)
            # print(f"{item_name:<35}{avg_change:>15.2f}{echo_value:>10.2f}{'*' if estimated else ''}{echo_per_action:>10.2f}{scrip_value:>10.2f}{scrip_per_action:>10.2f}")

        print(f"\n{'Totals**':<35}{total_echo_value / self.total_actions:>35.2f}{total_scrip_value / self.total_actions:>20.2f}")


simulation = RailwaySimulationRunner(
    runs = 100,
    location = Location.Balmoral,

    initial_values= {
        Item.ColourAtTheChessboard: 1,

        Item.TrainLuxuries: 6,
        Item.TrainDefences: 6,
        Item.TrainBaggageAccomodations: 6,
        Item.SeeingBanditryInTheUpperRiver: 0,

        Item.MoonPearl: 20_000,
        Item.InTheCompanyOfAHellworm: 1,
        # Item.HellwormSaddle: 1,
    
        Item.EalingGardensCommemorativeDevelopment: 99,
        Item.JerichoLocksCommemorativeDevelopment: 99,
        Item.MagistracyOfEvenlodeCommemorativeDevelopment: 99,
        Item.BalmoralCommemorativeDevelopment: 99,
        Item.StationVIIICommemorativeDevelopment: 99,
        Item.BurrowInfraMumpCommemorativeDevelopment: 99,
        Item.MoulinCommemorativeDevelopment: 99,
        Item.HurlersCommemorativeDevelopment: 99,
        Item.MarigoldCommemorativeDevelopment: 99,

        Item.EalingGardensDarkness: utils.pyramid(7),
        Item.JerichoLocksDarkness: utils.pyramid(7),
        Item.MagistracyOfEvenlodeDarkness: utils.pyramid(7),
        Item.BalmoralDarkness: utils.pyramid(1),
        Item.StationVIIIDarkness: utils.pyramid(1),
        Item.BurrowInfraMumpDarkness: utils.pyramid(5),
        Item.MoulinCommemorativeDevelopment: utils.pyramid(5),
        Item.HurlersDarkness: utils.pyramid(5),
        # Item.MarigoldDarkness: utils.pyramid(2),
    })

simulation.outfit = PlayerOutfit(334, 18)

simulation.run_simulation()