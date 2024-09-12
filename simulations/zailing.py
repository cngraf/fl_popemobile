import random
import sys
from collections import defaultdict
from enum import Enum, auto
from enums import *
from collections import defaultdict

item_echo_values = {
    Item.Plunder: 0.01,
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

class GameState:
    def __init__(self):
        self.outfits = OutfitList()

        self.items = {
            Item.TroubledWaters: 0,
            Item.CreepingFear: 0,

            Item.Plunder: 0,
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
            Item.Plunder: random.randint(1, 3),
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

    def pass_ev(self, state: 'GameState'):
        return 5  # Placeholder for actual EV

    def failure_ev(self, state: 'GameState'):
        return -10  # Placeholder for actual EV

class SignalRamillies(Action):
    def __init__(self):
        super().__init__("Signal the HMS Ramillies for Support")
    
    def pass_rate(self, state: 'GameState'):
        # Narrow challenge, Zeefaring 11 (50% base)
        return self.narrow_pass_rate(11, state.outfits.zeefaring)

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.Plunder: random.randint(1, 2),
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

    def pass_ev(self, state: 'GameState'):
        return 5  # Placeholder for actual EV

    def failure_ev(self, state: 'GameState'):
        return -10  # Placeholder for actual EV

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

    def pass_ev(self, state: 'GameState'):
        return 3  # Placeholder for actual EV

    def failure_ev(self, state: 'GameState'):
        return -8  # Placeholder for actual EV

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
            Item.Plunder: random.randint(1, 3),
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
###                            DreamOfSunbeams                                ###
################################################################################
################################################################################
###                            DreamOfSunbeams                                ###
################################################################################
################################################################################
###                            DreamOfSunbeams                                ###
################################################################################
################################################################################
###                            DreamOfSunbeams                                ###
################################################################################
################################################################################
###                            DreamOfSunbeams                                ###
################################################################################



cards = [
    BountyUponYourHead(),
    BlankSpaceOnTheCharts(),
    CorvetteOfHerMajestysNavy(),
    CorvetteWithCorsairColours(),
    DreamOfACup(),
    DreamOfATable(),
    DreamOfAscent(),
    DreamOfDesigns(),
    DreamOfStainedGlass(),
    DreamOfSunbeams(),
    FlockOfProphets(),
    GiantAnglerCrab(),
    GrowingConcern()
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
