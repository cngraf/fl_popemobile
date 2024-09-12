import random
import sys
from collections import defaultdict
from enum import Enum, auto
from enums import *
from collections import defaultdict

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
        return 1.0
    
    def failure_ev(self, state: 'GameState'):
        return 0.0
    
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
        self.zeefaring = 15  # Example stat for "Zeefaring"
        self.zailing_speed = 55  # Example stat for "Zailing Speed"
        self.persuasive = 300

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
        self.troubled_waters = 0
        self.unwelcome_on_the_waters = 0
        self.pieces_of_plunder = 0
        self.zailing = 0
        self.time_spent_at_zee = 0

        # Initialize cards in the deck
        self.deck = []  # This will be populated with cards
        self.hand = []
        self.actions = 0

        self.card_draw_counts = defaultdict(int)
        self.card_play_counts = defaultdict(int)
        self.action_success_counts = defaultdict(int)
        self.action_failure_counts = defaultdict(int)
        self.action_play_counts = defaultdict(int)

        # Track total changes for each item
        self.total_item_changes = defaultdict(int)

    def draw_card(self):
        drawn, lowest = None, float('inf')
        for card in self.deck:
            if card not in self.hand and card.can_draw(self):
                rand = random.random() / card.weight
                if rand < lowest:
                    drawn = card
                    lowest = rand

        self.card_draw_counts[drawn.name] += 1
        self.hand.append(drawn)

    def step(self):
        # TODO: smart redraw
        while len(self.hand) < 3:
            self.draw_card()

        best_card, best_action, best_action_ev = None, None, -float('inf')

        for card in self.hand:
            for action in card.actions:
                if action.can_perform(self):
                    action_ev = action.pass_ev(self)
                    if action_ev > best_action_ev:
                        best_card, best_action, best_action_ev = card, action, action_ev

        outcome = best_action.perform(self)
        self.actions += best_action.action_cost
        self.action_play_counts[best_action.name] += 1

        if best_card is not None:
            self.card_play_counts[best_card.name] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)

        # Track successes and failures
        if outcome == "Success":
            self.action_success_counts[best_action.name] += 1
        else:
            self.action_failure_counts[best_action.name] += 1

        # Update item tracking
        for item, value in self.items.items():
            self.total_item_changes[item] += value

        self.actions += 1
        self.hand = [card for card in self.hand if card.can_draw(self)]

    def run(self, steps):
        while self.actions < steps:
            self.step()

    def display_results(self, runs):
        print_action_table(self.action_play_counts, self.action_success_counts, self.action_failure_counts, self.deck, runs)
        print_item_summary(self.total_item_changes, runs)

from enum import Enum

# Define the Item Enum
class Item(Enum):
    TroubledWaters = 1
    CreepingFear = 2
    Plunder = 3
    ZailingProgress = 4
    ChasingDownYourBounty = 5
    UnwelcomeOnTheWaters = 6
    TimeSpentAtZee = 7
    Nightmares = 8
    RosyColours = 9
    Suspicion = 10
    SilentStalker = 11
    PartialMap = 12
    WhirringContraption = 13

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



# Initial setup
def setup_simulation():
    state = GameState()

    # Add all defined cards to the deck
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
        DreamOfSunbeams()
    ]
    
    # Add each card to the deck
    for card in cards:
        state.deck.append(card)

    return state

# Print the action table with average plays per run and success rates
def print_action_table(action_play_counts, action_success_counts, action_failure_counts, deck, runs):
    print(f"\n{'Card':<30}{'Action':<30}{'Avg Plays/Run':<15}{'Success Rate':<15}")
    print("-" * 95)
    for card in deck:
        print(f"{card.name:<30}")
        for action in card.actions:
            played = action_play_counts.get(action.name, 0) / runs
            successes = action_success_counts.get(action.name, 0)
            failures = action_failure_counts.get(action.name, 0)
            total = successes + failures
            success_rate = (successes / total) * 100 if total > 0 else 0
            print(f"{'':<30}{action.name:<30}{played:<15.2f}{success_rate:.2f}%")
        print("-" * 95)

# Print the average change in items per run
def print_item_summary(total_item_changes, runs):
    print(f"\n{'Item':<30}{'Avg Change/Run':<15}")
    print("-" * 45)
    for item, total_change in total_item_changes.items():
        avg_change = total_change / runs
        print(f"{item.name:<30}{avg_change:<15.2f}")

# Update progress bar function
def update_progress(progress):
    bar_length = 40
    block = int(round(bar_length * progress))
    text = f"\rProgress: [{'#' * block + '-' * (bar_length - block)}] {progress * 100:.2f}%"
    sys.stdout.write(text)
    sys.stdout.flush()

# Now run the simulation
if __name__ == "__main__":
    steps = 1000
    state = setup_simulation()
    state.run(steps=steps)  # Run for 1000 steps
    state.display_results(steps)
