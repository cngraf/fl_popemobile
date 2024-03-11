from enums import *
from utils import *

class Deck:
    def __init__(self, name, size_handicap):
        self.name = name
        self.deck_size = size_handicap # from holding cards in hand
        self.num_good_cards = 0
        self.total_items = {}

    def card(self, name, freq, play, exchanges):
        copies = freq.value
        self.deck_size += copies
        if (play):
            self.num_good_cards += copies
            for item, value in exchanges.items():
                self.total_items[item] = self.total_items.get(item, 0) + (copies * value)

    def normalized_trade(self):
        trade = {}
        trade[Item.CardDraws] = -1
        for item, value in self.total_items.items():
            trade[item] = value / self.deck_size
        return trade

def add_trades(trade):
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
        wounds_multiplier,
        scandal_multiplier,
        suspicion_multiplier,
        nightmares_multiplier,
        replacement_epa
        ):


    london_deck = Deck("London", -400)

    # Lair in the Marshes
    london_deck.card("Lair in the Marshes", Rarity.Standard, True, {
        Item.FavSociety: 1,
        Item.CertifiableScrap: 1,
        Item.Nightmares: 1 * nightmares_multiplier
    })

    # The Tower of Knives: Difficulties at a Smoky Flophouse
    # The next victim?
    knives_rare_success_rate = 0.05
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

    # The Tower of Sun and Moon: a Reservation at the Royal Bethlehem Hotel
    london_deck.card("Royal Beth lodings", Rarity.Frequent, False, {
        Item.CertifiableScrap: 3
    })

    # -----------------------------------------------------
    # --- Cards: Companions
    # ----------------------------------------------------

    london_deck.card("What will you do with your [connected pet]?", Rarity.Standard, True, {
        Item.ConnectedPetCard: 1
    })


    # With Bewildering Procession
    london_deck.card("Attend to your spouses", Rarity.VeryInfrequent, True, {
        Item.FavBohemians: 1
    })

    # -----------------------------------------------------
    # --- Cards: Other Equipment
    # ----------------------------------------------------

    # avoidable
    london_deck.card("A day out in your Clay Sedan Chair", Rarity.Standard, True, {
        Item.FavSociety: 1,
        Item.Hedonist: -3
    })

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

    # -----------------------------------------------------
    # --- Cards: Factions
    # ----------------------------------------------------

    # Bohemians
    london_deck.card("Bohemians Faction", Rarity.Standard, True, {
        Item.Echo: -1.2,
        Item.FavBohemians: 1
    })

    # Church
    london_deck.card("Church Faction", Rarity.Standard, True, {
        Item.Echo: -0.1,
        Item.FavChurch: 1
    })

    # Constables
    london_deck.card("Constables Faction", Rarity.Standard, False, {
        Item.Echo: -0.1,
        Item.FavConstables: 1
    })

    # Criminals
    london_deck.card("Criminals Faction", Rarity.Standard, True, {
        Item.Suspicion: 1 * suspicion_multiplier,
        Item.FavCriminals: 1,
    })

    # Docks
    london_deck.card("Docks Faction", Rarity.Standard, True, {
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
    london_deck.card("Rev Faction", Rarity.Standard, True, {
        Item.Echo: -0.5,
        Item.FavRevolutionaries: 1 
    })

    # RubberyMen
    london_deck.card("Rubbery Faction", Rarity.Standard, False, {
        Item.Echo: -0.1,
        Item.FavRubberyMen: 1
    })

    # Society
    london_deck.card("Society Faction", Rarity.Standard, True, {
        Item.Echo: -0.5,
        Item.FavSociety: 1
    })

    # Tomb-Colonies
    london_deck.card("Tomb Colonies Faction", Rarity.Standard, False, {
        Item.FavTombColonies: 1
    })

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

    # ----------------------
    # --- Cards: General London
    # ----------------------

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
        # TODO
    })


    london_deck.card("A Polite Invitation", Rarity.Standard, False, {
        # TODO: Separate entry for party carousel
    })

    london_deck.card("Give a Gift!", Rarity.Standard, False, {
        # TODO
    })

    # > A disgraceful spectacle
    london_deck.card("A day at the races", Rarity.Standard, True, {
        Item.FavChurch: 1
    })

    # Avoidable!
    # Sulky Bat >= 1
    london_deck.card("A parliament of bats", Rarity.Standard, False, {
        Item.VisionOfTheSurface: -1,
        Item.FavGreatGame: 1
    })

    london_deck.card("One's public", Rarity.Standard, False, {
        # TODO    
    })

    london_deck.card("A Day with God's Editors", Rarity.Standard, False, {
        Item.TaleOfTerror: -1,
        Item.FavChurch: 1
    })

    # Avoidable? unsure
    london_deck.card("Bringing the revolution", Rarity.Standard, True, {
        Item.CompromisingDocument: -1,
        Item.FavRevolutionaries: 1
    })

    # Time limited, also lots of good options?
    # Maybe just leave it out?
    # london_deck.card("The Calendrical Confusion of 1899", Rarity.Standard, True, {
    #     Item.ScrapOfIncendiaryGossip: 14
    # })

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

    # # avoidable with no Favours: Hell
    # london_deck.card("A consideration for services rendered", Rarity.Standard, {
    #     # TODO
    # })

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
    london_deck.card("A merry sort of crime", Rarity.VeryInfrequent, True, {
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

    # ----------------------
    # --- Cards: Relickers
    # ----------------------

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


def chasing_ev(region, isAdvanced, pass_rate = 1.0, rare_success_rate = 0.1):
    gain_from_basic = 0
    gain_from_advanced = 0
    plunder = 0

    if region == Location.HomeWaters:
        gain_from_basic = 8
        gain_from_advanced = 8
        plunder = 5334
    elif region == Location.ShepherdsWash:
        gain_from_basic = 8
        gain_from_advanced = 9
        plunder = 5350
    elif region == Location.Stormbones:
        gain_from_basic = 8
        gain_from_advanced = 9
        plunder = 5403
    elif region == Location.TheSeaOfVoices:
        gain_from_basic = 8
        gain_from_advanced = 10
        plunder = 5568
    elif region == Location.TheSaltSteppes:
        gain_from_basic = 13
        gain_from_advanced = 14
        plunder = 5597
    elif region == Location.ThePillaredSea:
        gain_from_basic = 14
        gain_from_advanced = 15
        plunder = 5597    
    elif region == Location.TheSnares:
        gain_from_basic = 15
        gain_from_advanced = 16
        plunder = 5659

    gain_on_success = gain_from_advanced if isAdvanced else gain_from_basic

    # why did we add a plunder var
    return pass_rate * (gain_on_success + (2 * rare_success_rate))

def plunder_ev(region, isAdvanced, player_stat, rare_success_rate = 0.1):
    gain_from_basic = 0
    gain_from_advanced = 0

    basic_challenge = 0
    advanced_challenge = 0

    if region == Location.HomeWaters:
        gain_from_basic = 300
        gain_from_advanced = 250

        basic_challenge = 160
        advanced_challenge = 5
    elif region == Location.ShepherdsWash:
        gain_from_basic = 300
        gain_from_advanced = 300

        basic_challenge = 160
        advanced_challenge = 6
    elif region == Location.Stormbones:
        gain_from_basic = 300
        gain_from_advanced = 300

        basic_challenge = 160
        advanced_challenge = 6        
    elif region == Location.TheSeaOfVoices:
        gain_from_basic = 300
        gain_from_advanced = 350

        basic_challenge = 160
        advanced_challenge = 7        
    elif region == Location.TheSaltSteppes:
        gain_from_basic = 400
        gain_from_advanced = 400

        basic_challenge = 160
        advanced_challenge = 11        
    elif region == Location.ThePillaredSea:
        gain_from_basic = 450
        gain_from_advanced = 450

        basic_challenge = 160
        advanced_challenge = 12        
    elif region == Location.TheSnares:
        gain_from_basic = 500
        gain_from_advanced = 500

        basic_challenge = 160
        advanced_challenge = 13        

    gain_on_success = 0
    success_rate = 0.0

    if isAdvanced:
        gain_on_success = gain_from_advanced
        success_rate = narrow_challenge_success_rate(player_stat, advanced_challenge)
    else:
        gain_on_success = gain_from_basic
        success_rate = broad_challenge_success_rate(player_stat, basic_challenge)

    # why did we add a plunder var
    return success_rate * (gain_on_success + (50 * rare_success_rate))

def create_zailing_deck(player_stats, region, profession, treasure):
    # hold "Creaking above" card, and one other infrequent one
    deck = Deck("Zailing", -200)

    troubled_waters_multiplier = 0.65 # hat plus cruiser

    # with FATE commodore companion
    # wiki does not have actual figures, just guessing
    deck.card("A Corvette", Rarity.Standard, True, {
        Item.Suspicion: -2,
        Item.TroubledWaters: -2
    })

    deck.card("Giant Enemy Crab", Rarity.Infrequent, True, {
        Item.TroubledWaters: -2
    })    

    deck.card("Huge terrible beast", Rarity.Infrequent, True, {
        Item.TroubledWaters: 3 * troubled_waters_multiplier
    })    

    # deck.card("A navigation error", Rarity.Infrequent, True, {
    #     Item.NavigationErrorCard: 1
    # })

    if treasure == Treasure.FalseStartOfYourOwn:
        # TODO: figure out how to allow the best split
        rate_use_tw_reduction = 0.9
        deck.card("Navigation error - False-star", Rarity.Infrequent, True, {
            Item.TroubledWaters: -5 * rate_use_tw_reduction + 2 * troubled_waters_multiplier * (1 - rate_use_tw_reduction),
            Item.ChasingDownYourBounty: chasing_ev(region, True) * (1 - rate_use_tw_reduction)
        })

        deck.card("Your False-Star", Rarity.Standard, True, {
            Item.TroubledWaters: -5
        })
    else:
        deck.card("Navigation error", Rarity.Infrequent, True, {
            Item.TroubledWaters: 2 * troubled_waters_multiplier,
            Item.ChasingDownYourBounty: chasing_ev(region, True)
        })

    deck.card("A ship of zealots", Rarity.Infrequent, True, {
        Item.StashedTreasure: plunder_ev(region, True, 20)
    })

    # TODO: cladery heart option
    deck.card("A spit of land", Rarity.Infrequent, True, {
        Item.TroubledWaters: 1 * troubled_waters_multiplier
    })

    # TODO zee peril values by region
    # probably skip/hold this card
    deck.card("Creaking from above", Rarity.Standard, False, {
        Item.ShardOfGlim: 250,
        Item.TroubledWaters: 11.5 * troubled_waters_multiplier
    })

    deck.card("Passing a lightship", Rarity.Infrequent, True, {
        Item.ChasingDownYourBounty: chasing_ev(region, False)
    })

    if profession == Profession.MonsterHunter:
        # doesn't increase TW, might be better?
        deck.card("Rats in the hold - Harpoon", Rarity.Infrequent, True, {
            Item.RatOnAString: 100
        })
    else:
        deck.card("Rats in the hold", Rarity.Infrequent, True, {
            Item.TroubledWaters: 2 * troubled_waters_multiplier,
            Item.ChasingDownYourBounty: chasing_ev(region, False)
        })

    deck.card("Clinging coral mass", Rarity.Infrequent, True, {
        # ignoring rare success bc lazy
        Item.TroubledWaters: 2 * troubled_waters_multiplier
    })

    deck.card("The fleet of truth", Rarity.Infrequent, True, {
        Item.TroubledWaters: 2 * troubled_waters_multiplier,
        Item.ChasingDownYourBounty: chasing_ev(region, False)
    })

    # # TODO come back to this one. only appears with TW 4+
    # # with zub it's good, otherwise you never play it
    # deck.card("The killing wind", Rarity.Standard, True, {
    #     Item.TroubledWaters: -2,
    #     Item.ZeeZtory: 4.5
    # })

    # with fruits of the Zee item
    # deck.card("What do the drownies sing", Rarity.Standard, True, {
    #     Item.TroubledWaters: -5
    # })

    deck.card("What do the drownies sing", Rarity.Standard, True, {
        Item.TroubledWaters: 2 * troubled_waters_multiplier,
        Item.ChasingDownYourBounty: chasing_ev(region, True)
    })

    if region == Location.TheSaltSteppes:
        if (profession == Profession.MonsterHunter):
            deck.card("A Chelonite hunting ketch", Rarity.Standard, True, {
                Item.TroubledWaters: -4
                # TODO: other items
            })
        else:
            deck.card("A Chelonite hunting ketch", Rarity.Standard, True, {
                Item.ChasingDownYourBounty: 16
            })

        # TODO: other options
        deck.card("A distant gleam", Rarity.Standard, True, {
            Item.MemoryOfDistantShores: 5,
            Item.TroubledWaters: 2 * troubled_waters_multiplier
        })

        deck.card("A Khaganian patrol vessel", Rarity.Standard, False, {
            Item.TroubledWaters: 4 * troubled_waters_multiplier,
            Item.ChasingDownYourBounty: chasing_ev(region, True)
        })

    return deck