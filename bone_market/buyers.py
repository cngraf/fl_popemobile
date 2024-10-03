import math
from enum import Enum, auto
from bone_market.models import Bone
from enums import *
import helper.utils as utils
from config import Config
from player import Player
from bone_market.models import *

suspicion_multiplier = 0.85
exhaustion_hard_cap = 4

exhaustion_items = {
    Item.GenericBoneMarketExhaustion,

    Item.AmalgamyReptileExhaustion,
    Item.AmalgamyAmphibianExhaustion,
    Item.AmalgamyBirdExhaustion ,
    Item.AmalgamyFishExhaustion,
    Item.AmalgamyArachnidExhaustion,
    Item.AmalgamyInsectExhaustion,
    Item.AmalgamyPrimateExhaustion,

    Item.MenaceReptileExhaustion,
    Item.MenaceAmphibianExhaustion,    
    Item.MenaceBirdExhaustion,
    Item.MenaceFishExhaustion,
    Item.MenaceArachnidExhaustion,
    Item.MenaceInsectExhaustion,      
    Item.MenacePrimateExhaustion,      

    Item.AntiquityGeneralExhaustion,
    Item.AmalgamyGeneralExhaustion,
    Item.MenaceGeneralExhaustion,

    Item.GeneralReptileExhaustion,
    Item.GeneralAmphibianExhaustion,    
    Item.GeneralBirdExhaustion,
    Item.GeneralFishExhaustion,
    Item.GeneralArachnidExhaustion,
    Item.GeneralInsectExhaustion,    
    Item.GeneralPrimateExhaustion,       
}

class Buyer():
    def __init__(self, name, impl_dc: 0):
        self.name = name
        # zoo_type = zoo_type
        # flux = flux
        self.implausibility_dc = impl_dc
        self.suspicion_on_failure = 2

    def add_trade(self, config, flux, zoo_type, recipe):
        weekly_action_type = self.match_action_type(zoo_type, flux)
        weekly_action_cost = {
            weekly_action_type: recipe[Item.Action]
        }

        skeleton = Bone.create_skeleton(recipe)
        primary = self.primary_payout(flux, zoo_type, skeleton)
        secondary = self.secondary_payout(flux, zoo_type, skeleton)

        failures = self.expected_failed_sell_attempts(config, zoo_type, skeleton)
        failure_penalty = {
            Item.Action: -1 * failures,
            weekly_action_type: -1 * failures,
            Item.Suspicion: self.suspicion_on_failure * suspicion_multiplier * failures
        }

        total = utils.sum_dicts(
            recipe,
            weekly_action_cost,
            skeleton.addtl_costs,
            primary,
            secondary,
            failure_penalty)
        
        exhaustion_type = self.match_exhaustion_type(zoo_type, flux)
        if total.get(exhaustion_type, 0) <= exhaustion_hard_cap:
            config.add(total)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        return {}
    
    def secondary_payout(self, flux, zoo_type, skeleton: Bone):
        return {}
    
    def expected_failed_sell_attempts(self, config: Config, zoo_type, skeleton: Bone):
        shadowy = config.player.qualities[Item.Shadowy]
        impl = skeleton.implausibility
        if zoo_type == ZooType.Chimera:
            impl += 3
        
        dc = self.implausibility_dc * (skeleton.implausibility)
    
        pass_rate = max(0.01, utils.broad_challenge_pass_rate(shadowy, dc))
        return (1.0 / pass_rate) - 1
     
    # TODO implement for relevant buyers
    def can_buy(self, skeleton: Bone):
        return True

    @staticmethod
    def zoo_multiplier(skeletonType = ZooType):
        if skeletonType in (ZooType.Bird, ZooType.Amphibian, ZooType.Reptile, ZooType.Primate):
            return 1.1
        if skeletonType in (ZooType.Fish, ZooType.Insect, ZooType.Spider):
            return 1.15
        else:
            return 1.0
    
    @staticmethod
    def match_action_type(zoo_type, flux_type):
        if zoo_type == ZooType.Reptile:
            if flux_type == Flux.Antiquity:
                return Item._AntiquityReptileAction
            elif flux_type == Flux.Amalgamy:
                return Item._AmalgamyReptileAction
            elif flux_type == Flux.Menace:
                return Item._MenaceReptileAction
            else:
                return Item._GeneralReptileAction
        
        elif zoo_type == ZooType.Amphibian:
            if flux_type == Flux.Antiquity:
                return Item._AntiquityAmphibianAction
            elif flux_type == Flux.Amalgamy:
                return Item._AmalgamyAmphibianAction
            elif flux_type == Flux.Menace:
                return Item._MenaceAmphibianAction
            else:
                return Item._GeneralAmphibianAction        

        elif zoo_type == ZooType.Bird:
            if flux_type == Flux.Antiquity:
                return Item._AntiquityBirdAction
            elif flux_type == Flux.Amalgamy:
                return Item._AmalgamyBirdAction
            elif flux_type == Flux.Menace:
                return Item._MenaceBirdAction
            else:
                return Item._GeneralBirdAction
            
        elif zoo_type == ZooType.Fish:
            if flux_type == Flux.Antiquity:
                return Item._AntiquityFishAction
            elif flux_type == Flux.Amalgamy:
                return Item._AmalgamyFishAction
            elif flux_type == Flux.Menace:
                return Item._MenaceFishAction
            else:
                return Item._GeneralFishAction        

        elif zoo_type == ZooType.Spider:
            if flux_type == Flux.Antiquity:
                return Item._AntiquityArachnidAction
            elif flux_type == Flux.Amalgamy:
                return Item._AmalgamyArachnidAction
            elif flux_type == Flux.Menace:
                return Item._MenaceArachnidAction
            else:
                return Item._GeneralArachnidAction        

        elif zoo_type == ZooType.Insect:
            if flux_type == Flux.Antiquity:
                return Item._AntiquityInsectAction
            elif flux_type == Flux.Amalgamy:
                return Item._AmalgamyInsectAction
            elif flux_type == Flux.Menace:
                return Item._MenaceInsectAction
            else:
                return Item._GeneralInsectAction
            
        elif zoo_type == ZooType.Primate:
            if flux_type == Flux.Antiquity:
                return Item._AntiquityPrimateAction
            elif flux_type == Flux.Amalgamy:
                return Item._AmalgamyPrimateAction
            elif flux_type == Flux.Menace:
                return Item._MenacePrimateAction
            else:
                return Item._GeneralPrimateAction

        else:
            if flux_type == Flux.Antiquity:
                return Item._AntiquityGeneralAction
            elif flux_type == Flux.Amalgamy:
                return Item._AmalgamyGeneralAction
            elif flux_type == Flux.Menace:
                return Item._MenaceGeneralAction
            else:
                return Item._NoItem # HACK        

    @staticmethod
    def match_exhaustion_type(zoo_type, flux_type):
        if zoo_type == ZooType.Reptile:
            if flux_type == Flux.Antiquity:
                return Item.AntiquityReptileExhaustion
            elif flux_type == Flux.Amalgamy:
                return Item.AmalgamyReptileExhaustion
            elif flux_type == Flux.Menace:
                return Item.MenaceReptileExhaustion
            else:
                return Item.GeneralReptileExhaustion
        
        elif zoo_type == ZooType.Amphibian:
            if flux_type == Flux.Antiquity:
                return Item.AntiquityAmphibianExhaustion
            elif flux_type == Flux.Amalgamy:
                return Item.AmalgamyAmphibianExhaustion
            elif flux_type == Flux.Menace:
                return Item.MenaceAmphibianExhaustion
            else:
                return Item.GeneralAmphibianExhaustion        

        elif zoo_type == ZooType.Bird:
            if flux_type == Flux.Antiquity:
                return Item.AntiquityBirdExhaustion
            elif flux_type == Flux.Amalgamy:
                return Item.AmalgamyBirdExhaustion
            elif flux_type == Flux.Menace:
                return Item.MenaceBirdExhaustion
            else:
                return Item.GeneralBirdExhaustion
            
        elif zoo_type == ZooType.Fish:
            if flux_type == Flux.Antiquity:
                return Item.AntiquityFishExhaustion
            elif flux_type == Flux.Amalgamy:
                return Item.AmalgamyFishExhaustion
            elif flux_type == Flux.Menace:
                return Item.MenaceFishExhaustion
            else:
                return Item.GeneralFishExhaustion        

        elif zoo_type == ZooType.Spider:
            if flux_type == Flux.Antiquity:
                return Item.AntiquityArachnidExhaustion
            elif flux_type == Flux.Amalgamy:
                return Item.AmalgamyArachnidExhaustion
            elif flux_type == Flux.Menace:
                return Item.MenaceArachnidExhaustion
            else:
                return Item.GeneralArachnidExhaustion        

        elif zoo_type == ZooType.Insect:
            if flux_type == Flux.Antiquity:
                return Item.AntiquityInsectExhaustion
            elif flux_type == Flux.Amalgamy:
                return Item.AmalgamyInsectExhaustion
            elif flux_type == Flux.Menace:
                return Item.MenaceInsectExhaustion
            else:
                return Item.GeneralInsectExhaustion
            
        elif zoo_type == ZooType.Primate:
            if flux_type == Flux.Antiquity:
                return Item.AntiquityPrimateExhaustion
            elif flux_type == Flux.Amalgamy:
                return Item.AmalgamyPrimateExhaustion
            elif flux_type == Flux.Menace:
                return Item.MenacePrimateExhaustion
            else:
                return Item.GeneralPrimateExhaustion

        else:
            if flux_type == Flux.Antiquity:
                return Item.AntiquityGeneralExhaustion
            elif flux_type == Flux.Amalgamy:
                return Item.AmalgamyGeneralExhaustion
            elif flux_type == Flux.Menace:
                return Item.MenaceGeneralExhaustion
            else:
                return Item.GenericBoneMarketExhaustion

    suspicion_multiplier = 0.85

class AuthorOfGothicTales(Buyer):
    def __init__(self):
        super().__init__("An Author of Gothic Tales", 75)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.HinterlandScrip: 5 + (skeleton.echo_value * 2 * multi) 
        }
    
    def secondary_payout(self, flux, zoo_type, skeleton: Bone):
        menace_bonus = 0.5 if flux == Flux.Menace else 0
        antiquity_bonus = 0.5 if flux == Flux.Antiquity else 0
        exhaustion_type = self.match_exhaustion_type(zoo_type, flux)
        qty = (skeleton.antiquity + menace_bonus) * (skeleton.menace + antiquity_bonus)
        exhaution = math.floor(skeleton.antiquity * skeleton.menace * 0.05)

        return {
            exhaustion_type: exhaution,
            Item.CarvedBallOfStygianIvory: qty,
        }

class ZailorWithParticularInterests(Buyer):
    def __init__(self):
        super().__init__("A Zailor with Particular Interests", 75)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.NoduleOfWarmAmber: 25 + (skeleton.echo_value * 10 * multi) 
        }
    
    def secondary_payout(self, flux, zoo_type, skeleton: Bone):
        amalgamy_bonus = 0.5 if flux == Flux.Amalgamy else 0
        antiquity_bonus = 0.5 if flux == Flux.Antiquity else 0
        exhaustion_type = self.match_exhaustion_type(zoo_type, flux)
        qty = (skeleton.antiquity + amalgamy_bonus) * (skeleton.amalgamy + antiquity_bonus)
        exhaution = math.floor(skeleton.antiquity * skeleton.amalgamy * 0.05)

        return {
            exhaustion_type: exhaution,
            Item.KnobOfScintillack: qty,
        }

class RubberyCollector(Buyer):
    def __init__(self):
        super().__init__("A Rubbery Collector", 75)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.NightsoilOfTheBazaar: 5 + (skeleton.echo_value * 2 * multi) 
        }
    
    def secondary_payout(self, flux, zoo_type, skeleton: Bone):
        amalgamy_bonus = 0.5 if flux == Flux.Amalgamy else 0
        menace_bonus = 0.5 if flux == Flux.Menace else 0
        exhaustion_type = self.match_exhaustion_type(zoo_type, flux)
        qty = (skeleton.menace + amalgamy_bonus) * (skeleton.amalgamy + menace_bonus)
        exhaution = math.floor(skeleton.menace * skeleton.amalgamy * 0.05)

        return {
            exhaustion_type: exhaution,
            Item.BasketOfRubberyPies: qty,
        }

class Constable(Buyer):
    def __init__(self):
        super().__init__("A Constable", 50)
        self.suspicion_on_failure = 3

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.HinterlandScrip: 20 + (skeleton.echo_value * 2 * multi)
        }
    
class TheologianOfTheOldSchool(Buyer):
    def __init__(self):
        super().__init__("A Theologian of the Old School", 50)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.CrateOfIncorruptibleBiscuits: 4 + (skeleton.echo_value * 1/2.5 * multi)
        }    

class TellerOfTerrors(Buyer):
    def __init__(self):
        super().__init__("A Teller of Terrors", 75)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.BottelofMorelways1872: 25 + (skeleton.echo_value * 10 * multi) 
        }
    
    def secondary_payout(self, flux, zoo_type, skeleton: Bone):
        exhaustion_type = self.match_exhaustion_type(zoo_type, flux)
        exhaution = math.floor((skeleton.menace ** 2)/25)

        exponent = 2.1 if flux == Flux.Menace else 2.0
        qty = 4 * skeleton.menace ** exponent 

        return {
            exhaustion_type: exhaution,
            Item.RoyalBlueFeather: qty,
        }    

class TentacledEntrepreneur(Buyer):
    def __init__(self):
        super().__init__("A Tentacled Entrepreneur", 75)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.MemoryOfDistantShores: 5 + (skeleton.echo_value * 2 * multi) 
        }
    
    def secondary_payout(self, flux, zoo_type, skeleton: Bone):
        exhaustion_type = self.match_exhaustion_type(zoo_type, flux)
        exhaution = math.floor((skeleton.amalgamy ** 2)/25)

        exponent = 2.1 if flux == Flux.Amalgamy else 2.0
        qty = 4 * skeleton.amalgamy ** exponent 

        return {
            exhaustion_type: exhaution,
            Item.FinalBreath: qty,
        }    

class InvestmedMindedAmbassador(Buyer):
    def __init__(self):
        super().__init__("An Investment-minded Ambassador", 75)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.MemoryOfLight: 5 + (skeleton.echo_value * 2 * multi) 
        }
    
    def secondary_payout(self, flux, zoo_type, skeleton: Bone):
        exhaustion_type = self.match_exhaustion_type(zoo_type, flux)
        exhaution = math.floor((skeleton.antiquity ** 2)/25)

        exponent = 2.1 if flux == Flux.Antiquity else 2.0
        qty = 0.8 * skeleton.antiquity ** exponent 

        return {
            exhaustion_type: exhaution,
            Item.TailfeatherBrilliantAsFlame: qty,
        }    

class HoardingPalaeontologist(Buyer):
    def __init__(self):
        super().__init__("A Palaeontologist with Hoarding Propensities", 40)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.UnearthlyFossil: 2,
            Item.BoneFragments: 5 + (skeleton.echo_value * 100 * multi) 
        }

class NaiveCollector(Buyer):
    def __init__(self):
        super().__init__("A Naive Collector", 40)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.ThirstyBombazineScrap: (skeleton.echo_value * multi) / 2.5 
        }

class BohemianSculptress(Buyer):
    def __init__(self):
        super().__init__("A Familiar Bohemian Sculptress", 50)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        multi = self.zoo_multiplier(zoo_type)
        return {
            Item.PreservedSurfaceBlooms: 4 + (skeleton.echo_value * 1/2.5 * multi)
        }
    
    def secondary_payout(self, flux, zoo_type, skeleton: Bone):
        qty = skeleton.theology
        return {
            Item.RumourOfTheUpperRiver: qty
        }

# - many variants
# - weekly quality not tied to normal bone market, but does share exhaustion
# - actually nvm this guy sucks don't bother
class TriflingDiplomatTripleQuality(Buyer):
    def __init__(self):
        super().__init__("The Trifling Diplomat", 50)

    def primary_payout(self, flux, zoo_type, skeleton: Bone):
        return {
            Item.AssortmentOfKhaganianCoinage: 1 + (skeleton.echo_value * 2)
        }
    
    def secondary_payout(self, flux, zoo_type, skeleton: Bone):
        sum_quals = skeleton.antiquity + skeleton.amalgamy + skeleton.menace
        payout = (sum_quals/3) ** 2.2

        # TODO
        # exhaustion_type = self.match_exhaustion_type(zoo_type, flux)
        exhaustion = math.floor(((sum_quals / 3) ** 2.2) / 100)
        return {
            Item.CompromisingDocument: payout,
            Item.GenericBoneMarketExhaustion: exhaustion
        }
