import random
import sys
import math
from collections import defaultdict
from enum import Enum, auto

from enums import *
from simulations.models import *
from simulations.models import GameState

'''
TODO
figure out how to handle non-standard outcomes
- rare success
    - constant bugbear in these sims
    - we don't know what the odds are for any given card
    - we don't know which cards share odds, if any
    - we don't know if odds are constant wrt. anything
    - therefore, reasonable options:
        - ignore it entirely
        - pick an arbitrary number and use it for everything
- alternate success
    - wiki distinguishes btw this and rare success
        - not sure if this is acknowledged in-game?
        - rare success is usually a significant bonus
        - alternate successes are side-grades, eg. different item of equal value
    - how to handle
        - (preferred) assume it's 50/50 with normal success
        - ignore it
            - need to handle it for the student cards at least
            - otherwise assumes we can avoid disgruntlement indefinitely
        - use whatever number we pick for rare success
- alternate failure
    - treat it the same as alternate success?
    - some cards are luck challenges with both alternate success and alternate failure
        - can assume these are meant to be roughly 1-in-4 random
        - except they're not all 50% challenges so idk 
- rare failure
    - treat same as rare success?
    - can be better than regular failure, eg. gain sotc


add the rest of the experts and students
- starting with the recommended lineup for convenience
    - visionary student
    - gifted student
    - silk-clad expert
    - lettice

crappy cards that you can remove/replace
- the two super early ones
    - One day...
    - Blank walls
- various cards with workers < 3
    - washing up
    - unpacking crates
    - filing a report
    work with your equipment

handling students
- add graduation and hiring storylets

'''

class LabState(GameState):
    def __init__(self):
        super().__init__()
        self.status = "InProgress"

        self.outfit = OutfitList(300, 18)

        self.items = {
            # Experiment
            Item.LaboratoryResearch: 0,
            Item.TotalLabReserchRequired: 2700,
            Item.ExperimentalObject: 820,

            # Progression qualities
            Item.EquipmentForScientificExperimentation: 9,
            Item.PrestigeOfYourLaboratory: 100,
            Item.NumberOfWorkersInYourLaboratory: 4,
            Item.ScholarOfTheCorrespondence: 21,

            # Workers
            Item.LaboratoryServicesOfLetticeTheMercy: 1,
            Item.LaboratoryServicesOfSilkCladExpert: 1,
            Item.LaboratoryServicesFromGiftedStudent: 5,
            Item.LaboratoryServicesFromVisionaryStudent: 5
        }

        self.storylets = [
            AlwaysAvailable()
        ]

        self.hand = []

        self.deck = [
            # Short
            PreparingForBriefExperiment(),

            # Long
            FormNewHypotheses(),
            ReviewThePriorLiterature(),
            UnorthodoxMethods(),
            RefreshYourConsumables(),
            DirectingYourTeam(),
            EngageInEmpiricalResearch(),
            WriteUpYourFindings(),

            # Very long
            RunningOutOfSteam(),
            RunningOutOfTerms(),

            # Special items
            TheIntrusionOfAThought(),
            Eureka(),
            ReadBooksOthersCannot(),
            InvolveSecretCollege(),
            InvokeLongDeadPriests(),
            GenericMan1Card(),

            # Experts
            RelyOnLettice(),
            RelyOnSilkCladExpert(),

            # Students
            WorkWithYourGiftedStudent(),
            WorkWithYourVisionaryStudent()
        ]

    def equipment(self):
        return self.items.get(Item.EquipmentForScientificExperimentation, 0)
    
    def preparations(self):
        return self.items.get(Item.ResearchPreparations, 0)

    def highest_worker_level(self):
        # assuming we always have an expert
        return 5

    def equipment_formula1(self):
        equipment = self.equipment()
        if equipment < 4:
            return 2 * equipment
        elif equipment == 4:
            return 9
        else:
            return 4 * equipment - 8
        

    def advanced_skill_formula1(self, stat):
        # TODO not the exact formula
        return min(6 + (2 * stat), 34)

    def advanced_skill_formula2(self, stat):
        if stat <= 5:
            return stat + 2
        elif stat <= 8:
            return stat + 3
        else:
            return min(15, stat+4)
        
    def ev_from_item(self, item, val: int):
        research_unit_ev = 1
        if item == Item.LaboratoryResearch:
            return val * research_unit_ev
        elif item == Item.UnwiseIdea:
            return 7 * research_unit_ev
        elif item == Item.UnexpectedResult:
            return 7 * research_unit_ev
        elif item == Item.UnlikelyConnection:
            return 4 * research_unit_ev
        else:
            return 0

        
    def step(self):
        # TODO smart redraw
        while len(self.hand) < 3:
            self.draw_card()

        best_card, best_action, best_action_ev = None, None, -float('inf')

        for card in self.hand:
            for action in card.actions:
                if action.can_perform(self):
                    action_ev = 0
                    for i in range(1,6):
                        zailing_bonus_estimate = i
                        action_ev += action.ev(self)
                    action_ev /= 5.0
                    if action_ev > best_action_ev:
                        best_card, best_action, best_action_ev = card, action, action_ev

        # for card in self.hand:
        #     for action in card.actions:
        #         if action.can_perform(self):
        #             attempts = 50
        #             action_ev = sum(action.ev(self) for _ in range(attempts)) / attempts
        #             if action_ev > best_action_ev:
        #                 best_card, best_action, best_action_ev = card, action, action_ev

        if best_action:
            outcome = best_action.perform(self)
            self.action_play_counts[best_action.name] += 1
            self.actions += best_action.action_cost
            # self.region_action_counts[self.current_region] += best_action.action_cost
            # print(best_action.name)
            if outcome == "Success":
                self.action_success_counts[best_action.name] += 1
            else:
                self.action_failure_counts[best_action.name] += 1

        if best_card is not None:
            self.card_play_counts[best_card.name] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)            

        # if self.items[Item.TroubledWaters] >= 36:
        #     self.status = "Failure"
        # elif self.items[Item.ZailingProgress] >= self.progress_required:
        #     self.go_to_next_region()

        self.hand = [card for card in self.hand if card.can_draw(self)]

        research = self.items.get(Item.LaboratoryResearch, 0)

        # TODO other research types
        if self.items.get(Item.LaboratoryResearch, 0) >= self.items.get(Item.TotalLabReserchRequired):
            self.status = "Success"

    def run(self):
        while self.status == "InProgress":
            self.step()

################################################################################
###                            Actions always available                      ###
################################################################################

class AlwaysAvailable(OpportunityCard):
    def __init__(self):
        super().__init__("London storylets & social actions")
        self.actions = [
            ReduceWoundsSocial1(),
            ReduceWoundsSocial2(),
            ReduceNightmaresSocial1(),
            ReduceNightmaresSocial2(),
            ReduceScandalSocial1(),
            ReduceSuspicionSocial1(),
            SendNameWrittenInGant()
        ]

class ReduceWoundsSocial1(Action):
    def __init__(self):
        super().__init__("Allow them to bandage you")

    def can_perform(self, state: GameState):
        return state.items.get(Item.Wounds, 0) > 0

    def pass_items(self, state: LabState):
        wounds = state.items.get(Item.Wounds, 0)
        lessons = state.items.get(Item.SuddenInsight, 0)
        return {
            Item.HardEarnedLesson: 1 if lessons < 20 else 0,
            Item.Wounds: -1 * max(4, wounds)
        }
    
class ReduceWoundsSocial2(Action):
    def __init__(self):
        super().__init__("Drink the medicine they bring")

    def can_perform(self, state: GameState):
        return state.items.get(Item.Wounds, 0) > 0

    def pass_items(self, state: LabState):
        wounds = state.items.get(Item.Wounds, 0)
        return {
            Item.Wounds: -1 * max(6, wounds)
        }

class ReduceNightmaresSocial1(Action):
    def __init__(self):
        super().__init__("Allow them to watch over your rest")

    def can_perform(self, state: GameState):
        return state.items.get(Item.Nightmares, 0) > 0

    def pass_items(self, state: LabState):
        nightmares = state.items.get(Item.Nightmares, 0)
        insights = state.items.get(Item.SuddenInsight, 0)
        return {
            Item.SuddenInsight: 1 if insights < 20 else 0,
            Item.Nightmares: -1 * max(4, nightmares)
        }    
    
class ReduceNightmaresSocial2(Action):
    def __init__(self):
        super().__init__("Allow them to watch over your rest")

    def can_perform(self, state: GameState):
        return state.items.get(Item.Nightmares, 0) > 0

    def pass_items(self, state: LabState):
        nightmares = state.items.get(Item.Nightmares, 0)
        return {
            Item.Nightmares: -1 * max(6, nightmares)
        }
    
class ReduceScandalSocial1(Action):
    def __init__(self):
        super().__init__("Write to the newspaper about your acquaintance's virtue")

    def can_perform(self, state: GameState):
        return state.items.get(Item.Scandal, 0) > 0

    def pass_items(self, state: LabState):
        current = state.items.get(Item.Scandal, 0)
        return {
            Item.Scandal: -1 * max(5, current)
        }
    
class ReduceSuspicionSocial1(Action):
    def __init__(self):
        super().__init__("Reduce suspicion with social action")

    def can_perform(self, state: GameState):
        return state.items.get(Item.Suspicion, 0) > 0

    def pass_items(self, state: LabState):
        current = state.items.get(Item.Suspicion, 0)
        return {
            Item.Suspicion: -1 * max(4, current)
        }
    
class SendNameWrittenInGant(Action):
    def __init__(self):
        super().__init__("Send a name, written in Gant")

    def can_perform(self, state: GameState):
        return (state.items.get(Item.Suspicion, 0) > 0 or
                state.items.get(Item.Scandal, 0) > 0)

    def pass_items(self, state: LabState):
        scandal = state.items.get(Item.Scandal, 0)
        suspicion = state.items.get(Item.Suspicion, 0)
        return {
            Item.PieceOfRostygold: -500,
            Item.Scandal: -1 * max(6, scandal),
            Item.Suspicion: -1 * max(6, suspicion)
        }    

################################################################################
###                            PreparingForBriefExperiment                   ###
################################################################################

class PreparingForBriefExperiment(OpportunityCard):
    def __init__(self):
        super().__init__("Preparing for a brief Experiment")
        self.actions = [
            PrepareCarefully(), 
            LookForNovelAngle(),
            RelyOnBrilliance(),
            QuickJauntIntoParabola()
        ]
        self.weight = 1_000_000 # Ubiquitous Frequency
    
    def can_draw(self, state: LabState):
        return state.items.get(Item.NoLongerReviewingLiterature, 0) == 0 and \
            state.items.get(Item.TotalLabReserchRequired, 0) < 200

class PrepareCarefully(Action):
    def __init__(self):
        super().__init__("Prepare carefully")
    
    def pass_items(self, state: LabState):
        return {
            Item.ResearchPreparations: 10,
            Item.NoLongerReviewingLiterature: 1,
            Item.LaboratoryResearch: state.equipment_formula1(),
        }

class LookForNovelAngle(Action):
    def __init__(self):
        super().__init__("Look for a novel angle")
    
    def pass_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: 3,
            Item.NoLongerReviewingLiterature: 1,
            Item.LaboratoryResearch: state.equipment_formula1(),
        }

class RelyOnBrilliance(Action):
    def __init__(self):
        super().__init__("Rely on your own brilliance")

    def can_perform(self, state: LabState):
        return (state.items.get(Item.EquipmentForScientificExperimentation, 0) >= 7 and 
                state.items.get(Item.PrestigeOfLaboratory, 0) >= 20)
    
    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(170, state.outfit.watchful)
    
    def pass_items(self, state: LabState):
        return {
            Item.UnavoidableEpiphany: 1,
            Item.NoLongerReviewingLiterature: 1,
            Item.LaboratoryResearch: state.equipment_formula1()
        }
    
    def fail_items(self, state: LabState):
        return {
            Item.UnwiseIdea: 1,
            Item.LaboratoryResearch: 10,
            Item.NoLongerReviewingLiterature: 1,
            Item.Wounds: 2
        }

# TODO: discount for Silverer
class QuickJauntIntoParabola(Action):
    def __init__(self):
        super().__init__("Begin with a quick jaunt into Parabola")
    
    def can_perform(self, state: LabState):
        # return (state.items.get(Item.RouteLabReflection, 0) > 0 and 
        #         state.items.get(Item.DropOfPrisonersHoney, 0) >= 50 and 
        #         state.items.get(Item.GlassStudies, 0) >= 2)
        return True

    def pass_items(self, state: LabState):
        return {
            Item.ParabolanResearch: 15,
            Item.DropOfPrisonersHoney: -50
        }
    
    def fail_items(self, state: LabState):
        return {
            Item.DropOfPrisonersHoney: -100
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(5, state.outfit.glasswork)
    
################################################################################
###                            FormNewHypotheses                             ###
################################################################################

class FormNewHypotheses(OpportunityCard):
    def __init__(self):
        super().__init__("Form New Hypotheses")
        self.actions = [
            ReviewPossibilities(),
            ConsiderEveryPossibility(),
            NoMoreOfThis()
        ]
        self.weight = 2.0  # Frequent Frequency
    
    def can_draw(self, state: LabState):
        return state.items.get(Item.NoLongerFormingHypotheses, 0) == 0 and \
            state.items.get(Item.TotalLabReserchRequired, 0) >= 200

class ReviewPossibilities(Action):
    def __init__(self):
        super().__init__("Review the possibilities")
    
    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 4 + state.equipment(),
            Item.ResearchPreparations: 5
        }

    # TODO rate
    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 8 + state.equipment(),
            Item.ResearchPreparations: 20,
            Item.UnwiseIdea: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: state.equipment()
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(150 - state.preparations(), state.outfit.watchful)

class ConsiderEveryPossibility(Action):
    def __init__(self):
        super().__init__("Consider every possibility")
    
    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 4 + state.equipment(),
            Item.UnlikelyConnection: 5,
        }

    def fail_items(self, state: LabState):
        return {
            Item.UnwiseIdea: 1,
            Item.LaboratoryResearch: state.equipment()
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(180 - state.preparations(), state.outfit.watchful)

class NoMoreOfThis(Action):
    def __init__(self):
        super().__init__("No more of this!")

    def can_perform(self, state: GameState):
        req = state.items[Item.TotalLabReserchRequired]
        return state.items[Item.LaboratoryResearch] >= req/6
    
    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 8 + state.equipment(),
            Item.NoLongerFormingHypotheses: 1
        }

################################################################################
###                            ReviewThePriorLiterature                      ###
################################################################################

class ReviewThePriorLiterature(OpportunityCard):
    def __init__(self):
        super().__init__("Review the Prior Literature")
        self.actions = [
            ReadCanonicalTexts(),
            ChaseDownCitations(),
            GatherUnofficialLiterature(),
            RelateToPastEnigma(),
            NoMoreOfThisLiterature()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: LabState):
        return state.items.get(Item.NoLongerReviewingLiterature, 0) == 0 and \
            state.items.get(Item.TotalLabReserchRequired, 0) >= 200

class ReadCanonicalTexts(Action):
    def __init__(self):
        super().__init__("Read the canonical texts; make pertinent notes")
    
    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 4 + state.equipment(),
            Item.ResearchPreparations: 5
        }

    # TODO
    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 8 + state.equipment(),
            Item.ResearchPreparations: 10
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: state.equipment()
        }

    def pass_rate(self, state: LabState):
        difficulty = 150 - state.preparations()
        return self.broad_pass_rate(difficulty, state.outfit.watchful)


class ChaseDownCitations(Action):
    def __init__(self):
        super().__init__("Chase down every last citation")
    
    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 4 + state.equipment(),
            Item.UnlikelyConnection: 5
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: state.equipment()
        }

    def pass_rate(self, state: LabState):
        difficulty = 220 - state.preparations()
        return self.broad_pass_rate(difficulty, state.outfit.watchful)


class GatherUnofficialLiterature(Action):
    def __init__(self):
        super().__init__("Gather some unofficial literature")
    
    def can_perform(self, state: LabState):
        # return state.items.get(Item.IncisiveObservation, 0) >= 5
        return True
    
    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 2 * state.equipment(),
            Item.UnlikelyConnection: 5,
            Item.IncisiveObservation: -5
        }

    # TODO alternative failure?
    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: state.equipment()
        }

    def pass_rate(self, state: LabState):
        difficulty = 190 - state.preparations()
        return self.broad_pass_rate(difficulty, state.outfit.watchful)


class RelateToPastEnigma(Action):
    def __init__(self):
        super().__init__("Relate this problem to a past Enigma")

    def can_perform(self, state: LabState):
        # return (state.items.get(Item.SearingEnigma, 0) >= 1 and
        research_remaining = (state.items[Item.TotalLabReserchRequired] -
                              state.items[Item.LaboratoryResearch])
        return (research_remaining >= 500 and 
            1001 <= state.items.get(Item.ExperimentalObject, 0) <= 1200)
    
    def pass_items(self, state: LabState):
        focus_bonus = 25 * state.items.get(Item.CorrespondenceFocus, 0)
        return {
            Item.LaboratoryResearch: 500 + focus_bonus,
            Item.SearingEnigma: -1,
            Item.UnavoidableEpiphany: 1,
            Item._HandClear: 1
        }
        
    def perform_pass(self, state: LabState):
        super().perform_pass(state)
        state.clear_hand()  # Clears hand after the action

    def fail_items(self, state: LabState):
        focus_bonus = 25 * state.items.get(Item.CorrespondenceFocus, 0)
        return {
            Item.SearingEnigma: -1,
            Item.LaboratoryResearch: 500 + focus_bonus
        }

    def pass_rate(self, state: LabState):
        difficulty = 220 - state.preparations()
        return self.broad_pass_rate(difficulty, state.outfit.watchful)

class NoMoreOfThisLiterature(Action):
    def __init__(self):
        super().__init__("No more of this!")

    def pass_items(self, state: LabState):
        return {
            Item.NoLongerReviewingLiterature: 1,
            Item.LaboratoryResearch: 8 + state.equipment()
        }

################################################################################
###                            EngageInEmpiricalResearch                     ###
################################################################################

class EngageInEmpiricalResearch(OpportunityCard):
    def __init__(self):
        super().__init__("Engage in some Empirical Research")
        self.actions = [
            SimpleExperiment(),
            HookUpMeters(),
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: LabState):
        return (
            state.items.get(Item.NoLongerFormingHypotheses, 0) > 0 and
            state.items.get(Item.NoLongerResupplying, 0) > 0
        )

class SimpleExperiment(Action):
    def __init__(self):
        super().__init__("Perform a comparatively simple experiment")
    
    def pass_items(self, state: LabState):
        return {
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: 4 + state.equipment()
        }

    # TODO rare success
    def rare_success_items(self, state: LabState):
        return {
            Item.UnwiseIdea: 1,
            Item.LaboratoryResearch: 8 + state.equipment()
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: state.equipment(),
            Item.Wounds: 2
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(200 - state.preparations(), state.outfit.dangerous)

class HookUpMeters(Action):
    def __init__(self):
        super().__init__("Hook up all the meters and stand well back")
    
    def pass_items(self, state: LabState):
        return {
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: 12 + 2 * state.equipment(),
            Item.NoLongerResupplying: 0 - state.items.get(Item.NoLongerResupplying, 0),
            Item._HandClear: 1
        }
    
    def perform_pass(self, state: LabState):
        super().perform_pass(state)
        state.clear_hand()  # Clears hand after the action

    # TODO
    def rare_success_items(self, state: LabState):
        return {
            Item.UnwiseIdea: 1,
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: 12 + 2 * state.equipment(),
            Item.NoLongerResupplying: 0 - state.items.get(Item.NoLongerResupplying, 0),
            Item._HandClear: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.Wounds: 2,
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(250 - state.preparations(), state.outfit.dangerous)


################################################################################
###                            UnorthodoxMethods                             ###
################################################################################

# TODO wiki inconsistent re: difficulty, big table says 8 but page says 7
class UnorthodoxMethods(OpportunityCard):
    def __init__(self):
        super().__init__("Unorthodox Methods")
        self.actions = [
            UseRedScience(),
            ExperimentInParabola(),
            RearrangeBrain(),
            AdoptBetterFrameOfMind()
        ]
        self.weight = 0.5  # Very Infrequent Frequency
    
    def can_draw(self, state: LabState):
        return (state.items.get(Item.TotalLabReserchRequired, 0) >= 200 and
            state.items.get(Item.UnlikelyConnection, 0) >= 1 and
            state.items.get(Item.PrestigeOfYourLaboratory, 0) >= 20)

class UseRedScience(Action):
    def __init__(self):
        super().__init__("Use what you know of the Red Science")
    
    def pass_items(self, state: LabState):
        stat = state.outfit.artisan_of_the_red_science
        return {
            Item.UnlikelyConnection: -1,
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: state.advanced_skill_formula1(stat)
        }

    def fail_items(self, state: LabState):
        stat = state.outfit.artisan_of_the_red_science
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: state.advanced_skill_formula2(stat),
            Item.Wounds: 1
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(7, state.outfit.artisan_of_the_red_science)

class ExperimentInParabola(Action):
    def __init__(self):
        super().__init__("Perform an experiment in Parabola")
    
    def pass_items(self, state: LabState):
        stat = state.outfit.glasswork
        return {
            Item.UnlikelyConnection: -1,
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: state.advanced_skill_formula1(stat)
        }

    def fail_items(self, state: LabState):
        stat = state.outfit.glasswork
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: state.advanced_skill_formula2(stat),
            Item.Nightmares: 1
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(7, state.outfit.glasswork)

class RearrangeBrain(Action):
    def __init__(self):
        super().__init__("Rearrange your brain around the problem")
    
    def pass_items(self, state: LabState):
        stat = state.outfit.shapeling_arts
        return {
            Item.UnlikelyConnection: -1,
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: state.advanced_skill_formula1(stat)
        }

    def fail_items(self, state: LabState):
        stat = state.outfit.shapeling_arts
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: state.advanced_skill_formula2(stat),
            Item.Nightmares: 1
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(7, state.outfit.shapeling_arts)

class AdoptBetterFrameOfMind(Action):
    def __init__(self):
        super().__init__("Adopt a better frame of mind")

    def pass_items(self, state: LabState):
        stat = state.outfit.kataleptic_toxicology
        return {
            Item.UnlikelyConnection: -1,
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: state.advanced_skill_formula1(stat)
        }

    def fail_items(self, state: LabState):
        stat = state.outfit.kataleptic_toxicology
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: state.advanced_skill_formula2(stat),
            Item.Wounds: 1
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(7, state.outfit.kataleptic_toxicology)

################################################################################
###                            RefreshYourConsumables                        ###
################################################################################

class RefreshYourConsumables(OpportunityCard):
    def __init__(self):
        super().__init__("Refresh your Consumables")
        self.actions = [
            DemandDelivery(),
            AllowPossessionsToPropagate(),
            WorkThroughIntermediary(),
            RelyOnIllicitContacts(),
            AppropriateWhateverYouNeed()
        ]
        self.weight = 1.0  # Standard Frequency
    
    def can_draw(self, state: LabState):
        return state.items.get(Item.NoLongerResupplying, 0) == 0 and \
            state.items.get(Item.TotalLabReserchRequired, 0) >= 200

class DemandDelivery(Action):
    def __init__(self):
        super().__init__("Demand a delivery")
    
    def can_perform(self, state: LabState):
        # Treasure
        return state.items.get(Item.RobeOfMrCards, 0) > 0

    def pass_items(self, state: LabState):
        return {
            Item.NoLongerResupplying: 1,
            Item.LaboratoryResearch: 12 + 2 * state.equipment(),
            Item.UnexpectedResult: 1
        }

class AllowPossessionsToPropagate(Action):
    def __init__(self):
        super().__init__("Allow your possessions to propagate on your own")
    
    def can_perform(self, state: LabState):
        # Treasure
        return state.items.get(Item.KittenSizedDiamond, 0) > 0

    def pass_items(self, state: LabState):
        return {
            Item.NoLongerResupplying: 1,
            Item.LaboratoryResearch: 12 + 2 * state.equipment(),
            Item.UnexpectedResult: 1
        }

class WorkThroughIntermediary(Action):
    def __init__(self):
        super().__init__("Work through a trusted intermediary")
    
    def pass_items(self, state: LabState):
        return {
            Item.NoLongerResupplying: 1,
            Item.LaboratoryResearch: 8 + 2 * state.equipment(),
        }

    # TODO
    def rare_success_items(self, state: LabState):
        return {
            Item.NoLongerResupplying: 1,
            Item.LaboratoryResearch: 10 + 2 * state.equipment(),
        }

    # TODO alternate failure? seems identical
    def fail_items(self, state: LabState):
        return {
            Item.NoLongerResupplying: 1,
            Item.LaboratoryResearch: state.equipment(),
            Item.Scandal: 2
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(150, state.outfit.persuasive)

class RelyOnIllicitContacts(Action):
    def __init__(self):
        super().__init__("Rely on illicit contacts")

    def can_perform(self, state: LabState):
        # return state.items.get(Item.ConnectedTheWidow, 0) >= 5
        return True

    def pass_items(self, state: LabState):
        return {
            Item.NoLongerResupplying: 1,
            Item.LaboratoryResearch: state.equipment_formula1(), # unsure
        }

    def fail_items(self, state: LabState):
        return {
            Item.Suspicion: 1.5
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(200, state.outfit.shadowy)

class AppropriateWhateverYouNeed(Action):
    def __init__(self):
        super().__init__("Appropriate whatever you need")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.VastNetworkOfConnections, 0) > 0

    def pass_items(self, state: LabState):
        return {
            Item.NoLongerResupplying: 1,
            Item.LaboratoryResearch: 12 + 2 * state.equipment(),
            Item.UnexpectedResult: 1
        }


################################################################################
###                            DirectingYourTeam                             ###
################################################################################

class DirectingYourTeam(OpportunityCard):
    def __init__(self):
        super().__init__("Directing your Team")
        self.actions = [
            PutThemToWork(),
            GiveLineOfInquiry(),
            CoordinatePlanOfResearchNoDisgruntlement(),
            CoordinatePlanOfResearchDisgruntlement(),
            GiveDayOff(),
            TakeDayOff()
        ]
        self.weight = 0.8  # Infrequent Frequency
    
    def can_draw(self, state: LabState):
        return (state.items.get(Item.NoLongerFormingHypotheses, 0) >= 1 and
                state.items.get(Item.NumberOfWorkersInYourLaboratory, 0) >= 3 and
                state.items.get(Item.TotalLabReserchRequired, 0) >= 200 and
                state.items.get(Item.NoLongerReviewingLiterature, 0) >= 1)

class PutThemToWork(Action):
    def __init__(self):
        super().__init__("Put them to work examining data")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.UnexpectedResult, 0) > 0

    def pass_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        highest_worker_level = state.highest_worker_level()
        equipment_level = state.items.get(Item.EquipmentForScientificExperimentation, 0)
        lab_research = (2 + 0.2 * equipment_level) * (num_workers**0.5) * highest_worker_level
        return {
            Item.UnexpectedResult: -1,
            Item.LaboratoryResearch: lab_research
        }

    # TODO
    def rare_success_items(self, state: LabState):
        items = self.pass_items(state)
        items.update({
            Item.UnwiseIdea: 1,
            Item.Nightmares: 1
        })
        return items

class GiveLineOfInquiry(Action):
    def __init__(self):
        super().__init__("Give them a line of inquiry to follow up on")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.UnavoidableEpiphany, 0) > 0

    def pass_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        highest_worker_level = state.highest_worker_level()
        equipment_level = state.items.get(Item.EquipmentForScientificExperimentation, 0)
        lab_research = (2 + 0.2 * equipment_level) * (num_workers**0.5) * highest_worker_level
        return {
            Item.UnavoidableEpiphany: -1,
            Item.LaboratoryResearch: lab_research
        }

class CoordinatePlanOfResearchNoDisgruntlement(Action):
    def __init__(self):
        super().__init__("Coordinate a plan of research (No Disgruntlement)")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.DisgruntlementAmongStudents, 0) == 0

    def pass_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        highest_worker_level = state.highest_worker_level()
        equipment_level = state.items.get(Item.EquipmentForScientificExperimentation, 0)
        lab_research = (2 + 0.08 * equipment_level) * (num_workers**0.5) * highest_worker_level
        return {
            Item.LaboratoryResearch: lab_research
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 6 + 1.25 * state.items.get(Item.EquipmentForScientificExperimentation, 0)
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(210 - state.preparations(), state.outfit.persuasive)

class CoordinatePlanOfResearchDisgruntlement(Action):
    def __init__(self):
        super().__init__("Coordinate a plan of research (Disgruntlement)")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.DisgruntlementAmongStudents, 0) > 0

    def pass_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        highest_worker_level = state.highest_worker_level()
        equipment_level = state.items.get(Item.EquipmentForScientificExperimentation, 0)
        lab_research = (2 + 0.08 * equipment_level) * (num_workers**0.5) * highest_worker_level
        return {
            Item.LaboratoryResearch: lab_research,
            Item.DisgruntlementAmongStudents: 1  # Increases Disgruntlement on success
        }

    # TODO
    def alternative_success_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        highest_worker_level = state.highest_worker_level()
        equipment_level = state.items.get(Item.EquipmentForScientificExperimentation, 0)
        lab_research = (2 + 0.2 * equipment_level) * (num_workers**0.5) * highest_worker_level
        return {
            Item.LaboratoryResearch: lab_research,
            Item.DisgruntlementAmongStudents: 1  # Increases Disgruntlement on alternative success
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 6 + 1.25 * state.items.get(Item.EquipmentForScientificExperimentation, 0),
            Item.DisgruntlementAmongStudents: 1
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(210, state.outfit.persuasive)

class GiveDayOff(Action):
    def __init__(self):
        super().__init__("Give them a day off")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.DisgruntlementAmongStudents, 0) >= 3

    def pass_items(self, state: LabState):
        return {
            Item.DisgruntlementAmongStudents: -2,
            # TODO round up
            Item.LaboratoryResearch: 6 + (1.25 * state.items.get(Item.EquipmentForScientificExperimentation, 0))
        }

class TakeDayOff(Action):
    def __init__(self):
        super().__init__("Take a day off")
    
    def pass_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        highest_worker_level = state.highest_worker_level()
        equipment_level = state.items.get(Item.EquipmentForScientificExperimentation, 0)
        lab_research = (2 + 0.08 * equipment_level) * (num_workers**0.5) * highest_worker_level
        return {
            Item.LaboratoryResearch: lab_research,
            Item.Nightmares: -2,
            Item.DisgruntlementAmongStudents: 2 # TODO only if already > 0
        }

    # TODO
    def alternative_success_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        highest_worker_level = state.highest_worker_level()
        equipment_level = state.items.get(Item.EquipmentForScientificExperimentation, 0)
        lab_research = (2 + 0.08 * equipment_level) * (num_workers**0.5) * highest_worker_level
        return {
            Item.LaboratoryResearch: lab_research,
            Item.Suspicion: -2,
        }

    # TODO alt failure, same but -scandal
    def fail_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        highest_worker_level = state.highest_worker_level()
        equipment_level = state.items.get(Item.EquipmentForScientificExperimentation, 0)
        lab_research = (2 + 0.08 * equipment_level) * (num_workers**0.5) * highest_worker_level
        return {
            Item.LaboratoryResearch: lab_research,
            Item.Wounds: -2,
            Item.DisgruntlementAmongStudents: 2 # TODO only if already > 0
        }

    def pass_rate(self, state: LabState):
        return 0.4  # Fixed 40% chance


################################################################################
###                            WriteUpYourFindings                           ###
################################################################################

class WriteUpYourFindings(OpportunityCard):
    def __init__(self):
        super().__init__("Write up your findings")
        self.actions = [
            CirculateDraft(),
            OrganiseNotes()
        ]
        self.weight = 0.5  # Very Infrequent Frequency
    
    def can_draw(self, state: LabState):
        return (state.items.get(Item.LaboratoryResearch, 0) >= 200 and
                state.items.get(Item.NoLongerWritingUp, 0) == 0)

# TODO need to be smart about when to use this card
class CirculateDraft(Action):
    def __init__(self):
        super().__init__("Circulate a draft of your findings")

    def pass_items(self, state: LabState):
        # Calculate the research gained based on the formula provided
        lab_research = state.items.get(Item.LaboratoryResearch, 0)
        total_lab_required = state.items.get(Item.TotalLabReserchRequired, 1)
        unexpected_result = state.items.get(Item.UnexpectedResult, 0)

        research_gain = (100 * lab_research / total_lab_required) + \
                        (10 * unexpected_result ** (0.9 + total_lab_required / 200_000))

        return {
            Item.NoLongerWritingUp: 1,
            Item.LaboratoryResearch: research_gain,
            Item.UnexpectedResult: 0 - state.items.get(Item.UnexpectedResult, 0)
        }

    def fail_items(self, state: LabState):
        return {
            Item.Scandal: 2
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(200, state.outfit.watchful)

class OrganiseNotes(Action):
    def __init__(self):
        super().__init__("Organise your notes")

    def can_perform(self, state: LabState):
        return state.items.get(Item.UnexpectedResult, 0) >= 2

    def pass_items(self, state: LabState):        
        return {
            Item.UnavoidableEpiphany: 1,
            Item.UnexpectedResult: -2,
            Item.LaboratoryResearch: state.equipment_formula1()
        }

    def fail_items(self, state: LabState):
        equipment_level = state.equipment()  # Use the custom equipment() function
        return {
            Item.LaboratoryResearch: 5 + 2 * equipment_level,
            Item.Nightmares: 2
        }

    def pass_rate(self, state: LabState):
        dc = 300 - 10 * state.items.get(Item.UnexpectedResult, 0) - state.preparations()
        return self.broad_pass_rate(dc, state.outfit.watchful)


################################################################################
###                            RunningOutOfSteam                             ###
################################################################################

class RunningOutOfSteam(OpportunityCard):
    def __init__(self):
        super().__init__("Running out of Steam")
        self.actions = [
            GoForAWalk(),
            BrewAnotherPotOfTea(),
            TakeAnExtendedSabbatical()
        ]
        self.weight = 0.2  # Unusual Frequency (20% as common as Standard)
    
    def can_draw(self, state: LabState):
        return state.items.get(Item.LaboratoryResearch, 0) >= 1200 and \
               state.items.get(Item.NoLongerFatigued, 0) == 0

class GoForAWalk(Action):
    def __init__(self):
        super().__init__("Go for a walk")
    
    def pass_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.NoLongerFatigued: 1,
            Item.UnwiseIdea: 1,
            Item.LaboratoryResearch: 18 + 3 * equipment_level
        }

    # TODO
    def rare_success_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.NoLongerFatigued: 1,
            Item.UnlikelyConnection: 5,
            Item.LaboratoryResearch: 5 + 2 * equipment_level
        }

    def fail_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.NoLongerFatigued: 1,
            Item.LaboratoryResearch: 5 + 2 * equipment_level,
            Item.Wounds: -5
        }

    # TODO
    def alternative_fail_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.NoLongerFatigued: 1,
            Item.UnavoidableEpiphany: 1,
            Item.LaboratoryResearch: 5 + 2 * equipment_level
        }

    def pass_rate(self, state: LabState):
        return 0.5  # 50% chance

class BrewAnotherPotOfTea(Action):
    def __init__(self):
        super().__init__("Brew another pot of tea")
    
    def pass_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.NoLongerFatigued: 1,
            Item.ResearchPreparations: 10,
            Item.LaboratoryResearch: 5 + 2 * equipment_level
        }

    def pass_rate(self, state: LabState):
        return 1.0  # Always success

class TakeAnExtendedSabbatical(Action):
    def __init__(self):
        super().__init__("Take an extended sabbatical")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.PalatialHolidayHomeInArcticCircle, 0) > 0

    def pass_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.UnavoidableEpiphany: 1,
            Item.ResearchPreparations: 10,
            Item.Wounds: -2,
            Item.Nightmares: -2,
            Item.NoLongerFatigued: 1,
            Item.LaboratoryResearch: 25 + 2 * equipment_level
        }

    def pass_rate(self, state: LabState):
        return 1.0  # Always success


################################################################################
###                            RunningOutOfTerms                             ###
################################################################################

class RunningOutOfTerms(OpportunityCard):
    def __init__(self):
        super().__init__("Running out of Terms")
        self.actions = [
            PullAnotherAlphabetOffTheShelf(),
            CombineGreekAndLatin()
        ]
        self.weight = 0.2  # Unusual Frequency (20% as common as Standard)
    
    def can_draw(self, state: LabState):
        return state.items.get(Item.LaboratoryResearch, 0) >= 5000 and \
               state.items.get(Item.NoLongerFatigued, 0) > 0 and \
               state.items.get(Item.NumberOfWorkersInYourLaboratory, 0) >= 2

class PullAnotherAlphabetOffTheShelf(Action):
    def __init__(self):
        super().__init__("Pull another alphabet off the shelf")
    
    def pass_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.NoLongerFatigued: 0 - state.items.get(Item.NoLongerFatigued, 0),
            Item.LaboratoryResearch: 8 + equipment_level
        }

    def pass_rate(self, state: LabState):
        return 1.0  # Always success

class CombineGreekAndLatin(Action):
    def __init__(self):
        super().__init__("Combine Greek and Latin")
    
    def pass_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.NoLongerFatigued: 0 - state.items.get(Item.NoLongerFatigued, 0),
            Item.LaboratoryResearch: 18 + 3 * equipment_level,
            Item.Scandal: 1
        }

    def pass_rate(self, state: LabState):
        return 1.0  # Always success

################################################################################
###                            TheIntrusionOfAThought                        ###
################################################################################

class TheIntrusionOfAThought(OpportunityCard):
    def __init__(self):
        super().__init__("The Intrusion of a Thought")
        self.actions = [
            WriteItDownForLater(),
            PerformUnsafeExperiment(),
            PublishUnprovenTheory(),
            PursueUnthinkableInquiry()
        ]
        self.weight = 0.8  # Infrequent Frequency (80% as common as Standard)
    
    def can_draw(self, state: LabState):
        return state.items.get(Item.UnwiseIdea, 0) > 0 and \
               state.items.get(Item.EquipmentForScientificExperimentation, 0) > 0 and \
               state.items.get(Item.ExperimentalObject, 0) > 0

class WriteItDownForLater(Action):
    def __init__(self):
        super().__init__("Write it down for later")
    
    def pass_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.LaboratoryResearch: 8 + equipment_level,
            Item.UnwiseIdea: 1
        }

    def pass_rate(self, state: LabState):
        return 1.0  # Always success

class PerformUnsafeExperiment(Action):
    def __init__(self):
        super().__init__("Perform an unsafe experiment")

    # Defunct quality?
    # def can_perform(self, state: LabState):
    #     return state.items.get(Item.TheoreticalMethods, 0) > 0
    
    def pass_items(self, state: LabState):
        unwise_idea = state.items.get(Item.UnwiseIdea, 1)
        return {
            Item.LaboratoryResearch: 20 * unwise_idea,
            Item.Wounds: unwise_idea,
            Item.UnwiseIdea: 0 - state.items.get(Item.UnwiseIdea, 0)
        }

    def pass_rate(self, state: LabState):
        return 1.0  # Always success

class PublishUnprovenTheory(Action):
    def __init__(self):
        super().__init__("Publish an unproven theory")
    
    def pass_items(self, state: LabState):
        unwise_idea = state.items.get(Item.UnwiseIdea, 1)
        return {
            Item.LaboratoryResearch: 20 * unwise_idea,
            Item.Scandal: unwise_idea,
            Item.UnwiseIdea: 0 - state.items.get(Item.UnwiseIdea, 0)
        }
    
    def pass_rate(self, state: LabState):
        return 1.0  # Always success

class PursueUnthinkableInquiry(Action):
    def __init__(self):
        super().__init__("Pursue an unthinkable line of inquiry")
    
    def pass_items(self, state: LabState):
        unwise_idea = state.items.get(Item.UnwiseIdea, 1)
        return {
            Item.LaboratoryResearch: 20 * unwise_idea,
            Item.Nightmares: unwise_idea,
            Item.UnwiseIdea: 0 - state.items.get(Item.UnwiseIdea, 0)
        }

    def pass_rate(self, state: LabState):
        return 1.0  # Always success

################################################################################
###                                  Eureka                                  ###
################################################################################

class Eureka(OpportunityCard):
    def __init__(self):
        super().__init__("Eureka!")
        self.actions = [ProfoundRealisation()]
        self.weight = 0.8  # Infrequent Frequency (80% as common as Standard)

    def can_draw(self, state: LabState):
        return state.items.get(Item.UnavoidableEpiphany, 0) > 0 and \
               state.items.get(Item.ExperimentalObject, 0) > 0

class ProfoundRealisation(Action):
    def __init__(self):
        super().__init__("Make a profound realisation")
    
    def pass_items(self, state: LabState):
        equipment_level = state.equipment()
        return {
            Item.LaboratoryResearch: 18 + (3 * equipment_level),
            Item.UnavoidableEpiphany: -1  # Consume 1 Unavoidable Epiphany
        }

    def pass_rate(self, state: LabState):
        return 1.0  # Always succeeds

################################################################################
###                   Read the Books that Others Cannot                      ###
################################################################################

class ReadBooksOthersCannot(OpportunityCard):
    def __init__(self):
        super().__init__("Read the Books that Others Cannot")
        self.actions = [DiscoverMandated(), PursueThroughRedScience()]
        self.weight = 0.8  # Infrequent Frequency

    def can_draw(self, state: LabState):
        return state.items.get(Item.PotOfViolantInk, 0) > 0 and \
               state.items.get(Item.ExperimentalObject, 0) > 0

class DiscoverMandated(Action):
    def __init__(self):
        super().__init__("Discover what is mandated")

    def pass_items(self, state: LabState):
        # Using the logistic formula for calculating Laboratory Research
        asotc = state.items.get(Item.ScholarOfTheCorrespondence, 0)
        equipment = state.equipment()
        research_gain = (equipment / 9) * (5 + (35 / (1 + math.exp(-0.5 * (asotc - 12)))))
        return {
            Item.LaboratoryResearch: research_gain,
        }

    # TODO
    def rare_success_items(self, state: LabState):
        research_gain = self.pass_items(state).get(Item.LaboratoryResearch, 0)
        return {
            Item.UnwiseIdea: 1,
            Item.LaboratoryResearch: research_gain
        }

    def fail_items(self, state: LabState):
        research_gain = self.pass_items(state).get(Item.LaboratoryResearch, 0)
        return {
            Item.LaboratoryResearch: research_gain,
            Item.Wounds: 2
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(175 - state.preparations(), state.outfit.watchful)


class PursueThroughRedScience(Action):
    def __init__(self):
        super().__init__("Pursue truths through the Red Science")

    def can_perform(self, state: LabState):
        return state.items.get(Item.ScholarOfTheCorrespondence, 0) >= 5

    def pass_items(self, state: LabState):
        art_red_sci = state.items.get(Item.ArtisanOfTheRedScience, 0)
        research_gain = state.advanced_skill_formula1(art_red_sci)
        return {
            Item.LaboratoryResearch: research_gain
        }

    # TODO
    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: self.pass_items(state).get(Item.LaboratoryResearch, 0),
            Item.AScholarOfTheCorrespondence: 1,
            Item.Wounds: 2.5
        }

    # TODO rare failure, same plus +1 SOTC
    def fail_items(self, state: LabState):
        art_red_sci = state.items.get(Item.ArtisanOfTheRedScience, 0)
        research_gain = state.advanced_skill_formula1(art_red_sci)        
        return {
            Item.LaboratoryResearch: research_gain,
            Item.Wounds: 1
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(5, state.items.get(Item.ArtisanOfTheRedScience, 0))

################################################################################
###                           Involve Your Secret College                    ###
################################################################################

class InvolveSecretCollege(OpportunityCard):
    def __init__(self):
        super().__init__("Involve Your Secret College")
        self.actions = [
            WriteToSecretCollege(),
            BroadenResearch()
        ]
        self.weight = 0.5  # Very Infrequent Frequency

    def can_draw(self, state: LabState):
        return state.items.get(Item.SecretCollege, 0) > 0 and \
               state.items.get(Item.ExperimentalObject, 0) > 0


class WriteToSecretCollege(Action):
    def __init__(self):
        super().__init__("Write to your Secret College for help")

    def pass_items(self, state: LabState):
        # Using the logistic formula for calculating Laboratory Research
        asotc = state.items.get(Item.AScholarOfTheCorrespondence, 0)
        equipment = state.equipment()
        research_gain = (equipment / 9) * (5 + (35 / (1 + math.exp(-0.5 * (asotc - 12)))))
        return {
            Item.LaboratoryResearch: research_gain,
            Item.UnexpectedResult: 1
        }

    # TODO
    def rare_success_items(self, state: LabState):
        research_gain = self.pass_items(state).get(Item.LaboratoryResearch, 0)
        return {
            Item.LaboratoryResearch: research_gain,
            Item.UnwiseIdea: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 8 + state.equipment(),
            Item.Nightmares: 2
        }

    def pass_rate(self, state: LabState):
        rate1 = self.broad_pass_rate(5, state.items.get(Item.ScholarOfTheCorrespondence, 0))
        rate2 = self.broad_pass_rate(175 - state.preparations(), state.outfit.watchful)
        return rate1 * rate2


class BroadenResearch(Action):
    def __init__(self):
        super().__init__("Broaden your research")

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 2 + (2 * state.equipment()),
            Item.UnavoidableEpiphany: 1,
            Item.UnlikelyConnection: 3
        }

    def rare_success_items(self, state: LabState):
        research_gain = state.equipment_formula1()
        return {
            Item.LaboratoryResearch: research_gain,
            Item.UnwiseIdea: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 4 + state.equipment(),
            Item.UnlikelyConnection: 2
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(300 - state.preparations(), state.outfit.watchful)


################################################################################
###                          Invoke the Long-Dead Priests                    ###
################################################################################

class InvokeLongDeadPriests(OpportunityCard):
    def __init__(self):
        super().__init__("Invoke the Long-Dead Priests")
        self.actions = [
            PhobophagicRites()
        ]
        self.weight = 0.8  # Infrequent Frequency

    def can_draw(self, state: LabState):
        return state.items.get(Item.ExperimentalObject, 0) > 0 and \
               state.items.get(Item.Nightmares, 0) >= 2 and \
               state.items.get(Item.LongDeadPriestsOfRedBird, 0) > 0


class PhobophagicRites(Action):
    def __init__(self):
        super().__init__("Phobophagic rites")

    # TODO might require special outfit
    def pass_items(self, state: LabState):
        glasswork = state.outfit.glasswork
        research_gain = state.advanced_skill_formula1(glasswork)
        return {
            Item.LaboratoryResearch: research_gain,
            Item.Nightmares: -state.items.get(Item.Nightmares, 0)  # Clears Nightmares
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 15,  # Flat amount for failure
            Item.Nightmares: 2
        }

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(145 - state.preparations(), state.outfit.watchful)

################################################################################
###                          Genericman1 (FATE)                             ###
################################################################################

class GenericMan1Card(OpportunityCard):
    def __init__(self):
        super().__init__("Genericman1.png (FATE)")
        self.actions = [
            GenericMan1Resupply(),
            GenericMan1Discard()
        ]
        self.weight = 0.2  # Unusual Frequency

    def can_draw(self, state: LabState):
        return state.items.get(Item.NumberOfWorkersInYourLaboratory, 0) >= 4


class GenericMan1Resupply(Action):
    def __init__(self):
        super().__init__("Candle.png")

    # TODO: does this check resupply quality?

    def pass_items(self, state: LabState):
        equipment_level = state.equipment()
        research_gain = 5 * equipment_level
        return {
            Item.NoLongerResupplying: 1,
            Item.LaboratoryResearch: research_gain,
        }

class GenericMan1Discard(Action):
    def __init__(self):
        super().__init__("University.png")

    def pass_items(self, state: LabState):
        equipment_level = state.equipment()
        research_gain = 5 * equipment_level
        return {
            Item.LaboratoryResearch: research_gain,
            Item._HandClear: 1
        }

    def perform_pass(self, state: LabState):
        """Custom implementation to also discard hand on pass."""
        super().perform_pass(state)
        state.clear_hand()


################################################################################
###                      Rely on Lettice, the Mercy                          ###
################################################################################

class RelyOnLettice(OpportunityCard):
    def __init__(self):
        super().__init__("Rely on Lettice, the Mercy")
        self.actions = [
            AskTombColonist(),
            HelpWithResearch(),
            TakeTea(),
            SuperviseGiftedStudent(),
            ApplyExpertise()
        ]
        self.weight = 1.0  # Standard Frequency

    def can_draw(self, state: LabState):
        return state.items.get(Item.LaboratoryServicesOfLetticeTheMercy, 0) > 0


class AskTombColonist(Action):
    def __init__(self):
        super().__init__("Ask her what a Tomb Colonist would say about this")

    def can_perform(self, state: LabState):
        return 110 <= state.items.get(Item.ExperimentalObject, 0) <= 120 or \
               state.items.get(Item.ExperimentalObject, 0) == 1320

    def pass_items(self, state: LabState):
        return {
            Item.ExpertiseOfTheThirdCity: 10
        }


class HelpWithResearch(Action):
    def __init__(self):
        super().__init__("Ask her to help with ordinary research")

    def can_perform(self, state: LabState):
        return state.items.get(Item.ExperimentalObject, 0) > 0 and \
               state.items.get(Item.EquipmentForScientificExperimentation, 0) >= 5

    def pass_items(self, state: LabState):
        return {
            # TODO very high variance, nonlinear EV?
            Item.UnwiseIdea: 0.5,
            Item.LaboratoryResearch: 22.5
        }


class TakeTea(Action):
    def __init__(self):
        super().__init__("Take tea with Lettice")

    def pass_items(self, state: LabState):
        return {
            Item.Wounds: -2,
            Item.Nightmares: -2
        }


class SuperviseGiftedStudent(Action):
    def __init__(self):
        super().__init__("Have her supervise the Gifted Student")

    def can_perform(self, state: LabState):
        return state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0) >= 5 and \
               401 <= state.items.get(Item.ExperimentalObject, 0) <= 500

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(220, state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 12 + 2 * state.equipment(),
            Item.UnexpectedResult: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 5 + 2 * state.equipment()
        }


class ApplyExpertise(Action):
    def __init__(self):
        super().__init__("Apply her particular expertise in a novel way")

    def can_perform(self, state: LabState):
        return state.items.get(Item.UnlikelyConnection, 0) > 0

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(220 - state.preparations(), state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: 7 + 2 * state.equipment(),
            Item.UnexpectedResult: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: 5 + 2 * state.equipment()
        }


################################################################################
###                            Rely on the Silk-Clad Expert                  ###
################################################################################

class RelyOnSilkCladExpert(OpportunityCard):
    def __init__(self):
        super().__init__("Ask the Silk-Clad Expert")
        self.actions = [
            SilkCladExpert1(),
            SilkCladExpert2(),
            SilkCladExpert3(),
            SilkCladExpert4()
        ]
        self.weight = 1.0  # Standard Frequency

    def can_draw(self, state: LabState):
        return state.items.get(Item.ExperimentalObject, 0) > 100


class SilkCladExpert1(Action):
    def __init__(self):
        super().__init__("Ask for research (101-400)")

    def can_perform(self, state: LabState):
        return 101 <= state.items.get(Item.ExperimentalObject, 0) <= 400 or \
               state.items.get(Item.ExperimentalObject, 0) >= 501

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 5/3 * state.equipment()
        }

class SilkCladExpert2(Action):
    def __init__(self):
        super().__init__("Ask for research (Unlikely Connection)")

    def can_perform(self, state: LabState):
        return state.items.get(Item.UnlikelyConnection, 0) > 0 and \
               (101 <= state.items.get(Item.ExperimentalObject, 0) <= 400 or \
               state.items.get(Item.ExperimentalObject, 0) >= 501)

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(220 - state.preparations(), state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: 7 + 2 * state.equipment(),
            Item.UnexpectedResult: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: 5 + 2 * state.equipment()
        }

class SilkCladExpert3(Action):
    def __init__(self):
        super().__init__("Ask for research (401-500)")

    def can_perform(self, state: LabState):
        return 401 <= state.items.get(Item.ExperimentalObject, 0) <= 500

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 8 + 1.5 * state.equipment(),
            Item.UnavoidableEpiphany: 1
        }

class SilkCladExpert4(Action):
    def __init__(self):
        super().__init__("Ask for Parabolan research")

    def pass_items(self, state: LabState):
        return {
            Item.ParabolanResearch: 5,
            Item.LaboratoryResearch: 5/3 * state.equipment()
        }


################################################################################
###                            WorkWithYourGiftedStudent                     ###
################################################################################

class WorkWithYourGiftedStudent(OpportunityCard):
    def __init__(self):
        super().__init__("Work with your Gifted Student")
        self.actions = [
            ShepherdThroughResearch(),
            CollaborateWithStudent(),
            WorkWithExpertStudent(),
            FollowUpHunch(),
            PairWithSilkCladExpert()
        ]
        self.weight = 1.0  # Standard Frequency

    def can_draw(self, state: LabState):
        return state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0) > 0

class ShepherdThroughResearch(Action):
    def __init__(self):
        super().__init__("Shepherd your student through some research")
    
    def can_perform(self, state: LabState):
        return 1 <= state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0) <= 2

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(210 - state.preparations(), state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 2 + state.equipment()
        }

    # TODO yeah definitely need to model this somehow
    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 3 + 5/3 * state.equipment(),
            Item.LaboratoryServicesFromGiftedStudent: min(1, 5 - state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0))
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 2 + state.equipment()
        }

class CollaborateWithStudent(Action):
    def __init__(self):
        super().__init__("Collaborate with your student")

    def can_perform(self, state: LabState):
        return 3 <= state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0) <= 4
    
    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(215 - state.preparations(), state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: math.ceil(3 + 5/3 * state.equipment())
        }

    # TODO
    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: math.ceil(3 + 5/3 * state.equipment()),
            Item.LaboratoryServicesFromGiftedStudent: min(1, 5 - state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0))
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: math.ceil(2 + state.equipment())
        }

class WorkWithExpertStudent(Action):
    def __init__(self):
        super().__init__("Work with your expert student")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0) >= 5
    
    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(220 - state.preparations(), state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 5 + 2 * state.equipment(),
            Item.UnlikelyConnection: 1
        }

    # TODO
    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 10 + 2 * state.equipment(),
            Item.UnlikelyConnection: 1,
            Item.DisgruntlementAmongTheStudents: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: math.ceil(3 + 5/3 * state.equipment())
        }

class FollowUpHunch(Action):
    def __init__(self):
        super().__init__("Follow up a hunch with your student")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.UnavoidableEpiphany, 0) >= 1 and \
               state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0) >= 5

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(220 - state.preparations(), state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.UnavoidableEpiphany: -1,
            Item.LaboratoryResearch: 18 + 3 * state.equipment()
        }

    # TODO
    def rare_success_items(self, state: LabState):
        return {
            Item.UnavoidableEpiphany: -1,
            Item.LaboratoryResearch: 18 + 3 * state.equipment(),
            Item.UnexpectedResult: 1,
            Item.DisgruntlementAmongTheStudents: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 8 + 2 * state.equipment()
        }

class PairWithSilkCladExpert(Action):
    def __init__(self):
        super().__init__("Pair her with the Silk-Clad Expert")
    
    def can_perform(self, state: LabState):
        return state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0) < 5 and \
               state.items.get(Item.ExperimentalObject, 0) in range(401, 501) and \
               state.items.get(Item.LaboratoryServicesOfSilkCladExpert, 0) >= 1

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(180, state.outfit.persuasive)

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 12 + state.equipment(),
            Item.LaboratoryServicesFromGiftedStudent: min(1, 5 - state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0))
        }

    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 12 + 2 * state.equipment(),
            Item.UnexpectedResult: 1,
            Item.UnlikelyConnection: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 15 if state.equipment() == 7 else 18
        }


################################################################################
###                           WorkWithYourVisionaryStudent                   ###
################################################################################

class WorkWithYourVisionaryStudent(OpportunityCard):
    def __init__(self):
        super().__init__("Work with your Visionary Student")
        self.actions = [
            ShepherdThroughVisionaryResearch(),
            CollaborateWithVisionaryStudent(),
            WorkWithExpertVisionaryStudent(),
            LeaveVisionaryStudent(),
            FollowUpVisionaryHunch(),
            # TutorOtherStudents()
        ]
        self.weight = 1.0  # Standard Frequency

    def can_draw(self, state: LabState):
        return state.items.get(Item.LaboratoryServicesFromVisionaryStudent, 0) > 0

class ShepherdThroughVisionaryResearch(Action):
    def __init__(self):
        super().__init__("Shepherd your student through some research")

    def can_perform(self, state: LabState):
        return 1 <= state.items.get(Item.LaboratoryServicesFromVisionaryStudent, 0) <= 2

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(210 - state.preparations(), state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 4 + state.equipment()
        }

    # TODO
    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 4 + state.equipment(),
            Item.LaboratoryServicesFromVisionaryStudent: min(state.items.get(Item.LaboratoryServicesFromVisionaryStudent, 0) + 1, 5)
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 3 + state.equipment()
        }

class CollaborateWithVisionaryStudent(Action):
    def __init__(self):
        super().__init__("Collaborate with your student")

    def can_perform(self, state: LabState):
        return 3 <= state.items.get(Item.LaboratoryServicesFromVisionaryStudent, 0) <= 4

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(215 - state.preparations(), state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: math.floor(7 + 5/3 * state.equipment())
        }

    # TODO
    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: math.floor(8 + 5/3 * state.equipment()),
            Item.LaboratoryServicesFromVisionaryStudent: min(state.items.get(Item.LaboratoryServicesFromVisionaryStudent, 0) + 1, 5)
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: math.floor(6 + 5/3 * state.equipment())
        }

class WorkWithExpertVisionaryStudent(Action):
    def __init__(self):
        super().__init__("Work with your expert student")

    def can_perform(self, state: LabState):
        return state.items.get(Item.LaboratoryServicesFromVisionaryStudent, 0) == 5

    def pass_rate(self, state: LabState):
        return self.broad_pass_rate(220 - state.preparations(), state.outfit.watchful)

    def pass_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 9 + 2 * state.equipment()
        }

    def rare_success_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 10 + 2 * state.equipment(),
            Item.DisgruntlementAmongTheStudents: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 6.5 + 1.6 * state.equipment()
        }

class LeaveVisionaryStudent(Action):
    def __init__(self):
        super().__init__("Leave your student to their own devices")

    def can_perform(self, state: LabState):
        return state.items.get(Item.LaboratoryServicesFromVisionaryStudent, 0) == 5

    def pass_rate(self, state: LabState):
        return 0.5  # 50% chance

    def pass_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        return {
            Item.UnlikelyConnection: 1,
            Item.LaboratoryResearch: (2 + 0.2 * state.equipment()) * math.sqrt(num_workers) * state.highest_worker_level()
        }

    # TODO
    def rare_success_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        return {
            Item.UnwiseIdea: 1,
            Item.LaboratoryResearch: (2 + 0.2 * state.equipment()) * math.sqrt(num_workers) * state.highest_worker_level()
        }

    def fail_items(self, state: LabState):
        num_workers = state.items.get(Item.NumberOfWorkersInYourLaboratory, 1)
        return {
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: (2 + 0.2 * state.equipment()) * math.sqrt(num_workers) * state.highest_worker_level()
        }

class FollowUpVisionaryHunch(Action):
    def __init__(self):
        super().__init__("Follow up a hunch with your student")

    def can_perform(self, state: LabState):
        return state.items.get(Item.UnavoidableEpiphany, 0) >= 1 and \
               state.items.get(Item.LaboratoryServicesFromVisionaryStudent, 0) == 5

    def pass_items(self, state: LabState):
        return {
            Item.UnavoidableEpiphany: -1,
            Item.LaboratoryResearch: 18 + 3 * state.equipment()
        }

    def rare_success_items(self, state: LabState):
        return {
            Item.UnavoidableEpiphany: -1,
            Item.LaboratoryResearch: 18 + 3 * state.equipment(),
            Item.UnwiseIdea: 1,
            Item.DisgruntlementAmongTheStudents: 1
        }

    def fail_items(self, state: LabState):
        return {
            Item.LaboratoryResearch: 8 + 2 * state.equipment()
        }

# # TODO
# class TutorOtherStudents(Action):
#     def __init__(self):
#         super().__init__("Let them tutor your other students")

#     def can_perform(self, state: LabState):
#         return state.items.get(Item.LaboratoryServicesFromVisionaryStudent, 0) == 5 and \
#                (state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0) > 0 or
#                 state.items.get(Item.LaboratoryServicesFromShiftyStudent, 0) > 0 or
#                 state.items.get(Item.LaboratoryServicesFromProfoundStudent, 0) > 0 or
#                 state.items.get(Item.LaboratoryServicesFromMeticulousStudent, 0) > 0)

#     def pass_items(self, state: LabState):
#         return {
#             Item.LaboratoryServicesFromGiftedStudent: min(state.items.get(Item.LaboratoryServicesFromGiftedStudent, 0) + 1, 5),
#             Item.LaboratoryServicesFromShiftyStudent: min(state.items.get(Item.LaboratoryServicesFromShiftyStudent, 0) + 1, 5),
#             Item.LaboratoryServicesFromProfoundStudent: min(state.items.get(Item.LaboratoryServicesFromProfoundStudent, 0) + 1, 5),
#             Item.LaboratoryServicesFromMeticulousStudent: min(state.items.get(Item.LaboratoryServicesFromMeticulousStudent, 0) + 1, 5),
#             Item.LaboratoryResearch: 8 + 2 * state.equipment()
#         }

#     def fail_items(self, state: LabState):
#         return {
#             Item.LaboratoryResearch: 8 + 2 * state.equipment(),
#             Item.DisgruntlementAmongTheStudents: 1
#         }

# Update progress bar function
def update_progress(progress):
    bar_length = 40
    block = int(round(bar_length * progress))
    text = f"\rProgress: [{'#' * block + '-' * (bar_length - block)}] {progress * 100:.2f}%"
    sys.stdout.write(text)
    sys.stdout.flush()

results = []

for i in range(0, 100):
    state = LabState()
    state.run()
    results.append(state.actions)
    update_progress(i / 100)

print()
print(results)
print(sum(results)/100)
