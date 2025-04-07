"""
Stacks Simulation v4

This module simulates exploration of the Stacks in Fallen London, focusing on
optimizing resource gathering and navigation through the library. It supports
both economic and speed-based optimization strategies.

Key Features:
- Multi-stage exploration simulation
- Card-based action system
- Resource management (keys, routes, fragments)
- Multiple optimization strategies
- Statistical analysis of outcomes
"""

import random
import sys
import math
from collections import defaultdict
from enum import Enum, auto
from typing import List, Tuple, Optional, Dict, Any
import helper.utils as utils
from enums import *
from simulations.item_conversions import conversion_rate
from simulations.models import *
from simulations.models import GameState

class ApocryphaSoughtBook(Enum):
    """Enumeration of books that can be sought in the Stacks."""
    IndexOfBannedWorks = 201
    AnnalOfDeadStars = 202
    LePrecipiceDeLaTombee = 203
    CodexOfUnrealPlaces = 204
    BookOfProperSpeech = 205
    ChainedOctavo = 1001

class LibraryState(GameState):
    """
    Manages the state of a library exploration run.
    
    Attributes:
        status (str): Current state of the simulation ("InProgress", "Success", "Failure")
        items (dict): Current inventory of items
        cartographer_enabled (bool): Whether cartographer tools are available
        storylets (list): Available storylets/actions
        hand (list): Current hand of cards
        deck (list): Available cards in deck
    """
    
    def __init__(self):
        super().__init__(max_hand_size=4)
        self.status = "InProgress"
        self.items = {
            Item._StacksProgress: 0,
            Item.RouteTracedThroughTheLibrary: 0,
            Item.FragmentaryOntology: 0,
            Item.LibraryKey: 0,
        }
        self.cartographer_enabled = False
        self.storylets = []
        self.hand = []
        self.deck = []

    def step(self) -> None:
        """Execute one step of the simulation."""
        best_card, best_action = self.best_action_by_simple_ranking_econ()

        if best_action is None:
            self._log_hand_state()
            return

        if best_action:
            result = best_action.perform(self)
            self.actions += best_action.action_cost
            self.action_result_counts[best_action][result] += 1

        if best_card is not None:
            self.card_play_counts[best_card] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)            

        self.hand = [card for card in self.hand if card.can_draw(self)]

        if self.get(Item.NoisesInTheLibrary) >= 36:
            print("Noises Failure!")
            self.status = "Failure"

    def _log_hand_state(self) -> None:
        """Log the current state of cards in hand."""
        print("Cards in hand: " + str(len(self.hand)))
        for card in self.hand:
            print(card.name)

    def run(self) -> None:
        """Run the simulation until completion or failure."""
        while self.status == "InProgress":
            self.step()

    def holding_any(self, card_classes: List[Any]) -> bool:
        """Check if any card of the specified classes is in hand."""
        return any(card.__class__ in card_classes for card in self.hand)

    def best_action_by_simple_ranking_econ(self) -> Tuple[Optional[Any], Optional[Any]]:
        """
        Determine the best action based on economic optimization.
        
        Returns:
            Tuple of (best_card, best_action) or (None, None) if no action available
        """
        # Get current state
        progress = self.get(Item._StacksProgress)
        keys = self.get(Item.LibraryKey)
        routes = self.get(Item.RouteTracedThroughTheLibrary)
        frags = self.get(Item.FragmentaryOntology)
        noises = self.get(Item.NoisesInTheLibrary)
        stage = self.get(Item.InSearchOfLostTime)
        octavo_available = self.get(Item.AnathemaUnchained) == 0 and stage == 1

        # Calculate remaining progress needed
        total_prog_left = 40 - progress + 40 if stage == 1 else 0

        # Define high-value cards based on current state
        high_value_cards = self._get_high_value_cards(total_prog_left, keys)
        high_value_card_in_hand = self.holding_any(high_value_cards)

        # Define action priorities
        action_list = self._build_action_list(
            total_prog_left, keys, noises, progress, 
            high_value_card_in_hand, octavo_available
        )

        # Find best action
        return self._find_best_action(action_list)

    def _get_high_value_cards(self, total_prog_left: int, keys: int) -> List[Any]:
        """Get list of high-value cards based on current state."""
        high_value_cards = [
            ChainedOctavo,
            GaolerLibrarian,
            MapRoom,
            LibrariansOffice,
        ]

        if keys > 1 and total_prog_left > 10:
            high_value_cards.append(LockedGate)

        if total_prog_left > 5:
            high_value_cards.append(TeaRoom)

        if total_prog_left <= 10:
            high_value_cards.append(DeadEnd)

        return high_value_cards

    def _build_action_list(
        self, total_prog_left: int, keys: int, noises: int,
        progress: int, high_value_card_in_hand: bool,
        octavo_available: bool
    ) -> List[Any]:
        """Build list of available actions in priority order."""
        action_list = [
            Storylet_EnterStacks,
            Storylet_ReturnToRoof,
            Storylet_FindYourWayBack,
            ChainedOctavo1_Unchain,
        ]

        # Add conditional actions
        if total_prog_left <= 10:
            action_list.append(DeadEnd2_VantagePoint)

        if self.holding_any([GrandStaircase]) and noises > 0:
            action_list.append(DeadEnd2_VantagePoint)

        # Add key-related actions
        if keys < 15:  # key_cap
            action_list.extend([LibrariansOffice1_PickDrawers])
            if noises < 22:
                action_list.append(GaolerLibrarian2_LiftKey)

        # Add route-related actions
        action_list.extend([
            MapRoom4_PaintRoutes,
            MapRoom1_LibraryMaps,
        ])

        # Add progress-related actions
        if progress >= 40:
            action_list.extend([Deck_RefillHand])
        
        action_list.extend([
            ReadingRoom_OpenTheBook,
            ApocryphaFound_Claim,
        ])

        return action_list

    def _find_best_action(self, action_list: List[Any]) -> Tuple[Optional[Any], Optional[Any]]:
        """Find the best available action from the list."""
        for action in action_list:
            if action.can_perform(self):
                return None, action
        return None, None

    def best_action_by_simple_ranking_speed(self) -> Tuple[Optional[Any], Optional[Any]]:
        """
        Determine the best action based on speed optimization.
        
        Returns:
            Tuple of (best_card, best_action) or (None, None) if no action available
        """
        # Implementation similar to economic ranking but with different priorities
        # TODO: Implement speed-based optimization
        pass

class StacksSimRunner(SimulationRunner):
    def __init__(self, runs: int, initial_values: dict):
        super().__init__(runs, initial_values)
        self.storylets = []  # Will be initialized in create_state
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
        
        for item in (
            Item.LibraryKey,
            Item.RouteTracedThroughTheLibrary,
            Item.FragmentaryOntology,
            Item.AnathemaUnchained):

            state.items[item] = self.total_item_changes.get(item, 0)

        state.items[Item.ApocryphaSought] = ApocryphaSoughtBook.CodexOfUnrealPlaces.value            

        # Initialize storylets with the state
        self.storylets = [
            Deck_RefillHand(state),
            Storylet_ToggleCartographer(state),
            Storylet_EnterStacks(state),
            Storylet_FindYourWayBack(state),
            Storylet_ReturnToRoof(state),
            ApocryphaFound(state),
            ReadingRoom(state)
        ]

        return state

class StacksStorylets:
    """Base class for all Stacks storylets."""
    def __init__(self, state: LibraryState):
        self.state = state

class Deck_RefillHand(StacksStorylets):
    """Storylet for refilling the player's hand."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Refill Hand"
        self.description = "Draw cards to refill your hand"
        self.actions = [self.Action_RefillHand()]

    class Action_RefillHand:
        def __init__(self):
            self.name = "Draw cards"
            self.description = "Draw cards until you have 4 in hand"

        def perform(self, state: LibraryState) -> bool:
            """Draw cards until hand is full."""
            while len(state.hand) < 4 and state.deck:
                state.hand.append(state.deck.pop())
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if hand is not full and deck is not empty."""
            return len(state.hand) < 4 and len(state.deck) > 0

class Storylet_ToggleCartographer(StacksStorylets):
    """Storylet for toggling the Cartographer's Hoard."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Cartographer's Hoard"
        self.description = "Toggle the Cartographer's Hoard"
        self.actions = [self.Action_ToggleCartographer()]

    class Action_ToggleCartographer:
        def __init__(self):
            self.name = "Toggle Cartographer's Hoard"
            self.description = "Toggle the Cartographer's Hoard"

        def perform(self, state: LibraryState) -> bool:
            """Toggle the Cartographer's Hoard state."""
            state.cartographer_hoard = not state.cartographer_hoard
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can always perform."""
            return True

class Storylet_EnterStacks(StacksStorylets):
    """Storylet for entering the Stacks."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Enter the Stacks"
        self.description = "Enter the Stacks"
        self.actions = [self.Action_EnterStacks()]

    class Action_EnterStacks:
        def __init__(self):
            self.name = "Enter the Stacks"
            self.description = "Enter the Stacks"

        def perform(self, state: LibraryState) -> bool:
            """Enter the Stacks and initialize state."""
            state.in_stacks = True
            state.stacks_progress = 0
            state.route_traced = 0
            state.fragmentary_ontology = 0
            state.library_key = 0
            state.noise = 0
            state.hand = []
            state.deck = []
            state.cartographer_hoard = False
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if not already in Stacks."""
            return not state.in_stacks

class Storylet_FindYourWayBack(StacksStorylets):
    """Storylet for finding your way back."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Find Your Way Back"
        self.description = "Find your way back"
        self.actions = [self.Action_FindYourWayBack()]

    class Action_FindYourWayBack:
        def __init__(self):
            self.name = "Find Your Way Back"
            self.description = "Find your way back"

        def perform(self, state: LibraryState) -> bool:
            """Find your way back and reset state."""
            state.in_stacks = False
            state.stacks_progress = 0
            state.route_traced = 0
            state.fragmentary_ontology = 0
            state.library_key = 0
            state.noise = 0
            state.hand = []
            state.deck = []
            state.cartographer_hoard = False
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if in Stacks."""
            return state.in_stacks

class Storylet_ReturnToRoof(StacksStorylets):
    """Storylet for returning to the roof."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Return to Roof"
        self.description = "Return to the roof"
        self.actions = [self.Action_ReturnToRoof()]

    class Action_ReturnToRoof:
        def __init__(self):
            self.name = "Return to Roof"
            self.description = "Return to the roof"

        def perform(self, state: LibraryState) -> bool:
            """Return to the roof and reset state."""
            state.in_stacks = False
            state.stacks_progress = 0
            state.route_traced = 0
            state.fragmentary_ontology = 0
            state.library_key = 0
            state.noise = 0
            state.hand = []
            state.deck = []
            state.cartographer_hoard = False
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if in Stacks."""
            return state.in_stacks

class ApocryphaFound(StacksStorylets):
    """Storylet for finding Apocrypha."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Apocrypha Found"
        self.description = "Apocrypha Found"
        self.actions = [self.Action_ApocryphaFound()]

    class Action_ApocryphaFound:
        def __init__(self):
            self.name = "Apocrypha Found"
            self.description = "Apocrypha Found"

        def perform(self, state: LibraryState) -> bool:
            """Mark Apocrypha as found and reset state."""
            state.apocrypha_found = True
            state.in_stacks = False
            state.stacks_progress = 0
            state.route_traced = 0
            state.fragmentary_ontology = 0
            state.library_key = 0
            state.noise = 0
            state.hand = []
            state.deck = []
            state.cartographer_hoard = False
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if in Stacks and have enough progress."""
            return state.in_stacks and state.stacks_progress >= 100

class ReadingRoom(StacksStorylets):
    """Storylet for the Reading Room."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Reading Room"
        self.description = "Reading Room"
        self.actions = [self.Action_ReadingRoom()]

    class Action_ReadingRoom:
        def __init__(self):
            self.name = "Reading Room"
            self.description = "Reading Room"

        def perform(self, state: LibraryState) -> bool:
            """Enter the Reading Room and reset state."""
            state.in_stacks = False
            state.stacks_progress = 0
            state.route_traced = 0
            state.fragmentary_ontology = 0
            state.library_key = 0
            state.noise = 0
            state.hand = []
            state.deck = []
            state.cartographer_hoard = False
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if in Stacks."""
            return state.in_stacks

class OpportunityCard:
    """Base class for all opportunity cards."""
    def __init__(self, state: LibraryState):
        self.state = state
        self.name = "Opportunity Card"
        self.description = "Base opportunity card"
        self.actions = []

class ChainedOctavo(OpportunityCard):
    """Opportunity card for the Chained Octavo."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Chained Octavo"
        self.description = "A chained octavo"
        self.actions = [
            self.Action_Unchain(),
            self.Action_ExamineSection()
        ]

    class Action_Unchain:
        def __init__(self):
            self.name = "Unchain"
            self.description = "Unchain the octavo"

        def perform(self, state: LibraryState) -> bool:
            """Unchain the octavo and gain progress."""
            state.stacks_progress += 10
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 5

    class Action_ExamineSection:
        def __init__(self):
            self.name = "Examine Section"
            self.description = "Examine a section of the octavo"

        def perform(self, state: LibraryState) -> bool:
            """Examine section and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 3

class Atrium(OpportunityCard):
    """Opportunity card for the Atrium."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Atrium"
        self.description = "The Atrium"
        self.actions = [
            self.Action_Explore(),
            self.Action_Study()
        ]

    class Action_Explore:
        def __init__(self):
            self.name = "Explore"
            self.description = "Explore the Atrium"

        def perform(self, state: LibraryState) -> bool:
            """Explore and gain route traced."""
            state.route_traced += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can always perform."""
            return True

    class Action_Study:
        def __init__(self):
            self.name = "Study"
            self.description = "Study in the Atrium"

        def perform(self, state: LibraryState) -> bool:
            """Study and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 4

class MapRoom(OpportunityCard):
    """Opportunity card for the Map Room."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Map Room"
        self.description = "The Map Room"
        self.actions = [
            self.Action_LibraryMaps(),
            self.Action_StudyMaps(),
            self.Action_PaintRoutes()
        ]

    class Action_LibraryMaps:
        def __init__(self):
            self.name = "Library Maps"
            self.description = "Study the library maps"

        def perform(self, state: LibraryState) -> bool:
            """Study maps and gain route traced."""
            state.route_traced += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can always perform."""
            return True

    class Action_StudyMaps:
        def __init__(self):
            self.name = "Study Maps"
            self.description = "Study the maps in detail"

        def perform(self, state: LibraryState) -> bool:
            """Study maps and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 3

    class Action_PaintRoutes:
        def __init__(self):
            self.name = "Paint Routes"
            self.description = "Paint routes on the maps"

        def perform(self, state: LibraryState) -> bool:
            """Paint routes and gain significant route traced."""
            state.route_traced += 4
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 5

class DeadEnd(OpportunityCard):
    """Opportunity card for the Dead End."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Dead End"
        self.description = "A dead end in the stacks"
        self.actions = [
            self.Action_Retrace(),
            self.Action_Investigate(),
            self.Action_VantagePoint()
        ]

    class Action_Retrace:
        def __init__(self):
            self.name = "Retrace"
            self.description = "Retrace your steps"

        def perform(self, state: LibraryState) -> bool:
            """Retrace steps and reduce noise."""
            state.noise = max(0, state.noise - 1)
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can always perform."""
            return True

    class Action_Investigate:
        def __init__(self):
            self.name = "Investigate"
            self.description = "Investigate the dead end"

        def perform(self, state: LibraryState) -> bool:
            """Investigate and gain route traced."""
            state.route_traced += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if noise is not too high."""
            return state.noise < 5

    class Action_VantagePoint:
        def __init__(self):
            self.name = "Vantage Point"
            self.description = "Use the dead end as a vantage point"

        def perform(self, state: LibraryState) -> bool:
            """Use vantage point and gain significant route traced."""
            state.route_traced += 3
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 4

class PoisonGallery(OpportunityCard):
    """Opportunity card for the Poison Gallery."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Poison Gallery"
        self.description = "The Poison Gallery"
        self.actions = [
            self.Action_FurnitureSteppingStones(),
            self.Action_StudyPoison()
        ]

    class Action_FurnitureSteppingStones:
        def __init__(self):
            self.name = "Furniture Stepping Stones"
            self.description = "Use furniture as stepping stones"

        def perform(self, state: LibraryState) -> bool:
            """Use furniture and gain route traced."""
            state.route_traced += 3
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 2

    class Action_StudyPoison:
        def __init__(self):
            self.name = "Study Poison"
            self.description = "Study the poison"

        def perform(self, state: LibraryState) -> bool:
            """Study poison and gain fragmentary ontology."""
            state.fragmentary_ontology += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 4

class StoneGallery(OpportunityCard):
    """Opportunity card for the Stone Gallery."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Stone Gallery"
        self.description = "The Stone Gallery"
        self.actions = [
            self.Action_SilentGallery(),
            self.Action_StudyStones()
        ]

    class Action_SilentGallery:
        def __init__(self):
            self.name = "Silent Gallery"
            self.description = "Move through the silent gallery"

        def perform(self, state: LibraryState) -> bool:
            """Move silently and gain route traced."""
            state.route_traced += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if noise is not too high."""
            return state.noise < 3

    class Action_StudyStones:
        def __init__(self):
            self.name = "Study Stones"
            self.description = "Study the stones"

        def perform(self, state: LibraryState) -> bool:
            """Study stones and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 3

class Index(OpportunityCard):
    """Opportunity card for the Index."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Index"
        self.description = "The Index"
        self.actions = [
            self.Action_Search(),
            self.Action_StudyIndex()
        ]

    class Action_Search:
        def __init__(self):
            self.name = "Search"
            self.description = "Search the index"

        def perform(self, state: LibraryState) -> bool:
            """Search and gain route traced."""
            state.route_traced += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can always perform."""
            return True

    class Action_StudyIndex:
        def __init__(self):
            self.name = "Study Index"
            self.description = "Study the index"

        def perform(self, state: LibraryState) -> bool:
            """Study index and gain fragmentary ontology."""
            state.fragmentary_ontology += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 5

class LibrariansOffice(OpportunityCard):
    """Opportunity card for the Librarian's Office."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Librarian's Office"
        self.description = "The Librarian's Office"
        self.actions = [
            self.Action_PickDrawers(),
            self.Action_StudyOffice(),
            self.Action_SearchDesk()
        ]

    class Action_PickDrawers:
        def __init__(self):
            self.name = "Pick Drawers"
            self.description = "Pick through the drawers"

        def perform(self, state: LibraryState) -> bool:
            """Pick drawers and gain library key."""
            state.library_key += 1
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 6

    class Action_StudyOffice:
        def __init__(self):
            self.name = "Study Office"
            self.description = "Study the office"

        def perform(self, state: LibraryState) -> bool:
            """Study office and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 4

    class Action_SearchDesk:
        def __init__(self):
            self.name = "Search Desk"
            self.description = "Search the librarian's desk"

        def perform(self, state: LibraryState) -> bool:
            """Search desk and gain significant fragmentary ontology."""
            state.fragmentary_ontology += 2
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 7

class FloweringGallery(OpportunityCard):
    """Opportunity card for the Flowering Gallery."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Flowering Gallery"
        self.description = "The Flowering Gallery"
        self.actions = [
            self.Action_KeepGoing(),
            self.Action_StudyFlowers()
        ]

    class Action_KeepGoing:
        def __init__(self):
            self.name = "Keep Going"
            self.description = "Keep going through the gallery"

        def perform(self, state: LibraryState) -> bool:
            """Keep going and gain route traced."""
            state.route_traced += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can always perform."""
            return True

    class Action_StudyFlowers:
        def __init__(self):
            self.name = "Study Flowers"
            self.description = "Study the flowers"

        def perform(self, state: LibraryState) -> bool:
            """Study flowers and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 3

class BlackGallery(OpportunityCard):
    """Opportunity card for the Black Gallery."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Black Gallery"
        self.description = "The Black Gallery"
        self.actions = [
            self.Action_Explore(),
            self.Action_StudyBlack()
        ]

    class Action_Explore:
        def __init__(self):
            self.name = "Explore"
            self.description = "Explore the black gallery"

        def perform(self, state: LibraryState) -> bool:
            """Explore and gain route traced."""
            state.route_traced += 3
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 5

    class Action_StudyBlack:
        def __init__(self):
            self.name = "Study Black"
            self.description = "Study the black gallery"

        def perform(self, state: LibraryState) -> bool:
            """Study black gallery and gain fragmentary ontology."""
            state.fragmentary_ontology += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 7

class GaolerLibrarian(OpportunityCard):
    """Opportunity card for the Gaoler Librarian."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Gaoler Librarian"
        self.description = "The Gaoler Librarian"
        self.actions = [
            self.Action_Distract(),
            self.Action_LiftKey()
        ]

    class Action_Distract:
        def __init__(self):
            self.name = "Distract"
            self.description = "Distract the gaoler librarian"

        def perform(self, state: LibraryState) -> bool:
            """Distract and reduce noise."""
            state.noise = max(0, state.noise - 2)
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if noise is high enough."""
            return state.noise >= 2

    class Action_LiftKey:
        def __init__(self):
            self.name = "Lift Key"
            self.description = "Lift the key from the gaoler librarian"

        def perform(self, state: LibraryState) -> bool:
            """Lift key and gain library key."""
            state.library_key += 1
            state.noise += 3
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if noise is low enough."""
            return state.noise < 2

class TerribleShushing(OpportunityCard):
    """Opportunity card for the Terrible Shushing."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Terrible Shushing"
        self.description = "The Terrible Shushing"
        self.actions = [
            self.Action_Ignore(),
            self.Action_Investigate()
        ]

    class Action_Ignore:
        def __init__(self):
            self.name = "Ignore"
            self.description = "Ignore the shushing"

        def perform(self, state: LibraryState) -> bool:
            """Ignore and reduce noise."""
            state.noise = max(0, state.noise - 1)
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can always perform."""
            return True

    class Action_Investigate:
        def __init__(self):
            self.name = "Investigate"
            self.description = "Investigate the shushing"

        def perform(self, state: LibraryState) -> bool:
            """Investigate and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if noise is not too high."""
            return state.noise < 4

class GodsEyeView(OpportunityCard):
    """Opportunity card for the God's Eye View."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "God's Eye View"
        self.description = "The God's Eye View"
        self.actions = [
            self.Action_HoldItAll(),
            self.Action_StudyView()
        ]

    class Action_HoldItAll:
        def __init__(self):
            self.name = "Hold It All"
            self.description = "Hold the entire view in your mind"

        def perform(self, state: LibraryState) -> bool:
            """Hold view and gain route traced."""
            state.route_traced += 4
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 8

    class Action_StudyView:
        def __init__(self):
            self.name = "Study View"
            self.description = "Study the god's eye view"

        def perform(self, state: LibraryState) -> bool:
            """Study view and gain fragmentary ontology."""
            state.fragmentary_ontology += 3
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 6

class ShapeOfTheLabyrinth(OpportunityCard):
    """Opportunity card for the Shape of the Labyrinth."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Shape of the Labyrinth"
        self.description = "The Shape of the Labyrinth"
        self.actions = [
            self.Action_RethinkMovements(),
            self.Action_StudyShape()
        ]

    class Action_RethinkMovements:
        def __init__(self):
            self.name = "Rethink Movements"
            self.description = "Rethink your movements"

        def perform(self, state: LibraryState) -> bool:
            """Rethink movements and gain route traced."""
            state.route_traced += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 4

    class Action_StudyShape:
        def __init__(self):
            self.name = "Study Shape"
            self.description = "Study the shape of the labyrinth"

        def perform(self, state: LibraryState) -> bool:
            """Study shape and gain fragmentary ontology."""
            state.fragmentary_ontology += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 6

class GreyCardinal(OpportunityCard):
    """Opportunity card for the Grey Cardinal."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Grey Cardinal"
        self.description = "The Grey Cardinal"
        self.actions = [
            self.Action_FurryLunch(),
            self.Action_StudyCardinal()
        ]

    class Action_FurryLunch:
        def __init__(self):
            self.name = "Furry Lunch"
            self.description = "Have a furry lunch"

        def perform(self, state: LibraryState) -> bool:
            """Have lunch and reduce noise."""
            state.noise = max(0, state.noise - 2)
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if noise is high enough."""
            return state.noise >= 2

    class Action_StudyCardinal:
        def __init__(self):
            self.name = "Study Cardinal"
            self.description = "Study the grey cardinal"

        def perform(self, state: LibraryState) -> bool:
            """Study cardinal and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if noise is not too high."""
            return state.noise < 3

class GlimpseThroughAWindow(OpportunityCard):
    """Opportunity card for the Glimpse Through a Window."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Glimpse Through a Window"
        self.description = "A glimpse through a window"
        self.actions = [
            self.Action_Look(),
            self.Action_StudyGlimpse()
        ]

    class Action_Look:
        def __init__(self):
            self.name = "Look"
            self.description = "Look through the window"

        def perform(self, state: LibraryState) -> bool:
            """Look and gain route traced."""
            state.route_traced += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can always perform."""
            return True

    class Action_StudyGlimpse:
        def __init__(self):
            self.name = "Study Glimpse"
            self.description = "Study the glimpse"

        def perform(self, state: LibraryState) -> bool:
            """Study glimpse and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 3

class TeaRoom(OpportunityCard):
    """Opportunity card for the Tea Room."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Tea Room"
        self.description = "The Tea Room"
        self.actions = [
            self.Action_Regroup(),
            self.Action_StudyTea()
        ]

    class Action_Regroup:
        def __init__(self):
            self.name = "Regroup"
            self.description = "Regroup in the tea room"

        def perform(self, state: LibraryState) -> bool:
            """Regroup and reduce noise."""
            state.noise = max(0, state.noise - 3)
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if noise is high enough."""
            return state.noise >= 3

    class Action_StudyTea:
        def __init__(self):
            self.name = "Study Tea"
            self.description = "Study the tea room"

        def perform(self, state: LibraryState) -> bool:
            """Study tea room and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if noise is not too high."""
            return state.noise < 2

class DiscardedLadder(OpportunityCard):
    """Opportunity card for a discarded ladder in the Stacks."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Discarded Ladder"
        self.description = "A discarded ladder"
        self.actions = [
            self.Action_Climb(),
            self.Action_StudyLadder()
        ]

    class Action_Climb:
        def __init__(self):
            self.name = "Climb"
            self.description = "Climb the ladder"

        def perform(self, state: LibraryState) -> bool:
            """Climb and gain route traced."""
            state.route_traced += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can always perform."""
            return True

    class Action_StudyLadder:
        def __init__(self):
            self.name = "Study Ladder"
            self.description = "Study the discarded ladder"

        def perform(self, state: LibraryState) -> bool:
            """Study ladder and gain fragmentary ontology."""
            state.fragmentary_ontology += 1
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 3

class GrandStaircase(OpportunityCard):
    """Opportunity card for the Grand Staircase in the Stacks."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Grand Staircase"
        self.description = "The Grand Staircase"
        self.actions = [
            self.Action_Ascend(),
            self.Action_StudyStaircase()
        ]

    class Action_Ascend:
        def __init__(self):
            self.name = "Ascend"
            self.description = "Ascend the grand staircase"

        def perform(self, state: LibraryState) -> bool:
            """Ascend and gain route traced."""
            state.route_traced += 3
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 4

    class Action_StudyStaircase:
        def __init__(self):
            self.name = "Study Staircase"
            self.description = "Study the grand staircase"

        def perform(self, state: LibraryState) -> bool:
            """Study staircase and gain fragmentary ontology."""
            state.fragmentary_ontology += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 5

class LockedGate(OpportunityCard):
    """Opportunity card for a locked gate in the Stacks."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Locked Gate"
        self.description = "A locked gate"
        self.actions = [
            self.Action_Unlock(),
            self.Action_StudyGate()
        ]

    class Action_Unlock:
        def __init__(self):
            self.name = "Unlock"
            self.description = "Unlock the gate"

        def perform(self, state: LibraryState) -> bool:
            """Unlock gate and gain route traced."""
            state.route_traced += 4
            state.noise += 2
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 6

    class Action_StudyGate:
        def __init__(self):
            self.name = "Study Gate"
            self.description = "Study the locked gate"

        def perform(self, state: LibraryState) -> bool:
            """Study gate and gain fragmentary ontology."""
            state.fragmentary_ontology += 2
            state.noise += 1
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.route_traced >= 7

class CartographerSnuffbox(OpportunityCard):
    """Opportunity card for the Cartographer's Snuffbox."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Cartographer's Snuffbox"
        self.description = "The Cartographer's Snuffbox"
        self.actions = [
            self.Action_ComputeFigure(),
            self.Action_Implication()
        ]

    def can_draw(self, state: LibraryState) -> bool:
        """Can draw if cartographer is enabled and have route traced."""
        return state.cartographer_enabled and state.get(Item.RouteTracedThroughTheLibrary) > 0

    class Action_ComputeFigure:
        def __init__(self):
            self.name = "Compute Figure"
            self.description = "Compute the figure"

        def perform(self, state: LibraryState) -> bool:
            """Compute figure and gain progress."""
            state.route_traced -= 1
            state.stacks_progress += 5
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.get(Item.RouteTracedThroughTheLibrary) > 0

    class Action_Implication:
        def __init__(self):
            self.name = "Implication"
            self.description = "Study the implication"

        def perform(self, state: LibraryState) -> bool:
            """Study implication and gain fragmentary ontology."""
            state.route_traced -= 3
            state.fragmentary_ontology += 5
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.get(Item.RouteTracedThroughTheLibrary) >= 3

class CartographerCompass(OpportunityCard):
    """Opportunity card for the Cartographer's Compass."""
    def __init__(self, state: LibraryState):
        super().__init__(state)
        self.name = "Cartographer's Compass"
        self.description = "The Cartographer's Compass"
        self.actions = [
            self.Action_Camera(),
            self.Action_Chart()
        ]

    def can_draw(self, state: LibraryState) -> bool:
        """Can draw if cartographer is enabled."""
        return state.cartographer_enabled

    class Action_Camera:
        def __init__(self):
            self.name = "Camera"
            self.description = "Use the camera"

        def perform(self, state: LibraryState) -> bool:
            """Use camera and gain route traced."""
            state.route_traced += random.randint(1, 3)
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough watchful."""
            return state.outfit.watchful_inerrant15 >= 200

    class Action_Chart:
        def __init__(self):
            self.name = "Chart"
            self.description = "Study the chart"

        def perform(self, state: LibraryState) -> bool:
            """Study chart and gain progress."""
            state.route_traced -= 3
            state.stacks_progress += random.choice([5, 10, 15])
            return True

        def can_perform(self, state: LibraryState) -> bool:
            """Can perform if have enough route traced."""
            return state.get(Item.RouteTracedThroughTheLibrary) >= 3

if __name__ == "__main__":
    # Example usage
    runner = StacksSimRunner(runs=100, initial_values={
        Item.RouteTracedThroughTheLibrary: 0,
        Item.FragmentaryOntology: 0,
        Item.LibraryKey: 0
    })
    stats = runner.run_simulations()
    print("Simulation Results:", stats) 