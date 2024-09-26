import random
import sys
from enum import Enum, auto
from collections import defaultdict
import simulations.item_conversions
from enums import Item
import utils

class ActionResult(Enum):
    NotAllowed = auto()
    Pass = auto()
    Failure = auto()
    AltSuccess = auto()
    AltFailure = auto()

class GameState:
    def __init__(self, max_hand_size = 3):
        self.max_hand_size = max_hand_size
        self.outfit = PlayerOutfit()

        self.items = {}
        self.deck = []
        self.hand = []
        self.storylets = []

        self.card_draw_counts = defaultdict(int)
        self.card_play_counts = defaultdict(int)

        self.action_result_counts = defaultdict(lambda: defaultdict(int))
    
        self.action_success_counts = defaultdict(int)
        self.action_failure_counts = defaultdict(int)
        # self.total_item_changes = defaultdict(int)
        
        self.cards_drawn = 0
        self.actions = 0
        self.status = "InProgress"

    def ev_from_item(self, item, val: int):
        if item == Item.Echo:
            return val * item 
        return val * simulations.item_conversions.conversion_rate(item, Item.Echo)
    
    def clear_hand(self):
        self.hand.clear()

    def draw_card(self):
        drawn, lowest = None, float('inf')
        for card in self.deck:
            if card not in self.hand and card.can_draw(self):
                rand = random.random() / card.weight
                if rand < lowest:
                    drawn = card
                    lowest = rand

        if drawn:
            self.cards_drawn += 1
            self.card_draw_counts[drawn] += 1
            self.hand.append(drawn)

    def add_items(self, dict):
        for item, amount in dict.items():
            if item not in self.items:
                self.items[item] = 0

            self.items[item] += amount

    def get(self, item: Item):
        return self.items.get(item, 0)
    
    def get_pyramidal_level(self, item: Item):
        return utils.cp_to_level(self.items.get(item, 0))    

    def run(self):
        while self.status == "InProgress":
            self.step()

    def step(self):
        best_card, best_action, best_action_ev = self.find_best_action()

    def find_best_action(self):
        best_card, best_action, best_action_ev = None, None, -float('inf')

        for card in self.storylets:
            for action in card.actions:
                if action.can_perform(self):
                    action_ev = action.ev(self)
                    if action_ev > best_action_ev:
                        best_card, best_action, best_action_ev = card, action, action_ev

        for card in self.hand:
            # HACK until I think of a better way to handle autofire cards
            autofire_bonus = 1_000_000 if card.autofire else 0
            for action in card.actions:
                if action.can_perform(self):
                    action_ev = action.ev(self) + autofire_bonus
                    if action_ev > best_action_ev:
                        best_card, best_action, best_action_ev = card, action, action_ev

        return (best_card, best_action, best_action_ev)
    
    def play_card_action(self, best_card, best_action):
        result = best_action.perform(self)
        self.actions += best_action.action_cost
        self.action_result_counts[best_action][result] += 1

        if best_card is not None:
            self.card_play_counts[best_card] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)

    def update_game_state(self):
        self.hand = [card for card in self.hand if card.can_draw(self)]

        if self.actions >= 100:
            self.status = "Complete"


class PlayerOutfit:
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

        self.reduce_wounds = 0
        self.reduce_nightmares = 0
        self.reduce_scandal = 0
        self.reduce_suspicion = 0

        self.zailing_speed = 55
        self.zubmersibility = 1
        self.luxurious = 0
        self.reduce_tw = 0 # TODO re-implement        

class OpportunityCard:
    def __init__(self, name, weight=1.0):
        self.name = name
        self.weight = weight # TODO rename this to frequency / use enum?
        self.actions = []  # List of possible actions

        #
        self.free_discard = False
        self.autofire = False

    def can_draw(self, state: 'GameState'):
        return True
    
class Action:
    def __init__(self, name):
        self.name = name
        self.action_cost = 1
        self.has_random_returns = False

        # given pass vs. fail already decided
        self.alt_pass_rate = 0.0
        self.alt_fail_rate = 0.0

    def can_perform(self, state: GameState):
        return True

    def pass_items(self, state: GameState):
        """Return a dictionary of items to be added on success."""
        return {}
    
    def alt_pass_items(self, state: GameState):
        return {}

    def fail_items(self, state: GameState):
        return {}
    
    def alt_fail_items(self, state: GameState):
        return {}

    def perform(self, state: GameState):
        if self.can_perform(state):
            rate = self.pass_rate(state)
            if random.random() < rate:
                if random.random() < self.alt_pass_rate:
                    return self.perform_alt_pass(state)
                return self.perform_pass(state)
            else:
                return self.perform_failure(state)
        else:
            return ActionResult.NotAllowed

    def perform_pass(self, state: GameState):
        """Default implementation to add items from pass_items to state.items."""
        items = self.pass_items(state)
        state.add_items(items)
        return ActionResult.Pass
    
    def perform_alt_pass(self, state: GameState):
        items = self.alt_pass_items(state)
        state.add_items(items)
        return ActionResult.AltSuccess
    
    def perform_failure(self, state: GameState):
        items = self.fail_items(state)
        state.add_items(items)
        return ActionResult.Failure
    
    def perform_alt_failure(self, state: GameState):
        items = self.alt_fail_items(state)
        state.add_items(items)
        return ActionResult.AltFailure

    def pass_rate(self, state: GameState):
        return 1.0  # Default pass rate is 100%

    def pass_ev(self, state: GameState):
        normal_rate = 1.0 - self.alt_pass_rate
        normal_ev = self.items_ev(state, self.pass_items(state))
        alt_ev = self.items_ev(state, self.alt_pass_items(state))
        return self.alt_pass_rate * alt_ev + normal_rate * normal_ev
    
    def failure_ev(self, state: GameState):
        normal_rate = 1.0 - self.alt_fail_rate
        normal_ev = self.items_ev(state, self.fail_items(state))
        alt_ev = self.items_ev(state, self.alt_fail_items(state))
        return self.alt_fail_rate * alt_ev + normal_rate * normal_ev
        
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
        if dc is not None and dc > 0:
            return 0.6 * stat_value / dc
        else:
            return 1.0
    
    @staticmethod
    def narrow_pass_rate(dc, stat_value):
        if dc is not None and dc > 0:
            return 0.5 + (stat_value - dc) * 0.1
        else:
            return 1.0        

class SimulationRunner:
    def __init__(self, runs: int, initial_values: dict):
        self.runs = runs
        self.initial_values = initial_values
        self.total_item_changes = defaultdict(int)

        self.total_actions = 0
        self.total_action_play_counts = defaultdict(int)
        self.total_action_result_counts = defaultdict(lambda: defaultdict(int))

        self.total_draws = 0
        self.total_card_draw_counts = defaultdict(int)
        self.total_card_play_counts = defaultdict(int)

        self.outfit = None

        self.outcome_counts = defaultdict(int)

        self.storylets = []
        self.cards = []

    def update_progress(self, progress):
        bar_length = 40
        block = int(round(bar_length * progress))
        text = f"\rProgress: [{'#' * block + '-' * (bar_length - block)}] {progress * 100:.2f}%"
        sys.stdout.write(text)
        sys.stdout.flush()

    def create_state(self) -> GameState:
        raise NotImplementedError

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

        self.display_results()

    def display_results(self):
        avg_actions_per_run = self.total_actions / self.runs
        avg_draws_per_run = self.total_draws / self.runs

        print(f"\n\nTotal Runs: {self.runs}")
        for outcome, count in self.outcome_counts.items():
            print(f"{outcome}: {count} ({(count / self.runs) * 100:.2f}%)")

        # Print the last outfit used
        if self.outfit:
            self.display_outfit(self.outfit)

        print("\nInitial Items & Qualities:")
        print("-" * 40)
        for item, value in self.initial_values.items():
            print(f"{self.truncate_string(item.name, 40):<45}{value:<10}")    

        # Display action and item results
        self.print_condensed_action_table()
        self.print_item_summary()

        print(f"\nAverage Actions per Run: {avg_actions_per_run:.2f}")
        print(f"Average Draws per Run:   {avg_draws_per_run:.2f}\n")

    def display_outfit(self, outfit):
        print("\nPlayer Max Stats:")
        print(f"{'Stat':<30}{'Value':<10}")
        print("-" * 40)
        for stat, value in vars(outfit).items():
            print(f"{stat:<30}{value:<10}")    

    def print_condensed_action_table(self):
        color_codes = {
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'reset': '\033[0m'
        }

        print(f"\n{'    Card Name':<34}{'Played / Drawn':<20}{'Play %':<20}")
        print(f"{'        Action':<63}{'Played / Run':<15}{'Pass %':<20}")
        print("-" * 105)

        # Sort cards by total play count (descending)
        sorted_cards = sorted(self.total_card_draw_counts.keys(), key=lambda card: self.total_card_play_counts.get(card, 0), reverse=True)

        for card in sorted_cards:
            card_name = self.truncate_string(card.name)

            drawn = self.total_card_draw_counts.get(card, 0) / self.runs
            played = self.total_card_play_counts.get(card, 0) / self.runs
            play_rate = (self.total_card_play_counts.get(card, 0) / self.total_card_draw_counts.get(card, 1)) * 100 if self.total_card_draw_counts.get(card, 0) > 0 else 0

            color = color_codes['green'] if play_rate >= 99 else color_codes['yellow']  # You can customize this condition

            # Print card name with color
            print(f"    {color}{card_name:<30}{color_codes['reset']}{f'{played:.2f} / {drawn:.2f}':<20}") #{play_rate:<15.2f}")
            print()

            sorted_actions = sorted(card.actions, key=lambda action: self.total_action_play_counts.get(action.__class__.__name__, 0), reverse=True)

            for action in sorted_actions:
                action_name = self.truncate_string(action.name, 40)
                action_played = self.total_action_play_counts.get(action, 0) / self.runs
                result_counts = self.total_action_result_counts.get(action, {})
                successes = result_counts.get(ActionResult.Pass, 0) + result_counts.get(ActionResult.AltSuccess, 0)
                failures = result_counts.get(ActionResult.Failure, 0) + result_counts.get(ActionResult.AltFailure, 0)
                total = successes + failures
                success_rate = (successes / total) if total > 0 else 0

                success_color = color_codes['red']
                if success_rate >= 0.95:
                    success_color = color_codes['green']
                elif success_rate >= 0.60:
                    success_color = color_codes['yellow']
                elif success_rate >= 0.40:
                    success_color = color_codes['magenta']

                if action_played > 0:
                    print(f"{'':<8}{action_name:<40}{'':<15}{action_played:<15.2f}{success_color}{success_rate * 100:.2f}{color_codes['reset']}%")

            print("-" * 105)


    def print_item_summary(self):
        max_name_length = 35
        print(f"\n{'Item':<40}{'Avg +/Run':<15}{'Echo Value':<15}{'Total Echo/Action':<20}")
        print("-" * 85)

        total_echo_value = 0.0
        item_summaries = []

        for item, total_change in self.total_item_changes.items():
            initial_qty = self.initial_values.get(item, 0) * self.runs
            net_change = total_change - initial_qty

            avg_change = net_change / self.runs
            echo_value = simulations.item_conversions.conversion_rate(item, Item.Echo)

            estimated = False
            if echo_value == 0:
                echo_value = simulations.item_conversions.conversion_rate(item, Item._ApproximateEchoValue)
                estimated = True

            item_total_echo_value = echo_value * net_change

            total_echo_value += item_total_echo_value
            truncated_item_name = item.name if len(item.name) <= max_name_length else item.name[:max_name_length - 3] + "..."

            if avg_change != 0.0:
                item_summaries.append((truncated_item_name, avg_change, echo_value, item_total_echo_value / self.total_actions))

        item_summaries.sort(key=lambda x: x[1], reverse=True)

        for item_name, avg_change, echo_value, echo_per_action in item_summaries:
            print(f"{item_name:<40}{avg_change:<15.2f}{echo_value:<15.2f}{echo_per_action:<20.4f}")

        print(f"\n{'Total Echo/Action':<40}{total_echo_value / self.total_actions:.4f}")

    def truncate_string(self, s, length=25):
        if len(s) > length:
            return s[:length - 3] + '...'
        return s
