# from enums import *
import random

"""
Assumptions
- 12 MA for "Dogs?" card
- 12 GW for "Intricate Lock" card
- 200 Shadowy for a couple cards
- 10 Dreaded (or a Lyrebird) for Watchman card
- 
"""


class HeistState:
    progress: int
    tread: int
    keys: int
    info: int
    deck: list
    hand: list

    cat_bribes: int

    status: str

    def __init__(self, info, keys):
        self.progress = 0
        self.tread = 3
        self.info = info
        self.keys = keys
        self.hand = []
        self.cat_bribes = 0

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
            Prize(),
        ]

    def draw_card(self):
        drawn = None
        best = float("inf")
        for card in self.deck:
            if card.weight(self):
                number = random.random() / card.weight(self)
                if number < best:
                    best = number
                    drawn = card
        self.hand.append(drawn)

    def step(self):
        self.steps += 1

        while len(self.hand) < 3:
            self.draw_card()

        self.hand.sort(key=lambda card: card.ev(self))
        card = self.hand.pop()
        card.play(self)

        self.progress = max(self.progress, 0)

        if self.tread <= 0:
            self.status = "Failure"

    def run(self):
        while self.status == "InProgress":
            self.step()


class HeistCard:
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
    def ev(self, state: HeistState):
        if state.progress <= 3:
            return 1.4
        else:
            return 1

    def play(self, state: HeistState):
        if state.progress <= 3:
            if random.random() > 0.3:
                state.progress += 2
        else:
            state.progress += 1


class Watchman(HeistCard):
    def ev(self, state: HeistState):
        return 1

    def play(self, state: HeistState):
        state.progress += 1


class Door(HeistCard):
    def ev(self, state: HeistState):
        if state.info > 0:
            return 2
        elif state.tread == 2:
            return -10
        else:
            return -5  # arbitrary

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
    def ev(self, state: HeistState):
        if state.info > 0:
            return 0.8  # safe but costs items
        else:
            return 0.2  # arbitrary

    def play(self, state: HeistState):
        if state.info > 0:
            state.info -= 1
            state.progress += 1
        else:
            if random.random() > 0.2:
                state.progress += 1
            else:
                state.tread -= 1


class Cat(HeistCard):
    def ev(self, state: HeistState):
        return 0.99

    def play(self, state: HeistState):
        state.progress += 1
        state.cat_bribes += 1


class Look(HeistCard):
    def ev(self, state: HeistState):
        if state.keys > 0:
            return 2
        elif state.tread == 1:
            return -10
        else:
            # TODO: would we rather play this or door at 3 tread?
            return -4

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
            state.tread -= 1
            if random.random() > 0.4:
                state.progress += 1
            else:
                state.progress -= 1


class Climb(HeistCard):
    def weight(self, state: HeistState):
        if self in state.hand:
            return 0
        else:
            return 0.2

    def ev(self, state: HeistState):
        if state.info > 0:
            return 0.9
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
    def ev(self, state: HeistState):
        if state.info > 0:
            return 2
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
    def ev(self, state: HeistState):
        if state.info > 0:
            return 2
        elif state.tread > 1:
            return -0.1  # arbitrary
        else:
            return -5  # arbitrary

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
            return 0.5
        else:
            return 0

    def play(self, state: HeistState):
        state.tread = min(state.tread + 1, 3)


class Rats(HeistCard):
    def ev(self, state: HeistState):
        return 1

    def play(self, state: HeistState):
        state.progress += 1


class Documents(HeistCard):
    # TODO: random key option?

    def ev(self, state: HeistState):
        return 1

    def play(self, state: HeistState):
        state.progress += 1


class Lock(HeistCard):
    def ev(self, state: HeistState):
        return 2

    def play(self, state: HeistState):
        state.progress += 2


class Dogs(HeistCard):
    def ev(self, state: HeistState):
        return 1

    def play(self, state: HeistState):
        state.progress += 1


class Prize(HeistCard):
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

for i in range(0, runs):
    heist = HeistState(info=info, keys=keys)
    heist.run()

    cat_bribes += heist.cat_bribes

    if heist.status == "Success":
        successes += 1
        success_steps += heist.steps
    else:
        failures += 1
        failure_steps += heist.steps

print(f"Completed {runs} runs with {info} Info & {keys} Keys.")
print(f"{successes/runs} success rate, in avg {success_steps/successes} steps")
print(f"{failures/runs} fail rate, in avg {failure_steps/max(failures, 1)} steps")
print(f"Bribed an avg of {cat_bribes/runs} cats")
