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

heist_targets = {
    HeistLocation.CUBIT_SQUARE: {
        Item.TargetSecurity: 1,
        Item._ApproximateEchoValue: 16.5
    },
    HeistLocation.BASEBORN_FOWLINGPIECE: {
        Item.TargetSecurity: 2,
        Item._ApproximateEchoValue: 25
    },
    HeistLocation.CONCORD_SQUARE_RECORDS: {
        Item.TargetSecurity: 2,
        Item._ApproximateEchoValue: 16
    },
    HeistLocation.ELUSIVE_COUNTESS_MANSION: {
        Item.TargetSecurity: 2,
        Item._ApproximateEchoValue: 32.5
    },
    HeistLocation.CONCORD_SQUARE_VAULT: {
        Item.TargetSecurity: 2,
        Item._ApproximateEchoValue: 4
    },
    HeistLocation.CIRCUMSPECT_ENVOY_TOWNHOUSE: {
        Item.TargetSecurity: 2,
        Item._ApproximateEchoValue: 30
    },
    HeistLocation.ADMIRALS_WIDOW_APARTMENTS: {
        Item.TargetSecurity: 3,
        Item._ApproximateEchoValue: 33.1
    },
    HeistLocation.DISCERNING_DEVILESS_TOWNHOUSE: {
        Item.TargetSecurity: 4,
        Item._ApproximateEchoValue: 62.5
    },
    HeistLocation.KHAGANIAN_DIGNITARY_RESIDENCE: {
        Item.TargetSecurity: 3,
        Item._ApproximateEchoValue: 0  # TODO: FATE locked
    },
    HeistLocation.UNSYMPATHETIC_LANDLORD_MANSION: {
        Item.TargetSecurity: 3,
        Item._ApproximateEchoValue: 31.7
    },
    HeistLocation.TREASURE_HIDING_PLACE: {
        Item.TargetSecurity: 4,
        Item._ApproximateEchoValue: 102.5
    },
    HeistLocation.MUSEUM_PRELAPSARIAN_HISTORY: {
        Item.TargetSecurity: 3,
        Item._ApproximateEchoValue: 23
    }
}

class HeistState(GameState):
    def __init__(self, heist_target: HeistLocation):
        super().__init__(max_hand_size=3)

        location = HeistLocation(heist_target)
        self.target_security = heist_targets[location][Item.TargetSecurity]
        self.prize_value = heist_targets[location][Item._ApproximateEchoValue]

        self.progress_required = 5
        if location == HeistLocation.BASEBORN_FOWLINGPIECE:
            self.progress_required = 7

        self.items[Item.BurglarsProgress] = 0
        self.status = "InProgress"

    def ev_from_item(self, item, val: int):
        ev_prog_base = 10
        ev_tread_base = 4
        ev_key = 1
        ev_info = 1

        if item == Item.BurglarsProgress:
            return self.ev_progress(val, ev_prog_base)
        elif item == Item.CatlikeTread:
            return self.ev_tread(val, ev_tread_base)
        elif item == Item.IntriguingKey:
            return ev_key * val
        elif item == Item.InsideInformation:
            return ev_info * val
        else:
            return val * conversion_rate(item, Item.Echo)

    def ev_progress(self, val: int, base_ev: int) -> float:
        cur = self.items[Item.BurglarsProgress]
        gain = max(-1 * cur, min(val, 5 - cur))

        if cur >= 5 and cur + gain >= 5:
            return 0

        return base_ev * gain

    def ev_tread(self, val: int, ev_tread_base: int) -> float:
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

    # TODO
    # def ev_escape(self):
    #     return ev_echo * -1 * self.items[Item.CatlikeTread]
        
    def run(self):
        while self.status == "InProgress":
            self.step()

    def step(self):
        best_card, best_action, best_action_ev = self.find_best_action()

        if best_action:
            result = best_action.perform(self)
            self.actions += best_action.action_cost
            self.action_result_counts[best_action][result] += 1

            if best_card is not None:
                self.card_play_counts[best_card] += 1
                if best_card in self.hand:
                    self.hand.remove(best_card)

class StoryletOnAHeist(OpportunityCard):
    def __init__(self):
        super().__init__("Storylet: On A Heist")
        self.actions = [
            RefillHand(),
        ]

class RefillHand(Action):
    def __init__(self):
        super().__init__("(REFILL HAND)")
        self.action_cost = 0

    def can_perform(self, state: GameState):
        return len(state.hand) < state.max_hand_size
    
    def perform(self, state: GameState):
        while len(state.hand) < state.max_hand_size:
            state.draw_card()
        return ActionResult.Pass

    def ev(self, state: GameState):
        return 5
    
class SkinOfYourTeeth(OpportunityCard):
    def __init__(self):
        super().__init__("The skin of your teeth")
        self.actions = [
            UpAndAway()
        ]
        self.autofire = True
    
    def can_draw(self, state: HeistState):
        return state.get(Item.CatlikeTread) < 1

class UpAndAway(Action):
    def __init__(self):
        super().__init__("Up and away!")

    def pass_items(self, state: GameState):
        return {
            Item.Suspicion: 4
        }

    def perform_pass(self, state: HeistState):
        result = super().perform_pass(state)
        state.status = "Escaped"
        return result

    def perform_failure(self, state: HeistState):
        result = super().perform_failure(state)
        state.status = "Imprisoned"
        return result
    
    def pass_rate(self, state: HeistState):
        return 0.5


# Card and Action implementations

################################################################################
###                           Winding Stairs                                  ###
################################################################################

class Stairs(OpportunityCard):
    def __init__(self):
        super().__init__("Winding Stairs")
        self.actions = [StairsAction1(), StairsAction2(), StairsAction3()]

class StairsAction1(Action):
    def __init__(self):
        super().__init__("Upstairs. That's probably right")

    def pass_rate(self, state: HeistState):
        return 0.7  # Luck

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 2
        }


class StairsAction2(Action):
    def __init__(self):
        super().__init__("Play it safe")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }


class StairsAction3(Action):
    def __init__(self):
        super().__init__("Pry into a side door")

    def can_perform(self, state: HeistState):
        return state.items.get(Item.IntriguingKey, 0) > 0

    def pass_items(self, state: HeistState):
        return {
            Item.IntriguingKey: -1,
            Item.OstentatiousDiamond: 3,
            Item.BurglarsProgress: 2
        }


################################################################################
###                        A Burly Night-Watchman                             ###
################################################################################

class Watchman(OpportunityCard):
    def __init__(self):
        super().__init__("A Burly Night-Watchman")
        self.actions = [
            WatchmanAction1(),
            WatchmanAction2(),
            WatchmanAction3(),
            WatchmanAction4(),
            WatchmanAction5()
        ]

class WatchmanAction1(Action):
    def __init__(self):
        super().__init__("Go through")

    def pass_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: 1
        }


class WatchmanAction2(Action):
    def __init__(self):
        super().__init__("Wait a few minutes")

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0

    def pass_rate(self, state: HeistState):
        return 0.7

    def pass_items(self, state: HeistState):
        return {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: -1
        }


class WatchmanAction3(Action):
    def __init__(self):
        super().__init__("Get out of my way")

    def pass_rate(self, state: HeistState):
        return self.narrow_pass_rate(5, state.outfit.dreaded)

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -2
        }


class WatchmanAction4(Action):
    def __init__(self):
        super().__init__("Deploy your Lyrebird")

    def can_perform(self, state: HeistState):
        return state.get(Item.UntrainedLyrebird)

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }


class WatchmanAction5(Action):
    def __init__(self):
        super().__init__("...go back")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: -1
        }


################################################################################
###                         A Promising Door                                  ###
################################################################################

class Door(OpportunityCard):
    def __init__(self):
        super().__init__("A Promising Door")
        self.actions = [DoorAction1(), DoorAction2()]

class DoorAction1(Action):
    def __init__(self):
        super().__init__("Forward planning")

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0

    def pass_items(self, state: HeistState):
        return {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }


class DoorAction2(Action):
    def __init__(self):
        super().__init__("Chance it")

    def pass_rate(self, state: HeistState):
        return 0.5

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 2
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -2
        }

    # def ev(self, state: HeistState):
    #     if any(card.__class__ in [MomentOfSafety, Lights] for card in state.hand) and \
    #             state.items.get(Item.CatlikeTread, 0) > 2:
    #         return super().ev(state)
    #     else:
    #         return -10


################################################################################
###                      A Clean Well-Lighted Place                           ###
################################################################################

class Place(OpportunityCard):
    def __init__(self):
        super().__init__("A Clean Well-Lighted Place")
        self.actions = [PlaceAction1(), PlaceAction2(), PlaceAction3()]

class PlaceAction1(Action):
    def __init__(self):
        super().__init__("Snaffle documents")

    def pass_rate(self, state: HeistState):
        return 0.5

    def pass_items(self, state: HeistState):
        return {
            Item.CompromisingDocument: 9,
            Item.StolenCorrespondence: 20,
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -2
        }

class PlaceAction2(Action):
    def __init__(self):
        super().__init__("Pass through the study")

    def pass_rate(self, state: HeistState):
        return 0.8

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

class PlaceAction3(Action):
    def __init__(self):
        super().__init__("Wait")

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }


################################################################################
###                          A Talkative Cat                                  ###
################################################################################

class Cat(OpportunityCard):
    def __init__(self):
        super().__init__("A Talkative Cat")
        self.actions = [CatAction1(), CatAction2(), CatAction3()]

class CatAction1(Action):
    def __init__(self):
        super().__init__("Trade on your connections")

    def pass_items(self, state: HeistState):
        return {
            Item.ConnectedTheDuchess: -3,
            Item.BurglarsProgress: 1
        }

class CatAction2(Action):
    def __init__(self):
        super().__init__("Grab the beast")

    def pass_rate(self, state: HeistState):
        return 0.5

    def pass_items(self, state: HeistState):
        return {
            Item.ConnectedTheDuchess: -10,
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.ConnectedTheDuchess: -10,
            Item.CatlikeTread: -2
        }

class CatAction3(Action):
    def __init__(self):
        super().__init__("Bribe it with secrets")

    def pass_items(self, state: HeistState):
        return {
            Item.AppallingSecret: -10,
            Item.BurglarsProgress: 1
        }

################################################################################
###                          A Nosy Caretaker                                 ###
################################################################################

class Caretaker(OpportunityCard):
    def __init__(self):
        super().__init__("A Nosy Caretaker")
        self.actions = [CaretakerAction1(), CaretakerAction2()]

    def can_draw(self, state: HeistState):
        return state.items.get(Item.EscapeRoute, 0) > 0


class CaretakerAction1(Action):
    def __init__(self):
        super().__init__("Deal with him before he cuts off your escape")

    def pass_rate(self, state: HeistState):
        return 0.6

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -2
        }


class CaretakerAction2(Action):
    def __init__(self):
        super().__init__("Let it go")

    def pass_items(self, state: HeistState):
        return {
            Item.EscapeRoute: -1,
            Item.BurglarsProgress: 1
        }


################################################################################
###                             A Weeping Maid                                ###
################################################################################

class WeepingMaid(OpportunityCard):
    def __init__(self):
        super().__init__("A Weeping Maid")
        self.actions = [WeepingMaidAction1(), WeepingMaidAction2()]
        self.weight = 0.2

    def can_draw(self, state: HeistState):
        return state.target_security < 2


class WeepingMaidAction1(Action):
    def __init__(self):
        super().__init__("Avoid her")

    def fail_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }


class WeepingMaidAction2(Action):
    def __init__(self):
        super().__init__("Speak to her")

    def fail_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: -1
        }


################################################################################
###                             Look up...                                    ###
################################################################################

class LookUp(OpportunityCard):
    def __init__(self):
        super().__init__("Look up...")
        self.actions = [LookUpAction1(), LookUpAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 2

class LookUpAction1(Action):
    def __init__(self):
        super().__init__("Move slowly past")

    def pass_rate(self, state: HeistState):
        return 0.3

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1,
            Item.Wounds: 1
        }

class LookUpAction2(Action):
    def __init__(self):
        super().__init__("Dash past")

    def pass_rate(self, state: HeistState):
        return 0.6

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1,
            Item.CatlikeTread: -1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1
        }
################################################################################
###                           A Sheer Climb                                   ###
################################################################################

class HandyWindow(OpportunityCard):
    def __init__(self):
        super().__init__("A Sheer Climb")
        self.actions = [HandyWindowAction1(), HandyWindowAction2()]
        self.weight = 0.2

    def can_draw(self, state: HeistState):
        return state.target_security < 2

class HandyWindowAction1(Action):
    def __init__(self):
        super().__init__("Escape! (Window)")

    def perform_pass(self, state: GameState):
        result = super().perform_pass(state)
        state.status = "Escaped"
        return result

class HandyWindowAction2(Action):
    def __init__(self):
        super().__init__("Climb the wall")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }


################################################################################
###                          A Sheer Climb (High Security)                    ###
################################################################################

class SheerClimb(OpportunityCard):
    def __init__(self):
        super().__init__("A Sheer Climb")
        self.actions = [SheerClimbAction1(), SheerClimbAction2(), SheerClimbAction3()]
        self.weight = 0.2

    def can_draw(self, state: HeistState):
        return state.target_security >= 2


class SheerClimbAction1(Action):
    def __init__(self):
        super().__init__("Escape! (Climb)")

    def perform_pass(self, state: HeistState):
        super().perform_pass(state)        
        state.status = "Escaped"

class SheerClimbAction2(Action):
    def __init__(self):
        super().__init__("An uncertain path")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

    def pass_ev(self, state: HeistState):
        return 0.5


class SheerClimbAction3(Action):
    def __init__(self):
        super().__init__("Foresight")

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0

    def pass_items(self, state: HeistState):
        return {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 1
        }


################################################################################
###                          Through the Shadows                              ###
################################################################################

class Shadows(OpportunityCard):
    def __init__(self):
        super().__init__("Through the Shadows")
        self.actions = [ShadowsAction1(), ShadowsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security < 2


class ShadowsAction1(Action):
    def __init__(self):
        super().__init__("And here you are hard at work")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }


class ShadowsAction2(Action):
    def __init__(self):
        super().__init__("Work wisely, not hard")

    def pass_items(self, state: HeistState):
        return {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }


################################################################################
###                         Through Deeper Shadows                            ###
################################################################################

class DeeperShadows(OpportunityCard):
    def __init__(self):
        super().__init__("Through Deeper Shadows")
        self.actions = [DeeperShadowsAction1(), DeeperShadowsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 2

class DeeperShadowsAction1(Action):
    def __init__(self):
        super().__init__("Blend into the Shadows")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: -1
        }

    def pass_rate(self, state: HeistState):
        return 0.5

class DeeperShadowsAction2(Action):
    def __init__(self):
        super().__init__("These ways are strange")

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0

    def pass_items(self, state: HeistState):
        return {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }





################################################################################
###                           An Alarming Bust                                ###
################################################################################

class Bust(OpportunityCard):
    def __init__(self):
        super().__init__("An Alarming Bust")
        self.actions = [BustAction1(), BustAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security < 2        


class BustAction1(Action):
    def __init__(self):
        super().__init__("Oh, it's just that bloody bust of the Consort")

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0

    def pass_items(self, state: HeistState):
        return {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }


class BustAction2(Action):
    def __init__(self):
        super().__init__("Aaagh!")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1,
            Item.CatlikeTread: -1
        }

    def pass_rate(self, state: HeistState):
        return 0.5


################################################################################
###                           A Menacing Corridor                             ###
################################################################################

class Corridor(OpportunityCard):
    def __init__(self):
        super().__init__("A Menacing Corridor")
        self.actions = [CorridorAction1(), CorridorAction2(), CorridorAction3()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 2        


class CorridorAction1(Action):
    def __init__(self):
        super().__init__("It's safe tonight...")

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0

    def pass_items(self, state: HeistState):
        return {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }


class CorridorAction2(Action):
    def __init__(self):
        super().__init__("Is it safe?")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1
        }

    def pass_rate(self, state: HeistState):
        return 0.3


class CorridorAction3(Action):
    def __init__(self):
        super().__init__("Blindfold yourself")

    def can_perform(self, state: HeistState):
        return state.outfit.shadowy >= 100

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1
        }

    def pass_rate(self, state: HeistState):
        return 0.5


################################################################################
###                          A Moment of Safety                               ###
################################################################################

class MomentOfSafety(OpportunityCard):
    def __init__(self):
        super().__init__("A Moment of Safety")
        self.actions = [MomentOfSafetyAction1()]

    def can_draw(self, state: HeistState):
        return state.target_security < 3


class MomentOfSafetyAction1(Action):
    def __init__(self):
        super().__init__("Hide for a little while")

    def pass_items(self, state: HeistState):
        return {
            Item.CatlikeTread: 1 if state.get(Item.CatlikeTread) < 3 else 0
        }

################################################################################
###                         Consider the Lights                               ###
################################################################################

class Lights(OpportunityCard):
    def __init__(self):
        super().__init__("Consider the Lights")
        self.actions = [LightsAction1()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 3        


class LightsAction1(Action):
    def __init__(self):
        super().__init__("Shut off the lights")

    def pass_items(self, state: HeistState):
        return {
            Item.CatlikeTread: 1
        }

    def perform_pass(self, state: HeistState):
        state.items[Item.CatlikeTread] = min(3, state.items[Item.CatlikeTread] + 1)


################################################################################
###                               Tiny Rivals                                 ###
################################################################################

class TinyRivals(OpportunityCard):
    def __init__(self):
        super().__init__("Tiny Rivals")
        self.actions = [TinyRivalsAction1(), TinyRivalsAction2(), TinyRivalsAction3()]

    def can_draw(self, state: HeistState):
        return state.target_security < 3


class TinyRivalsAction1(Action):
    def __init__(self):
        super().__init__("\"Well-met, thieflings!\"")

    def pass_items(self, state: HeistState):
        return {
            Item.InsideInformation: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.Wounds: 2
        }

    def pass_rate(self, state: HeistState):
        return 0.7


class TinyRivalsAction2(Action):
    def __init__(self):
        super().__init__("Hang back")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }


class TinyRivalsAction3(Action):
    def __init__(self):
        super().__init__("Sapphires?")

    def pass_items(self, state: HeistState):
        return {
            Item.Sapphire: 15,
            Item.CatlikeTread: -1
        }


################################################################################
###                           The Rats in the Walls                           ###
################################################################################

class Rats(OpportunityCard):
    def __init__(self):
        super().__init__("The Rats in the Walls")
        self.actions = [RatsAction1(), RatsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 3


class RatsAction1(Action):
    def __init__(self):
        super().__init__("Move in utter silence")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.Wounds: 1
        }

    def pass_rate(self, state: HeistState):
        return self.broad_pass_rate(120, state.outfit.shadowy)


class RatsAction2(Action):
    def __init__(self):
        super().__init__("Avoid their nests")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1,
            Item.InsideInformation: -1
        }

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0


################################################################################
###                         A Clutter of Bric-a-Brac                          ###
################################################################################

class Clutter(OpportunityCard):
    def __init__(self):
        super().__init__("A Clutter of Bric-a-Brac")
        self.actions = [ClutterAction1(), ClutterAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security < 3


class ClutterAction1(Action):
    def __init__(self):
        super().__init__("Poke through the possibilities")

    def pass_items(self, state: HeistState):
        return {
            Item.MoonPearl: 30,
            Item.OstentatiousDiamond: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1
        }

    def pass_rate(self, state: HeistState):
        return 0.7

    def rare_success_rate(self):
        return 0.1  # Estimate for rare success


class ClutterAction2(Action):
    def __init__(self):
        super().__init__("Play it safe")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }


################################################################################
###                           Mislaid Documents                               ###
################################################################################

class Documents(OpportunityCard):
    def __init__(self):
        super().__init__("Mislaid Documents")
        self.actions = [DocumentsAction2()]

    def can_draw(self, state: HeistState):
        return state.target_security >= 3


class DocumentsAction2(Action):
    def __init__(self):
        super().__init__("Move along")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

################################################################################
###                             Troublesome Lock                              ###
################################################################################

class TroublesomeLock(OpportunityCard):
    def __init__(self):
        super().__init__("An Intricate Lock")
        self.actions = [
            TroublesomeLockAction1(),
            TroublesomeLockAction2(),
            TroublesomeLockAction3(),
            TroublesomeLockAction4(),
            TroublesomeLockAction5()
        ]

    def can_draw(self, state: HeistState):
        return state.target_security < 4


class TroublesomeLockAction1(Action):
    def __init__(self):
        super().__init__("There may be an easier way")

    def pass_items(self, state: HeistState):
        return {
            Item.InsideInformation: -1,
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0


class TroublesomeLockAction2(Action):
    def __init__(self):
        super().__init__("What about that key?")

    def pass_items(self, state: HeistState):
        return {
            Item.IntriguingKey: -1,
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        return state.items.get(Item.IntriguingKey, 0) > 0


class TroublesomeLockAction3(Action):
    def __init__(self):
        super().__init__("Use your Kifers")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 2
        }

    def pass_rate(self, state: HeistState):
        return 0.4


class TroublesomeLockAction4(Action):
    def __init__(self):
        super().__init__("Use your Intricate Kifers")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 2
        }

    def pass_rate(self, state: HeistState):
        return 0.6


class TroublesomeLockAction5(Action):
    def __init__(self):
        super().__init__("Try your luck")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 2
        }

    def pass_rate(self, state: HeistState):
        return 0.3


################################################################################
###                             Intricate Lock                                ###
################################################################################

class IntricateLock(OpportunityCard):
    def __init__(self):
        super().__init__("An Intricate Lock")
        self.actions = [
            IntricateLockAction1(),
            IntricateLockAction2()
        ]

    def can_draw(self, state: HeistState):
        return state.target_security >= 4


class IntricateLockAction1(Action):
    def __init__(self):
        super().__init__("Pick the lock in Parabola")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 2
        }

    def pass_rate(self, state: HeistState):
        return self.narrow_pass_rate(7, state.outfit.glasswork)


class IntricateLockAction2(Action):
    def __init__(self):
        super().__init__("Use your key")

    def pass_items(self, state: HeistState):
        return {
            Item.IntriguingKey: -1,
            Item.BurglarsProgress: 2
        }

    def can_perform(self, state: HeistState):
        return state.items.get(Item.IntriguingKey, 0) > 0


################################################################################
###                             Sleeping... Dogs?                             ###
################################################################################

class RegularDogs(OpportunityCard):
    def __init__(self):
        super().__init__("Sleeping... Dogs?")
        self.actions = [
            RegularDogsAction1(),
            RegularDogsAction2()
        ]

    def can_draw(self, state: HeistState):
        return state.target_security < 4


class RegularDogsAction1(Action):
    def __init__(self):
        super().__init__("Creep past")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1
        }

    def pass_rate(self, state: HeistState):
        return 0.4


class RegularDogsAction2(Action):
    def __init__(self):
        super().__init__("Dash past")

    def pass_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1
        }

    def pass_rate(self, state: HeistState):
        return 0.7


################################################################################
###                             Spider Dogs                                   ###
################################################################################

class SpiderDogs(OpportunityCard):
    def __init__(self):
        super().__init__("Sleeping... Dogs?")
        self.actions = [
            SpiderDogsAction1(),
            SpiderDogsAction2()
        ]

    def can_draw(self, state: HeistState):
        return state.target_security >= 4


class SpiderDogsAction1(Action):
    def __init__(self):
        super().__init__("Creep past them")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1
        }

    def fail_items(self, state: HeistState):
        return {
            Item.CatlikeTread: -1,
            Item.BurglarsProgress: -1,
            Item.Nightmares: 4
        }

    def pass_rate(self, state: HeistState):
        return self.narrow_pass_rate(7, state.outfit.monstrous_anatomy)


class SpiderDogsAction2(Action):
    def __init__(self):
        super().__init__("Offer them a spare eyeball")

    def pass_items(self, state: HeistState):
        return {
            Item.BurglarsProgress: 1,
            Item.InsideInformation: -1
        }

    def can_perform(self, state: HeistState):
        return state.items.get(Item.InsideInformation, 0) > 0 and \
               state.outfit.shapeling_arts >= 8

class Prize(OpportunityCard):
    def __init__(self):
        super().__init__("Prize")
        self.actions = [PrizeAction1()]
        self.weight = 10

    def can_draw(self, state: HeistState):
        return state.items[Item.BurglarsProgress] >= state.progress_required
    
class PrizeAction1(Action):
    def __init__(self):
        super().__init__("Claim the Prize")

    def pass_items(self, state: HeistState):
        base_suspicion = 4 if state.target_security > 1 else 3
        return {
            Item.Suspicion: max(0, base_suspicion - state.get(Item.CatlikeTread)),
            Item.Echo: state.prize_value
        }

    def perform_pass(self, state: GameState):
        result = super().perform_pass(state)
        state.status = "Complete"
        return result


class HeistSimRunner(SimulationRunner):
    def __init__(self, runs: int, initial_values: dict):
        super().__init__(runs, initial_values)

        self.initial_values[Item.CatlikeTread] = 3

        self.storylets = [
            StoryletOnAHeist(),
            SkinOfYourTeeth()
        ]

        self.cards = [
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

    def create_state(self) -> HeistState:
        state = HeistState(self.initial_values[Item.PlanningAHeist])
        return state

simulation = HeistSimRunner(
    runs = 10000,
    initial_values= {
        Item.PlanningAHeist: HeistLocation.UNSYMPATHETIC_LANDLORD_MANSION.value,
        Item.UntrainedLyrebird: 1,
        Item.InsideInformation: 1,
        Item.IntriguingKey: 1,
        Item.EscapeRoute: 0
    })

simulation.outfit = PlayerOutfit(334, 18)

simulation.run_simulation()