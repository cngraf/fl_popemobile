import random
import sys
import math
from collections import defaultdict
from enum import Enum, auto
from collections import defaultdict

from enums import *
from decks.unterzee import *

item_echo_values = {
    Item.PiecesOfPlunder: 0.01,
    Item.WhirringContraption: 12.5,
    Item.MapScrap: 0.1,
    Item.AppallingSecret: 0.15,
    Item.TaleOfTerror: 0.5,
    Item.MemoryOfDistantShores: 0.5,
    Item.MemoryOfLight: 0.5,
    Item.ZeeZtory: 0.5,

    Item.BottleOfBrokenGiant1844: 2.5,

    # Menaces
    Item.Wounds: -0.2,
    Item.Nightmares: -0.2
}

# HACK may god forgive me
# for estimating EV of the random extra zailing from certain actions
# that occasionally makes the difference of an action
# maybe define a separate item for this or something idk
zailing_bonus_estimate = 0
comparison_mode = False
def random_zailing_bonus():
    if comparison_mode:
        return zailing_bonus_estimate
    else:
        # return random.randint(1, 5)
        return 0

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
            ev_from_item = state.ev_from_item(item, amount)
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
        self.zubmersibility = 0
        self.luxurious = 0

        self.dangerous = 300
        self.watchful = 300
        self.persuasive = 300
        self.shadowy = 300

        self.player_of_chess = 15
        self.zeefaring = 15
        self.monstrous_anatomy = 15
        self.mithridacy = 15
        self.artisan_of_the_red_science = 15
        self.kataleptic_toxicology = 15
        self.shapeling_arts = 15

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

        self.progress_required = 180
        self.piracy_enabled = True

        # Initialize cards in the deck
        self.deck = []  # This will be populated with cards
        self.hand = []

        self.actions = 0
        self.total_actions = 0  # Accumulates actions over all runs
        self.region_action_counts = defaultdict(int)

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

        self.current_region = ZeeRegion.HOME_WATERS
        self.next_region = ZeeRegion.SHEPHERDS_WASH
        self.route_progress = 0
        self.route = [
            (ZeeRegion.HOME_WATERS, ZeeRegion.SHEPHERDS_WASH)
        ]

    def region_data(self):
        return zee_regions[self.current_region]

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

        # TODO check how many actions this takes.
        # I guess you could be pirating without a bounty too
        if self.piracy_enabled and self.items[Item.ChasingDownYourBounty] < 1:
            self.region_action_counts[self.current_region] += 1
            self.actions += 1
            self.items[Item.ChasingDownYourBounty] = 1

        best_card, best_action, best_action_ev = None, None, -float('inf')

        comparison_mode = True
        for card in self.hand:
            for action in card.actions:
                if action.can_perform(self):
                    action_ev = 0
                    for i in range(1,6):
                        zailing_bonus_estimate = i
                        action_ev += action.ev(self)
                    action_ev /= 5.0
                    if action_ev > best_action_ev:
                        best_card, best_action, best_action_ev = card, action, action_ev
        comparison_mode = False

        # for card in self.hand:
        #     for action in card.actions:
        #         if action.can_perform(self):
        #             attempts = 25
        #             action_ev = sum(action.ev(self) for _ in range(attempts)) / attempts
        #             if action_ev > best_action_ev:
        #                 best_card, best_action, best_action_ev = card, action, action_ev

        if best_action:
            outcome = best_action.perform(self)
            self.action_play_counts[best_action.name] += 1
            self.actions += best_action.action_cost
            self.region_action_counts[self.current_region] += best_action.action_cost

            if outcome == "Success":
                self.action_success_counts[best_action.name] += 1
            else:
                self.action_failure_counts[best_action.name] += 1

        if best_card is not None:
            self.card_play_counts[best_card.name] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)            

        if self.items[Item.TroubledWaters] >= 36:
            self.status = "Failure"
        elif self.items[Item.ZailingProgress] >= self.progress_required:
            self.go_to_next_region()

        self.hand = [card for card in self.hand if card.can_draw(self)]



    def run(self):
        # self.items[Item.ZailingProgress] = 0  # Reset progress for each run
        # while self.items[Item.ZailingProgress] < 80:
        while self.status == "InProgress":
            self.step()

        # self.total_actions += self.actions  # Accumulate total actions after the run


    def go_to_next_region(self):
        self.route_progress += 1
        self.items[Item.ZailingProgress] = 0

        if self.route_progress >= len(self.route):
            self.status = "Success" 
        else:
            self.current_region, self.next_region = self.route[self.route_progress]
            if self.current_region == self.next_region:
                self.progress_required = 80
            else:
                self.progress_required = zee_regions[self.current_region].distance_to[self.next_region]


    # def update_item_totals(self):
        # for item, count in self.items.items():
        #     self.total_item_changes[item] += count

    # def reset(self):
    #     """Reset relevant parts of the game state but keep the deck and stats."""
    #     # self.items = {item: 0 for item in Item}
    #     self.hand = []
    #     self.items[Item.ZailingProgress] = 0 
    #     self.items[Item.TroubledWaters] = 0

    # def reach_port(self, clear_tw = True):
    #     self.items[Item.ZailingProgress] = 0
    #     if clear_tw:
    #         self.items[Item.TroubledWaters] = 

        # Optionally, display other tracking metrics if needed

    def ev_from_item(self, item: Item, val: int):
        if item == Item.ZailingProgress:
            return self.progress_ev(val)
        elif item == Item.TroubledWaters:
            return self.tw_ev(val)
        elif item == Item.ChasingDownYourBounty:
            return val * 12/53
        else:
            echo_value = item_echo_values.get(item, 0)
            # TODO echo value
            return echo_value * val

    def progress_ev(self, val: int):
        """Calculates the EV for a given progress value based on current progress."""
        # TODO
        prog_unit_ev = 0.05
        action_ev = 5.5

        # Current progress
        speed = self.outfits.zailing_speed
        current_progress = self.items.get(Item.ZailingProgress, 0)
        remaining_progress = max(0, self.progress_required - current_progress)

        current_remaining_actions = math.ceil(remaining_progress / speed)
        next_remaining_actions = math.ceil((remaining_progress - val) / speed)
        action_diff = current_remaining_actions - next_remaining_actions

        if remaining_progress <= 0:
            return 0.0
        elif action_diff > 0:
            return action_ev * action_diff
        # elif remaining_progress <= (val + zailing_speed):
        #     return baseline_ev
        else:
            return val * prog_unit_ev
    
    def tw_ev(self, val: int):
        # TODO
        tw_unit_ev = -0.2
        failure_threshold = 36

        current_tw = self.items.get(Item.TroubledWaters, 0)
        if current_tw + val >= failure_threshold:
            return -10000
        elif current_tw > 10 and current_tw + val >= 10:
            return (tw_unit_ev * 2) * val
        
        # TODO other threshold, for rank 7?

        else:
            return tw_unit_ev * val


################################################################################
################################################################################

class BlankSpaceOnTheCharts(OpportunityCard):
    def __init__(self):
        super().__init__("A Blank Space on the Charts")
        self.actions = [TheresAnIslandHere(), FortuitousFragments(), SearchUnchartedWaters()]
        self.weight = 0.8

    def can_draw(self, state: GameState):
        return state.items[Item.TroubledWaters] >= 28 and \
            state.items[Item.ZailingProgress] >= 60

class TheresAnIslandHere(Action):
    def __init__(self):
        super().__init__("There's an island here")

    def pass_items(self, state: 'GameState'):
        return {
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0),
            Item.TroubledWaters: -5
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0),
            Item.Nightmares: 3,
            Item.ZailingProgress: -60,
            Item.TroubledWaters: 4
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge

class FortuitousFragments(Action):
    def __init__(self):
        super().__init__("Fortuitous fragments")

    # TODO requires 2 partial map

    def pass_items(self, state: 'GameState'):
        # Sets TW to level 5 aka 15 CP
        tw = state.items[Item.TroubledWaters]
        return {
            Item.TroubledWaters: 15 - tw,
            Item.PartialMap: -2
        }

    def can_perform(self, state: 'GameState'):
        return state.items.get(Item.PartialMap, 0) >= 2  # Requires 2 Partial Maps

class SearchUnchartedWaters(Action):
    def __init__(self):
        super().__init__("Search the uncharted waters for your quarry")

    def can_perform(self, state: GameState):
        return state.piracy_enabled and state.items[Item.ChasingDownYourBounty] > 0

    # TODO rare success
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -1,
            Item.ChasingDownYourBounty: state.region_data().chasing_gain_advanced,
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -5,
            Item.CreepingFear: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)
    
################################################################################
###                          BountyUponYourHead                               ###
################################################################################

class BountyUponYourHead(OpportunityCard):
    def __init__(self):
        super().__init__("A Bounty Upon Your Head", 1.0)
        self.actions = [OpenFire(), SignalRamillies(), EvadeThem()]

    def can_draw(self, state: GameState):
        return state.piracy_enabled and state.items[Item.ChasingDownYourBounty] > 0

class OpenFire(Action):
    def __init__(self):
        super().__init__("Open Fire!")
    
    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)

    # TODO rare success
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.PiecesOfPlunder: state.region_data().plunder_gain_advanced,
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

    # TODO unlock req, rare success
    
    def pass_rate(self, state: 'GameState'):
        # TODO confirm DC
        dc = state.region_data().dc_advanced - 2
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.PiecesOfPlunder: state.region_data().plunder_gain_advanced - 100,
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
            Item.ZailingProgress: state.outfits.zailing_speed  + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed  + random_zailing_bonus(),
            Item.UnwelcomeOnTheWaters: 1
        }

################################################################################

class CorvetteOfHerMajestysNavy(OpportunityCard):
    def __init__(self):
        super().__init__("A Corvette of Her Majesty's Navy")
        self.actions = [ExchangePleasantries(), TheyreNotSlowing(), RelyOnOldCodes()]

    def can_draw(self, state: GameState):
        return state.piracy_enabled == False

class ExchangePleasantries(Action):
    def __init__(self):
        super().__init__("Exchange pleasantries via semaphore")

    def can_perform(self, state: GameState):
        return state.items[Item.Suspicion] < 15
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus()
        }

class TheyreNotSlowing(Action):
    def __init__(self):
        super().__init__("They're not slowing")

    def can_perform(self, state: GameState):
        return state.items[Item.Suspicion] >= 15

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

    # TODO requires special companion

    def pass_items(self, state: 'GameState'):
        return {
            Item.Suspicion: -3,
            Item.TroubledWaters: -random.randint(2, 8), # TODO unknown value
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.Suspicion: 4,
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.player_of_chess)

################################################################################


class CorvetteWithCorsairColours(OpportunityCard):
    def __init__(self):
        super().__init__("A Corvette of Her Majesty's Navy (with Corsair's Colours)")
        self.actions = [ExchangeInfo(), TakeThemForAll(), TheyreNotSlowing()]

    def can_draw(self, state: GameState):
        return state.piracy_enabled

class ExchangeInfo(Action):
    def __init__(self):
        super().__init__("Exchange information via semaphore")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ChasingDownYourBounty: state.region_data().chasing_gain_basic,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus()
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 6,
            Item.Suspicion: 2,
            Item.UnwelcomeOnTheWaters: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random_zailing_bonus()
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_basic
        return self.broad_pass_rate(dc, state.outfits.persuasive)

class TakeThemForAll(Action):
    def __init__(self):
        super().__init__("Take them for all they've got")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Suspicion: 1,
            Item.TroubledWaters: 4,
            Item.PiecesOfPlunder: state.region_data().plunder_gain_advanced,
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
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)

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

# TODO hand-check all the dream cards

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

    def can_draw(self, state: GameState):
        return state.piracy_enabled

# TODO rare success
class TakeAuspices(Action):
    def __init__(self):
        super().__init__("Take auspices")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ChasingDownYourBounty: state.region_data().chasing_gain_advanced,
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
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)

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
        self.actions = [FullReverse(), ReadyGuns(), HarpoonRamming()]
        self.weight = 0.8

class FullReverse(Action):
    def __init__(self):
        super().__init__("Full reverse! Turn us away!")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.SilentStalker: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().peril * 0.8
        return self.broad_pass_rate(dc, state.outfits.shadowy)

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
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.monstrous_anatomy)

# Only when hunting crab
# class PursueIt(Action):
#     def __init__(self):
#         super().__init__("Pursue it to its spawning grounds")
    
#     def pass_items(self, state: 'GameState'):
#         return {
#             Item.ZailingProgress: int(state.outfits.zailing_speed * 1.2),
#             Item.TimeSpentAtZee: 1
#         }

#     def fail_items(self, state: 'GameState'):
#         return {
#             Item.TroubledWaters: 2,
#             Item.ZailingProgress: state.outfits.zailing_speed // 2
#         }

#     def pass_rate(self, state: 'GameState'):
#         return self.broad_pass_rate(75, state.outfits.shadowy)

class HarpoonRamming(Action):
    def __init__(self):
        super().__init__("Reach for your harpoon; call for ramming speed!")

    def can_perform(self, state: GameState):
        # TODO: requires Monster Hunter
        return state.items.get(Item.NotchedBoneHarpoon, 0) > 0
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.DeepZeeCatch: 5,
            Item.TroubledWaters: 1,
            Item.RumblingStomachs: -1 * state.items.get(Item.RumblingStomachs, 0)
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
        # HACK for high urgency
        self.weight = 1_000_000.0

    def can_draw(self, state: GameState):
        tw = state.items[Item.TroubledWaters]
        return tw >= 28 and state.items[Item.CreepingFear] > 0

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
            # Sets to level 5
            Item.TroubledWaters: 15 - state.items[Item.TroubledWaters]
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # Luck challenge

class DoubleZailorsRations(Action):
    def __init__(self):
        super().__init__("Double the zailors' rations")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 15 - state.items.get(Item.TroubledWaters, 0),
            Item.CrateOfIncorruptibleBiscuits: -1,
            Item.FoxfireCandleStub: -100,
            Item.BottleOfGreyfields1882: -100,
            Item.RumblingStomachs: 1 - state.items.get(Item.RumblingStomachs, 0)
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
        self.actions = [DeliciousLumps(), SteamOnByBeast()]
        self.weight = 0.8

class DeliciousLumps(Action):
    def __init__(self):
        super().__init__("Delicious, delicious lumps")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.AppallingSecret: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.UnaccountablyPeckish: 1,
            Item.SomeoneIsComing: 1,
            Item.TaleOfTerror: 4,
            Item.RumblingStomachs: 1 - state.items.get(Item.RumblingStomachs, 0),  # Set Rumbling Stomachs to 1
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.RumblingStomachs: 1  # Set Rumbling Stomachs to 1
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().peril
        return self.broad_pass_rate(dc, state.outfits.dangerous)

class SteamOnByBeast(Action):
    def __init__(self):
        super().__init__("Steam on by")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.SilentStalker: 1 - state.items.get(Item.SilentStalker, 0),
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
        self.weight = 0.5

    def can_draw(self, state: GameState):
        return state.items[Item.DirectionsToAHiddenStash] == 0

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
        self.actions = [CorrectYourCourse(), ListenToTheZee(),
                        StarvedMen(),
                        LetYourStarGuide(), UseDisorientation()]

class CorrectYourCourse(Action):
    def __init__(self):
        super().__init__("Correct your course")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.MapScrap: 10,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().peril
        return self.broad_pass_rate(dc, state.outfits.watchful)

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
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)

class StarvedMen(Action):
    def __init__(self):
        super().__init__("Consider what you learned from the Starved Men")

    # TODO FATE-locked
    def can_perform(self, state: GameState):
        return False
    
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
    
    def can_perform(self, state: GameState):
        return state.items.get(Item.FalseStarOfYourOwn, 0) > 0

    def pass_items(self, state: 'GameState'):
        tw = state.items[Item.TroubledWaters]
        return {
            Item.TroubledWaters: max(-5, -1 * tw),
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().peril, state.outfits.persuasive)

class UseDisorientation(Action):
    def __init__(self):
        super().__init__("Use your disorientation to your advantage")

    def can_perform(self, state: GameState):
        return state.piracy_enabled
    
    # TODO rare success
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: random.randint(2, 3),
            Item.ChasingDownYourBounty: state.region_data().chasing_gain_advanced,
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
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)

################################################################################
###                            PromisingWreck                                ###
################################################################################

class PromisingWreck(OpportunityCard):
    def __init__(self):
        super().__init__("A Promising Wreck")
        self.actions = [DiveForSalvage(), ZailOnBy()]

    def can_draw(self, state: GameState):
        return state.piracy_enabled

class DiveForSalvage(Action):
    def __init__(self):
        super().__init__("Dive for salvage")
    
    # TODO rare success
    def pass_items(self, state: 'GameState'):
        bonus = 1 if state.outfits.zubmersibility > 0 else 0

        return {
            Item.TroubledWaters: 2,
            Item.PiecesOfPlunder: state.region_data().plunder_gain_advanced,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1,
            Item.UnprovenancedArtefact: bonus
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.CreepingFear: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)
    
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

# TODO: Only with lifeberg hunt

class RagtagFlotilla(OpportunityCard):
    def __init__(self):
        super().__init__("A Ragtag Flotilla")
        self.actions = [HailAShip(), SteamOnByFlotilla()]

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

class SteamOnByFlotilla(Action):
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
        self.actions = [SeeThemOff(), RaceAway(),
                        PreachVariantCreed(),
                        # SignalSamaritan(),
                        SendToFathomking()]

    def can_draw(self, state: GameState):
        tw = state.items[Item.TroubledWaters]
        return tw >= 10

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
        return self.broad_pass_rate(state.region_data().peril, state.outfits.dangerous)

class RaceAway(Action):
    def __init__(self):
        super().__init__("Race away from these lunatics")

    def can_perform(self, state: GameState):
        return state.outfits.zailing_speed >= 75
    
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
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.mithridacy)
    
class SignalSamaritan(Action):
    def __init__(self):
        super().__init__("Signal your experience on the Samaritan")

    # FATE-locked
    def can_perform(self, state: GameState):
        return False
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

class SendToFathomking(Action):
    def __init__(self):
        super().__init__("Send them down to the Fathomking's court")

    def can_perform(self, state: GameState):
        return state.piracy_enabled
    
    # TODO rare success
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.PiecesOfPlunder: state.region_data().plunder_gain_advanced,
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
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)

################################################################################
###                          A Sighting of the (Bounty)                       ###
################################################################################

class SightingOfTheBounty(OpportunityCard):
    def __init__(self):
        super().__init__("A Sighting of the (Bounty)")
        self.actions = [FollowThatShip(), LetThemPass()]

    def can_draw(self, state: GameState):
        return state.piracy_enabled

class FollowThatShip(Action):
    def __init__(self):
        super().__init__("Follow that ship!")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ChasingDownYourBounty: state.region_data().chasing_gain_advanced,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random_zailing_bonus()
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)
    
class LetThemPass(Action):
    def __init__(self):
        super().__init__("Let them pass over the horizon")
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 6,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus()
        }

################################################################################
###                             A Spit of Land                                ###
################################################################################

class SpitOfLand(OpportunityCard):
    def __init__(self):
        super().__init__("A Spit of Land")
        self.actions = [SteamOnBySpit(), StopAtIsland(), HeartsSuggestion()]
        self.weight = 0.8

class SteamOnBySpit(Action):
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

    # TODO requires Cladery Heart ship
    def can_perform(self, state: GameState):
        return False

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
        self.weight = 1_000_000 # HACK high urgency

    def can_draw(self, state: GameState):
        tw = state.items[Item.TroubledWaters]
        return tw >= 28 and state.items.get(Item.RumblingStomachs, 0) > 0

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
    
    def can_perform(self, state: GameState):
        return state.items[Item.UnaccountablyPeckish] > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.UnaccountablyPeckish: 1,
            Item.Nightmares: 1,
            Item.RumblingStomachs: -1 * state.items[Item.RumblingStomachs]
        }

    
################################################################################
###                             Architect's Dream                 ###
################################################################################ 

# TODO dream card

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

# TODO: hand-chec this card. midnight whale WQ
class BearingWitnessToPilgrimage(OpportunityCard):
    def __init__(self):
        super().__init__("Bearing Witness to a Pilgrimage")
        self.actions = [HailSteamship(), SteamOnByPilgrimage()]

class HailSteamship(Action):
    def __init__(self):
        super().__init__("Hail a passing steamship")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RomanticNotion: 25,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

class SteamOnByPilgrimage(Action):
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
        self.actions = [StrikeThemDown(), CallOffApproach()]
        self.weight = 1_000_000 # HACK high urgency

    def can_draw(self, state: GameState):
        return state.items[Item.ChasingDownYourBounty] >= 120

class StrikeThemDown(Action):
    def __init__(self):
        super().__init__("Strike them down")

    def pass_items(self, state: 'GameState'):
        return {
            # Item.AProlificPirate: 1,
            Item.TroubledWaters: 3,
            Item.ChasingDownYourBounty: -1 * state.items[Item.ChasingDownYourBounty],
            Item.PiecesOfPlunder: state.region_data().bounty
        }

    def fail_items(self, state: 'GameState'):
        return {
            # Item.AProlificPirate: 1,
            Item.TroubledWaters: 12,
            Item.ChasingDownYourBounty: -1 * state.items[Item.ChasingDownYourBounty],
            Item.PiecesOfPlunder: state.region_data().bounty,
            Item.UnwelcomeOnTheWaters: 1
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)
    
class CallOffApproach(Action):
    def __init__(self):
        super().__init__("Call off the approach")

    # TODO check values
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -7,
            Item.Wounds: 2,
            Item.ChasingDownYourBounty: 110 - state.items[Item.ChasingDownYourBounty]
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

# class EngageStarvedVessel(Action):
#     def __init__(self):
#         super().__init__("Engage the starved 'vessel'")

#     def pass_items(self, state: 'GameState'):
#         return {
#             # Item.AProlificPirate: 1,
#             Item.TroubledWaters: 3,
#             Item.PiecesOfPlunder: random.randint(1, 3)
#         }

#     def fail_items(self, state: 'GameState'):
#         return {
#             # Item.AProlificPirate: 1,
#             Item.TroubledWaters: 12,
#             Item.PiecesOfPlunder: random.randint(1, 3)
#         }

#     def pass_rate(self, state: 'GameState'):
#         dc = state.region_data().dc_advanced
#         return self.narrow_pass_rate(dc, state.outfits.zeefaring)

################################################################################
###                            Creaking from Above                            ###
################################################################################

class CreakingFromAbove(OpportunityCard):
    def __init__(self):
        super().__init__("Creaking from Above")
        self.actions = [GlimFall()]

    def can_draw(self, state: GameState):
        return state.items[Item.TroubledWaters] < 21

class GlimFall(Action):
    def __init__(self):
        super().__init__("Glim-fall!")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.ShardOfGlim: 2 * state.region_data().peril,
            Item.SomeoneIsComing: 1,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 9,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.ShardOfGlim: state.region_data().peril // 3,
            Item.SilentStalker: 1,
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
        self.weight = 0.8

class StopAndExchangeNews(Action):
    def __init__(self):
        super().__init__("Stop and exchange news")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZeeZtory: -7,
            Item.TaleOfTerror: 6, #random.randint(2, 10),
            Item.ScrapOfIncendiaryGossip: 5.5 # random.randint(1, 10)
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

    def can_perform(self, state: GameState):
        return state.piracy_enabled

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.ChasingDownYourBounty: state.region_data().chasing_gain_basic,
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
        dc = state.region_data().dc_basic
        return self.broad_pass_rate(dc, state.outfits.shadowy)    

################################################################################
###                            Rats in the Hold                               ###
################################################################################

class RatsInTheHold(OpportunityCard):
    def __init__(self):
        super().__init__("Rats in the Hold")
        self.actions = [NegotiateWithRats(), FillTheHoldWithTraps(),
                        RatCatchingExpedition(), QuestionAboutShips()]
        self.weight = 0.8

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
        return self.broad_pass_rate(state.region_data().peril, state.outfits.persuasive)    

class FillTheHoldWithTraps(Action):
    def __init__(self):
        super().__init__("Fill the hold with traps")

    def pass_items(self, state: 'GameState'):
        return {
            Item.RatOnAString: 50,
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.MutinousWhispers: 1,
            Item.TimeSpentAtZee: 1
        }
    
    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().peril, state.outfits.dangerous)    

class RatCatchingExpedition(Action):
    def __init__(self):
        super().__init__("Go on a rat-catching expedition")

    # TODO profession requirements
    def can_perform(self, state: GameState):
        return state.items.get(Item.NotchedBoneHarpoon, 0) > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.RatOnAString: 100,
            Item.ZailingProgress: state.outfits.zailing_speed + random.randint(1, 5),
            Item.TimeSpentAtZee: 1
        }

class QuestionAboutShips(Action):
    def __init__(self):
        super().__init__("Question them about other ships")

    def can_perform(self, state: GameState):
        return state.piracy_enabled

    # TODO rare success
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ChasingDownYourBounty: state.region_data().chasing_gain_basic,
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
        return self.broad_pass_rate(state.region_data().dc_basic, state.outfits.dangerous)    

################################################################################
###                           Signs of Disloyalty                             ###
################################################################################

class SignsOfDisloyalty(OpportunityCard):
    def __init__(self):
        super().__init__("Signs of Disloyalty")
        self.actions = [PrivateConversations(), DoubleTheirPay()]
        self.weight = 1_000_000 # HACK high urgency

    def can_draw(self, state: GameState):
        return state.items[Item.TroubledWaters] >= 28 and \
            state.items.get(Item.MutinousWhispers, 0) > 0

class PrivateConversations(Action):
    def __init__(self):
        super().__init__("A few private conversations")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -5,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }
    
    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge    

class DoubleTheirPay(Action):
    def __init__(self):
        super().__init__("Double their pay")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 15 - state.items[Item.TroubledWaters],
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
        self.weight = 1_000_000 # HACK high urgency

    def can_draw(self, state: GameState):
        return state.items[Item.TroubledWaters] > 28 and \
            state.items.get(Item.SilentStalker, 0) > 0

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
        zailing_loss = max(
            -1 * state.items[Item.ZailingProgress],
            (2 * state.outfits.zailing_speed))
        hull = 1 if state.items.get(Item.GroaningHull,0) < 1 else 0
        return {
            Item.TroubledWaters: 15 - state.items[Item.TroubledWaters],
            Item.ZailingProgress: zailing_loss,
            Item.GroaningHull: hull,
            Item.SilentStalker: -1 * state.items[Item.SilentStalker]
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().peril * 1.7
        return self.broad_pass_rate(dc, state.outfits.dangerous)

class ThrowBaitOverboard(Action):
    def __init__(self):
        super().__init__("Throw bait overboard")

    def can_perform(self, state: GameState):
        return state.items[Item.RumblingStomachs] < 1

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 15 - state.items[Item.TroubledWaters],
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
        self.weight = 1_000_000 # HACK high urgency

    def can_draw(self, state: GameState):
        return state.items[Item.TroubledWaters] > 28 and \
            state.items.get(Item.GroaningHull,0) > 0        

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
            Item.GroaningHull: -1 * state.items.get(Item.GroaningHull, 0),
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0)
        }
    
################################################################################
###                         The Clinging Coral Mass                           ###
################################################################################

class TheClingingCoralMass(OpportunityCard):
    def __init__(self):
        super().__init__("The Clinging Coral Mass")
        self.actions = [PutYourBacksIntoIt(), GrabAHammer()]
        self.weight = 0.8

class PutYourBacksIntoIt(Action):
    def __init__(self):
        super().__init__("Put your backs into it, lads!")

    # TODO rare success
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.MutinousWhispers: 1 - state.items.get(Item.MutinousWhispers, 0),
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().peril, state.outfits.persuasive)

class GrabAHammer(Action):
    def __init__(self):
        super().__init__("Grab a hammer yourself")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.MutinousWhispers: 1 - state.items.get(Item.MutinousWhispers, 0),
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().peril, state.outfits.dangerous)


################################################################################
###                            The Fleet of Truth                             ###
################################################################################

class TheFleetOfTruth(OpportunityCard):
    def __init__(self):
        super().__init__("The Fleet of Truth")
        self.actions = [Villainy(), Subterfuge(), EngagePeerReview()]
        self.weight = 0.8
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
        return self.broad_pass_rate(state.region_data().peril, state.outfits.dangerous)

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
        return self.broad_pass_rate(state.region_data().peril, state.outfits.shadowy)

class EngagePeerReview(Action):
    def __init__(self):
        super().__init__("Engage in a little bit of 'peer review'")

    def can_perform(self, state: GameState):
        return state.piracy_enabled

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.ChasingDownYourBounty: state.region_data().chasing_gain_basic,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.PageOfCryptopalaeontologicalNotes: 3,
            Item.PageOfPrelapsarianArchaeologicalNotes: 3,
            Item.PageOfTheosophisticalNotes: 3,
            Item.UnwelcomeOnTheWaters: 1,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().dc_basic, state.outfits.persuasive)

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

    def can_draw(self, state: GameState):
        return state.items[Item.TroubledWaters] >= 10

class OutrunStorm(Action):
    def __init__(self):
        super().__init__("Outrun the storm front")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0),
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

    def can_perform(self, state: GameState):
        return state.outfits.zubmersibility > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ZeeZtory: 4.5,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

class ChartStormCourse(Action):
    def __init__(self):
        super().__init__("Chart a course through the storm using your Storm in a Teacup")

    def can_perform(self, state: GameState):
        return state.items.get(Item.StormInATeacup, 0) > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.ZeeZtory: 2,
            Item.TroubledWaters: 4, # TODO unknown value
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: random.randint(10),
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0)
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
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 9,
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0),
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().peril, state.outfits.persuasive)

class DrownOutDrownies(Action):
    def __init__(self):
        super().__init__("Drown out the drownies")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 9,
            Item.GroaningHull: 1 - state.items.get(Item.GroaningHull, 0),
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().peril, state.outfits.dangerous)

class CureIgnorance(Action):
    def __init__(self):
        super().__init__("Cure the ignorance of your zailors")

    def can_perform(self, state: GameState):
        return state.items.get(Item.FacetedDecanterOfDrownieEffluvia, 0) > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TroubledWaters: max(-5, -1 * state.items[Item.TroubledWaters]),
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
        # TODO: Lower than usual dc?
        dc = state.region_data().dc_advanced - 2
        return self.narrow_pass_rate(dc, state.outfits.kataleptic_toxicology)
    
class ListenForQuarry(Action):
    def __init__(self):
        super().__init__("Listen to the songs, and for your quarry")

    def can_perform(self, state: GameState):
        return state.piracy_enabled

    # TODO rare success
    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ChasingDownYourBounty: state.region_data().chasing_gain_advanced,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 6,
            Item.Nightmares: 4,
            Item.SilentStalker: 1 - state.items.get(Item.SilentStalker, 0),
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) \
                + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.monstrous_anatomy)

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
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.MutinousWhispers: 1 - state.items.get(Item.MutinousWhispers, 0),
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) \
                + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().peril, state.outfits.dangerous)

class RestartParty(Action):
    def __init__(self):
        super().__init__("Restart the party")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.PiecesOfPlunder: state.region_data().plunder_gain_basic,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1,
            Item.BottleOfBrokenGiant1844: state.outfits.luxurious
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.MutinousWhispers: 1 - state.items.get(Item.MutinousWhispers, 0),
            Item.ZailingProgress: (state.outfits.zailing_speed // 2),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().dc_basic, state.outfits.persuasive)


################################################################################
###                             Your False-Star                               ###
################################################################################

class YourFalseStar(OpportunityCard):
    def __init__(self):
        super().__init__("Your False-Star")
        self.actions = [NavigateByStar()]

    def can_draw(self, state: GameState):
        return state.items.get(Item.FalseStarOfYourOwn, 0) > 0

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
        self.weight = 1_000_000 # HACK high urgency

    def can_draw(self, state: GameState):
        return state.items[Item.TroubledWaters] >= 28 \
            and state.items.get(Item.UnwelcomeOnTheWaters, 0) > 0

class EvadeThem(Action):
    def __init__(self):
        super().__init__("Evade them!")

    def pass_rate(self, state: 'GameState'):
        return 0.7  # Pretty good odds, 70% success chance

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random_zailing_bonus(),
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
            Item.UnwelcomeOnTheWaters: -1 * state.items.get(Item.UnwelcomeOnTheWaters, 0),
            Item.MutinousWhispers: 1 - state.items.get(Item.MutinousWhispers, 0)
        }


################################################################################
###                       A Steamer full of Passengers                        ###
################################################################################

class ASteamerFullOfPassengers(OpportunityCard):
    def __init__(self):
        super().__init__("A Steamer full of Passengers")
        self.actions = [SteamPast(), InviteAboard(), RecogniseQuarry(), RobThemBlind()]

    def can_draw(self, state: GameState):
        return state.current_region in (ZeeRegion.HOME_WATERS, ZeeRegion.SHEPHERDS_WASH)

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

    def can_perform(self, state: GameState):
        return state.outfits.luxurious > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.Scandal: 2,
            # Item.Hedonist: 3,
            Item.ScarletStockings: 1,
            Item.SecludedAddress: 6,
            # Item.Austere: -3
        }

class RecogniseQuarry(Action):
    def __init__(self):
        super().__init__("Recognise your quarry")

    def can_perform(self, state: GameState):
        return state.items.get(Item.ListOfAliasesWrittenInGant, 0)

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().peril, state.outfits.dangerous)

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 5,
            Item.PieceOfRostygold: 250,
            Item.ZailingProgress: state.outfits.zailing_speed,
        }
    
    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed,
        }    

class RobThemBlind(Action):
    def __init__(self):
        super().__init__("Rob them blind")

    def can_perform(self, state: GameState):
        return state.piracy_enabled

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().dc_basic, state.outfits.dangerous)

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
            Item.UnwelcomeOnTheWaters: 1 - state.items.get(Item.UnwelcomeOnTheWaters, 0)
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
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TroubledWaters: 3
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.GroaningHull: 1 - state.items.get(Item.GroaningHull, 0),
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random_zailing_bonus(),
        }

class FireWarningShot(Action):
    def __init__(self):
        super().__init__("Fire a warning shot")

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().peril, state.outfits.dangerous)

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TroubledWaters: 2
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 12,
            Item.GroaningHull: 1 - state.items.get(Item.GroaningHull, 0),
            Item.ZailingProgress: state.outfits.zailing_speed // 2 + random_zailing_bonus(),
        }

class FightBack(Action):
    def __init__(self):
        super().__init__("Fight back!")

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.artisan_of_the_red_science)
    
    def pass_items(self, state: 'GameState'):
        return {
            Item.PiecesOfPlunder: 300,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TroubledWaters: 4
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.ZailingProgress: state.outfits.zailing_speed // 4 + random_zailing_bonus(),
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
            Item.TroubledWaters: max(-2, -1 * state.items[Item.TroubledWaters])
        }

class LetUnterzeeHaveThem(Action):
    def __init__(self):
        super().__init__("Let the Unterzee have them")

    def pass_items(self, state: 'GameState'):
        return {
            # Item.Heartless: 3,
            # Item.Magnanimous: -3,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TroubledWaters: 1,
            Item.TimeSpentAtZee: 1
        }

class LootTheWreckage(Action):
    def __init__(self):
        super().__init__("Loot the wreckage")

    def can_perform(self, state: GameState):
        return state.piracy_enabled

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.PiecesOfPlunder: 250,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0),
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        dc = state.region_data().dc_advanced
        return self.narrow_pass_rate(dc, state.outfits.zeefaring)
    
################################################################################
###                        The Light of the Mountain                          ###
################################################################################

class TheLightOfTheMountain(OpportunityCard):
    def __init__(self):
        super().__init__("The Light of the Mountain")
        self.actions = [FixLookingGlass()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SHEPHERDS_WASH

class FixLookingGlass(Action):
    def __init__(self):
        super().__init__("Fix a looking-glass on the Mountain")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.SouthernWind: 4 if state.items.get(Item.SouthernWind, 0) == 0 else 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.MemoryOfDistantShores: 5,
            Item.TimeSpentAtZee: 1
        }

################################################################################
###                               The Wax-Wind                                ###
################################################################################

class TheWaxWind(OpportunityCard):
    def __init__(self):
        super().__init__("The Wax-Wind")
        self.actions = [HideBelowDecks(), ZailIntoWind(), Dive(), ZailIntoStormEye()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SHEPHERDS_WASH

class HideBelowDecks(Action):
    def __init__(self):
        super().__init__("Shut off the engines and hide belowdecks")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ZeeZtory: 1
        }

class ZailIntoWind(Action):
    def __init__(self):
        super().__init__("Zail into the wind")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.SouthernWind: 1 if state.items.get(Item.SouthernWind, 0) > 0 else 0,
            Item.ZeeZtory: 1,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ZeeZtory: 1
        }

    def pass_rate(self, state: 'GameState'):
        # TODO: this is what the wiki says?
        return self.broad_pass_rate(1, state.outfits.shadowy)

class Dive(Action):
    def __init__(self):
        super().__init__("Dive!")

    def can_perform(self, state: GameState):
        return state.outfits.zubmersibility > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -1,
            Item.SouthernWind: 1 if state.items.get(Item.SouthernWind, 0) > 0 else 0,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

class ZailIntoStormEye(Action):
    def __init__(self):
        super().__init__("Zail into the eye of the storm")

    # TODO: requires stormy-eyed, failure result

    def pass_items(self, state: 'GameState'):
        return {
            Item.MemoryOfDistantShores: 1,
            Item.ZeeZtory: 1,
            Item.MemoryOfLight: 1,
            Item.SouthernWind: 1 if state.items.get(Item.SouthernWind, 0) > 0 else 0,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(state.region_data().dc_advanced, state.outfits.zeefaring)

################################################################################
###                              Row, row, row                                ###
################################################################################

class RowRowRow(OpportunityCard):
    def __init__(self):
        super().__init__("Row, row, row")
        self.actions = [ZailOnBy(), BrawlWithMonks()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SHEPHERDS_WASH        

class ZailOnBy(Action):
    def __init__(self):
        super().__init__("Zail on by")

    def pass_items(self, state: 'GameState'):
        return {
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
        return self.broad_pass_rate(45, state.outfits.zailing_speed)

class BrawlWithMonks(Action):
    def __init__(self):
        super().__init__("Brawl with the monks")

    def pass_items(self, state: 'GameState'):
        return {
            Item.BottleOfBrokenGiant1844: 1,
            Item.ZeeZtory: 2
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(state.region_data().dc_basic, state.outfits.dangerous)

# Locked after Goddfall discovered
# class AskMonksOrigin(Action):
#     def __init__(self):
#         super().__init__("Ask the monks from where they hail")

#     def pass_items(self, state: 'GameState'):
#         return {
#             Item.CellarOfWine: -1,
#             Item.BottleOfMorelways1872: -100,
#             Item.DiscoveredGodfall: 1
#         }


################################################################################
###                              Coral Commotion                              ###
################################################################################

class CoralCommotion(OpportunityCard):
    def __init__(self):
        super().__init__("A Coral Commotion")
        self.actions = [ScavengeAmidstTheScrum(), WeaveThroughThrong()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.STORMBONES

class ScavengeAmidstTheScrum(Action):
    def __init__(self):
        super().__init__("Scavenge amidst the scrum of boats")

    # TODO rare success
    def pass_items(self, state: 'GameState'):
        return {
            Item.SilkScrap: 50,
            Item.TroubledWaters: 3,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0),
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge

class WeaveThroughThrong(Action):
    def __init__(self):
        super().__init__("Weave through the throng")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.GroaningHull: 1 - state.items.get(Item.GroaningHull, 0),
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(45, state.outfits.zailing_speed)

# class FindQuickerRoute(Action):
#     def __init__(self):
#         super().__init__("Find a quicker route into Port Cecil")

#     def pass_items(self, state: 'GameState'):
#         return {
#             Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
#             Item.DiscoveredPrinciplesOfCoral: 1,  # Hidden discovery
#             Item.TimeSpentAtZee: 1
#         }

#     def pass_rate(self, state: 'GameState'):
#         return 1.0  # Always success


################################################################################
###                    A Mountain of the Unterzee                            ###
################################################################################

class MountainOfTheUnterzee(OpportunityCard):
    def __init__(self):
        super().__init__("A Mountain of the Unterzee")
        self.actions = [HardToPort(), HoldAgainstMountain()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.STORMBONES

class HardToPort(Action):
    def __init__(self):
        super().__init__("Hard to port! Reverse engines!")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.AppallingSecret: 5,
            Item.SilentStalker: 1 - state.items.get(Item.SilentStalker, 0),
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 10,
            Item.SilentStalker: 1 - state.items.get(Item.SilentStalker, 0),
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(55, state.outfits.zailing_speed)

class HoldAgainstMountain(Action):
    def __init__(self):
        super().__init__("Hold!")

    # FATE-locked w cladery heart
    def can_perform(self, state: GameState):
        return False

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -1,
            Item.CarvedBallOfStygianIvory: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

################################################################################
###                             A Tiny Coral Island                          ###
################################################################################

class TinyCoralIsland(OpportunityCard):
    def __init__(self):
        super().__init__("A Tiny Coral Island")
        self.actions = [RecordAndMoveOn(), WhatsDownThere(), RecogniseShape()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.STORMBONES

class RecordAndMoveOn(Action):
    def __init__(self):
        super().__init__("Record it and move on")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TroubledWaters: 3,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class WhatsDownThere(Action):
    def __init__(self):
        super().__init__("What's that down there?")

    def can_perform(self, state: GameState):
        return state.outfits.zubmersibility > 0    

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.AppallingSecret: 5,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class RecogniseShape(Action):
    def __init__(self):
        super().__init__("Recognise its shape")

    def pass_items(self, state: 'GameState'):
        return {
            # Item.ShapelingArts: 1,
            Item.CrypticClue: 25,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(3, state.outfits.shapeling_arts)


################################################################################
###                            A Wind from the North                          ###
################################################################################

class WindFromTheNorth(OpportunityCard):
    def __init__(self):
        super().__init__("A Wind from the North")
        self.actions = [KeepCrewOnCourse(), HelpThem(), ListenToTheWind()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.STORMBONES        

class KeepCrewOnCourse(Action):
    def __init__(self):
        super().__init__("Keep your crew on course")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.NorthernWind: 1,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 12,
            Item.CreepingFear: 1,
            Item.UnaccountablyPeckish: 1,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.NorthernWind: 1,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(110, state.outfits.persuasive)

class HelpThem(Action):
    def __init__(self):
        super().__init__("Help them")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.NorthernWind: 1,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.Wounds: 5,
            Item.TroubledWaters: 5,
            Item.NorthernWind: 1,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        # NP reduces challenge but should already be 100%
        return self.broad_pass_rate(110, state.outfits.dangerous)

class ListenToTheWind(Action):
    def __init__(self):
        super().__init__("Listen to the wind")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 6,
            Item.NorthernWind: 1,
            Item.UnaccountablyPeckish: 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success


################################################################################
###                          Sighting a Lifeberg                              ###
################################################################################

class SightingLifeberg(OpportunityCard):
    def __init__(self):
        super().__init__("Sighting a Lifeberg")
        self.actions = [KeepDistance(), RamLifeberg(), ZailPastLifeberg()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.STORMBONES            

class KeepDistance(Action):
    def __init__(self):
        super().__init__("Keep your distance; make observations")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TaleOfTerror: 1,
            Item.ZeeZtory: 1,
            Item.NorthernWind: 1,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus()
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(110, state.outfits.watchful)

class RamLifeberg(Action):
    def __init__(self):
        super().__init__("Ram the lifeberg and claim a piece of it!")

    def can_perform(self, state: GameState):
        return state.items.get(Item.NotchedBoneHarpoon, 0) > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.NorthernWind: min(3, state.items.get(Item.NorthernWind, 0) + 1),
            Item.ExtraordinaryImplication: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class ZailPastLifeberg(Action):
    def __init__(self):
        super().__init__("Zail quickly past the lifeberg")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.Nightmares: 2
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.GroaningHull: 1 - state.items.get(Item.GroaningHull, 0)
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(45, state.outfits.zailing_speed)


################################################################################
###                              A Good Meal                                  ###
################################################################################

class GoodMeal(OpportunityCard):
    def __init__(self):
        super().__init__("A Good Meal")
        self.actions = [LittleBonus()]

    def can_draw(self, state: GameState):
        # TODO also requires Evolution progress
        return state.current_region == ZeeRegion.SEA_OF_VOICES

class LittleBonus(Action):
    def __init__(self):
        super().__init__("And a little bonus")

    def pass_items(self, state: 'GameState'):
        return {
            Item.PageOfCryptopalaeontologicalNotes: 3,
            Item.PageOfPrelapsarianArchaeologicalNotes: 3,
            Item.PageOfTheosophisticalNotes: 3,
            Item.MoonPearl: 1,
            Item.TroubledWaters: 3,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success


################################################################################
###                         A Hazard to Shipping                              ###
################################################################################

class HazardToShipping(OpportunityCard):
    def __init__(self):
        super().__init__("A Hazard to Shipping")
        self.actions = [SetCourseAroundThing()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SEA_OF_VOICES

class SetCourseAroundThing(Action):
    def __init__(self):
        super().__init__("Set a course around the thing")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.SilentStalker: 1 - state.items.get(Item.SilentStalker, 0),
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(150, state.outfits.watchful)


################################################################################
###                         A Light in the Fog                                ###
################################################################################

class LightInTheFog(OpportunityCard):
    def __init__(self):
        super().__init__("A Light in the Fog")
        self.actions = [GetClose(), KeepAway(), ListenForNews()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SEA_OF_VOICES

class GetClose(Action):
    def __init__(self):
        super().__init__("Get as close as you dare")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.WalkingTheFallingCities: 5,
            Item.ZeeZtory: 5,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class KeepAway(Action):
    def __init__(self):
        super().__init__("Keep away from the lighthouse")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class ListenForNews(Action):
    def __init__(self):
        super().__init__("Listen for news of your quarry")

    def can_perform(self, state: GameState):
        return state.piracy_enabled

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.ChasingDownYourBounty: 10,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus()
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.GroaningHull: 1 - state.items.get(Item.GroaningHull, 0),
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus()
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(160, state.outfits.watchful)


################################################################################
###                         Crossing Paths                                    ###
################################################################################

class CrossingPaths(OpportunityCard):
    def __init__(self):
        super().__init__("Crossing Paths")
        self.actions = [HailAndChat(), DuelCaptain(), SteamOnByPaths()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SEA_OF_VOICES

class HailAndChat(Action):
    def __init__(self):
        super().__init__("Hail the ship and have a chat with the captain")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ZeeZtory: 1,
            Item.WalkingTheFallingCities: 5,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class DuelCaptain(Action):
    def __init__(self):
        super().__init__("Demand to duel the steamer's captain")

    def can_perform(self, state: GameState):
        # TODO also requires FlexileSabre equipment
        return state.piracy_enabled

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 3,
            Item.PiecesOfPlunder: 350,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 7,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(6, state.outfits.zeefaring)

class SteamOnByPaths(Action):
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
###                          Listen to the Wind                               ###
################################################################################

class ListenToTheWind(OpportunityCard):
    def __init__(self):
        super().__init__("Listen to the Wind")
        self.actions = [ListenToVoices(), ListenClosely(), SteamWhereVoicesTell()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SEA_OF_VOICES
    
    # TODO: lock/unlock for all cards

class ListenToVoices(Action):
    def __init__(self):
        super().__init__("Listen to the Voices")

    def pass_items(self, state: 'GameState'):
        return {
            Item.EasternWind: 1,
            Item.NorthernWind: 1,
            Item.SouthernWind: 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TroubledWaters: 2,
            Item.ZeeZtory: 1,
            Item.WalkingTheFallingCities: 5
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TroubledWaters: 7,
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0)
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% chance

class ListenClosely(Action):
    def __init__(self):
        super().__init__("Listen closely to the Voices")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZeeZtory: 1,
            Item.WalkingTheFallingCities: 5,
            Item.TroubledWaters: 2,
            Item.EasternWind: 1,
            Item.NorthernWind: 1,
            Item.SouthernWind: 1,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus()
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TroubledWaters: 7,
            Item.CreepingFear: 1 - state.items.get(Item.CreepingFear, 0)
        }

    def pass_rate(self, state: 'GameState'):
        return 0.6  # 60% chance

class SteamWhereVoicesTell(Action):
    def __init__(self):
        super().__init__("Steam the way the voices tell you")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TroubledWaters: 3,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success


################################################################################
###                         Meeting a Local Steamer                           ###
################################################################################

class MeetingLocalSteamer(OpportunityCard):
    def __init__(self):
        super().__init__("Meeting a Local Steamer")
        self.actions = [
            HailSteamer(),
            SteamOnBySteamer(),
            SayMustYouDoThat(),
            BootsTranslate(),
            BoardSteamer()
        ]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SEA_OF_VOICES

class HailSteamer(Action):
    def __init__(self):
        super().__init__("Hail the steamer to exchange news")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: -2,
            Item.ZeeZtory: 1,
            Item.WalkingTheFallingCities: 5,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class SteamOnBySteamer(Action):
    def __init__(self):
        super().__init__("Steam on by")

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 2,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class SayMustYouDoThat(Action):
    def __init__(self):
        super().__init__("I say, must you do that?")

    def can_perform(self, state: GameState):
        return state.outfits.luxurious > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TroubledWaters: -1,
            Item.ZeeZtory: 4,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class BootsTranslate(Action):
    def __init__(self):
        super().__init__("Hail the steamer to exchange news, and let your Boots translate")

    # TODO unlock

    def can_perform(self, state: GameState):
        return False    

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZeeZtory: 3,
            Item.TroubledWaters: 1,
            Item.WalkingTheFallingCities: 5,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success

class BoardSteamer(Action):
    def __init__(self):
        super().__init__("Board her!")

    def can_perform(self, state: GameState):
        # TODO also requires RussetBrachiator
        return state.piracy_enabled

    def pass_items(self, state: 'GameState'):
        return {
            Item.Persuasive: 1,
            Item.TroubledWaters: '?',  # TBD based on outcome
            Item.PiecesOfPlunder: 350,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.Persuasive: 1,
            Item.TroubledWaters: 7,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(160, state.outfits.persuasive)


################################################################################
###                         The Giant of the Unterzee                         ###
################################################################################

class GiantOfUnterzee(OpportunityCard):
    def __init__(self):
        super().__init__("The Giant of the Unterzee")
        self.actions = [HelloGiant()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SEA_OF_VOICES

class HelloGiant(Action):
    def __init__(self):
        super().__init__("Erm, hello?")

    def pass_items(self, state: 'GameState'):
        return {
            Item.Persuasive: 1,
            Item.TroubledWaters: 5,
            Item.ZailingProgress: 80,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.Persuasive: 1,
            Item.TroubledWaters: 8,
            Item.ZailingProgress: (state.outfits.zailing_speed // 2) + random_zailing_bonus(),
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(150, state.outfits.persuasive)


################################################################################
###                            The Iceberg                                    ###
################################################################################

class TheIceberg(OpportunityCard):
    def __init__(self):
        super().__init__("The Iceberg")
        self.actions = [PrudentDistance(), LookUnderIceberg()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SEA_OF_VOICES and \
            state.items[Item.TroubledWaters] >= 10

class PrudentDistance(Action):
    def __init__(self):
        super().__init__("Keep a prudent distance")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus(),
            Item.TroubledWaters: 2,
            Item.WalkingTheFallingCities: 5
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.CreepingFear: 1 - state.items.get(Item.TroubledWaters, 0)
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% chance

class LookUnderIceberg(Action):
    def __init__(self):
        super().__init__("Have a look around under the iceberg")

    def can_perform(self, state: GameState):
        return state.outfits.zubmersibility > 0

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZeeZtory: 2,
            Item.TroubledWaters: -2,
            Item.WalkingTheFallingCities: 5,
            Item.ZailingProgress: state.outfits.zailing_speed + random_zailing_bonus()
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0  # Always success


################################################################################
###                           Unfinished Pirates!                             ###
################################################################################

class UnfinishedPirates(OpportunityCard):
    def __init__(self):
        super().__init__("Unfinished Pirates!")
        self.actions = [RepelBoarders(), ShowMightOfBroadside(), OutpaceThem()]

    def can_draw(self, state: GameState):
        return state.current_region == ZeeRegion.SEA_OF_VOICES and \
            state.items[Item.TroubledWaters] >= 10

class RepelBoarders(Action):
    def __init__(self):
        super().__init__("Repel Boarders!")

    def pass_items(self, state: 'GameState'):
        return {
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TroubledWaters: 3,
            Item.ZeeZtory: 1,
            Item.TimeSpentAtZee: 1
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.GroaningHull: 1 - state.items.get(Item.GroaningHull, 0),
            Item.TroubledWaters: 9,
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(120, state.outfits.dangerous)


class ShowMightOfBroadside(Action):
    def __init__(self):
        super().__init__("Show them the might of your broadside")

    def can_perform(self, state: GameState):
        return state.piracy_enabled

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.PiecesOfPlunder: 350,
            Item.ZailingProgress: state.outfits.zailing_speed
        }

    def fail_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 8,
            Item.UnwelcomeOnTheWaters: 1 - state.items.get(Item.UnwelcomeOnTheWaters, 0),
            Item.ZailingProgress: state.outfits.zailing_speed // 2,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(7, state.outfits.zeefaring)


class OutpaceThem(Action):
    def __init__(self):
        super().__init__("Outpace them")

    def can_perform(self, state: GameState):
        return state.outfits.zailing_speed >= 75        

    def pass_items(self, state: 'GameState'):
        return {
            Item.TroubledWaters: 4,
            Item.ZailingProgress: state.outfits.zailing_speed,
            Item.TimeSpentAtZee: 1
        }

    def pass_rate(self, state: 'GameState'):
        return 1.0

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
    # DreamOfSunbeams(),
    FlockOfProphets(),
    GiantAnglerCrab(),
    GrowingConcern(),
    HugeTerribleBeast(),
    # TODO complicated card
    # MessageInABottle(),
    NavigationError(),
    PromisingWreck(),
    # RagtagFlotilla(), # Lifeberg WQ only
    ShipOfZealots(),
    SightingOfTheBounty(),
    SpitOfLand(),
    WorryingAppetite(),
    ArchitectsDream(),
    # BearingWitnessToPilgrimage(), # Midnight Whale WQ
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

    # Home Waters
    ASteamerFullOfPassengers(), # also in SW
    ShesGoingDown(),

    # Shepherds Wash
    ACorsairGalley(),
    TheLightOfTheMountain(),
    TheWaxWind(),
    RowRowRow(),

    # Stormbones
    CoralCommotion(),
    MountainOfTheUnterzee(),
    TinyCoralIsland(),
    WindFromTheNorth(),
    SightingLifeberg(),

    # Sea of Voices
    GoodMeal(),
    HazardToShipping(),
    LightInTheFog(),
    CrossingPaths(),
    ListenToTheWind(),
    MeetingLocalSteamer(),
    GiantOfUnterzee(),
    TheIceberg(),
    UnfinishedPirates()
]

# Initial setup
def setup_simulation(chasing, route: list[tuple[ZeeRegion, ZeeRegion]]):
    state = GameState()

    # Add each card to the deck
    for card in cards:
        state.deck.append(card)

    state.items[Item.ChasingDownYourBounty] = chasing
    state.route = route
    state.current_region, state.next_region = route[0]
    state.progress_required = zee_regions[state.current_region].distance_to[state.next_region]

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
def print_item_summary(total_item_changes, runs, total_actions):
    print(f"\n{'Item':<30}{'Avg +/Run':<15}{'Echo Value':<15}{'Total Echo/Action':<20}")
    print("-" * 85)

    total_echo_value = 0.0

    for item, total_change in total_item_changes.items():
        avg_change = total_change / runs
        echo_value = item_echo_values.get(item, 0.0)
        item_total_echo_value = echo_value * total_change

        # Accumulate the total echo value across all items
        total_echo_value += item_total_echo_value

        # Only display items with non-zero average change
        if avg_change != 0.0:
            print(f"{item.name:<30}{avg_change:<15.2f}{echo_value:<15.2f}{item_total_echo_value / total_actions:<20.4f}")

    print(f"\n{'Total Echo/Action':<45}{total_echo_value / total_actions:.4f}")

# Update progress bar function
def update_progress(progress):
    bar_length = 40
    block = int(round(bar_length * progress))
    text = f"\rProgress: [{'#' * block + '-' * (bar_length - block)}] {progress * 100:.2f}%"
    sys.stdout.write(text)
    sys.stdout.flush()

def run_simulation(runs: int, route: list[tuple[ZeeRegion, ZeeRegion]]):
    total_item_changes = defaultdict(int)
    total_actions = 0
    total_region_action_counts = defaultdict(int)

    # Accumulate action stats
    total_action_play_counts = defaultdict(int)
    total_action_success_counts = defaultdict(int)
    total_action_failure_counts = defaultdict(int)
    total_card_draw_counts = defaultdict(int)
    total_card_play_counts = defaultdict(int)

    # Track the number of successful and failed runs
    successes = 0
    failures = 0    

    chasing_start = 1
    # Run the simulation for the specified number of runs
    for i in range(runs):
        state = setup_simulation(chasing_start, route)  # Initialize a fresh GameState for each run
        state.run()

        # Carry over chasing to next run
        chasing_start = state.items[Item.ChasingDownYourBounty]

        # Track success and failure of each run
        if state.status == "Success":
            successes += 1
        else:
            failures += 1


        # Accumulate total actions across all runs
        total_actions += state.actions

        # Accumulate item changes for each run
        for item, count in state.items.items():
            total_item_changes[item] += count

        # Accumulate region action counts
        for region, count in state.region_action_counts.items():
            total_region_action_counts[region] += count            

        # Accumulate action play/success/failure counts
        for action, count in state.action_play_counts.items():
            total_action_play_counts[action] += count

        for action, count in state.action_success_counts.items():
            total_action_success_counts[action] += count

        for action, count in state.action_failure_counts.items():
            total_action_failure_counts[action] += count

        # Accumulate card draw/play counts
        for card, count in state.card_draw_counts.items():
            total_card_draw_counts[card] += count

        for card, count in state.card_play_counts.items():
            total_card_play_counts[card] += count

        update_progress((i + 1) / runs)  # Update the progress bar

    avg_actions_per_run = total_actions / runs

    print()
    print("Route:")
    print(f"{route[0][0]} to {route[-1][1]} via:")
    for i in route:
        print(f"    {i[0]} => {i[1]}")

    display_results(
        total_item_changes, avg_actions_per_run, total_action_play_counts,
        total_action_success_counts, total_action_failure_counts, 
        total_card_draw_counts, total_card_play_counts, state.deck, 
        total_region_action_counts, total_actions, runs, successes, failures
    )

def display_results(
    total_item_changes, avg_actions_per_run, total_action_play_counts,
    total_action_success_counts, total_action_failure_counts, 
    total_card_draw_counts, total_card_play_counts, deck, 
    total_region_action_counts, total_actions, runs: int,
    successes: int, failures: int
):

    print()
    # Display success and failure counts
    print(f"Total Runs: {runs}")
    print(f"Successes: {successes} ({(successes / runs) * 100:.2f}%)")
    print(f"Failures: {failures} ({(failures / runs) * 100:.2f}%)")

    # Card and Action results display
    print_condensed_action_table(
        total_action_play_counts,
        total_action_success_counts,
        total_action_failure_counts,
        total_card_draw_counts,
        total_card_play_counts,
        deck,
        runs
    )

    # Display the average actions run
    print(f"\nAverage Actions per Run: {avg_actions_per_run:.2f}")

    # Display average change in items with echo values
    print_item_summary(total_item_changes, runs, total_actions)

    # Display actions spent in each region
    print_region_action_summary(total_region_action_counts, runs)


def print_item_summary(total_item_changes, runs, total_actions):
    print(f"\n{'Item':<30}{'Avg Change/Run':<20}{'Avg EPA':<20}")
    print("-" * 85)

    total_echo_value = 0.0

    for item, total_change in total_item_changes.items():
        avg_change = total_change / runs
        echo_value = item_echo_values.get(item, 0.0)
        item_total_echo_value = echo_value * total_change

        # Accumulate the total echo value across all items
        total_echo_value += item_total_echo_value

        # Only display items with non-zero average change
        if avg_change != 0.0:
            print(f"{item.name:<30}{avg_change:<20.2f}{item_total_echo_value / total_actions:<20.4f}")

    print(f"\n{'Avg Zailing EPA:':<50}{total_echo_value / total_actions:.4f}")
    # TODO: count the 1 extra action required to leave port?
    print()


# Print actions spent in each ZeeRegion
def print_region_action_summary(total_region_action_counts, runs):
    print(f"\n{'Region':<30}{'Avg Actions/Run':<15}")
    print("-" * 45)
    for region, total_actions in total_region_action_counts.items():
        avg_actions = total_actions / runs
        print(f"{region.name:<30}{avg_actions:<15.2f}")


# Condensed action table printing (already implemented)
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


london_to_elder_continent = [
    (ZeeRegion.HOME_WATERS, ZeeRegion.SHEPHERDS_WASH),
    (ZeeRegion.SHEPHERDS_WASH, ZeeRegion.SHEPHERDS_WASH)
]

elder_continent_to_london = [
    (ZeeRegion.SHEPHERDS_WASH, ZeeRegion.HOME_WATERS),
    (ZeeRegion.HOME_WATERS, ZeeRegion.HOME_WATERS)
]

# Now execute multiple runs:
if __name__ == "__main__":
    run_simulation(runs=1_000, route=london_to_elder_continent)
