"""
Burgundy Simulation

This module simulates exploration of the Burgundy location in Fallen London,
focusing on optimizing resource gathering through a finite deck of cards.

Key Features:
- Finite draw opportunities (cards are reshuffled but draws are limited)
- Economic optimization of card plays and draws
- Multiple card types with different actions
- State tracking for resources and draw opportunities

TODO 
- Knight of the golden carapace card + hand size
"""

import math
from collections import defaultdict
from enum import Enum, auto
import helper.utils as utils
from enums import *
from simulations.item_conversions import conversion_rate
from simulations.models import *
from simulations.models import GameState

class BurgundyState(GameState):
    """State management for Burgundy exploration."""
    def __init__(self):
        super().__init__(max_hand_size=5)
        self.status = "InProgress"
        self.skip_econ_inputs = False
        self.ev_threshold = 6.0

    def aiding_feast(self):
        return self.get(Item.PreparationsForASaintsDay) in (10, 11, 12, 13, 14)
    
    def feast_ready(self):
        return self.get(Item.PreparationsForASaintsDay) == 15

    def aiding_march(self):
        return self.get(Item.PreparationsForASaintsDay) in (20, 21, 22, 23, 24)

    def march_ready(self):
        return self.get(Item.PreparationsForASaintsDay) == 25

    def ev_from_item(self, item, val: int):
        """Calculate expected value for an item."""
        if item == Item.BurgundyResource:  # Replace with actual resource
            return self.ev_burgundy(val)
        else:
            return val * conversion_rate(item, Item.Echo)

    def ev_burgundy(self, val: int) -> float:
        """Calculate expected value for Burgundy-specific resource."""
        # Implement resource-specific EV calculation
        pass

    def ev_draw(self) -> float:
        """Calculate expected value of drawing a card."""
        # This should consider:
        # 1. The cost of drawing (actions/resources)
        # 2. The expected value of cards in the deck
        # 3. The current state of the game
        pass

    def run(self):
        """Run the simulation until completion."""
        while self.status == "InProgress":
            self.step()

    def step(self):
        """Execute one step of the simulation."""
        best_card, best_action = self.best_action_by_simple_ranking()

        if best_action is None:
            # Log state when no actions available
            print("Cards in hand: " + str(len(self.hand)))
            for card in self.hand:
                print(card.name)

        if best_action:
            result = best_action.perform(self)
            self.actions += best_action.action_cost
            self.action_result_counts[best_action][result] += 1

        if best_card is not None:
            self.card_play_counts[best_card] += 1
            if best_card in self.hand:
                self.hand.remove(best_card)

        self.hand = [card for card in self.hand if card.can_draw(self)]

    def best_action_by_simple_ranking(self):
        """Determine the best action based on economic optimization."""
        
        bb = self.get(Item.BurgundianBeneficence)
        atak = self.get(Item.AgainstTimeAndKings)
        hunt = self.get(Item.SeasonOfHunting)

        # Define action priority list based on current state
        action_list = []

        if len(self.hand) == 0:
            action_list.append(Deck_RefillHand)
        
        # BB and ATAK cashouts
        action_list.extend({
            GiftsOfBurgundy_PlunderHistory,
            SpoilsOfRebellion_SparkingAnachronism
        })

        # Feast carousel
        action_list.extend({
            MarchForThePeople_AttendPilgrimage,
            InAidOfAFeast_AttendFeast,

            PreparationsForASaintsDay_FomentUnrest,
            SpreadingSeditionTwistedPilgrimage_TweakRoute,
            SpreadingSeditionHeartsAndMinds_BendEars,

            PreparationsForASaintsDay_PledgeFeast,
            AidingFeastHeartsAndStomachs_TestSupplies,
            AidingFeastChurchAndState_ExposePriest
        })

        # Chevalier carousel
        action_list.extend({
            HuntingTheRoofPrey_GoForGlory,
            InvitationFromTheSwashbucklingChevalier_AttendRevels,
            WhosoListToHunt_ChooseSteedAndWeapon,
        })

        # cash out other
        action_list.extend({
            TollingOfTheThiefBells_StealGravensteen,
            AllAroundTheCountsRock_SeduceMasquer,
            CutthroatsAndCanalmen_ForayBeyond
        })

        bb_gains = [
            # StrangerOut
            StrangerOutOfTime_AcquireHelp,
            VineStrangledAisles_SavePriest,
            HonoursOfTheCourt_RescueReichsgraf,
            WarrensOfWorship_LightCandles
        ]

        atak_gains = [
            TintOfUnworthiness_CarrySupplies,
            TollingOfTheThiefBells_InspectPatrols,
            BurgundyOfBlood_PermitAnarchists,
            BeneathTheGiltExterior_DisseminatePamphlets,
            EchoesOfStormsPast_ReportPatterns
        ]

        if atak >= 5:
            action_list.extend(atak_gains)
            if bb < 4:
                action_list.extend(bb_gains)
        elif bb >= 5:
            action_list.extend(bb_gains)
            if atak < 4:
                action_list.extend(atak_gains)
        else:
            action_list.extend(atak_gains)
            action_list.extend(bb_gains)

        action_list.append(Deck_RefillHand)

        # Find the best available action
        for ranked_action in action_list:
            for storylet in self.storylets:
                for action in storylet.actions:
                    if isinstance(action, ranked_action) and action.can_perform(self):
                        return (storylet, action)
            for card in self.hand:
                for card_action in card.actions:
                    if isinstance(card_action, ranked_action) and card_action.can_perform(self):
                        return (card, card_action)

        return (None, None)

################################################################
#                     Base Storylet
################################################################

class StoryletBurgundy(OpportunityCard):
    """Base storylet for Burgundy location."""
    def __init__(self):
        super().__init__("Storylet: Burgundy")
        self.actions = [
            Deck_RefillHand(),
        ]

class Deck_RefillHand(Action):
    """Action to refill the player's hand."""
    def __init__(self):
        super().__init__("(REFILL HAND)")

    def can_perform(self, state: BurgundyState):
        return len(state.hand) < state.max_hand_size
    
    def perform(self, state: BurgundyState):
        while len(state.hand) < state.max_hand_size:
            state.draw_card()
        return ActionResult.Pass

################################################################
#                     Opportunity Cards
################################################################

################################################################
#                     A Gloomy Summer
################################################################

class GloomySummer(OpportunityCard):
    """A Gloomy Summer card."""
    def __init__(self):
        super().__init__("A Gloomy Summer")
        self.weight = 0.5
        self.free_discard = False
        self.actions = [
            GloomySummer_Convince(),
            GloomySummer_WorkInSecret(),
            GloomySummer_FundActivities()
        ]

    # TODO: Can you draw this while feast = exactly 15?
    def can_draw(self, state: BurgundyState):
        return state.aiding_feast() and state.get(Item.SaintsDayConflictsResolved) == 0

class GloomySummer_Convince(Action):
    def __init__(self):
        super().__init__("Convince her of the harmlessness of the cause")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.SecludedAddress: 6,
            Item.Scandal: 1
        }

class GloomySummer_WorkInSecret(Action):
    def __init__(self):
        super().__init__("Go about your work in secret")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.JournalOfInfamy: 6,
            Item.Suspicion: 1
        }

class GloomySummer_FundActivities(Action):
    def __init__(self):
        super().__init__("Fund her own activities")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.BlackmailMaterial) >= 1 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.BlackmailMaterial: -1,
            Item.ScrapOfIncendiaryGossip: 7,
            Item.SaintsDayConflictsResolved: 1,
            Item.AgainstTimeAndKings: 1
            # TODO: airs change
        }

################################################################
#                     A March for the People
################################################################

class MarchForThePeople(OpportunityCard):
    """A March for the People card."""
    def __init__(self):
        super().__init__("A March for the People")
        self.actions = [
            MarchForThePeople_AttendPilgrimage()
        ]

    def can_draw(self, state: BurgundyState):
        return state.get(Item.PreparationsForASaintsDay) == 25
    
class MarchForThePeople_AttendPilgrimage(Action):
    def __init__(self):
        super().__init__("Attend the pilgrimage")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.CausticApocryphon: 4,
            Item.PreparationsForASaintsDay: -state.get(Item.PreparationsForASaintsDay)
        }

################################################################
#                     A Stranger Out of Time
################################################################

class StrangerOutOfTime(OpportunityCard):
    """A Stranger Out of Time card."""
    def __init__(self):
        super().__init__("A Stranger Out of Time")
        self.weight = 2.0
        self.free_discard = False
        self.actions = [
            StrangerOutOfTime_SoldierOn(),
            StrangerOutOfTime_AcquireHelp(),
            StrangerOutOfTime_Recontextualise()
        ]

    def can_draw(self, state: BurgundyState):
        return state.get(Item.Scandal) >= 15

class StrangerOutOfTime_SoldierOn(Action):
    def __init__(self):
        super().__init__("Soldier on")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.Scandal: 2
            # TODO: airs change
        }

class StrangerOutOfTime_AcquireHelp(Action):
    def __init__(self):
        super().__init__("Acquire the help of a Master of Etiquette")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.Stuiver) >= 20 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.Stuiver: -20,
            Item.Scandal: -2,
            Item.BurgundianBeneficence: 1
            # TODO: airs change
        }

class StrangerOutOfTime_Recontextualise(Action):
    def __init__(self):
        super().__init__("Recontextualise your behaviour")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.VolumeOfCollatedResearch) >= 1 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.VolumeOfCollatedResearch: -1,
            Item.ScrapOfIncendiaryGossip: 1,
            Item.Scandal: -5
            # TODO: airs change
        }

################################################################
#                     Aiding a Feast: Church and State
################################################################

class AidingFeastChurchAndState(OpportunityCard):
    """Aiding a Feast: Church and State card."""
    def __init__(self):
        super().__init__("Aiding a Feast: Church and State")
        self.actions = [
            AidingFeastChurchAndState_HighlightVerses(),
            AidingFeastChurchAndState_ExposePriest()
        ]

    def can_draw(self, state: BurgundyState):
        return state.aiding_feast()

class AidingFeastChurchAndState_HighlightVerses(Action):
    def __init__(self):
        super().__init__("Highlight a few appropriate verses")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.PalimpsestScrap) >= 5 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.PalimpsestScrap: -5,
            Item.PreparationsForASaintsDay: 1
        }

class AidingFeastChurchAndState_ExposePriest(Action):
    def __init__(self):
        super().__init__("Expose an partisan priest")

    def can_perform(self, state: BurgundyState):
        return True
    
    def pass_rate(self, state: BurgundyState):
        return self.narrow_pass_rate(10, state.outfit.player_of_chess)
    
    def pass_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 1
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 1,
            Item.Scandal: 2
        }

################################################################
#                     Aiding a Feast: Hearts and Stomachs
################################################################

class AidingFeastHeartsAndStomachs(OpportunityCard):
    """Aiding a Feast: Hearts and Stomachs card."""
    def __init__(self):
        super().__init__("Aiding a Feast: Hearts and Stomachs")
        self.actions = [
            AidingFeastHeartsAndStomachs_SupplyVenison(),
            AidingFeastHeartsAndStomachs_TestSupplies()
        ]

    def can_draw(self, state: BurgundyState):
        return state.aiding_feast()        

class AidingFeastHeartsAndStomachs_SupplyVenison(Action):
    def __init__(self):
        super().__init__("Supply the revels with Venison Marrow")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.PotOfVenisonMarrow) >= 5 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.PotOfVenisonMarrow: -5,
            Item.PreparationsForASaintsDay: 1
        }

class AidingFeastHeartsAndStomachs_TestSupplies(Action):
    def __init__(self):
        super().__init__("Test supplies for poisons")

    def can_perform(self, state: BurgundyState):
        return True
    
    def pass_rate(self, state: BurgundyState):
        return self.narrow_pass_rate(10, state.outfit.kataleptic_toxicology)

    def pass_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 1
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 1,
            Item.Wounds: 3
        }

################################################################
#                     All Around the Count's Rock
################################################################

class AllAroundTheCountsRock(OpportunityCard):
    """All Around the Count's Rock card."""
    def __init__(self):
        super().__init__("All Around the Count's Rock")
        self.actions = [
            AllAroundTheCountsRock_CharmWithoutCrown(),
            AllAroundTheCountsRock_CharmWithCrown(),
            AllAroundTheCountsRock_ClimbParapet(),
            AllAroundTheCountsRock_CaseKeep(),
            AllAroundTheCountsRock_SeduceMasquer()
        ]

class AllAroundTheCountsRock_CharmWithoutCrown(Action):
    def __init__(self):
        super().__init__("Charm your way into a feast (without a Newly-Cast Crown)")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.NewlyCastCrownOfTheCityOfLondon) == 0

    def pass_rate(self, state: BurgundyState):
        score = state.outfit.persuasive + state.outfit.mithridacy * 15
        return self.broad_pass_rate(200, score)

    def pass_items(self, state: BurgundyState):
        return {
            Item.Persuasive: 1,
            Item.ScrapOfIncendiaryGossip: 8
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Scandal: 3
        }

class AllAroundTheCountsRock_CharmWithCrown(Action):
    def __init__(self):
        super().__init__("Charm your way into a feast (with a Newly-Cast Crown)")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.NewlyCastCrownOfTheCityOfLondon) >= 1

    def pass_items(self, state: BurgundyState):
        return {
            Item.ScrapOfIncendiaryGossip: 10
        }

class AllAroundTheCountsRock_ClimbParapet(Action):
    def __init__(self):
        super().__init__("Climb to the tallest parapet")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        score = state.outfit.watchful + state.outfit.insubstantial * 15
        return self.broad_pass_rate(200, score)

    def pass_items(self, state: BurgundyState):
        return {
            Item.AeolianScream: 1,
            Item.MemoryOfLight: 2,
            Item.AsAboveBecomesBelow: 2
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.TaleOfTerror: 3,
            Item.Suspicion: 1,
            Item.Wounds: 1
        }

class AllAroundTheCountsRock_CaseKeep(Action):
    def __init__(self):
        super().__init__("Case a lesser keep")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.Casing: 6,
            Item.CrypticClue: 50
        }

class AllAroundTheCountsRock_SeduceMasquer(Action):
    def __init__(self):
        super().__init__("Seduce an Alluring Masquer")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.Fascinating) >= 36 # or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.CellarOfWine: 1,
            Item.FavourInHighPlaces: 2,
            Item.RomanticNotion: 10,
            Item.Fascinating: -36
        }

################################################################
#                     An Encounter with the Poet-Thief
################################################################

class EncounterWithThePoetThief(OpportunityCard):
    """An Encounter with the Poet-Thief card."""
    def __init__(self):
        super().__init__("An Encounter with the Poet-Thief")
        self.free_discard = False
        self.actions = [
            EncounterWithThePoetThief_ConcludeBusiness()
        ]

    def can_draw(self, state: BurgundyState):
        return state.get(Item.SaddledWithAStolenSack) >= 1

class EncounterWithThePoetThief_ConcludeBusiness(Action):
    def __init__(self):
        super().__init__("Conclude your business (Poet-Thief)")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.SaddledWithAStolenSack) >= 1

    def pass_items(self, state: BurgundyState):
        return {
            Item.MagnificentDiamond: 1,
            Item.OstentatiousDiamond: 3,
            Item.ScrapOfIncendiaryGossip: 8,
            Item.SaddledWithAStolenSack: -1  # Removes the quality
        }

################################################################
#                     An Invitation from the Swashbuckling Chevalier
################################################################

class InvitationFromTheSwashbucklingChevalier(OpportunityCard):
    """An Invitation from the Swashbuckling Chevalier card."""
    def __init__(self):
        super().__init__("An Invitation from the Swashbuckling Chevalier")
        self.weight = 1_000_000 # HACK for urgent freq
        # self.urgency = 1 # TODO
        self.actions = [
            InvitationFromTheSwashbucklingChevalier_AttendRevels()
        ]

    def can_draw(self, state: BurgundyState):
        return state.get(Item.SeasonOfHunting) == 1

class InvitationFromTheSwashbucklingChevalier_AttendRevels(Action):
    def __init__(self):
        super().__init__("Attend the revels")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.MemoryOfAMuchStrangerSelf: 2,
            Item.CaveAgedCodeOfHonour: 2,
            # Item.MountedUpon: -1,  # Removes the quality
            # Item.ArmedWith: -1,    # Removes the quality
            Item.SeasonOfHunting: -state.get(Item.SeasonOfHunting)
        }

################################################################
#                     Beneath the Gilt Exterior
################################################################

class BeneathTheGiltExterior(OpportunityCard):
    """Beneath the Gilt Exterior card."""
    def __init__(self):
        super().__init__("Beneath the Gilt Exterior")
        self.actions = [
            BeneathTheGiltExterior_DisseminatePamphlets(),
            BeneathTheGiltExterior_GiveAlms(),
            BeneathTheGiltExterior_OfferElbowGrease()
        ]

class BeneathTheGiltExterior_DisseminatePamphlets(Action):
    def __init__(self):
        super().__init__("Disseminate pamphlets")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.Suspicion: 1,  # TODO Random 0-2 CP
            Item.AgainstTimeAndKings: 1
        }

class BeneathTheGiltExterior_GiveAlms(Action):
    def __init__(self):
        super().__init__("Give alms")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.Stuiver) >= 10 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.Stuiver: -10,
            Item.StolenKiss: 1,
            Item.DubiousTestimony: 3,
            Item.Nightmares: 1,
            # Item.AdriftOnASeaOfMisery: 1,
            Item.NotesOnAJoyousEntry: 2
        }

class BeneathTheGiltExterior_OfferElbowGrease(Action):
    def __init__(self):
        super().__init__("Offer your elbow-grease to dissidents")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.StrongBackedLabour) >= 3 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.StrongBackedLabour: -3,
            Item.CausticApocryphon: 1
        }

################################################################
#                     Cardinal Disagreements
################################################################

class CardinalDisagreements(OpportunityCard):
    """Cardinal Disagreements card."""
    def __init__(self):
        super().__init__("Cardinal Disagreements")
        self.actions = [
            CardinalDisagreements_StudyLight(),
            CardinalDisagreements_ProbeGravity(),
            CardinalDisagreements_FocusWeight(),
            CardinalDisagreements_PressPalms(),
        ]

class CardinalDisagreements_StudyLight(Action):
    def __init__(self):
        super().__init__("Study the light")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.MemoryOfLight: 8,
            Item.AsAboveBecomesBelow: 2
            # TODO: airs change
        }

class CardinalDisagreements_ProbeGravity(Action):
    def __init__(self):
        super().__init__("Probe the local gravity")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.AsAboveBecomesBelow) >= 15

    def pass_items(self, state: BurgundyState):
        return {
            Item.ShardOfGlim: 450,
            Item.AsAboveBecomesBelow: 2
            # TODO: airs change
        }

class CardinalDisagreements_FocusWeight(Action):
    def __init__(self):
        super().__init__("Focus on the weight in your heart")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.StoneHearted) >= 6 \
            and state.get(Item.AsAboveBecomesBelow) >= 28

    def pass_items(self, state: BurgundyState):
        return {
            Item.StoneHearted: -5,
            Item.MemoryOfMoonlight: 1,
            Item.StolenKiss: 1,
            Item.SampleOfRoofDrip: 50,
            Item.Wounds: -2,
            Item.Nightmares: -2,
            Item.AsAboveBecomesBelow: 2
            # TODO: airs change
        }

class CardinalDisagreements_PressPalms(Action):
    def __init__(self):
        super().__init__("Press your palms to the stone")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.AsAboveBecomesBelow) >= 55

    def pass_rate(self, state: BurgundyState):
        return self.narrow_pass_rate(7, state.outfit.chthonosophy)

    def pass_items(self, state: BurgundyState):
        return {
            Item.StolenKiss: 1,
            Item.TouchingLoveStory: 1,
            Item.AsAboveBecomesBelow: 2
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Nightmares: 2,
            Item.AsAboveBecomesBelow: 2
            # TODO: airs change
        }

################################################################
#                     Cutthroats and Canalmen
################################################################

class CutthroatsAndCanalmen(OpportunityCard):
    """Cutthroats and Canalmen card."""
    def __init__(self):
        super().__init__("Cutthroats and Canalmen")
        self.actions = [
            CutthroatsAndCanalmen_TradeKnowledge(),
            CutthroatsAndCanalmen_ViewCity(),
            CutthroatsAndCanalmen_ForayBeyond(),
            CutthroatsAndCanalmen_HeedCall()
        ]

class CutthroatsAndCanalmen_TradeKnowledge(Action):
    def __init__(self):
        super().__init__("Trade local knowledge with Inverse Boatmen")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.RoofChart) >= 4 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.RoofChart: -4,
            Item.UnearthlyFossil: 2,
            Item.CarvedBallOfStygianIvory: 2,
            Item.FinalBreath: 9
            # TODO: airs change
        }

class CutthroatsAndCanalmen_ViewCity(Action):
    def __init__(self):
        super().__init__("Get a view of the city from the water")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.Stuiver) >= 100 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.Stuiver: -100,
            Item.TempestuousTale: 7,
            Item.ExtraordinaryImplication: 2,
            Item.AsAboveBecomesBelow: 2
            # TODO: airs change
        }

class CutthroatsAndCanalmen_ForayBeyond(Action):
    def __init__(self):
        super().__init__("Foray beyond the walls")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.HuntIsOn: 3,
            Item.SampleOfRoofDrip: 10
            # TODO: airs change
        }

class CutthroatsAndCanalmen_HeedCall(Action):
    def __init__(self):
        super().__init__("Heed the call of the hunting-bell")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.HuntIsOn) >= 15 # or state.skip_econ_inputs

    def pass_rate(self, state: BurgundyState):
        # TODO combo score
        score = state.outfit.dangerous + state.outfit.monstrous_anatomy * 15
        return self.broad_pass_rate(220, score)

    def pass_items(self, state: BurgundyState):
        return {
            Item.HuntIsOn: -15,
            Item.StarvedExpression: 16,
            Item.EmeticRevelation: 1,
            Item.AntiqueMystery: 1
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Wounds: 3,
            Item.HuntIsOn: -5
            # TODO: airs change
        }

################################################################
#                     Dreams of Honour and Glory
################################################################

class DreamsOfHonourAndGlory(OpportunityCard):
    """Dreams of Honour and Glory card."""
    def __init__(self):
        super().__init__("Dreams of Honour and Glory")
        self.weight = 2.0
        self.disruptive = False
        self.actions = [
            DreamsOfHonourAndGlory_DetermineSleep(),
            DreamsOfHonourAndGlory_SinkDreams(),
            DreamsOfHonourAndGlory_ConquerSelf()
        ]
    
    def can_draw(self, state: BurgundyState):
        return state.get(Item.Nightmares) >= 15

class DreamsOfHonourAndGlory_DetermineSleep(Action):
    def __init__(self):
        super().__init__("Determine to sleep")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return 0.5  # 50% chance

    def pass_items(self, state: BurgundyState):
        return {
            Item.Nightmares: -1
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Nightmares: 2
            # TODO: airs change
        }

class DreamsOfHonourAndGlory_SinkDreams(Action):
    def __init__(self):
        super().__init__("Sink into the dreams")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.TantalisingPossibility: 10,
            Item.AeolianScream: 1,
            Item.Nightmares: 1,
            Item.FuelForGlorysFire: 2
            # TODO: airs change
        }

class DreamsOfHonourAndGlory_ConquerSelf(Action):
    def __init__(self):
        super().__init__("Conquer yourself, and sleep soundly")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.MemoryOfAMuchLesserSelf) >= 1 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.MemoryOfAMuchLesserSelf: -1,
            Item.TempestuousTale: 1,
            Item.Nightmares: -5
            # TODO: airs change
        }

################################################################
#                     Echoes of Storms Past
################################################################

class EchoesOfStormsPast(OpportunityCard):
    """Echoes of Storms Past card."""
    def __init__(self):
        super().__init__("Echoes of Storms Past")
        self.actions = [
            EchoesOfStormsPast_ReportPatterns(),
            EchoesOfStormsPast_ShelterDamp(),
            EchoesOfStormsPast_ShoutStorm(),
            EchoesOfStormsPast_WatchWinds()
        ]

class EchoesOfStormsPast_ReportPatterns(Action):
    def __init__(self):
        super().__init__("Report the patterns of thunder to the anarchists")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.AgainstTimeAndKings) < 10

    def pass_items(self, state: BurgundyState):
        return {
            Item.Suspicion: 1,
            Item.AgainstTimeAndKings: 1
            # TODO: airs change
        }

class EchoesOfStormsPast_ShelterDamp(Action):
    def __init__(self):
        super().__init__("Shelter from the damp")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.TaleOfTerror: 8
            # TODO: airs change
        }

class EchoesOfStormsPast_ShoutStorm(Action):
    def __init__(self):
        super().__init__("Shout into the storm")

    def can_perform(self, state: BurgundyState):
        # TODO also requires stormy eyed
        return state.get(Item.TempestuousTale) >= 16 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.TempestuousTale: -16,
            Item.StormThrenody: 1,
            Item.Nightmares: 1
            # TODO: airs change
        }

class EchoesOfStormsPast_WatchWinds(Action):
    def __init__(self):
        super().__init__("Watch the winds")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        # TODO aeolian sensitivity from unique hat = +50
        return self.broad_pass_rate(200, state.outfit.watchful)

    def pass_items(self, state: BurgundyState):
        return {
            Item.AeolianScream: 1,
            Item.ManiacsPrayer: 10,
            Item.AsAboveBecomesBelow: 2
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Wounds: 1
            # TODO: airs change
        }

################################################################
#                     Gifts of Burgundy
################################################################

class GiftsOfBurgundy(OpportunityCard):
    """Gifts of Burgundy card."""
    def __init__(self):
        super().__init__("Gifts of Burgundy")
        self.weight = 1_000_000 # HACK for urgent freq
        # self.urgency = 1 # TODO
        self.free_discard = False
        self.actions = [
            GiftsOfBurgundy_ChivalricRomance(),
            GiftsOfBurgundy_PlunderHistory(),
            GiftsOfBurgundy_SpoilsHunt(),
            GiftsOfBurgundy_DucalForgiveness()
        ]

    def can_draw(self, state: BurgundyState):
        return state.get(Item.BurgundianBeneficence) >= 10

class GiftsOfBurgundy_ChivalricRomance(Action):
    def __init__(self):
        super().__init__("A chivalric romance")
        self.action_cost = 0

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.CaptivatingBallad: 1,
            Item.BurgundianBeneficence: -10
            # TODO: airs change
        }

class GiftsOfBurgundy_PlunderHistory(Action):
    def __init__(self):
        super().__init__("The plunder of a violent history")
        self.action_cost = 0

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.MortificationOfAGreatPower: 1,
            Item.BurgundianBeneficence: -10
            # TODO: airs change
        }

class GiftsOfBurgundy_SpoilsHunt(Action):
    def __init__(self):
        super().__init__("The spoils of a great hunt")
        self.action_cost = 0

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.GlimEncrustedCarapace: 1,
            Item.BurgundianBeneficence: -10
            # TODO: airs change
        }

class GiftsOfBurgundy_DucalForgiveness(Action):
    def __init__(self):
        super().__init__("Ducal forgiveness")
        self.action_cost = 0

    def can_perform(self, state: BurgundyState):
        return state.get(Item.Malefactor) >= 1

    def pass_items(self, state: BurgundyState):
        return {
            Item.Malefactor: -1,
            Item.BurgundianBeneficence: -10
            # TODO: airs change
        }

################################################################
#                     Glories and Half-Lives
################################################################

class GloriesAndHalfLives(OpportunityCard):
    """Glories and Half-Lives card."""
    def __init__(self):
        super().__init__("Glories and Half-Lives")
        self.actions = [
            GloriesAndHalfLives_AidWeaver(),
            GloriesAndHalfLives_ObserveMoths(),
            GloriesAndHalfLives_WatchBoats(),
        ]

class GloriesAndHalfLives_AidWeaver(Action):
    def __init__(self):
        super().__init__("Aid a Terrified Weaver")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.TaleOfTerror: 8,
            Item.Nightmares: 2,
            Item.FuelForGlorysFire: 2
            # TODO: airs change
        }

class GloriesAndHalfLives_ObserveMoths(Action):
    def __init__(self):
        super().__init__("Observe the flight patterns of Tapestry-Moths")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        # TODO watchful converts at 0.03 per point
        return self.narrow_pass_rate(11, state.outfit.monstrous_anatomy)

    def pass_items(self, state: BurgundyState):
        return {
            Item.MourningCandle: 1,
            Item.InklingOfIdentity: 20,
            Item.FuelForGlorysFire: 2
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Scandal: 2
            # TODO: airs change
        }

class GloriesAndHalfLives_WatchBoats(Action):
    def __init__(self):
        super().__init__("Watch the boats of Slaughterhall")

    def can_perform(self, state: BurgundyState):
        return True

    # TODO keep this in mind. mid EPA but unique maybe for bone market
    def pass_items(self, state: BurgundyState):
        return {
            Item.ThirstyBombazineScrap: 1,
            Item.HumanArm: 1,
            Item.FuelForGlorysFire: 2
            # TODO: airs change
        }

################################################################
#                     Heralds from Elsewhere
################################################################

class HeraldsFromElsewhere(OpportunityCard):
    """Heralds from Elsewhere card."""
    def __init__(self):
        super().__init__("Heralds from Elsewhere")
        self.weight = 0.8
        self.actions = [
            HeraldsFromElsewhere_ChatGossip(),
            HeraldsFromElsewhere_SightSmuggler(),
            HeraldsFromElsewhere_RestMiserHerd(),
            HeraldsFromElsewhere_ObserveMiners(),
            HeraldsFromElsewhere_BreakFast(),
            HeraldsFromElsewhere_LookEastwardSaltVeined(),
            HeraldsFromElsewhere_LookEastwardNoSaltVeined()
        ]

class HeraldsFromElsewhere_ChatGossip(Action):
    def __init__(self):
        super().__init__("Chat to a Six-Throated Gossip")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.VisitorToBurgundy) <= 1

    def pass_items(self, state: BurgundyState):
        return {
            Item.ScrapOfIncendiaryGossip: 5,
            Item.SwornStatement: 1,
            Item.Scandal: 1,
            Item.VisitorToBurgundy: -state.get(Item.VisitorToBurgundy) + random.randint(1, 6)
            # TODO: airs change
        }

class HeraldsFromElsewhere_SightSmuggler(Action):
    def __init__(self):
        super().__init__("Sight a Circumspect Smuggler")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.VisitorToBurgundy) == 2

    def pass_items(self, state: BurgundyState):
        return {
            Item.BoneFragments: 450,
            Item.FuelForGlorysFire: 1,
            Item.VisitorToBurgundy: -state.get(Item.VisitorToBurgundy) + random.randint(1, 6)
            # TODO: airs change
        }

class HeraldsFromElsewhere_RestMiserHerd(Action):
    def __init__(self):
        super().__init__("Rest with a Weary Miser-Herd")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.VisitorToBurgundy) == 3

    def pass_items(self, state: BurgundyState):
        return {
            # TODO confirm range
            Item.Nightmares: -math.min(state.get(Item.Nightmares) + random.randint(1, 4)),
            Item.ShardOfGlim: 200,
            Item.VisitorToBurgundy: -state.get(Item.VisitorToBurgundy) + random.randint(1, 6)
            # TODO: airs change
        }

class HeraldsFromElsewhere_ObserveMiners(Action):
    def __init__(self):
        super().__init__("Observe a group of lost miners")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.VisitorToBurgundy) == 4

    def pass_items(self, state: BurgundyState):
        return {
            Item.PuzzlingMap: 1,
            Item.UnidentifiedThighBone: 1,
            Item.VisitorToBurgundy: -state.get(Item.VisitorToBurgundy) + random.randint(1, 6)
            # TODO: airs change
        }

class HeraldsFromElsewhere_BreakFast(Action):
    def __init__(self):
        super().__init__("Break fast with a Ravenous Researcher")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.VisitorToBurgundy) == 5

    def pass_items(self, state: BurgundyState):
        return {
            Item.VenomRuby: 50,
            Item.PotOfVenisonMarrow: 5,
            Item.Suspicion: 1,
            Item.UnaccountablyPeckish: random.randint(0, 1),  # TODO: random 0-1, up to 10?
            Item.VisitorToBurgundy: -state.get(Item.VisitorToBurgundy) + random.randint(1, 6)
            # TODO: airs change
        }

class HeraldsFromElsewhere_LookEastwardSaltVeined(Action):
    def __init__(self):
        super().__init__("Look eastward (Salt-Veined)")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.SaltVeined) >= 1 and state.get(Item.VisitorToBurgundy) == 6


    def pass_items(self, state: BurgundyState):
        return {
            Item.RomanticNotion: 20,
            Item.TantalisingPossibility: 45,
            Item.AsAboveBecomesBelow: 1,
            Item.Wounds: 2,
            Item.VisitorToBurgundy: -state.get(Item.VisitorToBurgundy) + random.randint(1, 6)
            # TODO: airs change
        }

class HeraldsFromElsewhere_LookEastwardNoSaltVeined(Action):
    def __init__(self):
        super().__init__("Look eastward (no Salt-Veined)")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.SaltVeined) == 0 and state.get(Item.VisitorToBurgundy) == 6

    def pass_items(self, state: BurgundyState):
        return {
            Item.TantalisingPossibility: 45,
            Item.Nightmares: 2,
            Item.VisitorToBurgundy: -state.get(Item.VisitorToBurgundy) + random.randint(1, 6)
            # TODO: airs change
        }

# TODO check this one, start HERE when we pick up again
################################################################
#                     Hunting the (Roof Prey)
################################################################

class HuntingTheRoofPrey(OpportunityCard):
    """Hunting the (Roof Prey) card."""
    def __init__(self):
        super().__init__("Hunting the (Roof Prey)")
        self.actions = [
            HuntingTheRoofPrey_GoForGlory(),
            HuntingTheRoofPrey_StayWithPack()
        ]

    def can_draw(self, state: BurgundyState):
        return state.get(Item.SeasonOfHunting) >= 1

class HuntingTheRoofPrey_GoForGlory(Action):
    def __init__(self):
        super().__init__("Go for glory")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.SeasonOfHunting) >= 1

    def pass_rate(self, state: BurgundyState):
        score = state.outfit.dangerous + 15 * state.outfit.neathproofed
        return self.broad_pass_rate(230, score)

    def pass_items(self, state: BurgundyState):
        return {
            Item.MakingWaves: 5,
            Item.SeasonOfHunting: -1
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Dangerous: 1,
            Item.Wounds: 3,  # TODO: random 2-4
            Item.Scandal: 2,  # TODO: random 1-2
            Item.SeasonOfHunting: -1
            # TODO: airs change
        }

class HuntingTheRoofPrey_StayWithPack(Action):
    def __init__(self):
        super().__init__("Stay with the pack")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.SeasonOfHunting) >= 1

    def pass_rate(self, state: BurgundyState):
        score = state.outfit.dangerous + 15 * state.outfit.neathproofed
        return self.broad_pass_rate(210, score)
    
    def pass_items(self, state: BurgundyState):
        return {
            Item.SeasonOfHunting: -1
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Dangerous: 1,
            Item.Wounds: 2,
            Item.SeasonOfHunting: -1
            # TODO: airs change
        }

################################################################
#                     In Aid of a Feast
################################################################

class InAidOfAFeast(OpportunityCard):
    """In Aid of a Feast card."""
    def __init__(self):
        super().__init__("In Aid of a Feast")
        self.free_discard = False
        self.actions = [
            InAidOfAFeast_AttendFeast()
        ]

    def can_draw(self, state: BurgundyState):
        return state.feast_ready()

class InAidOfAFeast_AttendFeast(Action):
    def __init__(self):
        super().__init__("Attend the feast")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.CellarOfWine: 4,
            Item.PreparationsForASaintsDay: -state.get(Item.PreparationsForASaintsDay),
            Item.SaintsDayConflictsResolved: -state.get(Item.SaintsDayConflictsResolved)
        }

################################################################
#                     Preparations for a Saint's Day
################################################################

class PreparationsForASaintsDay(OpportunityCard):
    """Preparations for a Saint's Day card."""
    def __init__(self):
        super().__init__("Preparations for a Saint's Day")
        self.weight = 0.5
        self.actions = [
            PreparationsForASaintsDay_PledgeFeast(),
            PreparationsForASaintsDay_FomentUnrest()
        ]

    def can_draw(self, state: BurgundyState):
        return state.get(Item.PreparationsForASaintsDay) == 0

class PreparationsForASaintsDay_PledgeFeast(Action):
    def __init__(self):
        super().__init__("Pledge yourself to aiding a glorious feast")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 10  # Sets to A Grand Feast
        }

class PreparationsForASaintsDay_FomentUnrest(Action):
    def __init__(self):
        super().__init__("Foment unrest within a procession")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 20  # Sets to A March of Dissent
        }

################################################################
#                     Rising and Falling
################################################################

class RisingAndFalling(OpportunityCard):
    """Rising and Falling card."""
    def __init__(self):
        super().__init__("Rising and Falling")
        self.actions = [
            RisingAndFalling_WanderStreets(),
            RisingAndFalling_SkirtEmptyPlaces(),
            RisingAndFalling_EavesdropLoyalists(),
            # RisingAndFalling_PledgeFortune()
        ]

class RisingAndFalling_WanderStreets(Action):
    def __init__(self):
        super().__init__("Wander the streets")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.PartialMap: 1,
            Item.FinalBreath: 3,
            Item.NotesOnAJoyousEntry: 2
            # TODO: airs change
        }

class RisingAndFalling_SkirtEmptyPlaces(Action):
    def __init__(self):
        super().__init__("Skirt the empty places")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.NotesOnAJoyousEntry) >= 15

    def pass_items(self, state: BurgundyState):
        return {
            Item.UnprovenancedArtefact: 1,
            Item.CorrespondencePlaque: 4,
            Item.NotesOnAJoyousEntry: 2
            # TODO: airs change
        }

class RisingAndFalling_EavesdropLoyalists(Action):
    def __init__(self):
        super().__init__("Eavesdrop on ducal loyalists")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.TantalisingPossibility: 25,
            Item.ExtraordinaryImplication: 1,
            Item.NotesOnAJoyousEntry: 2
            # TODO: airs change
        }

# class RisingAndFalling_PledgeFortune(Action):
#     def __init__(self):
#         super().__init__("Pledge a fortune to the cause of Burgundy")

#     def can_perform(self, state: BurgundyState):
#         return state.get(Item.Stuiver) >= 1_000_000

#     def pass_items(self, state: BurgundyState):
#         return {
#             Item.Stuiver: -1_000_000,
#             Item.KnightsOfTheGoldenCarapace: 1
#         }

################################################################
#                     Sought by Pike and Guardsman
################################################################

class SoughtByPikeAndGuardsman(OpportunityCard):
    """Sought by Pike and Guardsman card."""
    def __init__(self):
        super().__init__("Sought by Pike and Guardsman")
        self.weight = 2.0
        self.free_discard = False
        self.actions = [
            SoughtByPikeAndGuardsman_ActNatural(),
            SoughtByPikeAndGuardsman_PayForTale(),
            SoughtByPikeAndGuardsman_DonateCharts(),
            SoughtByPikeAndGuardsman_HandOverSack()
        ]
    
    def can_draw(self, state: BurgundyState):
        return state.get(Item.Suspicion) >= 15

class SoughtByPikeAndGuardsman_ActNatural(Action):
    def __init__(self):
        super().__init__("Act natural")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return 0.5  # 50% chance

    def pass_items(self, state: BurgundyState):
        return {
            Item.Suspicion: -2
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Suspicion: 1,
            Item.Wounds: 1
            # TODO: airs change
        }

class SoughtByPikeAndGuardsman_PayForTale(Action):
    def __init__(self):
        super().__init__("Pay for a tale from a prisoner")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.Stuiver) >= 160 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.Stuiver: -160,
            Item.MemoryOfMoonlight: 1,
            Item.Suspicion: 2
            # TODO: airs change
        }

class SoughtByPikeAndGuardsman_DonateCharts(Action):
    def __init__(self):
        super().__init__("Donate Roof-Charts to the dockmasters")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.RoofChart) >= 1 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.RoofChart: -1,
            Item.TaleOfTerror: 1,
            Item.Suspicion: -4
            # TODO: airs change
        }

class SoughtByPikeAndGuardsman_HandOverSack(Action):
    def __init__(self):
        super().__init__("Hand over a sack of stolen goods")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.SaddledWithAStolenSack) >= 1

    def pass_items(self, state: BurgundyState):
        return {
            Item.SaddledWithAStolenSack: -1,
            Item.Suspicion: -6
            # TODO: airs change
        }

################################################################
#                     Spreading Sedition: A Twisted Pilgrimage
################################################################

class SpreadingSeditionTwistedPilgrimage(OpportunityCard):
    """Spreading Sedition: A Twisted Pilgrimage card."""
    def __init__(self):
        super().__init__("Spreading Sedition: A Twisted Pilgrimage")
        self.actions = [
            SpreadingSeditionTwistedPilgrimage_SeedDebauchery(),
            SpreadingSeditionTwistedPilgrimage_TweakRoute()
        ]

    def can_draw(self, state: BurgundyState):
        return state.aiding_march()

class SpreadingSeditionTwistedPilgrimage_SeedDebauchery(Action):
    def __init__(self):
        super().__init__("Seed the city with debauchery")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.NightOnTheTown) >= 1 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.NightOnTheTown: -1,
            Item.PreparationsForASaintsDay: 1
        }

class SpreadingSeditionTwistedPilgrimage_TweakRoute(Action):
    def __init__(self):
        super().__init__("Tweak the route of the pilgrimage")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return self.narrow_pass_rate(10, state.outfit.zeefaring)

    def pass_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 1
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 1,
            Item.Nightmares: 2
        }

################################################################
#                     Spreading Sedition: Hearts and Minds
################################################################

class SpreadingSeditionHeartsAndMinds(OpportunityCard):
    """Spreading Sedition: Hearts and Minds card."""
    def __init__(self):
        super().__init__("Spreading Sedition: Hearts and Minds")
        self.actions = [
            SpreadingSeditionHeartsAndMinds_LubricateMarchers(),
            SpreadingSeditionHeartsAndMinds_BendEars()
        ]

    def can_draw(self, state: BurgundyState):
        return state.aiding_march()

class SpreadingSeditionHeartsAndMinds_LubricateMarchers(Action):
    def __init__(self):
        super().__init__("Lubricate the marchers with alcohol")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.MagisterialLager) >= 5 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.MagisterialLager: -5,
            Item.PreparationsForASaintsDay: 1
        }

class SpreadingSeditionHeartsAndMinds_BendEars(Action):
    def __init__(self):
        super().__init__("Bend the ears of Guildspeople")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return self.narrow_pass_rate(10, state.outfit.mithridacy)

    def pass_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 1
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.PreparationsForASaintsDay: 1,
            Item.Suspicion: 3
        }

################################################################
#                     Stopped by the Guards
################################################################

class StoppedByTheGuards(OpportunityCard):
    """Stopped by the Guards card."""
    def __init__(self):
        super().__init__("Stopped by the Guards")
        self.autofire = True
        self.weight = 2.0
        self.actions = [
            StoppedByTheGuards_Bribe(),
            StoppedByTheGuards_MakeRun(),
            StoppedByTheGuards_Bluff()
        ]

class StoppedByTheGuards_Bribe(Action):
    def __init__(self):
        super().__init__("Bribe them")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.TaleOfTerror: 2,
            Item.Suspicion: 2
            # TODO: airs change
        }

class StoppedByTheGuards_MakeRun(Action):
    def __init__(self):
        super().__init__("Make a run for it")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.HandPickedPeppercaps: 2,
            Item.Suspicion: 2
            # TODO: airs change
        }

class StoppedByTheGuards_Bluff(Action):
    def __init__(self):
        super().__init__("Bluff")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.PrimordialShriek: 50,
            Item.Suspicion: 2
            # TODO: airs change
        }

################################################################
#                     The Banners of the Guilds
################################################################

class BannersOfTheGuilds(OpportunityCard):
    """The Banners of the Guilds card."""
    def __init__(self):
        super().__init__("The Banners of the Guilds")
        self.actions = [
            BannersOfTheGuilds_FerretApothecaries(),
            BannersOfTheGuilds_VisitBoatmen(),
            BannersOfTheGuilds_WatchMoths(),
            BannersOfTheGuilds_LabourMorel()
        ]

class BannersOfTheGuilds_FerretApothecaries(Action):
    def __init__(self):
        super().__init__("Ferret out the Guild of Apothecaries")

    def can_perform(self, state: BurgundyState):
        # TODO: requires airs <= 50
        return True

    def pass_rate(self, state: BurgundyState):
        # TODO watchful adds 0.02 per point
        return self.narrow_pass_rate(11, state.outfit.kataleptic_toxicology)

    def pass_items(self, state: BurgundyState):
        return {
            Item.FlaskOfAbominableSalts: 10,
            Item.StarvedExpression: 6
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Scandal: 2
            # TODO: airs change
        }

class BannersOfTheGuilds_VisitBoatmen(Action):
    def __init__(self):
        super().__init__("Visit the Inverse Boatmen")

    def can_perform(self, state: BurgundyState):
        # TODO: requires airs >= 51
        return True

    def pass_rate(self, state: BurgundyState):
        return self.narrow_pass_rate(11, state.outfit.zeefaring)

    def pass_items(self, state: BurgundyState):
        return {
            Item.RoofChart: 1,
            Item.MapScrap: 15
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Scandal: 2
            # TODO: airs change
        }

class BannersOfTheGuilds_WatchMoths(Action):
    def __init__(self):
        super().__init__("Watch for Tapestry-Moths")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.CrypticClue: 175,
            Item.FuelForGlorysFire: 2
            # TODO: airs change
        }

class BannersOfTheGuilds_LabourMorel(Action):
    def __init__(self):
        super().__init__("Labour for the Guild of Morel-measurers")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.StrongBackedLabour) >= 1 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.StrongBackedLabour: -1,
            Item.StarvedExpression: 1,
            Item.Suspicion: -3
            # TODO: airs change
        }

################################################################
#                     The Burgundy of Blood
################################################################

class BurgundyOfBlood(OpportunityCard):
    """The Burgundy of Blood card."""
    def __init__(self):
        super().__init__("The Burgundy of Blood")
        self.weight = 2.0
        self.free_discard = False
        self.actions = [
            BurgundyOfBlood_CallDoctor(),
            BurgundyOfBlood_PermitAnarchists(),
            BurgundyOfBlood_PurchaseRelief()
        ]



class BurgundyOfBlood_CallDoctor(Action):
    def __init__(self):
        super().__init__("Call for the doctor")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return 0.5  # 50% chance

    def pass_items(self, state: BurgundyState):
        return {
            Item.Wounds: -1
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Wounds: 2
            # TODO: airs change
        }

class BurgundyOfBlood_PermitAnarchists(Action):
    def __init__(self):
        super().__init__("Permit anarchists to test 'new techniques'")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.Wounds: 1,
            Item.AgainstTimeAndKings: 1
            # TODO: airs change
        }

class BurgundyOfBlood_PurchaseRelief(Action):
    def __init__(self):
        super().__init__("Purchase relief from a visiting Starved Man")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.NoduleOfWarmAmber) >= 25 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.NoduleOfWarmAmber: -25,
            Item.StarvedExpression: 1,
            Item.Wounds: -4  # TODO: random 4-5 CP
            # TODO: airs change
        }

################################################################
#                     The Honours of the Court
################################################################

class HonoursOfTheCourt(OpportunityCard):
    """The Honours of the Court card."""
    def __init__(self):
        super().__init__("The Honours of the Court")
        self.actions = [
            HonoursOfTheCourt_CentreAttention(),
            HonoursOfTheCourt_RescueReichsgraf(),
            HonoursOfTheCourt_WalkWalls(),
            HonoursOfTheCourt_BringAcquaintance()
        ]

class HonoursOfTheCourt_CentreAttention(Action):
    def __init__(self):
        super().__init__("Make yourself the centre of attention")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return self.broad_pass_rate(220, state.outfit.persuasive)

    def pass_items(self, state: BurgundyState):
        return {
            Item.FinalBreath: 6,
            Item.DubiousTestimony: 2
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Persuasive: 1,
            Item.Scandal: 2
            # TODO: airs change
        }

class HonoursOfTheCourt_RescueReichsgraf(Action):
    def __init__(self):
        super().__init__("Rescue an Unwary Reichsgraf")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        # TODO inerrant adds 1 per point
        return self.narrow_pass_rate(11, state.outfit.monstrous_anatomy)

    def pass_items(self, state: BurgundyState):
        return {
            Item.BurgundianBeneficence: 1
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.LiveSpecimen: 1,
            Item.Wounds: 4
            # TODO: airs change
        }

class HonoursOfTheCourt_WalkWalls(Action):
    def __init__(self):
        super().__init__("Walk the court's eponymous broken walls")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.NightOnTheTown: 1,
            Item.TempestuousTale: 2,
            Item.NotesOnAJoyousEntry: 2
            # TODO: airs change
        }

class HonoursOfTheCourt_BringAcquaintance(Action):
    def __init__(self):
        super().__init__("Bring an acquaintance along")

    def can_perform(self, state: BurgundyState):
        # TODO requires DiptychPainter companion
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.Fascinating: 6,
            Item.WellPlacedPawn: 10
            # TODO: airs change
        }

################################################################
#                     The Spoils of Rebellion
################################################################

class SpoilsOfRebellion(OpportunityCard):
    """The Spoils of Rebellion card."""
    def __init__(self):
        super().__init__("The Spoils of Rebellion")
        self.weight = 1_000_000 # HACK urgency
        self.actions = [
            SpoilsOfRebellion_AspirationalChronicle(),
            SpoilsOfRebellion_PromiseOfCooperation(),
            SpoilsOfRebellion_SparkingAnachronism(),
            SpoilsOfRebellion_TheCoffin()
        ]

    def can_draw(self, state: GameState):
        return state.get(Item.AgainstTimeAndKings) >= 10

class SpoilsOfRebellion_AspirationalChronicle(Action):
    def __init__(self):
        self.action_cost = 0
        super().__init__("An aspirational chronicle")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.AgainstTimeAndKings) >= 10 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.ChimericalArchive: 1,
            Item.AgainstTimeAndKings: -10
            # TODO: airs change
        }

class SpoilsOfRebellion_PromiseOfCooperation(Action):
    def __init__(self):
        self.action_cost = 0
        super().__init__("The promise of cooperation")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.AgainstTimeAndKings) >= 10 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.MuchNeededGap: 1,
            Item.AgainstTimeAndKings: -10
            # TODO: airs change
        }

class SpoilsOfRebellion_SparkingAnachronism(Action):
    def __init__(self):
        self.action_cost = 0
        super().__init__("A sparking anachronism")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.AgainstTimeAndKings) >= 10 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.CracklingDevice: 1,
            Item.AgainstTimeAndKings: -10
            # TODO: airs change
        }

class SpoilsOfRebellion_TheCoffin(Action):
    def __init__(self):
        self.action_cost = 0
        super().__init__("The coffin")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.AgainstTimeAndKings) >= 10 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.SootheAndCooperLongBox: 1,
            Item.AgainstTimeAndKings: -10
            # TODO: airs change
        }

################################################################
#                     The Tint of Unworthiness
################################################################

class TintOfUnworthiness(OpportunityCard):
    """The Tint of Unworthiness card."""
    def __init__(self):
        super().__init__("The Tint of Unworthiness")
        self.actions = [
            TintOfUnworthiness_CarrySupplies(),
            TintOfUnworthiness_RevelHypocrisy(),
            TintOfUnworthiness_SearchStanding()
        ]

    def can_draw(self, state: GameState):
        return state.get(Item.Malefactor) >= 1
    
class TintOfUnworthiness_CarrySupplies(Action):
    def __init__(self):
        super().__init__("Carry anarchist supplies into the streets around the Gravensteen")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        # TODO a bunch of secondary stats
        return self.broad_pass_rate(180, state.outfit.watchful)

    def pass_items(self, state: BurgundyState):
        return {
            Item.AgainstTimeAndKings: 1
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Watchful: 1,
            Item.Suspicion: 2
            # TODO: airs change
        }

class TintOfUnworthiness_RevelHypocrisy(Action):
    def __init__(self):
        super().__init__("Revel in the hypocrisy")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.TaleOfTerror: 7,
            Item.NotesOnAJoyousEntry: 2,
            Item.AdriftOnASeaOfMisery: 1
            # TODO: airs change
        }

class TintOfUnworthiness_SearchStanding(Action):
    def __init__(self):
        super().__init__("Search for ways to regain your standing")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.ScrapOfIncendiaryGossip: 7,
            Item.Suspicion: 1
            # TODO: airs change
        }

################################################################
#                     The Tolling of the Thief-Bells
################################################################

class TollingOfTheThiefBells(OpportunityCard):
    """The Tolling of the Thief-Bells card."""
    def __init__(self):
        super().__init__("The Tolling of the Thief-Bells")
        self.actions = [
            TollingOfTheThiefBells_PlunderStudy(),
            TollingOfTheThiefBells_StealGravensteen(),
            TollingOfTheThiefBells_InspectPatrols(),
            TollingOfTheThiefBells_AcceptOpportunity()
        ]

class TollingOfTheThiefBells_PlunderStudy(Action):
    def __init__(self):
        super().__init__("Plunder a Silk-Clad Comte's study")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return self.broad_pass_rate(200, state.outfit.shadowy)

    def pass_items(self, state: BurgundyState):
        return {
            Item.MovesInTheGreatGame: 8
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Shadowy: 1,
            Item.Suspicion: 2
            # TODO: airs change
        }

class TollingOfTheThiefBells_StealGravensteen(Action):
    def __init__(self):
        super().__init__("Steal from the Gravensteen itself")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.Casing) >= 36

    def pass_items(self, state: BurgundyState):
        return {
            Item.VenomRuby: 10,
            Item.MemoryOfMoonlight: 1,
            Item.PuzzleDamaskScrap: 1,
            Item.MagnificentDiamond: 1,
            Item.Casing: -36
            # TODO: airs change
        }

class TollingOfTheThiefBells_InspectPatrols(Action):
    def __init__(self):
        super().__init__("Inspect the guard patrols of the great and the good")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return self.broad_pass_rate(210, state.outfit.shadowy)

    def pass_items(self, state: BurgundyState):
        return {
            Item.AgainstTimeAndKings: 1
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Suspicion: 3
            # TODO: airs change
        }

class TollingOfTheThiefBells_AcceptOpportunity(Action):
    def __init__(self):
        super().__init__("Accept a lucrative opportunity")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.SaddledWithAStolenSack) == 0

    def pass_items(self, state: BurgundyState):
        return {
            Item.SaddledWithAStolenSack: 1
            # TODO: airs change
        }

################################################################
#                     Vine-Strangled Aisles
################################################################

class VineStrangledAisles(OpportunityCard):
    """Vine-Strangled Aisles card."""
    def __init__(self):
        super().__init__("Vine-Strangled Aisles")
        self.actions = [
            VineStrangledAisles_PickFruit(),
            VineStrangledAisles_GiveCharity(),
            VineStrangledAisles_SavePriest()
        ]

class VineStrangledAisles_PickFruit(Action):
    def __init__(self):
        super().__init__("Pick a sainted fruit")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.CounterfeitHeadOfJohnTheBaptist: 1,
            Item.AnIdentityUncovered: 1
            # TODO: airs change
        }

class VineStrangledAisles_GiveCharity(Action):
    def __init__(self):
        super().__init__("Give 'charity'")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.NightsoilOfTheBazaar) >= 5 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.NightsoilOfTheBazaar: -5,
            Item.ApostatesPsalm: 3
            # TODO: airs change
        }

class VineStrangledAisles_SavePriest(Action):
    def __init__(self):
        super().__init__("Save a priest!")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return self.narrow_pass_rate(12, state.outfit.monstrous_anatomy)

    def pass_items(self, state: BurgundyState):
        return {
            Item.BurgundianBeneficence: 1
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.Scandal: 2
            # TODO: airs change
        }

################################################################
#                     Warrens of Worship
################################################################

class WarrensOfWorship(OpportunityCard):
    """Warrens of Worship card."""
    def __init__(self):
        super().__init__("Warrens of Worship")
        self.actions = [
            WarrensOfWorship_AskDirections(),
            WarrensOfWorship_LightCandles(),
            WarrensOfWorship_MakeDonation(),
            WarrensOfWorship_LeavePostHaste()
        ]

class WarrensOfWorship_AskDirections(Action):
    def __init__(self):
        super().__init__("Ask for directions")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_rate(self, state: BurgundyState):
        return self.broad_pass_rate(300, state.outfit.watchful)

    def pass_items(self, state: BurgundyState):
        return {
            Item.PartialMap: 1,
            Item.PalimpsestScrap: 2,
            Item.NotesOnAJoyousEntry: 2
            # TODO: airs change
        }

    def fail_items(self, state: BurgundyState):
        return {
            Item.PartialMap: 1,
            Item.Nightmares: 2,
            Item.NotesOnAJoyousEntry: 2
            # TODO: airs change
        }

class WarrensOfWorship_LightCandles(Action):
    def __init__(self):
        super().__init__("Light candles in the Count's Chapel")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.MourningCandle) >= 2 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.MourningCandle: -2,
            Item.TouchingLoveStory: 1,
            Item.ExtraordinaryImplication: 1,
            Item.BurgundianBeneficence: 1
            # TODO: airs change
        }

class WarrensOfWorship_MakeDonation(Action):
    def __init__(self):
        super().__init__("Make a generous donation")

    def can_perform(self, state: BurgundyState):
        return state.get(Item.Stuiver) >= 1160 or state.skip_econ_inputs

    def pass_items(self, state: BurgundyState):
        return {
            Item.Stuiver: -1160,
            Item.VerseOfCounterCreed: 5
            # TODO: airs change
        }

class WarrensOfWorship_LeavePostHaste(Action):
    def __init__(self):
        super().__init__("Leave post-haste")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.ApostatesPsalm: 1,
            Item.FinalBreath: 3,
            Item.Nightmares: 1  # TODO: random 0-1 CP
            # TODO: airs change
        }

################################################################
#                     Whoso List to Hunt
################################################################

class WhosoListToHunt(OpportunityCard):
    """Whoso List to Hunt card."""
    def __init__(self):
        super().__init__("Whoso List to Hunt")
        self.weight = 0.5
        self.actions = [
            WhosoListToHunt_ChooseSteedAndWeapon(),
        ]

    def can_perform(self, state: BurgundyState):
        return state.get(Item.SeasonOfHunting) == 0

class WhosoListToHunt_ChooseSteedAndWeapon(Action):
    def __init__(self):
        super().__init__("(Choose steed and arms)")

    def can_perform(self, state: BurgundyState):
        return True

    def pass_items(self, state: BurgundyState):
        return {
            Item.SeasonOfHunting: 6
            # TODO: airs change
        }

################################################################
#                     Simulation Runner
################################################################

class BurgundySimRunner(SimulationRunner):
    """Runner for Burgundy simulations."""
    def __init__(self, runs: int, initial_values: dict):
        super().__init__(runs, initial_values)
        self.storylets = [
            StoryletBurgundy()
        ]
        self.cards = [
            GloomySummer(),
            MarchForThePeople(),
            StrangerOutOfTime(),
            AidingFeastChurchAndState(),
            AidingFeastHeartsAndStomachs(),
            AllAroundTheCountsRock(),
            EncounterWithThePoetThief(),
            InvitationFromTheSwashbucklingChevalier(),
            BeneathTheGiltExterior(),
            CardinalDisagreements(),
            CutthroatsAndCanalmen(),
            DreamsOfHonourAndGlory(),
            EchoesOfStormsPast(),
            GiftsOfBurgundy(),
            GloriesAndHalfLives(),
            HeraldsFromElsewhere(),
            HuntingTheRoofPrey(),
            InAidOfAFeast(),
            PreparationsForASaintsDay(),
            RisingAndFalling(),
            SoughtByPikeAndGuardsman(),
            SpreadingSeditionTwistedPilgrimage(),
            SpreadingSeditionHeartsAndMinds(),
            StoppedByTheGuards(),
            BannersOfTheGuilds(),
            BurgundyOfBlood(),
            HonoursOfTheCourt(),
            SpoilsOfRebellion(),
            TintOfUnworthiness(),
            TollingOfTheThiefBells(),
            VineStrangledAisles(),
            WarrensOfWorship(),
            WhosoListToHunt()
        ]

    def create_state(self):
        """Create and initialize a new BurgundyState."""
        state = BurgundyState()
        return state

# Example usage
if __name__ == "__main__":
    runner = BurgundySimRunner(
        runs=10000,
        initial_values={
            Item.Scandal: 0,
            Item.Suspicion: 0,
            Item.BlackmailMaterial: 0,
            Item.Stuiver: 0,
            Item.VolumeOfCollatedResearch: 0,
            Item.BurgundianBeneficence: 0,
            Item.AgainstTimeAndKings: 0,
            Item.PalimpsestScrap: 0,
            Item.PotOfVenisonMarrow: 0,
            Item.NewlyCastCrownOfTheCityOfLondon: 0,
            Item.Watchful: 0,
            Item.Persuasive: 0,
            Item.Casing: 0,
            Item.Fascinating: 0,
            Item.Wounds: 0,
            Item.PreparationsForASaintsDay: 0,
            Item.SaddledWithAStolenSack: 0,
            Item.SeasonOfHunting: 0,
            Item.StrongBackedLabour: 0,
            Item.Nightmares: 0,
            # Item.AdriftOnASeaOfMisery: 0,
            Item.NotesOnAJoyousEntry: 0
        }
    )
    runner.outfit = PlayerOutfit(340, 18)  # Example outfit stats
    runner.run_simulation() 