import random
import sys
from collections import defaultdict
from enum import Enum, auto
from collections import defaultdict

from enums import *
from decks.unterzee import *

item_echo_values = {
    Item.PiecesOfPlunder: 0.01,
    Item.WhirringContraption: 12.5,

    # Menaces
    Item.Wounds: -0.2,
    Item.Nightmares: -0.2
}


class Action:
    def __init__(self, name):
        self.name = name
        self.action_cost = 1

    def can_perform(self, state: 'GameState'):
        return True

    def pass_items(self, state: 'GameState'):
        """Return a dictionary of items to be added on success."""
        return {}  # Default is no items

    def fail_items(self, state: 'GameState'):
        """Return a dictionary of items to be added on failure."""
        return {}  # Default is no items

    def perform(self, state: 'GameState'):
        if self.can_perform(state):
            rate = self.pass_rate(state)
            if random.random() < rate:
                self.perform_pass(state)
                return "Success"
            else:
                self.perform_failure(state)
                return "Failure"
        else:
            return "Cannot Perform"

    def perform_pass(self, state: 'GameState'):
        """Default implementation to add items from pass_items to state.items."""
        for item, amount in self.pass_items(state).items():
            # Ensure item key exists, if not, initialize it
            if item not in state.items:
                state.items[item] = 0
            state.items[item] += amount

    def perform_failure(self, state: 'GameState'):
        """Default implementation to add items from fail_items to state.items."""
        for item, amount in self.fail_items(state).items():
            # Ensure item key exists, if not, initialize it
            if item not in state.items:
                state.items[item] = 0
            state.items[item] += amount

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Default pass rate is 100%

    def pass_ev(self, state: 'GameState'):
        return self.items_ev(state, self.pass_items(state))
    
    def failure_ev(self, state: 'GameState'):
        return self.items_ev(state, self.fail_items(state))
    
    def ev(self, state: 'GameState'):
        pass_rate = min(1.0, max(0.0, self.pass_rate(state)))
        pass_ev = self.pass_ev(state)
        fail_ev = self.failure_ev(state)

        if pass_rate is None:
            print(f"Debug: {self.name} - pass_rate: {pass_rate}, success_ev: {pass_ev}, failure_ev: {fail_ev}")
            pass_rate = 0.0
        if pass_ev is None:
            print(f"Debug: {self.name} - pass_rate: {pass_rate}, success_ev: {pass_ev}, failure_ev: {fail_ev}")
            pass_ev = 0.0
        if fail_ev is None:
            print(f"Debug: {self.name} - pass_rate: {pass_rate}, success_ev: {pass_ev}, failure_ev: {fail_ev}")
            fail_ev = 0.0

        return pass_rate * pass_ev + (1.0 - pass_rate) * fail_ev
    
    def items_ev(self, state: 'GameState', items: dict):
        total_ev = 0
        for item, amount in items.items():
            ev_from_item = state.item_ev(item, amount)
            total_ev += ev_from_item
        return total_ev
        
    
    @staticmethod
    def broad_pass_rate(dc, stat_value):
        return 0.6 * stat_value / dc
    
    @staticmethod
    def narrow_pass_rate(dc, stat_value):
        return 0.5 + (stat_value - dc) * 0.1

class OpportunityCard:
    def __init__(self, name, weight=1.0):
        self.name = name
        self.weight = weight
        self.actions = []  # List of possible actions

    def can_draw(self, state: 'GameState'):
        return True

class OutfitList:
    def __init__(self):
        self.zailing_speed = 55  # Example stat for "Zailing Speed"
        self.dangerous = 300
        self.watchful = 300
        self.persuasive = 300
        self.shadowy = 300

        self.chess_player = 15
        self.zeefaring = 15  # Example stat for "Zeefaring"
        self.monstrous_anatomy = 15
        self.mithridacy = 15
        self.artisan_of_the_red_science = 15
        self.kataleptic_toxicology = 15

class GameState:
    def __init__(self):
        self.outfits = OutfitList()

        self.items = {
            Item.TroubledWaters: 0,
            Item.CreepingFear: 0,

            Item.PiecesOfPlunder: 0,
            Item.ZailingProgress: 0,
            Item.ChasingDownYourBounty: 0,
            Item.UnwelcomeOnTheWaters: 0,
            Item.TimeSpentAtZee: 0,
        }

        # Additional tracking variables for this simulation
        # self.troubled_waters = 0
        self.unwelcome_on_the_waters = 0
        # self.pieces_of_plunder = 0
        # self.zailing = 0
        # self.time_spent_at_zee = 0

        self.progress_required = 80

        # Initialize cards in the deck
        self.deck = []  # This will be populated with cards
        self.hand = []
        self.zee_region = ZeeRegion.HOME_WATERS
        self.actions = 0
        self.total_actions = 0  # Accumulates actions over all runs

        # Tracking data
        self.card_draw_counts = defaultdict(int)
        self.card_play_counts = defaultdict(int)
        self.action_play_counts = defaultdict(int)
        self.action_success_counts = defaultdict(int)
        self.action_failure_counts = defaultdict(int)
        self.total_item_changes = defaultdict(int)

        # Track total changes for each item
        self.total_item_changes = defaultdict(int)

        self.status = "InProgress"

    def region_data(self):
        return zee_regions[self.zee_region]

    def draw_card(self):
        drawn, lowest = None, float('inf')
        for card in self.deck:
            if card not in self.hand and card.can_draw(self):
                rand = random.random() / card.weight
                if rand < lowest:
                    drawn = card
                    lowest = rand

        if drawn:
            self.card_draw_counts[drawn.name] += 1
            self.hand.append(drawn)

    def step(self):
        # TODO smart redraw
        while len(self.hand) < 3:
            self.draw_card()

        best_card, best_action, best_action_ev = None, None, -float('inf')

        for card in self.hand:
            for action in card.actions:
                if action.can_perform(self):
                    action_ev = action.ev(self)
                    if action_ev > best_action_ev:
                        best_card, best_action, best_action_ev = card, action, action_ev

        if best_action:
            outcome = best_action.perform(self)
            self.action_play_counts[best_action.name] += 1
            self.actions += best_action.action_cost
            if outcome == "Success":
                self.action_success_counts[best_action.name] += 1
            else:
                self.action_failure_counts[best_action.name] += 1

        if best_card is not None:
            self.card_play_counts[best_card.name] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)            

        self.hand = [card for card in self.hand if card.can_draw(self)]

    def run(self):
        self.items[Item.ZailingProgress] = 0  # Reset progress for each run
        while self.items[Item.ZailingProgress] < 80:
            self.step()

        self.total_actions += self.actions  # Accumulate total actions after the run


    def update_item_totals(self):
        for item, count in self.items.items():
            self.total_item_changes[item] += count

    def reset(self):
        """Reset relevant parts of the game state but keep the deck and stats."""
        self.items = {item: 0 for item in Item}
        self.hand = []
        self.actions = 0
        self.items[Item.ZailingProgress] = 0  # Reset progress for each run

    def display_results(self, runs: int):
        avg_actions_per_run = self.total_actions / runs
        print(f"\nAverage Actions per Run: {avg_actions_per_run:.2f}")

        # Card and Action results display
        print_condensed_action_table(
            self.action_play_counts,
            self.action_success_counts,
            self.action_failure_counts,
            self.card_draw_counts,
            self.card_play_counts,
            self.deck,
            runs
        )

        # Display average change in items
        print_item_summary(self.total_item_changes, runs)
        print(f"\nAverage Actions per Run: {avg_actions_per_run:.2f}")
        
        # Optionally, display other tracking metrics if needed

    def item_ev(self, item: Item, val: int):
        if item == Item.ZailingProgress:
            return self.progress_ev(val)
        elif item == Item.TroubledWaters:
            return self.tw_ev(val)
        else:
            echo_value = item_echo_values.get(item, 0)
            # TODO echo value
            return echo_value * val

    def progress_ev(self, val: int):
        """Calculates the EV for a given progress value based on current progress."""
        # TODO
        prog_unit_ev = 0.1
        baseline_ev = 5.5

        # Current progress
        current_progress = self.items.get(Item.ZailingProgress, 0)
        zailing_speed = self.outfits.zailing_speed        
        remaining_progress = self.progress_required - current_progress
        
        if remaining_progress <= 0:
            return 0.0
        elif remaining_progress <= val:
            return baseline_ev
        elif remaining_progress <= (val + zailing_speed):
            return baseline_ev
        else:
            return val * prog_unit_ev
    
    def tw_ev(self, val: int):
        # TODO
        tw_unit_ev = -2
        failure_threshold = 36

        current_tw = self.items.get(Item.TroubledWaters, 0)
        if current_tw + val >= failure_threshold:
            return -10000
        else:
            return tw_unit_ev * val


################################################################################


class BlankSpaceOnTheCharts(OpportunityCard):
    def __init__(self):
        super().__init__("A Blank Space on the Charts")
        self.actions = [TheresAnIslandHere(), FortuitousFragments(), SearchUnchartedWaters()]

class TheresAnIslandHere(Action):
    def __init__(self):
        super().__init__("There's an island here")

    def pass_items(self, state: 'GameState'):
        return {
            Item.CreepingFear: 1,
            Item.TroubledWaters: -5
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.CreepingFear: 1,
            Item.Nightmares: 3,
            Item.ZailingProgress: -60,
            Item.TroubledWaters: 4
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge

class FortuitousFragments(Action):
    def __init__(self):
        super().__init__("Fortuitous fragments")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.PartialMap: -2
        }

    def can_perform(self, state: 'GameState'):
        return state.items.get(Item.PartialMap, 0) >= 2  # Requires 2 Partial Maps

class SearchUnchartedWaters(Action):
    def __init__(self):
        super().__init__("Search the uncharted waters for your quarry")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -1,
            Item.ChasingDownYourBounty: random.randint(1, 5),
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -5,
            Item.CreepingFear: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(6, state.outfits.zeefaring)
    
################################################################################
###                          BountyUponYourHead                               ###
################################################################################

class BountyUponYourHead(OpportunityCard):
    def __init__(self):
        super().__init__("A Bounty Upon Your Head", 1.0)
        self.actions = [OpenFire(), SignalRamillies(), EvadeThem()]

class OpenFire(Action):
    def __init__(self):
        super().__init__("Open Fire!")
    
    def pass_rate(self, state: 'GameState'):
        # Narrow challenge, Zeefaring 13 (50% base)
        return self.narrow_pass_rate(13, state.outfits.zeefaring)

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.PiecesOfPlunder: random.randint(1, 3),
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 12,
            Item.UnwelcomeOnTheWaters: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

class SignalRamillies(Action):
    def __init__(self):
        super().__init__("Signal the HMS Ramillies for Support")
    
    def pass_rate(self, state: 'GameState'):
        # Narrow challenge, Zeefaring 11 (50% base)
        return self.narrow_pass_rate(11, state.outfits.zeefaring)

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.PiecesOfPlunder: random.randint(1, 2),
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 12,
            Item.UnwelcomeOnTheWaters: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

class EvadeThem(Action):
    def __init__(self):
        super().__init__("Evade Them!")

    def pass_rate(self, state: 'GameState'):
        # Broad challenge, Zailing Speed 45 (60% base)
        return self.broad_pass_rate(45, state.outfits.zailing_speed)

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: random.randint(2, 3),
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.UnwelcomeOnTheWaters: 1
        }

################################################################################

class CorvetteOfHerMajestysNavy(OpportunityCard):
    def __init__(self):
        super().__init__("A Corvette of Her Majesty's Navy")
        self.actions = [ExchangePleasantries(), TheyreNotSlowing(), RelyOnOldCodes()]

class ExchangePleasantries(Action):
    def __init__(self):
        super().__init__("Exchange pleasantries via semaphore")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ZailingProgress: random.randint(1, 5)
        }

class TheyreNotSlowing(Action):
    def __init__(self):
        super().__init__("They're not slowing")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Suspicion: 3,
            Item.TroubledWaters: 3,
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.SilentStalker: 1,
            Item.TroubledWaters: 9,
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(55, state.outfits.zailing_speed)

class RelyOnOldCodes(Action):
    def __init__(self):
        super().__init__("Rely on the Commodore's old codes")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Suspicion: -3,
            Item.TroubledWaters: -random.randint(2, 8),
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.Suspicion: 4,
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(5, state.outfits.chess_player)

################################################################################


class CorvetteWithCorsairColours(OpportunityCard):
    def __init__(self):
        super().__init__("A Corvette of Her Majesty's Navy (with Corsair's Colours)")
        self.actions = [ExchangeInfo(), TakeThemForAll(), TheyreNotSlowing()]

class ExchangeInfo(Action):
    def __init__(self):
        super().__init__("Exchange information via semaphore")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ChasingDownYourBounty: 8,
            Item.ZailingProgress: random.randint(1, 5)
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 6,
            Item.Suspicion: 2,
            Item.UnwelcomeOnTheWaters: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5)
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(160, state.outfits.persuasive)

class TakeThemForAll(Action):
    def __init__(self):
        super().__init__("Take them for all they've got")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Suspicion: 1,
            Item.TroubledWaters: 4,
            Item.PiecesOfPlunder: random.randint(1, 3),
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.Suspicion: 4,
            Item.TroubledWaters: 8,
            Item.UnwelcomeOnTheWaters: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(5, state.outfits.zeefaring)

class TheyreNotSlowing(Action):
    def __init__(self):
        super().__init__("They're not slowing")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Suspicion: 3,
            Item.TroubledWaters: 3,
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.SilentStalker: 1,
            Item.TroubledWaters: 9,
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(75, state.outfits.zailing_speed)

################################################################################

class DreamOfACup(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of a Cup")
        self.actions = [DrinkTheWine(), AwakenFromDream()]

class DrinkTheWine(Action):
    def __init__(self):
        super().__init__("Drink the wine")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RosyColours: 4,
            Item.Nightmares: 3
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Nightmares: -3,
            Item.RosyColours: 0
        }

################################################################################

class DreamOfATable(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of a Table")
        self.actions = [JoinThemAtTheTable(), AwakenFromDream()]

class JoinThemAtTheTable(Action):
    def __init__(self):
        super().__init__("Join them at their table")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RosyColours: 6,
            Item.Nightmares: 3
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Nightmares: -3,
            Item.RosyColours: 0
        }
    
################################################################################
###                             DreamOfAscent                                 ###
################################################################################

class DreamOfAscent(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of Ascent")
        self.actions = [FlyHigher(), AwakenFromDream()]

class FlyHigher(Action):
    def __init__(self):
        super().__init__("Fly higher")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RosyColours: 5,
            Item.Nightmares: 3
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Nightmares: -3,
            Item.RosyColours: 0
        }


################################################################################
###                             DreamOfDesigns                                ###
################################################################################

class DreamOfDesigns(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of Designs")
        self.actions = [SunbatheInTheLight(), AwakenFromDream()]

class SunbatheInTheLight(Action):
    def __init__(self):
        super().__init__("Sunbathe in the light")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RosyColours: 0,  # 'Rosy Colours' quality is removed
            Item.Nightmares: 3,
            Item.WhirringContraption: 11  # New Accomplishment
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Nightmares: -3,
            Item.RosyColours: 0
        }


################################################################################
###                           DreamOfStainedGlass                             ###
################################################################################

class DreamOfStainedGlass(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of Stained-Glass")
        self.actions = [LookIntoTheLight(), AwakenFromDream()]

class LookIntoTheLight(Action):
    def __init__(self):
        super().__init__("Look into the light")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RosyColours: 3,
            Item.Nightmares: 2
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Nightmares: -3,
            Item.RosyColours: 0
        }


################################################################################
###                            DreamOfSunbeams                                ###
################################################################################

class DreamOfSunbeams(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of Sunbeams")
        self.actions = [StareThroughTheGlare(), AwakenFromDream()]

class StareThroughTheGlare(Action):
    def __init__(self):
        super().__init__("Stare through the glare")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RosyColours: 3,
            Item.Nightmares: 2
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Nightmares: -3,
            Item.RosyColours: 0
        }

################################################################################
###                            FlockOfProphets                                ###
################################################################################

class FlockOfProphets(OpportunityCard):
    def __init__(self):
        super().__init__("A Flock of Prophets")
        self.actions = [TakeAuspices(), ZailAroundThem()]

class TakeAuspices(Action):
    def __init__(self):
        super().__init__("Take auspices")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ChasingDownYourBounty: random.randint(1, 5),
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(13, state.outfits.zeefaring)

class ZailAroundThem(Action):
    def __init__(self):
        super().__init__("Zail around them")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

################################################################################
###                            GiantAnglerCrab                                ###
################################################################################

class GiantAnglerCrab(OpportunityCard):
    def __init__(self):
        super().__init__("A Giant Angler Crab")
        self.actions = [FullReverse(), ReadyGuns(), PursueIt(), HarpoonRamming()]

class FullReverse(Action):
    def __init__(self):
        super().__init__("Full reverse! Turn us away!")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.SilentStalker: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(80, state.outfits.shadowy)

class ReadyGuns(Action):
    def __init__(self):
        super().__init__("Ready the guns and fire at its soft spots")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.SilentStalker: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(3, state.outfits.monstrous_anatomy)

class PursueIt(Action):
    def __init__(self):
        super().__init__("Pursue it to its spawning grounds")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: int(state.outfits.zailing_speed * 1.2),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed // 2
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(75, state.outfits.shadowy)

class HarpoonRamming(Action):
    def __init__(self):
        super().__init__("Reach for your harpoon; call for ramming speed!")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.DeepZeeCatch: 5,
            Item.TroubledWaters: 1,
            # TODO
            # Item.RumblingStomachs: 0  # Removes Rumbling Stomachs
        }
    
    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success


################################################################################
###                            GrowingConcern                                ###
################################################################################

class GrowingConcern(OpportunityCard):
    def __init__(self):
        super().__init__("A Growing Concern")
        self.actions = [Investigate(), DoubleZailorsRations()]

class Investigate(Action):
    def __init__(self):
        super().__init__("Investigate")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -5
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.Nightmares: 8,
            Item.TroubledWaters: 5
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # Luck challenge

class DoubleZailorsRations(Action):
    def __init__(self):
        super().__init__("Double the zailors' rations")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.CrateOfIncorruptibleBiscuits: -1,
            Item.FoxfireCandleStub: -100,
            Item.BottleOfGreyfields1882: -100,
            Item.RumblingStomachs: 1
        }

    def can_perform(self, state: 'GameState'):
        return (state.items.get(Item.CrateOfIncorruptibleBiscuits, 0) >= 1 and
                state.items.get(Item.FoxfireCandleStub, 0) >= 100 and
                state.items.get(Item.BottleOfGreyfields1882, 0) >= 100)


################################################################################
###                            HugeTerribleBeast                                ###
################################################################################

class HugeTerribleBeast(OpportunityCard):
    def __init__(self):
        super().__init__("A Huge Terrible Beast of the Unterzee!")
        self.actions = [DeliciousLumps(), SteamOnBy()]

class DeliciousLumps(Action):
    def __init__(self):
        super().__init__("Delicious, delicious lumps")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.AppallingSecret: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.UnaccountablyPeckish: 1,
            # Item.SomeoneIsComing: 1,
            Item.TaleOfTerror: 4,
            Item.RumblingStomachs: 1,  # Set Rumbling Stomachs to 1
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.RumblingStomachs: 1  # Set Rumbling Stomachs to 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.dangerous)

class SteamOnBy(Action):
    def __init__(self):
        super().__init__("Steam on by")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.SilentStalker: 1,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

################################################################################
###                            MessageInABottle                                ###
################################################################################

# TODO complicated!
class MessageInABottle(OpportunityCard):
    def __init__(self):
        super().__init__("A Message in a Bottle")
        self.actions = [UnfurlThePaper()]

class UnfurlThePaper(Action):
    def __init__(self):
        super().__init__("Unfurl the paper")
    
    def pass_items(self, state: 'GameState'):
        # The effects of this action depend on a complex set of conditions, so we'll simplify it here.
        return {
            # Item.DirectionsToAHiddenStash: random.randint(1, 8),
            Item.SizeOfBuriedStash: 0  # The Size of a Buried Stash Quality is reset
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success


################################################################################
###                            NavigationError                                ###
################################################################################

class NavigationError(OpportunityCard):
    def __init__(self):
        super().__init__("A Navigation Error")
        self.actions = [CorrectYourCourse(), ListenToTheZee(), StarvedMen(), LetYourStarGuide(), UseDisorientation()]

class CorrectYourCourse(Action):
    def __init__(self):
        super().__init__("Correct your course")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.MapScrap: 10,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.watchful)

class ListenToTheZee(Action):
    def __init__(self):
        super().__init__("Listen to the Zee")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.MapScrap: 12,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 9,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(5, state.outfits.zeefaring)

class StarvedMen(Action):
    def __init__(self):
        super().__init__("Consider what you learned from the Starved Men")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.MapScrap: 13,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 9,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.watchful)

class LetYourStarGuide(Action):
    def __init__(self):
        super().__init__("Let your own star guide you")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -5,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.persuasive)

class UseDisorientation(Action):
    def __init__(self):
        super().__init__("Use your disorientation to your advantage")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: random.randint(2, 3),
            Item.ChasingDownYourBounty: random.randint(1, 5),
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(5, state.outfits.zeefaring)


################################################################################
###                            PromisingWreck                                ###
################################################################################

class PromisingWreck(OpportunityCard):
    def __init__(self):
        super().__init__("A Promising Wreck")
        self.actions = [DiveForSalvage(), ZailOnBy()]

class DiveForSalvage(Action):
    def __init__(self):
        super().__init__("Dive for salvage")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.PiecesOfPlunder: random.randint(1, 3),
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.CreepingFear: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(13, state.outfits.zeefaring)

class ZailOnBy(Action):
    def __init__(self):
        super().__init__("Zail on by")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

################################################################################
###                            RagtagFlotilla                                ###
################################################################################

class RagtagFlotilla(OpportunityCard):
    def __init__(self):
        super().__init__("A Ragtag Flotilla")
        self.actions = [HailAShip(), SteamOnBy()]

class HailAShip(Action):
    def __init__(self):
        super().__init__("Hail a ship and inquire about their purpose")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TaleOfTerror: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TroubledWaters: -2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class SteamOnBy(Action):
    def __init__(self):
        super().__init__("Steam on by")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success


################################################################################
###                             A Ship of Zealots                             ###
################################################################################

class ShipOfZealots(OpportunityCard):
    def __init__(self):
        super().__init__("A Ship of Zealots")
        self.actions = [SeeThemOff(), RaceAway(), PreachVariantCreed(), SignalSamaritan(), SendToFathomking()]

class SeeThemOff(Action):
    def __init__(self):
        super().__init__("See them off")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(200, state.outfits.dangerous)

class RaceAway(Action):
    def __init__(self):
        super().__init__("Race away from these lunatics")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 1,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

class PreachVariantCreed(Action):
    def __init__(self):
        super().__init__("Preach a variant creed")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(3, state.outfits.mithridacy)

class SignalSamaritan(Action):
    def __init__(self):
        super().__init__("Signal your experience on the Samaritan")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

class SendToFathomking(Action):
    def __init__(self):
        super().__init__("Send them down to the Fathomking's court")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.PiecesOfPlunder: random.randint(1, 3),
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(5, state.outfits.zeefaring)

################################################################################
###                          A Sighting of the (Bounty)                       ###
################################################################################

class SightingOfTheBounty(OpportunityCard):
    def __init__(self):
        super().__init__("A Sighting of the (Bounty)")
        self.actions = [FollowThatShip(), LetThemPass()]

class FollowThatShip(Action):
    def __init__(self):
        super().__init__("Follow that ship!")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ChasingDownYourBounty: random.randint(1, 5),
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5)
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(13, state.outfits.zeefaring)

class LetThemPass(Action):
    def __init__(self):
        super().__init__("Let them pass over the horizon")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 6,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5)
        }

################################################################################
###                             A Spit of Land                                ###
################################################################################

class SpitOfLand(OpportunityCard):
    def __init__(self):
        super().__init__("A Spit of Land")
        self.actions = [SteamOnBy(), StopAtIsland(), HeartsSuggestion()]

class SteamOnBy(Action):
    def __init__(self):
        super().__init__("Steam on by")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 1,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

class StopAtIsland(Action):
    def __init__(self):
        super().__init__("Stop briefly at the island")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge

class HeartsSuggestion(Action):
    def __init__(self):
        super().__init__("The Heart's suggestion")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -1,
            Item.TinOfZzoup: 1,
            Item.ZailingProgress: 75,
            Item.TimeSpentAtZee: 1
        }
    
################################################################################
###                             A Worrying Appetite                           ###
################################################################################    

class WorryingAppetite(OpportunityCard):
    def __init__(self):
        super().__init__("A Worrying Appetite")
        self.actions = [ScourHold(), YouTooHaveAnAppetite()]

class ScourHold(Action):
    def __init__(self):
        super().__init__("Scour the hold for anything edible")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -5
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.Nightmares: 8
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge

class YouTooHaveAnAppetite(Action):
    def __init__(self):
        super().__init__("You, too, have an appetite")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.UnaccountablyPeckish: 1,
            Item.Nightmares: 1,
            Item.RumblingStomachs: 0
        }

    
################################################################################
###                             Architect's Dream                 ###
################################################################################ 

class ArchitectsDream(OpportunityCard):
    def __init__(self):
        super().__init__("An Architect's Dream")
        self.actions = [HandHimAHammer(), AwakenFromDream()]

class HandHimAHammer(Action):
    def __init__(self):
        super().__init__("Hand him a hammer")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RosyColours: 4,
            Item.Nightmares: 2
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Nightmares: -3,
            Item.RosyColours: 0
        }
    
################################################################################
###                            BearingWitnessToPilgrimage               ###
################################################################################     

class BearingWitnessToPilgrimage(OpportunityCard):
    def __init__(self):
        super().__init__("Bearing Witness to a Pilgrimage")
        self.actions = [HailSteamship(), SteamOnBy()]

class HailSteamship(Action):
    def __init__(self):
        super().__init__("Hail a passing steamship")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RomanticNotion: 25,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

class SteamOnBy(Action):
    def __init__(self):
        super().__init__("Steam on by")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

################################################################################
###                            CorneringTheBounty          ###
################################################################################    

class CorneringTheBounty(OpportunityCard):
    def __init__(self):
        super().__init__("Cornering the (Bounty) at Last")
        self.actions = [StrikeThemDown(), CallOffApproach(), EngageStarvedVessel()]

class StrikeThemDown(Action):
    def __init__(self):
        super().__init__("Strike them down")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            # Item.AProlificPirate: 1,
            Item.PiecesOfPlunder: random.randint(1, 3)
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 12,
            # Item.AProlificPirate: 1,
            Item.PiecesOfPlunder: random.randint(1, 3),
            Item.UnwelcomeOnTheWaters: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(11, state.outfits.zeefaring)

class CallOffApproach(Action):
    def __init__(self):
        super().__init__("Call off the approach")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -7,
            Item.Wounds: 2,
            Item.ChasingDownYourBounty: 10
        }

# class PrepareToBoard(Action):
#     def __init__(self):
#         super().__init__("Prepare to board the Delight")

#     def pass_items(self, state: 'GameState'):
#         return {
#             Item.TroubledWaters: 0,
#             Item.AlmostTameBlueProphet: -1,
#             Item.WhirringContraption: -1
#         }

class EngageStarvedVessel(Action):
    def __init__(self):
        super().__init__("Engage the starved 'vessel'")

    def pass_items(self, state: 'GameState'):
        return {
            # Item.AProlificPirate: 1,
            Item.TroubledWaters: 3,
            Item.PiecesOfPlunder: random.randint(1, 3)
        }

    def fail_items(self, state: 'GameState'):
        return {
            # Item.AProlificPirate: 1,
            Item.TroubledWaters: 12,
            Item.PiecesOfPlunder: random.randint(1, 3)
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(11, state.outfits.zeefaring)


################################################################################
###                            Creaking from Above                            ###
################################################################################

class CreakingFromAbove(OpportunityCard):
    def __init__(self):
        super().__init__("Creaking from Above")
        self.actions = [GlimFall()]

class GlimFall(Action):
    def __init__(self):
        super().__init__("Glim-fall!")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.ShardOfGlim: 2 * state.region_data().peril,
            Item.SomeoneIsComing: 1,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 9,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.ShardOfGlim: state.region_data().peril // 3,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge


################################################################################
###                           Passing a Lightship                             ###
################################################################################

class PassingALightship(OpportunityCard):
    def __init__(self):
        super().__init__("Passing a Lightship")
        self.actions = [StopAndExchangeNews(), ZailOn(), StopForLead()]

class StopAndExchangeNews(Action):
    def __init__(self):
        super().__init__("Stop and exchange news")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZeeZtory: -7,
            Item.TaleOfTerror: random.randint(2, 10),
            Item.ScrapOfIncendiaryGossip: random.randint(1, 10)
        }

class ZailOn(Action):
    def __init__(self):
        super().__init__("Zail on")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

class StopForLead(Action):
    def __init__(self):
        super().__init__("Stop for lead")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 7,
            Item.UnwelcomeOnTheWaters: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }
    
    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(260, state.outfits.shadowy)    

################################################################################
###                            Rats in the Hold                               ###
################################################################################

class RatsInTheHold(OpportunityCard):
    def __init__(self):
        super().__init__("Rats in the Hold")
        self.actions = [NegotiateWithRats(), FillTheHoldWithTraps(), RatCatchingExpedition(), QuestionAboutShips()]

class NegotiateWithRats(Action):
    def __init__(self):
        super().__init__("Negotiate with them")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.CreepingFear: 1,
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }
    
    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.persuasive)    

class FillTheHoldWithTraps(Action):
    def __init__(self):
        super().__init__("Fill the hold with traps")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RatOnAString: 50,
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.MutinousWhispers: 1,
            Item.TimeSpentAtZee: 1
        }
    
    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.dangerous)    

class RatCatchingExpedition(Action):
    def __init__(self):
        super().__init__("Go on a rat-catching expedition")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RatOnAString: 100,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

class QuestionAboutShips(Action):
    def __init__(self):
        super().__init__("Question them about other ships")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 6,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }
    
    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(160, state.outfits.dangerous)    

################################################################################
###                           Signs of Disloyalty                             ###
################################################################################

class SignsOfDisloyalty(OpportunityCard):
    def __init__(self):
        super().__init__("Signs of Disloyalty")
        self.actions = [PrivateConversations(), DoubleTheirPay()]

class PrivateConversations(Action):
    def __init__(self):
        super().__init__("A few private conversations")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -5,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }
    
    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge    

class DoubleTheirPay(Action):
    def __init__(self):
        super().__init__("Double their pay")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,  # Set to calm seas
            Item.ShardOfGlim: -250,
            Item.MoonPearl: -250
        }

################################################################################
###                             Signs of Pursuit                              ###
################################################################################

class SignsOfPursuit(OpportunityCard):
    def __init__(self):
        super().__init__("Signs of Pursuit")
        self.actions = [TurnAroundAndConfront(), ThrowBaitOverboard()]

class TurnAroundAndConfront(Action):
    def __init__(self):
        super().__init__("Turn around and confront it")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -5,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,  # Reset troubled waters
            Item.ZailingProgress: -(2 * state.outfits.zailing_speed),  # Reset zailing progress
            Item.GroaningHull: 1,
            Item.SilentStalker: 0,  # Remove silent stalker
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(340, state.outfits.dangerous)

class ThrowBaitOverboard(Action):
    def __init__(self):
        super().__init__("Throw bait overboard")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.DeepZeeCatch: -10,
            Item.RumblingStomachs: 1
        }


################################################################################
###                          Spiralling Into Sorrow                           ###
################################################################################

# class SpirallingIntoSorrow(OpportunityCard):
#     def __init__(self):
#         super().__init__("Spiralling Into Sorrow")
#         self.actions = [DiveWithDivingBell()]

# class DiveWithDivingBell(Action):
#     def __init__(self):
#         super().__init__("Dive with the (diving-bell)")

#     def pass_items(self, state: 'GameState'):
#         return {
#             Item.TroubledWaters: 0,  # Reset troubled waters
#             Item.ShardOfGlim: 777,
#             # Item.AssociatingWithYouthfulNaturalist: 600
#         }

#     def perform_pass(self, state: 'GameState'):
#         # Specific pass actions to reset zailing states and move to a new area
#         state.items[Item.ZailingProgress] = 0
#         state.items[Item.ZailingSpeed] = 0
#         state.items[Item.ZeePeril] = 0
#         # Additional narrative changes could be added here


################################################################################
###                             Taking in Water                               ###
################################################################################

class TakingInWater(OpportunityCard):
    def __init__(self):
        super().__init__("Taking in Water")
        self.actions = [SealAndPump(), FieldRepairs()]

class SealAndPump(Action):
    def __init__(self):
        super().__init__("Seal the compartment and run the pumps")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed // 2
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.Wounds: 3
        }

    def pass_rate(self, state: 'GameState'):
        return 0.7  # 70% success chance

class FieldRepairs(Action):
    def __init__(self):
        super().__init__("Stop and make field repairs")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -7,
            Item.NevercoldBrassSliver: -500,
            # TODO
            # Item.GroaningHull: 0,  # Remove groaning hull damage
            Item.CreepingFear: 1
        }
    
################################################################################
###                         The Clinging Coral Mass                           ###
################################################################################

class TheClingingCoralMass(OpportunityCard):
    def __init__(self):
        super().__init__("The Clinging Coral Mass")
        self.actions = [PutYourBacksIntoIt(), GrabAHammer()]

class PutYourBacksIntoIt(Action):
    def __init__(self):
        super().__init__("Put your backs into it, lads!")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.MutinousWhispers: 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.persuasive)

class GrabAHammer(Action):
    def __init__(self):
        super().__init__("Grab a hammer yourself")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.MutinousWhispers: 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.dangerous)


################################################################################
###                            The Fleet of Truth                             ###
################################################################################

class TheFleetOfTruth(OpportunityCard):
    def __init__(self):
        super().__init__("The Fleet of Truth")
        self.actions = [Villainy(), Subterfuge(), EngagePeerReview()]
        #HatchPlans(), RendezvousWithScholars()]

class Villainy(Action):
    def __init__(self):
        super().__init__("Villainy!")

    def pass_items(self, state: 'GameState'):
        return {
            Item.PageOfCryptopalaeontologicalNotes: 5,
            Item.PageOfPrelapsarianArchaeologicalNotes: 5,
            Item.PageOfTheosophisticalNotes: 5,
            Item.TroubledWaters: 4,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.dangerous)

class Subterfuge(Action):
    def __init__(self):
        super().__init__("Subterfuge")

    def pass_items(self, state: 'GameState'):
        return {
            Item.PageOfCryptopalaeontologicalNotes: 7,
            Item.PageOfPrelapsarianArchaeologicalNotes: 7,
            Item.PageOfTheosophisticalNotes: 7,
            Item.TroubledWaters: 4,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.shadowy)

class EngagePeerReview(Action):
    def __init__(self):
        super().__init__("Engage in a little bit of 'peer review'")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.ChasingDownYourBounty: random.randint(1, 3),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.PageOfCryptopalaeontologicalNotes: 3,
            Item.PageOfPrelapsarianArchaeologicalNotes: 3,
            Item.PageOfTheosophisticalNotes: 3,
            Item.UnwelcomeOnTheWaters: 1,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(160, state.outfits.persuasive)

# class HatchPlans(Action):
#     def __init__(self):
#         super().__init__("Hatch plans with two Shifty Scholars")

#     def pass_items(self, state: 'GameState'):
#         return {
#             Item.OrganicComprehension: 7,
#             Item.TroubledWaters: 2,
#             Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random.randint(1, 5),
#             Item.TimeSpentAtZee: 1
#         }

# class RendezvousWithScholars(Action):
#     def __init__(self):
#         super().__init__("Rendezvous with two Shifty Scholars")

#     def pass_items(self, state: 'GameState'):
#         return {
#             Item.SilentStalker: 1,
#             Item.OrganicComprehension: 10,
#             Item.AssociatingWithYouthfulNaturalist: 10,
#             Item.UnearthlyFossil: 10,
#             Item.TroubledWaters: 2,
#             Item.ZailingProgress: (state.outfits.zailing_speed // 2),
#             Item.TimeSpentAtZee: 1
#         }


################################################################################
###                            The Killing Wind                               ###
################################################################################

class TheKillingWind(OpportunityCard):
    def __init__(self):
        super().__init__("The Killing Wind")
        self.actions = [OutrunStorm(), MakeReadyToDive(), ChartStormCourse()]

class OutrunStorm(Action):
    def __init__(self):
        super().__init__("Outrun the storm front")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.CreepingFear: 1,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 12,
            Item.CreepingFear: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge

class MakeReadyToDive(Action):
    def __init__(self):
        super().__init__("Make ready to dive")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ZeeZtory: random.randint(3, 6),
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

class ChartStormCourse(Action):
    def __init__(self):
        super().__init__("Chart a course through the storm using your Storm in a Teacup")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.ZeeZtory: 2,
            Item.TroubledWaters: random.randint(1, 4),
            Item.CreepingFear: 1,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: random.randint(5, 10),
            Item.CreepingFear: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge


################################################################################
###                       What do the Drownies Sing?                          ###
################################################################################

class WhatDoTheDrowniesSing(OpportunityCard):
    def __init__(self):
        super().__init__("What do the Drownies Sing?")
        self.actions = [KeepCrewFromListening(), DrownOutDrownies(), CureIgnorance(), ListenForQuarry()]

class KeepCrewFromListening(Action):
    def __init__(self):
        super().__init__("Keep the crew from listening")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 9,
            Item.CreepingFear: 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.persuasive)

class DrownOutDrownies(Action):
    def __init__(self):
        super().__init__("Drown out the drownies")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 9,
            Item.GroaningHull: 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.dangerous)

class CureIgnorance(Action):
    def __init__(self):
        super().__init__("Cure the ignorance of your zailors")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TroubledWaters: -5,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 12,
            Item.CreepingFear: 1,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(3, state.outfits.kataleptic_toxicology)

class ListenForQuarry(Action):
    def __init__(self):
        super().__init__("Listen to the songs, and for your quarry")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ChasingDownYourBounty: random.randint(1, 3),
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 6,
            Item.Nightmares: 4,
            Item.SilentStalker: 1,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(13, state.outfits.monstrous_anatomy)


################################################################################
###                        When the Carousing Stops                           ###
################################################################################

class WhenTheCarousingStops(OpportunityCard):
    def __init__(self):
        super().__init__("When the Carousing Stops")
        self.actions = [DisciplineCrew(), RestartParty()]

class DisciplineCrew(Action):
    def __init__(self):
        super().__init__("Discipline your crew")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.MutinousWhispers: 1,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.dangerous)

class RestartParty(Action):
    def __init__(self):
        super().__init__("Restart the party")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.PiecesOfPlunder: random.randint(1, 3),
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1,
            Item.BottleOfBrokenGiant1844: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.MutinousWhispers: 1,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(160, state.outfits.persuasive)


################################################################################
###                             Your False-Star                               ###
################################################################################

class YourFalseStar(OpportunityCard):
    def __init__(self):
        super().__init__("Your False-Star")
        self.actions = [NavigateByStar()]

class NavigateByStar(Action):
    def __init__(self):
        super().__init__("Navigate by the light of your star")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -5,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

################################################################################
###                             Zeeborne Pariahs                            ###
################################################################################

class ZeebornePariahs(OpportunityCard):
    def __init__(self):
        super().__init__("Zeeborne Pariahs")
        self.actions = [EvadeThem(), DisguiseShip()]

class EvadeThem(Action):
    def __init__(self):
        super().__init__("Evade them!")

    def pass_rate(self, state: 'GameState'):
        return 0.7  # Pretty good odds, 70% success chance

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,  # Estimated CP increase
            Item.Wounds: 4,
            Item.TimeSpentAtZee: 1
        }

class DisguiseShip(Action):
    def __init__(self):
        super().__init__("Put your crew to work disguising the ship")

    def pass_items(self, state: 'GameState'):
        return {
            Item.InklingOfIdentity: -50,
            Item.TroubledWaters: -7,
            Item.UnwelcomeOnTheWaters: 0,  # Removes all Unwelcome on the Waters
            Item.MutinousWhispers: 1  # Sets Mutinous Whispers to 1
        }


################################################################################
###                       A Steamer full of Passengers                        ###
################################################################################

class ASteamerFullOfPassengers(OpportunityCard):
    def __init__(self):
        super().__init__("A Steamer full of Passengers")
        self.actions = [SteamPast(), InviteAboard(), RecogniseQuarry(), RobThemBlind()]

class SteamPast(Action):
    def __init__(self):
        super().__init__("Steam past them")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TroubledWaters: 2
        }

class InviteAboard(Action):
    def __init__(self):
        super().__init__("Invite them aboard for a party")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Scandal: 2,
            Item.Hedonist: 3,
            Item.ScarletStockings: 1,
            Item.SecludedAddress: 6,
            # Item.Austere: -3
        }

class RecogniseQuarry(Action):
    def __init__(self):
        super().__init__("Recognise your quarry")

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(100, state.outfits.dangerous)

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.PieceOfRostygold: 250,
            Item.ZailingProgress: state.outfits.zailing_speed,
        }

class RobThemBlind(Action):
    def __init__(self):
        super().__init__("Rob them blind")

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(160, state.outfits.dangerous)

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.PiecesOfPlunder: 300,
            Item.ZailingProgress: state.outfits.zailing_speed,
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.UnwelcomeOnTheWaters: 1
        }

################################################################################
###                             A Corsair Galley                              ###
################################################################################

class ACorsairGalley(OpportunityCard):
    def __init__(self):
        super().__init__("A Corsair Galley")
        self.actions = [FullSteamAhead(), FireWarningShot(), FightBack()]

class FullSteamAhead(Action):
    def __init__(self):
        super().__init__("Full steam ahead!")

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(45, state.outfits.zailing_speed)

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TroubledWaters: 3
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.GroaningHull: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
        }

class FireWarningShot(Action):
    def __init__(self):
        super().__init__("Fire a warning shot")

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(110, state.outfits.dangerous)

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TroubledWaters: 2
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 12,
            Item.GroaningHull: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
        }

class FightBack(Action):
    def __init__(self):
        super().__init__("Fight back!")

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(6, state.outfits.artisan_of_the_red_science)

    def pass_items(self, state: 'GameState'):
        return {
            Item.PiecesOfPlunder: 300,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TroubledWaters: 4
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.ZailingProgress: state.outfits.zailing_speed // 4 + random.randint(1, 5),
            Item.UnwelcomeOnTheWaters: 1
        }

################################################################################
###                             She's Going Down!                             ###
################################################################################

class ShesGoingDown(OpportunityCard):
    def __init__(self):
        super().__init__("She's Going Down!")
        self.actions = [StopAndRescue(), LetUnterzeeHaveThem(), LootTheWreckage()]

class StopAndRescue(Action):
    def __init__(self):
        super().__init__("Stop and rescue them")

    def pass_items(self, state: 'GameState'):
        return {
            # Item.Steadfast: 3,
            # Item.Heartless: -3,
            Item.TroubledWaters: -2
        }

class LetUnterzeeHaveThem(Action):
    def __init__(self):
        super().__init__("Let the Unterzee have them")

    def pass_items(self, state: 'GameState'):
        return {
            # Item.Heartless: 3,
            # Item.Magnanimous: -3,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TroubledWaters: 1,
            Item.TimeSpentAtZee: 1
        }

class LootTheWreckage(Action):
    def __init__(self):
        super().__init__("Loot the wreckage")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.PiecesOfPlunder: 250,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.CreepingFear: 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(5, state.outfits.zeefaring)


cards = [
    BountyUponYourHead(),
    BlankSpaceOnTheCharts(),
    CorvetteOfHerMajestysNavy(),
    CorvetteWithCorsairColours(),
    # TODO draw conditions
    # DreamOfACup(),
    # DreamOfATable(),
    # DreamOfAscent(),
    # DreamOfDesigns(),
    # DreamOfStainedGlass(),
    DreamOfSunbeams(),
    FlockOfProphets(),
    GiantAnglerCrab(),
    GrowingConcern(),
    HugeTerribleBeast(),
    # TODO complicated card
    # MessageInABottle(),
    NavigationError(),
    PromisingWreck(),
    RagtagFlotilla(),
    ShipOfZealots(),
    SightingOfTheBounty(),
    SpitOfLand(),
    WorryingAppetite(),
    ArchitectsDream(),
    BearingWitnessToPilgrimage(),
    CorneringTheBounty(),
    CreakingFromAbove(),
    PassingALightship(),
    RatsInTheHold(),
    SignsOfDisloyalty(),
    SignsOfPursuit(),
    # SpirallingIntoSorrow(), # One-time story card
    TakingInWater(),
    TheClingingCoralMass(),
    TheFleetOfTruth(),
    TheKillingWind(),
    WhatDoTheDrowniesSing(),
    WhenTheCarousingStops(),
    YourFalseStar(),
    ASteamerFullOfPassengers(),
    ShesGoingDown(),
    ACorsairGalley(),

]

# Initial setup
def setup_simulation():
    state = GameState()

    # Add each card to the deck
    for card in cards:
        state.deck.append(card)

    return state

# Helper function to truncate long strings
def truncate_string(s, length=25):
    if len(s) > length:
        return s[:length - 3] + '...'  # Truncate and add ellipsis
    return s

# Print the action table with condensed card/action info
def print_condensed_action_table(action_play_counts, action_success_counts, action_failure_counts, card_draw_counts, card_play_counts, deck, runs, name_length=25):
    print(f"\n{'Card/Action':<30}{'Played/Drawn':<20}{'Draw/Play %':<15}{'Avg Plays/Run':<15}{'Success Rate':<15}")
    print("-" * 105)
    
    for card in deck:
        card_name = truncate_string(card.name, name_length)
        drawn = card_draw_counts.get(card.name, 0) / runs
        played = card_play_counts.get(card.name, 0) / runs
        play_rate = (card_play_counts.get(card.name, 0) / card_draw_counts.get(card.name, 1)) * 100 if card_draw_counts.get(card.name, 0) > 0 else 0

        # First row for card drawn/played info
        print(f"{card_name:<30}{f'{played:.2f}/{drawn:.2f}':<20}{play_rate:<15.2f}")

        # Next rows for action info (for each action in the card)
        for action in card.actions:
            action_name = truncate_string(action.name, name_length)
            action_played = action_play_counts.get(action.name, 0) / runs
            successes = action_success_counts.get(action.name, 0)
            failures = action_failure_counts.get(action.name, 0)
            total = successes + failures
            success_rate = (successes / total) * 100 if total > 0 else 0
            # Action rows indented under the card row
            print(f"{'':<30}{action_name:<30}{'':<15}{action_played:<15.2f}{success_rate:.2f}%")

        print("-" * 105)

# Print the average change in items per run
def print_item_summary(total_item_changes, runs):
    print(f"\n{'Item':<30}{'Avg Change/Run':<15}")
    print("-" * 45)
    for item, total_change in total_item_changes.items():
        avg_change = total_change / runs
        if avg_change != 0.0:
            print(f"{item.name:<30}{avg_change:<15.2f}")

# Update progress bar function
def update_progress(progress):
    bar_length = 40
    block = int(round(bar_length * progress))
    text = f"\rProgress: [{'#' * block + '-' * (bar_length - block)}] {progress * 100:.2f}%"
    sys.stdout.write(text)
    sys.stdout.flush()


def run_simulation(runs: int):
    state = setup_simulation()  # Assuming setup_simulation initializes the deck
    for i in range(runs):
        state.run()  # Run each simulation for 80 progress
        state.update_item_totals()  # Collect total changes in items
        state.reset()  # Reset the state for the next run
        update_progress((i + 1) / runs)  # Update the progress bar

    state.display_results(runs)

# Now execute multiple runs:
if __name__ == "__main__":
    run_simulation(runs=1000)  # Run for 1000 separate simulations
