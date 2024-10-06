import math
from enum import Enum, auto
from enums import *
import helper.utils as utils
from config import Config
from player import Player
from bone_market.models import *
from bone_market.buyers import *

def add_trades(config: Config):
    player = config.player
    trade = config.trade

    # HACK
    config.trade(0, { Item._NoItem: 1})

    bone_market_week_actions = {
        Flux.Antiquity: {
            ZooType.Reptile: Item._AntiquityReptileAction,
            ZooType.Amphibian: Item._AntiquityAmphibianAction,
            ZooType.Bird: Item._AntiquityBirdAction,
            ZooType.Fish: Item._AntiquityFishAction,
            ZooType.Spider: Item._AntiquityArachnidAction,
            ZooType.Insect: Item._AntiquityInsectAction,
            ZooType.Primate: Item._AntiquityPrimateAction,
            ZooType.NoType: Item._AntiquityGeneralAction
        },
        Flux.Amalgamy: {
            ZooType.Reptile: Item._AmalgamyReptileAction,
            ZooType.Amphibian: Item._AmalgamyAmphibianAction,
            ZooType.Bird: Item._AmalgamyBirdAction,
            ZooType.Fish: Item._AmalgamyFishAction,
            ZooType.Spider: Item._AmalgamyArachnidAction,
            ZooType.Insect: Item._AmalgamyInsectAction,
            ZooType.Primate: Item._AmalgamyPrimateAction,
            ZooType.NoType: Item._AmalgamyGeneralAction
        },
        Flux.Menace: {
            ZooType.Reptile: Item._MenaceReptileAction,
            ZooType.Amphibian: Item._MenaceAmphibianAction,
            ZooType.Bird: Item._MenaceBirdAction,
            ZooType.Fish: Item._MenaceFishAction,
            ZooType.Spider: Item._MenaceArachnidAction,
            ZooType.Insect: Item._MenaceInsectAction,
            ZooType.Primate: Item._MenacePrimateAction,
            ZooType.NoType: Item._MenaceGeneralAction
        },
        Flux.NoQuality: {
            ZooType.Reptile: Item._GeneralReptileAction,
            ZooType.Amphibian: Item._GeneralAmphibianAction,
            ZooType.Bird: Item._GeneralBirdAction,
            ZooType.Fish: Item._GeneralFishAction,
            ZooType.Spider: Item._GeneralArachnidAction,
            ZooType.Insect: Item._GeneralInsectAction,
            ZooType.Primate: Item._GeneralPrimateAction,
            # ZooType.NoType: None
        }
    }

    # TODO get this from config
    max_bone_market_actions_per_week = 700  # HACK hidden parameter
    exhaustion_per_week = -4
    unique_weeks = 21  # 3 vibes * 7 zoo types

    action_split = {
        Item._BoneMarketRotation: -1
    }

    for flux_type, zoo_actions in bone_market_week_actions.items():
        if (flux_type == Flux.NoQuality):
            continue

        generic_flux_action = zoo_actions[ZooType.NoType]
        generic_flux_exhaustion = Buyer.match_exhaustion_type(ZooType.NoType, flux_type)

        for zoo_type, weekly_action in zoo_actions.items():
            if zoo_type == ZooType.NoType:
                continue

            generic_zoo_action = bone_market_week_actions[Flux.NoQuality][zoo_type]
            generic_zoo_exhaustion = Buyer.match_exhaustion_type(zoo_type, Flux.NoQuality)

            exhaustion_type = Buyer.match_exhaustion_type(zoo_type, flux_type)

            action_split[weekly_action] = max_bone_market_actions_per_week / unique_weeks
            action_split[exhaustion_type] = exhaustion_per_week / unique_weeks

            config.add({ weekly_action: -1, generic_flux_action: 1 })
            config.add({ weekly_action: -1, generic_zoo_action: 1 })

            config.add({
                exhaustion_type: -exhaustion_per_week,
                generic_zoo_exhaustion: exhaustion_per_week
            })

            config.add({
                exhaustion_type: -exhaustion_per_week,
                generic_flux_exhaustion: exhaustion_per_week
            })

            config.add({
                exhaustion_type: -exhaustion_per_week,
                Item.GenericBoneMarketExhaustion: exhaustion_per_week
            })

    config.add(action_split)

    trade(0, {
        Item.HinterlandScrip: -2,
        Item.UnidentifiedThighBone: 1
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
        Item.HinterlandScrip: utils.challenge_ev(player.qualities[Item.Persuasive], 200, success= -120, failure= -125),
        Item.SabreToothedSkull: 1
    })

    trade(1 + utils.expected_failures(utils.broad_challenge_pass_rate(player.qualities[Item.Persuasive], 210)), {
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

    # A Public Lecture (Card)
    # TODO london deck constraint
    for ex_item in exhaustion_items:
        config.add({
            Item.Action: -1,
            Item.FistfulOfSurfaceCurrency: -1_000,
            Item.HinterlandScrip: -25,
            Item.FavourInHighPlaces: -1,
            
            ex_item: -1
        })

    # -----------------
    #   Skeleton Modifications
    # ----------------

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

    if player.get(Item.BagALegend):
        # min 1 action is baked into recipes, this only adds for failure
        # ignores other failure costs bc lazy
        success_rate = utils.narrow_challenge_pass_rate(player.qualities[Item.ArtisanOfTheRedScience], 5)
        failures = 1.0/success_rate - 1 if success_rate < 1.0 else 0
        trade(failures, {
            Item.BoneFragments: -6000,
            Item.DuplicatedVakeSkull: 1
        })

    if player.get(Item.ListOfAliasesWrittenInGant):
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
    gothic_tales_buyers = AuthorOfGothicTales()
    zailor_particular_buyers = ZailorWithParticularInterests()
    rubbery_collector_buyers = RubberyCollector()

    teller_buyers = TellerOfTerrors()
    entrepreneur_buyers = TentacledEntrepreneur()
    ambassador_buyers = InvestmedMindedAmbassador()

    paleo_buyers = HoardingPalaeontologist()
    naive_buyers = NaiveCollector()

    constable_buyer = Constable()
    theologial_buyer = TheologianOfTheOldSchool()

    sculptress_buyer = BohemianSculptress()

    diplomat_triple_buyer = TriflingDiplomatTripleQuality()

    # for flux_type in (Flux.Antiquity, Flux.Amalgamy, Flux.Menace, Flux.NoQuality):
    #     gothic_tales_buyers[flux_type] = {}
    #     zailor_particular_buyers[flux_type] = {}
    #     rubbery_collector_buyers[flux_type] = {}
    #     teller_buyers[flux_type] = {}
    #     entrepreneur_buyers[flux_type] = {}
    #     ambassador_buyers[flux_type] = {}
    #     paleo_buyers[flux_type] = {}
    #     naive_buyers[flux_type] = {}

    #     for zoo_type in (
    #         ZooType.Amphibian,
    #         ZooType.Bird,
    #         ZooType.Chimera,
    #         ZooType.Fish,
    #         ZooType.Insect,
    #         ZooType.Primate,
    #         ZooType.Reptile,
    #         ZooType.Spider,
    #         ZooType.NoType
    #     ):
    #         gothic_tales_buyers[flux_type][zoo_type] = AuthorOfGothicTales(zoo_type, flux_type)
    #         zailor_particular_buyers[flux_type][zoo_type] = ZailorWithParticularInterests(zoo_type, flux_type)
    #         rubbery_collector_buyers[flux_type][zoo_type] = RubberyCollector(zoo_type, flux_type)
    #         teller_buyers[flux_type][zoo_type] = TellerOfTerrors(zoo_type, flux_type)
    #         entrepreneur_buyers[flux_type][zoo_type] = TentacledEntrepreneur(zoo_type, flux_type)
    #         ambassador_buyers[flux_type][zoo_type] = InvestmedMindedAmbassador(zoo_type, flux_type)
    #         paleo_buyers[flux_type][zoo_type] = HoardingPalaeontologist(zoo_type, flux_type)
    #         naive_buyers[flux_type][zoo_type] = NaiveCollector(zoo_type, flux_type)


    # gothic_chimera_menace = AuthorOfGothicTales(ZooType.Chimera, Flux.Menace)
    # gothic_chimera_antiquity = AuthorOfGothicTales(ZooType.Chimera, Flux.Menace)
    # gothic_fish_antiquity = AuthorOfGothicTales(ZooType.Fish, Flux.Menace)
    # gothic_fish_menace = AuthorOfGothicTales(ZooType.Fish, Flux.Menace)

    # zailor_fish_antiquity = ZailorWithParticularInterests(ZooType.Fish, Flux.Antiquity)
    # zailor_fish_amalgamy = ZailorWithParticularInterests(ZooType.Fish, Flux.Amalgamy)

    # rubbery_collector_fish_amalgamy = RubberyCollector(ZooType.Fish, Flux.Amalgamy)
    # rubbery_collector_fish_menace = RubberyCollector(ZooType.Fish, Flux.Menace)

    # teller_fish_menace = TellerOfTerrors(ZooType.Fish, Flux.Menace)

    # entrepreneur_fish_amalgamy = TentacledEntrepreneur(ZooType.Fish, Flux.Amalgamy)

    # ambassador_fish_antiquity = InvestmedMindedAmbassador(ZooType.Fish, Flux.Antiquity)


    # constable_primate = Constable(ZooType.Primate)
    # constable_generic = Constable(ZooType.NoType)

    # theologial_primate = Theologian(ZooType.Primate)
    # theologian_generic = Theologian(ZooType.NoType)
    
    # -------------------------------
    #        Leviathan Frame

    # 7 antiquity, 1 ex
    ambassador_buyers.add_trade(config, Flux.Antiquity, ZooType.Chimera,
        recipe={
            Item.Action: -6,
            Item.LeviathanFrame: -1,

            Item.DoubledSkull: -1,
            Item.FossilisedForelimb: -2,
        })   

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

        gothic_tales_buyers.add_trade(config, Flux.Menace, ZooType.Chimera, chimera_levi_recipe)
        gothic_tales_buyers.add_trade(config, Flux.Antiquity, ZooType.Chimera, chimera_levi_recipe)

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

            entrepreneur_buyers.add_trade(config, Flux.Amalgamy, ZooType.Fish, levi_fish_recipe)

            ambassador_buyers.add_trade(config, Flux.Antiquity, ZooType.Fish, levi_fish_recipe)
            
            teller_buyers.add_trade(config, Flux.Menace, ZooType.Fish, levi_fish_recipe)
            teller_buyers.add_trade(config, Flux.Menace, ZooType.NoType, levi_fish_recipe)
            
            gothic_tales_buyers.add_trade(config, Flux.Antiquity, ZooType.Fish, levi_fish_recipe)
            gothic_tales_buyers.add_trade(config, Flux.Menace, ZooType.Fish, levi_fish_recipe)
            
            zailor_particular_buyers.add_trade(config, Flux.Antiquity, ZooType.Fish, levi_fish_recipe)
            zailor_particular_buyers.add_trade(config, Flux.Amalgamy, ZooType.Fish, levi_fish_recipe)

            rubbery_collector_buyers.add_trade(config, Flux.Amalgamy, ZooType.Fish, levi_fish_recipe)
            rubbery_collector_buyers.add_trade(config, Flux.Menace, ZooType.Fish, levi_fish_recipe)

            paleo_buyers.add_trade(config, Flux.NoQuality, ZooType.Fish, levi_fish_recipe)

    # ----------------------
    # ---- Mammoth Ribcage

    mammoth_menace_fish_recipe = {
        Item.Action: -9,
        Item.MammothRibcage: -1,

        Item.HornedSkull: -2,
        Item.AmberCrustedFin: -3,
        Item.FinBonesCollected: -1,
        Item.JetBlackStinger: -1
    }

    teller_buyers.add_trade(config, Flux.Menace, ZooType.Fish, mammoth_menace_fish_recipe)
    teller_buyers.add_trade(config, Flux.Menace, ZooType.NoType, mammoth_menace_fish_recipe)


    for skull in (Item.HornedSkull, Item.SabreToothedSkull):
        ambassador_buyers.add_trade(config, Flux.Antiquity, ZooType.Bird,
            recipe={
                Item.Action: -9,
                Item.MammothRibcage: -1,

                skull: -1,
                Item.WingOfAYoungTerrorBird: -2,
                Item.FossilisedForelimb: -1,
                Item.UnidentifiedThighBone: -1,
                Item.TombLionsTail: -1
            })   

    for zoo_type in (ZooType.Reptile, ZooType.NoType):
        ambassador_buyers.add_trade(config, Flux.Antiquity, zoo_type,
            recipe={
                Item.Action: -9,
                Item.MammothRibcage: -1,

                Item.BrightBrassSkull: -1,
                Item.FemurOfAJurassicBeast: -4,
                Item.TombLionsTail: -1
            })   

    ambassador_buyers.add_trade(config, Flux.Antiquity, ZooType.Bird,
        recipe={
            Item.Action: -9,
            Item.MammothRibcage: -1,

            Item.BrightBrassSkull: -1,
            Item.FemurOfAJurassicBeast: -2,
            Item.WingOfAYoungTerrorBird: -2,
            Item.TombLionsTail: -1
        })
    
    ambassador_buyers.add_trade(config, Flux.Antiquity, ZooType.NoType,
        recipe={
            Item.Action: -9,
            Item.MammothRibcage: -1,

            Item.BrightBrassSkull: -1,
            Item.FemurOfAJurassicBeast: -2,
            Item.WingOfAYoungTerrorBird: -2,
            Item.TombLionsTail: -1
        })            

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
        for tail in (Item.JetBlackStinger, Item.FailedJetBlackStinger):
            some_mammoth_recipe = {
                Item.Action: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -3,
                Item.HolyRelicOfTheThighOfStFiacre: -1,
                tail: -1
            }


            gothic_tales_buyers.add_trade(config, Flux.Antiquity, ZooType.Reptile, some_mammoth_recipe)
            gothic_tales_buyers.add_trade(config, Flux.Menace, ZooType.Reptile, some_mammoth_recipe)

        for tail in (Item.ObsidianChitinTail, Item._NoItem):
            some_mammoth_recipe = {
                Item.Action: -9,
                Item._AntiquityReptileAction: -9,
                Item.MammothRibcage: -1,
                skull_type: -1,
                Item.FemurOfAJurassicBeast: -4,
                tail: -1                
            }
           
            zailor_particular_buyers.add_trade(config, Flux.Antiquity, ZooType.Reptile, some_mammoth_recipe)
            zailor_particular_buyers.add_trade(config, Flux.Antiquity, ZooType.Amphibian, some_mammoth_recipe)
           
            zailor_particular_buyers.add_trade(config, Flux.Amalgamy, ZooType.Reptile, some_mammoth_recipe)
            zailor_particular_buyers.add_trade(config, Flux.Amalgamy, ZooType.Amphibian, some_mammoth_recipe)
        
        mammoth_recipe2 = {
            Item.Action: -9,
            Item._AntiquityAmphibianAction: -9,
            Item.MammothRibcage: -1,
            skull_type: -1,
            Item.FemurOfAJurassicBeast: -1,
            Item.HelicalThighbone: -2,
            Item.HolyRelicOfTheThighOfStFiacre: -1
        }

        zailor_particular_buyers.add_trade(config, Flux.Antiquity, ZooType.Amphibian, mammoth_recipe2)
        zailor_particular_buyers.add_trade(config, Flux.Amalgamy, ZooType.Amphibian, mammoth_recipe2)

    # -------------------------------
    # ----- Human Ribcage -----------
    # -------------------------------
    gothic_tales_buyers.add_trade(config, Flux.Antiquity, ZooType.Primate,
        recipe={
            Item.Action: -8,
            Item.HumanRibcage: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.FossilisedForelimb: -1,
            Item.FailedFossilisedForelimb: -1,
            Item.FemurOfAJurassicBeast: -2
        })
    
    # 7 menace
    teller_buyers.add_trade(config, Flux.Menace, ZooType.Chimera,
        recipe={
            Item.Action: -8,
            Item.HumanRibcage: -1,
            Item.DuplicatedVakeSkull: -1,
            Item.WingOfAYoungTerrorBird: -4,
        })
    
    # 7 Amalgamy
    entrepreneur_buyers.add_trade(config, Flux.Amalgamy, ZooType.Chimera,
        recipe={
            Item.Action: -8,
            Item.HumanRibcage: -1,

            Item.BrightBrassSkull: -1,
            Item.HelicalThighbone: -3,
            Item.AlbatrossWing: -1
        })
    
    entrepreneur_buyers.add_trade(config, Flux.Amalgamy, ZooType.Chimera,
        recipe={
            Item.Action: -8,
            Item.HumanRibcage: -1,

            Item.BrightBrassSkull: -1,
            Item.HelicalThighbone: -3,
            Item.FailedHelicalThighbone: -1
        })    
    
    entrepreneur_buyers.add_trade(config, Flux.Amalgamy, ZooType.Chimera,
        recipe={
            Item.Action: -8,
            Item.HumanRibcage: -1,

            Item.SkullInCoral: -1,
            Item.HelicalThighbone: -1,
            Item.AlbatrossWing: -3
        })
    
    # 7 Antiquity
    ambassador_buyers.add_trade(config, Flux.Antiquity, ZooType.Chimera,
        recipe={
            Item.Action: -8,
            Item.HumanRibcage: -1,

            Item.BrightBrassSkull: -1,
            Item.WingOfAYoungTerrorBird: -1,
            Item.FossilisedForelimb: -3
        })    

    for skull in (Item.HornedSkull, Item.SabreToothedSkull):
        ambassador_buyers.add_trade(config, Flux.Antiquity, ZooType.Chimera,
            recipe={
                Item.Action: -8,
                Item.HumanRibcage: -1,

                skull: -1,
                Item.WingOfAYoungTerrorBird: -2,
                Item.FossilisedForelimb: -2
            })    

    # ==============================================================
    #                   Skeleton of Your Own
    # ==============================================================

    # Brass Lollipop
    for ribcage in (Item.ASkeletonOfYourOwn, Item.HeadlessSkeleton):
        for skull in (Item.BrightBrassSkull, Item.DuplicatedVakeSkull):
            lollipop_recipe = {
                Item.Action: -4,
                ribcage: -1,
                skull: -1
            }

            constable_buyer.add_trade(config, Flux.NoQuality, ZooType.NoType, lollipop_recipe)
            constable_buyer.add_trade(config, Flux.NoQuality, ZooType.Primate, lollipop_recipe)

            theologial_buyer.add_trade(config, Flux.NoQuality, ZooType.NoType, lollipop_recipe)
            theologial_buyer.add_trade(config, Flux.NoQuality, ZooType.Primate, lollipop_recipe)

            teller_buyers.add_trade(config, Flux.Menace, ZooType.Primate, lollipop_recipe)
            teller_buyers.add_trade(config, Flux.NoQuality, ZooType.Primate, lollipop_recipe)
            teller_buyers.add_trade(config, Flux.Menace, ZooType.NoType, lollipop_recipe)
            teller_buyers.add_trade(config, Flux.NoQuality, ZooType.NoType, lollipop_recipe)

    '''
    "Biblically Inaccurate Angel"
    AKA the reject ribcage recycler

    the filler limb can be any limb with 0 antiquity, menace, and implausibility
    '''

    for filler_limb in (
        Item.KnottedHumerus,
        Item.IvoryHumerus,
        Item.UnidentifiedThighBone,
        Item.HelicalThighbone,
        Item.HolyRelicOfTheThighOfStFiacre,
        Item.IvoryFemur,
        Item.AlbatrossWing,
        Item.FinBonesCollected
    ):
        
        for num_wings in range(0, 4):
            for skull in (Item.DuplicatedVakeSkull,
                          Item.SabreToothedSkull,
                          Item.HornedSkull):
                filler_cherub_recipe = {
                    Item.Action: -8,
                    skull: -1,
                    Item.WingOfAYoungTerrorBird: -num_wings,
                    filler_limb: -4 + num_wings
                }

            gothic_tales_buyers.add_trade(config, Flux.Menace, ZooType.Chimera, filler_cherub_recipe)
            gothic_tales_buyers.add_trade(config, Flux.Antiquity, ZooType.Chimera, filler_cherub_recipe)


    # wtf was I thinking with this recipe
    menace_4ex_bird_recipe = {
        Item.Action: -12,

        Item.SkeletonWithSevenNecks: -1,

        Item.HornedSkull: -2,
        Item.SabreToothedSkull: -1,
        Item.DuplicatedVakeSkull: -1,
        Item.BrightBrassSkull: -3,
        Item.WingOfAYoungTerrorBird: -2
    }
    
    teller_buyers.add_trade(config, Flux.Menace, ZooType.Bird, menace_4ex_bird_recipe)
    teller_buyers.add_trade(config, Flux.Menace, ZooType.NoType, menace_4ex_bird_recipe)

    # # Exhaustion 4
    # teller_of_terrors_trade(config.trade, config.player,
    #     recipe={
    #         Item.Action: -12,
    #         Item.MenaceBirdAction: -12,
    #         Item.SkeletonWithSevenNecks: -1,
    #         Item.HornedSkull: -2,
    #         Item.SabreToothedSkull: -1,
    #         Item.DuplicatedVakeSkull: -1,
    #         Item.BrightBrassSkull: -3,
    #         Item.WingOfAYoungTerrorBird: -2
    #     },
    #     zoo_type=ZooType.Bird,
    #     fluctuations=Flux.Menace)

    # # Exhaustion 4
    # teller_of_terrors_trade(config.trade, config.player,
    #     recipe={
    #         Item.Action: -12,
    #         Item.MenaceBirdAction: -12,
    #         Item.SkeletonWithSevenNecks: -1,
    #         Item.HornedSkull: -2,
    #         Item.SabreToothedSkull: -1,
    #         Item.DuplicatedVakeSkull: -1,
    #         Item.BrightBrassSkull: -3,
    #         Item.WingOfAYoungTerrorBird: -2
    #     },
    #     zoo_type=ZooType.NoType,
    #     fluctuations=Flux.Menace)

    coral_bird_seven_recipe ={
        Item.Action: -12,
        Item.SkeletonWithSevenNecks: -1,
        Item.SkullInCoral: -7,
        Item.AlbatrossWing: -2
    }

    rubbery_collector_buyers.add_trade(config, Flux.Amalgamy, ZooType.Bird, coral_bird_seven_recipe)

    coral_bird_eight_recipe ={
        Item.Action: -16,
        Item.RibcageWithABoutiqueOfEightSpines: -1,
        Item.SkullInCoral: -8,
        Item.AlbatrossWing: -2,
        Item.FemurOfASurfaceDeer: -1,
        Item.UnidentifiedThighBone: -1,
        Item.WitheredTentacle: -1
    }

    rubbery_collector_buyers.add_trade(config, Flux.Amalgamy, ZooType.Bird, coral_bird_eight_recipe)

    # rubbery_collector_trade(config,
    #     recipe={
    #         Item.Action: -12,
    #         Item.AmalgamyBirdAction: -12,
    #         Item.SkeletonWithSevenNecks: -1,
    #         Item.SkullInCoral: -7,
    #         Item.AlbatrossWing: -2
    #     },
    #     zoo_type=ZooType.Bird,
    #     fluctuations=Flux.Amalgamy, debug=True)

    # Recipes selected by the model
    brass_bird_recipes = [
        # Bone Fragment or Bombazine generator, any Bird week
        {
            Item.Action: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -7,
            Item.WingOfAYoungTerrorBird: -2
        },        
        # more Bone Fragment generators, any Bird week
        # not sure why model has so many variations         
        {
            Item.Action: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -6,
            Item.DuplicatedVakeSkull: -1,
            Item.WingOfAYoungTerrorBird: -2
        },
        {
            Item.Action: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -4,
            Item.SabreToothedSkull: -2,
            Item.DuplicatedVakeSkull: -1,
            Item.WingOfAYoungTerrorBird: -2
        },
        # 11 Amalgamy, 4 exhaustion, any Bird week
        {
            Item.Action: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.BrightBrassSkull: -3,
            Item.SkullInCoral: -4,
            Item.AlbatrossWing: -1,
            Item.WingOfAYoungTerrorBird: -1
        },
        # MoDS generaetor, any week?
        {
            Item.Action: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.SkullInCoral: -4,
            Item.HornedSkull: -2,
            Item.BrightBrassSkull: -1,
            Item.WingOfAYoungTerrorBird: -2
        }
    ]

    for recipe in brass_bird_recipes:
        entrepreneur_buyers.add_trade(config, Flux.Amalgamy, ZooType.Bird, recipe)
        entrepreneur_buyers.add_trade(config, Flux.Amalgamy, ZooType.NoType, recipe)
        entrepreneur_buyers.add_trade(config, Flux.NoQuality, ZooType.NoType, recipe)

        paleo_buyers.add_trade(config, Flux.NoQuality, ZooType.Bird, recipe)
        paleo_buyers.add_trade(config, Flux.NoQuality, ZooType.NoType, recipe)
        
        zailor_particular_buyers.add_trade(config, Flux.NoQuality, ZooType.Bird, recipe)
        zailor_particular_buyers.add_trade(config, Flux.NoQuality, ZooType.NoType, recipe)

        # naive_buyers.add_trade(config, Flux.NoQuality, ZooType.Bird, recipe)
        # naive_buyers.add_trade(config, Flux.NoQuality, ZooType.NoType, recipe)

    # ------------------------------------------------
    # ------------ Thorned Ribcage ---------------
    # ------------------------------------------------

    thorned_jurassic_bird_recipe = {
        Item.Action: -9,
        Item.ThornedRibcage: -1,
        Item.DoubledSkull: -1,
        Item.FemurOfAJurassicBeast: -2,
        Item.WingOfAYoungTerrorBird: -2,
        Item.ObsidianChitinTail: -1
    }

    gothic_tales_buyers.add_trade(config, Flux.Antiquity, ZooType.Bird, thorned_jurassic_bird_recipe)
    zailor_particular_buyers.add_trade(config, Flux.Antiquity, ZooType.Bird, thorned_jurassic_bird_recipe)

    # use other items from doubled skull farm
    # 7 amalgamy humanoid
    thorned_humanoid_recipe = {
        Item.Action: -9,
        Item.ThornedRibcage: -1,
        Item.BrightBrassSkull: -1,
        Item.KnottedHumerus: -2,
        Item.HelicalThighbone: -2,
    }

    entrepreneur_buyers.add_trade(config, Flux.Amalgamy, ZooType.Primate, thorned_humanoid_recipe)

    # 7 amalgamy reptile
    for tail_type in (Item.JetBlackStinger, Item.PlasterTailBones, Item.TombLionsTail):
        thorned_reptile_recipe = utils.sum_dicts(thorned_humanoid_recipe, {
            Item.JetBlackStinger: -1,
        })
        entrepreneur_buyers.add_trade(config, Flux.Amalgamy, ZooType.Reptile, thorned_reptile_recipe)


    for filler_leg in (
        Item.FemurOfASurfaceDeer,
        Item.UnidentifiedThighBone,
        Item.FemurOfAJurassicBeast,
        Item.HelicalThighbone,
        Item.HolyRelicOfTheThighOfStFiacre,
        Item.IvoryFemur):

        thorned_menace_bird_recipe = {
            Item.Action: -9,
            Item.ThornedRibcage: -1,
            Item.HornedSkull: -1,
            filler_leg: -2,
            Item.WingOfAYoungTerrorBird: -2,
            Item.JetBlackStinger: -1,
        }

        teller_buyers.add_trade(config, Flux.Menace, ZooType.Bird, thorned_menace_bird_recipe)
        teller_buyers.add_trade(config, Flux.Menace, ZooType.NoType, thorned_menace_bird_recipe)

    # wtf is this
    # oh right trying to use all the parts of the fox sighting
    # zailor_particular_trade(trade, player,
    #     recipe={
    #         Item.Action: -9,
    #         Item.AntiquityGeneralAction: -9,
    #         Item.ThornedRibcage: -1,
    #         Item.DoubledSkull: -1,
    #         Item.KnottedHumerus: -2,
    #         Item.HelicalThighbone: -1,
    #         Item.FinBonesCollected: -1,
    #         Item.TombLionsTail: -1
    #     },
    #     zoo_type=ZooType.Chimera,
    #     fluctuations=Flux.Antiquity)       

    # ==============================================================
    #                   Glim-encrusted Carapace
    # ==============================================================    


    # trade(0, {
    #     Item.Action: -11,
    #     Item.GeneralArachnidAction: -11,
    #     Item.GlimEncrustedCarapace: -1,
    #     Item.HolyRelicOfTheThighOfStFiacre: -8,

    #     Item.PreservedSurfaceBlooms: 78,
    #     Item.RumourOfTheUpperRiver: 40
    # })

    sculptress_buyer.add_trade(config, Flux.NoQuality, ZooType.Spider,
        # TODO confirm this all ties out
        recipe={
            Item.Action: -12,
            Item.GlimEncrustedCarapace: -1,
            Item.CarvedBallOfStygianIvory: -1,
            Item.HolyRelicOfTheThighOfStFiacre: -8
        })


    # ==============================================================
    #                   Prismatic Frame
    # ==============================================================
    for skull in (
        Item.DuplicatedVakeSkull,
        Item.BrightBrassSkull,
        Item.SabreToothedSkull,
        Item.HornedSkull,
    ):
        for amber_fins in (0,1,2,3):

            prismatic_fish = {
                Item.Action: -11,
                Item.PrismaticFrame: -1,
                Item.CarvedBallOfStygianIvory: -2,
                skull: -1,
                Item.AmberCrustedFin: -amber_fins,
                Item.FinBonesCollected: -3 + amber_fins,
                Item.JetBlackStinger: -1
            }

            gothic_tales_buyers.add_trade(config, Flux.Antiquity, ZooType.Fish, prismatic_fish)
            gothic_tales_buyers.add_trade(config, Flux.Menace, ZooType.Fish, prismatic_fish)

            rubbery_collector_buyers.add_trade(config, Flux.Menace, ZooType.Fish, prismatic_fish)

    # ==============================================================
    #                   Trifling Diplomat
    # ==============================================================

    diplomat_triple_buyer.add_trade(config, Flux.NoQuality, ZooType.NoType,
        recipe={
            Item.Action: -12,
            Item.SkeletonWithSevenNecks: -1,
            Item.HornedSkull: -4,
            Item.DuplicatedVakeSkull: -2,
            Item.BrightBrassSkull: -1,
            Item.WingOfAYoungTerrorBird: -2,

            Item._TriflingDiplomatSale: -1
        })

    ##################################################################
    #            The Seven-Necked Combinatoric Shitshow
    ##################################################################

    # # Define the target sum
    # seven_skulls = 7

    '''
    TODO make this more efficient
    # IDEAS

    tries EVERY combination of skulls that add up to seven
    - involving 1 or 2 skull types
    - involving 3 skull types where one is brass skull

    PROBLEM:
    this combinatoric search adds a HUGE number of trades to the model
    as of this comment, WITHOUT the bone market, the model has around 1000 trades
    the bone market, WITHOUT this search, adds another ~1000
    then this

    say we have 10 other skull types
    10 choose 2 = 45 pairings
    times 7 ways to split = 315 distributions
    except we are also considering 1-6 brass skulls
    so that's actually ~28 ways to split (minus a few with empty groups)
    45 skull pairs * 28 groupings = 1260 unique permutations
    definitely getting some of this math wrong, suffice it's on the order of 10^3
    but then you have 3 ways to add wings (2-0, 1-1, 0-2) 
    and ~10 buyer+flux+zoo combos to evaluate
    that means we're adding 30 to 40 THOUSAND trades 
    
    experimentally, that's about right.
    last time I ran the full search, we got an out of index error with a 20k buffer
    but 40k was enough

    this isn't a problem per se, except it takes ages to run.
    from "basically instant" to "several minutes"

    so it's not worth doing this every single time we make any change
    let's review where that size is coming from.
    in log terms we're at 10^4.5
    we want to get down to 10^3

    10 chose 2 skull pairings:  1.65
    7 ways to split 2 skulls:   0.85
    ~21 ways w/ brass skulls:   1.3
    10 buyer variants:          1.0
    3 unique wing splits:       0.5

    lots of options to shrink the search space by tweaking these params
    
    start by pruning buyers
    - remove the buyers that only care about total penny value
        - i.e. naive collector, hoarding paleo
        - just hand pick a few reasonable generators for them
        - or put them in an outer loop with only brass + 1 other skull type
    - for the other buyers, prune obviously bad skeletons
        - for the quadratic buyers, we only want these quality values:
            - 0 exhaustion: 1-4
            - 1 exhaustion: 7
            - 4 exhaustion: 11
            - and maybe 8 and/or 9 for 2/3 exhaustion
        - for the two quality buyers, not as obvious
            - let's say only use skeletons where the total is between 1 and 5 points
                under the next exhaustion threshold
    '''
    # for brass_skulls in range(seven_skulls + 1):
    #     other_skull_types = [
    #         Item.HornedSkull,
    #         Item.SkullInCoral,
    #         Item.SabreToothedSkull,
    #         # Item.PlatedSkull,
    #         # Item.PentagrammicSkull, 
    #         # Item.DuplicatedCounterfeitHeadOfJohnTheBaptist,
    #         Item.DuplicatedVakeSkull,
    #         Item.DoubledSkull,

    #         Item.FailedHornedSkull,
    #         Item.FailedSabreToothedSkull,
    #         # Item.FailedDoubledSkull,
    #         # Item.FailedSkullInCoral
    #     ]

    #     num_skull_types = len(other_skull_types)

    #     for i in range(0, num_skull_types):
    #         skull_type_1 = other_skull_types[i]
            
    #         for j in range(i + 1, num_skull_types):
    #             skull_type_2 = other_skull_types[j]

    #             # Iterate over possible values of b
    #             for num_skull_1 in range(seven_skulls + 1 - brass_skulls):

    #                 # Calculate the value of c
    #                 num_skull_2 = seven_skulls - brass_skulls - num_skull_1

    #                 # for k in range(0, 3):
    #                 generator_bird_recipe = {
    #                         Item.Action: -12,
    #                         Item.SkeletonWithSevenNecks: -1,
    #                         Item.BrightBrassSkull: -1 * brass_skulls,
    #                         skull_type_1: -1 * num_skull_1,
    #                         skull_type_2: -1 * num_skull_2,
    #                         # Item.AlbatrossWing: -2,
    #                         Item.WingOfAYoungTerrorBird: -2
    #                 }

    #                 entrepreneur_buyers[Flux.Amalgamy][ZooType.Bird].add_trade(config, generator_bird_recipe)
    #                 entrepreneur_buyers[Flux.NoQuality][ZooType.Bird].add_trade(config, generator_bird_recipe)
    #                 # entrepreneur_buyers[Flux.Amalgamy][ZooType.NoType].add_trade(config, generator_bird_recipe)
    #                 entrepreneur_buyers[Flux.NoQuality][ZooType.NoType].add_trade(config, generator_bird_recipe)

    #                 # Memory of Distant Shores & Volumes of Collated Research
    #                 tentacled_entrepreneur_trade(config,
    #                     recipe={
    #                         Item.Action: -12,
    #                         Item.AmalgamyBirdAction: -12,
    #                         Item.SkeletonWithSevenNecks: -1,
    #                         Item.BrightBrassSkull: -1 * brass_skulls,
    #                         skull_type_1: -1 * num_skull_1,
    #                         skull_type_2: -1 * num_skull_2,
    #                         Item.AlbatrossWing: -2
    #                     },
    #                     zoo_type=ZooType.Bird,
    #                     fluctuations=Flux.Amalgamy)
                    
    #                 tentacled_entrepreneur_trade(config,
    #                     recipe={
    #                         Item.Action: -12,
    #                         Item.GeneralBirdAction: -12,
    #                         Item.SkeletonWithSevenNecks: -1,
    #                         Item.BrightBrassSkull: -1 * brass_skulls,
    #                         skull_type_1: -1 * num_skull_1,
    #                         skull_type_2: -1 * num_skull_2,
    #                         Item.WingOfAYoungTerrorBird: -2
    #                     },
    #                     zoo_type=ZooType.Bird,
    #                     fluctuations=Flux.NoQuality)            

    #                 # Bone Fragments
    #                 hoarding_paleo_trade(trade, player,
    #                     recipe={
    #                         Item.Action: -12,
    #                         Item.GeneralBirdAction: -12,
    #                         Item.SkeletonWithSevenNecks: -1,
    #                         Item.BrightBrassSkull: -1 * brass_skulls,
    #                         skull_type_1: -1 * num_skull_1,
    #                         skull_type_2: -1 * num_skull_2,
    #                         Item.WingOfAYoungTerrorBird: -2
    #                     },
    #                     zoo_type=ZooType.Bird,
    #                     fluctuations=Flux.NoQuality)                           

    #                 zailor_particular_trade(trade, player,
    #                     recipe={
    #                         Item.Action: -12,
    #                         Item.GeneralBirdAction: -12,
    #                         Item.SkeletonWithSevenNecks: -1,
    #                         Item.BrightBrassSkull: -1 * brass_skulls,
    #                         skull_type_1: -1 * num_skull_1,
    #                         skull_type_2: -1 * num_skull_2,
    #                         Item.WingOfAYoungTerrorBird: -2
    #                     },
    #                     zoo_type=ZooType.Bird,
    #                     fluctuations=Flux.NoQuality)


    #                 naive_collector_trade(trade, player,
    #                     recipe={
    #                         Item.Action: -12,
    #                         Item.GeneralBirdAction: -12,
    #                         Item.SkeletonWithSevenNecks: -1,
    #                         Item.BrightBrassSkull: -1 * brass_skulls,
    #                         skull_type_1: -1 * num_skull_1,
    #                         skull_type_2: -1 * num_skull_2,
    #                         Item.WingOfAYoungTerrorBird: -2
    #                     },
    #                     zoo_type=ZooType.Bird,
    #                     fluctuations=Flux.NoQuality)       




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