import random
import sys
import math
from collections import defaultdict
from enum import Enum, auto

from enums import *
from simulations.models import *
from simulations.models import GameState

class LabState(GameState):
    def __init__(self):
        self.outfit = OutfitList(300, 18)

        self.items = {
            Item.TotalLabReserchRequired: 250,
            Item.EquipmentForScientificExperimentation: 9,
            Item.PrestigeOfYourLaboratory: 100,
            Item.NumberOfWorkersInYourLaboratory: 4
        }

        self.deck = [
            PreparingForBriefExperiment(),
            FormNewHypotheses()
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
        if equipment == 4:
            return 9
        else:
            return 4 * equipment - 8
        

    def advanced_skill_formula1(self):
        # TODO
        return 34

    def advanced_skill_formula2(self):
        # TODO
        return 15

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
            state.items.get(Item.NoLongerFormingHypotheses, 0) == 0 and
            state.items.get(Item.NoLongerResupplying, 0) == 0
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
            Item.NoLongerResupplying: 0 - state.items.get(Item.NoLongerResupplying),
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
            Item.NoLongerResupplying: 0 - state.items.get(Item.NoLongerResupplying),
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
        return {
            Item.UnlikelyConnection: -1,
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: state.advanced_skill_formula1()
        }

    def fail_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: state.advanced_skill_formula2(),
            Item.Wounds: 1
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(7, state.outfit.artisan_of_the_red_science)

class ExperimentInParabola(Action):
    def __init__(self):
        super().__init__("Perform an experiment in Parabola")
    
    def pass_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: state.advanced_skill_formula1()
        }

    def fail_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: state.advanced_skill_formula2(),
            Item.Nightmares: 1
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(7, state.outfit.glasswork)

class RearrangeBrain(Action):
    def __init__(self):
        super().__init__("Rearrange your brain around the problem")
    
    def pass_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: state.advanced_skill_formula1()
        }

    def fail_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: state.advanced_skill_formula2(),
            Item.Nightmares: 1
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(7, state.outfit.shapeling_arts)

class AdoptBetterFrameOfMind(Action):
    def __init__(self):
        super().__init__("Adopt a better frame of mind")

    def pass_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.UnexpectedResult: 1,
            Item.LaboratoryResearch: state.advanced_skill_formula1()
        }

    def fail_items(self, state: LabState):
        return {
            Item.UnlikelyConnection: -1,
            Item.LaboratoryResearch: state.advanced_skill_formula2(),
            Item.Wounds: 1
        }

    def pass_rate(self, state: LabState):
        return self.narrow_pass_rate(7, state.outfit.watchful)

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
