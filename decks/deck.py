from enums import *
from utils import *
from config import Config
from player import Player

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


class Card:
    name: str
    freq: Rarity
    exchange: dict
    discardable: bool
    grade: Grade

    def __init__(self, name: str,
                 freq: Rarity,
                 grade: Grade = Grade.Good,
                 discardable: bool = True,
                 exchange = {}):
        self.name = name
        self.freq = freq
        self.score = grade
        self.discardable: discardable
        self.exchange = exchange
        
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


def create_zailing_deck(player, region):
    # hold "Creaking above" card, and one other infrequent one
    deck = Deck("Zailing", -200)

    player_stats = player.stats
    profession = player.profession
    treasure = player.treasure

    troubled_waters_multiplier = menace_multiplier(player.troubled_waters_reduction)

    # # non-piracy version
    # # with FATE commodore companion
    # # wiki does not have actual figures, just guessing
    # deck.card("A Corvette (no piracy)", Rarity.Standard, True, {
    #     Item.Suspicion: -2,
    #     Item.TroubledWaters: -2
    # })

    deck.card("A Corvette (piracy)", Rarity.Standard, True, {
        Item.ChasingDownYourBounty: 8,
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