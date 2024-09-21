import numbers
import pickle
import json
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix
from scipy.optimize import linprog
from enum import Enum, auto
from itertools import count

from config import *

from enums import *
import fate.whiskerways
import london.arbor
from utils import *
from player import *

import decks.deck as Decks

import decks.london_deck
import decks.nadir

import time_the_healer

import social_actions as SocialActions
import bazaar as Bazaar
import inventory_conversions as InventoryConversions

import old_rat_market
import rat_market

import professional_activities

import london.uncategorized

import london.laboratory
import london.newspaper
import london.bone_market
import london.hearts_game
import london.heists

import parabola

import unterzee.zailing
import unterzee.khanate
import unterzee.wakeful_eye
import unterzee.port_cecil

import upper_river.uncategorized
import upper_river.upper_river_exchange
import upper_river.ealing_gardens
import upper_river.jericho
import upper_river.evenlode
import upper_river.balmoral
import upper_river.burrow
import upper_river.station_viii
import upper_river.moulin
import upper_river.hurlers
import upper_river.marigold
import upper_river.tracklayers_city

import firmament.hallows_throat
import firmament.midnight_moon

import fate.philosofruits
import fate.upwards
import fate.whiskerways

import numpy as np
import pprint

'''
TODO
- Set up a table/matrix of all the "simple" item conversions and buy/sell options
    - meeting the following conditions
        - exactly one input and one output
        - can be done as much as you like, as often as you like
        - 0 action cost
        - no randomness
    - so buying and selling from the bazaar.
    - this would be used for easy conversions of outputs of our monte carlo sims
    - could also be generalized as a module
    - example:
        Item.RoofChart: {
            Item.Stuiver: 50,
            Item.MoonPearl: 253
        },
        Item.MoonPearl: {
            Item.Echo: 0.01
        }
    - maybe do it as a Shop class so we can control access by player prog

- add railway stuff before more london stuff bc it's prob more relevant

London
- all the chimes & chimes-tier carousels
    - brawling with dockers
    - sunken embassy
    - spider debates
    - whatever other crap i forgot
- all the MYN locations
- forgotten quarter expeditions
- model Airs somehow

Laboratory
- monte carlo sim

Parabola
- most parabolan hunts
- waswood shores?
    - figure out the odds
- basically everything else

Zailing
- plug the monte carlo results into the rest of the model

Khanate
- update w/ zailing monte carlo results
- smuggling
- intrigues

Railway
- TONS of shit
- opportunity deck

bone market exhaustion

crackpot idea
- normalize all trades to 1 echo where possible?
- get a better idea of weights/marginals
- prob make it much more difficult to read
- maybe go halfway and do this for the buy/sell actions and that's it
'''

# placeholder for upconversions and stuff
# if anyone knows the real values please share
default_rare_success_rate = 0.05

# maybe improve slightly with EPA
zailing_epa = 3.0

# lab research per action, somewhat optimistic
lab_rpa = 33

# for modeling actions that can grant more actions eg. the 30% success on the aunt card
replacement_epa = 6.5

# for modeling time spent outside london
replacement_good_card_density = 0.33

# for long trips outside longon/upper river
lost_draw_cost = 0

# # 0.85, 0.74, 0.65
# wounds_multiplier = 0.85
# scandal_multiplier = 0.85
# suspicion_multiplier = 0.85
# nightmares_multiplier = 0.85

# --------------------------------------------
# -------------- Player Config ---------------
# --------------------------------------------

# utils.sum
player_baseline_f2p = Player(
    stats = utils.sum_dicts(baseline_stats(), min_endgame_f2p_bonuses())
    )

player_advanced_f2p = Player(
    stats = utils.sum_dicts(baseline_stats(), advanced_endgame_f2p_bonuses())
    )

player_generic = Player(stats = {
    Stat.Watchful: 330,
    Stat.Shadowy: 330,
    Stat.Dangerous: 330,
    Stat.Persuasive: 330
})

player_generic_monster_hunter = Player(
    profession=Profession.MonsterHunter
)

# aka "cosmogone silvererhand"
player_third_city_silverer = Player(
    ambition=Ambition.BagALegend,
    treasure=Treasure.LongDeadPriestsOfTheRedBird,
    profession=Profession.Silverer,
    stats={
        Stat.Watchful: Player.baseline_watchful + 13,
        Stat.Shadowy: Player.baseline_shadowy + 6,
        Stat.Dangerous: Player.baseline_dangerous,
        Stat.Persuasive: Player.baseline_persuasive
    })

player_bal_licentiate = Player(
    ambition=Ambition.BagALegend,
    treasure=Treasure.WingedAndTalonedSteed,
    profession=Profession.Licentiate,
    stats={
        Stat.Watchful: Player.baseline_watchful,
        Stat.Shadowy: 230 + 97,
        Stat.Dangerous: Player.baseline_dangerous + 6 + 13,
        Stat.Persuasive: Player.baseline_persuasive
    })

player_generic_licentiate = Player(
    ambition=Ambition.NoAmbition,
    treasure=Treasure.NoTreasure,
    profession=Profession.Licentiate,
    stats={
        Stat.Watchful: Player.baseline_watchful,
        Stat.Shadowy: Player.baseline_shadowy + 6,
        Stat.Dangerous: Player.baseline_dangerous,
        Stat.Persuasive: Player.baseline_persuasive
    })

# aka my PC
player_bal_monster_hunter = Player(
    ambition=Ambition.BagALegend,
    treasure=Treasure.WingedAndTalonedSteed,
    profession=Profession.MonsterHunter,
    stats={
        Stat.Watchful: 230 + 102,
        Stat.Shadowy: 230 + 100,
        Stat.Dangerous: 230 + 101,
        Stat.Persuasive: 230 + 91
    })

active_player = player_bal_licentiate

# hack
# `IndexError: list assignment index out of range` => increase this number
# most of this is bone market combinatoric shit
var_buffer = 20_000
num_items = max(Item, key=lambda x: x.value).value
num_vars = num_items + 1 + var_buffer

config = Config(num_vars, active_player)

trade = config.trade

# ---------------- Decks ----------------------------

# london_deck = Decks.create_london_deck(active_player, 6.5, config)
# london_deck = decks.london_deck.create_deck_old(config)

# should just have one deck for each region and dummy "card draws in X" item for each one
zailing_deck = Decks.create_zailing_deck(active_player, Location.SaltSteppes)

# ---------------- Trades ----------------------------

# Plug in the basic economic contraints


actions_per_day = 120
full_draws_per_day = 3
# +10 for the weekly action refresh card
# -3 for rat market entry
actions_per_cycle = (7 * actions_per_day) + 10 - 3

core_constraint = {
    Item.Constraint: 1,
    Item.RootAction: actions_per_cycle,
    Item.VisitFromTimeTheHealer: 1,
    Item.CardDraws: full_draws_per_day * 7 * 10
}

config.add(core_constraint)

config.add({
    Item.RootAction: -1,
    Item.Action: 1
})

config.add({
    Item.RootAction: -1,
    Item.LondonAction: 1
})


# -----------------------------------------------------
# --- Modules
# ----------------------------------------------------

# doing some goofy inversion of control stuff here so that I can just copy paste everything

time_the_healer.add_trades(config)

SocialActions.add_trades(config)
Bazaar.add_trades(config)

rat_market.add_trades(config)

professional_activities.add_trades(active_player, config)

InventoryConversions.add_trades(active_player, config)

decks.london_deck.add_trades(config)

london.uncategorized.add_trades(active_player, config)
london.newspaper.add_trades(active_player, config)
london.laboratory.add_trades(active_player, lab_rpa, config)
london.hearts_game.add_trades(active_player, config)
london.arbor.add_trades(config)
london.heists.add_trades(config)

# london.bone_market.add_trades(active_player, config)

unterzee.khanate.add_trades(active_player, config)
unterzee.wakeful_eye.add_trades(active_player, config)
unterzee.port_cecil.add_trades(active_player, config)
unterzee.zailing.add_trades(active_player, zailing_epa, config)

parabola.add_trades(active_player, config)

upper_river.upper_river_exchange.add_trades(config)
upper_river.uncategorized.add_trades(active_player, config)
upper_river.ealing_gardens.add_trades(active_player, config)
upper_river.jericho.add_trades(config)
upper_river.evenlode.add_trades(active_player, config)
upper_river.balmoral.add_trades(active_player, config)
upper_river.burrow.add_trades(config)
upper_river.station_viii.add_trades(active_player, config)
upper_river.moulin.add_trades(active_player, config)
upper_river.hurlers.add_trades(active_player, config)
upper_river.marigold.add_trades(active_player, config)

# upper_river.tracklayers_city.add_trades(config)

firmament.hallows_throat.add_trades(config)
firmament.midnight_moon.add_trades(config)

# fate.philosofruits.add_trades(active_player, config)
# fate.upwards.add_trades(active_player, config)
# fate.whiskerways.add_trades(config)

# --------------
# Upper River Deck
# -------------

trade(1, zailing_deck.normalized_trade())

# ------------------------------------------
# ---------------- Optimization ------------
# ------------------------------------------

optimize_for = Item.Echo

c = np.zeros(num_vars)
c[optimize_for.value] = -1

opt_result = linprog(c, A_ub=config.A.toarray(), b_ub=config.b, bounds=config.bounds, method='highs')
print(opt_result)

# results = sorted(zip(Item, opt_result.x), key=lambda x: x[1])
# for item, quantity in results:
#     item_name = f"{item.name:40}"
#     if quantity > 0:
#         print(item_name
#         + f"{1/(quantity * actions_per_day):10.5}")
#     else:
#         print(item_name + f"{'unsourced':10}")
    
'''
591 fragments per action
1.28 wings per action

6000 fragments => 10.15 actions
3 wings => 2.34 actions
'''
pp = pprint.PrettyPrinter(indent=4)

print("------Assumptions-------")
# print(f"Core Constraint:"  {})
print(f"Core Constraint:                  {core_constraint}")
# print(f"Total Actions per Day:            {actions_per_day:10}")
# print(f"Cards Drawn per Day:              {cards_seen_per_day:10}")
# print(f"Good Card Density:                {london_good_card_density:10.3f}")

print(f"Optimize For:                     {optimize_for}")
print(f"-Player Stats-")
pp.pprint(active_player.stats)

print("------Summary-------")
# print(f"{str(optimize_for) + ' Per Day:':34}{-1.0/(opt_result.fun):10.3f}")
# print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.3f}")

trades_used = []
# actions_per_cycle = core_constraint[Item.Action]

items_gained = []
items_consumed = []

for i in range(0, len(opt_result.slack)):
    slack = opt_result.slack[i]
    marginal = opt_result.ineqlin.marginals[i]
    if (slack < 1.0 and marginal != 0):
        lose_items = ""
        gain_items = ""
        for ii in range(0, num_items):
            quantity = round(config.A[i, ii],2)
            item = Item(ii)
            if int(quantity) == quantity:
                quantity = int(quantity)
            if quantity < 0:
                lose_items += str(item) + ":" + str(quantity) + "; "
                if item not in items_consumed:
                    items_consumed.append(item)
            if quantity > 0:
                gain_items += str(item) + ":" + str(quantity) + "; "
                if item not in items_gained:
                    items_gained.append(item)
        # trade_items = lose_items + " => " + gain_items            
        # trade_items = trade_items.replace("Item.","")

        lose_items = lose_items.replace("Item.","")
        gain_items = gain_items.replace("Item.","")
        
        action_cost = config.A[i, Item.Action.value]

        trades_used.append([marginal * min(action_cost * -1, -0.01) * actions_per_cycle, lose_items + " => " + gain_items])
        # print("* " + trade_items)
        # print(f"{marginal:.3}       " + lose_items + " => " + gain_items)
        # print(f"")

trades_used.sort()

items_surplus = []
for i in items_gained:
    if i not in (items_consumed):
        items_surplus.append(str(i))

print("-----Gained & Unused-------")
for i in items_surplus:
    print(i)

print("-----Trades In Grind-------")
for i in trades_used:
    print(f"{i[0]:.3}       " + i[1])

print("-----Cycle-------")
print(core_constraint)

print("-----Optimization Target-------")
# print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.5f}")
print(f"{str(optimize_for) + ' Per Cycle ':34}{-1.0/(opt_result.fun):10.5f}")
print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_cycle):10.5f}")
print(f"{'Actions Per ' + str(optimize_for):34}{-(opt_result.fun * actions_per_cycle):10.5f}")

print("-------------------------------")
print("-------------------------------")

# print(london_deck.normalized_trade())
# print(zailing_deck.normalized_trade())
