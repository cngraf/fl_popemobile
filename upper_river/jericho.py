import itertools
from enums import *
from utils import *
from config import Config
# from optimize import *

def add_trades(config: Config):
    trade = config.trade
    player = config.player
    add = config.add

    for i in range(0, 11):
        visit_length = 2 ** i
        add({
            Item._UpperRiverRoundTrip: -1,
            Item.Action: -1 * visit_length,
            Item._JerichoAction: visit_length,
            Item._JerichoFavourExchange: 1
        })

    # --------- Canal Cruising

    if player.profession == Profession.CrookedCross:
        add({
            Item._JerichoAction: -1,
            Item.UnprovenancedArtefact: -4,
            Item.EsteemOfTheGuild: 1
        })

    add({
        Item._JerichoAction: -1,
        Item.VolumeOfCollatedResearch: -10,
        Item.EsteemOfTheGuild: 2
    })

    add({
        Item._JerichoAction: -1,
        Item.PartialMap: -6,
        Item.AnIdentityUncovered: -4,
        Item.EsteemOfTheGuild: 2
    })

    add({
        Item._JerichoAction: -1,
        Item.MemoryOfDistantShores: -40,
        Item.SwornStatement: -2,
        Item.EsteemOfTheGuild: 2
    })

    add({
        Item._JerichoAction: -1,
        Item.NightOnTheTown: -1,
        Item.ScrapOfIncendiaryGossip: -45,
        Item.EsteemOfTheGuild: 2
    })

    add({
        Item._JerichoAction: -1,
        Item.FavDocks: -5,
        Item.EsteemOfTheGuild: 2
    })

    # assume ranges are evenly distributed
    add({
        Item._JerichoAction: -2,
        Item.EsteemOfTheGuild: -3,
        Item.VitalIntelligence: 2.5,
        Item.ViennaOpening: 6.5
    })

    add({
        Item._JerichoAction: -2,
        Item.EsteemOfTheGuild: -3,
        Item.MirrorcatchBox: 1
    })

    add({
        Item._JerichoAction: -2,
        Item.EsteemOfTheGuild: -3,
        Item.MoonlightScales: 50,
        Item.FinBonesCollected: 5,
        Item.SkullInCoral: 1.5,
        Item.UnprovenancedArtefact: 8.5
    })

    # upper river destinations

    add({
        Item._JerichoAction: -2,
        Item.EsteemOfTheGuild: -6,
        Item.BrightBrassSkull: 1,
        Item.ExtraordinaryImplication: 5.5,
        Item.VerseOfCounterCreed: 2.5
    })

    add({
        Item._JerichoAction: -2,
        Item.EsteemOfTheGuild: -6,
        Item.MovesInTheGreatGame: 18.5,
        Item.PrimaevalHint: 1,
        Item.UncannyIncunabulum: 2.5
    })

    add({
        Item._JerichoAction: -2,
        Item.EsteemOfTheGuild: -6,
        Item.NightWhisper: 1,
        Item.TaleOfTerror: 3.5,
        Item.FinalBreath: 12,
        Item.HumanRibcage: 2
    })


    # --------- Calling in Favours
    # hack to model dipping into jericho to trade favours
    # when you would otherwise not go there

    # jericho_add = 0.0
    # def jericho_trade(exchange):
    #     exchange[Item.RumourOfTheUpperRiver] = jericho_add
    #     trade(1 + jericho_add, exchange)

    favour_trades = {
        Item.FavBohemians: {
            Item.IvoryHumerus: 2,
            Item.WingOfAYoungTerrorBird: 2
        },
        Item.FavChurch: {
            Item.RattyReliquary: 2,
            Item.ApostatesPsalm: 2
        },
        Item.FavConstables: {
            Item.CaveAgedCodeOfHonour: 2,
            Item.SwornStatement: 2
        },
        Item.FavCriminals: {
            Item.HumanRibcage: 2,
            Item.BoneFragments: 500
        },
        Item.FavDocks: {
            Item.UncannyIncunabulum: 2,
            Item.KnobOfScintillack: 2
        },
        Item.FavGreatGame: {
            Item.ViennaOpening: 2,
            Item.QueenMate: 1
        },
        Item.FavHell: {
            Item.ThornedRibcage: 2,
            Item.QueerSoul: 2
        },
        Item.FavRevolutionaries: {
            Item.UnlawfulDevice: 2,
            Item.ThirstyBombazineScrap: 2
        },
        Item.FavRubberyMen: {
            Item.FlourishingRibcage: 2,
            Item.BasketOfRubberyPies: 2
        },
        Item.FavSociety: {
            Item.FavourInHighPlaces: 2,
            Item.NightOnTheTown: 2
        },
        Item.FavTombColonies: {
            Item.AntiqueMystery: 2,
            Item.UnprovenancedArtefact: 2
        },
        Item.FavUrchins: {
            Item.StormThrenody: 2,
            Item.AeolianScream: 2
        }
    }

    for favour, reward in favour_trades.items():
        costs = {
            Item._JerichoFavourExchange: -1,
            Item._JerichoAction: -1,
            favour: -4
        }

        full_trade = sum_dicts(
            costs,
            reward
        )

        add(full_trade)    

    for trade1, trade2 in itertools.combinations(favour_trades.items(), 2):
        favour1 = trade1[0]
        favour2 = trade2[0]
        reward1 = trade1[1]
        reward2 = trade2[1]

        costs = {
            Item._JerichoFavourExchange: -1,
            Item._JerichoAction: -2,
            favour1: -4,
            favour2: -4,
        }

        full_trade = sum_dicts(
            costs,
            reward1,
            reward2
        )

        add(full_trade)

    # # 3 vs. 2 doesn't make a huge difference , ~0.01 EPA even with cards
    # for trade1, trade2, trade3 in itertools.combinations(favour_trades.items(), 3):
    #     favour1 = trade1[0]
    #     favour2 = trade2[0]
    #     favour3 = trade3[0]
    #     reward1 = trade1[1]
    #     reward2 = trade2[1]
    #     reward3 = trade3[1]

    #     costs = {
    #         Item._JerichoFavourExchange: -1,
    #         Item._JerichoAction: -3,
    #         favour1: -4,
    #         favour2: -4,
    #         favour3: -4,
    #     }

    #     full_trade = sum_dicts(
    #         costs,
    #         reward1,
    #         reward2,
    #         reward3,
    #     )

    #     add(full_trade)

    # Library
    add({
        Item._JerichoAction: -1,
        Item.RevisionistHistoricalNarrative: -1,
        Item.HinterlandScrip: 30
    })
    
    add({
        Item._JerichoAction: -1,
        Item.CorrectiveHistoricalNarrative: -1,
        Item.HinterlandScrip: 30
    })

    add({
        Item._JerichoAction: -1,
        Item.CorrectiveHistoricalNarrative: -2,
        Item.RevisionistHistoricalNarrative: -3,
        Item.NightWhisper: 1
    })

    # Library studies
    # AFAICT no way to improve on these rates

    add({
        Item._JerichoAction: -22,
        Item.FalseHagiotoponym: 1
    })

    add({
        Item._JerichoAction: -22,
        Item.OneiromanticRevelation: 1
    })

    add({
        Item._JerichoAction: -22,
        Item.PrimaevalHint: 1
    })