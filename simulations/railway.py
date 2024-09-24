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


class RailwayState(GameState):
    def __init__(self, location: Location):
        super().__init__(max_hand_size=5)
        self.location = location
        self.ev_threshold = 5.25

    def ev_from_item(self, item, val: int):
        # if item == Item.SeeingBanditryInTheUpperRiver:
        #     if self.banditry_level() > 5:
        #         return val * -3

        scrip_value = conversion_rate(item, Item.HinterlandScrip)
        echo_value = conversion_rate(item, Item.Echo)
        scrip_to_echo_value = scrip_value * 63.5/125

        echo_value = max(echo_value, scrip_to_echo_value)
        if echo_value != 0:
            return val * echo_value
        else:
            return val * conversion_rate(item, Item._ApproximateEchoValue)
    
    def banditry_level(self):
        return utils.pyramid(self.items.get(Item.SeeingBanditryInTheUpperRiver, 0))

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

# Skip cards that are avoidable or non-repeatable

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


# Bad? cards with specific item
Tomb Colonist Tour
Canal Workers on the Upper River
God's Editors at Burrow-Infra-Mump
    might be worthwhile still, check back

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
    
    # def can_perform(self, state: RailwayState):
    #     return state.items.get(Item.NightsoilOfTheBazaar, 0) >= 10
    
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
    
    # def can_perform(self, state: RailwayState):
    #     return (state.items.get(Item.VerseOfCounterCreed, 0) > 0 and 
    #             state.items.get(Item.ASubmergedRector, 0) > 0)
    
    def pass_items(self, state: RailwayState):
        return {
            Item.VerseOfCounterCreed: -1,  # Lose 1 Verse of Counter-Creed
            Item.HinterlandScrip: 36  # Gain 36 Hinterland Scrip
        }


class ArrangeTitledSurveyor(Action):
    def __init__(self):
        super().__init__("Arrange the services of a Titled Surveyor")
    
    # def can_perform(self, state: RailwayState):
    #     return (state.items.get(Item.InCorporateDebt, 0) > 0 and 
    #             state.items.get(Item.FavoursSociety, 0) >= 3)
    
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
            VisitParabolanBaseCampNonSilverer(),
            VisitParabolanBaseCampSilverer(),
            GoToMoonlitChessboard(),
            GoToReflectionOfLaboratory(),
            GoToDomeOfScales(),
            GoToViricJungle()
        ]
        self.weight = 0.5  # Very Infrequent Frequency

    # def can_draw(self, state: RailwayState):
    #     return state.items.get(Item.AccessParabolanBaseCamp, 0) > 0


class VisitParabolanBaseCampNonSilverer(Action):
    def __init__(self):
        super().__init__("Visit your Parabolan Base-Camp (non-Silverer)")
    
    def can_perform(self, state: RailwayState):
        return state.items.get(Item.DropOfPrisonersHoney, 0) >= 100 and \
               state.items.get(Item.SetOfCosmogoneSpectacles, 0) == 0

    def pass_items(self, state: RailwayState):
        return {
            Item.DropOfPrisonersHoney: -100  # Lose 100 x Drop of Prisoner's Honey
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
        }

    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(2, state.outfit.glasswork)

    def on_success(self, state: RailwayState):
        state.move_to_location(Location.ParabolanBaseCamp)


class VisitParabolanBaseCampSilverer(Action):
    def __init__(self):
        super().__init__("Visit your Parabolan Base-Camp (Silverer)")

    def can_perform(self, state: RailwayState):
        return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
               state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0

    def pass_items(self, state: RailwayState):
        return {
            Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
        }

    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(2, state.outfit.glasswork)

    def on_success(self, state: RailwayState):
        state.move_to_location(Location.ParabolanBaseCamp)


class GoToMoonlitChessboard(Action):
    def __init__(self):
        super().__init__("Go straight to the Moonlit Chessboard")

    def can_perform(self, state: RailwayState):
        return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
               state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0 and \
               state.items.get(Item.RouteChessboard, 0) > 0

    def pass_items(self, state: RailwayState):
        return {
            Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
        }

    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(2, state.outfit.glasswork)

    def on_success(self, state: RailwayState):
        state.move_to_location(Location.MoonlitChessboard)


class GoToReflectionOfLaboratory(Action):
    def __init__(self):
        super().__init__("Go straight to the Reflection of Your Laboratory")

    def can_perform(self, state: RailwayState):
        return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
               state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0 and \
               state.items.get(Item.RouteReflectionLaboratory, 0) > 0

    def pass_items(self, state: RailwayState):
        return {
            Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
        }

    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(2, state.outfit.glasswork)

    def on_success(self, state: RailwayState):
        state.move_to_location(Location.ReflectionLaboratory)


class GoToDomeOfScales(Action):
    def __init__(self):
        super().__init__("Go straight to the Dome of Scales")

    def can_perform(self, state: RailwayState):
        return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
               state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0 and \
               state.items.get(Item.RouteDomeOfScales, 0) > 0

    def pass_items(self, state: RailwayState):
        return {
            Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
        }

    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(2, state.outfit.glasswork)

    def on_success(self, state: RailwayState):
        state.move_to_location(Location.DomeOfScales)


class GoToViricJungle(Action):
    def __init__(self):
        super().__init__("Go straight to the Viric Jungle")

    def can_perform(self, state: RailwayState):
        return state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and \
               state.items.get(Item.SetOfCosmogoneSpectacles, 0) > 0 and \
               state.items.get(Item.RouteViricJungle, 0) > 0

    def pass_items(self, state: RailwayState):
        return {
            Item.DropOfPrisonersHoney: -50  # Lose 50 x Drop of Prisoner's Honey
        }
    
    def fail_items(self, state: RailwayState):
        return {
            Item.Nightmares: 2  # Gain 2 CP Nightmares on failure
        }

    def pass_rate(self, state: RailwayState):
        return self.narrow_pass_rate(2, state.outfit.glasswork)

    def on_success(self, state: RailwayState):
        state.move_to_location(Location.ViricJungle)

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
            Item.SeeingBanditryInTheUpperRiver: -1,
            Item.PieceOfRostygold: 400,
        }
    
    def alt_pass_items(self, state: RailwayState):
        return {
            Item.SeeingBanditryInTheUpperRiver: -1,
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

class RespectablePassengers(UpperRiverCard):
    def __init__(self):
        super().__init__("Respectable Passengers")
        self.actions = [
            ContributeEvidenceWithJudge(),
            ContributeEvidenceWithoutJudge(),
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
            Item.SeeingBanditryInTheUpperRiver: 1 if state.banditry_level() < 36 else 0
        }

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
        return state.items.get(Item.SeeingBanditryInTheUpperRiver, 0) >= 36


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

            # Ealing
            AdjustLightingInEalingGardens()
        ]

    def create_state(self) -> GameState:
        return RailwayState(self.location)
    

simulation = RailwaySimulationRunner(
    runs = 100,
    location = Location.EalingGardens,
    initial_values= {
        Item.SeeingBanditryInTheUpperRiver: 28
    })

simulation.outfit = PlayerOutfit(330, 18)

simulation.run_simulation()    