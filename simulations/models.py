import random
from collections import defaultdict

class GameState:
    def __init__(self):
        self.outfit = OutfitList()

        self.items = {}
        self.deck = []
        self.hand = []
        self.storylets = []

        self.card_draw_counts = defaultdict(int)
        self.card_play_counts = defaultdict(int)
        self.action_play_counts = defaultdict(int)
        self.action_success_counts = defaultdict(int)
        self.action_failure_counts = defaultdict(int)
        # self.total_item_changes = defaultdict(int)

    def ev_from_item(self, item, val: int):
        return 0
    
    def clear_hand(self):
        self.hand.clear()

class OutfitList:
    def __init__(self, default_basic = 330, default_advanced = 16):
        self.dangerous = default_basic
        self.watchful = default_basic
        self.persuasive = default_basic
        self.shadowy = default_basic

        self.player_of_chess = default_advanced
        self.zeefaring = default_advanced
        self.monstrous_anatomy = default_advanced
        self.mithridacy = default_advanced
        self.artisan_of_the_red_science = default_advanced
        self.kataleptic_toxicology = default_advanced
        self.shapeling_arts = default_advanced
        self.glasswork = default_advanced

        self.zailing_speed = 55
        self.zubmersibility = 1
        self.luxurious = 0
        self.reduce_tw = 0 # TODO re-implement        

class OpportunityCard:
    def __init__(self, name, weight=1.0):
        self.name = name
        self.weight = weight
        self.actions = []  # List of possible actions

    def can_draw(self, state: 'GameState'):
        return True
    
class Action:
    def __init__(self, name):
        self.name = name
        self.action_cost = 1

    def can_perform(self, state: GameState):
        return True

    def pass_items(self, state: GameState):
        """Return a dictionary of items to be added on success."""
        return {}  # Default is no items

    def fail_items(self, state: GameState):
        """Return a dictionary of items to be added on failure."""
        return {}  # Default is no items

    def perform(self, state: GameState):
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

    def perform_pass(self, state: GameState):
        """Default implementation to add items from pass_items to state.items."""
        for item, amount in self.pass_items(state).items():
            # Ensure item key exists, if not, initialize it
            if item not in state.items:
                state.items[item] = 0

            state.items[item] += amount

    def perform_failure(self, state: GameState):
        """Default implementation to add items from fail_items to state.items."""
        for item, amount in self.fail_items(state).items():
            # Ensure item key exists, if not, initialize it
            if item not in state.items:
                state.items[item] = 0
            state.items[item] += amount

    def pass_rate(self, state: GameState):
        return 1.0  # Default pass rate is 100%

    def pass_ev(self, state: GameState):
        return self.items_ev(state, self.pass_items(state))
    
    def failure_ev(self, state: GameState):
        return self.items_ev(state, self.fail_items(state))
    
    def ev(self, state: GameState):
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
    
    def items_ev(self, state: GameState, items: dict):
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
