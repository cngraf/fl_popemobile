import random

ev_route = 1.9
ev_tant = 0.1
ev_progress = 1
ev_key = 7.5
ev_frag = 1.5
ev_hand_clear = 1

class LibraryState:
    def __init__(self):
        # Carried over
        self.library_keys = 0  # Count of keys collected
        self.routes_traced = 0
        self.fragmentary_ontologies = 0
        self.hour_in_the_library = 1
        self.tantalizing_possibilities = 0
        self.completed_runs = 0

        # TODO
        self.librarians_office_failures = 0 

        self.cartographer_enabled = False
        self.in_search_of_lost_time = 1
        self.progress = 0
        self.noises = 0
        self.hand = []
        self.status = "InProgress"
        self.steps = 0
        self.deck = [
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
            LabyrinthShape(),
            GreyCardinal(),
            GlimpseThroughAWindow(),
            TeaRoom()
        ]

        self.play_counts = {card.name: 0 for card in self.deck}

    
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
        self.steps += 1
        while len(self.hand) < 4:
            self.draw_card()
        
        self.hand.sort(key=lambda card: card.ev(self))
        card = self.hand.pop()
        card.play(self)
        self.play_counts[card.name] += 1

        if self.noises >= 36:
            self.status = "Failure"

        if self.progress >= 40:  # Example win condition
            self.hour_in_the_library = (self.hour_in_the_library + 1) % 5

            if self.in_search_of_lost_time == 1:
                self.in_search_of_lost_time = 2
                self.progress = 0
            else:
                self.status = "Success"
                # TODO more exact sim
                self.in_search_of_lost_time = 1
                self.completed_runs += 1
                self.noises = 0
                self.progress = 0
                self.steps += 3 # approximation
                self.hand.clear()

    def run(self):
        while self.status == "InProgress":
            self.step()
        return self.status

class LibraryCard:
    def __init__(self):
        self.name = "Generic Card"
        self.weight = 1.0

    def can_draw(self, state: LibraryState):
        return True

    def play(self, state: LibraryState):
        pass

    def ev(self, state: LibraryState):
        return 1.0
    
    def pass_rate_narrow(dc, stat):
        rate = 0.5 + 0.1 * (stat - dc)
        return min(1.0, max(0, rate))
    
    def pass_rate_broad(dc, stat):
        rate = 0.6 * stat/dc
        return min(1.0, max(0, rate))

# Specific card implementations
class Atrium(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "An Atrium"

    def play(self, state: LibraryState):
        if state.in_search_of_lost_time == 1 and state.fragmentary_ontologies >= 1:
            state.fragmentary_ontologies -= 1
            state.routes_traced += 1
            state.progress += 5
        elif state.routes_traced >= 1:
            state.routes_traced -= 1
            state.progress += 5

    def ev(self, state: LibraryState):
        if state.in_search_of_lost_time == 1 and state.fragmentary_ontologies >= 1:
            return 5 * ev_progress + ev_route - ev_frag
        elif state.routes_traced >= 1:
            return 5 * ev_progress - ev_route
        else:
            return 0

class DeadEnd(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Dead End?"

    # TODO: other options
    def play(self, state: LibraryState):
        state.hand.clear()
        state.progress += 5

        if state.noises == 0 and state.library_keys < 100:
            state.noises += 2

    def ev(self, state: LibraryState):
        if state.noises == 0 and state.library_keys < 100:
            return ev_key # hack
        else:
            return ev_progress * 5 + ev_hand_clear

class DiscardedLadder(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Discarded Ladder"
        self.progress_gain = random.choice([1, 2])

    def play(self, state: LibraryState):
        if random.random() > 0.5:
            state.routes_traced += 2
        else:
            state.routes_traced += 1

    def ev(self, state: LibraryState):
        return ev_route * 1.5

class GrandStaircase(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Grand Staircase"

    def play(self, state: LibraryState):
        state.hand.clear()

        if state.routes_traced >= 1:
            state.routes_traced -= 1
            state.progress += 5
        else:
            if random.random() > 0.5:
                state.progress += 5
            else:
                state.progress += 1
                state.noises += 1

    def ev(self, state: LibraryState):
        if state.routes_traced >= 1:
            return ev_progress * 5 - ev_route + ev_hand_clear
        else:
            return ev_route * 3

class LockedGate(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Locked Gate"
        self.weight = 0.8

    def play(self, state: LibraryState):
        if state.library_keys > 0:
            state.library_keys -= 1
            state.progress += 15

    def ev(self, state: LibraryState):
        if state.library_keys > 0:
            potential_prog = min(15, 40 - state.progress)
            return ev_progress * potential_prog - ev_key
        else:
            return 0

class MapRoom(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Map Room"

    def play(self, state: LibraryState):
        state.routes_traced += 1
        state.tantalizing_possibilities += 50

        if random.random() > 0.5:
            state.routes_traced += 1

    def ev(self, state: LibraryState):
        return ev_route * 1.5 + ev_tant * 50

class PoisonGallery(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Poison-Gallery"

    def play(self, state: LibraryState):
        state.progress += 5

    def ev(self, state: LibraryState):
        return ev_progress * 5

class StoneGallery(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Stone Gallery"
        self.progress_gain = 5

    # TODO: other options
    def play(self, state: LibraryState):
        if state.routes_traced >= 2 and state.hour_in_the_library in (3, 4):
            state.routes_traced -= 2
            state.progress += 10
        else:
            state.progress += 5
        
    def ev(self, state: LibraryState):
        if state.routes_traced >= 2 and state.hour_in_the_library in (3, 4):
            return ev_progress * 10 - ev_route * 2
        else:
            return ev_progress * 5
        
class Index(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "An Index"

    # TODO: I think this auto discards when you advance time
    def can_draw(self, state: LibraryState):
        return state.in_search_of_lost_time == 1

    def play(self, state: LibraryState):
        state.routes_traced += 2

    def ev(self, state: LibraryState):
        return ev_route * 2

class LibrariansOffice(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Librarian's Office"
        self.weight = 0.8

    def play(self, state: LibraryState):
        rand = random.random()
        if rand <= 0.9:
            state.tantalizing_possibilities += 40
            if rand >= 0.667:
                state.library_keys += 1
            elif rand >= 0.334:
                state.routes_traced += 1
            else:
                state.fragmentary_ontologies += 1
        else:
            state.librarians_office_failures += 1

    def ev(self, state: LibraryState):
        return 0.9 * (ev_tant * 40 + (ev_key + ev_route + ev_frag) / 3)
    

class FloweringGallery(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Flowering Gallery"

    # TODO: auto discard with time change?
    def can_draw(self, state: LibraryState):
        return state.hour_in_the_library != 4

    def play(self, state: LibraryState):
        if state.routes_traced >= 1:
            state.routes_traced -= 1
            state.progress += 5
        else:
            state.fragmentary_ontologies += 2

    def ev(self, state: LibraryState):
        if state.routes_traced >= 1:
            return ev_progress * 5 - ev_route
        else:
            return ev_frag * 2

class BlackGallery(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Black Gallery"

    # TODO: auto discard with time change?
    def can_draw(self, state: LibraryState):
        return state.hour_in_the_library != 1

    def play(self, state: LibraryState):
        state.progress += 5

    def ev(self, state: LibraryState):
        return ev_progress * 5

class GaolerLibrarian(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Gaoler-Librarian"
        # self.pass_rate = 0.9 # hack

    def can_draw(self, state: LibraryState):
        return state.noises > 0        

    def play(self, state: LibraryState):
        if state.noises > 21:
            state.progress += 5
        elif random.random() <= 0.9:
            state.library_keys += 1
        else:
            state.noises += 6

    def ev(self, state: LibraryState):
        if state.noises <= 21: # hack
            return ev_key * 0.9
        else:
            return ev_progress * 5

class TerribleShushing(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Terrible Shushing"
        self.progress_gain = 5

    def can_draw(self, state: LibraryState):
        return state.noises >= 10        

    def play(self, state: LibraryState):
        if random.random() > 0.5:
            state.progress += self.progress_gain
            state.noises += 2

    def ev(self, state: LibraryState):
        return self.progress_gain * 5 - 1 # hack

class GodsEyeView(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A God's Eye View"
        self.progress_gain = 1

    def play(self, state: LibraryState):
        if state.fragmentary_ontologies >= 5:
            state.fragmentary_ontologies -= 5
            state.progress += 15

    def ev(self, state: LibraryState):
        if state.fragmentary_ontologies >= 5:
            potential_progress = min(15, 40 - state.progress)
            return potential_progress * ev_progress - ev_frag * 5
        else:
            return 0

class LabyrinthShape(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "The Shape of the Labyrinth"

    def can_draw(self, state: LibraryState):
        return state.in_search_of_lost_time == 2 and state.routes_traced >= 6

    def play(self, state: LibraryState):
        state.routes_traced -= 4
        state.progress += 10
        state.hand.clear()

    def ev(self, state: LibraryState):
        potential_prog = min(10, 40 - state.progress)
        return potential_prog * ev_progress - ev_route * 4
    
class GreyCardinal(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "The Grey Cardinal"

    def play(self, state: LibraryState):
        state.progress += 5

    def ev(self, state: LibraryState):
        return ev_progress * 5

class GlimpseThroughAWindow(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Glimpse through a Window"
        self.weight = 0.1

    def play(self, state: LibraryState):
        state.progress += 5

    def ev(self, state: LibraryState):
        return ev_progress * 5
    
class TeaRoom(LibraryCard):
    def __init__(self):
        super().__init__()
        self.name = "A Tea Room?"
        self.progress_gain = 10
        self.weight = 0.8

    def play(self, state: LibraryState):
        state.routes_traced -= 2 # TODO: double check this variable cost
        state.progress += 10

    def ev(self, state: LibraryState):
        if state.routes_traced >= 2:
            return min(10, 40 - state.progress) * ev_progress - ev_route * 2
        else:
            return 0

# Simulation setup
def simulate_runs(num_runs):
    """
    Simulates a large number of runs of the game and prints the results.
    
    Args:
    - num_runs (int): Number of runs to simulate.
    
    Returns:
    - None
    """
    total_steps = 0
    successes = 0
    failures = 0

    state = LibraryState()

    for _ in range(num_runs):
        result = state.run()

        if result == "Success":
            successes += 1
        else:
            failures += 1

        state.status = "InProgress"

    total_steps = state.steps
    avg_steps = total_steps/num_runs

    # Calculate and print statistics
    print(f"Total runs: {num_runs}")
    print(f"Successes: {successes} ({(successes / num_runs) * 100:.2f}%)")
    print(f"Failures: {failures} ({(failures / num_runs) * 100:.2f}%)")
    print(f"Average actions per run: {total_steps / num_runs:.2f}")
    print(f"Average TPs per run: {state.tantalizing_possibilities / num_runs:.2f}")

    print("\nAccumulated Items after all runs:")
    print(f"Library Keys: {state.library_keys}")
    print(f"Routes Traced: {state.routes_traced}")
    print(f"Fragmentary Ontologies: {state.fragmentary_ontologies}")
    print(f"Tantalizing Possibilities: {state.tantalizing_possibilities}")
    print(f"Librarian's Office Failures: {state.librarians_office_failures}")

    # Print insights on card play counts
    print("\nCard Play Counts:")
    for card_name, count in state.play_counts.items():
        print(f"{card_name}: {count/successes :.2f} per run")

    print(f"\nEst EPA: {(116 * successes + state.tantalizing_possibilities * 0.1)/total_steps}")

# Run the simulation
simulate_runs(10000)
