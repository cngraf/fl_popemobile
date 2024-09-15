from enums import *
from config import Config
from player import Player
from decks.deck import *
import utils

import random

def create_deck(config: Config):
    # quick and dirty version

    # tricky to model since you can only do 1 per go-round
    # also we have not modeled the acquisition of laws
    card_hole_in_your_head = Card("The Hole in your Head", Rarity.Ubiquitous, {
        Item.DiscordantLaw: -1,

        Item.DiscordantSoul: 1,
        Item.Irrigo: 2
    })

    card_a_card_game = Card("A card game", Rarity.Standard, {
        Item.Irrigo: 1,
        Item.TaleOfTerror: 1,
        Item.RomanticNotion: 1
    })

    card_a_familiar_face = Card("A Familiar Face?", Rarity.Standard, {
        Item.Irrigo: 1
    })

    
    card_refreshment = Card("A pause for refreshment", Rarity.Standard, {
        Item.Irrigo: 1,
        Item.CrypticClue: 50
    })

    # Nightmares >= 4
    card_dream_of_motion = Card("A Waking Dream of Motion", Rarity.Standard, {
        Item.Irrigo: 2,
        Item.Nightmares: 1,
        Item.AppallingSecret: 1
    })

    # Nightmares >= 2
    card_dream_of_reflections = Card("A waking dream of reflections", Rarity.Standard, {
        Item.Irrigo: 2,
        Item.Nightmares: 1,
        Item.AppallingSecret: 1
    })

    card_dream_of_water = Card("A waking dream of water", Rarity.Standard, {
        Item.Irrigo: 2,
        Item.Nightmares: 1,
        Item.AppallingSecret: 1
    })

    card_weakness_in_the_air = Card("A Weakness in the Air", Rarity.Standard, {
        Item.Irrigo: 1,
        Item.Nightmares: 1
        # +1 CP all dreams
    })

    card_altarful = Card("An altarful of strangers", Rarity.Standard,
                        exchange= config.challenge_ev(
                            stat = Stat.Persuasive,
                            dc = 200,
                            on_pass= {
                                Item.Irrigo: 1,
                                Item.ExtraordinaryImplication: 1
                            },
                            on_fail= {
                                Item.Irrigo: 1
                            }
                        ))
    
    # TODO: second chance is pretty valuable here
    garden_pass_rate = utils.pass_rate(config.player, Stat.Persuasive, 1000)
    garden_pass_rate_with_second_chance = 1.0 - (1.0 - garden_pass_rate) ** 2
    card_unlikely_garden = Card(
        name= "An Unlikely Garden",
        freq= Rarity.Standard,
        exchange=config.add_weighted_trade(1, (
            (garden_pass_rate_with_second_chance, {
                Item.ConfidentSmile: -1,
                Item.Irrigo: 2,
                Item.SearingEnigma: 1,
            }),
            (1.0 - garden_pass_rate_with_second_chance, {
                Item.Irrigo: 2,
                Item.CrypticClue: 50,
                Item.Nightmares: 1
            })
        )))
        # exchange= config.challenge_ev(
        #     stat= Stat.Persuasive,
        #     dc = 1000, # not a typo!
        #     on_pass= {
        #         Item.Irrigo: 2,
        #         Item.SearingEnigma: 1
        #     },
        #     on_fail= {
        #         Item.Irrigo: 2,
        #         Item.CrypticClue: 50,
        #         Item.Nightmares: 1
        #     }))

    # anything better on this card?
    card_recall = Card(
        "Do you recall how they came to that place",
        Rarity.Standard,
        {
            Item.Irrigo: 1,
            Item.NoduleOfWarmAmber: 1
        })
    
    card_losing = Card("Losing", Rarity.Standard, 
        {
            Item.JournalOfInfamy: -1,
            Item.Irrigo: 2,
            Item.UncannyIncunabulum: 1
        })
    
    card_lost_at_sea = Card("Lost at Sea", Rarity.Standard, {
        Item.Irrigo: 1
    })
    
    # FATE option
    card_old_bones = Card("Old Bones", Rarity.Standard, {
        Item.Irrigo: 1,
        Item.VisionOfTheSurface: 1,
        Item.RomanticNotion: 1,
        Item.MemoryOfDistantShores: 1,
        Item.AppallingSecret: 4,
        Item.DramaticTension: 1
    })

    card_old_sins = Card("Old sins", Rarity.Standard, {
        Item.MemoryOfMuchLesserSelf: 1,
        Item.ExtraordinaryImplication: 1.5,
        Item.Irrigo: 1
    })

    card_something_moves = Card("Something moves", Rarity.Standard, {
        Item.Irrigo: 1
    })

    # well this is gonna be hard to model
    # let's say you play this at 8
    card_the_captainfalcon = Card("The Catafalquerie", Rarity.Standard, {
        Item.ExtraordinaryImplication: 4, 
        Item.Irrigo: 2
    })

    # TODO: any of these might be the best option
    # need to add second chances to the rest of the model
    # shadowy easiest to acquire but hardest to cash out
    card_battles = Card("The End of Battles", Rarity.Standard, {
        # Item.ConfidentSmile: -3,
        Item.SearingEnigma: 1,
        Item.Irrigo: 2
    })

    card_web = Card("The Web", Rarity.Standard, {
        Item.Irrigo: 1,
        Item.ExtraordinaryImplication: 1,
        Item.Nightmares: 2
    })

    card_imprisoned = Card("Unjustly imprisoned!", Rarity.Standard, {
        Item.Irrigo: 1
    })

    card_woods_in_winter = Card("Woods in winter", Rarity.Standard, {
        Item.DramaticTension: 1,
        Item.FavRevolutionaries: 1,
        Item.FavGreatGame: 1,
        Item.FavSociety: 1
    })

    # gonna handle hole in your head separately
    return [
        # good cards
        card_battles,
        card_woods_in_winter,
        card_unlikely_garden,
        card_old_bones,
        card_losing,
        card_the_captainfalcon,
        card_old_sins,

        # the rest
        card_altarful,
        card_web,
        card_refreshment,
        card_imprisoned,
        card_recall,
        card_a_card_game,
        card_lost_at_sea,
        card_something_moves,

        card_a_familiar_face,
        card_weakness_in_the_air,
        card_dream_of_motion,
        card_dream_of_reflections,
        card_dream_of_water
    ]

def simulate_single_visit(config: Config, cards_by_play_count):
    card_priority = create_deck(config)


    # all standard, ignoring rarity for now
    draw_pile = card_priority.copy()
    hand = []
    total_trade = {
        Item.Action: -4,
        Item.Irrigo: 2,
        Item.DiscordantSoul: 1
    }

    def draw_card():
        random.shuffle(draw_pile)
        hand.append(draw_pile.pop())

    def play_card(card: Card):
        total_trade[Item.Action] -= 1
        utils.add_items(total_trade, card.exchange)

        hand.remove(card)
        draw_pile.append(card)

    def play_best_card():
        hand.sort(key= lambda x : card_priority.index(x))

        cards_by_play_count[card_priority.index(hand[0])] += 1

        play_card(hand[0])
        
    draw_card()
    draw_card()
    draw_card()

    # can improve by playing multiple high-value cards before redraw?
    while total_trade[Item.Irrigo] < 10:
        play_best_card()
        draw_card()

    return total_trade

def simulate_full(config: Config, runs: int):
    cummulative_trades = {}
    normalized_trade = {}

    card_count = [0] * 20

    for i in range(0, runs + 1):
        result = simulate_single_visit(config, card_count)
        utils.add_items(cummulative_trades, result)

    total_actions = abs(cummulative_trades[Item.Action])

    for key, val in cummulative_trades.items():
        normalized_trade[key] = val / total_actions

    print(f"Cave of the Nadir average after {runs} runs: ")
    print(normalized_trade)
    print(card_count)

    return normalized_trade