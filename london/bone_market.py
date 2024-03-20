from enums import *
from utils import *
import config

def actions_to_sell_skelly(shadowy, implausibility):
    if (implausibility < 1): return 1
    difficulty = 75 * implausibility
    success_rate = min(0.6 * shadowy/difficulty, 1.0)
    fails = 1.0/success_rate - 1

    # assumes 5 clear per action
    suspicion_penalty = 0.2 * fails
    return 1 + fails + suspicion_penalty

def add_trades(player, config: config.Config):
    trade = config.trade

    chimera_success_rate = narrow_challenge_success_rate(player.stats[Stat.Mithridacy], 10)
    actions_on_success = actions_to_sell_skelly(player.stats[Stat.Shadowy], 3)
    actions_on_failure = actions_to_sell_skelly(player.stats[Stat.Shadowy], 6)
    actions_to_sell_chimera = (actions_on_success * chimera_success_rate) + (actions_on_failure * (1.0 - chimera_success_rate))

    shadowy = player.stats[Stat.Shadowy]

    # out of curiosity, what happens if we could cash out everything for free
    # Suggests the following items can be acquired profitably:
    # - AmberCrustedFin
    # - Thigh of saint fiacre
    # - Skull in coral
    # - wing of a young terror bird
    # - skeleton with seven necks

    # trade(0, {
    #     Item.AlbatrossWing: -1, 
    #     Item.Echo: 12.50
    # })

    # trade(0, {
    #     Item.AmberCrustedFin: -1, 
    #     Item.Echo: 12.50
    # })

    # # counterfeit head of john the baptist
    # trade(0, {
    #     Item.BoneFragments: -500,
    #     Item.HandPickedPeppercaps: -10, 
    #     Item.Echo: 12.50
    # })

    # trade(0, {
    #     Item.DoubledSkull: -1,
    #     Item.Echo: 62.5
    # })

    # trade(0, {
    #     Item.EyelessSkull: -1, 
    #     Item.Echo: 30
    # })


    # trade(0, {
    #     Item.FemurOfAJurassicBeast: -1, 
    #     Item.Echo: 3
    # })

    # trade(0, {
    #     Item.FinBonesCollected: -1, 
    #     Item.Echo: 0.5
    # })

    # trade(0, {
    #     Item.FivePointedRibcage: -1, 
    #     Item.Echo: 312.5
    # })

    # trade(0, {
    #     Item.FlourishingRibcage: -1, 
    #     Item.Echo: 12.50
    # })

    # trade(0, {
    #     Item.FossilisedForelimb: -1, 
    #     Item.Echo: 27.50
    # })

    # trade(0, {
    #     Item.HeadlessSkeleton: -1, 
    #     Item.Echo: 2.50
    # })

    # trade(0, {
    #     Item.HelicalThighbone: -1, 
    #     Item.Echo: 3
    # })

    # trade(0, {
    #     Item.HolyRelicOfTheThighOfStFiacre: -1, 
    #     Item.Echo: 12.50
    # })

    # trade(0, {
    #     Item.HornedSkull: -1, 
    #     Item.Echo: 12.50
    # })

    # trade(0, {
    #     Item.HumanArm: -1, 
    #     Item.Echo: 2.50
    # })

    # trade(0, {
    #     Item.HumanRibcage: -1, 
    #     Item.Echo: 12.50
    # })

    # trade(0, {
    #     Item.IvoryFemur: -1, 
    #     Item.Echo: 65
    # })

    # trade(0, {
    #     Item.IvoryHumerus: -1, 
    #     Item.Echo: 15
    # })

    # trade(0, {
    #     Item.JetBlackStinger: -1, 
    #     Item.Echo: 0.5
    # })

    # trade(0, {
    #     Item.KnottedHumerus: -1, 
    #     Item.Echo: 3
    # })

    # trade(0, {
    #     Item.LeviathanFrame: -1, 
    #     Item.Echo: 312.50
    # })

    # trade(0, {
    #     Item.MammothRibcage: -1, 
    #     Item.Echo: 62.50
    # })

    # # vake skull
    # trade(0, {
    #     Item.BoneFragments: -6000,
    #     Item.Echo: 65
    # })

    # trade(0, {
    #     Item.PlatedSkull: -1,
    #     Item.Echo: 62.50
    # })

    # trade(0, {
    #     Item.PrismaticFrame: -1, 
    #     Item.Echo: 312.50
    # })

    # trade(0, {
    #     Item.RibcageWithABoutiqueOfEightSpines: -1, 
    #     Item.Echo: 312.50
    # })

    # trade(0, {
    #     Item.RubberySkull: -1,
    #     Item.Echo: 6
    # })

    # trade(0, {
    #     Item.SabreToothedSkull: -1, 
    #     Item.Echo: 62.50
    # })

    # trade(0, {
    #     Item.SegmentedRibcage: -1, 
    #     Item.Echo: 2.50
    # })

    # trade(0, {
    #     Item.SkeletonWithSevenNecks: -1, 
    #     Item.Echo: 62.50
    # })

    # trade(0, {
    #     Item.SkullInCoral: -1, 
    #     Item.Echo: 17.50
    # })

    # trade(0, {
    #     Item.ThornedRibcage: -1, 
    #     Item.Echo: 12.50
    # })

    # trade(0, {
    #     Item.WingOfAYoungTerrorBird: -1, 
    #     Item.Echo: 2.50
    # })

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
        Item.HinterlandScrip: challenge_ev(player.stats[Stat.Persuasive], 200, success= -120, failure= -125),
        Item.SabreToothedSkull: 1
    })

    trade(1 + expected_failures(broad_challenge_success_rate(player.stats[Stat.Persuasive], 210)), {
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
        success_rate = narrow_challenge_success_rate(player.stats[Stat.ArtisanOfTheRedScience], 5)
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
        Item.NightsoilOfTheBazaar: skelly_value_in_items(12.5 + 65 + (27.5 * 2) + (3 * 2), 0.5, False),
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
            Item.ASkeletonOfYourOwn: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.WingOfAYoungTerrorBird: -3,
            filler_limb: -1,
            Item.HinterlandScrip: 5 + skelly_value_in_items(2.5 + 65 + (3 * 2.5) + filler_limb_echo_value, 0.5, False),
            Item.CarvedBallOfStygianIvory: 21, # 20/18/21
        })

        # 3/1/6
        trade(7 + actions_to_sell_chimera, {
            Item.ASkeletonOfYourOwn: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.FemurOfAJurassicBeast: -1,
            Item.WingOfAYoungTerrorBird: -2,
            Item.AmberCrustedFin: -1,
            Item.HinterlandScrip: 5+ skelly_value_in_items(2.5 + 65 + 3 + (2 * 2.5) + 15, 0.5, False),
            Item.CarvedBallOfStygianIvory: 21, # 20/18/21
        })

        # 4/?/4
        trade(7 + actions_to_sell_chimera, {
            Item.ASkeletonOfYourOwn: -1,
            Item.SabreToothedSkull: -1,
            Item.WingOfAYoungTerrorBird: -3,
            filler_limb: -1,
            Item.HinterlandScrip: 5 + skelly_value_in_items(2.5 + 62.5 + (3 * 2.5) + filler_limb_echo_value, 0.5, False),
            Item.CarvedBallOfStygianIvory: 18, # 18/16/18
        })

        # 3/2/6
        trade(7 + actions_to_sell_chimera, {
            Item.ASkeletonOfYourOwn: -1,
            Item.HornedSkull: -1,
            Item.WingOfAYoungTerrorBird: -2,
            Item.AmberCrustedFin: -2,
            Item.HinterlandScrip: 5 + skelly_value_in_items(2.5 + 12.5 + (2 * 2.5) + (2 * 15), 0.5, False),
            Item.CarvedBallOfStygianIvory: 21 # 20/18/21,
        })

        # 4/0/4
        trade(7 + actions_to_sell_chimera, {
            Item.ASkeletonOfYourOwn: -1,
            Item.HornedSkull: -1,
            Item.WingOfAYoungTerrorBird: -3,
            Item.HumanArm: -1,
            Item.HinterlandScrip: 5 + skelly_value_in_items(2.5 + 12.5 + (3 * 2.5) + 2.5, 0.5, False),
            Item.CarvedBallOfStygianIvory: 18 # 18/16/18,
        })


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
            Item.HinterlandScrip: 5 + skelly_value_in_items(12.5 + 65 + (3 * 2.5) + filler_limb_echo_value, 0.5, False),
            Item.CarvedBallOfStygianIvory: 21, # 20/18/21
        })

        # 3/1/6
        trade(7 + actions_to_sell_chimera, {
            Item.HumanRibcage: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.FemurOfAJurassicBeast: -1,
            Item.WingOfAYoungTerrorBird: -2,
            Item.AmberCrustedFin: -1,
            Item.HinterlandScrip: 5+ skelly_value_in_items(12.5 + 65 + 3 + (2 * 2.5) + 15, 0.5, False),
            Item.CarvedBallOfStygianIvory: 21, # 20/18/21
        })

        # 4/?/4
        trade(7 + actions_to_sell_chimera, {
            Item.HumanRibcage: -1,
            Item.SabreToothedSkull: -1,
            Item.WingOfAYoungTerrorBird: -3,
            filler_limb: -1,
            Item.HinterlandScrip: 5 + skelly_value_in_items(12.5 + 62.5 + (3 * 2.5) + filler_limb_echo_value, 0.5, False),
            Item.CarvedBallOfStygianIvory: 18, # 18/16/18
        })

        # 3/2/6
        trade(7 + actions_to_sell_chimera, {
            Item.HumanRibcage: -1,
            Item.HornedSkull: -1,
            Item.WingOfAYoungTerrorBird: -2,
            Item.AmberCrustedFin: -2,
            Item.HinterlandScrip: 5 + skelly_value_in_items(12.5 + 12.5 + (2 * 2.5) + (2 * 15), 0.5, False),
            Item.CarvedBallOfStygianIvory: 21 # 20/18/21,
        })

        # 4/0/4
        trade(7 + actions_to_sell_chimera, {
            Item.HumanRibcage: -1,
            Item.HornedSkull: -1,
            Item.WingOfAYoungTerrorBird: -3,
            Item.HumanArm: -1,
            Item.HinterlandScrip: 5 + skelly_value_in_items(12.5 + 12.5 + (3 * 2.5) + 2.5, 0.5, False),
            Item.CarvedBallOfStygianIvory: 18 # 18/16/18,
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
        