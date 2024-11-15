import random
import sys
import math
from collections import defaultdict
from enum import Enum, auto
import helper.utils as utils
from enums import *
from simulations.item_conversions import conversion_rate
from simulations.models import *
from simulations.models import GameState

'''
Don't try to model "Overdue" event. Just add a disclamer error of 0..1 actions


Frags worth more than Routes? due to conversion via Atrium?
If we could get 12 Cthono, Index2 might be OK
Problem is dealing with God's Eye View
Need 10+ Frags to 100% Atrium2

Flowering Gallery has 100%-able check for 2 frags\
'''

class ApocryphaSoughtBook(Enum):
    IndexOfBannedWorks = 201
    AnnalOfDeadStars = 202
    LePrecipiceDeLaTombee = 203
    CodexOfUnrealPlaces = 204
    BookOfProperSpeech = 205
    ChainedOctavo = 1001

class LibraryState(GameState):
    def __init__(self):
        super().__init__(max_hand_size=4)
        # print("LibraryState__init__")

        self.status = "InProgress"

        # self.outfit = PlayerOutfit(330, 18)

        self.items = {
            Item._StacksProgress: 0,
            Item.RouteTracedThroughTheLibrary: 0,
            Item.FragmentaryOntology: 0,
            Item.LibraryKey: 0,
        }

        self.cartographer_enabled = True
        self.allow_cartographer_toggle = False

        self.storylets = []
        self.hand = []
        self.deck = []

    def step(self):

        best_card, best_action = self.best_action_by_simple_ranking()

        # best_card, best_action, best_action_ev = None, None, -float('inf')

        # for card in self.storylets:
        #     for action in card.actions:
        #         if action.can_perform(self):
        #             action_ev = action.ev(self)
        #             if action_ev > best_action_ev:
        #                 best_card, best_action, best_action_ev = card, action, action_ev

        # for card in self.hand:
        #     for action in card.actions:
        #         if action.can_perform(self):
        #             action_ev = action.ev(self)
        #             if action_ev > best_action_ev:
        #                 best_card, best_action, best_action_ev = card, action, action_ev

        if best_action is None:
            # TODO log or default to other strat?
            print("Cards in hand: " + str(len(self.hand)))
            for card in self.hand:
                print(card.name)
            # print("Best action: " + best_action.name)

        if best_action:
            result = best_action.perform(self)
            self.actions += best_action.action_cost
            self.action_result_counts[best_action][result] += 1
            # print(best_action.name)
            # print(self.hand)
            # print(self.items)

        if best_card is not None:
            self.card_play_counts[best_card] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)            

        self.hand = [card for card in self.hand if card.can_draw(self)]

    def run(self):
        while self.status == "InProgress":
            self.step()


    # Econ strat, TODO do another one for speed
    def best_action_by_simple_ranking(self):

        progress = self.get(Item._StacksProgress)
        keys = self.get(Item.LibraryKey)
        routes = self.get(Item.RouteTracedThroughTheLibrary)
        frags = self.get(Item.FragmentaryOntology)
        noises = self.get(Item.NoisesInTheLibrary)
        octavo_available = self.get(Item.AnathemaUnchained) == 0 and self.get(Item.InSearchOfLostTime) == 1

        key_cap = 1000
        route_floor = 10

        list = [
            Storylet_ReturnToRoof,
            Storylet_FindYourWayBack,
            ChainedOctavo1_Unchain,
        ]

        # key sources
        if keys < key_cap:
            list.extend([LibrariansOffice1_PickDrawers])

            if noises < 30:
                list.append(GaolerLibrarian2_LiftKey)

        list.extend([
            # Routes + Econ
            MapRoom4_PaintRoutes,
            MapRoom1_LibraryMaps,
            
            # Advance
            ReadingRoom_OpenTheBook,
            ApocryphaFound_Claim,
        ])

        if progress >= 40:
            list.extend([
                Deck_RefillHand
            ])

        # TODO check w/ use broad_pass_rate()
        # min for 100%
        if frags >= 9:
            list.extend([
                Atrium2_CourseCorrect
            ])

        # Routes + more TPs, harder check
        if routes < 5:
            list.append(DeadEnd2_VantagePoint)

        # 5 is min for 100%
        if progress < 35 and routes >= 5:
            list.append(TeaRoom2_ConsultMaps)

        # 15 progress
        if progress < 30 and keys >= 2:
            list.extend([
                LockedGate1_UseKey,
                LibrariansOffice3_UnlockCart,
            ])

        if progress < 30:
            list.extend([
                GodsEyeView2_FocusPath
            ])

        # Routes + more TPs, harder check
        if routes < route_floor:
            list.append(DeadEnd2_VantagePoint)

        list.append(Deck_RefillHand)

        # TODO experiment with this placement
        if progress < 35 and routes >= route_floor:
            list.append(StoneGallery3_FollowBorehole)

        if keys < key_cap and noises == 0:
            list.extend([
                BlackGallery1_Woesel,
                DeadEnd1_Woesel
            ])

        list.append(DeadEnd1_RopeDescend)
        list.append(Labyrinth1_RethinkMovements)

        list.append(GrandStaircase1_InformedDecision)

        list.extend([        
            # 5 progress free*
            GlimpseWindow2_MoveQuickly,
            FloweringGallery1_KeepGoing,

            GreyCardinal1_FurryLunch,
            BlackGallery2_NavigateAlternateSenses,

            BlackGallery1_LightLantern,
            StoneGallery1_SilentGallery,
            
            GaolerLibrarian3_Intervention,
            LibrariansOffice2_OppositeDoor,
            TerribleShushing2_HurryAlong,
            
            
            PoisonGallery1_FurnitureSteppingStones,
            # PoisonGalleryAction1,

            # fallback if few routes but bad hand
            # GrandStaircase1_InformedDecision,

            # 5 progress for 1 fragment
            Labyrinth2_RejectShape,
            Index3_SituateGreaterWhole,

            # Gain routes only
            DiscardedLadder1_Climb,
            Compass1_Camera,
            Index1_SearchReferenceCard,

            # 5 progress for 1 route
            Atrium1_Continue,

            Atrium2_CourseCorrect,

            Snuffbox1_ComputeFigure,
            ChainedOctavo2_ExamineSection,
            GrandStaircase2_UpDown,
            TeaRoom3_MakeSense
        ])

        # Find the best action from the ranked list that is in the hand
        for ranked_action in list:
            for storylet in self.storylets:
                for action in storylet.actions:
                    if isinstance(action, ranked_action) and action.can_perform(self):
                        return (storylet, action)
            for card in self.hand:
                for card_action in card.actions:
                    if isinstance(card_action, ranked_action) and card_action.can_perform(self):
                        return (card, card_action)

        # # If no card matches, check the refill action
        # if self.refill_action.can_perform(self):
        #     return (None, self.refill_action)
        
        # for ranked_action in low_prio:
        #     for card in self.hand:
        #         for card_action in card.actions:
        #             if isinstance(card_action, ranked_action) and card_action.can_perform(self):
        #                 return (card, card_action)


        # If no action can be performed, return None
        return (None, None)                        

class StacksStorylets(OpportunityCard):
    def __init__(self):
        super().__init__("Stacks Storylets")
        self.actions = [
            Deck_RefillHand(),
            Storylet_ToggleCartographer(),
            # EnableCartographer(),
            # DisableCartographer(),
            Storylet_FindYourWayBack(),
            Storylet_ReturnToRoof()
        ]

class Deck_RefillHand(Action):
    def __init__(self):
        super().__init__("(REFILL HAND)")
        self.action_cost = 0

    def can_perform(self, state: LibraryState):
        return len(state.hand) < state.max_hand_size
    
    def perform(self, state: GameState):
        # print("Refill hand called")
        while len(state.hand) < state.max_hand_size:
            state.draw_card()
        return ActionResult.Pass

    def ev(self, state: GameState):
        # TODO magic number
        return 5

class Storylet_ToggleCartographer(Action):
    def __init__(self):
        super().__init__("(TOGGLE CARTOGRAPHER)")

    def can_perform(self, state: LibraryState):
        return state.allow_cartographer_toggle \
            and state.get(Item.InSearchOfLostTime) == 1 \
            and state.get(Item.ApocryphaSought) != 204
    
    def pass_items(self, state):
        return {
            Item._StacksProgress: 5
        }

# class EnableCartographer(Action):
#     def __init__(self):
#         super().__init__("(Enable Cartographer)")
#         self.action_cost = 0

#     def can_perform(self, state: StacksState):
#         return not state.cartographer_enabled \
#             and state.allow_cartographer_toggle \
#             and state.get(Item.InSearchOfLostTime) == 1 \
#             and state.get(Item.ApocryphaSought) != 204
    
#     def pass_items(self, state):
#         return {
#             Item._StacksProgress: 5
#         }
    
#     def perform_pass(self, state: StacksState):
#         result = super().perform_pass(state)
#         state.cartographer_enabled = True
#         return result

    
# class DisableCartographer(Action):
#     def __init__(self):
#         super().__init__("(Disable Cartographer)")
#         self.action_cost = 1

#     def can_perform(self, state: StacksState):
#         return state.cartographer_enabled \
#             and state.allow_cartographer_toggle \
#             and state.get(Item.InSearchOfLostTime) == 1
    
#     def perform_pass(self, state: StacksState):
#         result = super().perform_pass(state)
#         state.cartographer_enabled = False
#         return result

# TODO rare failure/success with keys "Overdue"
# not set up to have alt rates calculated at runtime
class Storylet_FindYourWayBack(Action):
    def __init__(self):
        super().__init__("Find your way back to the entrance")
        self.alt_pass_rate = 0.0
        self.alt_fail_rate = 0.0

    def can_perform(self, state: LibraryState):
        return state.get(Item.UnwoundThread) > 0 #and not state.get(Item._OverdueStorylet)
    
    def pass_rate(self, state: LibraryState):
        # TODO
        return self.broad_pass_rate(250, state.outfit.shadowy_inerrant15)

    def pass_items(self, state):
        return {
            Item.UnwoundThread: -32,
        }
    
    def alt_pass_items(self, state):
        return {
            Item.UnwoundThread: -12,
            Item._OverdueStorylet: 1
        }
    
    def fail_items(self, state):
        return {
            Item.UnwoundThread: -12
        }
    
    def alt_fail_items(self, state):
        return {
            Item.UnwoundThread: -12,
            Item._OverdueStorylet: 1
        }

class Storylet_ReturnToRoof(Action):
    def __init__(self):
        super().__init__("Return to (Entry Point)")

    def can_perform(self, state):
        return state.get(Item.UnwoundThread) <= 0 and state.get(Item.InSearchOfLostTime) == 3
    
    def pass_items(self, state):
        return {
            Item.AnathemaUnchained: -1 if state.get(Item.AnathemaUnchained) > 0 else 0
        }
    
    def perform_pass(self, state: LibraryState):
        result = super().perform_pass(state)
        state.status = "Complete"
        return result
    
################################################################
#                     Apocrypha Found
################################################################

class ApocryphaFound(OpportunityCard):
    def __init__(self):
        super().__init__("Apocrypha Found", 10_000.0)
        self.actions = [ApocryphaFound_Claim()]

    def can_draw(self, state: LibraryState):
        return state.get(Item._StacksProgress) >= 40 and state.get(Item.InSearchOfLostTime) == 1

class ApocryphaFound_Claim(Action):
    def __init__(self):
        super().__init__("Claim the book")

    def pass_items(self, state):
        return {
            Item.InSearchOfLostTime: 1,
            Item._StacksProgress: -state.get(Item._StacksProgress),
            Item.HourInTheLibrary: 1 if state.get(Item.HourInTheLibrary) < 5 else -4
        }        

    
################################################################
#                     Reading Room
################################################################

class ReadingRoom(OpportunityCard):
    def __init__(self):
        super().__init__("The Reading Room", 10_000.0)
        self.actions = [ReadingRoom_OpenTheBook()]

    def can_draw(self, state: LibraryState):
        return state.get(Item._StacksProgress) >= 40 and state.get(Item.InSearchOfLostTime) == 2
    
class ReadingRoom_OpenTheBook(Action):
    def __init__(self):
        super().__init__("Open the book")
        self.action_cost = 2

    def pass_items(self, state):
        prize = None
        book = state.get(Item.ApocryphaSought)
        if book == ApocryphaSoughtBook.IndexOfBannedWorks.value:
            prize = Item._BannedWorksPrize
        elif book == ApocryphaSoughtBook.AnnalOfDeadStars.value:
            prize = Item._DeadStarsPrize
        elif book == ApocryphaSoughtBook.LePrecipiceDeLaTombee.value:
            prize = Item._PrecipicePrize
        elif book == ApocryphaSoughtBook.CodexOfUnrealPlaces.value:
            prize = Item._UnrealPlacesPrize
        elif book == ApocryphaSoughtBook.BookOfProperSpeech.value:
            prize = Item._ProperSpeechPrize
        elif book == ApocryphaSoughtBook.ChainedOctavo.value:
            prize = Item.GlimpseOfAnathema

        return {
            prize: 1,
            Item.UnwoundThread: 32,
            Item.InSearchOfLostTime: 1
        }

################################################################
#                     Chained Octavo
################################################################

class ChainedOctavo(OpportunityCard):
    def __init__(self):
        super().__init__("A Chained Volume", weight=0.1)
        self.actions = [ChainedOctavo1_Unchain(), ChainedOctavo2_ExamineSection()]
        
    def can_draw(self, state: LibraryState):
        return state.get(Item.AnathemaUnchained) == 0 and state.get(Item.InSearchOfLostTime) == 1


class ChainedOctavo1_Unchain(Action):
    def __init__(self):
        super().__init__("Unchain it")

    def can_perform(self, state: LibraryState):
        return state.get(Item.LibraryKey) > 1 and state.get(Item.NoisesInTheLibrary) < 28

    def pass_items(self, state: LibraryState):
        return {
            Item.LibraryKey: -1,
            Item.NoisesInTheLibrary: random.randint(5,7),
            Item.AnathemaUnchained: 10,

            Item._StacksProgress: -state.get(Item._StacksProgress),
            Item.InSearchOfLostTime: 1,
            Item.HourInTheLibrary: 1 if state.get(Item.HourInTheLibrary) < 5 else -4
        }
    
    def perform_pass(self, state: LibraryState):
        result = super().perform_pass(state)
        state.items[Item.ApocryphaSought] = ApocryphaSoughtBook.ChainedOctavo.value
        return result    


class ChainedOctavo2_ExamineSection(Action):
    def __init__(self):
        super().__init__("Examine this section, then move on")

    def pass_rate(self, state: LibraryState):
        bonus = state.get(Item.FragmentaryOntology)
        return self.narrow_pass_rate(10, state.outfit.cthonosophy + bonus)

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5,
            Item.TantalisingPossibility: 10
        }

    def fail_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }


################################################################
#                     Atrium
################################################################

class Atrium(OpportunityCard):
    def __init__(self):
        super().__init__("An Atrium")
        self.actions = [Atrium1_Continue(), Atrium2_CourseCorrect()]

class Atrium1_Continue(Action):
    def __init__(self):
        super().__init__("Continue on the same heading")

    def can_perform(self, state: LibraryState):
        return state.get(Item.RouteTracedThroughTheLibrary) > 0

    def pass_rate(self, state: LibraryState):
        bonus = state.items[Item.RouteTracedThroughTheLibrary] * 15
        return self.broad_pass_rate(220, state.outfit.watchful_inerrant15 + bonus)

    def pass_items(self, state):
        return {
            Item.RouteTracedThroughTheLibrary: -1,
            Item._StacksProgress: 5
        }
    
    def fail_items(self, state):
        return {
            Item.NoisesInTheLibrary: 6
        }

class Atrium2_CourseCorrect(Action):
    def __init__(self):
        super().__init__("Course correct")

    def can_perform(self, state: LibraryState):
        return state.get(Item.InSearchOfLostTime) == 1 and state.get(Item.FragmentaryOntology) > 0

    def pass_rate(self, state: LibraryState):
        bonus = state.get(Item.FragmentaryOntology) * 15
        return self.broad_pass_rate(300, state.outfit.watchful + bonus)

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5,
            Item.RouteTracedThroughTheLibrary: 1.5, # TODO random?
            Item.FragmentaryOntology: -1
        }

    def fail_items(self, state):
        return {
            Item._StacksProgress: 1,
            Item.NoisesInTheLibrary: 1
        }


################################################################
#                     Dead End
################################################################

class DeadEnd(OpportunityCard):
    def __init__(self):
        super().__init__("A Dead End?")
        self.actions = [DeadEnd1_RopeDescend(),
                        DeadEnd2_VantagePoint(),
                        DeadEnd3_CartographerEyes(),
                        DeadEnd1_Woesel()]

class DeadEnd1_RopeDescend(Action):
    def __init__(self):
        super().__init__("Tie a rope to the railing and descend")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(148, state.outfit.shadowy_watchful)

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5,
        }

    def fail_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5,
            Item.Wounds: 1.7,
            Item.NoisesInTheLibrary: random.randint(1, 6)
        }

    def perform(self, state: LibraryState):
        result = super().perform(state)
        state.clear_hand()  # Clears hand after the action
        return result    


class DeadEnd2_VantagePoint(Action):
    def __init__(self):
        super().__init__("Take advantage of the vantage point")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(350, state.outfit.watchful_cthonosophy15)

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: 2,
            Item.TantalisingPossibility: 50
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: 1
        }


class DeadEnd3_CartographerEyes(Action):
    def __init__(self):
        super().__init__("See through the Cartographer's eyes")

    def can_perform(self, state: LibraryState):
        return state.cartographer_enabled

    def pass_items(self, state: LibraryState):
        return {
            Item.TempestuousTale: 10
        }
    
class DeadEnd1_Woesel(Action):
    def __init__(self):
        super().__init__("(WOESEL) Tie a rope to the railing and descend")

    def pass_rate(self, state: LibraryState):
        return 0.0

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5,
            # Item.HandCardsCleared: 1  # Represents clearing the hand
        }

    def fail_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5,
            Item.Wounds: 2,
            Item.NoisesInTheLibrary: random.randint(1, 6)  # Average handled elsewhere if needed
        }
    
    def perform(self, state: LibraryState):
        result = super().perform(state)
        state.clear_hand()  # Clears hand after the action
        return result        



################################################################
#                     Discarded Ladder
################################################################

class DiscardedLadder(OpportunityCard):
    def __init__(self):
        super().__init__("A Discarded Ladder")
        self.actions = [DiscardedLadder1_Climb()]

class DiscardedLadder1_Climb(Action):
    def __init__(self):
        super().__init__("Climb")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(200, state.outfit.watchful)

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: 1.5,  # TODO: Random value replacement
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.Wounds: 1,
            Item.NoisesInTheLibrary: 6
        }


################################################################
#                     Grand Staircase
################################################################

class GrandStaircase(OpportunityCard):
    def __init__(self):
        super().__init__("A Grand Staircase")
        self.actions = [GrandStaircase1_InformedDecision(), GrandStaircase2_UpDown()]

class GrandStaircase1_InformedDecision(Action):
    def __init__(self):
        super().__init__("Make an informed decision")

    def can_perform(self, state: LibraryState):
        return state.get(Item.RouteTracedThroughTheLibrary) > 0

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: -1,
            Item._StacksProgress: 5,
            # Item.HandCardsCleared: 1  # Represents clearing the hand
        }

class GrandStaircase2_UpDown(Action):
    def __init__(self):
        super().__init__("Go up/Go down")

    def can_perform(self, state: LibraryState):
        return state.get(Item.RouteTracedThroughTheLibrary) <= 0

    def pass_rate(self, state: LibraryState):
        return 0.5

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 1,
            Item.NoisesInTheLibrary: 1
        }

################################################################
#                     Locked Gate
################################################################

class LockedGate(OpportunityCard):
    def __init__(self):
        super().__init__("A Locked Gate", weight=0.8)
        self.actions = [LockedGate1_UseKey()]

class LockedGate1_UseKey(Action):
    def __init__(self):
        super().__init__("Use a key")

    def can_perform(self, state: LibraryState):
        return state.get(Item.LibraryKey) > 0

    def pass_items(self, state: LibraryState):
        return {
            Item.LibraryKey: -1,
            Item._StacksProgress: 15
        }

################################################################
#                     Map Room
################################################################

class MapRoom(OpportunityCard):
    def __init__(self):
        super().__init__("A Map Room")
        self.actions = [
            MapRoom1_LibraryMaps(),
            MapRoom2_NeathMaps(),
            MapRoom3_CartographerLead(),
            MapRoom4_PaintRoutes()
        ]

class MapRoom1_LibraryMaps(Action):
    def __init__(self):
        super().__init__("Look for maps of the library")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(220, state.outfit.watchful)

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: 1.5,  # TODO: Random [1, 2]
            Item.TantalisingPossibility: 50
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.Nightmares: 1,  # TODO: Cap at 5?
            Item.NoisesInTheLibrary: 1.5,  # TODO: Random [1, 2]
            Item._StacksProgress: 1
        }

class MapRoom2_NeathMaps(Action):
    def __init__(self):
        super().__init__("Look for maps of the Neath")
        self.rare_pass_rate = 0.33

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(250, state.outfit.watchful)

    def pass_items(self, state: LibraryState):
        # Rare success condition handled within the logic
        return {
            Item.PartialMap: 2 * (1 - self.rare_pass_rate),
            Item.PuzzlingMap: self.rare_pass_rate
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.Nightmares: 1,  # TODO: Cap at 5?
            Item._StacksProgress: 1,
            Item.NoisesInTheLibrary: 1
        }

class MapRoom3_CartographerLead(Action):
    def __init__(self):
        super().__init__("Get a lead from the Cartographer")

    def can_perform(self, state: LibraryState):
        return state.cartographer_enabled

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5,
            Item.NoisesInTheLibrary: 2
        }

class MapRoom4_PaintRoutes(Action):
    def __init__(self):
        super().__init__("Paint new routes upon maps of the library")

    def can_perform(self, state: LibraryState):
        # TODO: Require Palette Hallowmas item
        return True

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: 1.5,  # TODO: Random [1, 2]
            Item.TantalisingPossibility: 50
        }

################################################################
#                     Poison Gallery
################################################################

class PoisonGallery(OpportunityCard):
    def __init__(self):
        super().__init__("A Poison-Gallery")
        self.actions = [PoisonGallery1_FurnitureSteppingStones(), PoisonGallery2_PrepareAntidote()]

class PoisonGallery1_FurnitureSteppingStones(Action):
    def __init__(self):
        super().__init__("Use furniture as stepping stones")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(240, state.outfit.shadowy_neathproofed15)

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: 6,
            Item.Wounds: 3
        }

class PoisonGallery2_PrepareAntidote(Action):
    def __init__(self):
        super().__init__("Prepare an antidote")

    def pass_rate(self, state: LibraryState):
        return self.narrow_pass_rate(10, state.outfit.kataleptic_toxicology)

    def pass_items(self, state: LibraryState):
        return {
            Item.FlaskOfAbominableSalts: -1,
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: 1,
            Item.Wounds: 2,
            Item._StacksProgress: 1
        }

################################################################
#                     Stone Gallery
################################################################

class StoneGallery(OpportunityCard):
    def __init__(self):
        super().__init__("A Stone Gallery")
        self.actions = [StoneGallery1_SilentGallery(),
                        StoneGallery2_ExamineVolumes(),
                        StoneGallery3_FollowBorehole()]

class StoneGallery1_SilentGallery(Action):
    def __init__(self):
        super().__init__("Make your way through the silent gallery")

    def pass_rate(self, state: LibraryState):
        return 0.5  # Luck-based

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        # TODO: this caps at lvl 7, consider?
        return {
            Item.Nightmares: 2,
            Item._StacksProgress: 5
        }

class StoneGallery2_ExamineVolumes(Action):
    def __init__(self):
        super().__init__("Stop and examine the ancient volumes")

    def pass_rate(self, state: LibraryState):
        return self.narrow_pass_rate(7, state.outfit.cthonosophy)

    def pass_items(self, state: LibraryState):
        return {
            Item.FragmentaryOntology: 1.5,  # TODO: Random [1, 2]
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: random.randint(1,2),
            Item._StacksProgress: 1
        }

class StoneGallery3_FollowBorehole(Action):
    def __init__(self):
        super().__init__("Follow a borehole through the back of a bookcase")

    def can_perform(self, state: LibraryState):
        return state.get(Item.RouteTracedThroughTheLibrary) >= 2 and state.get(Item.HourInTheLibrary) in (3, 4)

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(300, state.outfit.dangerous_watchful)

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: -2,
            Item._StacksProgress: 10
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: -1,
            Item._StacksProgress: 5,
            Item.NoisesInTheLibrary: 6
        }


################################################################
#                     Index
################################################################

class Index(OpportunityCard):
    def __init__(self):
        super().__init__("An Index")
        self.actions = [Index1_SearchReferenceCard(),
                        Index2_UnderstandOrganization(),
                        Index3_SituateGreaterWhole()]

    def can_draw(self, state: LibraryState):
        return state.get(Item.InSearchOfLostTime) == 1


class Index1_SearchReferenceCard(Action):
    def __init__(self):
        super().__init__("Search for a reference card")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(200, state.outfit.watchful_inerrant15)

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: 2,  # TODO: Random [1, 2, 3]
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: 1,
            Item.NoisesInTheLibrary: 2,
            Item._StacksProgress: 1,
        }

class Index2_UnderstandOrganization(Action):
    def __init__(self):
        super().__init__("Try to understand the organization of the library")

    def pass_rate(self, state: LibraryState):
        return self.narrow_pass_rate(7, state.outfit.cthonosophy)

    def pass_items(self, state: LibraryState):
        return {
            Item.FragmentaryOntology: 2,  # TODO: Random [1, 2, 3]
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.FragmentaryOntology: 1,
            Item.NoisesInTheLibrary: 1.5,  # TODO: Random [1, 2]
            Item._StacksProgress: 1,
        }

class Index3_SituateGreaterWhole(Action):
    def __init__(self):
        super().__init__("Situate yourself within the greater whole")

    def can_perform(self, state: LibraryState):
        return state.get(Item.FragmentaryOntology) > 0

    def pass_items(self, state: LibraryState):
        return {
            Item.FragmentaryOntology: -1,
            Item._StacksProgress: 5
        }


################################################################
#                     Librarian's Office
################################################################

class LibrariansOffice(OpportunityCard):
    def __init__(self):
        super().__init__("A Librarian's Office", weight=0.8)
        self.actions = [LibrariansOffice1_PickDrawers(),
                        LibrariansOffice2_OppositeDoor(),
                        LibrariansOffice3_UnlockCart()]

    def can_draw(self, state: LibraryState):
        return state.get(Item.InSearchOfLostTime) == 2

class LibrariansOffice1_PickDrawers(Action):
    def __init__(self):
        super().__init__("Pick through the drawers")

    def pass_rate(self, state: LibraryState):
        return 0.9

    def pass_items(self, state: LibraryState):
        items = {
            Item.TantalisingPossibility: 40,
        }

        drawer = random.choice([1,2,3])
        if drawer == 1:
            items[Item.LibraryKey] = 1
        elif drawer == 2:
            items[Item.RouteTracedThroughTheLibrary] = 1
        elif drawer == 3:
            items[Item.FragmentaryOntology] = 1

        return items

    def fail_items(self, state: LibraryState):
        return {
            Item.FinBonesCollected: 6,  # TODO: Random [2, 10]
            Item.DeepZeeCatch: 6  # TODO: Random [3, 10]
        }


class LibrariansOffice2_OppositeDoor(Action):
    def __init__(self):
        super().__init__("Take the opposite door")

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }


class LibrariansOffice3_UnlockCart(Action):
    def __init__(self):
        super().__init__("Unlock the cart")

    def can_perform(self, state: LibraryState):
        return state.get(Item.LibraryKey) > 0

    def pass_items(self, state: LibraryState):
        return {
            Item.LibraryKey: -1,
            Item._StacksProgress: 15
        }


################################################################
#                     Flowering Gallery
################################################################

class FloweringGallery(OpportunityCard):
    def __init__(self):
        super().__init__("A Flowering Gallery")
        self.actions = [FloweringGallery1_KeepGoing(),
                        FloweringGallery2_EatFruitKnowledge()]

    def can_draw(self, state: LibraryState):
        return state.get(Item.HourInTheLibrary) in [1, 2]

class FloweringGallery1_KeepGoing(Action):
    def __init__(self):
        super().__init__("Keep going")

    def pass_rate(self, state: LibraryState):
        return self.narrow_pass_rate(0, state.outfit.neathproofed_inerrant)

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.Nightmares: 2,  # TODO: Confirm cap via wiki
            Item.NoisesInTheLibrary: 6
        }

class FloweringGallery2_EatFruitKnowledge(Action):
    def __init__(self):
        super().__init__("Eat the fruit of knowledge")

    def pass_rate(self, state: LibraryState):
        return self.narrow_pass_rate(12, state.outfit.kataleptic_toxicology)

    def pass_items(self, state: LibraryState):
        return {
            Item.FragmentaryOntology: 2,
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.Wounds: 2,
            Item.NoisesInTheLibrary: 1,
            Item._StacksProgress: 1
        }

################################################################
#                     Black Gallery
################################################################

class BlackGallery(OpportunityCard):
    def __init__(self):
        super().__init__("A Black Gallery")
        self.actions = [BlackGallery1_LightLantern(),
                        BlackGallery1_Woesel(),
                        BlackGallery2_NavigateAlternateSenses()]

    def can_draw(self, state: LibraryState):
        return state.get(Item.HourInTheLibrary) in [3, 4, 5]


class BlackGallery1_LightLantern(Action):
    def __init__(self):
        super().__init__("Light a lantern")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(240, state.outfit.shadowy_insubstantial15)

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5,
            Item.NoisesInTheLibrary: 2
        }

class BlackGallery1_Woesel(Action):
    def __init__(self):
        super().__init__("Light a lantern")

    def pass_rate(self, state: LibraryState):
        return 0

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5,
            Item.NoisesInTheLibrary: 2
        }


class BlackGallery2_NavigateAlternateSenses(Action):
    def __init__(self):
        super().__init__("Navigate by alternate senses")

    def pass_rate(self, state: LibraryState):
        return 1.0

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 1,
            Item.NoisesInTheLibrary: 2
        }


################################################################
#                     Gaoler-Librarian
################################################################

class GaolerLibrarian(OpportunityCard):
    def __init__(self):
        super().__init__("A Gaoler-Librarian")
        self.actions = [GaolerLibrarian1_Distract(),
                        GaolerLibrarian2_LiftKey(),
                        GaolerLibrarian2_SecondChance(),
                        GaolerLibrarian3_Intervention()]

    def can_draw(self, state: LibraryState):
        return state.get(Item.NoisesInTheLibrary) > 0


class GaolerLibrarian1_Distract(Action):
    def __init__(self):
        super().__init__("Distract the Gaoler")

    def can_perform(self, state: LibraryState):
        return state.get(Item.NoisesInTheLibrary) > 0

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(200, state.outfit.shadowy)

    def fail_items(self, state: LibraryState):
        return {
            Item.Wounds: 4,  # TODO: Confirm from wiki
            Item.NoisesInTheLibrary: 1,
            Item._StacksProgress: 1
        }


class GaolerLibrarian2_LiftKey(Action):
    def __init__(self):
        super().__init__("Try to lift one of its keys")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(250, state.outfit.shadowy_insubstantial15)

    def pass_items(self, state: LibraryState):
        return {
            Item.LibraryKey: 1,
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: 6
        }


class GaolerLibrarian2_SecondChance(Action):
    def __init__(self):
        super().__init__("(SECOND CHANCE) Try to lift one of its keys")

    def pass_rate(self, state: LibraryState):
        rate = self.broad_pass_rate(250, state.outfit.shadowy_insubstantial15)
        return 1.0 - (1.0 - rate) ** 2

    def pass_items(self, state: LibraryState):
        return {
            Item.LibraryKey: 1,
            Item.HastilyScrawledWarningNote: -1,
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.HastilyScrawledWarningNote: -1,
            Item.NoisesInTheLibrary: 6
        }


class GaolerLibrarian3_Intervention(Action):
    def __init__(self):
        super().__init__("An intervention from the Grey Cardinal")

    def can_perform(self, state: LibraryState):
        return state.get(Item.DispositionOfTheCardinal) > 0

    def pass_items(self, state: LibraryState):
        return {
            Item.DispositionOfTheCardinal: -1,
            Item._StacksProgress: 5
        }


################################################################
#                     Terrible Shushing
################################################################

class TerribleShushing(OpportunityCard):
    def __init__(self):
        super().__init__("A Terrible Shushing")
        self.actions = [TerribleShushing1_HidingPlace(),
                        TerribleShushing2_HurryAlong(),
                        TerribleShushing3_QuietCartographer()]

    def can_draw(self, state: LibraryState):
        return state.get(Item.NoisesInTheLibrary) >= 10


class TerribleShushing1_HidingPlace(Action):
    def __init__(self):
        super().__init__("Find a hiding place")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(220, state.outfit.shadowy)

    def pass_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: -3
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: -1
        }


class TerribleShushing2_HurryAlong(Action):
    def __init__(self):
        super().__init__("Hurry along")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(295, state.outfit.shadowy)

    def pass_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: 2,
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: 4,
            Item._StacksProgress: 5
        }


class TerribleShushing3_QuietCartographer(Action):
    def __init__(self):
        super().__init__("Quiet the Cartographer")

    def can_perform(self, state: LibraryState):
        return state.cartographer_enabled

    def pass_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: -6  # TODO: Random range [3, 10]
        }

################################################################
#                     God's Eye View
################################################################

class GodsEyeView(OpportunityCard):
    def __init__(self):
        super().__init__("A God's Eye View")
        self.actions = [GodsEyeView1_HoldItAll(),
                        GodsEyeView2_FocusPath()]

    def can_draw(self, state: LibraryState):
        return state.get(Item.FragmentaryOntology) >= 5


class GodsEyeView1_HoldItAll(Action):
    def __init__(self):
        super().__init__("Try to hold it all in your mind at once")

    def pass_rate(self, state: LibraryState):
        return 0.4

    def pass_items(self, state: LibraryState):
        return {
            Item.TantalisingPossibility: 60,
            Item.FragmentaryOntology: -6
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.TantalisingPossibility: 40,
            Item.Nightmares: 3,  # TODO: Random [2, 4]
            Item.NoisesInTheLibrary: 1.5,  # TODO: Random [1, 2]
            Item._StacksProgress: 1
        }


class GodsEyeView2_FocusPath(Action):
    def __init__(self):
        super().__init__("Focus on the path ahead")

    def pass_items(self, state: LibraryState):
        return {
            Item.FragmentaryOntology: -5,
            Item._StacksProgress: 15
        }


################################################################
#                 The Shape of the Labyrinth
################################################################

class ShapeOfTheLabyrinth(OpportunityCard):
    def __init__(self):
        super().__init__("The Shape of the Labyrinth")
        self.actions = [Labyrinth1_RethinkMovements(),
                        Labyrinth2_RejectShape()]

    def can_draw(self, state: LibraryState):
        return state.get(Item.RouteTracedThroughTheLibrary) >= 6 and state.get(Item.InSearchOfLostTime) == 2


class Labyrinth1_RethinkMovements(Action):
    def __init__(self):
        super().__init__("Rethink your movements")

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: -3.5,  # TODO: Random [2, 5]
            Item._StacksProgress: 10,
            # Item.HandCardsCleared: 1
        }


class Labyrinth2_RejectShape(Action):
    def __init__(self):
        super().__init__("Reject the significance of shape")

    def can_perform(self, state: LibraryState):
        return state.get(Item.FragmentaryOntology) > 0

    def pass_rate(self, state: LibraryState):
        return self.narrow_pass_rate(5, state.outfit.cthonosophy)

    def pass_items(self, state: LibraryState):
        return {
            Item.FragmentaryOntology: -1,
            Item._StacksProgress: 5
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: 1,
            Item._StacksProgress: 1
        }


################################################################
#                     The Grey Cardinal
################################################################

class GreyCardinal(OpportunityCard):
    def __init__(self):
        super().__init__("The Grey Cardinal")
        self.actions = [GreyCardinal1_FurryLunch(),
                        GreyCardinal2_TinFishy(),
                        GreyCardinal3_Conversation()]


class GreyCardinal1_FurryLunch(Action):
    def __init__(self):
        super().__init__("Offer the cardinal a furry lunch")

    def pass_items(self, state: LibraryState):
        return {
            Item.DispositionOfTheCardinal: 1,
            Item.RatOnAString: -1,
            Item._StacksProgress: 5
        }


class GreyCardinal2_TinFishy(Action):
    def __init__(self):
        super().__init__("Offer the cardinal a tin of something fishy")

    def pass_items(self, state: LibraryState):
        return {
            Item.DispositionOfTheCardinal: 1.5,  # TODO: Random [1, 2]
            Item.DeepZeeCatch: -1,
            Item._StacksProgress: 5
        }


class GreyCardinal3_Conversation(Action):
    def __init__(self):
        super().__init__("Engage the Cardinal in conversation")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(250, state.outfit.persuasive_bizarre10)

    def pass_items(self, state: LibraryState):
        return {
            Item.TantalisingPossibility: 50,
            Item.DispositionOfTheCardinal: 1
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.TantalisingPossibility: 40
        }
    
################################################################
#                     Glimpse Through a Window
################################################################

class GlimpseThroughAWindow(OpportunityCard):
    def __init__(self):
        super().__init__("A Glimpse through a Window", weight=0.1)
        self.actions = [GlimpseWindow1_StopAndLook(), GlimpseWindow2_MoveQuickly()]


class GlimpseWindow1_StopAndLook(Action):
    def __init__(self):
        super().__init__("Stop and look through")

    def can_perform(self, state: LibraryState):
        return state.get(Item.HourInTheLibrary) != 4

    def pass_items(self, state: LibraryState):
        return {
            Item.TantalisingPossibility: 50
        }


class GlimpseWindow2_MoveQuickly(Action):
    def __init__(self):
        super().__init__("Move on quickly")

    def pass_items(self, state: LibraryState):
        return {
            Item._StacksProgress: 5
        }

################################################################
#                     Tea Room
################################################################

class TeaRoom(OpportunityCard):
    def __init__(self):
        super().__init__("A Tea Room?", weight=0.8)
        self.actions = [TeaRoom1_Regroup(), TeaRoom2_ConsultMaps(), TeaRoom3_MakeSense()]


class TeaRoom1_Regroup(Action):
    def __init__(self):
        super().__init__("Take a moment to regroup")

    def pass_items(self, state: LibraryState):
        # TODO: Define success outcomes
        return {}


class TeaRoom2_ConsultMaps(Action):
    def __init__(self):
        super().__init__("Consult your maps of the library")

    def pass_rate(self, state: LibraryState):
        return self.narrow_pass_rate(0, state.get(Item.RouteTracedThroughTheLibrary))

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: -1,
            Item._StacksProgress: 10
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: -1,
            Item._StacksProgress: 5
        }


class TeaRoom3_MakeSense(Action):
    def __init__(self):
        super().__init__("Try to make sense of what you've seen")

    def can_perform(self, state: LibraryState):
        return state.get(Item.FragmentaryOntology) > 0

    def pass_rate(self, state: LibraryState):
        return self.narrow_pass_rate(2, state.get(Item.FragmentaryOntology))

    def pass_items(self, state: LibraryState):
        return {
            Item.FragmentaryOntology: -1,
            Item.TantalisingPossibility: 50
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.FragmentaryOntology: 1,
        }

################################################################
#                     Cartographer's Snuffbox
################################################################

class CartographerSnuffbox(OpportunityCard):
    def __init__(self):
        super().__init__("Snuffbox.png")
        self.actions = [Snuffbox1_ComputeFigure(), Snuffbox2_Implication()]

    def can_draw(self, state: LibraryState):
        return state.cartographer_enabled and state.get(Item.RouteTracedThroughTheLibrary) > 0


class Snuffbox1_ComputeFigure(Action):
    def __init__(self):
        super().__init__("Computernofigure.png")

    def can_perform(self, state: LibraryState):
        return state.get(Item.RouteTracedThroughTheLibrary) > 0

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: -1,
            Item._StacksProgress: 5
        }


class Snuffbox2_Implication(Action):
    def __init__(self):
        super().__init__("Implication.png")

    def can_perform(self, state: LibraryState):
        return state.get(Item.RouteTracedThroughTheLibrary) >= 3

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: -3,
            Item.FragmentaryOntology: 5,
        }

################################################################
#                     Cartographer's Compass
################################################################

class CartographerCompass(OpportunityCard):
    def __init__(self):
        super().__init__("Compass.png")
        self.actions = [Compass1_Camera(), Compass2_Chart()]

    def can_draw(self, state: LibraryState):
        return state.cartographer_enabled


class Compass1_Camera(Action):
    def __init__(self):
        super().__init__("Camera2.png")

    def pass_rate(self, state: LibraryState):
        return self.broad_pass_rate(220, state.outfit.watchful_inerrant15)

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: 2,  # TODO: Random [1, 3]
        }

    def fail_items(self, state: LibraryState):
        return {
            Item.NoisesInTheLibrary: 2,
            Item._StacksProgress: 1
        }

class Compass2_Chart(Action):
    def __init__(self):
        super().__init__("Chart2.png")

    def can_perform(self, state: LibraryState):
        return state.get(Item.RouteTracedThroughTheLibrary) >= 3

    def pass_items(self, state: LibraryState):
        return {
            Item.RouteTracedThroughTheLibrary: -3,
            Item._StacksProgress: random.choose(5, 10, 15)
        }

class StacksSimRunner(SimulationRunner):
    def __init__(self, runs: int, initial_values: dict):
        super().__init__(runs, initial_values)

        self.storylets = [
            StacksStorylets()
        ]

        self.cards = [
            ApocryphaFound(),
            ChainedOctavo(),
            ReadingRoom(),

            Atrium(),
            DeadEnd(),
            DiscardedLadder(),
            GrandStaircase(),
            LockedGate(),
            MapRoom(),
            PoisonGallery(),
            StoneGallery(),
            Index(),
            LibrariansOffice(),
            FloweringGallery(),
            BlackGallery(),
            GaolerLibrarian(),
            TerribleShushing(),
            GodsEyeView(),
            ShapeOfTheLabyrinth(),
            GreyCardinal(),
            GlimpseThroughAWindow(),
            TeaRoom(),

            CartographerSnuffbox(),
            CartographerCompass(),
        ]

    def create_state(self):
        state = LibraryState()
        state.items[Item.InSearchOfLostTime] = 1
        state.actions = 1
        # state.outfit
        return state
    
    # TODO rewrite this so it's not a total override
    def run_simulation(self):
        for i in range(self.runs):
            state = self.create_state()

            for key, val in self.initial_values.items():
                state.items[key] = val

            state.outfit = self.outfit
            state.storylets.extend(self.storylets)
            state.deck.extend(self.cards)

            state.run()  # Run the individual simulation

            # Track success and failure of each run
            self.outcome_counts[state.status] += 1

            # Accumulate total actions across all runs
            self.total_draws += state.cards_drawn
            self.total_actions += state.actions

            # Accumulate item changes for each run
            for item, count in state.items.items():
                self.total_item_changes[item] += count

            # Accumulate action play/success/failure counts
            for action, result_counts in state.action_result_counts.items():
                for result, count in result_counts.items():
                    self.total_action_result_counts[action][result] += count
                    self.total_action_play_counts[action] += count

            # Accumulate card draw/play counts
            for card, count in state.card_draw_counts.items():
                self.total_card_draw_counts[card] += count

            for card, count in state.card_play_counts.items():
                self.total_card_play_counts[card] += count
            
            self.update_progress((i + 1) / self.runs)  # Update the progress bar

            # HACK this is the only change from base method
            self.initial_values[Item.LibraryKey] = state.get(Item.LibraryKey)
            self.initial_values[Item.RouteTracedThroughTheLibrary] = state.get(Item.RouteTracedThroughTheLibrary)
            self.initial_values[Item.FragmentaryOntology] = state.get(Item.FragmentaryOntology)

        self.display_results()    

simulation = StacksSimRunner(
    runs = 500,
    initial_values={
        Item.ApocryphaSought: ApocryphaSoughtBook.CodexOfUnrealPlaces.value,

        Item.RouteTracedThroughTheLibrary: 20,
        Item.FragmentaryOntology: 5,
        Item.LibraryKey: 5
    })

# HACK IDK why I did it this way but whatever, works for now
# These are my PC's stats, or close enough

my_outfit = PlayerOutfit()

# parenthetical is the cap for 100%, not the DC
# artium2 (500, frags add 15 ea)
my_outfit.watchful = 343

# atrium1 (367), index1 (334)
my_outfit.watchful_inerrant15 = 313 + 6 * 15

# deadend1 (247)
my_outfit.shadowy_watchful = 241 + 343

# stonegallery3 (500)
my_outfit.watchful_plus_dangerous = 332 + 261

# deadend2 (584)
my_outfit.watchful_cthonosophy15 = 323 + 9 * 15

# gaoler1 (334), shushing1, shushing2, overdue (334 + 10 * noise lvl)
my_outfit.shadowy = 333

# posiongallery1 (400)
my_outfit.shadowy_neathproofed15 = 281 + 9 * 15

# unwound thread (417)
my_outfit.shadowy_inerrant15 = 292 + 7 * 15

# blackGallery1 (400), gaoler2 (417)
my_outfit.shadowy_insubstantial15 = 314 + 4 * 15

# stonegallery2, shape2, octavo2
my_outfit.cthonosophy = 10

# greycardinal3 (417)
my_outfit.persuasive_bizarre10 = 260 + 28 * 10

# blackgallery2 (400)
my_outfit.watchful_monstrous10_inerrant15 = 295 + 13 * 10 + 6 * 15

# poisongallery2 (15), floweringgallery2 (17)
my_outfit.kataleptic_toxicology = 17

# flowering1 (5)
my_outfit.neathproofed_inerrant = 8 + 3

simulation.outfit = my_outfit

simulation.run_simulation()