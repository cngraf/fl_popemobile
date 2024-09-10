import argparse
import random
import sys
from enum import Enum
from collections import defaultdict
from enums import *

ev_action = 6
ev_prog_base = 10
ev_key = 1
ev_info = 1
ev_tread_base = 4
ev_echo = 1

hand_size = 3

item_values = {
    # Stacks items
    Item.StolenCorrespondence: { Item.Echo: 0.05 },
    Item.CompromisingDocument: { Item.Echo: 0.5 },

    Item.AppallingSecret: { Item.Echo: 0.15 },

    Item.OstentatiousDiamond: { Item.Echo: 0.5 },

    Item.ConnectedTheDuchess: { Item.Echo: ev_action * 0.05 },

    Item.TouchingLoveStory: { Item.Echo: 2.50 },
    Item.CaptivatingBallad: { Item.Echo: 62.5 },

    # Menaces
    # ballpark @ 1 action to clear 6 points with social alt
    Item.Wounds: { Item.Echo: ev_action * 0.17 },
    Item.Nightmares: { Item.Echo: ev_action * 0.17 }
}

def broad_pass_rate(dc, stat_value):
    return 0.6 * stat_value/dc

def narrow_pass_rate(dc, stat_value):
    return 0.5 + (stat_value - dc) * 0.1

from enum import Enum

class HeistLocation(Enum):
    CUBIT_SQUARE = 1
    BASEBORN_FOWLINGPIECE = 2
    CONCORD_SQUARE_RECORDS = 3
    ELUSIVE_COUNTESS_MANSION = 4
    CONCORD_SQUARE_VAULT = 5
    CIRCUMSPECT_ENVOY_TOWNHOUSE = 6
    ADMIRALS_WIDOW_APARTMENTS = 7
    DISCERNING_DEVILESS_TOWNHOUSE = 8
    KHAGANIAN_DIGNITARY_RESIDENCE = 9
    UNSYMPATHETIC_LANDLORD_MANSION = 10
    TREASURE_HIDING_PLACE = 11
    MUSEUM_PRELAPSARIAN_HISTORY = 12

# def aggregate_ev_dict(state, actions):
#     total_ev = {item: 0 for item in Item}
#     for action in actions:
#         total_ev = Action.add_dicts(total_ev, action.ev_dict(state))
#     return total_ev

class HeistPlayer:
    def __init__(self):
        self.shadowy = 300
        self.dreaded = 10
        self.monstrous_anatomy = 12
        self.glasswork = 12
        self.shapeling_arts = 8
        self.has_lyrebird = True
        self.has_intricate_kifers = True


class HeistState:
    def __init__(self, info, keys, routes, target):
        self.items = {
            Item.BurglarsProgress: 0,
            Item.CatlikeTread: 3,
            Item.InsideInformation: info,
            Item.IntriguingKey: keys,
            Item.EscapeRoute: routes
        }

        self.player = HeistPlayer()
        
        self.heist_target = target
        
        if self.heist_target == HeistLocation.CUBIT_SQUARE:
            self.target_security = 1
            self.prize_value = 16.5
        elif self.heist_target == HeistLocation.BASEBORN_FOWLINGPIECE:
            self.target_security = 2
            self.prize_value = 25
        elif self.heist_target == HeistLocation.CONCORD_SQUARE_RECORDS:
            self.target_security = 2
            self.prize_value = 16
        elif self.heist_target == HeistLocation.ELUSIVE_COUNTESS_MANSION:
            self.target_security = 2
            self.prize_value = 32.5
        elif self.heist_target == HeistLocation.CONCORD_SQUARE_VAULT:
            self.target_security = 2
            self.prize_value = 4
        elif self.heist_target == HeistLocation.CIRCUMSPECT_ENVOY_TOWNHOUSE:
            self.target_security = 2
            self.prize_value = 30
        elif self.heist_target == HeistLocation.ADMIRALS_WIDOW_APARTMENTS:
            self.target_security = 3
            self.prize_value = 33.1
        elif self.heist_target == HeistLocation.DISCERNING_DEVILESS_TOWNHOUSE:
            self.target_security = 4
            self.prize_value = 62.5
        elif self.heist_target == HeistLocation.KHAGANIAN_DIGNITARY_RESIDENCE:
            # TODO: FATE locked
            self.target_security = 3
            self.prize_value = 0
        elif self.heist_target == HeistLocation.UNSYMPATHETIC_LANDLORD_MANSION:
            self.target_security = 3
            self.prize_value = 31.7
        elif self.heist_target == HeistLocation.TREASURE_HIDING_PLACE:
            self.target_security = 4
            self.prize_value = 102.5
        elif self.heist_target == HeistLocation.MUSEUM_PRELAPSARIAN_HISTORY:
            self.target_security = 3
            self.prize_value = 23

        self.refill_action = RefillHandAction()
        self.hand = []
        self.status = "InProgress"
        self.steps = 0

        self.action_history = []

        self.deck = [
            Stairs(),
            Watchman(),
            Door(),
            Place(),
            Cat(),

            Caretaker(),
            
            WeepingMaid(),
            HandyWindow(),
            Shadows(),
            Bust(),

            MomentOfSafety(),
            TinyRivals(),
            Clutter(),
            TroublesomeLock(),
            RegularDogs(),

            LookUp(),
            SheerClimb(),
            DeeperShadows(),

            Corridor(),
            Lights(),
            Rats(),
            Documents(),
            IntricateLock(),
            SpiderDogs(),

            Prize()
        ]
        
        self.card_draw_counts = {card.name: 0 for card in self.deck}
        self.card_play_counts = {card.name: 0 for card in self.deck}
        self.action_play_counts = defaultdict(int)
        self.action_success_counts = defaultdict(int)
        self.action_failure_counts = defaultdict(int)
    
    def add_items(self, item_dict):
        for item, quantity in item_dict.items():
            if item in self.items:
                self.items[item] += quantity
            else:
                self.items[item] = quantity        

    def draw_card(self):
        drawn, lowest = None, float('inf')
        for card in self.deck:
            if card not in self.hand and card.can_draw(self):
                rand = random.random() / card.weight
                if rand < lowest:
                    drawn = card
                    lowest = rand
        self.hand.append(drawn)

    def ev_items(self, items: dict[Item, int]) -> float:
        net_ev = 0

        # Calculate EV for progress, tread, keys, and information
        net_ev += self.ev_prog(items.get(Item.BurglarsProgress, 0))
        net_ev += self.ev_tread(items.get(Item.CatlikeTread, 0))
        net_ev += items.get(Item.IntriguingKey, 0) * ev_key
        net_ev += items.get(Item.InsideInformation, 0) * ev_info

        # Add the echo value for items with a price in echoes
        for item, quantity in items.items():
            if item in item_values:
                echo_value = item_values[item].get(Item.Echo, 0)
                net_ev += echo_value * quantity

        return net_ev

    def ev_prog(self, val: int) -> float:
        unit_val = ev_prog_base
        cur = self.items[Item.BurglarsProgress]

        gain = max(-1 * cur, min(val, 5 - cur))

        if cur >= 5 and cur + gain >= 5:
            return 0

        return unit_val * gain

    def ev_tread(self, val: int) -> float:
        cur = self.items[Item.CatlikeTread]
        ev = 0

        # Handling positive val correctly
        if val > 0:
            for i in range(cur + 1, cur + val + 1):
                if i == 2:
                    ev += 1.5 * ev_tread_base
                elif i == 3:
                    ev += ev_tread_base
                else:
                    ev += 0.5 * ev_tread_base      
        # Handling negative val correctly
        elif val < 0:
            for i in range(cur, cur + val, -1):  # decrementing the range
                if i == 1:
                    ev += -100 * ev_tread_base
                elif i == 2:
                    ev += -2 * ev_tread_base
                elif i == 3:
                    ev += -1 * ev_tread_base
                else:
                    ev += -0.5 * ev_tread_base

        return ev

    def ev_escape(self):
        return ev_echo * -1 * self.items[Item.CatlikeTread]
        
    def run(self):
        while self.status == "InProgress":
            self.step()

    def step(self):
        best_card, best_action, best_action_ev = None, None, -float('inf')

        if len(self.hand) == 0:
            self.refill_action.perform(self)
        elif self.refill_action.can_perform(self):
            best_action = self.refill_action
            best_action_ev = self.refill_action.ev(self)

        for card in self.hand:
            for action in card.actions:
                if action.can_perform(self):
                    action_ev = action.ev(self)
                    if action_ev > best_action_ev:
                        best_card, best_action, best_action_ev = card, action, action_ev

        if best_card is not None:
            self.steps += 1
            self.card_play_counts[best_card.name] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)

        outcome = best_action.perform(self)
        self.action_play_counts[best_action.name] += 1
        if outcome == "Success":
            self.action_success_counts[best_action.name] += 1
        else:
            self.action_failure_counts[best_action.name] += 1

        if best_card is not None:
            self.action_history.append(f"{outcome} @ {best_card.name}: {best_action.name}")            

        if self.items[Item.CatlikeTread] <= 0:
            if random.random() < 0.5:
                self.status = "Escaped"
            else:
                self.status = "Imprisoned"

            if verbose:
                print("\n---Failure Summary---")
                print(f"Status: {self.status}")
                print(f"Progress: {self.items[Item.BurglarsProgress]}")
                print("Final hand:")
                for card in self.hand: print("  " + card.name)
                print("Action History: ")
                for i in self.action_history: print(f"  {i}")
                print()


class HeistCard:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.free_progress = 0
        self.weight = 1.0

    def can_draw(self, state: HeistState):
        return True

    def ev(self, state: HeistState):
        return max(action.ev(state) for action in self.actions)

    def select_best_action(self, state: HeistState):
        return max(self.actions, key=lambda action: action.ev(state))

class Action:
    def __init__(self, name):
        self.name = name
        self.pass_items = {}
        self.fail_items = {}
        self.rare_success_rate = 0.0

    def can_perform(self, state: HeistState):
        return True
    
    def pass_rate(self, state: HeistState):
        return 1.0
                
    def ev(self, state: HeistState):
        pass_rate = min(1.0, max(0.0, self.pass_rate(state)))
        pass_ev = self.pass_ev(state)
        fail_ev = self.fail_ev(state)

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
    
    def perform(self, state: HeistState):
        rate = self.pass_rate(state)
        if random.random() <= rate:
            self.perform_pass(state)
            return "Success"
        else:
            self.perform_fail(state)
            return "Failure"

    def perform_pass(self, state: HeistState):
        state.add_items(self.pass_items)

    def perform_fail(self, state: HeistState):
        state.add_items(self.fail_items)

    # # Method that combines pass_ev_dict and fail_ev_dict based on pass_rate
    # def ev_dict(self, state: HeistState):
    #     pass_rate = self.pass_rate(state)
    #     pass_ev = state
    #     fail_ev = self.fail_ev_dict(state)

    #     # Combine pass and fail EVs weighted by the pass rate
    #     combined_ev = {item: (pass_rate * pass_ev.get(item, 0)) + ((1 - pass_rate) * fail_ev.get(item, 0))
    #                    for item in set(pass_ev) | set(fail_ev)}
    #     return combined_ev

    def pass_ev(self, state: HeistState):
        return state.ev_items(self.pass_items)

    def fail_ev(self, state: HeistState):
        return state.ev_items(self.fail_items)
    
    # A utility function to add two dictionaries item-wise
    @staticmethod
    def add_dicts(dict1, dict2):
        return {key: dict1.get(key, 0) + dict2.get(key, 0) for key in set(dict1) | set(dict2)}
        
    
class RefillHandAction(Action):
    def __init__(self):
        super().__init__("Redraw")

    def can_perform(self, state: HeistState):
        return len(state.hand) < hand_size

    def perform_pass(self, state: HeistState):
        while len(state.hand) < hand_size:
            state.draw_card()

    def pass_ev(self, state: HeistState):
        return ev_prog_base

# Card and Action implementations

class Stairs(HeistCard):
    def __init__(self):
        super().__init__("Winding Stairs")
        self.actions = [StairsAction1(), StairsAction2(), StairsAction3()]

class StairsAction1(Action):
    def __init__(self):
        super().__init__("Upstairs. That's probably right")
        self.pass_items = {
            Item.BurglarsProgress: 2
        }

    def pass_rate(self, state: HeistState):
        # Luck
        return 0.7

class StairsAction2(Action):
    def __init__(self):
        super().__init__("Play it safe")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }        

class StairsAction3(Action):
    def __init__(self):
        super().__init__("Pry into a side door")
        self.pass_items = {
            Item.IntriguingKey: -1,
            Item.OstentatiousDiamond: 3,
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.IntriguingKey] > 0
    
class Watchman(HeistCard):
    def __init__(self):
        super().__init__("A Burly Night-Watchman")
        self.actions = [WatchmanAction1(),
                        WatchmanAction2(),
                        WatchmanAction3(),
                        WatchmanAction4(),
                        WatchmanAction5(),]

class WatchmanAction1(Action):
    def __init__(self):
        super().__init__("Go through")
        self.pass_items = {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: 1
        }

class WatchmanAction2(Action):
    def __init__(self):
        super().__init__("Wait a few minutes")
        self.pass_items = {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: -1
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0

    def pass_rate(self, state: HeistState):
        return 0.7
    
class WatchmanAction3(Action):
    def __init__(self):
        super().__init__("Get out of my way")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

        self.fail_items = {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -2
        }

    def pass_rate(self, state: HeistState):
        return narrow_pass_rate(5, state.player.dreaded)

class WatchmanAction4(Action):
    def __init__(self):
        super().__init__("Deploy your Lyrebird")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

    def can_perform(self, state: HeistState):
        return state.player.has_lyrebird

class WatchmanAction5(Action):
    def __init__(self):
        super().__init__("...go back")
        self.pass_items = {
            Item.BurglarsProgress: -1
        }

class Door(HeistCard):
    def __init__(self):
        super().__init__("A Promising Door")
        self.actions = [DoorAction1(),
                        DoorAction2()]

class DoorAction1(Action):
    def __init__(self):
        super().__init__("Forward planning")
        self.pass_items = {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0
    
class DoorAction2(Action):
    def __init__(self):
        super().__init__("Chance it")
        self.pass_items = {
            Item.BurglarsProgress: 2
        }
        self.fail_items = {
            Item.CatlikeTread: -2
        }

    def pass_rate(self, state: HeistState):
        return 0.5
    
    def ev(self, state: HeistState):
        if any(card.__class__ in [MomentOfSafety, Lights] for card in state.hand) and \
            state.items[Item.CatlikeTread] > 2:
            return super().ev(state)
        else:
            return -10


class Place(HeistCard):
    def __init__(self):
        super().__init__("A Clean Well-Lighted Place")
        self.actions = [PlaceAction1(),
                        PlaceAction2(),
                        PlaceAction3()]

class PlaceAction1(Action):
    def __init__(self):
        super().__init__("Snaffle documents")
        self.pass_items = {
            Item.CompromisingDocument: 9,
            Item.StolenCorrespondence: 20,
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.CatlikeTread: -2
        }

    def pass_rate(self, state: HeistState):
        return 0.5

class PlaceAction2(Action):
    def __init__(self):
        super().__init__("Pass through the study")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

    def pass_rate(self, state: HeistState):
        return 0.8
    
class PlaceAction3(Action):
    def __init__(self):
        super().__init__("Wait")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0

class Cat(HeistCard):
    def __init__(self):
        super().__init__("A Talkative Cat")
        self.actions = [CatAction1(),
                        CatAction2(),
                        CatAction3()]

class CatAction1(Action):
    def __init__(self):
        super().__init__("Trade on your connections")
        self.pass_items = {
            Item.ConnectedTheDuchess: -3,
            Item.BurglarsProgress: 1
        }

    # def can_perform(self, state: HeistState):
    #     # TODO: Connected Duchess >= 20

class CatAction2(Action):
    def __init__(self):
        super().__init__("Grab the beast")
        self.pass_items = {
            Item.ConnectedTheDuchess: -10,
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.ConnectedTheDuchess: -10,
            Item.CatlikeTread: -2
        }

    def pass_rate(self, state: HeistState):
        return 0.5

class CatAction3(Action):
    def __init__(self):
        super().__init__("Bribe it with secrets")
        self.pass_items = {
            Item.AppallingSecret: -10,
            Item.BurglarsProgress: 1
        }

class Caretaker(HeistCard):
    def __init__(self):
        super().__init__("A Nosy Caretaker")
        self.actions = [CaretakerAction1(),
                        CaretakerAction2()]

    def can_draw(self, state: HeistState):
        return state.items[Item.EscapeRoute] > 0 
    
class CaretakerAction1(Action):
    def __init__(self):
        super().__init__("Deal with him before he cuts off your escape")
        self.fail_items = {
            Item.CatlikeTread: -2
        }
    
    def pass_rate(self, state: HeistState):
        return 0.6

class CaretakerAction2(Action):
    def __init__(self):
        super().__init__("Let it go")
        self.pass_items = {
            Item.EscapeRoute: -1,
            Item.BurglarsProgress: 1
        }

class WeepingMaid(HeistCard):
    def __init__(self):
        super().__init__("A Weeping Maid")
        self.actions = [WeepingMaidAction1(),
                        WeepingMaidAction2()]
        self.weight = 0.2

    def can_draw(self, state: HeistState):
        return state.target_security < 2
    
class WeepingMaidAction1(Action):
    def __init__(self):
        super().__init__("Avoid her")
        self.fail_items = {
            Item.BurglarsProgress: 1
        }

class WeepingMaidAction2(Action):
    def __init__(self):
        super().__init__("Speak to her")
        self.fail_items = {
            Item.BurglarsProgress: -1
        }        

# TODO: 3rd action
class LookUp(HeistCard):
    def __init__(self):
        super().__init__("Look up...")
        self.actions = [LookUpAction1(),
                        LookUpAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 2

class LookUpAction1(Action):
    def __init__(self):
        super().__init__("Move slowly past")
        self.fail_items = {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1,
            Item.Wounds: 1
        }
    
    def pass_rate(self, state: HeistState):
        return 0.3
    
class LookUpAction2(Action):
    def __init__(self):
        super().__init__("Dash past")
        self.success_items = {
            Item.BurglarsProgress: 1,
            Item.CatlikeTread: -1
        }
        self.fail_items = {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1,
        }
    
    def pass_rate(self, state: HeistState):
        return 0.6
    
# TODO: escape action
class HandyWindow(HeistCard):
    def __init__(self):
        super().__init__("A Sheer Climb")
        self.actions = [HandyWindowAction2()]
        self.weight = 0.2

    def can_draw(self, state: HeistState):
        return state.target_security < 2
    
class HandyWindowAction1(Action):
    def __init__(self):
        super().__init__("Escape! (Window)")

    def perform_pass(self, state: HeistState):
        state.status = "Escaped"
    
    def pass_ev(self, state: HeistState):
        return state.ev_escape()

class HandyWindowAction2(Action):
    def __init__(self):
        super().__init__("Climb the wall")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

# TODO: escape action
class SheerClimb(HeistCard):
    def __init__(self):
        super().__init__("A Sheer Climb")
        self.actions = [SheerClimbAction1(),
                        SheerClimbAction2(),
                        SheerClimbAction3()]
        self.weight = 0.2

    def can_draw(self, state: HeistState):
        return state.target_security >= 2
    
class SheerClimbAction1(Action):
    def __init__(self):
        super().__init__("Escape! (Climb)")

    def perform_pass(self, state: HeistState):
        state.status = "Escaped"
    
    def pass_ev(self, state: HeistState):
        return state.ev_escape()

class SheerClimbAction2(Action):
    def __init__(self):
        super().__init__("An uncertain path")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

    def pass_ev(self, state: HeistState):
        return 0.5
    
class SheerClimbAction3(Action):
    def __init__(self):
        super().__init__("Foresight")
        self.pass_items = {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 1
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0

class Shadows(HeistCard):
    def __init__(self):
        super().__init__("Through the Shadows")
        self.actions = [ShadowsAction1(), ShadowsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security < 2

# TODO rare success
class ShadowsAction1(Action):
    def __init__(self):
        super().__init__("And here you are hard at work")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

class ShadowsAction2(Action):
    def __init__(self):
        super().__init__("Work wisely, not hard")
        self.pass_items = {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }        

class DeeperShadows(HeistCard):
    def __init__(self):
        super().__init__("Through Deeper Shadows")
        self.actions = [DeeperShadowsAction1(), DeeperShadowsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 2        

class DeeperShadowsAction1(Action):
    def __init__(self):
        super().__init__("Blend into the Shadows")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.BurglarsProgress: -1
        }

    def pass_rate(self, state: HeistState):
        return 0.5
    
    def perform_fail(self, state: HeistState):
        state.items[Item.BurglarsProgress] = max(0, state.items[Item.BurglarsProgress] - 1)

    def fail_ev(self, state: HeistState):
        if state.items[Item.BurglarsProgress] == 1:
            return 0
        else:
            return state.ev_items(self.fail_items)    

class DeeperShadowsAction2(Action):
    def __init__(self):
        super().__init__("These ways are strange")
        self.pass_items = {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0

class Bust(HeistCard):
    def __init__(self):
        super().__init__("An Alarming Bust")
        self.actions = [BustAction1(),
                        BustAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security < 2        

class BustAction1(Action):
    def __init__(self):
        super().__init__("Oh, it's just that bloody bust of the Consort")
        self.pass_items = {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }        

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0
    
class BustAction2(Action):
    def __init__(self):
        super().__init__("Aaagh!")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }
        self.pass_items = {
            Item.CatlikeTread: -1
        }                

    def pass_rate(self, state: HeistState):
        return 0.5

class Corridor(HeistCard):
    def __init__(self):
        super().__init__("A Menacing Corridor")
        self.actions = [CorridorAction1(),
                        CorridorAction2(),
                        CorridorAction3()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 2        

class CorridorAction1(Action):
    def __init__(self):
        super().__init__("It's safe tonight...")
        self.pass_items = {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }        

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0
    
class CorridorAction2(Action):
    def __init__(self):
        super().__init__("Is it safe?")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.CatlikeTread: -1
        }
    
    def pass_rate(self, state: HeistState):
        return 0.3
    
class CorridorAction3(Action):
    def __init__(self):
        super().__init__("Blindfold yourself")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.CatlikeTread: -1
        }

    def can_perform(self, state: HeistState):
        return state.player.shadowy >= 100

    def pass_rate(self, state: HeistState):
        return 0.5

# TODO: FATE option?
class MomentOfSafety(HeistCard):
    def __init__(self):
        super().__init__("A Moment of Safety")
        self.actions = [MomentOfSafetyAction1()]

    def can_draw(self, state: HeistState):
        return state.target_security < 3
    
class MomentOfSafetyAction1(Action):
    def __init__(self):
        super().__init__("Hide for a little while")
        self.pass_items = {
            Item.CatlikeTread: 1
        }

    def perform_pass(self, state: HeistState):
        state.items[Item.CatlikeTread] = min(3, state.items[Item.CatlikeTread] + 1)

    def pass_ev(self, state: HeistState):
        if state.items[Item.CatlikeTread] >= 3:
            return 0
        else:
            return state.ev_items(self.pass_items)

# TODO: FATE option?
class Lights(HeistCard):
    def __init__(self):
        super().__init__("Consider the Lights")
        self.actions = [LightsAction1()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 3        

class LightsAction1(Action):
    def __init__(self):
        super().__init__("Shut off the lights")
        self.pass_items = {
            Item.CatlikeTread: 1
        }

    def perform_pass(self, state: HeistState):
        state.items[Item.CatlikeTread] = min(3, state.items[Item.CatlikeTread] + 1)

    def pass_ev(self, state: HeistState):
        if state.items[Item.CatlikeTread] >= 3:
            return 0
        else:
            return state.ev_items(self.pass_items)

class TinyRivals(HeistCard):
    def __init__(self):
        super().__init__("Tiny Rivals")
        self.actions = [TinyRivalsAction1(),
                        TinyRivalsAction2(),
                        TinyRivalsAction3()]

    def can_draw(self, state: HeistState):
        return state.target_security < 3        

class TinyRivalsAction1(Action):
    def __init__(self):
        super().__init__("\"Well-met, thieflings!\"")
        self.pass_items = {
            Item.InsideInformation: 1
        }
        self.pass_items = {
            Item.CatlikeTread: -1,
            Item.Wounds: 2
        }        

    def pass_rate(self, state: HeistState):
        return 0.7

class TinyRivalsAction2(Action):
    def __init__(self):
        super().__init__("Hang back")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

class TinyRivalsAction3(Action):
    def __init__(self):
        super().__init__("Sapphires?")
        self.pass_items = {
            Item.Sapphire: 15,
            Item.CatlikeTread: -1
        }


class Rats(HeistCard):
    def __init__(self):
        super().__init__("The Rats in the Walls")
        self.actions = [RatsAction1(), RatsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 3        

class RatsAction1(Action):
    def __init__(self):
        super().__init__("Move in utter silence")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.CatlikeTread: -1,
            Item.Wounds: 1
        }

    def pass_rate(self, state: HeistState):
        return broad_pass_rate(120, state.player.shadowy)
    
class RatsAction2(Action):
    def __init__(self):
        super().__init__("Avoid their nests")
        self.pass_items = {
            Item.BurglarsProgress: 1,
            Item.InsideInformation: -1
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0

class Clutter(HeistCard):
    def __init__(self):
        super().__init__("A clutter of bric-a-brac")
        self.actions = [ClutterAction1(), ClutterAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security < 3

# TODO: rare success, alt failure?
class ClutterAction1(Action):
    def __init__(self):
        super().__init__("Poke through the possibilities")
        self.pass_items = {
            Item.MoonPearl: 30,
            Item.OstentatiousDiamond: 1
        }
        self.fail_items = {
            Item.CatlikeTread: -1
        }
        self.rare_success_rate = 0.1 # guess

    def pass_rate(self, state: HeistState):
        return 0.7

class ClutterAction2(Action):
    def __init__(self):
        super().__init__("Play it safe")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

# TODO: other action w/ rare success
class Documents(HeistCard):
    def __init__(self):
        super().__init__("Mislaid Documnets")
        self.actions = [DocumentsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 3

class DocumentsAction2(Action):
    def __init__(self):
        super().__init__("Move along")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }

class TroublesomeLock(HeistCard):
    def __init__(self):
        super().__init__("An Intricate Lock")
        self.actions = [TroublesomeLockAction1(),
                        TroublesomeLockAction2(),
                        TroublesomeLockAction3(),
                        TroublesomeLockAction4(),
                        TroublesomeLockAction5()]

    def can_draw(self, state: HeistState):
        return state.target_security < 4

class TroublesomeLockAction1(Action):
    def __init__(self):
        super().__init__("There may be an easier way")
        self.pass_items = {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0
    
class TroublesomeLockAction2(Action):
    def __init__(self):
        super().__init__("What about that key?")
        self.pass_items = {
            Item.IntriguingKey: -1,
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.IntriguingKey] > 0
    
class TroublesomeLockAction3(Action):
    def __init__(self):
        super().__init__("Use your Kifers")
        self.pass_items = {
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        # TODO really no reason to have this card
        return True
    
    def pass_rate(self, state: HeistState):
        return 0.4
    
class TroublesomeLockAction4(Action):
    def __init__(self):
        super().__init__("Use your Intricate Kifers")
        self.pass_items = {
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        # TODO
        return True
    
    def pass_rate(self, state: HeistState):
        return 0.6
    
class TroublesomeLockAction5(Action):
    def __init__(self):
        super().__init__("Try your luck")
        self.pass_items = {
            Item.BurglarsProgress: 2
        }

    def pass_rate(self, state: HeistState):
        return 0.3

class IntricateLock(HeistCard):
    def __init__(self):
        super().__init__("An Intricate Lock")
        self.actions = [IntricateLockAction1(), IntricateLockAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 4

class IntricateLockAction1(Action):
    def __init__(self):
        super().__init__("Pick the lock in Parabola")
        self.pass_items = {
            Item.BurglarsProgress: 2
        }

    def pass_rate(self, state: HeistState):
        return narrow_pass_rate(7, state.player.glasswork)
    
class IntricateLockAction2(Action):
    def __init__(self):
        super().__init__("Use your key")
        self.pass_items = {
            Item.IntriguingKey: -1,
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.IntriguingKey] > 0

# TODO stat challenges
class RegularDogs(HeistCard):
    def __init__(self):
        super().__init__("Sleeping... Dogs?")
        self.actions = [RegularDogsAction1(), RegularDogsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security < 4

class RegularDogsAction1(Action):
    def __init__(self):
        super().__init__("Creep past")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1,
        }

    def pass_rate(self, state: HeistState):
        return 0.4

class RegularDogsAction2(Action):
    def __init__(self):
        super().__init__("Dash past")
        self.pass_items = {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1,
        }

    def pass_rate(self, state: HeistState):
        return 0.7


class SpiderDogs(HeistCard):
    def __init__(self):
        super().__init__("Sleeping... Dogs?")
        self.actions = [SpiderDogsAction1(), SpiderDogsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 4

class SpiderDogsAction1(Action):
    def __init__(self):
        super().__init__("Creep past them")
        self.pass_items = {
            Item.BurglarsProgress: 1
        }
        self.fail_items = {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1,
            Item.Nightmares: 4
        }

    def pass_rate(self, state: HeistState):
        return narrow_pass_rate(7, state.player.monstrous_anatomy)
    
class SpiderDogsAction2(Action):
    def __init__(self):
        super().__init__("Offer them a spare eyeball")
        self.pass_items = {
            Item.BurglarsProgress: 1,
            Item.InsideInformation: -1
        }

    def can_perform(self, state: HeistState):
        return state.items[Item.InsideInformation] > 0 and \
        state.player.shapeling_arts >= 8


class Prize(HeistCard):
    def __init__(self):
        super().__init__("Prize")
        self.actions = [PrizeAction1()]
        self.weight = 10

    def can_draw(self, state: HeistState):
        return state.items[Item.BurglarsProgress] >= 5
    

class PrizeAction1(Action):
    def __init__(self):
        super().__init__("Claim the Prize")

    def ev(self, state: HeistState):
        return 100
    
    def perform(self, state: HeistState):
        state.add_items({
            Item.Echo: state.prize_value
        })
        state.status = "Success"

# Run the simulation
from collections import defaultdict

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
    
def print_action_table(action_play_counts, action_success_counts, action_failure_counts, deck):
    print(f"\n{'Card':<30}{'Action':<30}{'Avg Played':<10}{'Success Rate':<15}")
    print("-" * 95)
    for card in deck:
        print(f"{card.name:<30}")
        for action in card.actions:
            avg_played = action_play_counts.get(action.name, 0) / runs
            successes = action_success_counts.get(action.name, 0)
            failures = action_failure_counts.get(action.name, 0)
            total = successes + failures
            success_rate = (successes / total) * 100 if total > 0 else 0
            print(f"{'':<30}{action.name:<30}{avg_played:<10.2f}{success_rate:.2f}%")
        print("-" * 95)

def calculate_echoes(items):
    """Calculates the total echo value of the given items."""
    total_echoes = items.get(Item.Echo, 0)
    for item, quantity in items.items():
        if item in item_values:
            echo_value = item_values[item].get(Item.Echo, 0)
            total_echoes += echo_value * quantity
    return total_echoes

# Simulation parameters
parser = argparse.ArgumentParser(description='Run Heist simulation.')
parser.add_argument('--keys', type=int, default=0, help='Initial number of keys')
parser.add_argument('--info', type=int, default=0, help='Initial amount of inside info')
parser.add_argument('--routes', type=int, default=0, help='Initial amount of escape routes')
parser.add_argument('--runs', type=int, default=10_000, help='Number of runs to simulate')
parser.add_argument('--target', type=int, default=11, help='Target location as integer (use numbers 1-12)')

parser.add_argument('--verbose', action='store_true', help='Log action history on failures')

args = parser.parse_args()

# Command-line input parameters
keys = args.keys
info = args.info
runs = args.runs
routes = args.routes
verbose = args.verbose

try:
    target = HeistLocation(args.target)
except ValueError:
    print(f"Invalid target value. Please provide a number between 1 and {len(HeistLocation)}.")
    exit(1)

successes = 0
success_steps = 0
escapes = 0
escape_steps = 0
imprisonments = 0
imprisonment_steps = 0
total_echoes = 0

total_action_play_counts = defaultdict(int)
total_action_success_counts = defaultdict(int)
total_action_failure_counts = defaultdict(int)

for i in range(runs):
    heist = HeistState(info=info, keys=keys, routes=routes, target=target)
    heist.run()

    if heist.status == "Success":
        successes += 1
        success_steps += heist.steps
    elif heist.status == "Escaped":
        escapes += 1
        escape_steps += heist.steps
    else:
        imprisonments += 1
        imprisonment_steps += heist.steps

    # Aggregate action play counts
    for action, count in heist.action_play_counts.items():
        total_action_play_counts[action] += count
    for action, count in heist.action_success_counts.items():
        total_action_success_counts[action] += count
    for action, count in heist.action_failure_counts.items():
        total_action_failure_counts[action] += count

    # Calculate total echoes for the run
    total_echoes += calculate_echoes(heist.items)

    update_progress(i / runs)

update_progress(1.0)
print()

avg_success_steps = success_steps/successes if successes > 0 else 0
# Summary of simulation
print(f"Completed {runs} runs with {info} Info & {keys} Keys.")
print(f"{successes/runs:.2%} success rate, in avg {avg_success_steps:.2f} steps")
print(f"{escapes/runs:.2%} escape rate, in avg {escape_steps/max(escapes, 1):.2f} steps")
print(f"{imprisonments/runs:.2%} fail rate, in avg {imprisonment_steps/max(imprisonments, 1):.2f} steps")

# Calculate and print the average echoes gained per run
avg_echoes_per_run = total_echoes / runs
print(f"Average echoes gained per run: {avg_echoes_per_run:.2f} echoes")
# print(f"Average EPA per run: {avg_echoes_per_run/avg_success_steps if successes > 0 else 0:.2f} echoes")

# Print the action table with the collected data, grouped by card
print_action_table(total_action_play_counts, total_action_success_counts, total_action_failure_counts, heist.deck)