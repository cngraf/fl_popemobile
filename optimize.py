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

import social_actions as SocialActions
import bazaar as Bazaar
import inventory_conversions as InventoryConversions
import rat_market as RatMarket

import professional_activities

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

import fate.philosofruits
import fate.upwards
import fate.whiskerways

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
- most parabolan hunts
- waswood shores?
    - figure out the odds
- basically everything else

Zailing
- BETTER model of the deck, current one is a little too dumb
    - worse estimate for shorter trips
    - need to incorporate benefit of choosing from multiple good cards
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

crackpot idea
- normalize all trades to 1 echo where possible?
- get a better idea of weights/marginals
- prob make it much more difficult to read
- maybe go halfway and do this for the buy/sell actions and that's it
'''

# class Config:
#     def __init__(self):
#         self.actions_per_day = 120.0
#         self.cards_seen_per_day = 40

# Important Parameters
# actions doesn't matter on its own until I add some weekly+ stuff
# but it does matter relative to cards seen per day

# core_constraint = {
#     Item.Constraint: 1,
#     Item.Action: 1,
#     # Item.CardDraws: 0.25,

#     # bone inventory
#     # Item.BoneFragments: 51_000,
#     # Item.FinBonesCollected: 43,
#     # Item.JetBlackStinger: 68,
#     # Item.SurveyOfTheNeathsBones: 210,
#     # Item.UnidentifiedThighbone: 53,
#     # Item.WitheredTentacle: 62,
#     # Item.FemurOfAJurassicBeast: 6,
#     # Item.HeadlessSkeleton: 14,
#     # Item.HumanArm: 14,
#     # Item.KnottedHumerus: 13,
#     # Item.PlasterTailBones: 19,
#     # Item.WingOfAYoungTerrorBird: 21,
#     # Item.FlourishingRibcage: 12,
#     # Item.FossilisedForelimb: 1,
#     # Item.HolyRelicOfTheThighOfStFiacre: 29,
#     # Item.HumanRibcage: 22,
#     # Item.SkullInCoral: 4,
#     # Item.SabreToothedSkull: 1,
#     # Item.SkeletonWithSevenNecks: 4,
#     # Item.LeviathanFrame: 1
#     # Item.Echo: 1
# }

# actions_per_day = 120.0
# cards_seen_per_day = 0

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

player_generic = Player(stats = {
    Stat.Watchful: Player.baseline_watchful,
    Stat.Shadowy: Player.baseline_shadowy,
    Stat.Dangerous: Player.baseline_dangerous,
    Stat.Persuasive: Player.baseline_persuasive
})

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

active_player = player_bal_licentiate

# hack
var_buffer = 5_000
num_items = max(Item, key=lambda x: x.value).value
num_vars = num_items + 1 + var_buffer

config = Config(num_vars, active_player)

# Toggles
config.enable_all_rat_market_moons = True


trade = config.trade


# ---------------- Decks ----------------------------

# london_deck = Decks.create_london_deck(active_player, 6.5, config)
london_deck = decks.london_deck.create_deck_old(config)

# should just have one deck for each region and dummy "card draws in X" item for each one
zailing_deck = Decks.create_zailing_deck(active_player, Location.TheSaltSteppes)

# ---------------- Trades ----------------------------

# Plug in the basic economic contraints


# ------------------------------
# ----- Bone Market Hack -------
# ------------------------------

# Having written this code, it occurs to me it might make more sense to do it in reverse
# Like, keep the constraint just as "action" but add a trade to trade 18 actions
# for one of each of the subtypes. Well, whatever. this is fine

bone_market_week_actions = {
    "Antiquity": {
        "Reptile": Item.AntiquityReptileAction,
        "Amphibian": Item.AntiquityAmphibianAction,
        "Bird": Item.AntiquityBirdAction,
        "Fish": Item.AntiquityFishAction,
        "Arachnid": Item.AntiquityArachnidAction,
        "Insect": Item.AntiquityInsectAction,
    },
    "Amalgamy": {
        "Reptile": Item.AmalgamyReptileAction,
        "Amphibian": Item.AmalgamyAmphibianAction,
        "Bird": Item.AmalgamyBirdAction,
        "Fish": Item.AmalgamyFishAction,
        "Arachnid": Item.AmalgamyArachnidAction,
        "Insect": Item.AmalgamyInsectAction,
    },
    "Menace": {
        "Reptile": Item.MenaceReptileAction,
        "Amphibian": Item.MenaceAmphibianAction,
        "Bird": Item.MenaceBirdAction,
        "Fish": Item.MenaceFishAction,
        "Arachnid": Item.MenaceArachnidAction,
        "Insect": Item.MenaceInsectAction,
    }
}

bone_market_cycle_length = 18

core_constraint = {
    Item.Constraint: 1
}

for category, actions in bone_market_week_actions.items():
    for creature, action in actions.items():
        core_constraint[action] = 1

        config.add({
            action: -1,
            Item.Action: 1
        })

        if (category == "Amalgamy"):
            config.add({
                action: -1,
                Item.AmalgamyGeneralAction: 1
            })

        if (category == "Antiquity"):
            config.add({
                action: -1,
                Item.AntiquityGeneralAction: 1
            })

        if (category == "Menace"):
            config.add({
                action: -1,
                Item.MenaceGeneralAction: 1
            })

        if (creature == "Amphibian"):
            config.add({
                action: -1,
                Item.GeneralAmphibianAction: 1
            })

        if (creature == "Arachnid"):
            config.add({
                action: -1,
                Item.GeneralArachnidAction: 1
            })

        if (creature == "Bird"):
            config.add({
                action: -1,
                Item.GeneralBirdAction: 1
            })

        if (creature == "Fish"):
            config.add({
                action: -1,
                Item.GeneralFishAction: 1
            })

        if (creature == "Insect"):
            config.add({
                action: -1,
                Item.GeneralInsectAction: 1
            })

        if (creature == "Reptile"):
            config.add({
                action: -1,
                Item.GeneralReptileAction: 1
            })

config.add(core_constraint)

# -----------------------------------------------------
# --- Modules
# ----------------------------------------------------

# doing some goofy inversion of control stuff here so that I can just copy paste everything

SocialActions.add_trades(config)
Bazaar.add_trades(config)
# RatMarket.add_trades(config)

professional_activities.add_trades(active_player, config)

InventoryConversions.add_trades(active_player, config)

decks.london_deck.add_trades(config)

london.uncategorized.add_trades(active_player, config)
london.newspaper.add_trades(active_player, config)
london.laboratory.add_trades(active_player, lab_rpa, config)
london.hearts_game.add_trades(active_player, config)
london.arbor.add_trades(config)

london.bone_market.add_trades(active_player, config)

unterzee.khanate.add_trades(active_player, config)
unterzee.wakeful_eye.add_trades(active_player, config)
unterzee.port_cecil.add_trades(active_player, config)
unterzee.zailing.add_trades(active_player, zailing_epa, config)

parabola.add_trades(active_player, config)

upper_river.upper_river_exchange.add_trades(config)
upper_river.uncategorized.add_trades(active_player, config)
upper_river.ealing_gardens.add_trades(active_player, config)
upper_river.jericho.add_trades(active_player, config)
upper_river.evenlode.add_trades(active_player, config)
upper_river.balmoral.add_trades(active_player, config)
upper_river.burrow.add_trades(active_player, config)
upper_river.station_viii.add_trades(active_player, config)
upper_river.moulin.add_trades(active_player, config)
upper_river.hurlers.add_trades(active_player, config)
upper_river.marigold.add_trades(active_player, config)
upper_river.tracklayers_city.add_trades(config)

firmament.hallows_throat.add_trades(config)

# fate.philosofruits.add_trades(active_player, config)
# fate.upwards.add_trades(active_player, config)
# fate.whiskerways.add_trades(config)


# --------------
# Upper River Deck
# -------------

# TODO: upper river deck stuff
config.railway_card("Digs in the Magistracy of the Evenlode",
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

config.railway_card("Under the Statue - Liberation",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavRevolutionaries: -4,
    Item.NightOnTheTown: 12
})

config.railway_card("Under the Statue - Anchoress",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavChurch: -4,
    Item.VolumeOfCollatedResearch: 12
})

config.railway_card("Under the Statue - Goat Demons",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavHell: -4,
    Item.NightsoilOfTheBazaar: 60
})

config.railway_card("Under the Statue - Overgoat",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavHell: -4,
    Item.AeolianScream: 12
})

config.railway_card("Under the Statue - Ubergoat",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.FavHell: -4,
    Item.VolumeOfCollatedResearch: 12
})

config.railway_card("Under the Statue - Discordance",
        Rarity.Standard,
        Location.TheHurlers,
        True, {
    Item.MemoryOfDiscordance: -2,
    Item.CorrespondencePlaque: 60 
})

config.railway_card("Grazing Goat Demons",
        Rarity.Standard,
        Location.TheHurlers,
        False, {
    # TODO might be playable? looks complicated
})

# -------------------------------
# ---- Opportunity Deck Math ----
# -------------------------------

# print("")
# print("Starting Nadir simulation....")
# print("")
# nadir_average = decks.nadir.simulate_full(config, 10000)

# config.trade(0, nadir_average)

# # hack
# config.trade(1, {
#     Item.DiscordantSoul: -1,
#     Item.Echo: 62.5
# })

# London Deck
# deck_size = lon
# london_deck_normalized_trade = {}

# for item in Item:
#     if london[item.value] != 0:
#         london_deck_normalized_trade[item] = (LondonCardsByItem[item.value] / deck_size)

# london_deck_normalized_trade[Item.CardDraws] = -1

# print(card_exchange)
london_good_card_density = london_deck.num_good_cards / london_deck.deck_size

# trade(london_good_card_density, london_deck.normalized_trade())
# print(london_good_card_density)
# print(london_deck.normalized_trade())

trade(1, zailing_deck.normalized_trade())

# trade(1, {
#     Item.Echo: 100
# })


'''
I might be an idiot?
Instead of manually calibrating the cards as good or bad and running sims,
just give each one a value of Item.CardDraw inverse of its rarity, add as a trade,
and let the math do the rest.
'''
run_london_sim = False
london_sim_file_location = "simulated/london_deck.pkl"
if run_london_sim:
    with open(london_sim_file_location, "wb") as file:
        runs = 1000
        draws_per_run = 200
        print(f"Simulating London deck {runs} times with {draws_per_run} draws per run...")
        london_sim_result = decks.london_deck.monte_carlo(config, runs, draws_per_run)
        print(london_sim_result)

        trade(0, london_sim_result)
        pickle.dump(london_sim_result, file)
        print("London Deck result saved to " + london_sim_file_location)
else:
    print("Loading London deck sim from " + london_sim_file_location)
    with open(london_sim_file_location, "rb") as file:
        london_sim_result = pickle.load(file)
        print(london_sim_result)
        trade(0, london_sim_result)


# with open(london_sim_file_location, )



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
print(f"Good Card Density:                {london_good_card_density:10.3f}")

print(f"Optimize For:                     {optimize_for}")
print(f"-Player Stats-")
pp.pprint(active_player.stats)

print("------Summary-------")
print(f"{str(optimize_for) + ' Per Day:':34}{-1.0/(opt_result.fun):10.3f}")
# print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.3f}")

trades_used = []
# actions_per_cycle = core_constraint[Item.Action]
actions_per_cycle = bone_market_cycle_length

print("-----Trades In Grind-------")
for i in range(0, len(opt_result.slack)):
    slack = opt_result.slack[i]
    marginal = opt_result.ineqlin.marginals[i]
    if (slack < 1.0 and marginal != 0):
        lose_items = ""
        gain_items = ""
        for ii in range(0, num_items):
            quantity = round(config.A[i, ii],2)
            if int(quantity) == quantity:
                quantity = int(quantity)
            if quantity < 0:
                lose_items += str(Item(ii)) + ":" + str(quantity) + "; "
            if quantity > 0:
                gain_items += str(Item(ii)) + ":" + str(quantity) + "; "
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

for i in trades_used:
    print(f"{i[0]:.3}       " + i[1])

    
# print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.5f}")
print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_cycle):10.5f}")

# print(london_deck.normalized_trade())
# print(zailing_deck.normalized_trade())
