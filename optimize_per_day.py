import numbers
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix
from scipy.optimize import linprog
from enum import Enum, auto
from itertools import count

from enums import *
from utils import *
from player import *

import social_actions as SocialActions
import decks as Decks
import bazaar as Bazaar
import inventory_conversions as InventoryConversions
import rat_market as RatMarket



import london.uncategorized

import london.laboratory
import london.newspaper
import london.bone_market
import london.hearts_game

import parabola

import unterzee.zailing
import unterzee.khanate
import unterzee.wakeful_eye
import unterzee.port_cecil

import upper_river.uncategorized
import upper_river.ealing_gardens
import upper_river.jericho
import upper_river.evenlode
import upper_river.balmoral
import upper_river.burrow
import upper_river.station_viii
import upper_river.moulin
import upper_river.hurlers
import upper_river.marigold

import fate.philosofruits
import fate.upwards

import numpy as np
import pprint

'''
TODO
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
- model the actual deck & bonus payoffs
- highly dependent on exclusive character choices?
    - ambition, profession, etc.
- sounds like a lot of work payoff so putting this off unless something looks esp. promising

Parabola
- parabolan war
- most parabolan hunts
- waswood shores?
    - figure out the odds
- basically everything else

Zailing
- godfall
- polythreme
- irem
- other port cecil options
- hunting the beasts
- random smaller islands

Khanate
- model the round-trip costs
- smuggling
- intrigues

Railway
- TONS of shit
- opportunity deck
- TRACKLAYER CITY

short term
- Check out Red (free) cards esp. Discordance stuff
- check location-specific London cards
    - skin of the bazaar?
    - that university one for TC favours
- bone market exhaustion
    - model it as just 4/7ths of a point per day?
    - fuck maybe we have to move to a per-week basis blergh

medium term
- option to optimize for hinterland scrip instead of echoes
    - fuck it optimize for any item
    - it already does this, just the option for the terminal output
    
long term
- incorporate a given character's capabilities
    - what are your stats, what various options do you have unlocked
    - in general more fine-grained control over the various base assumptions
'''

class Config:
    def __init__(self):
        self.actions_per_day = 120.0
        self.cards_seen_per_day = 40

# Important Parameters
# actions doesn't matter on its own until I add some weekly+ stuff
# but it does matter relative to cards seen per day
actions_per_day = 120.0
cards_seen_per_day = 40

# placeholder for upconversions and stuff
# if anyone knows the real values please share
default_rare_success_rate = 0.05

# maybe improve slightly with EPA
zailing_epa = 3.2

# lab research per action, somewhat optimistic
lab_rpa = 33

# for modeling actions that can grant more actions eg. the 30% success on the aunt card
replacement_epa = 6.5

# for modeling time spent outside london
replacement_good_card_density = 0.33

# for long trips outside longon/upper river
lost_draw_cost = 0

# 0.85, 0.74, 0.65
wounds_multiplier = 0.85
scandal_multiplier = 0.85
suspicion_multiplier = 0.85
nightmares_multiplier = 0.85

# --------------------------------------------
# -------------- Player Config ---------------
# --------------------------------------------    
# TODO: separate class?

baseline_player = Player(stats = {
    Stat.Watchful: 230 + 92,
    Stat.Shadowy: 230 + 73,
    Stat.Dangerous: 230 + 83,
    Stat.Persuasive: 230 + 85,
})

player_third_city_silverer = Player(
    ambition=Ambition.BagALegend,
    treasure=Treasure.LongDeadPriestsOfTheRedBird,
    profession=Profession.Silverer,
    stats={
        Stat.Watchful: 330,
        Stat.Shadowy: 330,
        Stat.Dangerous: 330,
        Stat.Persuasive: 330
    })


active_player = player_third_city_silverer


def per_day(exchanges):
    n = next(counter)
    b[n] = 1
    for item, value in exchanges.items():
        A[n, item.value] = value

def trade(actionCost, exchanges):
    n = next(counter)
    b[n] = 0
    A[n, Item.Action.value] = -1 * actionCost
    for item, value in exchanges.items():
        A[n, item.value] = value

def railway_card(name, freq, location, isGood, exchanges):
    # dummy alias for now
    trade(1, exchanges)

# hack
var_buffer = 3000
num_items = max(Item, key=lambda x: x.value).value
num_vars = num_items + 1 + var_buffer

A = lil_matrix((num_vars, num_vars))

b = [1]*num_vars
counter = count(start=-1)

bounds = [(0, None) for _ in range(num_vars)]

# in practice it seems this rarely affects the output, but it makes me feel better
# I don't know if this even works the way I think it does as far as modeling long-term stockpiling
# but if you set it too low, you will lock out certain trades
# eg setting the upper bound of Bohemian favours to 3 will lock out the Jericho option
# so really it's a source of bugs more than anything else
# still keeping it in

# important that menace is capped at 0
# ensures any gains are pre-paid for
bounds[Item.Wounds.value] = (None, 0)
bounds[Item.Scandal.value] = (None, 0)
bounds[Item.Suspicion.value] = (None, 0)
bounds[Item.Nightmares.value] = (None, 0)

bounds[Item.TroubledWaters.value] = (None, 35)

bounds[Item.Hedonist.value] = (0, 55)

bounds[Item.SeeingBanditryInTheUpperRiver.value] = (0, 36)

bounds[Item.ConnectedBenthic.value] = (0, 800)

bounds[Item.Tribute.value] = (0, 260)
bounds[Item.TimeAtWakefulCourt.value] = (0, 13)
bounds[Item.TimeAtJerichoLocks.value] = (0, 5)

bounds[Item.FavBohemians.value] = (0, 7)
bounds[Item.FavChurch.value] = (0, 7)
bounds[Item.FavConstables.value] = (0, 7)
bounds[Item.FavCriminals.value] = (0, 7)
bounds[Item.FavDocks.value] = (0, 7)
bounds[Item.FavGreatGame.value] = (0, 7)
bounds[Item.FavHell.value] = (0, 7)
bounds[Item.FavRevolutionaries.value] = (0, 7)
bounds[Item.FavRubberyMen.value] = (0, 7)
bounds[Item.FavSociety.value] = (0, 7)
bounds[Item.FavTombColonies.value] = (0, 7)
bounds[Item.FavUrchins.value] = (0, 7)

bounds[Item.ResearchOnAMorbidFad.value] = (0, 6)


# ---------------- Decks ----------------------------

london_deck = Decks.create_london_deck(
    active_player,
    replacement_epa = 6.5)

zailing_deck = Decks.create_zailing_deck(active_player)


# ---------------- Trades ----------------------------

# Plug in the basic economic contraints

per_day({
    Item.Action: actions_per_day,
    Item.CardDraws: cards_seen_per_day
})

# -----------------------------------------------------
# --- Modules
# ----------------------------------------------------


# doing some goofy inversion of control stuff here so that I can just copy paste everything

SocialActions.add_trades(trade)

Decks.add_trades(trade)

Bazaar.add_trades(trade)
RatMarket.add_trades(trade)

InventoryConversions.add_trades(active_player, trade)

london.newspaper.add_trades(active_player, trade)
london.bone_market.add_trades(active_player, trade)
london.uncategorized.add_trades(active_player, trade)
london.laboratory.add_trades(active_player, lab_rpa, trade)

unterzee.khanate.add_trades(active_player, trade)
unterzee.wakeful_eye.add_trades(active_player, trade)
unterzee.port_cecil.add_trades(active_player, trade)
unterzee.zailing.add_trades(active_player, zailing_epa, trade)

parabola.add_trades(active_player, trade)

upper_river.uncategorized.add_trades(active_player, trade)
upper_river.ealing_gardens.add_trades(active_player, trade)
upper_river.jericho.add_trades(active_player, trade)
upper_river.evenlode.add_trades(active_player, trade)
upper_river.balmoral.add_trades(active_player, trade)
upper_river.burrow.add_trades(active_player, trade)
upper_river.station_viii.add_trades(active_player, trade)
upper_river.moulin.add_trades(active_player, trade)
upper_river.hurlers.add_trades(active_player, trade)
upper_river.marigold.add_trades(active_player, trade)

fate.philosofruits.add_trades(active_player, trade)
fate.upwards.add_trades(active_player, trade)


# --------------
# Upper River Deck
# -------------

# TODO: upper river deck stuff
railway_card("Digs in the Magistracy of the Evenlode",
    Rarity.Standard,
    Location.TheMagistracyOfTheEvenlode,
    True, {
    Item.DigsInEvenlode: 1
})

trade(0, {
    Item.DigsInEvenlode: -1,
    Item.SurveyOfTheNeathsBones: -120,
    Item.PalaeontologicalDiscovery: 5
})

trade(0, {
    Item.DigsInEvenlode: -1,
    Item.SurveyOfTheNeathsBones: -140,
    Item.PalaeontologicalDiscovery: 6
})

# specific treasure only
trade(0, {
    Item.DigsInEvenlode: -1,
    Item.SurveyOfTheNeathsBones: -240,
    Item.PalaeontologicalDiscovery: 10
})

railway_card("Under the Statue - Liberation",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavRevolutionaries: -4,
    Item.NightOnTheTown: 12
})

railway_card("Under the Statue - Anchoress",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavChurch: -4,
    Item.VolumeOfCollatedResearch: 12
})

railway_card("Under the Statue - Goat Demons",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavHell: -4,
    Item.NightsoilOfTheBazaar: 60
})

railway_card("Under the Statue - Overgoat",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavHell: -4,
    Item.AeolianScream: 12
})

railway_card("Under the Statue - Ubergoat",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavHell: -4,
    Item.VolumeOfCollatedResearch: 12
})

railway_card("Under the Statue - Discordance",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.MemoryOfDiscordance: -2,
    Item.CorrespondencePlaque: 60 
})

railway_card("Grazing Goat Demons",
        Rarity.Standard,
        Location.TheHurlers,
        False, {
    # TODO might be playable? looks complicated
})

# -------------------------------
# ---- Opportunity Deck Math ----
# -------------------------------

# London Deck
# deck_size = lon
# london_deck_normalized_trade = {}

# for item in Item:
#     if london[item.value] != 0:
#         london_deck_normalized_trade[item] = (LondonCardsByItem[item.value] / deck_size)

# london_deck_normalized_trade[Item.CardDraws] = -1

# print(card_exchange)
london_good_card_density = london_deck.num_good_cards / london_deck.deck_size

trade(london_good_card_density, london_deck.normalized_trade())
trade(1, zailing_deck.normalized_trade())

# ------------------------------------------
# ---------------- Optimization ------------
# ------------------------------------------

optimize_for = Item.Echo

c = np.zeros(num_vars)
c[optimize_for.value] = -1

opt_result = linprog(c, A_ub=A.toarray(), b_ub=b, bounds=bounds, method='highs')
print(opt_result)

# print("Opp Deck")

# print(f"{'Item Name':^30}")
# # for item, quantity in zip(Item, opt_result.x):
# #     item_name = f"{item.name:30}"
# #     per_action = f"{(1.0/(quantity * actions_per_day) if quantity != 0 else 0.0):10.3f}"
# #     per_card = LondonCardsByItem[item.value] / LondonDeckSize
# #     per_day_of_draws = per_card * cards_seen_per_day
# #     print(item_name + per_action + ((f"{per_card:10.2f}" + f"{per_day_of_draws:10.2f}") if per_card != 0 else ""))


results = sorted(zip(Item, opt_result.x), key=lambda x: x[1])
for item, quantity in results:
    item_name = f"{item.name:40}"
    if quantity > 0:
        print(item_name
        + f"{1/(quantity * actions_per_day):10.5}")
    else:
        print(item_name + f"{'unsourced':10}")
    
pp = pprint.PrettyPrinter(indent=4)


print("------Assumptions-------")
print(f"Total Actions per Day:            {actions_per_day:10}")
print(f"Cards Drawn per Day:              {cards_seen_per_day:10}")
print(f"Good Card Density:                {london_good_card_density:10.3f}")

print(f"Optimize For:                     {optimize_for}")
print(f"-Player Stats-")
pp.pprint(active_player.stats)

print("------Summary-------")
print(f"{str(optimize_for) + ' Per Day:':34}{-1.0/(opt_result.fun):10.3f}")
print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.3f}")

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(A)
# pp.pprint(A[0])
# pp.pprint(A[100, 0])

# print("-----Trades NOT USED-------")
# for i in range(0, len(opt_result.slack)):
#     slack = opt_result.slack[i]
#     marginal = opt_result.ineqlin.marginals[i]
#     if (slack != 1.0 and (slack > 1.0 or  marginal == 0)):
#         trade_items = ""
#         for ii in range(0, num_items):
#             if A[i, ii] != 0:
#                 trade_items += str(Item(ii)) + ":" + str(A[i, ii]) + "; "
#         print(f"Slack: {slack:3.3} " + trade_items)


print("-----Trades In Grind-------")
for i in range(0, len(opt_result.slack)):
    slack = opt_result.slack[i]
    marginal = opt_result.ineqlin.marginals[i]
    if (slack < 1.0 and marginal != 0):
        lose_items = ""
        gain_items = ""
        for ii in range(0, num_items):
            quantity = round(A[i, ii],2)
            if int(quantity) == quantity:
                quantity = int(quantity)
            if quantity < 0:
                lose_items += str(Item(ii)) + ":" + str(quantity) + "; "
            if quantity > 0:
                gain_items += str(Item(ii)) + ":" + str(quantity) + "; "
        trade_items = lose_items + " => " + gain_items            
        trade_items = trade_items.replace("Item.","");
        # print("* " + trade_items)
        print(f"{marginal:.3}       " + trade_items)

print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.5f}")

# print(london_deck.normalized_trade())
print(zailing_deck.normalized_trade())
