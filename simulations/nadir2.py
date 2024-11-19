import math
from collections import defaultdict
from enum import Enum, auto
import helper.utils as utils
from enums import *
from simulations.item_conversions import conversion_rate
from simulations.models import *
from simulations.models import GameState

# TODO add sound of wings

class NadirState(GameState):
    def __init__(self):
        super().__init__(max_hand_size=5)
        self.status = "InProgress"
        self.skip_econ_inputs = False

    def ev_from_item(self, item, val: int):
        if item == Item.Irrigo:
            return self.ev_irrigo(val)
        else:
            return val * conversion_rate(item, Item.Echo)

    def ev_irrigo(self, val: int, ev_tread_base: int) -> float:
        pass
        
    def run(self):
        while self.status == "InProgress":
            self.step()

    def step(self):

        best_card, best_action = self.best_action_by_simple_ranking()


        if best_action is None:
            # TODO log or default to other strat?
            print("Cards in hand: " + str(len(self.hand)))
            print(f"Irrigo {self.get(Item.Irrigo)}")
            for card in self.hand:
                print(card.name)
            # print("Best action: " + best_action.name)

        if best_action:
            result = best_action.perform(self)
            self.actions += best_action.action_cost
            self.action_result_counts[best_action][result] += 1
            # print(best_action.name)
            # print(self.hand)
            # print(self.items)

        if best_card is not None:
            self.card_play_counts[best_card] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)            

        self.hand = [card for card in self.hand if card.can_draw(self)]

    def run(self):
        while self.status == "InProgress":
            self.step()


    # Econ strat, TODO do another one for speed
    def best_action_by_simple_ranking(self):

        irrigo = self.get(Item.Irrigo)

        irrigo_cap = 5

        list = [
            Storylet_EnterNadir
        ]

        if irrigo >= irrigo_cap:
            list.append(Storylet_LeaveNadir)
    
        if irrigo + 2 <= irrigo_cap:
            list.extend([
                Battles1_Wisdom, # 62.5e/2, same as other 3
                Woods_DanceGoesOnWithClathermont, # 36.5e/2
                Hole_RipOutWordsWithDiscordantStudiesTwoCap
            ])

        # TODO fine-tune at lower Irrigo values?
        list.append(Losing3_Goldfish) # 25e/1

        if irrigo + 2 <= irrigo_cap:
            list.extend([
                Garden2_RosersReroll,
                # Garden2_RosersBail
            ])

        list.append(OldBones2_ExamineSiteWithDaughter) # ~12.5e/1
        list.append(Losing3_Goldfish)
        list.append(SoundOfWings1_Confront) # 25e/2

        list.append(Deck_RefillHand)

        # TODO where to put Catafalquerie

        # Low value 1 Irrigo
        if irrigo + 1 <= irrigo_cap:
            list.extend([
                Sins_AllowImmaculateEel, # 6.25e/1
                Cata3_RebelsWhoWillNotRise, # 5e/1

                Altarful3_Urchins, # 2.5e/1
                Web_Ascend, # 2.5e/1

                Pause1_Bread, # 1e/1
                CardGame1_SpeakManLeft, # 0.6e/1
                Recall1_Blank, # 0.1e/1

                Sea1_Trophies,
                Air1_Dream, # 0e/1
                Face1_GetOut, # 0e/1
                SomethingMoves1_WhatDoYouSee, # 0e/1
                Storylet_LeaveNadir
                ])


        # if irrigo >= 5:
        list.append(Storylet_LeaveNadir)

        # Low value 2 Irrigo
        list.extend([
            Motion1_Run,
            Reflections1_Run,
            Water1_Run
        ])


        # Find the best action from the ranked list that is in the hand
        for ranked_action in list:
            for storylet in self.storylets:
                for action in storylet.actions:
                    if isinstance(action, ranked_action) and action.can_perform(self):
                        return (storylet, action)
            for card in self.hand:
                for card_action in card.actions:
                    if isinstance(card_action, ranked_action) and card_action.can_perform(self):
                        return (card, card_action)

        # If no action can be performed, return None
        return (None, None)

################################################################
#                     Base Storylet
################################################################

class StoryletNadir(OpportunityCard):
    def __init__(self):
        super().__init__("Storylet: Nadir")
        self.actions = [
            Deck_RefillHand(),
            Storylet_EnterNadir(),
            Storylet_LeaveNadir()
        ]

class Deck_RefillHand(Action):
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

class Storylet_EnterNadir(Action):
    def __init__(self):
        super().__init__("(ENTER)")
        self.action_cost = 3

    def can_perform(self, state):
        return state.get(Item.Irrigo) == 0
    
    def pass_items(self, state):
        return {
            Item.Irrigo: 1
        }

class Storylet_LeaveNadir(Action):
    def __init__(self):
        super().__init__("(LEAVE)")
    
    def perform_pass(self, state: GameState):
        result = super().perform_pass(state)
        state.status = "Complete"
        return result

################################################################
#                          A Card Game
################################################################

class CardGame(OpportunityCard):
    def __init__(self):
        super().__init__("A Card Game")
        self.actions = [
            CardGame1_SpeakManLeft(),
            CardGame2_SpeakWomanRight(),
            CardGame3_DealYourselfIn(),
            # Dice()
        ]

class CardGame1_SpeakManLeft(Action):
    def __init__(self):
        super().__init__("Speak to the man on the left")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.TaleOfTerror: 1,
            Item.RomanticNotion: 1,
        }

class CardGame2_SpeakWomanRight(Action):
    def __init__(self):
        super().__init__("Speak to the woman on the right")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.MemoryOfDistantShores: 1,
            Item.ManiacsPrayer: 1,
        }

class CardGame3_DealYourselfIn(Action):
    def __init__(self):
        super().__init__("Deal yourself in")

    def can_perform(self, state: NadirState):
        return state.get(Ambition.HeartsDesire)

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.ExtraordinaryImplication: 1,
        }

# class Dice(Action):
#     def __init__(self):
#         super().__init__("Dice!")

#     def can_perform(self, state: NadirState):
#         return state.get(AirsOfLondon) == Irrigo * 3

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 1,
#             Item.DevilboneDie: 1,
#         }

################################################################
#                       A Familiar Face?
################################################################

class FamiliarFace(OpportunityCard):
    def __init__(self):
        super().__init__("A Familiar Face?")
        self.actions = [
            Face1_GetOut(),
            # SleepsFortressSuit(),
            # SleepsFortressFrock()
        ]

class Face1_GetOut(Action):
    def __init__(self):
        super().__init__("Get out. Get out!")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            # Item.Watchful: 4,
        }

# class SleepsFortressSuit(Action):
#     def __init__(self):
#         super().__init__("Sleep's fortress (Parabola-Linen Suit)")

#     def can_perform(self, state: NadirState):
#         return state.get(Item.ParabolaLinenSuit) >= 1

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 2,
#             Item.ParabolaLinenSuit: -1,
#             Item.StrangeShoreParabolaSuit: 1,
#         }

# class SleepsFortressFrock(Action):
#     def __init__(self):
#         super().__init__("Sleep's fortress (Parabola-Linen Frock)")

#     def can_perform(self, state: NadirState):
#         return state.get(Item.ParabolaLinenFrock) >= 1

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 2,
#             Item.ParabolaLinenFrock: -1,
#             Item.StrangeShoreParabolaFrock: 1,
#         }

################################################################
#                   A Pause for Refreshment
################################################################

class PauseForRefreshment(OpportunityCard):
    def __init__(self):
        super().__init__("A Pause for Refreshment")
        self.actions = [
            Pause1_Bread(),
            Pause2_Zzoup(),
            # Lunchbox()
        ]

class Pause1_Bread(Action):
    def __init__(self):
        super().__init__("Bread")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.CrypticClue: 50,
        }

class Pause2_Zzoup(Action):
    def __init__(self):
        super().__init__("'Zzoup.'")

    def can_perform(self, state: NadirState):
        return state.get(Item.BlackmailMaterial) >= 1

    def pass_items(self, state: NadirState):
        return {
            Item.BlackmailMaterial: -1,

            Item.Irrigo: 1,
            # Item.RecipeForZzoup: 1,
            Item.Wounds: -3,
            # Item.Dangerous: 3,
        }

# class Lunchbox(Action):
#     def __init__(self):
#         super().__init__("A lunchbox?")

#     def can_perform(self, state: NadirState):
#         return state.get(Item.MirrorcatchBox) >= 1

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 1,
#             Item.MirrorcatchBox: -1,
#             Item.IrrigoFilledMirrorcatchBox: 1, # TODO
#         }


################################################################
#                  A Waking Dream of Motion
################################################################

class WakingDreamOfMotion(OpportunityCard):
    def __init__(self):
        super().__init__("A Waking Dream of Motion")
        self.actions = [
            Motion1_Run(),
            # PastConfidences()
        ]

    def can_draw(self, state):
        return state.get_pyramidal_level(Item.Nightmares) >= 4

class Motion1_Run(Action):
    def __init__(self):
        super().__init__("Run")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            Item.Nightmares: 1,
            Item.AppallingSecret: 1,
        }

# # TODO dream qualities
# class PastConfidences(Action):
#     def __init__(self):
#         super().__init__("Past confidences")

#     def can_perform(self, state: NadirState):
#         return state.get(Item.RecurringDreamsGameOfChess) >= 4

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 1,
#             Item.RecurringDreamsGameOfChess: -10,
#             Item.BlackmailMaterial: 1,
#         }

################################################################
#                  A Waking Dream of Reflections
################################################################

class WakingDreamOfReflections(OpportunityCard):
    def __init__(self):
        super().__init__("A Waking Dream of Reflections")
        self.actions = [
            Reflections1_Run(),
            # KindOfMonster()
        ]

    def can_draw(self, state):
        return state.get_pyramidal_level(Item.Nightmares) >= 2

class Reflections1_Run(Action):
    def __init__(self):
        super().__init__("Run")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            Item.Nightmares: 1,
            Item.AppallingSecret: 1,
        }

# # TODO dream qualities
# class KindOfMonster(Action):
#     def __init__(self):
#         super().__init__("A kind of monster")

#     def can_perform(self, state: NadirState):
#         return state.get(Item.RecurringDreamsIsSomeoneThere) >= 4

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 1,
#             Item.RecurringDreamsIsSomeoneThere: -10,
#             Item.DirefulReflection: 1,
#         }

################################################################
#                  A Waking Dream of Water
################################################################

class WakingDreamOfWater(OpportunityCard):
    def __init__(self):
        super().__init__("A Waking Dream of Water")
        self.actions = [
            Water1_Run(),
            # ShipOfLights()
        ]

    def can_draw(self, state):
        return state.get_pyramidal_level(Item.Nightmares) >= 6

class Water1_Run(Action):
    def __init__(self):
        super().__init__("Run")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            Item.Nightmares: 1,
            Item.AppallingSecret: 1,
        }

# # TODO dream qualities
# class ShipOfLights(Action):
#     def __init__(self):
#         super().__init__("The Ship of Lights")

#     def can_perform(self, state: NadirState):
#         return state.get(Item.RecurringDreamsDeathByWater) >= 4

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 1,
#             Item.RecurringDreamsDeathByWater: -10,
#             Item.FavourInHighPlaces: 1,
#         }

################################################################
#                  A Weakness in the Air
################################################################

class WeaknessInTheAir(OpportunityCard):
    def __init__(self):
        super().__init__("A Weakness in the Air")
        self.actions = [
            Air1_Dream(),
            # DreamsCanWait()
        ]

class Air1_Dream(Action):
    def __init__(self):
        super().__init__("Dream")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            # Item.AllDreams: 1, # TODO
            Item.Nightmares: 1,
        }

# class DreamsCanWait(Action):
#     def __init__(self):
#         super().__init__("Dreams can wait")

#     def can_perform(self, state: NadirState):
#         return state.get(Item.LuminousNeathglassGoggles) >= 1 and state.get(Item.Watchful) >= 100

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 3,
#             Item.LuminousNeathglassGoggles: -1,
#             Item.PairOfIrrigoGoggles: 1,
#         }

#     def fail_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 1,
#             Item.Wounds: 1,
#             Item.Watchful: -5,
#         }


################################################################
#                     Altarful of Strangers
################################################################

class AltarfulOfStrangers(OpportunityCard):
    def __init__(self):
        super().__init__("An Altarful of Strangers")
        self.actions = [
            # SpeakMaskedMan(),
            # SpeakRubberyMan(),
            Altarful3_Urchins(),
            Altarful4_Examine()
        ]

# class SpeakMaskedMan(Action):
#     def __init__(self):
#         super().__init__("Speak to the masked man")

#     def can_perform(self, state: NadirState):
#         return state.skip_econ_inputs or state.get(Item.PairOfHushedSpidersilkSlippers) >= 1
    
#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 1,
#             Item.PairOfHushedSpidersilkSlippers: -1,
#             Item.PairOfForgottenSpidersilkSlippers: 1,
#         }

# class SpeakRubberyMan(Action):
#     def __init__(self):
#         super().__init__("Speak to the rubbery man")

#     def can_perform(self, state: NadirState):
#         return state.skip_econ_inputs or state.get(Item.NoduleOfWarmAmber) >= 1
    
#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 2,
#             Item.NoduleOfWarmAmber: -1,
#             Item.NoduleOfVioletAmber: 1,
#         }

class Altarful3_Urchins(Action):
    def __init__(self):
        super().__init__("Speak to the Urchins")

    def pass_rate(self, state: NadirState):
        return self.broad_pass_rate(200, state.outfit.persuasive)

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.ExtraordinaryImplication: 1,
        }
    
    def fail_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
        }

class Altarful4_Examine(Action):
    def __init__(self):
        super().__init__("Speak to the Urchins")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            Item.TaleOfTerror: 1,
            Item.CompromisingDocument: 1,
        }

################################################################
#                      An Unlikely Garden
################################################################

class UnlikelyGarden(OpportunityCard):
    def __init__(self):
        super().__init__("An Unlikely Garden")
        self.actions = [
            Garden1_Enemies(),
            Garden2_RosersReroll(),
            Garden2_RosersBail()
        ]

class Garden1_Enemies(Action):
    def __init__(self):
        super().__init__("But you were their enemies, were you not?")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.WalkingTheFallingCities: 10,
        }

class Garden2_RosersReroll(Action):
    def __init__(self):
        super().__init__("(SC + RETRY) Where did the Rosers go?")

    # Assume 2nd chance used
    def pass_rate(self, state):
        single_rate = self.broad_pass_rate(1000, state.outfit.persuasive)
        return 1 - (1 - single_rate) ** 2

    def pass_items(self, state: NadirState):
        return {
            Item.ConfidentSmile: -1,
            Item.Irrigo: 2,
            Item.SearingEnigma: 1,
        }
    
    def fail_items(self, state):
        return {
            Item.ConfidentSmile: -1,
            Item.Irrigo: 2,
            Item.CrypticClue: 50,
            Item.Nightmares: 1,
        }
    
class Garden2_RosersBail(Action):
    def __init__(self):
        super().__init__("(SC + NO RETRY) Where did the Rosers go?")

    # No reroll, no fail
    def pass_rate(self, state):
        return self.broad_pass_rate(1000, state.outfit.persuasive)

    def pass_items(self, state: NadirState):
        return {
            Item.ConfidentSmile: -1,
            Item.Irrigo: 2,
            Item.SearingEnigma: 1,
        }
    

################################################################
#                Do You Recall How They Came to That Place?
################################################################

# TODO item reqs
class RecallHowTheyCame(OpportunityCard):
    def __init__(self):
        super().__init__("Do you recall how they came to that place?")
        self.actions = [
            Recall1_Blank(),
            Recall2_Who(),
            Recall3_What(),
            Recall4_Why()
        ]

class Recall1_Blank(Action):
    def __init__(self):
        super().__init__("—")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.NoduleOfWarmAmber: 1,
        }

class Recall2_Who(Action):
    def __init__(self):
        super().__init__("Who-")

    def pass_items(self, state: NadirState):
        return {
            Item.AnIdentityUncovered: -5,
            Item.Irrigo: 1,
            Item.NoduleOfTremblingAmber: 1,
        }

class Recall3_What(Action):
    def __init__(self):
        super().__init__("What -")

    def pass_items(self, state: NadirState):
        return {
            Item.DiaryOfTheDead: -5,
            Item.Irrigo: 1,
            Item.NoduleOfFecundAmber: 1,
        }

class Recall4_Why(Action):
    def __init__(self):
        super().__init__("Why -")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.NoduleOfFecundAmber: -5,            
            Item.FlukeCore: 1,
        }

################################################################
#                          Losing
################################################################

class Losing(OpportunityCard):
    def __init__(self):
        super().__init__("Losing")
        self.actions = [
            Losing1_JustOne(),
            Losing2_DubiousAttribution(),
            Losing3_Goldfish(),
        ]

class Losing1_JustOne(Action):
    def __init__(self):
        super().__init__("Just one")

    def pass_items(self, state: NadirState):
        return {
            Item.CrypticClue: -1,
            Item.Irrigo: 1,
            Item.ExtraordinaryImplication: 1,
            # Item.Watchful: -10
        }

class Losing2_DubiousAttribution(Action):
    def __init__(self):
        super().__init__("Dubious attribution")

    def pass_items(self, state: NadirState):
        return {
            Item.JournalOfInfamy: -1,
            Item.Irrigo: 2,
            Item.UncannyIncunabulum: 1,
        }
    
class Losing3_Goldfish(Action):
    def __init__(self):
        super().__init__("Dubious attribution")

    def pass_rate(self, state):
        bonus = state.get(Item.Irrigo) * 20
        return self.broad_pass_rate(250, state.outfit.watchful + bonus)

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.AntiqueMystery: 1,
            Item.CaveAgedCodeOfHonour: 1,
        }    

################################################################
#                        Lost at Sea
################################################################

class LostAtSea(OpportunityCard):
    def __init__(self):
        super().__init__("Lost at Sea")
        self.actions = [
            Sea1_Trophies(),
            Sea2_MissYou(),
            Sea3_ItWasTheMilk()
        ]

class Sea1_Trophies(Action):
    def __init__(self):
        super().__init__('"They\'ll take your limbs for trophies. Please."')

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
        }

class Sea2_MissYou(Action):
    def __init__(self):
        super().__init__('"I\'ll miss you."')

    # req 5 zeefaring

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            Item.TouchingLoveStory: 1,
        }

class Sea3_ItWasTheMilk(Action):
    def __init__(self):
        super().__init__('"It was the milk... it was the milk, wasn\'t it?"')

    def can_perform(self, state: NadirState):
        return state.get(Item.LightFingers)

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.TouchingLoveStory: 1,
        }

################################################################
#                        Old Bones
################################################################

class OldBones(OpportunityCard):
    def __init__(self):
        super().__init__("Old Bones")
        self.actions = [
            OldBones1_ExamineSite(),
            OldBones2_ExamineSiteWithDaughter()
        ]

class OldBones1_ExamineSite(Action):
    def __init__(self):
        super().__init__("Examine the site")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            Item.TaleOfTerror: 1,
        }

class OldBones2_ExamineSiteWithDaughter(Action):
    def __init__(self):
        super().__init__("Examine the site (A Daughter in the Shadows)")

    # def can_perform(self, state: NadirState):
    #     # TODO 
    #     return state.get(Item.DaughterInTheShadows)

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.VisionOfTheSurface: 1,
            Item.RomanticNotion: 1,
            Item.MemoryOfDistantShores: 1,
            # Item.Melancholy: 3,
            Item.AppallingSecret: 4,
            Item.DramaticTension: 1,
        }

################################################################
#                        Old Sins
################################################################

class OldSins(OpportunityCard):
    def __init__(self):
        super().__init__("Old Sins")
        self.actions = [
            # Thirst(),
            Sins_LookIntoTheWaterWithoutSeeking(),
            # LookIntoTheWaterWithSeeking(),
            Sins_AllowImmaculateEel()
        ]

# class Thirst(Action):
#     def __init__(self):
#         super().__init__("Thirst?")

#     def pass_items(self, state: NadirState):
#         return {
#             Item.DeviousHenchman: -1,
#             Item.RavenousHenchman: 1,
#             Item.Irrigo: 1,
#         }

class Sins_LookIntoTheWaterWithoutSeeking(Action):
    def __init__(self):
        super().__init__("Look into the water (Not Seeking Mr Eaten's Name)")

    # def can_perform(self, state: NadirState):
    #     return state.get(SeekingMrEatensName) == 0

    def pass_rate(self, state):
        return self.broad_pass_rate(250, state.get(Item.Watchful))

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            Item.ExtraordinaryImplication: 1,
            Item.WhisperedHint: 50,
        }

    def fail_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            Item.WhisperedHint: 1,
        }

# class LookIntoTheWaterWithSeeking(Action):
#     def __init__(self):
#         super().__init__("Look into the water (Seeking Mr Eaten's Name)")

#     def can_perform(self, state: NadirState):
#         return state.get(SeekingMrEatensName)

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 2,
#             Item.Nightmares: 2,
#         }

class Sins_AllowImmaculateEel(Action):
    def __init__(self):
        super().__init__("Allow the Immaculate Eel to swim in the water")

    # def can_perform(self, state: NadirState):
    #     return state.get(Item.ImmaculateEel) >= 1 # TODO

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.MemoryOfMuchLesserSelf: 1,
            Item.ExtraordinaryImplication: 1.5
        }

################################################################
#                     Something Moves
################################################################

class SomethingMoves(OpportunityCard):
    def __init__(self):
        super().__init__("Something Moves")
        self.actions = [
            SomethingMoves1_WhatDoYouSee(),
            SomethingMoves2_CanIHelp()
        ]

class SomethingMoves1_WhatDoYouSee(Action):
    def __init__(self):
        super().__init__('"What do you see?"')

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
        }

class SomethingMoves2_CanIHelp(Action):
    def __init__(self):
        super().__init__('"Can I help?"')

    def pass_rate(self, state: NadirState):
        return self.broad_pass_rate(100, state.get(Item.Watchful))

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            # Item.Magnanimous: 3,
        }

    # def fail_items(self, state: NadirState):
    #     return {
    #         Item.Irrigo: 2,
    #         Item.Nightmares: 1,
    #     }

################################################################
#                    The Catafalquerie
################################################################

class TheCatafalquerie(OpportunityCard):
    def __init__(self):
        super().__init__("The Catafalquerie")
        self.actions = [
            Cata1_CasketMarkedWithName(),
            Cata2_EmptyCasket(),
            Cata3_RebelsWhoWillNotRise(),
            # CasketWithBlackRibbon()
        ]

    # def can_draw(self, state):
    #     # is this level or CP?
    #     return state.get(Item.Nightmares) < 21 

# TODO
class Cata1_CasketMarkedWithName(Action):
    def __init__(self):
        super().__init__("A casket marked with a familiar name")

    def pass_items(self, state: NadirState):
        nightmares_level = state.get_pyramidal_level(Item.Nightmares)
        return {
            Item.Nightmares: 1,
            Item.ExtraordinaryImplication: state.get_pyramidal_level(Item.Nightmares) / 2,
            Item.Irrigo: 2,
        }

class Cata2_EmptyCasket(Action):
    def __init__(self):
        super().__init__("An empty casket")

    def pass_items(self, state: NadirState):
        return {
            # Item.Irrigo: 1,
            Item.ExtraordinaryImplication: state.get(Item.Irrigo) // 2,
            Item.Irrigo: 2,
        }

class Cata3_RebelsWhoWillNotRise(Action):
    def __init__(self):
        super().__init__("Rebels who will not rise")

    # def can_perform(self, state: NadirState):
    #     return not state.get(Item.ComplaisantFrostMoth)

    def pass_items(self, state: NadirState):
        return {
            # Item.ComplaisantFrostMoth: 1,
            Item.Echo: 5,
            Item.Irrigo: 1,
        }

# class CasketWithBlackRibbon(Action):
#     def __init__(self):
#         super().__init__("A casket marked with a black ribbon")

#     def can_perform(self, state: NadirState):
#         return state.get(Item.PuttingThePiecesTogetherTasteOfLacre) >= 7

#     def pass_items(self, state: NadirState):
#         return {
#             Item.Irrigo: 2,
#             Item.VialOfTearsOfTheBazaar: 1,
#             Item.AppallingSecret: 1,
#             Item.PuttingThePiecesTogetherTasteOfLacre: -7,
#         }

################################################################
#                   The End of Battles
################################################################

class EndOfBattles(OpportunityCard):
    def __init__(self):
        super().__init__("The End of Battles")
        self.actions = [
            Battles1_Wisdom(),
            Battles2_Pleasure(),
            Battles3_Experience(),
            Battles4_Truth()
        ]

class Battles1_Wisdom(Action):
    def __init__(self):
        super().__init__("Wisdom")

    def pass_items(self, state: NadirState):
        return {
            Item.SuddenInsight: -3,
            Item.BottleOfFourthCityAirag: 1,
            Item.Irrigo: 2,
        }

class Battles2_Pleasure(Action):
    def __init__(self):
        super().__init__("Pleasure")

    def pass_items(self, state: NadirState):
        return {
            Item.HardEarnedLesson: -3,
            Item.NoduleOfPulsatingAmber: 1,
            Item.Irrigo: 2,
        }

class Battles3_Experience(Action):
    def __init__(self):
        super().__init__("Experience")

    def pass_items(self, state: NadirState):
        return {
            Item.HastilyScrawledWarningNote: -3,
            Item.CollectionOfCuriosities: 1,
            Item.Irrigo: 2,
        }

class Battles4_Truth(Action):
    def __init__(self):
        super().__init__("Truth")

    def pass_items(self, state: NadirState):
        return {
            Item.ConfidentSmile: -3,
            Item.SearingEnigma: 1,
            Item.Irrigo: 2,
        }

################################################################
#                 The Hole in Your Head
################################################################

class HoleInYourHead(OpportunityCard):
    def __init__(self):
        super().__init__("The Hole in Your Head")
        self.actions = [
            # RipOutWordsWithoutDiscordantStudies(),
            # RipOutWordsWithDiscordantStudiesCap(),
            # RipOutWordsWithDiscordantStudiesOneCap(),
            Hole_RipOutWordsWithDiscordantStudiesTwoCap()
        ]

    def can_draw(self, state):
        return state.get(Item.DiscordantLaw)

# class RipOutWordsWithoutDiscordantStudies(Action):
#     def __init__(self):
#         super().__init__("Rip out the words (without Discordant Studies)")

#     def pass_items(self, state: NadirState):
#         return {
#             CP.StewardOfTheDiscordance: 1,
#             Item.DiscordantLaw: -1,
#             Item.DiscordantStudies: 1,
#             Item.SomeoneFollowingYou: -1,
#             Item.FrozenThoughts: -1,
#             Item.AnotherMouth: -1,
#             Item.Irrigo: 1,
#         }

# class RipOutWordsWithDiscordantStudiesCap(Action):
#     def __init__(self):
#         super().__init__("Rip out the words (with Discordant Studies, within cap)")

#     def pass_items(self, state: NadirState):
#         return {
#             CP.StewardOfTheDiscordance: 1,
#             Item.DiscordantLaw: -1,
#             Item.SomeoneFollowingYou: -1,
#             Item.FrozenThoughts: -1,
#             Item.AnotherMouth: -1,
#             Item.Irrigo: 1,
#         }

# class RipOutWordsWithDiscordantStudiesOneCap(Action):
#     def __init__(self):
#         super().__init__("Rip out the words (with Discordant Studies, Exactly 1, at cap)")

#     def pass_items(self, state: NadirState):
#         return {
#             Item.CrystallisedEuphoria: 1,
#             Item.CrystallisedCurio: 3,
#             Item.DiscordantLaw: -1,
#             Item.SomeoneFollowingYou: -1,
#             Item.FrozenThoughts: -1,
#             Item.AnotherMouth: -1,
#             Item.Irrigo: 1,
#         }

class Hole_RipOutWordsWithDiscordantStudiesTwoCap(Action):
    def __init__(self):
        super().__init__("Rip out the words (with Discordant Studies, Exactly 2, at cap)")

    def pass_items(self, state: NadirState):
        return {
            Item.DiscordantSoul: 1,
            Item.DiscordantLaw: -1,
            # Item.SomeoneFollowingYou: -1,
            # Item.FrozenThoughts: -1,
            # Item.AnotherMouth: -1,
            Item.Irrigo: 2,
        }

################################################################
#                         The Web
################################################################

class TheWeb(OpportunityCard):
    def __init__(self):
        super().__init__("The Web")
        self.actions = [
            Web_NoWeb(),
            Web_YesWeb(),
            Web_Ascend()
        ]

class Web_NoWeb(Action):
    def __init__(self):
        super().__init__("No")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.HardEarnedLesson: 1,
        }

class Web_YesWeb(Action):
    def __init__(self):
        super().__init__("Yes")

    def pass_items(self, state: NadirState):
        return {
            Item.PuttingThePiecesTogetherTheDrownies: 1,
            Item.Irrigo: 1,
            Item.SuddenInsight: 1,
        }

class Web_Ascend(Action):
    def __init__(self):
        super().__init__("The Third Choice: Ascend")

    # def can_perform(self, state):
    #     state.get(Item.BrachiatingSpindlewolf) > 1,

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            Item.ExtraordinaryImplication: 1,
            Item.Nightmares: 2,
        }

################################################################
#                  Unjustly Imprisoned!
################################################################

class UnjustlyImprisoned(OpportunityCard):
    def __init__(self):
        super().__init__("Unjustly Imprisoned!")
        self.actions = [
            Imprisoned_RecallWhereYouAre(),
            Imprisoned_ConcentrateOnEscaping()
        ]

class Imprisoned_RecallWhereYouAre(Action):
    def __init__(self):
        super().__init__("Recall where you are")

    def pass_items(self, state: NadirState):
        return {
            # Item.Watchful: -2,
            Item.Irrigo: 2,
            Item.CrypticClue: 1,
        }

class Imprisoned_ConcentrateOnEscaping(Action):
    def __init__(self):
        super().__init__("Concentrate on escaping!")

    def pass_items(self, state: NadirState):
        return {
            # Item.Dangerous: -1,
            # Item.Persuasive: -1,
            # Item.Shadowy: -1,
            # Item.Watchful: -1,
            Item.Irrigo: 1,
        }

################################################################
#                   Woods in Winter
################################################################

class WoodsInWinter(OpportunityCard):
    def __init__(self):
        super().__init__("Woods in winter")
        self.actions = [
            Woods_FortunesPage(),
            # DanceGoesOnWithoutClathermont(),
            Woods_DanceGoesOnWithClathermont()
        ]

class Woods_FortunesPage(Action):
    def __init__(self):
        super().__init__("Fortune's page")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 1,
            # Item.CountingTheDays: 1, # TODO
        }

# class DanceGoesOnWithoutClathermont(Action):
#     def __init__(self):
#         super().__init__("The dance goes on (without Clathermont Family 30)")

#     def can_perform(self, state: NadirState):
#         return not state.has(Item.EntwinedInTheIntriguesOfTheClathermontFamily, 30)

#     def pass_items(self, state: NadirState):
#         return {
#             # TODO
#             # Item.DramaticTension: 1,  # Rare success only
#             Item.FavoursRevolutionaries: 1,
#             Item.FavoursTheGreatGame: 1,
#             Item.FavoursSociety: 1,
#             Item.Irrigo: 2,
#         }

class Woods_DanceGoesOnWithClathermont(Action):
    def __init__(self):
        super().__init__("The dance goes on (with Clathermont Family 30)")

    # TODO
    # def can_perform(self, state: NadirState):
    #     return state.get(Item.EntwinedInTheIntriguesOfTheClathermontFamily) >= 30

    def pass_items(self, state: NadirState):
        return {
            Item.DramaticTension: 1,
            Item.FavRevolutionaries: 1,
            Item.FavGreatGame: 1,
            Item.FavSociety: 1,
            Item.Irrigo: 2,
        }

################################################################
#                   The Sound of Wings
################################################################

class SoundOfWings(OpportunityCard):
    def __init__(self):
        super().__init__("The Sound of Wings")
        self.actions = [
            SoundOfWings1_Confront(),
        ]

    def can_draw(self, state):
        return state.get(Item.WingsOfChange) > 0

class SoundOfWings1_Confront(Action):
    def __init__(self):
        super().__init__("Confront it")

    def pass_items(self, state: NadirState):
        return {
            Item.Irrigo: 2,
            Item.WingsOfChange: -1,
            Item.MemoryOfAMuchStrangerSelf: 1,
            Item.CausticApocryphon: 1
        }


class NadirSimRunner(SimulationRunner):
    def __init__(self, runs: int, initial_values: dict):
        super().__init__(runs, initial_values)


        self.storylets = [
            StoryletNadir()
        ]

        self.cards = [
            CardGame(),
            FamiliarFace(),
            PauseForRefreshment(),
            WakingDreamOfMotion(),
            WakingDreamOfReflections(),
            WakingDreamOfWater(),
            WeaknessInTheAir(),
            AltarfulOfStrangers(),
            UnlikelyGarden(),
            RecallHowTheyCame(),
            Losing(),
            LostAtSea(),
            OldBones(),
            OldSins(),
            SomethingMoves(),
            TheCatafalquerie(),
            EndOfBattles(),
            HoleInYourHead(),
            SoundOfWings(),
            TheWeb(),
            UnjustlyImprisoned(),
            WoodsInWinter()
        ]

    def create_state(self):
        state = NadirState()
        return state
    
runner = NadirSimRunner(
    runs = 20000,
    initial_values= {
        # Item.
        Item.WingsOfChange: 1,
        Item.Nightmares: 0,
        # Item.DiscordantLaw: 1
    }
)

runner.outfit = PlayerOutfit(340, 18)

runner.run_simulation()