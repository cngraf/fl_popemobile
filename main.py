import numbers
import pickle
import json
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix
from scipy.optimize import linprog
from enum import Enum, auto
from itertools import count
import pprint
from tabulate import tabulate
from termcolor import colored

from config import *

from enums import *
import fate.whiskerways
import london.arbor
from utils import *
import player as player

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
import london.hearts_game
import london.heists

import bone_market.trades

import parabola

import unterzee.gaiders_mourn
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
import upper_river.decks

import firmament.hallows_throat
import firmament.midnight_moon

import fate.philosofruits
import fate.upwards
# import fate.whiskerways

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
- add more experiments & workers to monte carlo sim

Parabola
- most parabolan hunts
- waswood shores?
    - figure out the odds
- basically everything else
- do a sim of parabolan war?
    - wiki calc seems pretty good tho

Zailing
- plug the monte carlo results into the rest of the model

Khanate
- mostly done?

Railway
- deck monte carlo sim is done!
    - gotta plug into the optimizer now
- let's see what are we still missing
- Ealing
    - helicon house: OK, not perfect
    - butcher: done
    - spa: TODO low prio
    - passenger area: TODO?
- Jericho
    - canal cruising: DONE
    - curio stall: done?
    - library: DONE
    - favours: done
- Balmoral
    - Crathie: idk
    - Castle: TODO just add to TtH
    - woods: done? might be missing fox
    - smuggler: not econ
    - clay highwayman: TODO bandit carousel
    - cabinet noir
        - deciphering: TODO?
        - cover identities: OK, bit hacky
- Station VIII
    - kitchen: partially done? TODO
    - alchemy: TODO
- Burrow
    - nothing repeatable afaik
- Moulin
    - expeditions: partial, TODO monte carlo sim
    - monographs: very simplified, TODO
- Hurlers
    - adulterine castle: TODO
    - digging: TODO
    - goatball: TODO
    - any other repeatable discordance stuff: TODO
- Marigold
    - wtf do they even have here
bone market exhaustion

crackpot idea
- normalize all trades to 1 echo where possible?
- get a better idea of weights/marginals
- prob make it much more difficult to read
- maybe go halfway and do this for the buy/sell actions and that's it
'''

# # placeholder for upconversions and stuff
# # if anyone knows the real values please share
# default_rare_success_rate = 0.05

# # maybe improve slightly with EPA
# zailing_epa = 3.0

# lab research per action, somewhat optimistic
lab_rpa = 33

# # for modeling actions that can grant more actions eg. the 30% success on the aunt card
# replacement_epa = 6.5

# # for modeling time spent outside london
# replacement_good_card_density = 0.33

# # for long trips outside longon/upper river
# lost_draw_cost = 0

# # 0.85, 0.74, 0.65
# wounds_multiplier = 0.85
# scandal_multiplier = 0.85
# suspicion_multiplier = 0.85
# nightmares_multiplier = 0.85

# --------------------------------------------
# -------------- Player Config ---------------
# --------------------------------------------

active_player = player.player_third_city_silverer

# hack
# `IndexError: list assignment index out of range` => increase this number
# most of this is bone market combinatoric shit
var_buffer = 5_000
num_items = max(Item, key=lambda x: x.value).value
print(num_items)
num_vars = num_items + 1 + var_buffer

config = Config(num_vars, active_player)

trade = config.trade


# -----------------------------------------------------
# --- Modules
# ----------------------------------------------------

# doing some goofy inversion of control stuff here so that I can just copy paste everything

time_the_healer.add_trades(config)

SocialActions.add_trades(config)
Bazaar.add_trades(config)

rat_market.add_trades(config)

professional_activities.add_trades(config)

InventoryConversions.add_trades(active_player, config)

# decks.london_deck.add_trades(config)

london.uncategorized.add_trades(active_player, config)
london.newspaper.add_trades(active_player, config)
london.laboratory.add_trades(active_player, lab_rpa, config)
london.hearts_game.add_trades(active_player, config)
london.arbor.add_trades(config)
london.heists.add_trades(config)

bone_market.trades.add_trades(config)

unterzee.khanate.add_trades(active_player, config)
unterzee.wakeful_eye.add_trades(active_player, config)
unterzee.port_cecil.add_trades(active_player, config)
unterzee.gaiders_mourn.add_trades(config)

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
upper_river.marigold.add_trades(config)
upper_river.decks.add_trades(config)

upper_river.tracklayers_city.add_trades(config)

firmament.hallows_throat.add_trades(config)
firmament.midnight_moon.add_trades(config)

# fate.philosofruits.add_trades(active_player, config)
# fate.upwards.add_trades(active_player, config)
# fate.whiskerways.add_trades(config)

# ------------------------------------------
# ---------------- Optimization ------------
# ------------------------------------------

# ---------------- Trades ----------------------------

# Plug in the basic economic contraints

input_per_cycle = 7 * 120

actions_per_day = 120
full_draws_per_day = 3
# +10 for the weekly action refresh card
# -3 for rat market entry
actions_per_week = (7 * actions_per_day) + 10 - 3

optimize_input = Item.Action
optimize_for = Item.Echo

# input_per_cycle

core_constraint = {
    Item.Constraint: 1,
    optimize_input: input_per_cycle,
    # Item.VisitFromTimeTheHealer: 1,
    # Item._BoneMarketRotation: 1,
    Item._RatMarketRotation: 1,
    Item._CardDraws: full_draws_per_day * 7 * 10
}

config.add(core_constraint)

c = np.zeros(num_vars)
c[optimize_for.value] = -1

opt_result = linprog(c, A_ub=config.A.toarray(), b_ub=config.b, bounds=config.bounds, method='highs')
# print(opt_result)

# Printing


trades_used = []
free_item_conversions = []
# actions_per_cycle = core_constraint[Item.Action]

items_gained = []
items_consumed = []

for i in range(0, len(opt_result.slack)):
    slack = opt_result.slack[i]
    marginal = opt_result.ineqlin.marginals[i]
    if (slack < 1.0 and marginal != 0):
        lose_items = ""
        gain_items = ""
        count_terms = 0
        for ii in range(0, num_items):
            quantity = round(config.A[i, ii],2)
            item = Item(ii)
            if int(quantity) == quantity:
                quantity = int(quantity)
            if quantity < 0:
                count_terms += 1
                lose_items += item.name + ":" + str(quantity) + "; "
                if item not in items_consumed:
                    items_consumed.append(item)
            if quantity > 0:
                count_terms += 1
                gain_items += item.name + ":" + str(quantity) + "; "
                if item not in items_gained:
                    items_gained.append(item)
        # trade_items = lose_items + " => " + gain_items            
        # trade_items = trade_items.replace("Item.","")

        # lose_items = lose_items.replace("Item.","")
        # gain_items = gain_items.replace("Item.","")
        
        action_cost = config.A[i, Item.Action.value]
        trade = [marginal * 1000, lose_items, gain_items]

        if count_terms == 2 and action_cost == 0:
            free_item_conversions.append(trade)
        else:
            # trades_used.append([marginal * min(action_cost * -1, -0.01) * input_per_cycle, lose_items + " => " + gain_items])
            trades_used.append([marginal, lose_items, gain_items])

trades_used.sort()

items_surplus = []
for i in items_gained:
    if i not in (items_consumed):
        items_surplus.append(str(i))

pp = pprint.PrettyPrinter(indent=4)

# print("------Assumptions-------")
# print(f"Core Constraint:")
# for item, val in core_constraint.items():
#     print(f"|  {item.name:<30} {val}\n")


print(f"Optimize For:                     {optimize_for.name}")
print(f"-Player Stats-")
pp.pprint(active_player.qualities)

# print("------Summary-------")
# # print(f"{str(optimize_for) + ' Per Day:':34}{-1.0/(opt_result.fun):10.3f}")
# # print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.3f}")


# print("-----Gained & Unused-------")
# for i in items_surplus:
#     print(i)

# print("-----Trades In Grind-------")
# for i in trades_used:
#     # print(f"{i[0]:.3}       " + i[1])
#     print(f"{i[0]:<10.3}{i[1]:<20} => {i[2]}")

# print("-----Cycle-------")
# print(core_constraint)

# print("-----Optimization Target-------")
# items_per_input = -1.0/(input_per_cycle * opt_result.fun)
# # print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.5f}")
# print(f"{optimize_for.name} per {optimize_input.name}: {items_per_input:10.5f}")
# print(f"{optimize_input.name} per {optimize_for.name}: {1.0/items_per_input:10.5f}")
# # print(f"{str(optimize_for) + ' Per Action':34}{items_per_cycle:10.5f}")
# # print(f"{'Actions Per ' + str(optimize_for):34}{-(opt_result.fun * actions_per_cycle):10.5f}")

# print("-------------------------------")


# Optional: Colorized output using termcolor (you can replace with colorama)

# Header with color
print(colored("\n------ Assumptions -------", "green", attrs=['bold']))
print(f"Core Constraint:")
# for item, val in core_constraint.items():
#     print(f"|  {item.name:<30} : {val}")
pp.pprint(core_constraint.items())

# Optimize For section with color
print(colored(f"\nOptimize For: {optimize_for.name}", "cyan", attrs=['bold']))
print("\n-Player Stats-")
pp.pprint(active_player.qualities)

# Summary section
print(colored("\n------ Summary -------", "green", attrs=['bold']))

def wrap_text(text, width=50):
    items = text.split('; ')  # Split the text by '; '
    wrapped_items = []
    for item in items:
        # Wrap long items
        if len(item) > width:
            wrapped_items.append('\n'.join([item[i:i+width] for i in range(0, len(item), width)]))
        else:
            wrapped_items.append(item)
    return '\n'.join(wrapped_items)  # Rejoin with ';\n' to place each item on a new line

# Format trade data for table
conversion_data = []
for trade in free_item_conversions:
    wrapped_loss = wrap_text(trade[1], width=40)
    wrapped_gain = wrap_text(trade[2], width=40)
    conversion_data.append([f"{trade[0]:.3f}", wrapped_loss, wrapped_gain])

# Use a simpler table format for better readability
print("\n----- Conversions -------")
print(tabulate(conversion_data, headers=["Marginal", "Loss", "Gain"], tablefmt="fancy_grid"))

# Format trade data for table
trade_data = []
for trade in trades_used:
    wrapped_loss = wrap_text(trade[1], width=40)
    wrapped_gain = wrap_text(trade[2], width=40)
    trade_data.append([f"{trade[0]:.3f}", wrapped_loss, wrapped_gain])

# Use a simpler table format for better readability
print("\n----- Actions -------")
print(tabulate(trade_data, headers=["Marginal", "Loss", "Gain"], tablefmt="fancy_grid"))

# Surplus items
print(colored("\n----- Gained & Unused Items -------", "cyan", attrs=['bold']))
for i in items_surplus:
    print(i)

# Cycle information
print(colored("\n----- Constraint (per week) -------", "green", attrs=['bold']))
pp.pprint(core_constraint)

# Optimization results
print(colored("\n----- Optimization Target -------", "green", attrs=['bold']))
items_per_input = -1.0 / (input_per_cycle * opt_result.fun)
print(f"{optimize_for.name} per Week:   {-1.0 / opt_result.fun:10.5f}")
print(f"{optimize_for.name} per {optimize_input.name}: {items_per_input:10.5f}")
print(f"{optimize_input.name} per {optimize_for.name}: {1.0 / items_per_input:10.5f}")

print(colored("\n-------------------------------", "yellow", attrs=['bold']))
