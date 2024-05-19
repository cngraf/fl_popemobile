import math
from enum import Enum, auto

from enums import *
import utils
from config import Config
from player import Player

class Fluctuations(Enum):
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

class Bone():
    def __init__(self,
                 item: Item,
                 echo_value: int,
                 anitquity: int = 0,
                 amalgamy: int = 0,
                 menace: int = 0,
                 theology: int = 0,
                 implausibility: int = 0,
                 addtl_costs: dict = {}):
        self.item = item
        self.echo_value = echo_value
        self.antiquity = anitquity
        self.amalgamy = amalgamy
        self.menace = menace
        self.theology = theology
        self.implausibility = implausibility
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
        Bone(Item.RibcageWithABoutiqueOfEightSpines, 312.5, amalgamy=1,menace=1),
        Bone(Item.LeviathanFrame, 312.5, anitquity=1, menace=1),
        Bone(Item.PrismaticFrame, 312.5, anitquity=2, amalgamy=2),
        Bone(Item.FivePointedRibcage, 312.5, amalgamy=2, menace=1),

        # Bone(Item.VictimsSkull, 2.5),
        Bone(Item.CarvedBallOfStygianIvory, 2.5),
        Bone(Item.RubberySkull, 6, amalgamy=1),
        Bone(Item.HornedSkull, 12.5, anitquity=1, menace=2),
        Bone(Item.PentagrammicSkull, 12.5, amalgamy=2, menace=2),
        Bone(Item.DuplicatedCounterfeitHeadOfJohnTheBaptist, 12.5, theology=1),
        Bone(Item.SkullInCoral, 17.5, amalgamy=2, addtl_costs={Item.KnobOfScintillack: -1}),
        Bone(Item.PlatedSkull, 25, menace=2),
        Bone(Item.EyelessSkull, 30, menace=2),
        Bone(Item.DoubledSkull, 30, anitquity=2, amalgamy=1),
        Bone(Item.SabreToothedSkull, 30, anitquity=1, menace=1),
        Bone(Item.BrightBrassSkull, 65, implausibility=2, addtl_costs={Item.NevercoldBrassSliver: -200}),
        Bone(Item.DuplicatedVakeSkull, 65, menace=3),

        Bone(Item.CrustaceanPincer, 0, menace=1),
        Bone(Item.KnottedHumerus, 3, amalgamy=1),
        Bone(Item.HumanArm, 2.5, menace=-1),
        Bone(Item.IvoryHumerus, 15),
        Bone(Item.FossilisedForelimb, 15, anitquity=2),
        Bone(Item.FemurOfASurfaceDeer, 0.1, menace=-1),
        Bone(Item.UnidentifiedThighbone, 1),
        Bone(Item.FemurOfAJurassicBeast, 3, anitquity=1),
        Bone(Item.HelicalThighbone, 3, amalgamy=2),
        Bone(Item.HolyRelicOfTheThighOfStFiacre, 12.5),
        Bone(Item.IvoryFemur, 65),
        Bone(Item.BatWing, 0.01, menace=-1),
        Bone(Item.WingOfAYoungTerrorBird, 2.5, anitquity=1, menace=1),
        Bone(Item.AlbatrossWing, 12.5, amalgamy=1),
        Bone(Item.FinBonesCollected, 0.5),
        Bone(Item.AmberCrustedFin, 15, amalgamy=1, menace=1),

        Bone(Item.WitheredTentacle, 2.5, anitquity=-1),
        Bone(Item.JetBlackStinger, 2.5, menace=2),
        Bone(Item.PlasterTailBones, 2.5, implausibility=1),
        Bone(Item.TombLionsTail, 2.5, anitquity=1),
        Bone(Item.ObsidianChitinTail, 5, amalgamy=1),

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

def naive_collector_payout(skeleton: Bone, zoo_multi: float = 1.0):
    return {
        Item.ThirstyBombazineScrap: skeleton.echo_value * (zoo_multi)/2.5
    }
    
def bone_hoarder_payout(skeleton: Bone, zoo_multi: float = 1.0):
    return {
        Item.BoneFragments: 5 + (skeleton.echo_value * zoo_multi * 100),
        Item.UnearthlyFossil: 2
    }

def bohemian_sculptress_payout(skeleton: Bone, zoo_multi: float = 1.0):
    if skeleton.antiquity > 0:
        return {}
    else:
        return {
            Item.PreservedSurfaceBlooms: 4 + (skeleton.echo_value * zoo_multi / 2.5),
            Item.RumourOfTheUpperRiver: skeleton.theology
        }

def skeleton_exchange(bones: dict, calculate_payout):
    skelly = create_skeleton(bones)
    payout = calculate_payout(skelly)

    return utils.sum_dicts(bones, payout)

# def pedagocially_inclinded_grandmother_payout(skeleton: Bone, zoo_multi: float = 1.0):

def zoo_multiplier(skeletonType = ZooType):
    if skeletonType in (ZooType.Bird, ZooType.Amphibian, ZooType.Reptile):
        return 1.1
    if skeletonType in (ZooType.Fish, ZooType.Insect, ZooType.Spider):
        return 1.15
    else:
        return 1.0
    
def match_action_type(zoo_type, flux_type):
    if zoo_type == ZooType.Reptile:
        if flux_type == Fluctuations.Antiquity:
            return Item.AntiquityReptileAction
        elif flux_type == Fluctuations.Amalgamy:
            return Item.AmalgamyReptileAction
        elif flux_type == Fluctuations.Menace:
            return Item.MenaceReptileAction
        else:
            return Item.GeneralReptileAction
    
    elif zoo_type == ZooType.Amphibian:
        if flux_type == Fluctuations.Antiquity:
            return Item.AntiquityAmphibianAction
        elif flux_type == Fluctuations.Amalgamy:
            return Item.AmalgamyAmphibianAction
        elif flux_type == Fluctuations.Menace:
            return Item.MenaceAmphibianAction
        else:
            return Item.GeneralAmphibianAction        

    elif zoo_type == ZooType.Bird:
        if flux_type == Fluctuations.Antiquity:
            return Item.AntiquityBirdAction
        elif flux_type == Fluctuations.Amalgamy:
            return Item.AmalgamyBirdAction
        elif flux_type == Fluctuations.Menace:
            return Item.MenaceBirdAction
        else:
            return Item.GeneralBirdAction
        
    elif zoo_type == ZooType.Fish:
        if flux_type == Fluctuations.Antiquity:
            return Item.AntiquityFishAction
        elif flux_type == Fluctuations.Amalgamy:
            return Item.AmalgamyFishAction
        elif flux_type == Fluctuations.Menace:
            return Item.MenaceFishAction
        else:
            return Item.GeneralFishAction        

    elif zoo_type == ZooType.Spider:
        if flux_type == Fluctuations.Antiquity:
            return Item.AntiquityArachnidAction
        elif flux_type == Fluctuations.Amalgamy:
            return Item.AmalgamyArachnidAction
        elif flux_type == Fluctuations.Menace:
            return Item.MenaceArachnidAction
        else:
            return Item.GeneralArachnidAction        

    elif zoo_type == ZooType.Insect:
        if flux_type == Fluctuations.Antiquity:
            return Item.AntiquityInsectAction
        elif flux_type == Fluctuations.Amalgamy:
            return Item.AmalgamyInsectAction
        elif flux_type == Fluctuations.Menace:
            return Item.MenaceInsectAction
        else:
            return Item.GeneralInsectAction        

    else:
        if flux_type == Fluctuations.Antiquity:
            return Item.AntiquityGeneralAction
        elif flux_type == Fluctuations.Amalgamy:
            return Item.AmalgamyGeneralAction
        elif flux_type == Fluctuations.Menace:
            return Item.MenaceGeneralAction
        else:
            return Item.Action

    
def tentacled_entrepreneur_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Fluctuations = Fluctuations.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.amalgamy
    flux_power = 2.1 if fluctuations == Fluctuations.Amalgamy else 2.0

    if prop_a >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            Item.BoneMarketExhaustion: math.floor((prop_a ** 2)/25),
            Item.MemoryOfDistantShores: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.FinalBreath: 4 * (prop_a ** flux_power)
        }

    action_penalty = -1 * expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, { action_type: action_penalty })
    trade(0, totals)
 
def ambassador_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Fluctuations = Fluctuations.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.antiquity
    flux_power = 2.1 if fluctuations == Fluctuations.Antiquity else 2.0

    if prop_a >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            Item.BoneMarketExhaustion: math.floor((prop_a ** 2)/25),
            Item.MemoryOfLight: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.TailfeatherBrilliantAsFlame: 0.8 * (prop_a ** flux_power)
        }

    action_penalty = -1 * expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, { action_type: action_penalty })
    trade(0, totals)

def teller_of_terrors_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Fluctuations = Fluctuations.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.menace
    flux_power = 2.1 if fluctuations == Fluctuations.Menace else 2.0

    if prop_a >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            Item.BoneMarketExhaustion: math.floor((prop_a ** 2)/25),
            Item.BottelofMorelways1872: 25 + (skeleton.echo_value * zoo_multi * 10),
            Item.RoyalBlueFeather: 4 * (prop_a ** flux_power)
        }

    action_penalty = -1 * expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, { action_type: action_penalty })
    trade(0, totals)

def gothic_tales_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Fluctuations = Fluctuations.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.antiquity
    prop_b = skeleton.menace

    bonus_a = 0.5 if fluctuations == Fluctuations.Antiquity else 0
    bonus_b = 0.5 if fluctuations == Fluctuations.Menace else 0

    if prop_a >= 1 and prop_b >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            Item.BoneMarketExhaustion: math.floor(prop_a * prop_b/20),
            Item.HinterlandScrip: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.CarvedBallOfStygianIvory: (prop_a + bonus_b) * (prop_b + bonus_a)
        }

    action_penalty = -1 * expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, { action_type: action_penalty })
    trade(0, totals)

def zailor_particular_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Fluctuations = Fluctuations.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.antiquity
    prop_b = skeleton.amalgamy

    bonus_a = 0.5 if fluctuations == Fluctuations.Antiquity else 0
    bonus_b = 0.5 if fluctuations == Fluctuations.Amalgamy else 0

    if prop_a >= 1 and prop_b >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            Item.BoneMarketExhaustion: math.floor(prop_a * prop_b/20),
            Item.NoduleOfWarmAmber: 25 + (skeleton.echo_value * zoo_multi * 10),
            Item.KnobOfScintillack: (prop_a + bonus_b) * (prop_b + bonus_a)
        }

    action_penalty = -1 * expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, { action_type: action_penalty })
    trade(0, totals)

def rubbery_collector_trade(trade,
                        player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Fluctuations = Fluctuations.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    prop_a = skeleton.antiquity
    prop_b = skeleton.amalgamy

    bonus_a = 0.5 if fluctuations == Fluctuations.Antiquity else 0
    bonus_b = 0.5 if fluctuations == Fluctuations.Amalgamy else 0

    if prop_a >= 1 and prop_b >= 1:
        zoo_multi = zoo_multiplier(zoo_type)

        payout = {
            Item.BoneMarketExhaustion: math.floor(prop_a * prop_b/20),
            Item.HinterlandScrip: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.BasketOfRubberyPies: (prop_a + bonus_b) * (prop_b + bonus_a)
        }

    action_penalty = -1 * expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)
    action_type = match_action_type(zoo_type, fluctuations)

    totals = utils.sum_dicts(recipe, payout, skeleton.addtl_costs, { action_type: action_penalty })
    trade(0, totals)

# def author_of_gothic_tales_payout(skeleton: Bone, zoo_multi: float = 1.0,
#                                   fluctuations: Fluctuations = Fluctuations.NoQuality):
    
#     menace_bonus = 0.5 if fluctuations == Fluctuations.Menace else 0
#     antiquity_bonus = 0.5 if fluctuations == Fluctuations.Antiquity else 0

#     if skeleton.antiquity < 1 and skeleton.menace < 1:
#         return {}
#     else:
#         return {
#             Item.BoneMarketExhaustion: math.floor(skeleton.antiquity * skeleton.menace/20),
#             Item.HinterlandScrip: 5 + (skeleton.echo_value * zoo_multi * 2),
#             Item.CarvedBallOfStygianIvory: (skeleton.antiquity + menace_bonus) * (skeleton.menace + antiquity_bonus)
#         }

def expected_failed_sell_attempts(player, skeleton: Bone, is_chimera: bool = False, dc_per_point: int = 75):
    challenge_dc = dc_per_point * (skeleton.implausibility)
    if is_chimera: challenge_dc += 3
    
    pass_rate = utils.pass_rate(player, Stat.Shadowy, challenge_dc)
    return (1.0 / pass_rate) - 1

def actions_to_sell_skelly(shadowy, implausibility, second_chance = False):
    if (implausibility < 1): return 1
    difficulty = 75 * implausibility
    success_rate = min(0.6 * shadowy/difficulty, 1.0)
    if second_chance:
        success_rate =  1.0 - ((1.0 - success_rate) ** 2)
    fails = 1.0/success_rate - 1
    second_chance_penalty = 0.33 * (fails + 1) if second_chance else 0
    # assumes 5 clear per action
    suspicion_penalty = 0.2 * fails
    return 1 + fails + suspicion_penalty + second_chance_penalty

def add_trades(player: Player, config: Config):
    trade = config.trade

    chimera_success_rate = utils.narrow_challenge_success_rate(player.stats[Stat.Mithridacy], 10)
    actions_on_success = actions_to_sell_skelly(player.stats[Stat.Shadowy], 3)
    actions_on_failure = actions_to_sell_skelly(player.stats[Stat.Shadowy], 6)
    actions_to_sell_chimera = (actions_on_success * chimera_success_rate) + (actions_on_failure * (1.0 - chimera_success_rate))

    shadowy = player.stats[Stat.Shadowy]

    # Bone Market
    trade(0, {
        Item.HinterlandScrip: -2,
        Item.UnidentifiedThighbone: 1
    })

    trade(1, {
        Item.BoneFragments: -100,
        Item.NoduleOfWarmAmber: -25,
        Item.WingOfAYoungTerrorBird: 2
    })

    trade(0, {
        Item.Echo: -62.5,
        Item.BrightBrassSkull: 1
    })


    # Buy from patrons

    trade(1, {
        Item.HinterlandScrip: utils.challenge_ev(player.stats[Stat.Persuasive], 200, success= -120, failure= -125),
        Item.SabreToothedSkull: 1
    })

    trade(1 + utils.expected_failures(utils.broad_challenge_success_rate(player.stats[Stat.Persuasive], 210)), {
        Item.ParabolanOrangeApple: -1,
        Item.IvoryHumerus: 1
    })


    # -----------------
    # Sell To Patrons
    # ----------------

    trade(1, {
        Item.HumanRibcage: -1,
        Item.IncisiveObservation: 30
    })

    # -------------------------
    # ------- Recipes ---------
    # -------------------------
    # TODO: Verify all outputs

    # TODO: some of these definitely produce exhaustion

    '''
    6000 fragment recipes require:
    - BaL for the vake skull
    - AotRS 10 to 100% the check
    '''

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

    trade(0, {
        Item.BoneFragments: -500,
        Item.HandPickedPeppercaps: -10,
        Item.DuplicatedCounterfeitHeadOfJohnTheBaptist: 1
    })

    # -------------------------------
    # ------ Leviathan Frame

    # 3/0/6 sweet spot
    gothic_tales_trade(trade, player,
        recipe={
            Item.MenaceGeneralAction: -6,
            Item.LeviathanFrame: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.WingOfAYoungTerrorBird: -2
        },
        zoo_type=ZooType.Chimera,
        fluctuations=Fluctuations.Menace)

    for skull_type in (
        Item.BrightBrassSkull,
        Item.DuplicatedVakeSkull,
        Item.SabreToothedSkull,
        Item.PlatedSkull,
        Item.HornedSkull):

        # TODO: 1/1 split
        for i in range(0, 3):
            amber_fins = -1 * i
            fin_bones_collected = 2 - amber_fins

            ambassador_trade(trade, player,
                recipe={
                    Item.AntiquityFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Fluctuations.Antiquity)

            tentacled_entrepreneur_trade(trade, player,
                recipe={
                    Item.AmalgamyFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Fluctuations.Amalgamy)
            
            teller_of_terrors_trade(trade, player,
                recipe={
                    Item.MenaceFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Fluctuations.Menace)
                        
            gothic_tales_trade(trade, player,
                recipe={
                    Item.AntiquityFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Fluctuations.Antiquity)            
                        
            gothic_tales_trade(trade, player,
                recipe={
                    Item.MenaceFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Fluctuations.Menace)
            
            zailor_particular_trade(trade, player,
                recipe={
                    Item.AntiquityFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Fluctuations.Antiquity)

            zailor_particular_trade(trade, player,
                recipe={
                    Item.AmalgamyFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Fluctuations.Amalgamy)
            
            rubbery_collector_trade(trade, player,
                recipe={
                    Item.AmalgamyFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Fluctuations.Amalgamy)         

            rubbery_collector_trade(trade, player,
                recipe={
                    Item.MenaceFishAction: -6,
                    Item.LeviathanFrame: -1,
                    skull_type: -1,
                    Item.AmberCrustedFin: amber_fins,
                    Item.FinBonesCollected: fin_bones_collected
                },
                zoo_type=ZooType.Fish,
                fluctuations=Fluctuations.Menace)


    # gothic_tales_trade(trade,
    #     player=player,
    #     recipe={
    #         Item.MenaceFishAction: -6,
    #         Item.LeviathanFrame: -1,
    #         Item.DuplicatedVakeSkull: -1,
    #         Item.AmberCrustedFin: -2
    #     },
    #     zoo_type=ZooType.Fish,
    #     fluctuations=Fluctuations.Menace)
    
    # gothic_tales_trade(trade,
    #     player=player,
    #     recipe={
    #         Item.MenaceFishAction: -6,
    #         Item.LeviathanFrame: -1,
    #         Item.DuplicatedVakeSkull: -1,
    #         Item.FinBonesCollected: -2
    #     },
    #     zoo_type=ZooType.Fish,
    #     fluctuations=Fluctuations.Menace)
    
    # gothic_tales_trade(trade,
    #     player=player,
    #     recipe={
    #         Item.MenaceFishAction: -6,
    #         Item.LeviathanFrame: -1,
    #         Item.BrightBrassSkull: -1,
    #         Item.FinBonesCollected: -2
    #     },
    #     zoo_type=ZooType.Fish,
    #     fluctuations=Fluctuations.Menace)

    # # 2/2/4 fish => gothic
    # gothic_tales_trade(trade,
    #     player=player,
    #     recipe={
    #         Item.MenaceFishAction: -6,
    #         Item.LeviathanFrame: -1,
    #         Item.SabreToothedSkull: -1,
    #         Item.AmberCrustedFin: -2,
    #     },
    #     zoo_type=ZooType.Fish,
    #     fluctuations=Fluctuations.Menace
    # )

    # # 1/2/3 fish => gothic
    # gothic_tales_trade(trade,
    #     player=player,
    #     recipe={
    #         Item.MenaceFishAction: -6,
    #         Item.LeviathanFrame: -1,
    #         Item.BrightBrassSkull: -1,
    #         Item.AmberCrustedFin: -2,
    #     },
    #     zoo_type=ZooType.Fish,
    #     fluctuations=Fluctuations.Menace
    # )

    # # chimera => grandmother
    # trade(5 + actions_to_sell_skelly(shadowy, 3), {
    #     Item.LeviathanFrame: -1,
    #     Item.SabreToothedSkull: -1,
    #     Item.HumanArm: -2,
    #     Item.IncisiveObservation: 780
    # })

    # TODO: wrong recipe, fix this
    # # fish => grandmother
    # trade(5 + actions_to_sell_skelly(shadowy, 3), {
    #     Item.MammothRibcage: -1,
    #     Item.BrightBrassSkull: -1,
    #     Item.FinBonesCollected: -2,
    #     Item.IncisiveObservation: 316
    # })

    # ----------------------
    # ---- Mammoth Ribcage

    trade(9, {
        Item.MammothRibcage: -1,
        Item.SabreToothedSkull: -1,
        Item.FemurOfAJurassicBeast: -3,
        Item.HolyRelicOfTheThighOfStFiacre: -1,
        Item.JetBlackStinger: -1,
        Item.HinterlandScrip: 299,
        Item.CarvedBallOfStygianIvory: 21
    })

    # -------------------------------
    # ----- Human Ribcage

    # 0/6/3 humanoid
    trade(8, {
        Item.HumanRibcage: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.KnottedHumerus: -2,
        Item.HelicalThighbone: -2,
        Item.NightsoilOfTheBazaar: 184,
        Item.BasketOfRubberyPies: 21,
    })

    trade(8, {
        Item.HumanRibcage: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.FossilisedForelimb: -2,
        Item.FemurOfAJurassicBeast: -2,
        Item.NightsoilOfTheBazaar: utils.skelly_value_in_items(12.5 + 65 + (27.5 * 2) + (3 * 2), 0.5, False),
        Item.CarvedBallOfStygianIvory: 21,
    })

    '''
    "Biblically Inaccurate Angel"
    AKA the reject ribcage recycler

    the filler limb can be any limb with 0 antiquity, menace, and implausibility
    '''

    for filler_limb, filler_limb_echo_value in (
        (Item.KnottedHumerus, 3),
        (Item.IvoryHumerus, 15),
        (Item.UnidentifiedThighbone, 1),
        (Item.HelicalThighbone, 2),
        (Item.HolyRelicOfTheThighOfStFiacre, 12.5),
        (Item.IvoryFemur, 65),
        (Item.AlbatrossWing, 12.5),
        (Item.FinBonesCollected, 0.5)
    ):
        # 3/?/6
        trade(7 + actions_to_sell_chimera, {
            Item.HumanRibcage: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.WingOfAYoungTerrorBird: -3,
            filler_limb: -1,
            Item.HinterlandScrip: 5 + utils.skelly_value_in_items(12.5 + 65 + (3 * 2.5) + filler_limb_echo_value, 0.5, False),
            Item.CarvedBallOfStygianIvory: 21, # 20/18/21
        })

        # 4/?/4
        trade(7 + actions_to_sell_chimera, {
            Item.HumanRibcage: -1,
            Item.SabreToothedSkull: -1,
            Item.WingOfAYoungTerrorBird: -3,
            filler_limb: -1,
            Item.HinterlandScrip: 5 + utils.skelly_value_in_items(12.5 + 62.5 + (3 * 2.5) + filler_limb_echo_value, 0.5, False),
            Item.CarvedBallOfStygianIvory: 18, # 18/16/18
        })

    # 3/1/6
    trade(7 + actions_to_sell_chimera, {
        Item.HumanRibcage: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.FemurOfAJurassicBeast: -1,
        Item.WingOfAYoungTerrorBird: -2,
        Item.AmberCrustedFin: -1,
        Item.HinterlandScrip: 5+ utils.skelly_value_in_items(12.5 + 65 + 3 + (2 * 2.5) + 15, 0.5, False),
        Item.CarvedBallOfStygianIvory: 21, # 20/18/21
    })

    # 3/2/6
    trade(7 + actions_to_sell_chimera, {
        Item.HumanRibcage: -1,
        Item.HornedSkull: -1,
        Item.WingOfAYoungTerrorBird: -2,
        Item.AmberCrustedFin: -2,
        Item.HinterlandScrip: 5 + utils.skelly_value_in_items(12.5 + 12.5 + (2 * 2.5) + (2 * 15), 0.5, False),
        Item.CarvedBallOfStygianIvory: 21 # 20/18/21,
    })

    foo_recipe = {
        Item.HumanRibcage: -1,
        Item.HornedSkull: -1,
        Item.WingOfAYoungTerrorBird: -2,
        Item.AmberCrustedFin: -2
    }

    # agt_payout = author_of_gothic_tales_payout(
    #     create_skeleton(foo_recipe),
    #     fluctuations=Fluctuations.Menace)
    
    # skelly_exchange = skeleton_exchange(
    #     foo_recipe,
    #     lambda x : author_of_gothic_tales_payout(x, fluctuations=Fluctuations.Menace))

    # ------------------------------------------------
    # ------ Skeleton with Seven Necks Reicpes -------
    # ------------------------------------------------

    gothic_tales_trade(trade, player,
        recipe = {
            Item.MenaceBirdAction: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -5,
            Item.DuplicatedVakeSkull: -2,
            Item.WingOfAYoungTerrorBird: -2
        },
        zoo_type = ZooType.Bird,
        fluctuations= Fluctuations.Menace)


    # for i in range(0,8):

    #     brass_bird = {
    #         Item.SkeletonWithSevenNecks: -1,
    #         Item.BrightBrassSkull: -1 * i,
    #         Item.SabreToothedSkull: -1 * (7 - i),
    #         Item.WingOfAYoungTerrorBird: -2
    #     }

    #     trade(
    #         actionCost= 12 + actions_to_sell_skelly(315, 2 * i, True),
    #         exchanges= utils.sum_dicts(
    #             brass_bird,
    #             author_of_gothic_tales_payout(
    #                 create_skeleton(brass_bird),
    #                 1.15,
    #                 fluctuations=Fluctuations.Menace
    #             )
    #     ))

    # Generator Skeleton, various
    # testing various balances of brass vs. sabre-toothed skull
    # TODO: remove ones that create exhaustion

    for i in range(0, 4):
        zoo_bonus = 0.1

        brass_skulls = i
        sabre_toothed_skulls = 7 - i

        penny_value = 6250 + 2500
        penny_value += 6500 * brass_skulls
        penny_value += 6250 * sabre_toothed_skulls

        trade(11 + actions_to_sell_skelly(player.stats[Stat.Shadowy], brass_skulls * 2), {
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -1 * brass_skulls,
            Item.NevercoldBrassSliver: -200 * brass_skulls,
            Item.SabreToothedSkull: -1 * sabre_toothed_skulls,
            Item.AlbatrossWing: -2,
            Item.MemoryOfDistantShores: 5 + (penny_value * (1 + zoo_bonus)/50),
            Item.FinalBreath: 74
        })

    # same as above but with 1x skull in coral and different wings
    for i in range(0, 4):
        brass_skulls = i
        sabre_toothed_skulls = 6 - i

        penny_value = 6250 + 1750 + 500
        penny_value += 6500 * brass_skulls
        penny_value += 6250 * sabre_toothed_skulls

        zoo_bonus = 0.1

        trade(11 + actions_to_sell_skelly(shadowy, brass_skulls * 2), {
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -1 * brass_skulls,
            Item.NevercoldBrassSliver: -200 * brass_skulls,
            Item.SabreToothedSkull: -1 * sabre_toothed_skulls,
            Item.SkullInCoral: -1,
            Item.KnobOfScintillack: -1,
            Item.WingOfAYoungTerrorBird: -2,
            Item.MemoryOfDistantShores: 5 + (penny_value * (1 + zoo_bonus)/50),
            # amalgamy week
            Item.FinalBreath: 74
        })

    # Hoarding Palaeo
    for i in range(0, 4):
        zoo_bonus = 0.1

        brass_skulls = i
        sabre_toothed_skulls = 7 - i

        penny_value = 0
        penny_value += 6250 # skelly
        penny_value += 6500 * brass_skulls
        penny_value += 6250 * sabre_toothed_skulls
        penny_value += 250 * 2 # wings

        trade(11 + actions_to_sell_skelly(shadowy, brass_skulls * 2), {
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -1 * brass_skulls,
            Item.NevercoldBrassSliver: -200 * brass_skulls,
            Item.SabreToothedSkull: -1 * sabre_toothed_skulls,
            Item.WingOfAYoungTerrorBird: -2,
            Item.BoneFragments: penny_value * (1 + zoo_bonus),
            Item.UnearthlyFossil: 2
        })

    # Zailor Particular
    for i in range(0, 4):
        zoo_bonus = 0.1
        antiquity_bonus = 0.5
        amalgamy_bonus  = 0

        brass_skulls = i
        sabre_toothed_skulls = 7 - i

        penny_value = 0
        penny_value += 6250 # skelly
        penny_value += 6500 * brass_skulls
        penny_value += 6250 * sabre_toothed_skulls
        penny_value += 250 * 2 # wings

        antiquity = sabre_toothed_skulls + 2
        amalgamy = 2

        trade(11 + actions_to_sell_skelly(shadowy, brass_skulls * 2), {
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -1 * brass_skulls,
            Item.NevercoldBrassSliver: -200 * brass_skulls,
            Item.SabreToothedSkull: -1 * sabre_toothed_skulls,
            Item.WingOfAYoungTerrorBird: -2,
            Item.NoduleOfWarmAmber: 25 + (penny_value * (1 + zoo_bonus))/10,
            Item.KnobOfScintillack: ((antiquity + amalgamy_bonus) * (amalgamy + antiquity_bonus))
        })    

    for i in range(0, 8):
        zoo_bonus = 0.1

        brass_skulls = i
        sabre_toothed_skulls = 7 - i

        penny_value = 6250 + 2500
        penny_value += 6500 * brass_skulls
        penny_value += 6250 * sabre_toothed_skulls

        trade(11 + actions_to_sell_skelly(player.stats[Stat.Shadowy], (brass_skulls * 2)/3), {
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -1 * brass_skulls,
            Item.NevercoldBrassSliver: -200 * brass_skulls,
            Item.SabreToothedSkull: -1 * sabre_toothed_skulls,
            Item.AlbatrossWing: -2,

            Item.ThirstyBombazineScrap: (penny_value * (1 + zoo_bonus)/250),
        })

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

    # # trade(0, {
    # #     Item.Echo: -60,
    # #     Item.GlimEncrustedCarapace: 1
    # # })

    # trade(12, {
    #     Item.GlimEncrustedCarapace: -1,
    #     Item.DuplicatedCounterfeitHeadOfJohnTheBaptist: -1,
    #     Item.HolyRelicOfTheThighOfStFiacre: -8,

    #     Item.PreservedSurfaceBlooms: 83,
    #     Item.RumourOfTheUpperRiver: 41
    # })  

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