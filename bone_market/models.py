import math
from enum import Enum, auto

import helper.utils as utils
from enums import *
from config import Config
from player import Player
from bone_market.models import *

'''
TODO
- negative modifiers can sometimes be ignored?!
    negative mods will not reduce a quality below 0,
    and so can be sidestepped depending on order
'''

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

    @staticmethod
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
        Bone(Item.UnidentifiedThighBone, 1),
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

        # Need to add warm amber cost manually
        Bone(Item._FourMoreJoints, 0, addtl_costs = { Item.NoduleOfTremblingAmber: -1 }),
        Bone(Item._ReduceAntiquity, 0, anitquity = -2),
        Bone(Item._ReduceAmalgamy, 0, amalgamy = -2, addtl_costs = { Item.JadeFragment: -25 }),
        Bone(Item._ReduceMenace, 0, menace = -2),

        # TODO: modifications
        # Bone(Item.FourMoreJoints, 0, amalgamy=2),
    ):
        dictionary[bone.item] = bone

    return dictionary
