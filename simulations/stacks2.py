import random
from collections import defaultdict
from enum import Enum, auto

ev_route = 1.9
ev_tant = 0.1
ev_progress = 1
ev_key = 7.51
ev_frag = 1.5
ev_hand_clear = 1
ev_wounds = -0.15
ev_nightmares = -0.15
ev_office_failure = 3 # idk

class ApocryphaSought(Enum):
    BannedWorks = 201
    DeadStars = 202
    SomeFrenchBullshit = 203
    UnrealPlaces = 204
    # ChainedOctavo = 1001

class Action:
    def __init__(self, name):
        self.name = name

    def can_perform(self, state: 'LibraryState'):
        return True

    def perform(self, state: 'LibraryState'):
        rate = self.pass_rate(state)
        if random.random() < rate:
            self.perform_success(state)
        else:
            self.perform_failure(state)

    def ev(self, state: 'LibraryState'):
        pass_rate = self.pass_rate(state)
        success_ev = self.success_ev(state)
        failure_ev = self.failure_ev(state)


        if pass_rate is None:
            print(f"Debug: {self.name} - pass_rate: {pass_rate}, success_ev: {success_ev}, failure_ev: {failure_ev}")
            pass_rate = 0.0
        if success_ev is None:
            print(f"Debug: {self.name} - pass_rate: {pass_rate}, success_ev: {success_ev}, failure_ev: {failure_ev}")
            success_ev = 0.0
        if failure_ev is None:
            print(f"Debug: {self.name} - pass_rate: {pass_rate}, success_ev: {success_ev}, failure_ev: {failure_ev}")
            failure_ev = 0.0        

        return pass_rate * success_ev + (1.0 - pass_rate) * failure_ev

    def pass_rate(self, state: 'LibraryState'):
        return 1.0
    
    def perform_success(self, state: 'LibraryState'):
        pass

    def success_ev(self, state: 'LibraryState'):
        return 1.0
    
    def perform_failure(self, state: 'LibraryState'):
        pass

    def failure_ev(self, state: 'LibraryState'):
        return 0.0

class LibraryState:
    def __init__(self):
        # Carried over
        self.library_keys = 0  # Count of keys collected
        self.routes_traced = 0
        self.fragmentary_ontologies = 0        
        self.tantalizing_possibilities = 0
        self.disposition_of_the_cardinal = 0

        # TODO
        self.librarians_office_failures = 0 

        self.wounds = 0
        self.nightmares = 0

        self.completed_normal_runs = 0
        self.completed_anathema_runs = 0
        self.failed_runs = 0

        self.hour_in_the_library = 0
        self.apocrypha_sought = 0

        self.cartographer_enabled = False
        self.in_search_of_lost_time = 1
        self.progress = 0
        self.noises = 0
        self.anathema_unchained = 0

        self.refill_action = RefillHandAction()
        self.hand = []
        self.actions = 0
        self.deck = [
            ApocryphaFound(),
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
            
            ChainedOctavo()
        ]

        self.card_play_counts = {card.name: 0 for card in self.deck}
        # self.action_play_counts = {self.refill_action.name: 0}
        self.action_play_counts = defaultdict(int)


    def total_runs(self):
        return self.failed_runs + self.completed_normal_runs + self.completed_anathema_runs

    def start_new_run(self, apocrypha_sought, cartographer_enabled):
        self.actions += 1
        self.progress = 0
        self.noises = 0
        self.hand.clear()
        self.in_search_of_lost_time = 1

        self.apocrypha_sought = apocrypha_sought
        self.cartographer_enabled = cartographer_enabled

        if apocrypha_sought == ApocryphaSought.BannedWorks:
            self.hour_in_the_library = 1

        if apocrypha_sought == ApocryphaSought.DeadStars:
            self.hour_in_the_library = 2

        if apocrypha_sought == ApocryphaSought.SomeFrenchBullshit:
            self.hour_in_the_library = 3

        if apocrypha_sought == ApocryphaSought.UnrealPlaces:
            self.hour_in_the_library = 4

    def ev_progress(self, val):
        # TODO this is actually wrong bc there should be no diff between 30 and 31
        # but brain no work rn so leaving it
        progress = min(40 - self.progress, val)
        ev = progress * ev_progress

        # basically if we're somehow at 39 then 1 is as good as 5
        if self.progress < 40 and self.progress + progress >= 40:
            ev = max(ev, ev_progress * 5)

        # HACK save better cards for full value
        if progress < val:
            ev -= 1

        return ev
    
    def ev_noises(self, val):
        if val == 0: return 0

        cur = self.noises
        ev = -1

        if cur == 0 and val > 0:
            # adds Gaoler to deck
            ev += 5
        
        if cur + val >= 36:
            # YOU DIED
            ev -= 1000
        elif cur + val >= 10:
            # adds Shushing to deck
            ev -= 4
        elif cur >= 10 and cur + val < 10:
            # removes Shushing from deck
            if cur + val > 0:
                # keeps Gaoler
                ev += 4
            else:
                ev += 2

        return ev

    def ev_hand_clear(self):
        ev = ev_hand_clear
        if self.anathema_unchained <= 0:
            ev += 2

        return ev

    
    def draw_card(self):
        drawn, lowest = None, float('inf')
        for card in self.deck:
            if card not in self.hand and card.can_draw(self):
                rand = random.random() / card.weight
                if rand < lowest:
                    drawn = card
                    lowest = rand
        self.hand.append(drawn)

    def step(self):
        # print("Cards in hand: " + str(len(self.hand)))
        # print("Progress: " + str(self.progress))

        if self.in_search_of_lost_time > 2:
            self.start_new_run(self.apocrypha_sought, self.cartographer_enabled)

        if len(self.hand) == 0:
            self.refill_action.perform(self)
            self.action_play_counts[self.refill_action.name] += 1
            return

        # Evaluate the best action across all cards in hand
        best_card, best_action, best_action_ev = None, None, -float('inf')

        if self.refill_action.can_perform(self):
            best_action = self.refill_action
            best_action_ev = self.refill_action.ev(self)

        for card in self.hand:
            for action in card.actions:
                if action.can_perform(self):
                    action_ev = action.ev(self)
                    if action_ev > best_action_ev:
                        best_card, best_action, best_action_ev = card, action, action_ev


        best_action.perform(self)
        self.action_play_counts[best_action.name] += 1

        if best_card is not None:
            self.actions += 1
            self.card_play_counts[best_card.name] += 1

            if best_card in self.hand:
                self.hand.remove(best_card)

        self.hand = [card for card in self.hand if card.can_draw(self)]

        # Check for failure condition
        if self.noises >= 36:
            self.failed_runs += 1
            self.hand.clear()
            self.progress = 0
            self.noises = 0
            self.in_search_of_lost_time = 1
            self.actions += 1

    def run(self, steps):
        while self.actions < steps:
            self.step()

class LibraryCard:
    def __init__(self, name, weight=1.0):
        self.name = name
        self.weight = weight
        self.actions = []  # List of possible actions

    def can_draw(self, state: LibraryState):
        return True
    
class RefillHandAction(Action):
    def __init__(self):
        super().__init__("Redraw")

    def can_perform(self, state: LibraryState):
        return len(state.hand) < 4

    def perform(self, state: LibraryState):
        while len(state.hand) < 4:
            state.draw_card()

    def ev(self, state: LibraryState):
        # TODO
        return ev_progress * 5

# Specific card implementations with actions
class ApocryphaFound(LibraryCard):
    def __init__(self):
        super().__init__("Apocrypha Found", 10_000.0)
        self.actions = [ApocryphaFoundAction1()]

    def can_draw(self, state: LibraryState):
        return state.progress >= 40 and state.in_search_of_lost_time == 1

class ApocryphaFoundAction1(Action):
    def __init__(self):
        super().__init__("Claim the book")

    def perform(self, state: LibraryState):
        state.in_search_of_lost_time = 2
        state.progress = 0

        # TODO
        state.hour_in_the_library = (state.hour_in_the_library + 1) % 5

    def ev(self, state: LibraryState):
        # TODO
        return 6
    
class ReadingRoom(LibraryCard):
    def __init__(self):
        super().__init__("The Reading Room", 10_000.0)
        self.actions = [ReadingRoomAction1()]

    def can_draw(self, state: LibraryState):
        return state.progress >= 40 and state.in_search_of_lost_time == 2
    
class ReadingRoomAction1(Action):
    def __init__(self):
        super().__init__("Open the book")

    def perform(self, state: LibraryState):
         # TODO pretty sure Hour doesn't work this way
        state.hour_in_the_library = (state.hour_in_the_library + 1) % 5
        
        # TODO separate flag for this just to be safe
        if state.anathema_unchained == 10:
            state.completed_anathema_runs += 1    
        else:
            state.completed_normal_runs += 1

        state.anathema_unchained = max(0, state.anathema_unchained - 1)

        state.in_search_of_lost_time = 3
        state.actions += 2 # approximation

    def ev(self, state: LibraryState):
        # TODO
        return 6    

class Atrium(LibraryCard):
    def __init__(self):
        super().__init__("An Atrium")
        self.actions = [AtriumAction1(), AtriumAction2()]

class AtriumAction1(Action):
    def __init__(self):
        super().__init__("Continue on the same heading")

    def can_perform(self, state: LibraryState):
        return state.routes_traced > 0

    def pass_rate(self, state: LibraryState):
        # TODO
        # Watchful DC 220, Inerrant & RouteTraced each +15
        return 1.0

    def perform_success(self, state: LibraryState):
        state.routes_traced -= 1
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return ev_progress * 5 - ev_route

    def perform_failure(self, state: LibraryState):
        state.noises += 6

    def failure_ev(self, state: LibraryState):
        # TODO
        return 0

class AtriumAction2(Action):
    def __init__(self):
        super().__init__("Atrium Action 2")

    def can_perform(self, state: LibraryState):
        return state.in_search_of_lost_time == 1 and state.fragmentary_ontologies > 0

    def pass_rate(self, state: LibraryState):
        # TODO Watchful 300, Frag +15
        return 1.0

    def perform_success(self, state: LibraryState):
        state.progress += 5
        state.routes_traced += random.choice([1,2])
        state.fragmentary_ontologies -= 1

    def success_ev(self, state: LibraryState):
        return ev_progress * 5 + ev_route * 1.5 - ev_frag

    def perform_failure(self, state: LibraryState):
        state.progress += 1
        state.noises += 1

    def failure_ev(self, state: LibraryState):
        return 0

class DeadEnd(LibraryCard):
    def __init__(self):
        super().__init__("A Dead End?")
        self.actions = [DeadEndAction1(), DeadEndAction2(),
                        DeadEndAction3(), DeadEndAction4()]

class DeadEndAction1(Action):
    def __init__(self):
        super().__init__("Tie a rope")

    def pass_rate(self, state: LibraryState):
        # TODO Watchful + Shadowy 300
        return 1.0

    def perform_success(self, state: LibraryState):
        state.progress += 5
        state.hand.clear()

    def success_ev(self, state: LibraryState):
        return ev_progress * 5 + ev_route * 1.5 - ev_frag + state.ev_hand_clear()

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.wounds += 2
        state.noises += random.randint(1,6)

    def failure_ev(self, state: LibraryState):
        # TODO
        return 0
    
class DeadEndAction2(Action):
    def __init__(self):
        super().__init__("Take advantage")

    def pass_rate(self, state: LibraryState):
        # TODO Watchful 350, Cthonosophy +15
        return 1.0

    def perform_success(self, state: LibraryState):
        state.routes_traced += 2
        state.tantalizing_possibilities += 50

    def success_ev(self, state: LibraryState):
        return ev_tant * 50 + ev_route * 2

    def perform_failure(self, state: LibraryState):
        state.routes_traced += 1

    def failure_ev(self, state: LibraryState):
        return ev_route
    
class DeadEndAction3(Action):
    def __init__(self):
        super().__init__("See through")

    def can_perform(self, state: LibraryState):
        return state.cartographer_enabled

    def pass_rate(self, state: LibraryState):
        return 1.0

    def perform_success(self, state: LibraryState):
        # TODO +10 tempestuous tale
        return

class DeadEndAction4(Action):
    def __init__(self):
        super().__init__("Tie a rope + Woesel")

    def perform(self, state: LibraryState):
        state.progress += 5
        state.noises += random.randint(1,6)
        state.wounds += 2
        state.hand.clear()
    
    def ev(self, state: LibraryState):
        # TODO average noises ev over range 1-6
        return state.ev_progress(5) \
            + state.ev_noises(4) \
            + state.ev_hand_clear() \
            + ev_wounds * 2
            

class DiscardedLadder(LibraryCard):
    def __init__(self):
        super().__init__("A Grand Staircase")
        self.actions = [DiscardedLadderAction1()]

class DiscardedLadderAction1(Action):
    def __init__(self):
        super().__init__("Climb")

    def pass_rate(self, state: LibraryState):
        # TODO Watchful 200
        return 0.99

    def perform_success(self, state: LibraryState):
        state.routes_traced += random.choice([1,2])

    def success_ev(self, state: LibraryState):
        return ev_route * 1.5

    def perform_failure(self, state: LibraryState):
        state.wounds += 1
        state.noises += 6

    def failure_ev(self, state: LibraryState):
        return ev_wounds + state.ev_noises(6)


class GrandStaircase(LibraryCard):
    def __init__(self):
        super().__init__("A Grand Staircase")
        # TODO: other actions locked by having any Routes
        self.actions = [GrandStaircaseAction1()]

class GrandStaircaseAction1(Action):
    def __init__(self):
        super().__init__("Make an informed decision")

    def can_perform(self, state: LibraryState):
        return state.routes_traced > 0

    def perform(self, state: LibraryState):
        state.routes_traced -= 1
        state.progress += 5
        state.hand.clear()

    def ev(self, state: LibraryState):
        return state.ev_hand_clear() + state.ev_progress(5) - ev_route

class LockedGate(LibraryCard):
    def __init__(self):
        super().__init__("A Locked Gate", 0.8)
        self.actions = [LockedGateAction1()]

class LockedGateAction1(Action):
    def __init__(self):
        super().__init__("Use a key")

    def can_perform(self, state: LibraryState):
        return state.library_keys > 0

    def perform_success(self, state: LibraryState):
        state.library_keys -= 1
        state.progress += 15

    def ev(self, state: LibraryState):
        return state.ev_progress(15) - ev_key

class MapRoom(LibraryCard):
    def __init__(self):
        super().__init__("A Map Room")
        self.actions = [MapRoomAction1(), MapRoomAction2(), MapRoomAction3()]

class MapRoomAction1(Action):
    def __init__(self):
        super().__init__("Look for maps of the library")

    def pass_rate(self, state: LibraryState):
        # TODO Watchful 220
        return 0.90

    def perform_success(self, state: LibraryState):
        state.routes_traced += random.choice([1,2])
        state.tantalizing_possibilities += 50

    def success_ev(self, state: LibraryState):
        return ev_route * 1.5 + ev_tant * 50

    def perform_failure(self, state: LibraryState):
        state.nightmares += 1
        state.noises += random.choice([1,2])
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        # TODO noises range
        return ev_nightmares + state.ev_noises(2) + state.ev_progress(1)

# TODO add item tracking and EV
class MapRoomAction2(Action):
    def __init__(self):
        super().__init__("Look for maps of the Neath")

    def pass_rate(self, state: LibraryState):
        return 0.79

    def perform_success(self, state: LibraryState):
        # TODO: +2 partial map, rare success +1 puzzling map instead
        pass

    def success_ev(self, state: LibraryState):
        return 0
    
    def perform_failure(self, state: LibraryState):
        state.nightmares += 1 # TODO caps at 5 per wiki, still true?
        state.progress += 1
        state.noises += 1

    def failure_ev(self, state: LibraryState):
        return ev_nightmares + state.ev_progress(1) + state.ev_noises(1)
        


class MapRoomAction3(Action):
    def __init__(self):
        super().__init__("Get a lead from the Cartographer")

    def can_perform(self, state: LibraryState):
        return state.cartographer_enabled

    def perform(self, state: LibraryState):
        state.noises += 2
        state.progress += 5

    def ev(self, state: LibraryState):
        return state.ev_noises(2) + state.ev_progress(5)

# class MapRoomAction1(Action):
#     def __init__(self):
#         super().__

class PoisonGallery(LibraryCard):
    def __init__(self):
        super().__init__("A Poison-Gallery")
        self.actions = [PoisonGalleryAction1(), PoisonGalleryAction2()]

class PoisonGalleryAction1(Action):
    def __init__(self):
        super().__init__("Use furniture as stepping stones")

    def pass_rate(self, state: LibraryState):
        # TODO
        # Shadowy 240, Neathproofed +15
        return 1.0

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.noises += 6
        state.wounds += 3

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(6) + ev_wounds * 3

class PoisonGalleryAction2(Action):
    def __init__(self):
        super().__init__("Prepare an antidote")

    def pass_rate(self, state: LibraryState):
        # TODO
        # KT 10
        return 1.0

    def perform_success(self, state: LibraryState):
        # flask of abominable salts -= 1
        state.progress += 5

    def success_ev(self, state: LibraryState):
        # TODO material cost
        return state.ev_progress(5) - 0.2

    def perform_failure(self, state: LibraryState):
        state.noises += 1
        state.wounds += 2
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(1) + ev_wounds * 2 + state.ev_progress(1)

class StoneGallery(LibraryCard):
    def __init__(self):
        super().__init__("A Stone Gallery")
        self.actions = [StoneGalleryAction1(),
                        StoneGalleryAction2(),
                        StoneGalleryAction3(),
                        StoneGalleryAction4()]

class StoneGalleryAction1(Action):
    def __init__(self):
        super().__init__("Make your way through the silent gallery")

    def can_perform(self, state: LibraryState):
        return True

    def pass_rate(self, state: LibraryState):
        # Luck
        return 0.5

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.nightmares += 2
        state.progress += 5

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) + ev_nightmares * 2

class StoneGalleryAction2(Action):
    def __init__(self):
        super().__init__("Stop and examine the ancient volumes")

    def pass_rate(self, state: LibraryState):
        # TODO Cthonosophy 7
        return 0.8
    
    def perform_success(self, state: LibraryState):
        state.fragmentary_ontologies += random.choice([1,2])

    def success_ev(self, state: LibraryState):
        return ev_frag * 1.5

    def perform_failure(self, state: LibraryState):
        state.noises += random.choice([1,2])
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return ev_progress + state.ev_noises(2)

class StoneGalleryAction3(Action):
    def __init__(self):
        super().__init__("Follow a borehole through the back of a bookcase")

    def can_perform(self, state: LibraryState):
        return state.routes_traced >= 2 and state.hour_in_the_library in (3, 4)

    def pass_rate(self, state: LibraryState):
        # TODO Dangerous + Watchful DC 300
        return 1.0

    def perform_success(self, state: LibraryState):
        state.routes_traced -= 2
        state.progress += 10

    def success_ev(self, state: LibraryState):
        return state.ev_progress(10) - ev_route * 2

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.noises += 6
        state.routes_traced -= 1

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) - ev_route * 1 + state.ev_noises(6)

class StoneGalleryAction4(Action):
    def __init__(self):
        super().__init__("Follow a borehole + WOESEL")

    def can_perform(self, state: LibraryState):
        return state.routes_traced >= 2 and state.hour_in_the_library in (3, 4)

    def pass_rate(self, state: LibraryState):
        return 0.0

    def perform_success(self, state: LibraryState):
        state.routes_traced -= 2
        state.progress += 10

    def success_ev(self, state: LibraryState):
        return state.ev_progress(10) - ev_route * 2

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.noises += 6
        state.routes_traced -= 1

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) - ev_route * 1 + state.ev_noises(6)


class Index(LibraryCard):
    def __init__(self):
        super().__init__("An Index")
        self.actions = [IndexAction1(),
                        IndexAction2(),
                        IndexAction3()]
        
    def can_draw(self, state: LibraryState):
        return state.in_search_of_lost_time == 1

class IndexAction1(Action):
    def __init__(self):
        super().__init__("Search for a reference card")

    def pass_rate(self, state: LibraryState):
        # TODO Watchful 200, Inerrant +15
        return 1.0

    def perform_success(self, state: LibraryState):
        state.routes_traced += random.choice([1,2,3])

    def success_ev(self, state: LibraryState):
        return ev_route * 2

    def perform_failure(self, state: LibraryState):
        state.routes_traced += 1
        state.noises += 2
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(1) + ev_route + state.ev_noises(2)
    
class IndexAction2(Action):
    def __init__(self):
        super().__init__("Try to understand the organization of the library")

    def pass_rate(self, state: LibraryState):
        # TODO Cthonosophy 7
        return 0.8

    def perform_success(self, state: LibraryState):
        state.fragmentary_ontologies += random.choice([1,2,3])

    def success_ev(self, state: LibraryState):
        return ev_frag * 2

    def perform_failure(self, state: LibraryState):
        state.fragmentary_ontologies += 1
        state.noises += random.choice([1,2])
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(1) + ev_route + state.ev_noises(2)
    
class IndexAction3(Action):
    def __init__(self):
        super().__init__("Situate yourself within the greater whole")

    def can_perform(self, state: LibraryState):
        return state.fragmentary_ontologies > 0

    def perform(self, state: LibraryState):
        state.fragmentary_ontologies -= 1
        state.progress += 5

    def ev(self, state: LibraryState):
        return state.ev_progress(5) - ev_frag


class LibrariansOffice(LibraryCard):
    def __init__(self):
        super().__init__("An Index", 0.8)
        self.actions = [LibrariansOfficeAction1(),
                        LibrariansOfficeAction2(),
                        LibrariansOfficeAction3()]
        
    def can_draw(self, state: LibraryState):
        return state.in_search_of_lost_time == 2

class LibrariansOfficeAction1(Action):
    def __init__(self):
        super().__init__("Search for a reference card")

    def pass_rate(self, state: LibraryState):
        return 0.9

    def perform_success(self, state: LibraryState):
        state.tantalizing_possibilities += 40
        drawer = random.choice([1,2,3])
        if drawer == 1: state.library_keys += 1
        if drawer == 2: state.routes_traced += 1
        if drawer == 3: state.fragmentary_ontologies += 1

    def success_ev(self, state: LibraryState):
        return ev_tant * 40 + (ev_key + ev_route + ev_frag)/3.0

    def perform_failure(self, state: LibraryState):
        state.librarians_office_failures += 1

    def failure_ev(self, state: LibraryState):
        return ev_office_failure
    
class LibrariansOfficeAction2(Action):
    def __init__(self):
        super().__init__("Take the opposite door")

    def perform(self, state: LibraryState):
        state.progress += 5

    def ev(self, state: LibraryState):
        return state.ev_progress(5)
    
class LibrariansOfficeAction3(Action):
    def __init__(self):
        super().__init__("Unlock the cart")

    def can_perform(self, state: LibraryState):
        return state.library_keys > 0

    def perform(self, state: LibraryState):
        state.library_keys -= 1
        state.progress += 15

    def ev(self, state: LibraryState):
        return state.ev_progress(15) - ev_key
    

class FloweringGallery(LibraryCard):
    def __init__(self):
        super().__init__("A Flowering Gallery")
        self.actions = [FloweringGalleryAction1(),
                        FloweringGalleryAction2()]
        
    def can_draw(self, state: LibraryState):
        return state.hour_in_the_library in [1,2]

class FloweringGalleryAction1(Action):
    def __init__(self):
        super().__init__("Keep going")

    def pass_rate(self, state: LibraryState):
        # TODO NP + Inerrant 0
        return 1.0

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        # TODO: wiki doesn't have exact num for nightmares, +2 is a guess
        state.nightmares += 2
        state.noises += 6

    def failure_ev(self, state: LibraryState):
        return ev_nightmares * 2 + state.ev_noises(6)
    
class FloweringGalleryAction2(Action):
    def __init__(self):
        super().__init__("Eat the fruit of knowledge")

    def pass_rate(self, state: LibraryState):
        # TODO KT 12
        return 0.9

    def perform_success(self, state: LibraryState):
        state.fragmentary_ontologies += 2

    def success_ev(self, state: LibraryState):
        return ev_frag * 2

    def perform_failure(self, state: LibraryState):
        state.wounds += 2
        state.noises += 1
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return ev_wounds * 2 + state.ev_noises(2) + state.ev_progress(1)


class BlackGallery(LibraryCard):
    def __init__(self):
        super().__init__("A Flowering Gallery")
        self.actions = [BlackGalleryAction1(),
                        BlackGalleryAction2(),
                        BlackGalleryAction3()]
        
    def can_draw(self, state: LibraryState):
        return state.hour_in_the_library in [3,4,5]

class BlackGalleryAction1(Action):
    def __init__(self):
        super().__init__("Light a lantern")

    def pass_rate(self, state: LibraryState):
        # TODO Shadowy 240, Insub +15
        return 1.0

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.noises += 2

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) + state.ev_noises(2)
    
class BlackGalleryAction2(Action):
    def __init__(self):
        super().__init__("Navigate by alternate senses")

    def pass_rate(self, state: LibraryState):
        # TODO Watchful 240, MA +10, Inerrant +15
        return 1.0

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.progress += 1
        state.noises += 2

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(1) + state.ev_noises(2)
    
class BlackGalleryAction3(Action):
    def __init__(self):
        super().__init__("Light a lantern + WOESEL")

    def pass_rate(self, state: LibraryState):
        return 0.0

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.noises += 2

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) + state.ev_noises(2)

class GaolerLibrarian(LibraryCard):
    def __init__(self):
        super().__init__("A Gaoler-Librarian")
        self.actions = [GaolerLibrarianAction1(),
                        GaolerLibrarianAction2(),
                        GaolerLibrarianAction3()]

    def can_draw(self, state: LibraryState):
        return state.noises > 0

class GaolerLibrarianAction1(Action):
    def __init__(self):
        super().__init__("Distract the Gaoler")

    def can_perform(self, state: LibraryState):
        return state.noises > 0  # Action only available if there's noise

    def pass_rate(self, state: LibraryState):
        # TODO: Shadowy 200
        return 0.96

    def perform_success(self, state: LibraryState):
        # Does nothing
        pass

    def success_ev(self, state: LibraryState):
        return 0

    def perform_failure(self, state: LibraryState):
        state.wounds += 4 # TODO wiki is unsure
        state.noises += 1
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return ev_wounds * 4 + state.ev_noises(1) + state.ev_progress(1)

class GaolerLibrarianAction2(Action):
    def __init__(self):
        super().__init__("Try to lift one of its keys")

    def pass_rate(self, state: LibraryState):
        # TODO Shadowy 250, Insub +15
        return 0.87

    def perform_success(self, state: LibraryState):
        state.library_keys += 1

    def success_ev(self, state: LibraryState):
        return ev_key

    def perform_failure(self, state: LibraryState):
        state.noises += 6

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(6)
    
class GaolerLibrarianAction3(Action):
    def __init__(self):
        super().__init__("An intervention from the Grey Cardinal")

    def can_perform(self, state: LibraryState):
        return state.disposition_of_the_cardinal > 0

    def perform(self, state: LibraryState):
        state.progress += 5
        state.disposition_of_the_cardinal -= 1

    def ev(self, state: LibraryState):
        return state.ev_progress(5)
    
class TerribleShushing(LibraryCard):
    def __init__(self):
        super().__init__("A Terrible Shushing")
        self.actions = [TerribleShushingAction1(),
                        TerribleShushingAction2(),
                        TerribleShushingAction3()]

    def can_draw(self, state: LibraryState):
        return state.noises >= 10

class TerribleShushingAction1(Action):
    def __init__(self):
        super().__init__("Find a hiding place")

    def pass_rate(self, state: LibraryState):
        # TODO Shadowy 220
        return 0.87

    def perform_success(self, state: LibraryState):
        state.noises -= 3

    def success_ev(self, state: LibraryState):
        return state.ev_noises(-3)

    def perform_failure(self, state: LibraryState):
        state.noises -= 1

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(-1)
    
class TerribleShushingAction2(Action):
    def __init__(self):
        super().__init__("Hurry along")

    def pass_rate(self, state: LibraryState):
        # TODO Shadowy 295
        return 0.65

    def perform_success(self, state: LibraryState):
        state.noises += 2
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_noises(2) + state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.noises += 4
        state.progress += 5

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(4) + state.ev_progress(5)

# TODO: wiki is unsure about exact range of outcomes
class TerribleShushingAction3(Action):
    def __init__(self):
        super().__init__("Hurry along")

    def can_perform(self, state: LibraryState):
        return state.cartographer_enabled

    def perform(self, state: LibraryState):
        state.noises = max(0, state.noises - random.randint(3, 10))

    def ev(self, state: LibraryState):
        return state.ev_noises(-6)

class GodsEyeView(LibraryCard):
    def __init__(self):
        super().__init__("A God's Eye View")
        self.actions = [GodsEyeViewAction1(), GodsEyeViewAction2()]

    def can_draw(self, state: LibraryState):
        return state.fragmentary_ontologies >= 5

class GodsEyeViewAction1(Action):
    def __init__(self):
        super().__init__("Try to hold it all in your mind at once")

    def pass_rate(self, state: LibraryState):
        return 0.4

    def perform_success(self, state: LibraryState):
        state.tantalizing_possibilities += 60
        state.fragmentary_ontologies = max(0, state.fragmentary_ontologies - 6)

    def success_ev(self, state: LibraryState):
        return ev_tant * 60 - ev_frag * 6

    def perform_failure(self, state: LibraryState):
        state.tantalizing_possibilities += 40
        state.nightmares += random.randint(2,4)
        state.noises += random.randint(1,2)
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return ev_tant * 40 + ev_nightmares * 3 \
            + state.ev_noises(2) + state.ev_progress(1)

class GodsEyeViewAction2(Action):
    def __init__(self):
        super().__init__("Focus on the path ahead")

    def perform(self, state: LibraryState):
        state.progress += 15
        state.fragmentary_ontologies -= 5
    
    def ev(self, state: LibraryState):
        return state.ev_progress(15) - ev_frag * 5 
    

class ShapeOfTheLabyrinth(LibraryCard):
    def __init__(self):
        super().__init__("The Shape of the Labyrinth")
        self.actions = [ShapeOfTheLabyrinthAction1(), ShapeOfTheLabyrinthAction2()]

    def can_draw(self, state: LibraryState):
        return state.routes_traced >= 6 and state.in_search_of_lost_time == 2

class ShapeOfTheLabyrinthAction1(Action):
    def __init__(self):
        super().__init__("Rethink your movements")

    def perform(self, state: LibraryState):
        state.hand.clear()
        state.progress += 10
        state.routes_traced -= random.randint(2,5)

    def ev(self, state: LibraryState):
        return ev_progress * 10 - ev_route * 3.5 + state.ev_hand_clear()

class ShapeOfTheLabyrinthAction2(Action):
    def __init__(self):
        super().__init__("Reject the significance of shape")
        
    def can_perform(self, state: LibraryState):
        return state.fragmentary_ontologies > 0

    def pass_rate(self, state: LibraryState):
        # Cthonosophy 5
        return 0.9

    def perform_success(self, state: LibraryState):
        state.fragmentary_ontologies -= 1
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5) - ev_frag

    def perform_failure(self, state: LibraryState):
        state.noises += 1
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(1) + state.ev_progress(1)

# TODO: fine tune EVs and item tracking
class GreyCardinal(LibraryCard):
    def __init__(self):
        super().__init__("The Grey Cardinal")
        self.actions = [GreyCardinalAction1(),
                        GreyCardinalAction2(),
                        GreyCardinalAction3()]

class GreyCardinalAction1(Action):
    def __init__(self):
        super().__init__("Offer the cardinal a furry lunch")

    def perform(self, state: LibraryState):
        state.disposition_of_the_cardinal += 1
        # TODO track rats spent
        state.progress += 5

    def ev(self, state: LibraryState):
        return state.ev_progress(5)

class GreyCardinalAction2(Action):
    def __init__(self):
        super().__init__("Offer the cardinal a tin of something fishy")

    def perform(self, state: LibraryState):
        state.disposition_of_the_cardinal += random.randint(1,2)
        # TODO track deep zee catches spent
        state.progress += 5

    def ev(self, state: LibraryState):
        return state.ev_progress(5)

class GreyCardinalAction3(Action):
    def __init__(self):
        super().__init__("Engage the Cardinal in conversation")

    def pass_rate(self, state: LibraryState):
        # TODO Persuasive 250, Bizarre +10
        return 1.0

    def perform_success(self, state: LibraryState):
        state.tantalizing_possibilities += 50
        state.disposition_of_the_cardinal += 1

    def success_ev(self, state: LibraryState):
        return ev_tant * 50

    def perform_failure(self, state: LibraryState):
        state.tantalizing_possibilities += 40

    def failure_ev(self, state: LibraryState):
        return ev_tant * 40

class GlimpseThroughAWindow(LibraryCard):
    def __init__(self):
        super().__init__("A Glimpse through a Window", 0.1)
        self.actions = [GlimpseThroughAWindowAction1(), GlimpseThroughAWindowAction2()]

class GlimpseThroughAWindowAction1(Action):
    def __init__(self):
        super().__init__("Stop and look through")

    def can_perform(self, state: LibraryState):
        return state.hour_in_the_library != 4
    
    def perform(self, state: LibraryState):
        state.tantalizing_possibilities += 50

    def ev(self, state: LibraryState):
        return ev_tant * 50

class GlimpseThroughAWindowAction2(Action):
    def __init__(self):
        super().__init__("Move on quickly")

    def perform(self, state: LibraryState):
        state.progress += 5

    def ev(self, state: LibraryState):
        return state.ev_progress(5)

class TeaRoom(LibraryCard):
    def __init__(self):
        super().__init__("A Tea Room?", 0.8)
        self.actions = [TeaRoomAction1(), TeaRoomAction2(), TeaRoomAction3()]

class TeaRoomAction1(Action):
    def __init__(self):
        super().__init__("Take a moment to regroup")

    def perform(self, state: LibraryState):
        # TODO
        pass

    def ev(self, state: LibraryState):
        # TODO
        return 0

class TeaRoomAction2(Action):
    def __init__(self):
        super().__init__("Consult your maps of the library")

    def pass_rate(self, state: LibraryState):
        # TODO Routes Traced 0
        return 1.0

    def perform_success(self, state: LibraryState):
        state.routes_traced -= 1
        state.progress += 10

    def success_ev(self, state: LibraryState):
        return state.ev_progress(10) - ev_route

    def perform_failure(self, state: LibraryState):
        state.routes_traced -= 1
        state.progress += 5

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) - ev_route

class TeaRoomAction3(Action):
    def __init__(self):
        super().__init__("Try to make sense of what you've seen")

    def can_perform(self, state: LibraryState):
        return state.fragmentary_ontologies > 0

    def pass_rate(self, state: LibraryState):
        # TODO Fragmentary Ontologies 2
        return 1.0

    def perform_success(self, state: LibraryState):
        state.fragmentary_ontologies -= 1
        state.tantalizing_possibilities += 50

    def success_ev(self, state: LibraryState):
        return ev_tant * 50

    def perform_failure(self, state: LibraryState):
        state.fragmentary_ontologies += 1

    def failure_ev(self, state: LibraryState):
        return ev_frag

# TODO Check rarity on these
class CartographerSnuffbox(LibraryCard):
    def __init__(self):
        super().__init__("Snuffbox.png")
        self.actions = [CartographerSnuffboxAction1(),
                        CartographerSnuffboxAction2()]

    def can_draw(self, state: LibraryState):
        # TODO confirm this requires routes to draw
        return state.cartographer_enabled and state.routes_traced > 0

class CartographerSnuffboxAction1(Action):
    def __init__(self):
        super().__init__("Computernofigure.png")

    def can_perform(self, state: LibraryState):
        return state.routes_traced > 0

    def perform(self, state: LibraryState):
        state.routes_traced -= 1
        state.progress += 5

    def ev(self, state: LibraryState):
        return state.ev_progress(5) - ev_route

class CartographerSnuffboxAction2(Action):
    def __init__(self):
        super().__init__("Implication.png")

    def can_perform(self, state: LibraryState):
        return state.routes_traced >= 3

    def perform(self, state: LibraryState):
        state.routes_traced -= 3
        state.fragmentary_ontologies += 5

    def ev(self, state: LibraryState):
        return ev_frag * 5 - ev_route * 3

class CartographerCompass(LibraryCard):
    def __init__(self):
        super().__init__("Compass.png")
        self.actions = [CartographerCompassAction1(),
                        CartographerCompassAction2()]

class CartographerCompassAction1(Action):
    def __init__(self):
        super().__init__("Camera2.png")

    def pass_rate(self, state: LibraryState):
        # TODO Watchful + Inerrant, need exact DC
        return 1.0

    def perform_success(self, state: LibraryState):
        state.routes_traced += random.randint(1, 3)

    def success_ev(self, state: LibraryState):
        return ev_route * 2

    def perform_failure(self, state: LibraryState):
        state.noises += 2
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(2) + state.ev_progress(1)

class CartographerCompassAction2(Action):
    def __init__(self):
        super().__init__("Chart2.png")

    def can_perform(self, state: LibraryState):
        return state.routes_traced >= 3

    def perform(self, state: LibraryState):
        state.progress += random.choice([5, 10, 15])
        state.routes_traced -= 3

    def ev(self, state: LibraryState):
        return (state.ev_progress(5) + state.ev_progress(10) + state.ev_progress(15)) / 3.0

# TODO requires True Denizen
class ChainedOctavo(LibraryCard):
    def __init__(self):
        super().__init__("A Chained Octavo", 0.1)
        self.actions = [ChainedOctavoAction1(),
                        ChainedOctavoAction2()]
    
    def can_draw(self, state: LibraryState):
        return state.anathema_unchained <= 0 and state.in_search_of_lost_time == 1

class ChainedOctavoAction1(Action):
    def __init__(self):
        super().__init__("Camera2.png")

    def can_perform(self, state: LibraryState):
        return state.library_keys > 1 and state.noises < 28

    def perform(self, state: LibraryState):
        state.library_keys -= 1
        state.noises += random.randint(5,7)
        
        state.progress = 0
        state.in_search_of_lost_time = 2

        state.anathema_unchained = 10

        # TODO: confirm this advances Hour, vs sets to specific value
        state.hour_in_the_library = (state.hour_in_the_library + 1) % 5

    def ev(self, state: LibraryState):
        return 100

class ChainedOctavoAction2(Action):
    def __init__(self):
        super().__init__("Camera2.png")

    def pass_rate(self, state: LibraryState):
        # TODO Cthonosophy + Fragmentary Ontology 10
        return 1.0

    def perform_success(self, state: LibraryState):
        state.progress += 5
        state.tantalizing_possibilities += 10

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5) + ev_tant * 10

    def perform_failure(self, state: LibraryState):
        state.progress += 5

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5)

def simulate_runs(num_runs):
    """
    Simulates a large number of runs of the game and prints the results.
    
    Args:
    - num_runs (int): Number of runs to simulate.
    
    Returns:
    - None
    """

    state = LibraryState()
    state.apocrypha_sought = ApocryphaSought.BannedWorks
    state.cartographer_enabled = True

    while state.total_runs() < num_runs:
        state.step()

    total_steps = state.actions
    avg_steps = total_steps / num_runs

    total_runs = state.total_runs()

    # Calculate and print statistics
    print(f"Total runs: {num_runs}")
    print(f"Successes: {total_runs} ({(total_runs / num_runs) * 100:.2f}%)")
    print(f"Failures: {state.failed_runs} ({(state.failed_runs / num_runs) * 100:.2f}%)")
    print(f"Average actions per run: {total_steps / num_runs:.2f}")
    # print(f"Average TPs per run: {state.tantalizing_possibilities / num_runs:.2f}\n")

    print("\nCard and Action Play Counts:")
    print(f"{'Card':<30} {'Count':<10} {'Action':<40} {'Count per Run':<15}")
    print("-" * 95)

    # Sort the deck by the card play counts in descending order
    sorted_deck = sorted(state.deck, key=lambda card: state.card_play_counts[card.name], reverse=True)

    for card in sorted_deck:
        card_name = card.name
        # Truncate card name if it exceeds max length
        truncated_card_name = (card_name[:27] + '...') if len(card_name) > 27 else card_name
        card_count = state.card_play_counts[card_name]
        card_count_per_run = card_count / total_runs if total_runs > 0 else 0

        print(f"{truncated_card_name:<30} {card_count:<10.2f}")

        for action in card.actions:
            action_name = action.name
            # Truncate action name if it exceeds max length
            truncated_action_name = (action_name[:37] + '...') if len(action_name) > 37 else action_name
            action_count = state.action_play_counts[action_name]
            action_count_per_run = action_count / total_runs if total_runs > 0 else 0

            print(f"{'':<30} {'':<10} {truncated_action_name:<40} {action_count_per_run:<15.2f}")

    # Define the value of items in echoes and stuivers
    item_values = {
        'Library Keys': {'echoes': 0.0},
        'Routes Traced': {'echoes': 0.0},
        'Fragmentary Ontologies': {'echoes': 0.0},
        'Tantalizing Possibilities': {'echoes': 0.1, 'stuivers': 2},
        'Librarian\'s Office Failures': {'echoes': 3},
        'Wounds': {'echoes': -1.0 },  # approx @ 6 heal for 1 action & 6 EPA
        'Normal Completions': {'echoes': 116, 'stuivers': 2320},  # example value
        'Glimpse of Anathema': {'echoes': 312.5, 'stuivers': 6250}  # example value
    }

    print("Accumulated Items after all runs:")
    print(f"{'Item':<30} {'Count':<10} {'Value per Unit (E/S)':<25} {'Total Value (E/S)':<25}")
    print("-" * 95)

    # Initialize total sums for echoes and stuivers
    total_echoes = 0
    total_stuivers = 0

    # Print item counts and values
    items = {
        'Library Keys': state.library_keys,
        'Routes Traced': state.routes_traced,
        'Fragmentary Ontologies': state.fragmentary_ontologies,
        'Tantalizing Possibilities': state.tantalizing_possibilities,
        'Librarian\'s Office Failures': state.librarians_office_failures,
        'Wounds': state.wounds,
        'Normal Completions': state.completed_normal_runs,
        'Glimpse of Anathema': state.completed_anathema_runs
    }

    for item, count in items.items():
        value_data = item_values.get(item, {})
        echo_value = value_data.get('echoes', None)
        stuiver_value = value_data.get('stuivers', None)
        total_echo_value = 0
        total_stuiver_value = 0

        if echo_value is not None:
            total_echo_value = count * echo_value
            total_echoes += total_echo_value

        if stuiver_value is not None:
            total_stuiver_value = count * stuiver_value
            total_stuivers += total_stuiver_value

        # Display both Echo and Stuiver values if both are present
        if echo_value is not None and stuiver_value is not None:
            print(f"{item:<30} {count:<10} {echo_value:.2f} E / {stuiver_value:.2f} S{'':<8} {total_echo_value:.2f} E / {total_stuiver_value:.2f} S")
        elif echo_value is not None:
            print(f"{item:<30} {count:<10} {echo_value:.2f} E{'':<14} {total_echo_value:.2f} E{'':<10}")
        elif stuiver_value is not None:
            print(f"{item:<30} {count:<10} {stuiver_value:.2f} S{'':<14} {total_stuiver_value:.2f} S{'':<10}")

    # Print total sums
    print("-" * 95)
    print(f"{'Total':<30} {'':<10} {'':<25} {total_echoes:.2f} E / {total_stuivers:.2f} S")

    # Calculate and print Echoes and Stuivers earned per action
    echoes_per_action = total_echoes / total_steps if total_steps > 0 else 0
    stuivers_per_action = total_stuivers / total_steps if total_steps > 0 else 0
    print(f"{'Per Action':<30} {'':<10} {'':<25} {echoes_per_action:.4f} E / {stuivers_per_action:.4f} S")

    print(f"ApocryphaSought: {state.apocrypha_sought}")
    print(f"Cartographer Enabled: {state.cartographer_enabled}")
    # print(f"\nEst EPA: {(116 * state.completed_normal_runs + 312 * state.completed_anathema_runs + state.tantalizing_possibilities * 0.1) / total_steps:.2f}")

simulate_runs(100_000)
