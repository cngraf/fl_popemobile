import random
from collections import defaultdict

class Action:
    def __init__(self, name):
        self.name = name
        self.pass_items = {}  # Items gained or lost on success
        self.fail_items = {}  # Items gained or lost on failure

    def can_perform(self, state: 'GameState'):
        return True

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
        for item, amount in self.pass_items.items():
            state.items[item] += amount

    def perform_failure(self, state: 'GameState'):
        for item, amount in self.fail_items.items():
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

class GameState:
    def __init__(self):
        self.outfits = OutfitList()

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
        if len(self.hand) == 0:
            self.draw_card()

        best_action, best_action_ev = None, -float('inf')

        for card in self.hand:
            for action in card.actions:
                if action.can_perform(self):
                    action_ev = action.pass_ev(self)
                    if action_ev > best_action_ev:
                        best_action, best_action_ev = action, action_ev

        outcome = best_action.perform(self)
        if outcome == "Success":
            self.action_success_counts[best_action.name] += 1
        else:
            self.action_failure_counts[best_action.name] += 1

        self.actions += 1
        self.hand = [card for card in self.hand if card.can_draw(self)]

    def run(self, steps):
        while self.actions < steps:
            self.step()

    def display_results(self):
        print(f"Troubled Waters: {self.troubled_waters}")
        print(f"Unwelcome on the Waters: {self.unwelcome_on_the_waters}")
        print(f"Pieces of Plunder: {self.pieces_of_plunder}")
        print(f"Zailing: {self.zailing}")
        print(f"Time Spent at Zee: {self.time_spent_at_zee}")
        print(f"Total Actions: {self.actions}")
        print(f"Successes: {sum(self.action_success_counts.values())}")
        print(f"Failures: {sum(self.action_failure_counts.values())}")






class BlankSpaceOnTheCharts(OpportunityCard):
    def __init__(self):
        super().__init__("A Blank Space on the Charts")
        self.actions = [TheresAnIslandHere(), FortuitousFragments(), SearchUnchartedWaters()]

class TheresAnIslandHere(Action):
    def __init__(self):
        super().__init__("There's an island here")
        self.pass_items = {
            'CreepingFear': 1,
            'TroubledWaters': -5
        }
        self.fail_items = {
            'CreepingFear': 1,
            'Nightmares': 3,
            'Zailing': -60,
            'TroubledWaters': 4
        }

    def pass_rate(self, state: 'GameState'):
        return 0.5  # 50% luck challenge

class FortuitousFragments(Action):
    def __init__(self):
        super().__init__("Fortuitous fragments")
        self.pass_items = {
            'TroubledWaters': 5,
            'PartialMap': -2
        }

    def can_perform(self, state: 'GameState'):
        return state.items['PartialMap'] >= 2  # Requires 2 Partial Maps

class SearchUnchartedWaters(Action):
    def __init__(self):
        super().__init__("Search the uncharted waters for your quarry")
        self.pass_items = {
            'TroubledWaters': -1,
            'ChasingBounty': random.randint(1, 5),
            'Zailing': state.outfits.zailing_speed
        }
        self.fail_items = {
            'TroubledWaters': -5,
            'CreepingFear': 1,
            'Zailing': state.outfits.zailing_speed // 2
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(6, state.outfits.zeefaring)










class CorvetteOfHerMajestysNavy(OpportunityCard):
    def __init__(self):
        super().__init__("A Corvette of Her Majesty's Navy")
        self.actions = [ExchangePleasantries(), TheyreNotSlowing(), RelyOnOldCodes()]

class ExchangePleasantries(Action):
    def __init__(self):
        super().__init__("Exchange pleasantries via semaphore")
        self.pass_items = {
            'TroubledWaters': -2,
            'Zailing': random.randint(1, 5)
        }

class TheyreNotSlowing(Action):
    def __init__(self):
        super().__init__("They're not slowing")
        self.pass_items = {
            'Suspicion': 3,
            'TroubledWaters': 3,
            'Zailing': state.outfits.zailing_speed
        }
        self.fail_items = {
            'SilentStalker': 1,
            'TroubledWaters': 9,
            'Zailing': state.outfits.zailing_speed
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(55, state.outfits.zailing_speed)

class RelyOnOldCodes(Action):
    def __init__(self):
        super().__init__("Rely on the Commodore's old codes")
        self.pass_items = {
            'Suspicion': -3,
            'TroubledWaters': -random.randint(2, 8),
            'Zailing': state.outfits.zailing_speed
        }
        self.fail_items = {
            'Suspicion': 4,
            'TroubledWaters': 8,
            'Zailing': state.outfits.zailing_speed
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(5, state.outfits.chess_player)










class CorvetteWithCorsairColours(OpportunityCard):
    def __init__(self):
        super().__init__("A Corvette of Her Majesty's Navy (with Corsair's Colours)")
        self.actions = [ExchangeInfo(), TakeThemForAll(), TheyreNotSlowing()]

class ExchangeInfo(Action):
    def __init__(self):
        super().__init__("Exchange information via semaphore")
        self.pass_items = {
            'TroubledWaters': -2,
            'ChasingBounty': 8,
            'Zailing': random.randint(1, 5)
        }
        self.fail_items = {
            'TroubledWaters': 6,
            'Suspicion': 2,
            'UnwelcomeOnWaters': 1,
            'Zailing': state.outfits.zailing_speed // 2 + random.randint(1, 5)
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(160, state.outfits.persuasive)

class TakeThemForAll(Action):
    def __init__(self):
        super().__init__("Take them for all they've got")
        self.pass_items = {
            'Suspicion': 1,
            'TroubledWaters': 4,
            'PiecesOfPlunder': random.randint(1, 3),
            'Zailing': state.outfits.zailing_speed
        }
        self.fail_items = {
            'Suspicion': 4,
            'TroubledWaters': 8,
            'UnwelcomeOnWaters': 1,
            'Zailing': state.outfits.zailing_speed // 2
        }

    def pass_rate(self, state: 'GameState'):
        return self.narrow_pass_rate(5, state.outfits.zeefaring)

class TheyreNotSlowing(Action):
    def __init__(self):
        super().__init__("They're not slowing")
        self.pass_items = {
            'Suspicion': 3,
            'TroubledWaters': 3,
            'Zailing': state.outfits.zailing_speed
        }
        self.fail_items = {
            'SilentStalker': 1,
            'TroubledWaters': 9,
            'Zailing': state.outfits.zailing_speed
        }

    def pass_rate(self, state: 'GameState'):
        return self.broad_pass_rate(75, state.outfits.zailing_speed)










class DreamOfACup(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of a Cup")
        self.actions = [DrinkTheWine(), AwakenFromDream()]

class DrinkTheWine(Action):
    def __init__(self):
        super().__init__("Drink the wine")
        self.pass_items = {
            'RosyColours': 4,
            'Nightmares': 3
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")
        self.pass_items = {
            'Nightmares': -3,
            'RosyColours': 0
        }











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

    def perform_pass(self, state: 'GameState'):
        state.troubled_waters += 5
        state.pieces_of_plunder += random.randint(1, 3)
        state.zailing += state.outfits.zailing_speed
        state.time_spent_at_zee += 1

    def pass_ev(self, state: 'GameState'):
        return 5  # Placeholder for actual EV

    def perform_failure(self, state: 'GameState'):
        state.troubled_waters += 12
        state.unwelcome_on_the_waters = 1
        state.zailing += state.outfits.zailing_speed // 2
        state.time_spent_at_zee += 1

    def failure_ev(self, state: 'GameState'):
        return -10  # Placeholder for actual EV

class SignalRamillies(Action):
    def __init__(self):
        super().__init__("Signal the HMS Ramillies for Support")
    
    def pass_rate(self, state: 'GameState'):
        # Narrow challenge, Zeefaring 11 (50% base)
        return self.narrow_pass_rate(11, state.outfits.zeefaring)

    def perform_pass(self, state: 'GameState'):
        state.troubled_waters += 5
        state.pieces_of_plunder += random.randint(1, 2)
        state.zailing += state.outfits.zailing_speed
        state.time_spent_at_zee += 1

    def pass_ev(self, state: 'GameState'):
        return 5  # Placeholder for actual EV

    def perform_failure(self, state: 'GameState'):
        state.troubled_waters += 12
        state.unwelcome_on_the_waters = 1
        state.zailing += state.outfits.zailing_speed // 2
        state.time_spent_at_zee += 1

    def failure_ev(self, state: 'GameState'):
        return -10  # Placeholder for actual EV

class EvadeThem(Action):
    def __init__(self):
        super().__init__("Evade Them!")

    def pass_rate(self, state: 'GameState'):
        # Broad challenge, Zailing Speed 45 (60% base)
        return self.broad_pass_rate(45, state.outfits.zailing_speed)

    def perform_pass(self, state: 'GameState'):
        state.troubled_waters += random.randint(2, 3)
        state.zailing += state.outfits.zailing_speed + random.randint(1, 5)
        state.time_spent_at_zee += 1

    def pass_ev(self, state: 'GameState'):
        return 3  # Placeholder for actual EV

    def perform_failure(self, state: 'GameState'):
        state.troubled_waters += 8
        state.zailing += state.outfits.zailing_speed + random.randint(1, 5)
        state.unwelcome_on_the_waters = 1

    def failure_ev(self, state: 'GameState'):
        return -8  # Placeholder for actual EV










class DreamOfATable(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of a Table")
        self.actions = [JoinThemAtTheTable(), AwakenFromDream()]

class JoinThemAtTheTable(Action):
    def __init__(self):
        super().__init__("Join them at their table")
        self.pass_items = {
            'RosyColours': 6,
            'Nightmares': 3
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")
        self.pass_items = {
            'Nightmares': -3,
            'RosyColours': 0
        }









class DreamOfAscent(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of Ascent")
        self.actions = [FlyHigher(), AwakenFromDream()]

class FlyHigher(Action):
    def __init__(self):
        super().__init__("Fly higher")
        self.pass_items = {
            'RosyColours': 5,
            'Nightmares': 3
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")
        self.pass_items = {
            'Nightmares': -3,
            'RosyColours': 0
        }










class DreamOfAscent(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of Ascent")
        self.actions = [FlyHigher(), AwakenFromDream()]

class FlyHigher(Action):
    def __init__(self):
        super().__init__("Fly higher")
        self.pass_items = {
            'RosyColours': 5,
            'Nightmares': 3
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")
        self.pass_items = {
            'Nightmares': -3,
            'RosyColours': 0
        }










class DreamOfDesigns(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of Designs")
        self.actions = [SunbatheInTheLight(), AwakenFromDream()]

class SunbatheInTheLight(Action):
    def __init__(self):
        super().__init__("Sunbathe in the light")
        self.pass_items = {
            'RosyColours': 0,  # 'Rosy Colours' quality is removed
            'Nightmares': 3,
            'WhirringContraption': 11  # New Accomplishment
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")
        self.pass_items = {
            'Nightmares': -3,
            'RosyColours': 0
        }










class DreamOfStainedGlass(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of Stained-Glass")
        self.actions = [LookIntoTheLight(), AwakenFromDream()]

class LookIntoTheLight(Action):
    def __init__(self):
        super().__init__("Look into the light")
        self.pass_items = {
            'RosyColours': 3,
            'Nightmares': 2
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")
        self.pass_items = {
            'Nightmares': -3,
            'RosyColours': 0
        }










class DreamOfSunbeams(OpportunityCard):
    def __init__(self):
        super().__init__("A Dream of Sunbeams")
        self.actions = [StareThroughTheGlare(), AwakenFromDream()]

class StareThroughTheGlare(Action):
    def __init__(self):
        super().__init__("Stare through the glare")
        self.pass_items = {
            'RosyColours': 3,
            'Nightmares': 2
        }

class AwakenFromDream(Action):
    def __init__(self):
        super().__init__("Awaken from a familiar dream")
        self.pass_items = {
            'Nightmares': -3,
            'RosyColours': 0
        }

# Initial setup
def setup_simulation():
    state = GameState()
    
    # Example card added to deck
    bounty_card = BountyUponYourHead()
    state.deck.append(bounty_card)
    
    return state


# Now run the simulation
if __name__ == "__main__":
    state = setup_simulation()
    state.run(steps=1000)  # Run for 1000 steps
    state.display_results()
