from enums import *
from utils import *
from config import Config
from player import Player
from decks.deck import *



def add_trades(config):
    trade = config.trade

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavBohemians: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavChurch: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavConstables: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavCriminals: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavDocks: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavGreatGame: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavHell: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavRevolutionaries: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavRubberyMen: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavSociety: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavTombColonies: 1
    })

    trade(0, {
        Item.ConnectedPetCard: -1,
        Item.FavUrchins: 1
    })


def create_london_deck(
        player: Player,
        replacement_epa,
        config: Config
        ):

    wounds_multiplier = menace_multiplier(player.wounds_reduction)
    suspicion_multiplier = menace_multiplier(player.suspicion_reduction)
    scandal_multiplier = menace_multiplier(player.scandal_reduction)    
    nightmares_multiplier = menace_multiplier(player.nightmares_reduction)

    london_deck = Deck("London", -400)
    good_cards = []
    bad_cards = []

    good_cards.append(
        Card(
            name= "Lair in the Marshes: Peril and pyjamas",
            freq= Rarity.Standard,
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

    # Lair in the Marshes
    london_deck.card("Lair in the Marshes", Rarity.Standard, True, {
        Item.FavSociety: 1,
        Item.CertifiableScrap: 1,
        Item.Nightmares: 1 * nightmares_multiplier
    })

    knives_rare_success_rate = 0.05
    good_cards.append(Card("Smoky Flophouse", Rarity.Standard, config.challenge_ev(
        Stat.Shadowy,40,
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

    # The Tower of Knives: Difficulties at a Smoky Flophouse
    # The next victim?
    london_deck.card("The Tower of Knives", Rarity.Standard, True, {
        Item.FavCriminals: 0.5 - knives_rare_success_rate / 2.0,
        Item.FavRevolutionaries: 0.5 - knives_rare_success_rate / 2.0,
        Item.AeolianScream: knives_rare_success_rate
    })

    # The Tower of Eyes: Behind Closed Doors at a Handsome Townhouse
    # scandalous party
    london_deck.card("The Tower of Eyes", Rarity.Frequent, True, {
    Item.FavBohemians: 0.5,
    Item.FavSociety: 0.5,
    Item.Hedonist: 3,
    Item.Scandal: 2 * scandal_multiplier
    })

    good_cards.append(
        Card(
            name = "Handsome Townhouse: Scandalous Party",
            freq = Rarity.Frequent,
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

    # The Tower of Sun and Moon: a Reservation at the Royal Bethlehem Hotel
    london_deck.card("Royal Beth lodings", Rarity.Frequent, False, {
        Item.CertifiableScrap: 3
    })

    # TODO: check if this is actually worthwile
    good_cards.append(
        Card(
            name= "Premises at the Bazaar w/ Kraken",
            freq= Rarity.Standard,
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

    london_deck.card("What will you do with your [connected pet]?", Rarity.Standard, True, {
        Item.ConnectedPetCard: 1
    })

    good_cards.append(
        Card(
            "What will you do with your [connected pet]?",
            Rarity.Standard,
            {
                Item.ConnectedPetCard: 1
            }))


    # With Bewildering Procession
    london_deck.card("Attend to your spouses", Rarity.VeryInfrequent, True, {
        Item.FavBohemians: 1
    })

    good_cards.append(
        Card(
            "Attend to your spouses",
            Rarity.VeryInfrequent,
            exchange= {
                Item.FavBohemians: 1
            }
        )
    )

    # -----------------------------------------------------
    # --- Cards: Other Equipment
    # ----------------------------------------------------

    # avoidable
    london_deck.card("A day out in your Clay Sedan Chair", Rarity.Standard, True, {
        Item.FavSociety: 1,
        Item.Hedonist: -3
    })

    good_cards.append(
        Card(
            "A day out in your Clay Sedan Chair",
            Rarity.Standard,
            {
                Item.FavSociety: 1,
                Item.Hedonist: -3
            }
        )
    )

    # # avoidable? A: yes, with watchful gains
    # london_deck.card("Riding your Velocipede", Rarity.Standard, False, {
    #     Item.ManiacsPrayer: -5,
    #     Item.FavConstables: 1
    # })

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

    london_deck.card("More Larks with the Young Stags", Rarity.Standard, True, {
        # Item.PieceOfRostygold: -500,
        Item.Echo: -5, # everyone has rostygold
        Item.FavSociety: 2,
        Item.FavBohemians: 1
    })

    good_cards.append(Card(
        name="Young Stags",
        freq=Rarity.Standard,
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

    # assuming you end up with 5 and they are all Unusual
    london_deck.card("omni-Dreams placeholder card", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="dreams placeholder card",
        freq=Rarity.Standard,
        exchange={}
    ))

    # -----------------------------------------------------
    # --- Cards: Factions
    # ----------------------------------------------------

    # Bohemians
    london_deck.card("Bohemians Faction", Rarity.Standard, True, {
        Item.Echo: -1.2,
        Item.FavBohemians: 1
    })

    good_cards.append(Card(
        name="Bohemians faction card",
        freq=Rarity.Standard,
        exchange={
            Item.FoxfireCandleStub: -20,
            Item.BottleOfGreyfields1882: -15,
            Item.Scandal: 1 * scandal_multiplier,
            Item.FavBohemians: 1
        }
    ))

    # Church
    london_deck.card("Church Faction", Rarity.Standard, True, {
        Item.Echo: -0.1,
        Item.FavChurch: 1
    })

    good_cards.append(Card(
        name="Church faction card",
        freq=Rarity.Standard,
        exchange={
            Item.PieceOfRostygold: -10,
            Item.FavChurch: 1,
            Item.AirsOfLondonChange: 1
        }))

    # Constables
    london_deck.card("Constables Faction", Rarity.Standard, False, {
        Item.Echo: -0.1,
        Item.FavConstables: 1
    })

    bad_cards.append(Card(
        name="Constables faction card",
        freq=Rarity.Standard,
        exchange={
            Item.PieceOfRostygold: -10,
            Item.FavConstables: 1,
            Item.AirsOfLondonChange: 1
        }))
    
    # Criminals
    london_deck.card("Criminals Faction", Rarity.Standard, True, {
        Item.Suspicion: 1 * suspicion_multiplier,
        Item.FavCriminals: 1,
    })

    good_cards.append(Card(
        name="Criminals faction card",
        freq=Rarity.Standard,
        exchange={
            Item.Suspicion: 1 * suspicion_multiplier,
            Item.FavCriminals: 1,
        }))
    
    # Docks
    london_deck.card("Docks Faction", Rarity.Standard, True, {
        Item.Echo: -0.1,
        Item.FavDocks: 1
    })

    good_cards.append(Card(
        name="Docks faction card",
        freq=Rarity.Standard,
        exchange={
            Item.PieceOfRostygold: -10,
            Item.FavDocks: 1,
        })) 

    # GreatGame
    london_deck.card("Great Game Faction", Rarity.Standard, False, {
        Item.Wounds: 1 * wounds_multiplier,
        Item.FavGreatGame: 1
    })

    bad_cards.append(Card(
        name="Great Game faction card",
        freq=Rarity.Standard,
        exchange={
            Item.Wounds: 1 * suspicion_multiplier,
            Item.FavGreatGame: 1,
        }))

    # Hell
    london_deck.card("Burning Shadows: the Devils of London", Rarity.Standard, False, {
        Item.Scandal: 1 * scandal_multiplier,
        Item.FavHell: 1
    })

    bad_cards.append(Card(
        name="Hell faction card",
        freq=Rarity.Standard,
        exchange={
            Item.Scandal: 1 * suspicion_multiplier,
            Item.FavHell: 1,
            Item.AirsOfLondonChange: 1
        }))    

    # Revolutionaries
    london_deck.card("Rev Faction", Rarity.Standard, True, {
        Item.Echo: -0.5,
        Item.FavRevolutionaries: 1 
    })

    good_cards.append(Card(
        name="Revolutionaries faction card",
        freq=Rarity.Standard,
        exchange={
            Item.VisionOfTheSurface: -1,
            Item.Suspicion: 1 * suspicion_multiplier,
            Item.FavRevolutionaries: 1,
        }))    

    # RubberyMen
    london_deck.card("Rubbery Faction", Rarity.Standard, False, {
        Item.Echo: -0.1,
        Item.FavRubberyMen: 1
    })

    bad_cards.append(Card(
        name="Rubbery Men faction card",
        freq=Rarity.Standard,
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

    # Society
    london_deck.card("Society Faction", Rarity.Standard, True, {
        Item.Echo: -0.5,
        Item.FavSociety: 1
    })

    good_cards.append(Card(
        name="Society faction card",
        freq=Rarity.Standard,
        exchange={
            Item.ScrapOfIncendiaryGossip: -1,
            Item.Suspicion: 1 * suspicion_multiplier,
            Item.FavSociety: 1,
        }))        

    # Tomb-Colonies
    london_deck.card("Tomb Colonies Faction", Rarity.Standard, False, {
        Item.FavTombColonies: 1
    })

    bad_cards.append(Card(
        name="Tomb-Colonies faction card",
        freq=Rarity.Standard,
        exchange={
            Item.FavTombColonies: 1,
        }))    


    # # Urchins
    # london_deck.card("Urchins Faction", Rarity.Standard, False, {
    #     Item.Echo: -0.4, # 1x lucky weasel
    #     Item.FavUrchins: 1
    # })

    # With HOJOTOHO ending
    london_deck.card("Urchins Faction", Rarity.Standard, True, {
        Item.FavUrchins: 1,
        Item.Nightmares: -2
    })

    good_cards.append(Card(
        name="Urchins faction card",
        freq=Rarity.Standard,
        exchange={
            Item.LuckyWeasel: -1,
            Item.FavUrchins: 1,
        }
        # exchange={
        #     Item.Nightmares: -2,
        #     Item.FavUrchins: 1,
        # }
        ))

    # ----------------------
    # --- Cards: General London
    # ----------------------

    # A tournament of weasels
    london_deck.card("A tournament of weasels", Rarity.Unusual, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="a tournament of weasels",
        freq=Rarity.Unusual,
        exchange={}
    ))

    # Nightmares >= 1
    london_deck.card("Orthographic Infection", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="Orthographic Infection",
        freq=Rarity.Standard,
        exchange={}
    ))

    # FavBohe >= 1
    london_deck.card("City Vices: A rather decadent evening", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="City Vices: a rather decadent evening",
        freq=Rarity.Standard,
        exchange={}
    ))

    # Wounds >= 2
    london_deck.card("A Restorative", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="A restorative",
        freq=Rarity.Standard,
        exchange={}
    ))

    # Scandal >= 2
    # > an afternoon of mischief
    london_deck.card("An Afternoon of Good Deeds", Rarity.Standard, False, {
        Item.FavHell: 1,
        ## TODO
        # Item.ConfidentSmile: 1,
        # Item.JadeFragment: 10
    })

    bad_cards.append(Card(
        name="An afternoon of good deeds",
        freq=Rarity.Standard,
        exchange={}
    ))    

    # Nightmares >= 3
    london_deck.card("A Moment's Peace", Rarity.VeryInfrequent, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="A moment's peace",
        freq=Rarity.VeryInfrequent,
        exchange={}
    ))

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

    bad_cards.append(Card(
        name="The interpreter of dreams",
        freq=Rarity.Unusual,
        exchange={}
    ))

    london_deck.card("An implausible penance", Rarity.Standard, False, {
        # TODO
    })

    # double-check this one, might be ok
    bad_cards.append(Card(
        name="An implausible penance",
        freq=Rarity.Standard,
        exchange={}
    ))

    # > Repentant forger
    london_deck.card("A visit", Rarity.Standard, True, {
        Item.CrypticClue: 230, # base shadowy,
        Item.FavBohemians: 1,
        Item.FavCriminals: 1,
    })

    # TODO: options for other acquaintances
    good_cards.append(Card(
        name="A visit",
        freq=Rarity.Standard,
        exchange={
            Item.CrypticClue: 230,
            Item.FavBohemians: 1,
            Item.FavCriminals: 1
        }
    ))

    # with Evolution completed
    london_deck.card("The seekers of the garden", Rarity.Standard, True, {
        Item.ZeeZtory: -7,
        Item.FavBohemians: 1,
        Item.FavDocks: 0.5,
        Item.FavSociety: 0.5,
        Item.Fascinating: 7
    })

    good_cards.append(Card(
        name="The seekers of the garden",
        freq=Rarity.Standard,
        exchange={
            Item.ZeeZtory: -7,
            Item.FavBohemians: 1,
            Item.FavDocks: 0.5,
            Item.FavSociety: 0.5,
            Item.Fascinating: 7
        }
    ))

    london_deck.card("devices and desires", Rarity.Standard, False, {
    })

    bad_cards.append(Card(
        name="Devices and desires",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("A Polite Invitation", Rarity.Standard, False, {
    })

    bad_cards.append(Card(
        name="A polite invitation",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("Give a Gift!", Rarity.Standard, False, {
    })

    # TODO
    bad_cards.append(Card(
        name="Give a gift!",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    # > A disgraceful spectacle
    london_deck.card("A day at the races", Rarity.Standard, True, {
        Item.FavChurch: 1
    })

    good_cards.append(Card(
        name="A day at the races",
        freq=Rarity.Standard,
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


    london_deck.card("One's public", Rarity.Standard, False, {
        # TODO    
    })

    bad_cards.append(Card(
        name="One's public",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("A Day with God's Editors", Rarity.Standard, False, {
        Item.TaleOfTerror: -1,
        Item.FavChurch: 1
    })

    good_cards.append(Card(
        name="God's Editors",
        freq=Rarity.Standard,
        exchange={
            Item.TaleOfTerror: -1,
            Item.FavChurch: 1
        }
    ))

    # Avoidable? unsure
    london_deck.card("Bringing the revolution", Rarity.Standard, True, {
        Item.CompromisingDocument: -1,
        Item.FavRevolutionaries: 1
    })

    good_cards.append(Card(
        name="Bringing the revolution",
        freq=Rarity.Standard,
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

    london_deck.card("Mirrors and Clay", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="Mirrors and clay",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("The Cities that Fell", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="The cities that fell",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("The Soft-Hearted Widow", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="The soft hearted widow",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("All fear the overgoat!", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="all fear the overgoat",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("The Northbound Parliamentarian", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="The northbound parliamentarian",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("A Dream of Roses", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="A dream of roses",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("Weather at last", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="Weather at last",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("An unusual wager", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="An unusual wager",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("Mr Wines is holding a sale!", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="Mr wines is holding a sale!",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("The awful temptation of money", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="The awful temptation of money",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    # not sure if this can be avoided
    london_deck.card("Investigation the Affluent Photographer", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="investigating the affluent photographer",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    london_deck.card("The Geology of Winewound", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="the geology of winewound",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    # > Ask her about the sudden influx of bones
    # Debatable whether this one is "good"
    london_deck.card("A Public Lecture", Rarity.Standard, False, {
        Item.CrypticClue: 100
        # also RoaMF for newspaper grind
    })

    bad_cards.append(Card(
        name="A public lecture",
        freq=Rarity.Standard,
        exchange={
        }
    ))    

    # # avoidable with no Favours: Hell
    # london_deck.card("A consideration for services rendered", Rarity.Standard, {
    #     # TODO
    # })

    london_deck.card("Wanted: Reminders of Brighter Days", Rarity.Standard, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="Wanted: reminders of brighter days",
        freq=Rarity.Standard,
        exchange={
        }
    ))

    # notability >= 1
    london_deck.card("An Unsigned Message", Rarity.VeryInfrequent, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="An unsigned message",
        freq=Rarity.VeryInfrequent,
        exchange={
        }
    ))

    london_deck.card("A Presumptuous Little Opportunity", Rarity.VeryInfrequent, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="A presumptuous little opportunity",
        freq=Rarity.VeryInfrequent,
        exchange={
        }
    ))

    london_deck.card("A visit from slowcake's amanuensis", Rarity.Infrequent, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="A visit from slowcake's amanuensis",
        freq=Rarity.Infrequent,
        exchange={
        }
    ))

    # Shadowy >= 69, Renown Crims >= 20
    london_deck.card("A merry sort of crime", Rarity.VeryInfrequent, True, {
        Item.FavCriminals: 1
    })

    good_cards.append(Card(
        name="A merry sort of crime",
        freq=Rarity.VeryInfrequent,
        exchange={
            Item.FavCriminals: 1
        }
    ))

    london_deck.card("A dusty bookshop", Rarity.Rare, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="A dusty bookshop",
        freq=Rarity.Rare,
        exchange={
        }
    ))

    london_deck.card("A little omen", Rarity.Rare, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="A little omen",
        freq=Rarity.Rare,
        exchange={
        }
    ))

    london_deck.card("A disgraceful spectacle", Rarity.Rare, True, {
        Item.Echo: 12.5
    })

    good_cards.append(Card(
        name="A disgraceful spectable",
        freq=Rarity.Rare,
        exchange={
            Item.Echo: 12.5
        }
    ))

    london_deck.card("A voice from a well", Rarity.Rare, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="A voice from a well",
        freq=Rarity.Rare,
        exchange={
        }
    ))

    london_deck.card("A fine day in the flit", Rarity.Unusual, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="A fine day in the flit",
        freq=Rarity.Unusual,
        exchange={
        }
    ))

    london_deck.card("The Paranomastic Newshound", Rarity.Unusual, False, {
        # TODO
    })

    bad_cards.append(Card(
        name="The paranomastic newshound",
        freq=Rarity.Unusual,
        exchange={
        }
    ))

    # ----------------------
    # --- Cards: Relickers
    # ----------------------

    bad_cards.append(Card(
        name="The curt relicker",
        freq=Rarity.VeryInfrequent,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The capering relicker",
        freq=Rarity.VeryInfrequent,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The shivering relicker",
        freq=Rarity.VeryInfrequent,
        exchange={
        }
    ))

    bad_cards.append(Card(
        name="The coquettish relicker",
        freq=Rarity.VeryInfrequent,
        exchange={
        }
    ))

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

    # ----------------------
    # --- Cards: FATE-locked
    # ----------------------

    london_deck.card("A Trade in Souls card", Rarity.Standard, True, {
        Item.Echo: -4, # 50 souls + 5 contracts
        Item.FavConstables: 1,
        Item.FavChurch: 1,
        Item.FavSociety: 1
    })

    good_cards.append(Card(
        name="A trade in souls",
        freq=Rarity.Standard,
        exchange={
            Item.Echo: -4,
            Item.FavConstables: 1,
            Item.FavChurch: 1,
            Item.FavSociety: 1
        }
    ))

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

    good_cards.append(Card(
        name="The OP Aunt card",
        freq=Rarity.Standard,
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

    return london_deck

# hmm this is gonna be harder to model since you can't discard cards
# start by just making everying Play=true
# also the fact that troubled waters is cleared by docking
# shit we also gotta add zee legs gain at some point ugh

# TODO
# - the stuff listed above
# - difficulty by region
# - delighted cards
# - player stats, pull out separate method just for success rate
# - just rewrite the whole cards function to have success & failure inputs

# first past, everything as if it's 100% pass rate