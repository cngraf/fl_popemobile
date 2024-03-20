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

# class Skeleton():
#     def __init__(self,
#                  zooType: ZooType,
#                  recipe: dict):
#         self.zooType = zooType
#         self.recipe = recipe
#         self.bone_totals = create_skeleton(recipe)

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
        Bone(Item.HolyRelicOfTheThighOfStFiacre, 12.5), # TODO
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
            # result.addtl_costs = utils.sum_dicts(result, bone.addtl_costs)

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

def gothic_tales_trade(player: Player,
                       recipe: dict,
                       zoo_type: ZooType = ZooType.NoType,
                       fluctuations: Fluctuations = Fluctuations.NoQuality):
    payout = {}

    skeleton = create_skeleton(recipe)
    if skeleton.antiquity >= 1 and skeleton.menace >= 1:
        zoo_multi = zoo_multiplier(zoo_type)
        menace_bonus = 0.5 if fluctuations == Fluctuations.Menace else 0
        antiquity_bonus = 0.5 if fluctuations == Fluctuations.Antiquity else 0

        payout = {
            Item.BoneMarketExhaustion: math.floor(skeleton.antiquity * skeleton.menace/20),
            Item.HinterlandScrip: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.CarvedBallOfStygianIvory: (skeleton.antiquity + menace_bonus) * (skeleton.menace + antiquity_bonus)
        }

    action_penalty = -1 * expected_failed_sell_attempts(player, skeleton, zoo_type == ZooType.Chimera)

    payout = utils.sum_dicts(recipe, payout, { Item.Action: action_penalty})

def author_of_gothic_tales_payout(skeleton: Bone, zoo_multi: float = 1.0,
                                  fluctuations: Fluctuations = Fluctuations.NoQuality):
    
    menace_bonus = 0.5 if fluctuations == Fluctuations.Menace else 0
    antiquity_bonus = 0.5 if fluctuations == Fluctuations.Antiquity else 0

    if skeleton.antiquity < 1 and skeleton.menace < 1:
        return {}
    else:
        return {
            Item.BoneMarketExhaustion: math.floor(skeleton.antiquity * skeleton.menace/20),
            Item.HinterlandScrip: 5 + (skeleton.echo_value * zoo_multi * 2),
            Item.CarvedBallOfStygianIvory: (skeleton.antiquity + menace_bonus) * (skeleton.menace + antiquity_bonus)
        }

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

    # assumes 5 clear per action
    suspicion_penalty = 0.2 * fails
    return 1 + fails + suspicion_penalty



def add_trades(player, config: Config):
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

    # -------------------------------
    # ------ Leviathan Frame

    # 3/0/6/0/3 chimera => gothic w/ menace week
    trade(5 + actions_to_sell_chimera, {
        Item.LeviathanFrame: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.WingOfAYoungTerrorBird: -2,
        Item.HinterlandScrip: 770,
        Item.CarvedBallOfStygianIvory: 21
    })

    # 1/2/6 fish => gothic
    trade(6, {
        Item.LeviathanFrame: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.AmberCrustedFin: -2,
        Item.HinterlandScrip: 942,
        Item.CarvedBallOfStygianIvory: 9
    })

    sk_vake_levi_fish = gothic_tales_trade(
        player=player,
        recipe={
            Item.Action: -6,
            Item.LeviathanFrame: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.AmberCrustedFin: -2
        },
        zoo_type=ZooType.Fish,
        fluctuations=Fluctuations.Menace)

    # 2/2/4 fish => gothic
    trade(6, {
        Item.LeviathanFrame: -1,
        Item.SabreToothedSkull: -1,
        Item.AmberCrustedFin: -2,
        Item.HinterlandScrip: 937,
        Item.CarvedBallOfStygianIvory: 10
    })

    # 1/2/3 fish => gothic
    trade(5 + actions_to_sell_skelly(player.stats[Stat.Shadowy], 2), {
        Item.LeviathanFrame: -1,
        Item.BrightBrassSkull: -1,
        Item.AmberCrustedFin: -2,
        Item.HinterlandScrip: 948,
        Item.CarvedBallOfStygianIvory: 5
    })

    # chimera => grandmother
    trade(5 + actions_to_sell_skelly(shadowy, 3), {
        Item.LeviathanFrame: -1,
        Item.SabreToothedSkull: -1,
        Item.HumanArm: -2,
        Item.IncisiveObservation: 780
    })

    # fish => grandmother
    trade(5 + actions_to_sell_skelly(shadowy, 3), {
        Item.MammothRibcage: -1,
        Item.BrightBrassSkull: -1,
        Item.FinBonesCollected: -2,
        Item.IncisiveObservation: 316
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

    if config.player.profession == Profession.Licentiate:
        trade(0, { Item.ASkeletonOfYourOwn: 1 })

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

    agt_payout = author_of_gothic_tales_payout(
        create_skeleton(foo_recipe),
        fluctuations=Fluctuations.Menace)
    
    print("Gothic Tales payout: ")
    print(agt_payout)

    skelly_exchange = skeleton_exchange(
        foo_recipe,
        lambda x : author_of_gothic_tales_payout(x, fluctuations=Fluctuations.Menace))
    
    print(foo_recipe)
    print(skelly_exchange)

    # 4/0/4
    trade(7 + actions_to_sell_chimera, {
        Item.HumanRibcage: -1,
        Item.HornedSkull: -1,
        Item.WingOfAYoungTerrorBird: -3,
        Item.HumanArm: -1,
        Item.HinterlandScrip: 5 + utils.skelly_value_in_items(12.5 + 12.5 + (3 * 2.5) + 2.5, 0.5, False),
        Item.CarvedBallOfStygianIvory: 18 # 18/16/18,
    })

        # trade(8, {
        #     Item.ThornedRibcage
        # })

    # segmented ribcage
        
    # 3/0/6/0/3 chimera => gothic w/ menace
    trade(5 + actions_to_sell_chimera, {
        Item.SegmentedRibcage: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.FossilisedForelimb: -1,
        Item.WingOfAYoungTerrorBird: -1,
        Item.JetBlackStinger: -1,

        Item.HinterlandScrip: 201,
        Item.CarvedBallOfStygianIvory: 21
    })

    # 3/0/5/0/3 chimera => gothic w/ menace
    trade(5 + actions_to_sell_chimera, {
        Item.SegmentedRibcage: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.WingOfAYoungTerrorBird: -2,
        Item.TombLionsTail: -1,

        Item.HinterlandScrip: 155,
        Item.CarvedBallOfStygianIvory: 18
    })

    # thorned ribcage
    # 3/1/6/0/0 => gothic w/ reptiles + menace
    trade(8, {
        Item.ThornedRibcage: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.FemurOfAJurassicBeast: -3,
        Item.UnidentifiedThighbone: -1,
        Item.JetBlackStinger: -1,

        Item.HinterlandScrip: 199,
        Item.CarvedBallOfStygianIvory: 21
    })

    trade(8, {
        Item.ThornedRibcage: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.FemurOfAJurassicBeast: -3,
        Item.UnidentifiedThighbone: -1,
        Item.JetBlackStinger: -1,

        Item.HinterlandScrip: 199,
        Item.CarvedBallOfStygianIvory: 21
    })    

    # Generator Skeleton, various
    # testing various balances of brass vs. sabre-toothed skull

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

        trade(11 + actions_to_sell_skelly(player.stats[Stat.Shadowy], brass_skulls * 2), {
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

        trade(11 + actions_to_sell_skelly(player.stats[Stat.Shadowy], brass_skulls * 2), {
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

        trade(11 + actions_to_sell_skelly(player.stats[Stat.Shadowy], brass_skulls * 2), {
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
        