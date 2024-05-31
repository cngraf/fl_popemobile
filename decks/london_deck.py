from enums import *
# from utils import *
import utils
from config import Config
from player import Player
from decks.deck import *

import random


def add_trades(config: Config):
    trade = config.trade
    add = config.add
    player = config.player

    cards = [
        Card(Item.CL_AVisit, ),

        Card(Item.CL_Bohemians),
        Card(Item.CL_Church),    
        Card(Item.CL_Constables),
        Card(Item.CL_Criminals),
        Card(Item.CL_Docks),
        Card(Item.CL_GreatGame),
        Card(Item.CL_Hell),
        Card(Item.CL_Revolutionaries),
        Card(Item.CL_RubberyMen),
        Card(Item.CL_Society),                            
        Card(Item.CL_TombColonies),                            
        Card(Item.CL_Urchins),

        # Companions
        Card(Item.CL_ConnectedPet),

        # Spouses
        Card(Item.CL_BewilderingProcessionSpouse, freq=Rarity.VeryInfrequent),

        # Equipment
        Card(Item.CL_ClaySedanChair),

        # Lodgings
        Card(Item.CL_SmokyFlophouse),
        Card(Item.CL_HandsomeTownhouse, freq=Rarity.Frequent),
        Card(Item.CL_PremisesAtTheBazaar, freq=Rarity.Frequent),
        Card(Item.CL_LairInTheMarshes),

        # Clubs
        Card(Item.CL_YoungStags),

        # Dreams
        Card(Item.CL_Dreams1),
        Card(Item.CL_Dreams2),
        Card(Item.CL_Dreams3),
        Card(Item.CL_Dreams4),
        Card(Item.CL_Dreams5),

        Card(Item.CL_TheSeekersOfTheGarden),
        Card(Item.CL_ATradeInSouls),
        Card(Item.CL_YourAunt),

        # all TODO
        Card(Item.CL_TournamentOfWeasels, freq=Rarity.Unusual),
        Card(Item.CL_OrthographicInfection),
        Card(Item.CL_CityVicesDecadentEvening),
        Card(Item.CL_ARestorative),
        Card(Item.CL_AfternoonOfGoodDeeds), # done
        Card(Item.CL_AMomentsPeace, freq=Rarity.VeryInfrequent),
        Card(Item.CL_TheInterpreterOfDreams, freq=Rarity.Unusual),
        Card(Item.CL_AnImplausiblePenance),
        Card(Item.CL_DevicesAndDesires),
        Card(Item.CL_APoliteInvitation),
        Card(Item.CL_GiveAGift), # done
        Card(Item.CL_ADayAtTheRaces), # done
        Card(Item.CL_OnesPublic),
        Card(Item.CL_GodsEditors), # done
        Card(Item.CL_BringingTheRevolution),
        Card(Item.CL_MirrorsAndClay),
        Card(Item.CL_TheCitiesThatFell),
        Card(Item.CL_TheSoftHeartedWidow),
        Card(Item.CL_AllFearTheOvergoat),
        Card(Item.CL_TheNorthboundParliamentarian),
        Card(Item.CL_Arbor),
        Card(Item.CL_WeatherAtLast),
        Card(Item.CL_AnUnusualWager),
        Card(Item.CL_MrWinesIsHoldingASale),
        Card(Item.CL_TheAwfulTemtpationfMoney),
        Card(Item.CL_InvestigatingTheAffluentPhotographer),
        Card(Item.CL_TheGeologyOfWinewound),
        Card(Item.CL_APublicLecture),
        Card(Item.CL_WantedRemindersOfBrighterDays),
        Card(Item.CL_AnUnsignedMessage, freq=Rarity.VeryInfrequent),
        Card(Item.CL_APresumptuousLittleOpportunity, freq=Rarity.VeryInfrequent),
        Card(Item.CL_SLowcakesAmanuensis, freq=Rarity.Infrequent),
        Card(Item.CL_AMerrySortOfCrime, freq=Rarity.VeryInfrequent),
        Card(Item.CL_ADustyBookshop, freq=Rarity.Rare),
        Card(Item.CL_ALittleOmen, freq=Rarity.Rare),
        Card(Item.CL_ADisgracefulSpectacle, freq=Rarity.Rare),
        Card(Item.CL_AVoiceFromAWell, freq=Rarity.Rare),
        Card(Item.CL_AFineDayInTheFlit, freq=Rarity.Unusual),
        Card(Item.CL_TheParanomasticNewshound, freq=Rarity.Unusual),
        Card(Item.CL_Relicker1, freq=Rarity.VeryInfrequent),
        Card(Item.CL_Relicker2, freq=Rarity.VeryInfrequent),
        Card(Item.CL_Relicker3, freq=Rarity.VeryInfrequent),
        Card(Item.CL_Relicker4, freq=Rarity.VeryInfrequent),
    ]

    deck_size = sum(i.freq.value for i in cards)

    draw_conversion = {
        Item.LondonDraw: -1,
    }

    for card in cards:
        draw_rate = card.freq.value / (deck_size - Rarity.Standard.value * 4)
        draw_conversion[card.item] = draw_rate

    config.trade(0, {Item.CardDraws: -1, Item.LondonDraw: 1})
    config.trade(0, draw_conversion)

    base_watchful = 230
    base_shadowy = 230
    base_dangerous = 230
    base_persuasive = 230
    wounds_multiplier = menace_multiplier(player.wounds_reduction)
    suspicion_multiplier = menace_multiplier(player.suspicion_reduction)
    scandal_multiplier = menace_multiplier(player.scandal_reduction)    
    nightmares_multiplier = menace_multiplier(player.nightmares_reduction)


    # ----------------------------------------------------
    # --- Factions
    # ----------------------------------------------------    

    trade(0, {
        Item.Action: -1,
        Item.CL_Bohemians: -1,

        Item.FoxfireCandleStub: -20,
        Item.BottleOfGreyfields1882: -15,
        Item.Scandal: 1 * scandal_multiplier,
        Item.FavBohemians: 1
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_Church: -1,
        Item.PieceOfRostygold: -10,

        Item.FavChurch: 1,
        Item.AirsOfLondonChange: 1
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_Constables: -1,
        Item.PieceOfRostygold: -10,

        Item.FavConstables: 1,
        Item.AirsOfLondonChange: 1
    })    

    trade(0, {
        Item.Action: -1,
        Item.CL_Criminals: -1,

        Item.FavCriminals: 1,
        Item.Suspicion: 1 * suspicion_multiplier
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_Docks: -1,
        Item.PieceOfRostygold: -10,

        Item.FavDocks: 1
    })    

    trade(0, {
        Item.Action: -1,
        Item.CL_GreatGame: -1,

        Item.FavGreatGame: 1,
        Item.Wounds: 1 * wounds_multiplier
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_Hell: -1,

        Item.FavHell: 1,
        Item.Suspicion: 1 * suspicion_multiplier
    })


    trade(0, {
        Item.Action: -1,
        Item.CL_Revolutionaries: -1,
        Item.VisionOfTheSurface: -1,

        Item.FavRevolutionaries: 1,
        Item.Suspicion: 1 * suspicion_multiplier
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_RubberyMen: -1,
        Item.NoduleOfWarmAmber: -1,

        Item.NoduleOfDeepAmber: 50,
        Item.FavRubberyMen: 1
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_RubberyMen: -1,
        Item.NoduleOfWarmAmber: -100,
        
        Item.NoduleOfTremblingAmber: 1,
        Item.FavRubberyMen: 1
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_RubberyMen: -1,
        Item.NoduleOfWarmAmber: -100,
        
        Item.NoduleOfTremblingAmber: 1,
        Item.FavRubberyMen: 1
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_Society: -1,
        Item.ScrapOfIncendiaryGossip: -1,
        
        Item.FavSociety: 1,
        Item.ScrapOfIncendiaryGossip: 1 * suspicion_multiplier
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_TombColonies: -1,
        
        Item.FavTombColonies: 1,
    })

    add({
        Item.Action: -1,
        Item.CL_TombColonies: -1,
        Item.FavTombColonies: -1,
        Item.CollectionOfCuriosities: -1,

        Item.PuzzlingMap: 5,
        Item.ExtraordinaryImplication: 1
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_Urchins: -1,
        Item.LuckyWeasel: -1,
        
        Item.FavUrchins: 1,
    })

    # Requires FATE story
    # trade(0, {
    #     Item.Action: -1,
    #     Item.CL_Urchins: -1,
        
    #     Item.FavUrchins: 1,
    #     Item.Nightmares: -2
    # })

    # ----------------------------------------------------
    # --- General
    # ----------------------------------------------------

    trade(0, {
        Item.Action: -1,
        Item.CL_AVisit: -1,

        Item.CrypticClue: base_shadowy,
        Item.FavCriminals: 1,
        Item.FavBohemians: 1
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_AVisit: -1,

        Item.WhisperedHint: 50 + base_dangerous,
        Item.RatOnAString: 50 + base_dangerous,
        Item.FavDocks: 1,
        Item.FavConstables: 1
    })

    trade(0, {
        Item.Action: -1,        
        Item.CL_AVisit: -1,

        Item.WhisperedHint: base_persuasive * 1.5,
        Item.FavBohemians: 1,
        Item.FavSociety: 1
    })

    trade(0, {
        Item.Action: -1,        
        Item.CL_AVisit: -1,

        Item.CrypticClue: base_watchful,
        Item.FavGreatGame: 1,
        Item.FavSociety: 1
    })    

    # ----------------------------------------------------
    # --- Companions & Spouses
    # ----------------------------------------------------

    # TODO: require lock-in
    for favour in (
        Item.FavBohemians,
        Item.FavChurch,
        Item.FavConstables,
        Item.FavCriminals,
        Item.FavDocks,
        Item.FavGreatGame,
        Item.FavHell,
        Item.FavRevolutionaries,
        Item.FavRubberyMen,
        Item.FavSociety,
        Item.FavTombColonies,
        Item.FavUrchins):
        add({
            Item.Action: -1,
            Item.CL_ConnectedPet: -1,
            favour: 1})
        
        # HACK
        add({
            Item.FavourableCircumstance: -1,
            favour: 1
        })
        
    trade(0, {
        Item.Action: -1,
        Item.CL_BewilderingProcessionSpouse: -1,

        Item.FavBohemians: 1
    })


    # -----------------------------------------------------
    # --- Cards: Other Equipment
    # ----------------------------------------------------

    trade(0, {
        Item.Action: -1,
        Item.CL_ClaySedanChair: -1,

        Item.FavSociety: 1,
        Item.Hedonist: -3
    })

    # -----------------------------------------------------
    # --- Cards: Clubs
    # ----------------------------------------------------

    trade(0, {
        Item.Action: -1,
        Item.CL_YoungStags: -1,

        Item.PieceOfRostygold: -500,
        Item.FavSociety: 2,
        Item.FavBohemians: 1
    })

    # ----- Lodgings ----------

    # ehh not sure about this format
    rare_success_rate = 0.05
    config.weighted_trade(
        {
            Item.Action: -1,
            Item.CL_SmokyFlophouse: -1,
        },
        (1.0 - rare_success_rate, {
            Item.FavCriminals: 0.5,
            Item.FavRevolutionaries: 0.05
        }),
        (rare_success_rate, {
            Item.AeolianScream: 1
        })
    )

    trade(0, {
        Item.Action: -1,
        Item.CL_LairInTheMarshes: -1,

        Item.FavSociety: 1,
        Item.CertifiableScrap: 1,
        Item.Nightmares: 1 * nightmares_multiplier
    })

    trade(0, {
        Item.Action: -1,
        Item.CL_HandsomeTownhouse: -1,
        Item.Scandal: 2 * scandal_multiplier,
        Item.Hedonist: 3,
        Item.FavBohemians: 0.5,
        Item.FavSociety: 0.5
    })

    config.challenge_trade(
        stat=Stat.APlayerOfChess,
        dc=9,
        cost={
            Item.Action: -1,
            Item.CL_PremisesAtTheBazaar: -1
        },
        on_pass={
            Item.TouchingLoveStory: 1.5,
            Item.StolenKiss: 1.5,
            Item.NightsoilOfTheBazaar: 2            
        },
        on_fail={
            Item.Echo: -2,
            Item.Scandal: 1
        })
    
    # ----------------------------------------------------
    # --- General
    # ----------------------------------------------------    

    add({
        # TODO: unique hallowmas option looks pretty good too
        Item.CL_AfternoonOfGoodDeeds: -1,
        Item.Action: -1,

        Item.FavHell: 1,
        Item.ConfidentSmile: 1,
        Item.Scandal: 2 * scandal_multiplier,
        Item.JadeFragment: 10
    })

    add({
        Item.CL_GiveAGift: -1,
        Item.Action: -1,

        Item.ConfidentSmile: 1,
        Item.HardEarnedLesson: 1,
        Item.SuddenInsight: 1,
        Item.HastilyScrawledWarningNote: 1        
    })

    add({
        Item.CL_ADayAtTheRaces: -1,
        Item.Action: -1,

        Item.FavChurch: 1
    })

    add({
        Item.CL_GodsEditors: -1,
        Item.Action: -1,
        Item.TaleOfTerror: -1,

        Item.FavChurch: 1
    })

    config.challenge_trade(
        stat=Stat.Persuasive,
        dc=220,
        cost={
            Item.CL_OnesPublic: -1,
            Item.Action: -1
        },
        on_pass={
            Item.PieceOfRostygold: 20,
            Item.JadeFragment: 20,
            Item.ConfidentSmile: 2,
            Item.PrimordialShriek: 30,
            Item.Echo: 1,
            Item.BottleOfGreyfields1879: 100
        },
        on_fail={
            Item.Scandal: 1
        }
    )

    # assume Evolution completed
    add({
        Item.Action: -1,
        Item.CL_TheSeekersOfTheGarden: -1,
        Item.ZeeZtory: -7, 

        Item.FavBohemians: 1,
        Item.FavDocks: 0.5,
        Item.FavSociety: 0.5,
        Item.Fascinating: 7
    })

    # FATE
    config.weighted_trade(
        {
            Item.Action: -1,
            Item.CL_YourAunt: -1,
            Item.BottleOfGreyfields1882: -50
        },
        (0.3, {
            Item.Action: 10
        }),
        (0.7, {
            Item.FavSociety: 1,
            Item.ScrapOfIncendiaryGossip: 3,
            Item.InklingOfIdentity: 5,
            Item.Scandal: -2
        })
    )

    # FATE
    add({
        Item.Action: -1,
        Item.CL_ATradeInSouls: -1,
        Item.Soul: -50,
        Item.InfernalContract: -5,

        Item.FavConstables: 1,
        Item.FavChurch: 1,
        Item.FavSociety: 1 
    })    

def create_deck_old(config: Config):
    replacement_epa = 6.5
    player = config.player
    wounds_multiplier = menace_multiplier(player.wounds_reduction)
    suspicion_multiplier = menace_multiplier(player.suspicion_reduction)
    scandal_multiplier = menace_multiplier(player.scandal_reduction)    
    nightmares_multiplier = menace_multiplier(player.nightmares_reduction)

    london_deck = Deck("London", -400)

    single_favours_enabled = False

    # Lair in the Marshes
    london_deck.card("Lair in the Marshes", Rarity.Standard, single_favours_enabled, {
        Item.FavSociety: 1,
        Item.CertifiableScrap: 1,
        Item.Nightmares: 1 * nightmares_multiplier
    })

    # The Tower of Knives: Difficulties at a Smoky Flophouse
    # The next victim?
    knives_rare_success_rate = 0.05
    london_deck.card("The Tower of Knives", Rarity.Standard, single_favours_enabled, {
        Item.FavCriminals: 0.5 - knives_rare_success_rate / 2.0,
        Item.FavRevolutionaries: 0.5 - knives_rare_success_rate / 2.0,
        Item.AeolianScream: knives_rare_success_rate
    })

    # The Tower of Eyes: Behind Closed Doors at a Handsome Townhouse
    # scandalous party
    london_deck.card("The Tower of Eyes", Rarity.Frequent, single_favours_enabled, {
        Item.FavBohemians: 0.5,
        Item.FavSociety: 0.5,
        Item.Hedonist: 3,
        Item.Scandal: 2 * scandal_multiplier
    })

    # The Tower of Sun and Moon: a Reservation at the Royal Bethlehem Hotel
    london_deck.card("Royal Beth lodings", Rarity.Frequent, False, {
        Item.CertifiableScrap: 3
    })

    london_deck.card("What will you do with your [connected pet]?", Rarity.Standard, single_favours_enabled, {
        Item.CL_ConnectedPet: 1
    })    

    # With Bewildering Procession
    london_deck.card("Attend to your spouses", Rarity.VeryInfrequent, single_favours_enabled, {
        Item.FavBohemians: 1
    })

    # avoidable
    london_deck.card("A day out in your Clay Sedan Chair", Rarity.Standard, single_favours_enabled, {
        Item.FavSociety: 1,
        Item.Hedonist: -3
    })

    london_deck.card("More Larks with the Young Stags", Rarity.Standard, True, {
        # Item.PieceOfRostygold: -500,
        Item.Echo: -5, # everyone has rostygold
        Item.FavSociety: 2,
        Item.FavBohemians: 1
    })

    # assuming you end up with 5 and they are all Unusual
    london_deck.card("omni-Dreams placeholder card", Rarity.Standard, False, {
        # TODO
    })    

        # Bohemians
    london_deck.card("Bohemians Faction", Rarity.Standard, single_favours_enabled, {
        Item.Echo: -1.2,
        Item.FavBohemians: 1
    })

    # Church
    london_deck.card("Church Faction", Rarity.Standard, single_favours_enabled, {
        Item.Echo: -0.1,
        Item.FavChurch: 1
    })

    # Constables
    london_deck.card("Constables Faction", Rarity.Standard, single_favours_enabled, {
        Item.Echo: -0.1,
        Item.FavConstables: 1
    })
    
    # Criminals
    london_deck.card("Criminals Faction", Rarity.Standard, single_favours_enabled, {
        Item.Suspicion: 1 * suspicion_multiplier,
        Item.FavCriminals: 1,
    })

    # Docks
    london_deck.card("Docks Faction", Rarity.Standard, single_favours_enabled, {
        Item.Echo: -0.1,
        Item.FavDocks: 1
    })

    # GreatGame
    london_deck.card("Great Game Faction", Rarity.Standard, False, {
        Item.Wounds: 1 * wounds_multiplier,
        Item.FavGreatGame: 1
    })

    # Hell
    london_deck.card("Burning Shadows: the Devils of London", Rarity.Standard, False, {
        Item.Scandal: 1 * scandal_multiplier,
        Item.FavHell: 1
    })

    # Revolutionaries
    london_deck.card("Rev Faction", Rarity.Standard, single_favours_enabled, {
        Item.Echo: -0.5,
        Item.FavRevolutionaries: 1 
    })

    # RubberyMen
    london_deck.card("Rubbery Faction", Rarity.Standard, False, {
        Item.Echo: -0.1,
        Item.FavRubberyMen: 1
    })    

    # Society
    london_deck.card("Society Faction", Rarity.Standard, single_favours_enabled, {
        Item.Echo: -0.5,
        Item.FavSociety: 1
    })

    # Tomb-Colonies
    london_deck.card("Tomb Colonies Faction", Rarity.Standard, False, {
        Item.FavTombColonies: 1
    })

    # With HOJOTOHO ending
    london_deck.card("Urchins Faction", Rarity.Standard, single_favours_enabled, {
        Item.FavUrchins: 1,
        Item.Nightmares: -2
    })

    # A tournament of weasels
    london_deck.card("A tournament of weasels", Rarity.Unusual, False, {
        # TODO
    })

    # Nightmares >= 1
    london_deck.card("Orthographic Infection", Rarity.Standard, False, {
        # TODO
    })

    # FavBohe >= 1
    london_deck.card("City Vices: A rather decadent evening", Rarity.Standard, False, {
        # TODO
    })

    # Wounds >= 2
    london_deck.card("A Restorative", Rarity.Standard, False, {
        # TODO
    })    

    # Scandal >= 2
    # > an afternoon of mischief
    london_deck.card("An Afternoon of Good Deeds", Rarity.Standard, False, {
        Item.FavHell: 1,
        ## TODO
        # Item.ConfidentSmile: 1,
        # Item.JadeFragment: 10
    })

    # Nightmares >= 3
    london_deck.card("A Moment's Peace", Rarity.VeryInfrequent, False, {
        # TODO
    })    

    # Nightmares >= 3
    # Publish => War-games
    # With testing, slightly lowers EPA
    london_deck.card("The interpreter of dreams", Rarity.Unusual, False, {
        # Success
        Item.Nightmares: -5 * 0.6,
        Item.FavGreatGame: 1 * 0.6,

        # Failure
        Item.Scandal: 1 * 0.4 * scandal_multiplier
    })    

    london_deck.card("An implausible penance", Rarity.Standard, False, {
        # TODO
    })    

    # > Repentant forger
    london_deck.card("A visit", Rarity.Standard, True, {
        Item.CrypticClue: 230, # base shadowy,
        Item.FavBohemians: 1,
        Item.FavCriminals: 1,
    })

    # with Evolution completed
    london_deck.card("The seekers of the garden", Rarity.Standard, True, {
        Item.ZeeZtory: -7,
        Item.FavBohemians: 1,
        Item.FavDocks: 0.5,
        Item.FavSociety: 0.5,
        Item.Fascinating: 7
    })

    london_deck.card("devices and desires", Rarity.Standard, False, {
    })

    london_deck.card("A Polite Invitation", Rarity.Standard, False, {
    })

    london_deck.card("Give a Gift!", Rarity.Standard, False, {
    })

    # > A disgraceful spectacle
    london_deck.card("A day at the races", Rarity.Standard, single_favours_enabled, {
        Item.FavChurch: 1
    })

    london_deck.card("One's public", Rarity.Standard, False, {
        # TODO    
    })

    london_deck.card("A Day with God's Editors", Rarity.Standard, False, {
        Item.TaleOfTerror: -1,
        Item.FavChurch: 1
    })    

    # Avoidable? unsure
    london_deck.card("Bringing the revolution", Rarity.Standard, single_favours_enabled, {
        Item.CompromisingDocument: -1,
        Item.FavRevolutionaries: 1
    })

    london_deck.card("Mirrors and Clay", Rarity.Standard, False, {
        # TODO
    })

    london_deck.card("The Cities that Fell", Rarity.Standard, False, {
        # TODO
    })

    london_deck.card("The Soft-Hearted Widow", Rarity.Standard, False, {
        # TODO
    })

    london_deck.card("All fear the overgoat!", Rarity.Standard, False, {
        # TODO
    })

    london_deck.card("The Northbound Parliamentarian", Rarity.Standard, False, {
        # TODO
    })    

    london_deck.card("A Dream of Roses", Rarity.Standard, False, {
        # TODO
    })

    london_deck.card("Weather at last", Rarity.Standard, False, {
        # TODO
    })

    london_deck.card("An unusual wager", Rarity.Standard, False, {
        # TODO
    })

    london_deck.card("Mr Wines is holding a sale!", Rarity.Standard, False, {
        # TODO
    })

    london_deck.card("The awful temptation of money", Rarity.Standard, False, {
        # TODO
    })

    # not sure if this can be avoided
    london_deck.card("Investigation the Affluent Photographer", Rarity.Standard, False, {
        # TODO
    })

    london_deck.card("The Geology of Winewound", Rarity.Standard, False, {
        # TODO
    })

    # > Ask her about the sudden influx of bones
    # Debatable whether this one is "good"
    london_deck.card("A Public Lecture", Rarity.Standard, False, {
        Item.CrypticClue: 100
        # also RoaMF for newspaper grind
    })

    london_deck.card("Wanted: Reminders of Brighter Days", Rarity.Standard, False, {
        # TODO
    })

    # notability >= 1
    london_deck.card("An Unsigned Message", Rarity.VeryInfrequent, False, {
        # TODO
    })    

    london_deck.card("A Presumptuous Little Opportunity", Rarity.VeryInfrequent, False, {
        # TODO
    })

    london_deck.card("A visit from slowcake's amanuensis", Rarity.Infrequent, False, {
        # TODO
    })

    # Shadowy >= 69, Renown Crims >= 20
    london_deck.card("A merry sort of crime", Rarity.VeryInfrequent, single_favours_enabled, {
        Item.FavCriminals: 1
    })

    london_deck.card("A dusty bookshop", Rarity.Rare, False, {
        # TODO
    })

    london_deck.card("A little omen", Rarity.Rare, False, {
        # TODO
    })

    london_deck.card("A disgraceful spectacle", Rarity.Rare, True, {
        Item.Echo: 12.5
    })    

    london_deck.card("A voice from a well", Rarity.Rare, False, {
        # TODO
    })

    london_deck.card("A fine day in the flit", Rarity.Unusual, False, {
        # TODO
    })

    london_deck.card("The Paranomastic Newshound", Rarity.Unusual, False, {
        # TODO
    })


    london_deck.card("The curt relicker and montgomery are moving quietly past",
        Rarity.VeryInfrequent, False, {
            # TODO
        })

    london_deck.card("The Capering Relicker and Gulliver are outside in the street",
        Rarity.VeryInfrequent, False, {
            # TODO
        })

    london_deck.card("The Shivering Relicker and Pinnock are trundling by",
        Rarity.VeryInfrequent, False, {
            # TODO
        })

    london_deck.card("The Coquettish Relicker and Mathilde are making the rounds",
        Rarity.VeryInfrequent, False, {
            # TODO
        })
    
    
    # --- Cheesemonger
    # slight loss over finishing the story

    # london_deck.card("A task from the cheesemonger", Rarity.Standard, True, {
    #     Item.FavUrchins: 1
    # })

    # london_deck.card("A commission from the cheesemonger", Rarity.Standard, False, {
    #     Item.FavRubberyMen: 0.5,
    #     Item.NoduleOfDeepAmber: 50
    # })

    # london_deck.card("A job from the cheesemonger", Rarity.Standard, True, {
    #     Item.CrypticClue: 24,
    #     Item.FavTombColonies: 1
    # })

    # london_deck.card("An assignment from the cheesemonger", Rarity.Standard, True, {
    #   Item.FavChurch: 1  
    # })
    
    # ----------------------
    # --- Cards: Location-specific
    # ----------------------

    # so far no special location is positive EPA
    # but these have potential 

    # if (player_location == Location.BazaarSideStreet):
    #     card("The Skin of the Bazaar", Rarity.Rare, False, {

    #     })

    # if (player_location == Location.LadybonesRoad):
    #     card("1000 Nevercold Brass Silver Wanted!", Rarity.Standard, True, {
    #         Item.NevercoldBrassSliver: -1000,
    #         Item.CrypticClue: 500,
    #         Item.AppallingSecret: 10,
    #         Item.FavGreatGame: 1
    #     })

    # if (player_location == Location.Spite):
    #     card("2000 Foxfire Candles Wanted!", Rarity.Standard, True, {
    #         Item.FoxfireCandleStub: -2000,
    #         Item.PieceOfRostygold: 2000,
    #         Item.MysteryOfTheElderContinent: 1,
    #         Item.FavChurch: 1
    #     })

    # if (player_location == Location.TheUniversity):
    #     card("A peculiar practice", Rarity.Standard, True, {
    #         # Item.ConnectedSummerset: -5 # ignoring for now
    #         Item.FavTombColonies: 1,
    #         Item.Echo: 0.6 # bundle of oddities
    #     })

    #     card("Stone by stone", Rarity.Standard, False, {

    #     })

    # if (player_location == Location.YourLodgings):
    #     card("A commotion above", Rarity.Rare, False, {
            
    #     })    

    #     card("The Neath's Mysteries", Rarity.Standard, False, {
            
    #     })

    #     card("The Urchin and the Monkey", Rarity.VeryInfrequent, True, {
    #         Item.CompromisingDocument: -2,
    #         Item.FavUrchins: 1
    #     })

    #     card("Your Grubby Urchin is becoming troublesome", Rarity.VeryInfrequent, True, {
    #         Item.TaleOfTerror: -2,
    #         Item.FavUrchins: 1
    #     })    

    # # TODO: check the actual rarity of this
    # # also it adds that other rare card to the deck that clears all wounds
    # card("Slavering Dream Hound", Rarity.Unusual, True, {
    #     Item.DropOfPrisonersHoney: 200
    # })

    london_deck.card("A Trade in Souls card", Rarity.Standard, True, {
        Item.Echo: -4, # 50 souls + 5 contracts
        Item.FavConstables: 1,
        Item.FavChurch: 1,
        Item.FavSociety: 1
    })    

    # Society ending since that's what I have
    # probably the best of the aunt-bitions anyway
    london_deck.card("The OP Aunt card", Rarity.Standard, True, {
        Item.BottleOfGreyfields1882: -50,

        # 0.7 Failure
        Item.FavSociety: 1 * 0.7,
        Item.ScrapOfIncendiaryGossip: 3 * 0.7,
        Item.InklingOfIdentity: 5 * 0.7,
        Item.Scandal: -2 * 0.7,
        
        # 0.3 success
        Item.Echo: 10 * replacement_epa * 0.3
    })    

    return london_deck

def create_london_deck(config: Config):

    replacement_epa = 6.0
    player = config.player
    wounds_multiplier = menace_multiplier(player.wounds_reduction)
    suspicion_multiplier = menace_multiplier(player.suspicion_reduction)
    scandal_multiplier = menace_multiplier(player.scandal_reduction)    
    nightmares_multiplier = menace_multiplier(player.nightmares_reduction)

    london_deck = Deck("London", -400)
    all_cards = []

    # HACK for refactor convenience
    good_cards = all_cards
    bad_cards = all_cards
    single_favour_cards_list = good_cards


    # card worth calculated with baseline of 120/40 w 3rd city silverer
    # and ~6.46 EPA

    # borderline? minimal difference good vs. bad
    single_favour_cards_list.append(
        Card(
            item=Item.CL_RooftopShack,
            name= "Lair in the Marshes: Peril and pyjamas",
            freq= Rarity.Standard,
            grade= Grade.Good,
            exchange= config.challenge_ev(
                Stat.Dangerous,
                60,
                {
                    Item.CertifiableScrap: 1,
                    Item.FavSociety: 1,
                    Item.Nightmares: 1 * nightmares_multiplier
                },
                {
                    Item.Wounds: 1 * wounds_multiplier
                }
    )))

    knives_rare_success_rate = 0.05
    single_favour_cards_list.append(Card(
        item=Item.CL_SmokyFlophouse,
        name="Smoky Flophouse",
        freq=Rarity.Standard,
        grade= Grade.Good,        
        exchange=config.challenge_ev(
            Stat.Shadowy,
            40,
            on_pass = weighted_exchange(
                (knives_rare_success_rate, {
                    Item.AeolianScream: 1
                }),
                (1.0 - knives_rare_success_rate, {
                    Item.FavCriminals: 0.5,
                    Item.FavRevolutionaries: 0.5
                }),
            ),
            on_fail = {}
    )))

    single_favour_cards_list.append(
        Card(
            item = Item.CL_HandsomeTownhouse,
            name = "Handsome Townhouse: Scandalous Party",
            freq = Rarity.Frequent,
            grade= Grade.Good,
            exchange = config.challenge_ev(
                stat = Stat.Persuasive,
                dc = 80,
                on_pass = {
                    Item.Scandal: 2 * scandal_multiplier,
                    Item.Hedonist: 3,
                    Item.FavBohemians: 0.5,
                    Item.FavSociety: 0.5
                },
                on_fail = {
                    Item.Scandal: 1 * scandal_multiplier
                }
            )
    ))

    # adds ~0.02 EPA
    good_cards.append(
        Card(
            item = Item.CL_PremisesAtTheBazaar,
            name= "Premises at the Bazaar w/ Kraken",
            freq= Rarity.Standard,
            grade= Grade.Good,
            exchange= config.challenge_ev(
                stat=Stat.APlayerOfChess,
                dc=9,
                on_pass={
                    Item.TouchingLoveStory: 1.5,
                    Item.StolenKiss: 1.5,
                    Item.NightsoilOfTheBazaar: 2
                },
                on_fail={
                    Item.Scandal: 1 * scandal_multiplier,
                    Item.Echo: -2
                }
            )
        )
    )

    # -----------------------------------------------------
    # --- Cards: Companions
    # ----------------------------------------------------

    good_cards.append(
        Card(
            "What will you do with your [connected pet]?",
            Rarity.Standard,
            grade= Grade.Good,
            exchange={
                Item.CL_ConnectedPet: 1
            }))

    single_favour_cards_list.append(
        Card(
            "Attend to your spouses",
            Rarity.VeryInfrequent,
            grade= Grade.Good,
            exchange= {
                Item.FavBohemians: 1
            }))

    # good_cards.append(
    #     Card(
    #         name="Slavering Dream-Hound standard card",
    #         freq=Rarity.Standard,
    #         exchange= {
    #             Item.DropOfPrisonersHoney: 200
    #         }))
    
    # # can't encode "all" of anything so just picking level 5
    # good_cards.append(
    #     Card(
    #         name="Slavering Dream-Hound rare card",
    #         freq=Rarity.Rare,
    #         exchange= {
    #             Item.Wounds: -15,
    #             Item.PieceOfRostygold: 100
    #         }))    

    # -----------------------------------------------------
    # --- Cards: Other Equipment
    # ----------------------------------------------------

    single_favour_cards_list.append(
        Card(
            "A day out in your Clay Sedan Chair",
            Rarity.Standard,
            grade= Grade.Good,
            exchange={
                Item.FavSociety: 1,
                Item.Hedonist: -3
            }
        )
    )

    # -----------------------------------------------------
    # --- Cards: Clubs
    # ----------------------------------------------------

    # # Sophia's
    # # Can also be Tomb-Colony favour, maybe 50/50?
    # london_deck.card("Club: Sophia's", Rarity.Standard, True, {
    #     Item.RumourOfTheUpperRiver: -5,
    #     Item.PieceOfRostygold: 1500,
    #     Item.JetBlackStinger: 5
    # })

    good_cards.append(Card(
        name="Young Stags",
        freq=Rarity.Standard,
        grade= Grade.Excellent,
        exchange={
            Item.PieceOfRostygold: -500,
            Item.FavSociety: 2,
            Item.FavBohemians: 1
        }
    ))
    # -----------------------------------------------------
    # --- Cards: Dreams
    # ----------------------------------------------------

    # Not sure how to model this? Can they be locked out of altogether?
    # Or just have one card for each of the four
    # Guessing at rarity for the red cards

    # london_deck.card("A dream about a clouded place", Rarity.Unusual, {
    #     # TODO
    # })

    bad_cards.append(Card(
        name="dreams placeholder card 1",
        freq=Rarity.Unusual,
        grade= Grade.Bad,
        exchange={}
    ))

    bad_cards.append(Card(
        name="dreams placeholder card 2",
        freq=Rarity.Unusual,
        grade= Grade.Bad,
        exchange={}
    ))

    bad_cards.append(Card(
        name="dreams placeholder card 3",
        freq=Rarity.Unusual,
        grade= Grade.Bad,
        exchange={}
    ))

    bad_cards.append(Card(
        name="dreams placeholder card 4",
        freq=Rarity.Unusual,
        grade= Grade.Bad,
        exchange={}
    ))

    bad_cards.append(Card(
        name="dreams placeholder card 5",
        freq=Rarity.Unusual,
        grade= Grade.Bad,
        exchange={}
    ))

    # -----------------------------------------------------
    # --- Cards: Factions
    # ----------------------------------------------------

    single_favour_cards_list.append(Card(
        name="Bohemians faction card",
        freq=Rarity.Standard,
        grade=Grade.Good,
        exchange={
            Item.FoxfireCandleStub: -20,
            Item.BottleOfGreyfields1882: -15,
            Item.Scandal: 1 * scandal_multiplier,
            Item.FavBohemians: 1
        }
    ))

    single_favour_cards_list.append(Card(
        name="Church faction card",
        freq=Rarity.Standard,
        exchange={
            Item.PieceOfRostygold: -10,
            Item.FavChurch: 1,
            Item.AirsOfLondonChange: 1
        }))

    bad_cards.append(Card(
        name="Constables faction card",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={
            Item.PieceOfRostygold: -10,
            Item.FavConstables: 1,
            Item.AirsOfLondonChange: 1
        }))

    single_favour_cards_list.append(Card(
        name="Criminals faction card",
        freq=Rarity.Standard,
        exchange={
            Item.Suspicion: 1 * suspicion_multiplier,
            Item.FavCriminals: 1,
        }))
    
    single_favour_cards_list.append(Card(
        name="Docks faction card",
        freq=Rarity.Standard,
        exchange={
            Item.PieceOfRostygold: -10,
            Item.FavDocks: 1,
        })) 

    bad_cards.append(Card(
        name="Great Game faction card",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={
            Item.Wounds: 1 * suspicion_multiplier,
            Item.FavGreatGame: 1,
        }))

    bad_cards.append(Card(
        name="Hell faction card",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={
            Item.Scandal: 1 * suspicion_multiplier,
            Item.FavHell: 1,
            Item.AirsOfLondonChange: 1
        }))    

    single_favour_cards_list.append(Card(
        name="Revolutionaries faction card",
        freq=Rarity.Standard,
        exchange={
            Item.VisionOfTheSurface: -1,
            Item.Suspicion: 1 * suspicion_multiplier,
            Item.FavRevolutionaries: 1,
        }))    

    bad_cards.append(Card(
        name="Rubbery Men faction card",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        # exchange={
        #     Item.NoduleOfWarmAmber: -1,
        #     Item.NoduleOfDeepAmber: 50,
        #     Item.FavRubberyMen: 1,
        # }
        exchange={
            Item.NoduleOfWarmAmber: -100,
            Item.NoduleOfTremblingAmber: 1,
            Item.FavRubberyMen: 1,
        }
    ))    

    single_favour_cards_list.append(Card(
        name="Society faction card",
        freq=Rarity.Standard,
        grade= Grade.Good,
        exchange={
            Item.ScrapOfIncendiaryGossip: -1,
            Item.Suspicion: 1 * suspicion_multiplier,
            Item.FavSociety: 1,
        }))        

    single_favour_cards_list.append(Card(
        name="Tomb-Colonies faction card",
        freq=Rarity.Standard,
        grade= Grade.Good,
        exchange={
            Item.FavTombColonies: 1,
        }))    


    # # Urchins
    # london_deck.card("Urchins Faction", Rarity.Standard, False, {
    #     Item.Echo: -0.4, # 1x lucky weasel
    #     Item.FavUrchins: 1
    # })


    single_favour_cards_list.append(Card(
        name="Urchins faction card",
        freq=Rarity.Standard,
        grade= Grade.Good,
        # exchange={
        #     Item.LuckyWeasel: -1,
        #     Item.FavUrchins: 1,
        # }
        exchange={
            Item.Nightmares: -2,
            Item.FavUrchins: 1,
        }
        ))

    # ----------------------
    # --- Cards: General London
    # ----------------------

    bad_cards.append(Card(
        name="a tournament of weasels",
        freq=Rarity.Unusual,
        grade= Grade.Bad,
        exchange={}
    ))

    bad_cards.append(Card(
        name="Orthographic Infection",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={}
    ))

    bad_cards.append(Card(
        name="City Vices: a rather decadent evening",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={}
    ))

    bad_cards.append(Card(
        name="A restorative",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={}
    ))

    bad_cards.append(Card(
        name="An afternoon of good deeds",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={}
    ))    

    bad_cards.append(Card(
        name="A moment's peace",
        freq=Rarity.VeryInfrequent,
        grade= Grade.Bad,
        exchange={}
    ))

    bad_cards.append(Card(
        name="The interpreter of dreams",
        freq=Rarity.Unusual,
        grade= Grade.Bad,
        exchange={}
    ))

    # double-check this one, might be ok
    bad_cards.append(Card(
        name="An implausible penance",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={}
    ))

    # TODO: options for other acquaintances
    good_cards.append(Card(
        name="A visit",
        freq=Rarity.Standard,
        grade= Grade.Excellent,
        exchange={
            Item.CL_AVisit: 1
        }
    ))

    good_cards.append(Card(
        name="The seekers of the garden",
        freq=Rarity.Standard,
        grade= Grade.Excellent,
        exchange={
            Item.ZeeZtory: -7,
            Item.FavBohemians: 1,
            Item.FavDocks: 0.5,
            Item.FavSociety: 0.5,
            Item.Fascinating: 7
        }
    ))


    bad_cards.append(Card(
        name="Devices and desires",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={
        }
    ))


    bad_cards.append(Card(
        name="A polite invitation",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={
        }
    ))

    # TODO
    bad_cards.append(Card(
        name="Give a gift!",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange={
        }
    ))

    good_cards.append(Card(
        name="A day at the races",
        freq=Rarity.Standard,
        grade= Grade.Good,
        exchange={
            Item.FavChurch: 1
        }
    ))

    # Avoidable!
    # Sulky Bat >= 1
    # london_deck.card("A parliament of bats", Rarity.Standard, False, {
    #     Item.VisionOfTheSurface: -1,
    #     Item.FavGreatGame: 1
    # })


    bad_cards.append(Card(
        name="One's public",
        freq=Rarity.Standard,
        grade= Grade.Bad,
        exchange=config.challenge_ev(
            stat=Stat.Persuasive,
            dc=220,
            on_pass={
                Item.PieceOfRostygold: 20,
                Item.JadeFragment: 20,
                Item.ConfidentSmile: 2,
                Item.PrimordialShriek: 30,
                Item.Echo: 1,
                Item.BottleOfGreyfields1879: 100
            },
            on_fail={
                Item.Scandal: 1
            }
        )
    ))

    single_favour_cards_list.append(Card(
        name="God's Editors",
        freq=Rarity.Standard,
        grade=Grade.Good,        
        exchange={
            Item.TaleOfTerror: -1,
            Item.FavChurch: 1
        }
    ))

    single_favour_cards_list.append(Card(
        name="Bringing the revolution",
        freq=Rarity.Standard,
        grade=Grade.Good,        

        exchange={
            Item.CompromisingDocument: -1,
            Item.FavRevolutionaries: 1
        }
    ))

    # Time limited, also lots of good options?
    # Maybe just leave it out?
    # london_deck.card("The Calendrical Confusion of 1899", Rarity.Standard, True, {
    #     Item.ScrapOfIncendiaryGossip: 14
    # })

    bad_cards.append(Card(
        name="Mirrors and clay",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The cities that fell",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The soft hearted widow",
        freq=Rarity.Standard,
        grade=Grade.Bad,        
        exchange={
        }
    ))

    # Becomes good/excellent when you have the Overgoat
    bad_cards.append(Card(
        name="all fear the overgoat",
        freq=Rarity.Standard,
        grade=Grade.Bad,        
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The northbound parliamentarian",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    # Double check, might still be good long-term
    # but very boring
    bad_cards.append(Card(
        name="A dream of roses",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="Weather at last",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="An unusual wager",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="Mr wines is holding a sale!",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The awful temptation of money",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="investigating the affluent photographer",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="the geology of winewound",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    # borderline? depends on if publishing the boney paper is good
    bad_cards.append(Card(
        name="A public lecture",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))    

    # # avoidable with no Favours: Hell
    # london_deck.card("A consideration for services rendered", Rarity.Standard, {
    #     # TODO
    # })


    bad_cards.append(Card(
        name="Wanted: reminders of brighter days",
        freq=Rarity.Standard,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="An unsigned message",
        freq=Rarity.VeryInfrequent,
        grade=Grade.Bad,
        exchange={
        }
    ))

    # might be good sometimes
    bad_cards.append(Card(
        name="A presumptuous little opportunity",
        freq=Rarity.VeryInfrequent,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="A visit from slowcake's amanuensis",
        freq=Rarity.Infrequent,
        grade=Grade.Bad,
        exchange={
        }
    ))

    single_favour_cards_list.append(Card(
        name="A merry sort of crime",
        freq=Rarity.VeryInfrequent,
        grade=Grade.Good,
        exchange={
            Item.FavCriminals: 1
        }
    ))

    bad_cards.append(Card(
        name="A dusty bookshop",
        freq=Rarity.Rare,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="A little omen",
        freq=Rarity.Rare,
        grade=Grade.Bad,
        exchange={
        }
    ))

    good_cards.append(Card(
        name="A disgraceful spectable",
        freq=Rarity.Rare,
        grade=Grade.Excellent,
        exchange={
            Item.Echo: 12.5
        }
    ))

    bad_cards.append(Card(
        name="A voice from a well",
        freq=Rarity.Rare,
        grade=Grade.Avoid,
        exchange={
        }
    ))


    bad_cards.append(Card(
        name="A fine day in the flit",
        freq=Rarity.Unusual,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The paranomastic newshound",
        freq=Rarity.Unusual,
        grade=Grade.Bad,
        exchange={
        }
    ))

    # ----------------------
    # --- Cards: Relickers
    # ----------------------

    bad_cards.append(Card(
        name="The curt relicker",
        freq=Rarity.VeryInfrequent,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The capering relicker",
        freq=Rarity.VeryInfrequent,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The shivering relicker",
        freq=Rarity.VeryInfrequent,
        grade=Grade.Bad,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The coquettish relicker",
        freq=Rarity.VeryInfrequent,
        grade=Grade.Bad,
        exchange={
        }
    ))


    # ----------------------
    # --- Cards: FATE-locked
    # ----------------------

    good_cards.append(Card(
        name="A trade in souls",
        freq=Rarity.Standard,
        grade=Grade.Excellent,
        exchange={
            Item.Echo: -4,
            Item.FavConstables: 1,
            Item.FavChurch: 1,
            Item.FavSociety: 1
        }
    ))

    good_cards.append(Card(
        name="The OP Aunt card",
        freq=Rarity.Standard,
        grade=Grade.Excellent,
        exchange={
            Item.BottleOfGreyfields1882: -50,

            # 0.7 Failure
            Item.FavSociety: 1 * 0.7,
            Item.ScrapOfIncendiaryGossip: 3 * 0.7,
            Item.InklingOfIdentity: 5 * 0.7,
            Item.Scandal: -2 * 0.7,
            
            # 0.3 success
            Item.Echo: 10 * replacement_epa * 0.3
        }
    ))

    return [good_cards, bad_cards]

# TODO rewrite algo to use Grade attr instead of split lists
def monte_carlo(config, runs, draws_per_run):
    cummulative = {}
    good_cards, bad_cards = create_london_deck(config)

    for i in range(0, runs):
        print(f"Simulation progress: {i}/{runs} ", end="\r")
        result = simulate_run(config, good_cards, bad_cards, draws_per_run)
        utils.add_items(cummulative, result)
    
    # total_actions = abs(cummulative[Item.Action])
    total_draws = runs * draws_per_run

    per_draw = {}
    for key, value in cummulative.items():
        per_draw[key] = value / total_draws

    per_draw[Item.CardDraws] = -1
    return per_draw



def simulate_run(config, good_cards, bad_cards, draws):
    deck = []
    deck += good_cards
    deck += bad_cards
    
    hand = []
    totals = {
        Item.Action: 0
    }

    # deck = all_cards.copy()
    # total = sum(i.freq for i in all_cards)

    def draw_card():
        weights = [card.freq.value for card in deck]
        card = random.choices(deck, weights, k=1)[0]
        deck.remove(card)
        hand.append(card)

    def play_card(card: Card):
        # print("Playing " + card.name)
        totals[Item.Action] -= 1
        utils.add_items(totals, card.exchange)
        # print(totals)
        hand.remove(card)
        deck.append(card)
    
    def good_cards_in_hand():
        return [card for card in hand if card in good_cards]
    
    def bad_cards_in_hand():
        return [card for card in hand if card in bad_cards]

    def discard_rarest_bad_card():
        bads = bad_cards_in_hand()
        if len(bads) > 0:
                bads.sort(key= lambda card : card.freq.value)
                card = bads[0]
                hand.remove(card)
                deck.append(card)

    # def refill_hand():

    while draws > 0:

        # there is a slightly smarter way to do this
        # requires setting EV of every card
        # and playing cards as long as they increase EV of next draw
        # but that sounds like a lot more work
        for card in good_cards_in_hand():
            play_card(card)

        while len(hand) < 5 and draws > 0:
            draw_card()
            draws -= 1
            
        if not good_cards_in_hand():
            discard_rarest_bad_card()
            # refill_hand()
            while len(hand) < 5 and draws > 0:
                draw_card()
                draws -= 1

    return totals

