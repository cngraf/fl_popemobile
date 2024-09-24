import math
from enum import Enum, auto

from enums import *
import utils
from config import Config
from player import Player

class Flux(Enum):
    NoQuality = 0
    Antiquity = auto()
    Amalgamy = auto()
    Menace = auto()

class ZooType(Enum):
    NoType = auto()
    Chimera = auto()
    Humanoid = auto()
    Ape = auto()
    Moneky = auto()
    Bird = auto()
    Amphibian = auto()
    Reptile = auto()
    Fish = auto()
    Insect = auto()
    Spider = auto()
    Curator = auto()
    Primate = auto()

class Bone():
    def __init__(self,
                 item: Item,
                 echo_value: int,
                 anitquity: int = 0,
                 amalgamy: int = 0,
                 menace: int = 0,
                 theology: int = 0,
                 implausibility: int = 0,
                 skulls: int = 0,
                 addtl_costs: dict = {}):
        self.item = item
        self.echo_value = echo_value
        self.antiquity = anitquity
        self.amalgamy = amalgamy
        self.menace = menace
        self.theology = theology
        self.implausibility = implausibility
        self.skulls = skulls
        self.addtl_costs = addtl_costs

def bone_table():
    dictionary = {}
    for bone in (
        Bone(Item.HeadlessSkeleton, 2.50),
        Bone(Item.ASkeletonOfYourOwn, 2.50),
        Bone(Item.HumanRibcage, 12.50),
        Bone(Item.ThornedRibcage, 12.50, amalgamy=1, menace=1),
        Bone(Item.SegmentedRibcage, 2.50),
        Bone(Item.SkeletonWithSevenNecks, 62.5, amalgamy=2, menace=1),
        Bone(Item.FlourishingRibcage, 12.5, amalgamy=2),
        Bone(Item.MammothRibcage, 62.5, anitquity=2),
        Bone(Item.RibcageWithABoutiqueOfEightSpines, 312.5, amalgamy=1,menace=2),
        Bone(Item.LeviathanFrame, 312.5, anitquity=1, menace=1),
        Bone(Item.PrismaticFrame, 312.5, anitquity=2, amalgamy=2),
        Bone(Item.FivePointedRibcage, 312.5, amalgamy=2, menace=1),

        Bone(Item.VictimsSkull, 2.5, skulls=1),
        Bone(Item.CarvedBallOfStygianIvory, 2.5),
        Bone(Item.RubberySkull, 6, amalgamy=1, skulls=1),
        Bone(Item.HornedSkull, 12.5, anitquity=1, menace=2, skulls=1),
        Bone(Item.PentagrammicSkull, 12.5, amalgamy=2, menace=2, skulls=1),
        Bone(Item.DuplicatedCounterfeitHeadOfJohnTheBaptist, 12.5, theology=1, skulls=1),
        Bone(Item.SkullInCoral, 17.5, amalgamy=2, skulls=1, addtl_costs={Item.KnobOfScintillack: -1}),
        Bone(Item.PlatedSkull, 25, menace=2, skulls=1),
        Bone(Item.EyelessSkull, 30, menace=2, skulls=1),
        Bone(Item.DoubledSkull, 30, anitquity=2, amalgamy=1, skulls=2),
        Bone(Item.SabreToothedSkull, 62.5, anitquity=1, menace=1, skulls=1),
        Bone(Item.BrightBrassSkull, 65, implausibility=2, skulls=1, addtl_costs={Item.NevercoldBrassSliver: -200}),
        Bone(Item.DuplicatedVakeSkull, 65, menace=3, skulls=1),

        Bone(Item.FailedStygianIvorySkull, 2.5, implausibility=2, skulls=1),
        Bone(Item.FailedHornedSkull, 12.5, anitquity=1, menace=1, skulls=1),
        Bone(Item.FailedPentagrammaticSkull, 12.5, amalgamy=1, menace=1, skulls=1),
        Bone(Item.FailedSkullInCoral, 17.5, amalgamy=1, implausibility=1, skulls=1, addtl_costs={Item.KnobOfScintillack: -1}),
        Bone(Item.FailedPlatedSkull, 25, menace=1, skulls=1),
        Bone(Item.FailedDoubledSkull, 30, anitquity=1, amalgamy=1, skulls=2),
        Bone(Item.FailedSabreToothedSkull, 30, anitquity=1, skulls=1),
        Bone(Item.FailedBrightBrassSkull, 65, implausibility=6, skulls=1),

        Bone(Item.CrustaceanPincer, 0, menace=1),
        Bone(Item.KnottedHumerus, 3, amalgamy=1),
        Bone(Item.HumanArm, 2.5, menace=-1),
        Bone(Item.IvoryHumerus, 15),
        Bone(Item.FossilisedForelimb, 27.5, anitquity=2),
        Bone(Item.FemurOfASurfaceDeer, 0.1, menace=-1),
        Bone(Item.UnidentifiedThighbone, 1),
        Bone(Item.FemurOfAJurassicBeast, 3, anitquity=1),
        Bone(Item.HelicalThighbone, 3, amalgamy=2),
        Bone(Item.HolyRelicOfTheThighOfStFiacre, 12.5),
        Bone(Item.IvoryFemur, 65),

        Bone(Item.FailedKnottedHumerus, 0.1, amalgamy=1, implausibility=2),
        Bone(Item.FailedFossilisedForelimb, 27.5, anitquity=1),
        Bone(Item.FailedIvoryHumerus, 15, implausibility=2),
        Bone(Item.FailedFemurOfAJurassicBeast, 3, anitquity=1, implausibility=2),
        Bone(Item.FailedHelicalThighbone, 3, amalgamy=1),
        Bone(Item.FailedHolyRelicOfTheThighOfStFiacre, 12.5, implausibility=2),
        Bone(Item.FailedIvoryFemur, 65, implausibility=4),        

        Bone(Item.BatWing, 0.01, menace=-1),
        Bone(Item.WingOfAYoungTerrorBird, 2.5, anitquity=1, menace=1),
        Bone(Item.AlbatrossWing, 12.5, amalgamy=1),
        Bone(Item.FinBonesCollected, 0.5),
        Bone(Item.AmberCrustedFin, 15, amalgamy=1, menace=1),

        Bone(Item.FailedBatWing, 0.01, menace=-1, implausibility=2),
        Bone(Item.FailedWingOfAYoungTerrorBird, 2.5, anitquity=1, menace=1, implausibility=2),
        Bone(Item.FailedAlbatrossWing, 12.5, amalgamy=1, implausibility=2), # TODO: confirm
        Bone(Item.FailedFinBonesCollected, 0.5, implausibility=2),
        Bone(Item.FailedAmberCrustedFin, 15, amalgamy=1, implausibility=2),

        Bone(Item.WitheredTentacle, 2.5, anitquity=-1),
        Bone(Item.JetBlackStinger, 2.5, menace=2),
        Bone(Item.PlasterTailBones, 2.5, implausibility=1),
        Bone(Item.TombLionsTail, 2.5, anitquity=1),
        Bone(Item.ObsidianChitinTail, 5, amalgamy=1),

        Bone(Item.FailedWitheredTentacleLimb, 0.5, anitquity=-1, implausibility=1),
        Bone(Item.FailedWitheredTentacleTail, 2.5, anitquity=-1, implausibility=2),
        Bone(Item.FailedJetBlackStinger, 2.5, menace=1),
        Bone(Item.FailedPlasterTailBones, 2.5, implausibility=4),
        Bone(Item.FailedTombLionsTail, 2.5),
        Bone(Item.FailedObsidianChitinTail, 5),

        # TODO: modifications
        # Bone(Item.FourMoreJoints, 0, amalgamy=2),
    ):
        dictionary[bone.item] = bone

    return dictionary

# class Skeleton():
#     def __init__(self,
#                  zooType: ZooType,
#                  recipe: dict):
#         self.zooType = zooType
#         self.recipe = recipe
#         self.bone_totals = create_skeleton(recipe)

# bleh should just make a Skeleton class
def create_skeleton(recipe: dict):
    bones = bone_table()

    result = Bone(Item.Placeholder, 0, addtl_costs= {})

    for item, quantity in recipe.items():
        count = abs(quantity)
        if item in bones:
            bone: Bone = bones[item]
            result.echo_value += bone.echo_value * count
            result.antiquity += bone.antiquity * count
            result.amalgamy += bone.amalgamy * count
            result.menace += bone.menace * count
            result.theology += bone.theology * count
            result.skulls += bone.skulls * count
            result.implausibility += bone.implausibility * count
            for i in range(0, count):
                result.addtl_costs = utils.sum_dicts(result.addtl_costs, bone.addtl_costs)

    if (Item.DuplicatedVakeSkull in recipe):
        count = abs(recipe[Item.DuplicatedVakeSkull])

        for i in range(0, count):
            # each addtl skull is worth 5 less than previous
            result.echo_value -= 5 * i

            # each addtl skull worth 1 less menace, min 1
            result.menace -= min(i, 2)

            # TODO: check formula for OBO. first point at 3rd, or 4th?
            result.implausibility += math.floor(i/2)

    if (Item.HolyRelicOfTheThighOfStFiacre in recipe):
        count = abs(recipe[Item.HolyRelicOfTheThighOfStFiacre])
        theology = 0

        if Item.FivePointedRibcage in recipe:
            theology = 7
        elif Item.PrismaticFrame in recipe:
            theology = 6
        elif Item.LeviathanFrame in recipe:
            theology = 6
        elif Item.RibcageWithABoutiqueOfEightSpines in recipe:
            theology = 5
        elif Item.MammothRibcage in recipe:
            theology = 4
        elif Item.SegmentedRibcage in recipe:
            theology = 3
        elif Item.FlourishingRibcage in recipe:
            theology = 3
        elif Item.SkeletonWithSevenNecks in recipe:
            theology = 2
        elif Item.ThornedRibcage in recipe:
            theology = 2
        elif Item.HumanRibcage in recipe:
            theology = 1
        elif Item.HeadlessSkeleton in recipe:
            theology = 1

        result.theology += count * theology

    return result

def bohemian_sculptress_payout(skeleton: Bone, zoo_multi: float = 1.0):
    if skeleton.antiquity > 0:
        return {}
    else:
        return {
            Item.PreservedSurfaceBlooms: 4 + (skeleton.echo_value * zoo_multi / 2.5),
            Item.RumourOfTheUpperRiver: skeleton.theology
        }

def zoo_multiplier(skeletonType = ZooType):
    if skeletonType in (ZooType.Bird, ZooType.Amphibian, ZooType.Reptile, ZooType.Primate):
        return 1.1
    if skeletonType in (ZooType.Fish, ZooType.Insect, ZooType.Spider):
        return 1.15
    else:
        return 1.0
    
def match_action_type(zoo_type, flux_type):
    if zoo_type == ZooType.Reptile:
        if flux_type == Flux.Antiquity:
            return Item.AntiquityReptileAction
        elif flux_type == Flux.Amalgamy:
            return Item.AmalgamyReptileAction
        elif flux_type == Flux.Menace:
            return Item.MenaceReptileAction
        else:
            return Item.GeneralReptileAction
    
    elif zoo_type == ZooType.Amphibian:
        if flux_type == Flux.Antiquity:
            return Item.AntiquityAmphibianAction
        elif flux_type == Flux.Amalgamy:
            return Item.AmalgamyAmphibianAction
        elif flux_type == Flux.Menace:
            return Item.MenaceAmphibianAction
        else:
            return Item.GeneralAmphibianAction        

    elif zoo_type == ZooType.Bird:
        if flux_type == Flux.Antiquity:
            return Item.AntiquityBirdAction
        elif flux_type == Flux.Amalgamy:
            return Item.AmalgamyBirdAction
        elif flux_type == Flux.Menace:
            return Item.MenaceBirdAction
        else:
            return Item.GeneralBirdAction
        
    elif zoo_type == ZooType.Fish:
        if flux_type == Flux.Antiquity:
            return Item.AntiquityFishAction
        elif flux_type == Flux.Amalgamy:
            return Item.AmalgamyFishAction
        elif flux_type == Flux.Menace:
            return Item.MenaceFishAction
        else:
            return Item.GeneralFishAction        

    elif zoo_type == ZooType.Spider:
        if flux_type == Flux.Antiquity:
            return Item.AntiquityArachnidAction
        elif flux_type == Flux.Amalgamy:
            return Item.AmalgamyArachnidAction
        elif flux_type == Flux.Menace:
            return Item.MenaceArachnidAction
        else:
            return Item.GeneralArachnidAction        

    elif zoo_type == ZooType.Insect:
        if flux_type == Flux.Antiquity:
            return Item.AntiquityInsectAction
        elif flux_type == Flux.Amalgamy:
            return Item.AmalgamyInsectAction
        elif flux_type == Flux.Menace:
            return Item.MenaceInsectAction
        else:
            return Item.GeneralInsectAction
        
    elif zoo_type == ZooType.Primate:
        if flux_type == Flux.Antiquity:
            return Item.AntiquityPrimateAction
        elif flux_type == Flux.Amalgamy:
            return Item.AmalgamyPrimateAction
        elif flux_type == Flux.Menace:
            return Item.MenacePrimateAction
        else:
            return Item.GeneralPrimateAction

    else:
        if flux_type == Flux.Antiquity:
            return Item.AntiquityGeneralAction
        elif flux_type == Flux.Amalgamy:
            return Item.AmalgamyGeneralAction
        elif flux_type == Flux.Menace:
            return Item.MenaceGeneralAction
        else:
            return Item._NoItem # HACK

def reverse_match_action_type(item):
    # Check for Reptile actions
    if item == Item.AntiquityReptileAction:
        return ZooType.Reptile, Flux.Antiquity
    elif item == Item.AmalgamyReptileAction:
        return ZooType.Reptile, Flux.Amalgamy
    elif item == Item.MenaceReptileAction:
        return ZooType.Reptile, Flux.Menace
    elif item == Item.GeneralReptileAction:
        return ZooType.Reptile, Flux.NoQuality
    
    # Check for Amphibian actions
    elif item == Item.AntiquityAmphibianAction:
        return ZooType.Amphibian, Flux.Antiquity
    elif item == Item.AmalgamyAmphibianAction:
        return ZooType.Amphibian, Flux.Amalgamy
    elif item == Item.MenaceAmphibianAction:
        return ZooType.Amphibian, Flux.Menace
    elif item == Item.GeneralAmphibianAction:
        return ZooType.Amphibian, Flux.NoQuality

    # Check for Bird actions
    elif item == Item.AntiquityBirdAction:
        return ZooType.Bird, Flux.Antiquity
    elif item == Item.AmalgamyBirdAction:
        return ZooType.Bird, Flux.Amalgamy
    elif item == Item.MenaceBirdAction:
        return ZooType.Bird, Flux.Menace
    elif item == Item.GeneralBirdAction:
        return ZooType.Bird, Flux.NoQuality

    # Check for Fish actions
    elif item == Item.AntiquityFishAction:
        return ZooType.Fish, Flux.Antiquity
    elif item == Item.AmalgamyFishAction:
        return ZooType.Fish, Flux.Amalgamy
    elif item == Item.MenaceFishAction:
        return ZooType.Fish, Flux.Menace
    elif item == Item.GeneralFishAction:
        return ZooType.Fish, Flux.NoQuality

    # Check for Spider actions
    elif item == Item.AntiquityArachnidAction:
        return ZooType.Spider, Flux.Antiquity
    elif item == Item.AmalgamyArachnidAction:
        return ZooType.Spider, Flux.Amalgamy
    elif item == Item.MenaceArachnidAction:
        return ZooType.Spider, Flux.Menace
    elif item == Item.GeneralArachnidAction:
        return ZooType.Spider, Flux.NoQuality

    # Check for Insect actions
    elif item == Item.AntiquityInsectAction:
        return ZooType.Insect, Flux.Antiquity
    elif item == Item.AmalgamyInsectAction:
        return ZooType.Insect, Flux.Amalgamy
    elif item == Item.MenaceInsectAction:
        return ZooType.Insect, Flux.Menace
    elif item == Item.GeneralInsectAction:
        return ZooType.Insect, Flux.NoQuality

    # Check for Primate actions
    elif item == Item.AntiquityPrimateAction:
        return ZooType.Primate, Flux.Antiquity
    elif item == Item.AmalgamyPrimateAction:
        return ZooType.Primate, Flux.Amalgamy
    elif item == Item.MenacePrimateAction:
        return ZooType.Primate, Flux.Menace
    elif item == Item.GeneralPrimateAction:
        return ZooType.Primate, Flux.NoQuality

    # Check for General actions
    elif item == Item.AntiquityGeneralAction:
        return None, Flux.Antiquity
    elif item == Item.AmalgamyGeneralAction:
        return None, Flux.Amalgamy
    elif item == Item.MenaceGeneralAction:
        return None, Flux.Menace
    # elif item == Item._NoItem:
    #     return None, Fluctuations.NoQuality

    else:
        # raise ValueError(f"Unrecognized item: {item}")
        return ZooType.NoType, Flux.NoQuality


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
            return Item._NoItem # HACK

suspicion_multiplier = 0.85

class Buyer():
    def __init__(self, name, zoo_type: ZooType, flux: Flux, impl_dc: 0):
        self.name = name
        self.zoo_type = zoo_type
        self.flux = flux
        self.implausibility_dc = impl_dc

    def add_trade(self, config, recipe):
        weekly_action_type = match_action_type(self.zoo_type, self.flux)
        weekly_action_cost = {
            weekly_action_type: recipe[Item.Action]
        }

        skeleton = create_skeleton(recipe)
        primary = self.primary_payout(skeleton)
        secondary = self.secondary_payout(skeleton)

        failures = self.expected_failed_sell_attempts(config, skeleton)
        failure_penalty = {
            Item.Action: -1 * failures,
            weekly_action_type: -1 * failures,
             # TODO check if consistent for all buyers
            Item.Suspicion: 2 * suspicion_multiplier * failures
        }

        total = utils.sum_dicts(
            recipe,
            weekly_action_cost,
            skeleton.addtl_costs,
            primary,
            secondary,
            failure_penalty)
        config.add(total)

    def primary_payout(self, skeleton: Bone):
        return {}
    
    def secondary_payout(self, skeleton: Bone):
        return {}
    
    def expected_failed_sell_attempts(self, config: Config, skeleton: Bone):
        shadowy = config.player.stats[Stat.Shadowy]
        impl = skeleton.implausibility
        if self.zoo_type == ZooType.Chimera:
            impl += 3
        
        dc = self.implausibility_dc * (skeleton.implausibility)
    
        pass_rate = max(0.01, utils.broad_challenge_success_rate(shadowy, dc))
        return (1.0 / pass_rate) - 1
     

    @staticmethod
    def zoo_multiplier(skeletonType = ZooType):
        if skeletonType in (ZooType.Bird, ZooType.Amphibian, ZooType.Reptile, ZooType.Primate):
            return 1.1
        if skeletonType in (ZooType.Fish, ZooType.Insect, ZooType.Spider):
            return 1.15
        else:
            return 1.0


class AuthorOfGothicTales(Buyer):
    def __init__(self, zoo_type: ZooType, flux: Flux):
        super().__init__("An Author of Gothic Tales", zoo_type, flux, 75)

    def primary_payout(self, skeleton: Bone):
        multi = self.zoo_multiplier(self.zoo_type)
        return {
            Item.HinterlandScrip: 5 + (skeleton.echo_value * 2 * multi) 
        }
    
    def secondary_payout(self, skeleton: Bone):
        menace_bonus = 0.5 if self.flux == Flux.Menace else 0
        antiquity_bonus = 0.5 if self.flux == Flux.Antiquity else 0
        exhaustion_type = match_exhaustion_type(self.zoo_type, self.flux)
        qty = (skeleton.antiquity + menace_bonus) * (skeleton.menace + antiquity_bonus)
        exhaution = math.floor(skeleton.antiquity * skeleton.menace * 0.05)

        return {
            exhaustion_type: exhaution,
            Item.CarvedBallOfStygianIvory: qty,
        }

class ZailorWithParticularInterests(Buyer):
    def __init__(self, zoo_type: ZooType, flux: Flux):
        super().__init__("A Zailor with Particular Interests", zoo_type, flux, 75)

    def primary_payout(self, skeleton: Bone):
        multi = self.zoo_multiplier(self.zoo_type)
        return {
            Item.NoduleOfWarmAmber: 25 + (skeleton.echo_value * 10 * multi) 
        }
    
    def secondary_payout(self, skeleton: Bone):
        amalgamy_bonus = 0.5 if self.flux == Flux.Amalgamy else 0
        antiquity_bonus = 0.5 if self.flux == Flux.Antiquity else 0
        exhaustion_type = match_exhaustion_type(self.zoo_type, self.flux)
        qty = (skeleton.antiquity + amalgamy_bonus) * (skeleton.amalgamy + antiquity_bonus)
        exhaution = math.floor(skeleton.antiquity * skeleton.amalgamy * 0.05)

        return {
            exhaustion_type: exhaution,
            Item.KnobOfScintillack: qty,
        }

class RubberyCollector(Buyer):
    def __init__(self, zoo_type: ZooType, flux: Flux):
        super().__init__("A Rubbery Collector", zoo_type, flux, 75)

    def primary_payout(self, skeleton: Bone):
        multi = self.zoo_multiplier(self.zoo_type)
        return {
            Item.NightsoilOfTheBazaar: 5 + (skeleton.echo_value * 2 * multi) 
        }
    
    def secondary_payout(self, skeleton: Bone):
        amalgamy_bonus = 0.5 if self.flux == Flux.Amalgamy else 0
        menace_bonus = 0.5 if self.flux == Flux.Menace else 0
        exhaustion_type = match_exhaustion_type(self.zoo_type, self.flux)
        qty = (skeleton.menace + amalgamy_bonus) * (skeleton.amalgamy + menace_bonus)
        exhaution = math.floor(skeleton.menace * skeleton.amalgamy * 0.05)

        return {
            exhaustion_type: exhaution,
            Item.BasketOfRubberyPies: qty,
        }



def naive_collector_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Flux = Flux.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    zoo_multi = zoo_multiplier(zoo_type)

    payout = {
        Item.ThirstyBombazineScrap: (skeleton.echo_value * zoo_multi / 2.5),
    }

    avg_failures = expected_failed_sell_attempts(player,
                        skeleton,
                        zoo_type == ZooType.Chimera,
                        dc_per_point=25)
    
    action_type = match_action_type(zoo_type, fluctuations)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)
    trade(0, totals)

def bohemian_sculptress_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Flux = Flux.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    zoo_multi = zoo_multiplier(zoo_type)

    payout = {
        Item.PreservedSurfaceBlooms: 4 + (skeleton.echo_value * zoo_multi / 2.5),
        Item.RumourOfTheUpperRiver: skeleton.theology
    }

    avg_failures = expected_failed_sell_attempts(player,
                        skeleton,
                        zoo_type == ZooType.Chimera,
                        dc_per_point=50)
    
    action_type = match_action_type(zoo_type, fluctuations)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)
    trade(0, totals)


def hoarding_paleo_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Flux = Flux.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    zoo_multi = zoo_multiplier(zoo_type)

    payout = {
        Item.BoneFragments: 5 + (skeleton.echo_value * zoo_multi * 100),
        Item.UnearthlyFossil: 2
    }

    avg_failures = expected_failed_sell_attempts(player,
                        skeleton,
                        zoo_type == ZooType.Chimera,
                        dc_per_point=40)
    
    action_type = match_action_type(zoo_type, fluctuations)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)
    trade(0, totals)

exhaustion_hard_cap = 4

def tentacled_entrepreneur_trade(config,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Flux = Flux.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.amalgamy
    flux_power = 2.1 if fluctuations == Flux.Amalgamy else 2.0
    exhaustion = match_exhaustion_type(zoo_type, fluctuations)

    if prop_a >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor((prop_a ** 2)/25),
            Item.MemoryOfDistantShores: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.FinalBreath: 4 * (prop_a ** flux_power)
        }

    avg_failures = expected_failed_sell_attempts(config.player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -1 * avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return
    config.trade(0, totals)
 
def ambassador_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Flux = Flux.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.antiquity
    flux_power = 2.1 if fluctuations == Flux.Antiquity else 2.0
    exhaustion = match_exhaustion_type(zoo_type, fluctuations)

    if prop_a >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor((prop_a ** 2)/25),
            Item.MemoryOfLight: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.TailfeatherBrilliantAsFlame: 0.8 * (prop_a ** flux_power)
        }

    avg_failures = expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -1 * avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return
    trade(0, totals)

def teller_of_terrors_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Flux = Flux.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.menace
    flux_power = 2.1 if fluctuations == Flux.Menace else 2.0
    exhaustion = match_exhaustion_type(zoo_type, fluctuations)

    if prop_a >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor((prop_a ** 2)/25),
            Item.BottelofMorelways1872: 25 + (skeleton.echo_value * zoo_multi * 10),
            Item.RoyalBlueFeather: 4 * (prop_a ** flux_power)
        }

    avg_failures = expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -1 * avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return

    trade(0, totals)

def gothic_tales_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Flux = Flux.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.antiquity
    prop_b = skeleton.menace

    bonus_a = 0.5 if fluctuations == Flux.Antiquity else 0
    bonus_b = 0.5 if fluctuations == Flux.Menace else 0
    exhaustion = match_exhaustion_type(zoo_type, fluctuations)


    if prop_a >= 1 and prop_b >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor(prop_a * prop_b/20),
            Item.HinterlandScrip: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.CarvedBallOfStygianIvory: (prop_a + bonus_b) * (prop_b + bonus_a)
        }

    avg_failures = expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -1 * avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return

    trade(0, totals)

def zailor_particular_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Flux = Flux.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.antiquity
    prop_b = skeleton.amalgamy

    bonus_a = 0.5 if fluctuations == Flux.Antiquity else 0
    bonus_b = 0.5 if fluctuations == Flux.Amalgamy else 0

    exhaustion = match_exhaustion_type(zoo_type, fluctuations)

    if prop_a >= 1 and prop_b >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor(prop_a * prop_b/20),
            Item.NoduleOfWarmAmber: 25 + (skeleton.echo_value * zoo_multi * 10),
            Item.KnobOfScintillack: (prop_a + bonus_b) * (prop_b + bonus_a)
        }

    avg_failures = expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -1 * avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return

    trade(0, totals)

def rubbery_collector_trade(config,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Flux = Flux.NoQuality,
                       debug: bool = False):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.amalgamy
    prop_b = skeleton.menace

    bonus_a = 0.5 if fluctuations == Flux.Amalgamy else 0
    bonus_b = 0.5 if fluctuations == Flux.Menace else 0
    exhaustion = match_exhaustion_type(zoo_type, fluctuations)


    if prop_a >= 1 and prop_b >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor(prop_a * prop_b/20),
            Item.NightsoilOfTheBazaar: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.BasketOfRubberyPies: (prop_a + bonus_b) * (prop_b + bonus_a)
        }

    avg_failures = expected_failed_sell_attempts(config.player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -1 * avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    # if debug:
    #     print(payout)
    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return

    config.trade(0, totals)

def phantasist_amalgamy_trade(config: Config,
                                    recipe: dict,
                                    zoo_type: ZooType = ZooType.NoType):

    player = config.player
    payout = {}

    skeleton = create_skeleton(recipe)
    prop = skeleton.amalgamy
    imp = skeleton.implausibility
    exhaustion = match_exhaustion_type(zoo_type, flux_type=Flux.NoQuality)


    if prop >= 4 and imp >= 2:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor((imp * prop + 1)/20),
            Item.HinterlandScrip: 2 + (skeleton.echo_value * zoo_multi * 2),
            Item.SlimVolumeOfBazaarinePoetry: 1 + imp * prop
        }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return

    config.trade(0, totals)    

def phantasist_antiquity_trade(config: Config,
                                    recipe: dict,
                                    zoo_type: ZooType = ZooType.NoType):

    player = config.player
    payout = {}

    skeleton = create_skeleton(recipe)
    prop = skeleton.antiquity
    imp = skeleton.implausibility
    exhaustion = match_exhaustion_type(zoo_type, flux_type=Flux.NoQuality)

    if prop >= 4 and imp >= 2:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor((imp * prop + 1)/20),
            Item.MemoryOfLight: 2 + (skeleton.echo_value * zoo_multi * 2),
            Item.KnobOfScintillack: 1 + imp * prop
        }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return

    config.trade(0, totals)


def phantasist_menace_trade(config: Config,
                                    recipe: dict,
                                    zoo_type: ZooType = ZooType.NoType):

    player = config.player
    payout = {}

    skeleton = create_skeleton(recipe)
    prop = skeleton.menace
    imp = skeleton.implausibility
    exhaustion = match_exhaustion_type(zoo_type, flux_type=Flux.NoQuality)
 
    if prop >= 4 and imp >= 2:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor((imp * prop + 1)/20),
            Item.HinterlandScrip: 2 + (skeleton.echo_value * zoo_multi * 2),
            Item.CarvedBallOfStygianIvory: 1 + imp * prop
        }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return

    config.trade(0, totals)

def enthusiast_skulls_trade(config: Config,
                                    recipe: dict,
                                    zoo_type: ZooType = ZooType.NoType):

    player = config.player
    payout = {}

    skeleton = create_skeleton(recipe)
    skulls = skeleton.skulls
    exhaustion = match_exhaustion_type(zoo_type, flux_type=Flux.NoQuality)

    if skulls >= 2:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            exhaustion: math.floor(((skulls - 1) ** 1.8)/4),
            Item.PieceOfRostygold: (skeleton.echo_value * zoo_multi * 100),
            Item.VitalIntelligence: math.floor((skulls - 1) ** 1.8)
        }

    avg_failures = expected_failed_sell_attempts(player, skeleton,
                                                zoo_type == ZooType.Chimera,
                                                dc_per_point=60)
    action_type = match_action_type(zoo_type, Flux.NoQuality)

    failure_penalty = {
        Item.Action: -avg_failures,
        action_type: -1 * avg_failures,
        Item.Suspicion: 2 * avg_failures * suspicion_multiplier
    }

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, failure_penalty)
    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs)

    if (totals.get(exhaustion, 0) > exhaustion_hard_cap): return

    config.trade(0, totals)

def expected_failed_sell_attempts(player, skeleton: Bone, is_chimera: bool = False, dc_per_point: int = 75):
    imp = skeleton.implausibility
    if is_chimera:
        imp += 3
    challenge_dc = dc_per_point * (imp)
    
    pass_rate = utils.pass_rate(player, Stat.Shadowy, challenge_dc)
    return (1.0 / pass_rate) - 1

def add_trades(player: Player, config: Config):
    trade = config.trade

    bone_market_week_actions = {
        "Antiquity": {
            "Reptile": Item.AntiquityReptileAction,
            "Amphibian": Item.AntiquityAmphibianAction,
            "Bird": Item.AntiquityBirdAction,
            "Fish": Item.AntiquityFishAction,
            "Arachnid": Item.AntiquityArachnidAction,
            "Insect": Item.AntiquityInsectAction,
            "Primate": Item.AntiquityPrimateAction,
        },
        "Amalgamy": {
            "Reptile": Item.AmalgamyReptileAction,
            "Amphibian": Item.AmalgamyAmphibianAction,
            "Bird": Item.AmalgamyBirdAction,
            "Fish": Item.AmalgamyFishAction,
            "Arachnid": Item.AmalgamyArachnidAction,
            "Insect": Item.AmalgamyInsectAction,
            "Primate": Item.AmalgamyPrimateAction,
        },
        "Menace": {
            "Reptile": Item.MenaceReptileAction,
            "Amphibian": Item.MenaceAmphibianAction,
            "Bird": Item.MenaceBirdAction,
            "Fish": Item.MenaceFishAction,
            "Arachnid": Item.MenaceArachnidAction,
            "Insect": Item.MenaceInsectAction,
            "Primate": Item.MenacePrimateAction,
        }
    }

    max_bone_market_actions_per_week = 700 # HACK
    exhaustion_per_week = -4
    action_split = {
        Item._BoneMarketRotation: -1
    }

    for category, actions in bone_market_week_actions.items():
        for creature, action in actions.items():

            unique_weeks = 21 # 3 vibes * 7 zoo types

            action_split[action] = max_bone_market_actions_per_week/unique_weeks
            zoo_type, flux_type = reverse_match_action_type(action)
            exhaustion_type = match_exhaustion_type(zoo_type, flux_type)

            action_split[exhaustion_type] = exhaustion_per_week/unique_weeks
            # config.add({
            #     action: -1,
            #     Item.Action: 1
            # })

            if (category == "Amalgamy"):
                config.add({
                    action: -1,
                    Item.AmalgamyGeneralAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.AmalgamyGeneralExhaustion: exhaustion_per_week,
                })

            if (category == "Antiquity"):
                config.add({
                    action: -1,
                    Item.AntiquityGeneralAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.AntiquityGeneralExhaustion: exhaustion_per_week,
                })

            if (category == "Menace"):
                config.add({
                    action: -1,
                    Item.MenaceGeneralAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.MenaceGeneralExhaustion: exhaustion_per_week,
                })

            if (creature == "Amphibian"):
                config.add({
                    action: -1,
                    Item.GeneralAmphibianAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.GeneralAmphibianExhaustion: exhaustion_per_week,
                })

            if (creature == "Arachnid"):
                config.add({
                    action: -1,
                    Item.GeneralArachnidAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.GeneralArachnidExhaustion: exhaustion_per_week,
                })

            if (creature == "Bird"):
                config.add({
                    action: -1,
                    Item.GeneralBirdAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.GeneralBirdExhaustion: exhaustion_per_week,
                })

            if (creature == "Fish"):
                config.add({
                    action: -1,
                    Item.GeneralFishAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.GeneralFishExhaustion: exhaustion_per_week,
                })

            if (creature == "Insect"):
                config.add({
                    action: -1,
                    Item.GeneralInsectAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.GeneralInsectExhaustion: exhaustion_per_week,
                })

            if (creature == "Reptile"):
                config.add({
                    action: -1,
                    Item.GeneralReptileAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.GeneralReptileExhaustion: exhaustion_per_week,
                })

            if (creature == "Primate"):
                config.add({
                    action: -1,
                    Item.GeneralPrimateAction: 1,
                })

                config.add({
                    exhaustion_type: -exhaustion_per_week,
                    Item.GeneralPrimateExhaustion: exhaustion_per_week,
                })


    config.add(action_split)

    trade(0, {
        Item.HinterlandScrip: -2,
        Item.UnidentifiedThighbone: 1
    })

    trade(1, {
        Item.BoneFragments: -100,
        Item.NoduleOfWarmAmber: -25,
        Item.WingOfAYoungTerrorBird: 2
    })

    # trade(0, {
    #     Item.Echo: -62.5,
    #     Item.BrightBrassSkull: 1
    # })

    # Buy from patrons

    trade(1, {
        Item.HinterlandScrip: utils.challenge_ev(player.stats[Stat.Persuasive], 200, success= -120, failure= -125),
        Item.SabreToothedSkull: 1
    })

    trade(1 + utils.expected_failures(utils.broad_challenge_success_rate(player.stats[Stat.Persuasive], 210)), {
        Item.ParabolanOrangeApple: -1,
        Item.IvoryHumerus: 1
    })

    # Failed Items
    trade(0, { Item.CarvedBallOfStygianIvory: -1, Item.FailedStygianIvorySkull: 1 })
    trade(0, { Item.HornedSkull: -1, Item.FailedHornedSkull: 1 })
    trade(0, { Item.PentagrammicSkull: -1, Item.FailedPentagrammaticSkull: 1 })
    trade(0, { Item.SkullInCoral: -1, Item.FailedSkullInCoral: 1 })
    trade(0, { Item.PlatedSkull: -1, Item.FailedPlatedSkull: 1 })
    trade(0, { Item.DoubledSkull: -1, Item.FailedDoubledSkull: 1 })
    trade(0, { Item.SabreToothedSkull: -1, Item.FailedSabreToothedSkull: 1 })
    trade(0, { Item.BrightBrassSkull: -1, Item.FailedBrightBrassSkull: 1 })

    trade(0, { Item.KnottedHumerus: -1, Item.FailedKnottedHumerus: 1 })
    trade(0, { Item.FossilisedForelimb: -1, Item.FailedFossilisedForelimb: 1 })
    trade(0, { Item.IvoryHumerus: -1, Item.FailedIvoryHumerus: 1 })

    trade(0, { Item.FemurOfAJurassicBeast: -1, Item.FailedFemurOfAJurassicBeast: 1 })
    trade(0, { Item.HelicalThighbone: -1, Item.FailedHelicalThighbone: 1 })
    trade(0, { Item.HolyRelicOfTheThighOfStFiacre: -1, Item.FailedHolyRelicOfTheThighOfStFiacre: 1 })
    trade(0, { Item.IvoryFemur: -1, Item.FailedIvoryFemur: 1 })

    trade(0, { Item.BatWing: -1, Item.FailedBatWing: 1 })
    trade(0, { Item.WingOfAYoungTerrorBird: -1, Item.FailedWingOfAYoungTerrorBird: 1 })
    trade(0, { Item.AlbatrossWing: -1, Item.FailedAlbatrossWing: 1 })
    trade(0, { Item.FinBonesCollected: -1, Item.FailedFinBonesCollected: 1 })
    trade(0, { Item.AmberCrustedFin: -1, Item.FailedAmberCrustedFin: 1 })

    trade(0, { Item.JetBlackStinger: -1, Item.FailedJetBlackStinger: 1 })
    trade(0, { Item.ObsidianChitinTail: -1, Item.FailedObsidianChitinTail: 1 })
    trade(0, { Item.PlasterTailBones: -1, Item.FailedPlasterTailBones: 1 })
    trade(0, { Item.TombLionsTail: -1, Item.FailedTombLionsTail: 1 })

    trade(0, { Item.WitheredTentacle: -1, Item.FailedWitheredTentacleLimb: 1 })
    trade(0, { Item.WitheredTentacle: -1, Item.FailedWitheredTentacleTail: 1 })

    # -----------------
    # Sell To Patrons
    # ----------------

    trade(1, {
        Item.HumanRibcage: -1,
        Item.IncisiveObservation: 30
    })

    # Value estimates to hit 5.7 EPA
    # trade(0, {
    #     Item.SkeletonWithSevenNecks: -1,
    #     Item.Echo: 84
    # })
    # needs about 153 in profit per skeleton
    # 

    # # ----- Test

    # # Identify items that can be acquired profitably
    # for (item, data) in bone_table().items():
    #     blacklist = [
    #         # Infintite loop
    #         Item.BrightBrassSkull,
    #         Item.FailedBrightBrassSkull,
    #         Item.ASkeletonOfYourOwn,
    #         Item.VictimsSkull,
    #         # Item.CarvedBallOfStygianIvory,

    #         # # Profitable Tier 1
    #         # Item.DuplicatedCounterfeitHeadOfJohnTheBaptist,
    #         # Item.WingOfAYoungTerrorBird,
    #         # Item.FailedWingOfAYoungTerrorBird,

    #         # # Tier 2
    #         # Item.WitheredTentacle,
    #         # Item.FailedWitheredTentacleTail,

    #         # # Tier 3
    #         # Item.DuplicatedVakeSkull,
    #         # Item.HumanArm,
    #         # Item.UnidentifiedThighbone,
    #         # Item.PlasterTailBones,
    #         # Item.JetBlackStinger,
    #         # Item.FailedJetBlackStinger,

    #         # # Tier 4 - below TLC communing
    #         # Item.SkullInCoral,
    #         # Item.FailedSkullInCoral,

    #         # # Tier 5 - only with 1.15 zoo bonus
    #         # Item.AlbatrossWing,
    #         # Item.FailedAlbatrossWing,
    #         # Item.PlasterTailBones,
    #         # Item.FailedPlasterTailBones,
    #         # Item.HolyRelicOfTheThighOfStFiacre,
    #         # Item.FailedWitheredTentacleLimb,
    #         # Item.RibcageWithABoutiqueOfEightSpines
    #     ]
    #     if item in blacklist:
    #         pass
    #     else:
    #         # # sell freely
    #         trade(0, {
    #             item: -1,
    #             Item.Echo: data.echo_value * 1
    #         })

    #         # buy at cost
    #         # trade(0, {
    #         #     item: 1,
    #         #     Item.Echo: data.echo_value * -1.05
    #         # })

    # -------------------------
    # ------- Recipes ---------
    # -------------------------
    # TODO: Verify all outputs

    if (player.ambition == Ambition.BagALegend):
        # min 1 action is baked into recipes, this only adds for failure
        # ignores other failure costs bc lazy
        success_rate = utils.narrow_challenge_success_rate(player.stats[Stat.ArtisanOfTheRedScience], 5)
        failures = 1.0/success_rate - 1 if success_rate < 1.0 else 0
        trade(failures, {
            Item.BoneFragments: -6000,
            Item.DuplicatedVakeSkull: 1
        })

    if player.profession == Profession.Licentiate:
        trade(0, { Item.ASkeletonOfYourOwn: 1 })
        trade(0, { Item.VictimsSkull: 1 })

    trade(0, {
        Item.BoneFragments: -500,
        Item.HandPickedPeppercaps: -10,
        Item.DuplicatedCounterfeitHeadOfJohnTheBaptist: 1
    })

    # Break down 8 spine ribcage for parts + woesel
    trade(10, {
        Item.BrightBrassSkull: -8,
        Item.NevercoldBrassSliver: -1600,
        Item.BoneFragments: 52000
    })

    # Buyers
    
    gothic_chimera_menace = AuthorOfGothicTales(ZooType.Chimera, Flux.Menace)
    gothic_chimera_antiquity = AuthorOfGothicTales(ZooType.Chimera, Flux.Menace)
    gothic_fish_antiquity = AuthorOfGothicTales(ZooType.Fish, Flux.Menace)
    gothic_fish_menace = AuthorOfGothicTales(ZooType.Fish, Flux.Menace)

    zailor_fish_antiquity = ZailorWithParticularInterests(ZooType.Fish, Flux.Antiquity)
    zailor_fish_amalgamy = ZailorWithParticularInterests(ZooType.Fish, Flux.Amalgamy)

    rubbery_collector_fish_amalgamy = RubberyCollector(ZooType.Fish, Flux.Amalgamy)
    rubbery_collector_fish_menace = RubberyCollector(ZooType.Fish, Flux.Menace)
    
    # -------------------------------
    # ------ Leviathan Frame

    # # 3/0/6 sweet spot
    # gothic_tales_trade(trade, player,
    #     recipe={
    #         Item.Action: -6,
    #         Item.MenaceGeneralAction: -6,
    #         Item.LeviathanFrame: -1,
    #         Item.DuplicatedVakeSkull: -1,
    #         Item.WingOfAYoungTerrorBird: -2
    #     },
    #     zoo_type=ZooType.Chimera,
    #     fluctuations=Flux.Menace)

    for skull_type in (
        Item.BrightBrassSkull,
        Item.DuplicatedVakeSkull,
        Item.SabreToothedSkull,
        Item.PlatedSkull,
        Item.HornedSkull,
        Item.DoubledSkull,

        Item.FailedHornedSkull,
        Item.FailedSabreToothedSkull):

        chimera_levi_recipe = {
            Item.Action: -6,
            Item.LeviathanFrame: -1,
            skull_type: -1,
            Item.WingOfAYoungTerrorBird: -2
        }

        gothic_chimera_menace.add_trade(config, chimera_levi_recipe)
        gothic_chimera_antiquity.add_trade(config, chimera_levi_recipe)

        # # Chimera
        # gothic_tales_trade(trade, player, 
        #     recipe={
        #         Item.Action: -6,
        #         Item.AntiquityGeneralAction: -6,
        #         Item.LeviathanFrame: -1,
        #         skull_type: -1,
        #         Item.WingOfAYoungTerrorBird: -2
        #     },
        #     zoo_type=ZooType.Chimera,
        #     fluctuations=Flux.Antiquity)
        
        # gothic_tales_trade(trade, player, 
        #     recipe={
        #         Item.Action: -6,
        #         Item.MenaceGeneralAction: -6,
        #         Item.LeviathanFrame: -1,
        #         skull_type: -1,
        #         Item.WingOfAYoungTerrorBird: -2
        #     },
        #     zoo_type=ZooType.Chimera,
        #     fluctuations=Flux.Menace)   

        # Fish
        for i in range(0, 3):
            amber_fins = -1 * i
            fin_bones_collected = -2 -amber_fins

            levi_fish_recipe = {
                Item.Action: -6,
                Item.LeviathanFrame: -1,
                skull_type: -1,
                Item.AmberCrustedFin: amber_fins,
                Item.FinBonesCollected: fin_bones_collected                
            }

            ambassador_trade(trade, player,
                recipe={
                    Item.Action: -6,
                    Item.AntiquityFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Flux.Antiquity)

            tentacled_entrepreneur_trade(config,
                recipe={
                    Item.Action: -6,
                    Item.AmalgamyFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Flux.Amalgamy)
            
            teller_of_terrors_trade(trade, player,
                recipe={
                    Item.Action: -6,
                    Item.MenaceFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Flux.Menace)

            gothic_fish_antiquity.add_trade(config, levi_fish_recipe)
            gothic_fish_menace.add_trade(config, levi_fish_recipe)
            # gothic_tales_trade(trade, player,
            #     recipe={
            #         Item.Action: -6,
            #         Item.AntiquityFishAction: -6,
            #         Item.LeviathanFrame: -1,
            #         skull_type: -1,
            #         Item.AmberCrustedFin: amber_fins,
            #         Item.FinBonesCollected: fin_bones_collected
            #     },
            #     zoo_type=ZooType.Fish,
            #     fluctuations=Flux.Antiquity)            
                        
            # gothic_tales_trade(trade, player,
            #     recipe={
            #         Item.Action: -6,
            #         Item.MenaceFishAction: -6,
            #         Item.LeviathanFrame: -1,
            #         skull_type: -1,
            #         Item.AmberCrustedFin: amber_fins,
            #         Item.FinBonesCollected: fin_bones_collected
            #     },
            #     zoo_type=ZooType.Fish,
            #     fluctuations=Flux.Menace)            
            
            zailor_fish_antiquity.add_trade(config, levi_fish_recipe)
            zailor_fish_amalgamy.add_trade(config, levi_fish_recipe)

            # zailor_particular_trade(trade, player,
            #     recipe={
            #         Item.Action: -6,
            #         Item.AntiquityFishAction: -6,
            #         Item.LeviathanFrame: -1,
            #         skull_type: -1,
            #         Item.AmberCrustedFin: amber_fins,
            #         Item.FinBonesCollected: fin_bones_collected
            #     },
            #     zoo_type=ZooType.Fish,
            #     fluctuations=Flux.Antiquity)

            # zailor_particular_trade(trade, player,
            #     recipe={
            #         Item.Action: -6,
            #         Item.AmalgamyFishAction: -6,
            #         Item.LeviathanFrame: -1,
            #         skull_type: -1,
            #         Item.AmberCrustedFin: amber_fins,
            #         Item.FinBonesCollected: fin_bones_collected
            #     },
            #     zoo_type=ZooType.Fish,
            #     fluctuations=Flux.Amalgamy)
            
            rubbery_collector_fish_amalgamy.add_trade(config, levi_fish_recipe)
            rubbery_collector_fish_menace.add_trade(config, levi_fish_recipe)

            # rubbery_collector_trade(config,
            #     recipe={
            #         Item.Action: -6,
            #         Item.AmalgamyFishAction: -6,
            #         Item.LeviathanFrame: -1,
            #         skull_type: -1,
            #         Item.AmberCrustedFin: amber_fins,
            #         Item.FinBonesCollected: fin_bones_collected
            #     },
            #     zoo_type=ZooType.Fish,
            #     fluctuations=Flux.Amalgamy)         

            # rubbery_collector_trade(config,
            #     recipe={
            #         Item.Action: -6,
            #         Item.MenaceFishAction: -6,
            #         Item.LeviathanFrame: -1,
            #         skull_type: -1,
            #         Item.AmberCrustedFin: amber_fins,
            #         Item.FinBonesCollected: fin_bones_collected
            #     },
            #     zoo_type=ZooType.Fish,
            #     fluctuations=Flux.Menace)
            
            hoarding_paleo_trade(trade, player,
                recipe={
                    Item.Action: -6,
                    Item.GeneralFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Flux.NoQuality)


    # ----------------------
    # ---- Mammoth Ribcage

    for skull_type in (
        Item.VictimsSkull,
        Item.HornedSkull,
        Item.PentagrammicSkull,
        Item.DuplicatedCounterfeitHeadOfJohnTheBaptist,
        Item.SkullInCoral,
        Item.PlatedSkull,
        Item.EyelessSkull,
        Item.SabreToothedSkull,
        Item.BrightBrassSkull,
        Item.DuplicatedVakeSkull
    ):
        gothic_tales_trade(trade, player,
            recipe={
                Item.Action: -9,
                Item.AntiquityReptileAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -3,
                Item.HolyRelicOfTheThighOfStFiacre: -1,
                Item.JetBlackStinger: -1
            },
            zoo_type=ZooType.Reptile,
            fluctuations=Flux.Antiquity)
        
        gothic_tales_trade(trade, player,
            recipe={
                Item.Action: -9,
                Item.AntiquityReptileAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -3,
                Item.HolyRelicOfTheThighOfStFiacre: -1,
                Item.FailedJetBlackStinger: -1
            },
            zoo_type=ZooType.Reptile,
            fluctuations=Flux.Antiquity)        
        
        gothic_tales_trade(trade, player,
            recipe={
                Item.Action: -9,
                Item.MenaceReptileAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -3,
                Item.HolyRelicOfTheThighOfStFiacre: -1,
                Item.JetBlackStinger: -1
            },
            zoo_type=ZooType.Reptile,
            fluctuations=Flux.Menace)

        gothic_tales_trade(trade, player,
            recipe={
                Item.Action: -9,
                Item.MenaceReptileAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -3,
                Item.HolyRelicOfTheThighOfStFiacre: -1,
                Item.FailedJetBlackStinger: -1
            },
            zoo_type=ZooType.Reptile,
            fluctuations=Flux.Menace)           
           
        zailor_particular_trade(trade, player,
            recipe={
                Item.Action: -9,
                Item.AntiquityReptileAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -4,
                Item.ObsidianChitinTail: -1
            },
            zoo_type=ZooType.Reptile,
            fluctuations=Flux.Antiquity)
        
        zailor_particular_trade(trade, player,
            recipe={
                Item.Action: -9,
                Item.AmalgamyReptileAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -4,
                Item.ObsidianChitinTail: -1
            },
            zoo_type=ZooType.Reptile,
            fluctuations=Flux.Amalgamy)        

        zailor_particular_trade(trade, player,
            recipe={
                Item.Action: -9,
                Item.AntiquityAmphibianAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -4,
            },
            zoo_type=ZooType.Amphibian,
            fluctuations=Flux.Antiquity)
        
        zailor_particular_trade(trade, player,
            recipe={
                Item.Action: -9,
                Item.AntiquityAmphibianAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -1,
                Item.HelicalThighbone: -2,
                Item.HolyRelicOfTheThighOfStFiacre: -1
            },
            zoo_type=ZooType.Amphibian,
            fluctuations=Flux.Antiquity)
        
        zailor_particular_trade(trade, player,
            recipe={
                Item.Action: -9,
                Item.AmalgamyAmphibianAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -1,
                Item.HelicalThighbone: -2,
                Item.HolyRelicOfTheThighOfStFiacre: -1
            },
            zoo_type=ZooType.Amphibian,
            fluctuations=Flux.Amalgamy)                

    # trade(9, {
    #     Item.MammothRibcage: -1,
    #     Item.SabreToothedSkull: -1,
    #     Item.FemurOfAJurassicBeast: -3,
    #     Item.HolyRelicOfTheThighOfStFiacre: -1,
    #     Item.JetBlackStinger: -1,
    #     Item.HinterlandScrip: 299,
    #     Item.CarvedBallOfStygianIvory: 21
    # })

    # -------------------------------
    # ----- Human Ribcage -----------
    # -------------------------------

    # # 0/6/3 humanoid
    # trade(8, {
    #     Item.HumanRibcage: -1,
    #     Item.DuplicatedVakeSkull: -1,
    #     Item.KnottedHumerus: -2,
    #     Item.HelicalThighbone: -2,
    #     Item.NightsoilOfTheBazaar: 184,
    #     Item.BasketOfRubberyPies: 21,
    # })

    # trade(8, {
    #     Item.HumanRibcage: -1,
    #     Item.DuplicatedVakeSkull: -1,
    #     Item.FossilisedForelimb: -2,
    #     Item.FemurOfAJurassicBeast: -2,
    #     Item.NightsoilOfTheBazaar: utils.skelly_value_in_items(12.5 + 65 + (27.5 * 2) + (3 * 2), 0.5, False),
    #     Item.CarvedBallOfStygianIvory: 21,
    # })

    
    teller_of_terrors_trade(trade, player,
        recipe={
            Item.Action: -4,
            Item.GeneralPrimateAction: -4,
            Item.ASkeletonOfYourOwn: -1,
            Item.DuplicatedVakeSkull: -1
        },
        zoo_type=ZooType.Primate,
        fluctuations=Flux.NoQuality)

    gothic_tales_trade(trade, player,
        recipe={
            Item.Action: -8,
            Item.AntiquityGeneralAction: -8,
            Item.HumanRibcage: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.FossilisedForelimb: -1,
            Item.FailedFossilisedForelimb: -1,
            Item.FemurOfAJurassicBeast: -2
        },
        zoo_type=ZooType.Primate,
        fluctuations=Flux.Antiquity)
    
    # Exhaustion 1
    teller_of_terrors_trade(trade, player,
        recipe={
            Item.Action: -8,
            Item.MenaceGeneralAction: -8,
            Item.HumanRibcage: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.WingOfAYoungTerrorBird: -4,
        },
        zoo_type=ZooType.Chimera,
        fluctuations=Flux.Menace)    

    teller_of_terrors_trade(trade, player,
        recipe={
            Item.Action: -4,
            Item.MenacePrimateAction: -4,
            Item.ASkeletonOfYourOwn: -1,
            Item.DuplicatedVakeSkull: -1
        },
        zoo_type=ZooType.Primate,
        fluctuations=Flux.Menace)
    
    teller_of_terrors_trade(trade, player,
        recipe={
            Item.Action: -4,
            Item.ASkeletonOfYourOwn: -1,
            Item.DuplicatedVakeSkull: -1
        },
        zoo_type=ZooType.NoType,
        fluctuations=Flux.NoQuality)    
   
    teller_of_terrors_trade(trade, player,
        recipe={
            Item.Action: -4,
            Item.ASkeletonOfYourOwn: -1,
            Item.DuplicatedVakeSkull: -1
        },
        zoo_type=ZooType.NoType,
        fluctuations=Flux.Menace)
    
    teller_of_terrors_trade(trade, player,
        recipe={
            Item.Action: -4,
            Item.ASkeletonOfYourOwn: -1,
            Item.BrightBrassSkull: -1
        },
        zoo_type=ZooType.NoType,
        fluctuations=Flux.NoQuality)        

    # phantasist_menace_trade(trade, player,
    #     recipe={
    #         Item.HumanRibcage: -1,
    #         Item.FailedBrightBrassSkull: -1,

    #     },
    #     zoo_type=ZooType.Chimera)

    '''
    "Biblically Inaccurate Angel"
    AKA the reject ribcage recycler

    the filler limb can be any limb with 0 antiquity, menace, and implausibility
    '''

    for filler_limb in (
        Item.KnottedHumerus,
        Item.IvoryHumerus,
        Item.UnidentifiedThighbone,
        Item.HelicalThighbone,
        Item.HolyRelicOfTheThighOfStFiacre,
        Item.IvoryFemur,
        Item.AlbatrossWing,
        Item.FinBonesCollected
    ):
        
        for num_wings in range(0, 4):

            gothic_chimera_menace.add_trade(config, {
                    Item.Action: -8,
                    Item.HumanRibcage: -1,
                    Item.DuplicatedVakeSkull: -1,
                    Item.WingOfAYoungTerrorBird: -1 * num_wings,
                    filler_limb: -4 + num_wings                
            })

            gothic_tales_trade(trade, player,
                recipe={
                    Item.Action: -8,
                    Item.MenaceGeneralAction: -8,
                    Item.HumanRibcage: -1,
                    Item.DuplicatedVakeSkull: -1,
                    Item.WingOfAYoungTerrorBird: -1 * num_wings,
                    filler_limb: -4 + num_wings
                },
                zoo_type=ZooType.Chimera,
                fluctuations=Flux.Menace)
            
            gothic_tales_trade(trade, player,
                recipe={
                    Item.Action: -8,
                    Item.MenaceGeneralAction: -8,
                    Item.HumanRibcage: -1,
                    Item.HornedSkull: -1,
                    Item.WingOfAYoungTerrorBird: -1 * num_wings,
                    filler_limb: -4 + num_wings
                },
                zoo_type=ZooType.Chimera,
                fluctuations=Flux.Menace)
            
            gothic_tales_trade(trade, player,
                recipe={
                    Item.Action: -8,
                    Item.MenaceGeneralAction: -8,
                    Item.HumanRibcage: -1,
                    Item.SabreToothedSkull: -1,
                    Item.WingOfAYoungTerrorBird: -1 * num_wings,
                    filler_limb: -4 + num_wings
                },
                zoo_type=ZooType.Chimera,
                fluctuations=Flux.Menace)
                            
            gothic_tales_trade(trade, player,
                recipe={
                    Item.Action: -8,
                    Item.AntiquityGeneralAction: -8,
                    Item.HumanRibcage: -1,
                    Item.SabreToothedSkull: -1,
                    Item.WingOfAYoungTerrorBird: -1 * num_wings,
                    filler_limb: -4 + num_wings
                },
                zoo_type=ZooType.Chimera,
                fluctuations=Flux.Antiquity)

        # # # 3/?/6
        # # trade(7 + actions_to_sell_chimera, {
        # #     Item.HumanRibcage: -1,
        # #     Item.DuplicatedVakeSkull: -1,
        # #     Item.WingOfAYoungTerrorBird: -3,
        # #     filler_limb: -1,
        # #     Item.HinterlandScrip: 5 + utils.skelly_value_in_items(12.5 + 65 + (3 * 2.5) + filler_limb_echo_value, 0.5, False),
        # #     Item.CarvedBallOfStygianIvory: 21, # 20/18/21
        # # })

        # # 4/?/4
        # trade(7 + actions_to_sell_chimera, {
        #     Item.HumanRibcage: -1,
        #     Item.SabreToothedSkull: -1,
        #     Item.WingOfAYoungTerrorBird: -3,
        #     filler_limb: -1,
        #     Item.HinterlandScrip: 5 + utils.skelly_value_in_items(12.5 + 62.5 + (3 * 2.5) + filler_limb_echo_value, 0.5, False),
        #     Item.CarvedBallOfStygianIvory: 18, # 18/16/18
        # })

    # # 3/1/6
    # trade(7 + actions_to_sell_chimera, {
    #     Item.HumanRibcage: -1,
    #     Item.DuplicatedVakeSkull: -1,
    #     Item.FemurOfAJurassicBeast: -1,
    #     Item.WingOfAYoungTerrorBird: -2,
    #     Item.AmberCrustedFin: -1,
    #     Item.HinterlandScrip: 5+ utils.skelly_value_in_items(12.5 + 65 + 3 + (2 * 2.5) + 15, 0.5, False),
    #     Item.CarvedBallOfStygianIvory: 21, # 20/18/21
    # })

    # # 3/2/6
    # trade(7 + actions_to_sell_chimera, {
    #     Item.HumanRibcage: -1,
    #     Item.HornedSkull: -1,
    #     Item.WingOfAYoungTerrorBird: -2,
    #     Item.AmberCrustedFin: -2,
    #     Item.HinterlandScrip: 5 + utils.skelly_value_in_items(12.5 + 12.5 + (2 * 2.5) + (2 * 15), 0.5, False),
    #     Item.CarvedBallOfStygianIvory: 21 # 20/18/21,
    # })

    # ------------------------------------------------
    # ------ Skeleton with Seven Necks ---------------
    # ------------------------------------------------

    # gothic_tales_trade(trade, player,
    #     recipe = {
    #         Item.MenaceBirdAction: -12,
    #         Item.SkeletonWithSevenNecks: -1,
    #         Item.BrightBrassSkull: -5,
    #         Item.DuplicatedVakeSkull: -2,
    #         Item.WingOfAYoungTerrorBird: -2
    #     },
    #     zoo_type = ZooType.Bird,
    #     fluctuations= Fluctuations.Menace)
    
    # Generator Skeleton, various

    # Okay we want 3 imp, and 6 of either menace or antiquity
    # or 2 and 9

    # # 6 menace, 3 imp
    # phantasist_menace_trade(config,
    #     recipe={
    #         Item.GeneralBirdAction: -12,
    #         Item.SkeletonWithSevenNecks: -1,
    #         Item.FailedSkullInCoral: -1,
    #         Item.BrightBrassSkull: -1,
    #         Item.DuplicatedVakeSkull: -1,
    #         Item.DuplicatedCounterfeitHeadOfJohnTheBaptist: -4,
    #         Item.WingOfAYoungTerrorBird: -2
    #     },
    #     zoo_type=ZooType.Bird)
    
    # # 9 men, 2 imp
    # # actually not sure if this works
    # phantasist_menace_trade(config,
    #     recipe={
    #         Item.GeneralBirdAction: -12,
    #         Item.SkeletonWithSevenNecks: -1,
    #         Item.BrightBrassSkull: -1,
    #         Item.DuplicatedVakeSkull: -3,
    #         Item.DuplicatedCounterfeitHeadOfJohnTheBaptist: -3,
    #         Item.WingOfAYoungTerrorBird: -2
    #     },
    #     zoo_type=ZooType.Bird)
    
    # phantasist_menace_trade(config,
    #     recipe={
    #         Item.GeneralBirdAction: -12,
    #         Item.SkeletonWithSevenNecks: -1,
    #         Item.DuplicatedVakeSkull: -4,
    #         Item.DuplicatedCounterfeitHeadOfJohnTheBaptist: -3,
    #         Item.WingOfAYoungTerrorBird: -2
    #     },
    #     zoo_type=ZooType.Bird)

    # Exhaustion 4
    teller_of_terrors_trade(config.trade, config.player,
        recipe={
            Item.Action: -12,
            Item.MenaceBirdAction: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.HornedSkull: -2,
            Item.SabreToothedSkull: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.BrightBrassSkull: -3,
            Item.WingOfAYoungTerrorBird: -2
        },
        zoo_type=ZooType.Bird,
        fluctuations=Flux.Menace)

    # Exhaustion 4
    teller_of_terrors_trade(config.trade, config.player,
        recipe={
            Item.Action: -12,
            Item.MenaceBirdAction: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.HornedSkull: -2,
            Item.SabreToothedSkull: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.BrightBrassSkull: -3,
            Item.WingOfAYoungTerrorBird: -2
        },
        zoo_type=ZooType.NoType,
        fluctuations=Flux.Menace)


    rubbery_collector_trade(config,
        recipe={
            Item.Action: -12,
            Item.AmalgamyBirdAction: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.SkullInCoral: -7,
            Item.AlbatrossWing: -2
        },
        zoo_type=ZooType.Bird,
        fluctuations=Flux.Amalgamy, debug=True)
    
    rubbery_collector_trade(config,
        recipe={
            Item.Action: -16,
            Item.AmalgamyBirdAction: -16,
            Item.RibcageWithABoutiqueOfEightSpines: -1,
            Item.SkullInCoral: -8,
            Item.AlbatrossWing: -2,
            Item.FemurOfASurfaceDeer: -1,
            Item.UnidentifiedThighbone: -1,
            Item.WitheredTentacle: -1
        },
        zoo_type=ZooType.Bird,
        fluctuations=Flux.Amalgamy, debug=True)

    # Define the target sum
    seven_skulls = 7

    # Iterate over possible values
    for brass_skulls in range(seven_skulls + 1):
        other_skull_types = [
            Item.HornedSkull,
            Item.SkullInCoral,
            Item.SabreToothedSkull,
            Item.PlatedSkull,
            # Item.PentagrammicSkull, 
            Item.DuplicatedCounterfeitHeadOfJohnTheBaptist,
            Item.DuplicatedVakeSkull,
            Item.DoubledSkull,

            Item.FailedHornedSkull,
            Item.FailedSabreToothedSkull,
            Item.FailedDoubledSkull,
            Item.FailedSkullInCoral
        ]

        num_skull_types = len(other_skull_types)

        for i in range(0, num_skull_types):
            skull_type_1 = other_skull_types[i]
            
            for j in range(i + 1, num_skull_types):
                skull_type_2 = other_skull_types[j]

                # Iterate over possible values of b
                for num_skull_1 in range(seven_skulls + 1 - brass_skulls):

                    # Calculate the value of c
                    num_skull_2 = seven_skulls - brass_skulls - num_skull_1

                    # Memory of Distant Shores & Volumes of Collated Research
                    tentacled_entrepreneur_trade(config,
                        recipe={
                            Item.Action: -12,
                            Item.AmalgamyBirdAction: -12,
                            Item.SkeletonWithSevenNecks: -1,
                            Item.BrightBrassSkull: -1 * brass_skulls,
                            skull_type_1: -1 * num_skull_1,
                            skull_type_2: -1 * num_skull_2,
                            Item.AlbatrossWing: -2
                        },
                        zoo_type=ZooType.Bird,
                        fluctuations=Flux.Amalgamy)
                    
                    tentacled_entrepreneur_trade(config,
                        recipe={
                            Item.Action: -12,
                            Item.GeneralBirdAction: -12,
                            Item.SkeletonWithSevenNecks: -1,
                            Item.BrightBrassSkull: -1 * brass_skulls,
                            skull_type_1: -1 * num_skull_1,
                            skull_type_2: -1 * num_skull_2,
                            Item.WingOfAYoungTerrorBird: -2
                        },
                        zoo_type=ZooType.Bird,
                        fluctuations=Flux.NoQuality)            

                    # Bone Fragments
                    hoarding_paleo_trade(trade, player,
                        recipe={
                            Item.Action: -12,
                            Item.GeneralBirdAction: -12,
                            Item.SkeletonWithSevenNecks: -1,
                            Item.BrightBrassSkull: -1 * brass_skulls,
                            skull_type_1: -1 * num_skull_1,
                            skull_type_2: -1 * num_skull_2,
                            Item.WingOfAYoungTerrorBird: -2
                        },
                        zoo_type=ZooType.Bird,
                        fluctuations=Flux.NoQuality)                           

                    zailor_particular_trade(trade, player,
                        recipe={
                            Item.Action: -12,
                            Item.GeneralBirdAction: -12,
                            Item.SkeletonWithSevenNecks: -1,
                            Item.BrightBrassSkull: -1 * brass_skulls,
                            skull_type_1: -1 * num_skull_1,
                            skull_type_2: -1 * num_skull_2,
                            Item.WingOfAYoungTerrorBird: -2
                        },
                        zoo_type=ZooType.Bird,
                        fluctuations=Flux.NoQuality)


                    naive_collector_trade(trade, player,
                        recipe={
                            Item.Action: -12,
                            Item.GeneralBirdAction: -12,
                            Item.SkeletonWithSevenNecks: -1,
                            Item.BrightBrassSkull: -1 * brass_skulls,
                            skull_type_1: -1 * num_skull_1,
                            skull_type_2: -1 * num_skull_2,
                            Item.WingOfAYoungTerrorBird: -2
                        },
                        zoo_type=ZooType.Bird,
                        fluctuations=Flux.NoQuality)       


    # ------------------------------------------------
    # ------------ Thorned Ribcage ---------------
    # ------------------------------------------------

    # 6/3/3 recipe
    gothic_tales_trade(trade, player,
        recipe={
            Item.Action: -9,
            Item.AntiquityBirdAction: -9,
            Item.ThornedRibcage: -1,
            Item.DoubledSkull: -1,
            Item.FemurOfAJurassicBeast: -2,
            Item.WingOfAYoungTerrorBird: -2,
            Item.ObsidianChitinTail: -1
        },
        zoo_type=ZooType.Bird,
        fluctuations=Flux.Antiquity)
    
    zailor_particular_trade(trade, player,
        recipe={
            Item.Action: -9,
            Item.AntiquityBirdAction: -9,
            Item.ThornedRibcage: -1,
            Item.DoubledSkull: -1,
            Item.FemurOfAJurassicBeast: -2,
            Item.WingOfAYoungTerrorBird: -2,
            Item.ObsidianChitinTail: -1
        },
        zoo_type=ZooType.Bird,
        fluctuations=Flux.Antiquity)

    zailor_particular_trade(trade, player,
        recipe={
            Item.Action: -9,
            Item.AntiquityGeneralAction: -9,
            Item.ThornedRibcage: -1,
            Item.DoubledSkull: -1,
            Item.KnottedHumerus: -2,
            Item.HelicalThighbone: -1,
            Item.FinBonesCollected: -1,
            Item.TombLionsTail: -1
        },
        zoo_type=ZooType.Chimera,
        fluctuations=Flux.Antiquity)       

    # ------------------------------------------------
    # ------------ Segmented Ribcage -----------------
    # ------------------------------------------------

    # TODO: organize this
    # Random Stuff

    # # 4/0/4
    # trade(7 + actions_to_sell_chimera, {
    #     Item.HumanRibcage: -1,
    #     Item.HornedSkull: -1,
    #     Item.WingOfAYoungTerrorBird: -3,
    #     Item.HumanArm: -1,
    #     Item.HinterlandScrip: 5 + utils.skelly_value_in_items(12.5 + 12.5 + (3 * 2.5) + 2.5, 0.5, False),
    #     Item.CarvedBallOfStygianIvory: 18 # 18/16/18,
    # })

    #     # trade(8, {
    #     #     Item.ThornedRibcage
    #     # })

    # # counter-church
    # # not verified

    # trade(12, {
    #     Item.FlourishingRibcage: -1,
    #     Item.DuplicatedCounterfeitHeadOfJohnTheBaptist: -2,
    #     Item.HolyRelicOfTheThighOfStFiacre: -6,

    #     Item.PreservedSurfaceBlooms: 49,
    #     Item.RumourOfTheUpperRiver: 20
    # })

    # trade(14, {
    #     Item.SegmentedRibcage: -3,
    #     Item.HolyRelicOfTheThighOfStFiacre: -8,
    #     Item.WitheredTentacle: -1,

    #     Item.PreservedSurfaceBlooms: 52,
    #     Item.RumourOfTheUpperRiver: 24
    # })

    # hack for testing
    # trade(29, {
    #     # Item.Echo: -60,
    #     Item.GlimEncrustedCarapace: 1
    # })

    # TODO require spider week
    trade(0, {
        Item.Action: -11,
        Item.GeneralArachnidAction: -11,
        Item.GlimEncrustedCarapace: -1,
        Item.HolyRelicOfTheThighOfStFiacre: -8,

        Item.PreservedSurfaceBlooms: 78,
        Item.RumourOfTheUpperRiver: 40
    })

    # trade(0, {
    #     Item.Echo: -312.5,
    #     Item.PrismaticFrame: 1
    # })

    # # might be 11 actions? declare no more tails?
    # trade(10, {
    #     Item.PrismaticFrame: -1,
    #     Item.SabreToothedSkull: -1,
    #     Item.CarvedBallOfStygianIvory: -2,
    #     Item.AmberCrustedFin: -3,
    #     Item.JetBlackStinger: -1,

    #     Item.HinterlandScrip: 84,
    #     Item.CarvedBallOfStygianIvory: 20
    # })

    gothic_tales_trade(trade, player,
        recipe={
            Item.Action: -11,
            Item.AntiquityFishAction: -11, # might be 10?
            Item.PrismaticFrame: -1,
            Item.SabreToothedSkull: -1,
            Item.CarvedBallOfStygianIvory: -2,
            Item.AmberCrustedFin: -3,
            Item.JetBlackStinger: -1,
        },
        zoo_type=ZooType.Fish,
        fluctuations=Flux.Antiquity)
    
    gothic_tales_trade(trade, player,
        recipe={
            Item.Action: -11,
            Item.MenaceFishAction: -11,
            Item.PrismaticFrame: -1,
            Item.SabreToothedSkull: -1,
            Item.CarvedBallOfStygianIvory: -2,
            Item.AmberCrustedFin: -3,
            Item.JetBlackStinger: -1,
        },
        zoo_type=ZooType.Fish,
        fluctuations=Flux.Menace)
    
    gothic_tales_trade(trade, player,
        recipe={
            Item.Action: -11,
            Item.MenaceFishAction: -11,
            Item.PrismaticFrame: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.CarvedBallOfStygianIvory: -2,
            Item.FinBonesCollected: -3,
            Item.JetBlackStinger: -1,
        },
        zoo_type=ZooType.Fish,
        fluctuations=Flux.Menace)     
    
    rubbery_collector_trade(config,
        recipe={
            Item.Action: -11,
            Item.MenaceFishAction: -11,
            Item.PrismaticFrame: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.CarvedBallOfStygianIvory: -2,
            Item.FinBonesCollected: -3,
            Item.JetBlackStinger: -1,
        },
        zoo_type=ZooType.Fish,
        fluctuations=Flux.Menace)         

    gothic_tales_trade(trade, player,
        recipe={
            Item.Action: -11,
            Item.GeneralFishAction: -11,
            Item.PrismaticFrame: -1,
            Item.SabreToothedSkull: -1,
            Item.CarvedBallOfStygianIvory: -2,
            Item.AmberCrustedFin: -3,
            Item.JetBlackStinger: -1,
        },
        zoo_type=ZooType.Fish,
        fluctuations=Flux.NoQuality)    
    
    # # 3/0/6/0/3 chimera => gothic w/ menace
    # trade(5 + actions_to_sell_chimera, {
    #     Item.SegmentedRibcage: -1,
    #     Item.DuplicatedVakeSkull: -1,
    #     Item.FossilisedForelimb: -1,
    #     Item.WingOfAYoungTerrorBird: -1,
    #     Item.JetBlackStinger: -1,

    #     Item.HinterlandScrip: 201,
    #     Item.CarvedBallOfStygianIvory: 21
    # })

    # # 3/0/5/0/3 chimera => gothic w/ menace
    # trade(5 + actions_to_sell_chimera, {
    #     Item.SegmentedRibcage: -1,
    #     Item.DuplicatedVakeSkull: -1,
    #     Item.WingOfAYoungTerrorBird: -2,
    #     Item.TombLionsTail: -1,

    #     Item.HinterlandScrip: 155,
    #     Item.CarvedBallOfStygianIvory: 18
    # })

    # # thorned ribcage
    # # 3/1/6/0/0 => gothic w/ reptiles + menace
    # trade(8, {
    #     Item.ThornedRibcage: -1,
    #     Item.DuplicatedVakeSkull: -1,
    #     Item.FemurOfAJurassicBeast: -3,
    #     Item.UnidentifiedThighbone: -1,
    #     Item.JetBlackStinger: -1,

    #     Item.HinterlandScrip: 199,
    #     Item.CarvedBallOfStygianIvory: 21
    # })

    # trade(8, {
    #     Item.ThornedRibcage: -1,
    #     Item.DuplicatedVakeSkull: -1,
    #     Item.FemurOfAJurassicBeast: -3,
    #     Item.UnidentifiedThighbone: -1,
    #     Item.JetBlackStinger: -1,

    #     Item.HinterlandScrip: 199,
    #     Item.CarvedBallOfStygianIvory: 21
    # })