# from enums import *
import random

'''
Assumptions
- 12 MA for "Dogs?" card
- 12 GW for "Intricate Lock" card
- 200 Shadowy for a couple cards
- 10 Dreaded (or a Lyrebird) for Watchman card

general improvements
- don't redraw early when you have a win in hand

'''

class HeistState:
    progress: int
    tread: int
    keys: int
    info: int
    deck: list
    hand: list

    cat_bribes: int
    snaffled_docs: int
    stolen_correspondence: int

    status: str

    def __init__(self, info, keys):
        self.progress = 0
        self.tread = 3
        self.info = info
        self.keys = keys
        self.hand = []
        self.cat_bribes = 0
        self.snaffled_docs = 0
        self.stolen_correspondence = 0

        self.status = "InProgress"
        self.steps = 0

        self.deck = [
            Stairs(),
            Watchman(),
            Door(),
            Place(),
            Cat(),
            Look(),
            Climb(),
            Shadows(),
            Corridor(),
            Lights(),
            Rats(),
            Documents(),
            Lock(),
            Dogs(),
            Prize()
        ]

        self.card_play_counts = {card.__class__.__name__: 0 for card in self.deck}  # Track how many times each card is played


    def draw_card(self):
        drawn, lowest = None, float('inf')
        for card in self.deck:
            if card not in self.hand and card.can_draw(self):
                rand = random.random() / card.weight(self)
                if rand < lowest:
                    drawn = card
                    lowest = rand
        self.hand.append(drawn)

    def step(self):
        self.steps += 1

        sum_free_prog = sum(i.free_progress for i in self.hand) + self.progress
        sum_ev = sum(i.ev(self) for i in self.hand) + self.progress

        has_2prog = False
        if self.hand:
            has_2prog = any(card.free_progress >= 2 for card in self.hand)

        while len(self.hand) < 3 and ((sum_ev < 5 and not has_2prog) or self.progress >= 5):
            self.draw_card()

        self.hand.sort(key=lambda card: card.ev(self))
        card = self.hand.pop()
        self.card_play_counts[card.__class__.__name__] += 1  # Increment card play counter
        card.play(self)

        self.progress = max(self.progress, 0)

        if self.tread <= 0:
            self.status = "Failure"


    def run(self):
        while self.status == "InProgress":
            self.step()

class HeistCard:
    free_progress: int
    info_progress: int
    key_progress: int

    def __init__(self):
        self.free_progress = 0
        self.info_progress = 0
        self.key_progress = 0

    def can_draw(self, state: HeistState):
        return True

    def weight(self, state: HeistState):
        if self in state.hand:
            return 0
        else:
            return 1.0

    def ev(self, state: HeistState):
        pass

    def play(self, state: HeistState):
        pass

class Stairs(HeistCard):
    # Improvements: smarter about when to YOLO?

    def __init__(self):
        super().__init__()
        self.free_progress = 1.4

    def ev(self, state: HeistState):
        if state.progress <= 3:
            return 2.01
        else:
            return 1.01

    def play(self, state: HeistState):
        if state.progress <= 3:
            if random.random() > 0.3:
                state.progress += 2
        else:
            state.progress += 1


class Watchman(HeistCard):
    def __init__(self):
        super().__init__()
        self.free_progress = 1

    def ev(self, state: HeistState):
        return 1.01

    def play(self, state: HeistState):
        state.progress += 1

class Door(HeistCard):
    def __init__(self):
        super().__init__()
        self.info_progress = 2
        
    def ev(self, state: HeistState):
        if state.info > 0:
            return 2.001
        elif state.tread <= 2:
            return -10
        else:
            return 0
        # elif state.tread >= 3 and state.progress <= 3:
        #     return 0.01
        # elif state.tread >= 3 and state.progress == 4:
        #     return -1
        # else:
        #     return -9

    def play(self, state: HeistState):
        if state.info > 0:
            state.info -= 1
            state.progress += 2
        else:
            if random.random() > 0.5:
                state.progress += 2
            else:
                state.tread -= 2

class Place(HeistCard):
    # TODO
    # snaffle when 4+ progress and 3 tread?

    def __init__(self):
        super().__init__()
        self.info_progress = 1

    def ev(self, state: HeistState):
        # if state.progress == 4 and state.tread >= 3: # and len(state.hand) < 3:
        # if state.tread >= 3 and info < 1:
            # return 0.1
        if state.info > 0:
            return 1
        elif state.tread > 1:
            return 0.8 # arbitrary
        else:
            return 0.1

    def play(self, state: HeistState):
        # if state.progress == 4 and state.tread >= 3: # and len(state.hand) < 3:
        # if state.tread >= 3:
        #     if random.random() > 0.5:
        #         state.snaffled_docs += 9
        #         state.stolen_correspondence += 20
        #     else:
        #         state.tread -= 2
        if state.info > 0:
            state.info -= 1
            state.progress += 1
        else:
            if random.random() > 0.2:
                state.progress += 1
            else:
                state.tread -= 1

class Cat(HeistCard):
    def __init__(self):
        super().__init__()
        self.free_progress = 1

    def ev(self, state: HeistState):
        return 1

    def play(self, state: HeistState):
        state.progress += 1
        state.cat_bribes += 1

class Look(HeistCard):
    def __init__(self):
        super().__init__()
        self.key_progress = 2

    def ev(self, state: HeistState):
        if state.keys > 0:
            return 2.02
        elif state.tread == 1:
            return -50
        else:
            # TODO: would we rather play this or door at 3 tread?
            return -1
        
    def play(self, state: HeistState):
        if state.keys > 0:
            state.keys -= 1
            state.progress += 2
        elif state.tread == 1:
            if random.random() > 0.7:
                pass
            else:
                state.progress -= 1
                state.tread -= 1
        else:
            # this option always loses tread
            state.tread -=1
            if random.random() > 0.4:
                state.progress += 1
            else:
                state.progress -= 1

class Climb(HeistCard):
    def __init__(self):
        super().__init__()
        self.info_progress = 1

    def weight(self, state: HeistState):
        if self in state.hand:
            return 0
        else:
            return 0.2
        
    def ev(self, state: HeistState):
        if state.info > 0:
            return 1
        else:
            return 0.5
        # TODO: escape option if things are really bad?

    def play(self, state: HeistState):
        if state.info > 0:
            state.info -= 1
            state.progress += 1
        else:
            if random.random() > 0.5:
                state.progress += 1

class Shadows(HeistCard):
    def __init__(self):
        super().__init__()
        self.info_progress = 2

    def ev(self, state: HeistState):
        if state.info > 0:
            return 2.01
        elif state.progress == 0:
            return 0.5
        else:
            return 0
        
    def play(self, state: HeistState):
        if state.info > 0:
            state.info -= 1
            state.progress += 2
        else:
            if random.random() > 0.5:
                state.progress += 1
            else:
                state.progress -= 1

class Corridor(HeistCard):
    def __init__(self):
        super().__init__()
        self.info_progress = 2

    def ev(self, state: HeistState):
        if state.info > 0:
            return 2.01
        elif state.tread > 1:
            return 0.5
        else:
            return -0.05  # arbitrary
        
    def play(self, state: HeistState):
        if state.info > 0:
            state.info -= 1
            state.progress += 2
        else:
            if random.random() > 0.5:
                state.progress += 1
            else:
                state.tread -= 1    


class Lights(HeistCard):
    def ev(self, state: HeistState):
        if state.tread < 3:
            return 0.51
        else:
            return 0
        
    def play(self, state: HeistState):
        state.tread = min(state.tread + 1, 3)

class Rats(HeistCard):
    def __init__(self):
        super().__init__()
        self.free_progress = 1

    def ev(self, state: HeistState):
        return 1.01
    
    def play(self, state: HeistState):
        state.progress += 1

class Documents(HeistCard):
    # TODO: random key option?

    def __init__(self):
        super().__init__()
        self.free_progress = 1

    def ev(self, state: HeistState):
        return 1.01
    
    def play(self, state: HeistState):
        # if state.progress >= 5:
        #     if random.random() > 0.5: # assumed 50/50
        #         state.snaffled_docs += 3
        #     else:
        #         state.keys += 1
        # else:
            state.progress += 1


class Lock(HeistCard):
    def __init__(self):
        super().__init__()
        self.free_progress = 2

    def ev(self, state: HeistState):
        return 2.1
    
    def play(self, state: HeistState):
        state.progress += 2

class Dogs(HeistCard):
    def __init__(self):
        super().__init__()
        self.free_progress = 1

    def ev(self, state: HeistState):
        return 1.01
    
    def play(self, state: HeistState):
        state.progress += 1        

class Prize(HeistCard):
    def can_draw(self, state: HeistState):
        return state.progress >= 5

    def weight(self, state: HeistState):
        if state.progress >= 5:
            return 10
        else:
            return 0
        
    def ev(self, state: HeistState):
        return 100
    
    def play(self, state: HeistState):
        state.status = "Success"

runs = 100_000
keys = 0
info = 0

successes = 0
success_steps = 0

failures = 0
failure_steps = 0

cat_bribes = 0
docs = 0
corresondence = 0

total_card_play_counts = {card.__class__.__name__: 0 for card in HeistState(info=info, keys=keys).deck}  # Initialize total counts

for i in range(0, runs):
    heist = HeistState(info=info, keys=keys)
    heist.run()

    # Track how many times each card was played
    for card, count in heist.card_play_counts.items():
        total_card_play_counts[card] += count

    cat_bribes += heist.cat_bribes
    docs += heist.snaffled_docs
    corresondence += heist.stolen_correspondence

    if heist.status == "Success":
        successes += 1
        success_steps += heist.steps
    else:
        failures += 1
        failure_steps += heist.steps

print(f"Completed {runs} runs with {info} Info & {keys} Keys.")
print(f"{successes/runs} success rate, in avg {success_steps/successes} steps")
print(f"{failures/runs} fail rate, in avg {failure_steps/max(failures, 1)} steps")
print(f"Bribed an avg of {cat_bribes/runs} cats," +
      f" and snaffled {docs/runs} documents and {corresondence/runs} correspondence")

print("\nAverage card plays per run:")
for card, total in total_card_play_counts.items():
    print(f"{card}: {total / runs:.2f} plays per run")