import math
from enum import Enum, auto

from enums import *
import helper.utils as utils
from config import Config
from player import Player

def add_trades(config: Config):
    trade = config.trade
    add = config.add

    efficiency = 300

    # Optimistic
    avg_hp_per_action = 520

    for i in range(0, 8):
        visit_length = 2 ** i
        add({
            Item._UpperRiverRoundTrip: -1,
            Item.Action: -1 * visit_length,
            Item._TracklayerCityAction: visit_length,
        })

    # ballpark
    add({
        Item._TracklayerCityAction: -1,
        Item.HinterlandProsperity: 510
    })

    # TODO monte carlo how many actions it actually takes to get right card
    '''
    How many cards are in a normal TLC deck?
    Max efficiency, fully habituated, 0 waning
    
    Standard Frequency
    - Assist (LEADER)
    - Charting the Hinterland
        - also cash out for puzzling map
    - Genii Locorum
    - Growing the Population
    - Hinterland City Streets
    - Mouths to Feed
    - Near (SITE)
    - The (ALIGNMENT) Way
    - Participate in construction efforts
    - The Housing Market
    
    0.8 Freq
    - Denizens of the Neath (0.8)

    0.5 Freq
    - Day of Rest (0.5)
        hand clear on play
    - Creditor's Greivances (0.5 freq)
    - Troubled Times (0.5 freq)
    
    0.1 Freq
    - A Visitor For (LEADER) (0.1 freq)

    then 3 more that are avoidable but not trivially:
    - Landscape in Moonlight
        - with Moonlit >= 1
    - Merely Passing Through
        - with Spur Line    
    - (LEADER) Leading (ALIGNMENT) (2.0 freq)
        - if leader and alignment have no overlap, eg. furnance + lib/pre


    So that's 10 standard frequency, say another 2 from the rarer cards,
    and then call it 2 more from the avoidable ones. 14 total.

    And the main cash out cards:
    - Imports and Exports
        Has the most cash out options
        If you're going for this one, stay under 6k, and hold 3 in hand
        so odds are ~1/12
        except you're gaining HP faster than you can spend it, so you'll also have
        Flow of Commerce in the deck. which means you oughta play it, or lower the rate.
        1k HP

    - The Flow of Commerce (2.0 freq)
        6k HP
        Adds I&E to hand as well, but 2x freq compensates. Say 1/6.
    
    - A Visit from Virginia (5.0 freq)
        requirement is so high, just treat it as a permanent storylet    

    - Officially Non-Criminal
            25k HP
    '''

    # Cashing in

    for item in (
        Item.NoduleOfTremblingAmber,
        Item.LegalDocument,
        Item.VitalIntelligence,
        Item.CrystallizedEuphoria,
        Item.VerseOfCounterCreed,
        Item.LostResearchAssistant,
        Item.BlackmailMaterial,
    ):
        # Every 14 card draws, play 1 imports
        add({
            Item._TracklayerCityAction: -14,
            item: 1,
            Item.HinterlandProsperity: avg_hp_per_action * 13 - (1000 - efficiency)
        })

        # Every 12 card draws, play 1 imports & 1 flow of commerce
        add({
            Item._TracklayerCityAction: -12,
            item: 1,
            Item.CaptivatingBallad: 1,
            Item.HinterlandProsperity: avg_hp_per_action * 10 - 1000 - 6250
        })

    add({
        Item._TracklayerCityAction: -14,
        Item.PuzzlingMap: 1,
        Item.HinterlandProsperity: avg_hp_per_action * 13 - 1000
    })

    add({
        Item._TracklayerCityAction: -12,
        Item.PuzzlingMap: 1,
        Item.CaptivatingBallad: 1,
        Item.HinterlandProsperity: avg_hp_per_action * 10 - 1000 - 6250
    })    

    # TODO actual rarity like above
    add({
        Item._TracklayerCityAction: -12,
        Item.HinterlandProsperity: -1050 + efficiency,
        Item.AmbiguousEolith: 15,
        Item.UnidentifiedThighBone: 5
    })

    add({
        Item._TracklayerCityAction: -1,
        Item.HinterlandProsperity: -6250,
        Item.HolyRelicOfTheThighOfStFiacre: 1,
        Item.VerseOfCounterCreed: 3,
        Item.ApostatesPsalm: 5
    })

    # Card is 2x rarity so close enough
    add({
        Item._TracklayerCityAction: -6,
        Item.HinterlandProsperity: -6250 + 5 * avg_hp_per_action,
        Item.CaptivatingBallad: 1,
    })

    add({
        Item._TracklayerCityAction: -12,
        Item.HinterlandProsperity: -31250,
        Item.BottleOfFourthCityAirag: 5,
    })

    add({
        Item._TracklayerCityAction: -1,
        Item.HinterlandProsperity: -156000,
        Item.RumourmongersNetwork: 1,
    })

    add({
        Item._TracklayerCityAction: -1,
        Item.HinterlandProsperity: -156000,
        Item.VialOfMastersBlood: 1,
    })

    # amortized betrayal options
    add({
        Item._TracklayerCityAction: -1,
        Item.HinterlandProsperity: -500_000,
        Item.JournalOfInfamy: 10_000,

        # Item.TheCityWaning: 36,
        # Item.FavCriminals: 3
    })

    add({
        Item._TracklayerCityAction: -1,
        Item.HinterlandProsperity: -500_000,
        Item.DubiousTestimony: 10_000,

        # Item.TheCityWaning: 36,
        # Item.FavConstables: 3
    })

    add({
        # Moves city from Marigold to Moulin/Hurlers
        Item._TracklayerCityAction: -1,
        Item.HinterlandProsperity: -500_000,
        Item.InfernalContract: 25_000,
    })    

    # Communing

    # Needs 15 in 3 advanced stats to 100%

    def commune(stat: Item, dc: int, reward: Item):
        config.challenge_trade(stat, dc,
            cost={
                Item._TracklayerCityAction: -1
            },
            on_pass={
                reward: 1
            },
            on_fail={
                Item.Nightmares: 2
            }
        )

    commune(Item.MonstrousAnatomy, 10, Item.TheMindsAscent1)
    commune(Item.ShapelingArts, 10, Item.TheMindsAscent1)
    commune(Item.KatalepticToxicology, 10, Item.TheMindsAscent1)

    commune(Item.ArtisanOfTheRedScience, 10, Item.TheMindsAscent2)
    commune(Item.Zeefaring, 10, Item.TheMindsAscent2)
    commune(Item.StewardOfTheDiscordance, 4, Item.TheMindsAscent2)

    commune(Item.Mithridacy, 10, Item.TheMindsAscent3)
    commune(Item.Glasswork, 10, Item.TheMindsAscent3)
    commune(Item.APlayerOfChess, 10, Item.TheMindsAscent3)

    add({
        Item._TracklayerCityAction: -2,
        Item.MemoryOfMuchLesserSelf: -2,
        Item.TheMindsAscent1: -2,
        Item.TheMindsAscent2: -3,     
        Item.TheMindsAscent3: -4,     
        Item.SearingEnigma: 1
    })
    
    add({
        Item._TracklayerCityAction: -2,
        Item.MemoryOfMuchLesserSelf: -2,
        Item.TheMindsAscent1: -2,
        Item.TheMindsAscent2: -3,     
        Item.TheMindsAscent3: -4,     
        Item.PrimaevalHint: 1
    })
    
    add({
        Item._TracklayerCityAction: -1,
        Item.CrystallizedEuphoria: -5,
        Item.TheCityWaning: -45 # TODO confirm
    })

    add({
        Item._TracklayerCityAction: -1,
        Item.OneiromanticRevelation: -1,
        Item.HinterlandProsperity: 6250
    })