from enums import *
from utils import *
# from optimize import *

def add_trades(active_player, config):
    trade = config.trade
    add = config.add

    visit_length = 10

    add({
        Item.RootAction: -1 * (visit_length + 1),
        Item.JerichoAction: visit_length,
        Item.RumourOfTheUpperRiver: 1
    })

    # --------- Canal Cruising

    if active_player.profession == Profession.CrookedCross:
        add({
            Item.JerichoAction: -1,
            Item.UnprovenancedArtefact: -4,
            Item.EsteemOfTheGuild: 1
        })

    add({
        Item.JerichoAction: -1,
        Item.VolumeOfCollatedResearch: -10,
        Item.EsteemOfTheGuild: 2
    })

    add({
        Item.JerichoAction: -1,
        Item.PartialMap: -6,
        Item.AnIdentityUncovered: -4,
        Item.EsteemOfTheGuild: 2
    })

    add({
        Item.JerichoAction: -1,
        Item.MemoryOfDistantShores: -40,
        Item.SwornStatement: -2,
        Item.EsteemOfTheGuild: 2
    })

    add({
        Item.JerichoAction: -1,
        Item.NightOnTheTown: -1,
        Item.ScrapOfIncendiaryGossip: -45,
        Item.EsteemOfTheGuild: 2
    })

    add({
        Item.JerichoAction: -1,
        Item.FavDocks: -5,
        Item.EsteemOfTheGuild: 2
    })

    # assume ranges are evenly distributed
    add({
        Item.JerichoAction: -2,
        Item.EsteemOfTheGuild: -3,
        Item.VitalIntelligence: 2.5,
        Item.ViennaOpening: 6.5
    })

    add({
        Item.JerichoAction: -2,
        Item.EsteemOfTheGuild: -3,
        Item.MirrorcatchBox: 1
    })

    add({
        Item.JerichoAction: -2,
        Item.EsteemOfTheGuild: -3,
        Item.MoonlightScales: 50,
        Item.FinBonesCollected: 5,
        Item.SkullInCoral: 1.5,
        Item.UnprovenancedArtefact: 8.5
    })

    # upper river destinations

    add({
        Item.JerichoAction: -2,
        Item.EsteemOfTheGuild: -6,
        Item.BrightBrassSkull: 1,
        Item.ExtraordinaryImplication: 5.5,
        Item.VerseOfCounterCreed: 2.5
    })

    add({
        Item.JerichoAction: -2,
        Item.EsteemOfTheGuild: -6,
        Item.MovesInTheGreatGame: 18.5,
        Item.PrimaevalHint: 1,
        Item.UncannyIncunabulum: 2.5
    })

    add({
        Item.JerichoAction: -2,
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

    add({
        Item.JerichoAction: -1,
        Item.FavBohemians: -4,
        Item.HolyRelicOfTheThighOfStFiacre: 2,
        Item.WingOfAYoungTerrorBird: 1,
    })

    add({
        Item.JerichoAction: -1,
        Item.FavChurch: -4,
        Item.RattyReliquary: 2,
        Item.ApostatesPsalm: 1,
    })

    add({
        Item.JerichoAction: -1,
        Item.FavConstables: -4,
        Item.CaveAgedCodeOfHonour: 2,
        Item.SwornStatement: 1
    })

    add({
        Item.JerichoAction: -1,
        Item.FavCriminals: -4,
        Item.HumanRibcage: 2,
        Item.HumanArm: 1
    })

    add({
        Item.JerichoAction: -1,
        Item.FavDocks: -4,
        Item.UncannyIncunabulum: 2,
        Item.KnobOfScintillack: 1
    })

    add({
        Item.JerichoAction: -1,
        Item.FavGreatGame: -4,
        Item.ViennaOpening: 1,
        Item.QueenMate: 1
    })

    add({
        Item.JerichoAction: -1,
        Item.FavHell: -4,
        Item.ThornedRibcage: 2,
        Item.QueerSoul: 1
    })

    add({
        Item.JerichoAction: -1,
        Item.FavRevolutionaries: -4,
        Item.UnlawfulDevice: 2,
        Item.ThirstyBombazineScrap: 1
    })

    add({
        Item.JerichoAction: -1,
        Item.FavRubberyMen: -4,
        Item.FlourishingRibcage: 2,
        Item.BasketOfRubberyPies: 1,
    })

    add({
        Item.JerichoAction: -1,
        Item.FavSociety: -4,
        Item.FavourInHighPlaces: 2,
        Item.NightOnTheTown: 1
    })

    add({
        Item.JerichoAction: -1,
        Item.FavTombColonies: -4,
        Item.AntiqueMystery: 2,
        Item.UnprovenancedArtefact: 1,
    })

    add({
        Item.JerichoAction: -1,
        Item.FavUrchins: -4,
        Item.StormThrenody: 2,
        Item.AeolianScream: 1
    })

    # Library
    add({
        Item.JerichoAction: -1,
        Item.RevisionistHistoricalNarrative: -1,
        Item.HinterlandScrip: 30
    })
    
    add({
        Item.JerichoAction: -1,
        Item.CorrectiveHistorialNarrative: -1,
        Item.HinterlandScrip: 30
    })

    add({
        Item.JerichoAction: -1,
        Item.CorrectiveHistorialNarrative: -2,
        Item.RevisionistHistoricalNarrative: -3,
        Item.NightWhisper: 1
    })