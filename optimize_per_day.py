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

#  ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ██╗     
# ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗██║     
# ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║██║     
# ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║██║     
# ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║███████╗
#  ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝


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

fate.philosofruits.add_trades(active_player, trade)
fate.upwards.add_trades(active_player, trade)


#  █████╗  █████╗ ██╗██╗     ██╗    ██╗ █████╗ ██╗   ██╗
# ██╔══██╗██╔══██╗██║██║     ██║    ██║██╔══██╗╚██╗ ██╔╝
# ██████╔╝███████║██║██║     ██║ █╗ ██║███████║ ╚████╔╝ 
# ██╔══██╗██╔══██║██║██║     ██║███╗██║██╔══██║  ╚██╔╝  
# ██║  ██║██║  ██║██║███████╗╚███╔███╔╝██║  ██║   ██║   
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   


# -----------------------------------
# ---- Jericho
# -----------------------------------

# --------- Canal Cruising

if active_player.profession == Profession.CrookedCross:
    trade(1, {
        Item.UnprovenancedArtefact: -4,
        Item.EsteemOfTheGuild: 1
    })

trade(1, {
    Item.VolumeOfCollatedResearch: -10,
    Item.EsteemOfTheGuild: 2
})

trade(1, {
    Item.PartialMap: -6,
    Item.AnIdentityUncovered: -4,
    Item.EsteemOfTheGuild: 2
})

trade(1, {
    Item.MemoryOfDistantShores: -40,
    Item.SwornStatement: -2,
    Item.EsteemOfTheGuild: 2
})

trade(1, {
    Item.NightOnTheTown: -1,
    Item.ScrapOfIncendiaryGossip: -45,
    Item.EsteemOfTheGuild: 2
})

trade(1, {
    Item.FavDocks: -5,
    Item.EsteemOfTheGuild: 2
})

# assume ranges are evenly distributed
trade(2, {
    Item.EsteemOfTheGuild: -3,
    Item.VitalIntelligence: 2.5,
    Item.ViennaOpening: 6.5
})

trade(2, {
    Item.EsteemOfTheGuild: -3,
    Item.MirrorcatchBox: 1
})

trade(2, {
    Item.EsteemOfTheGuild: -3,
    Item.MoonlightScales: 50,
    Item.FinBonesCollected: 5,
    Item.SkullInCoral: 1.5,
    Item.UnprovenancedArtefact: 8.5
})

# upper river destinations

trade(2, {
    Item.EsteemOfTheGuild: -6,
    Item.BrightBrassSkull: 1,
    Item.ExtraordinaryImplication: 5.5,
    Item.VerseOfCounterCreed: 2.5
})

trade(2, {
    Item.EsteemOfTheGuild: -6,
    Item.MovesInTheGreatGame: 18.5,
    Item.PrimaevalHint: 1,
    Item.UncannyIncunabulum: 2.5
})

trade(2, {
    Item.EsteemOfTheGuild: -6,
    Item.NightWhisper: 1,
    Item.TaleOfTerror: 3.5,
    Item.FinalBreath: 12,
    Item.HumanRibcage: 2
})


# --------- Calling in Favours
# hack to model dipping into jericho to trade favours
# when you would otherwise not go there

jericho_add = 0.0
def jericho_trade(exchange):
    exchange[Item.RumourOfTheUpperRiver] = jericho_add
    trade(1 + jericho_add, exchange)

jericho_trade({
    Item.FavBohemians: -4,
    Item.HolyRelicOfTheThighOfStFiacre: 2,
    Item.WingOfAYoungTerrorBird: 1,
})

jericho_trade({
    Item.FavChurch: -4,
    Item.RattyReliquary: 2,
    Item.ApostatesPsalm: 1,
})

jericho_trade({
    Item.FavConstables: -4,
    Item.CaveAgedCodeOfHonour: 2,
    Item.SwornStatement: 1
})

jericho_trade({
    Item.FavCriminals: -4,
    Item.HumanRibcage: 2,
    Item.HumanArm: 1
})

jericho_trade({
    Item.FavDocks: -4,
    Item.UncannyIncunabulum: 2,
    Item.KnobOfScintillack: 1
})

jericho_trade({
    Item.FavGreatGame: -4,
    Item.ViennaOpening: 1,
    Item.QueenMate: 1
})

jericho_trade({
    Item.FavHell: -4,
    Item.ThornedRibcage: 2,
    Item.QueerSoul: 1
})

jericho_trade({
    Item.FavRevolutionaries: -4,
    Item.UnlawfulDevice: 2,
    Item.ThirstyBombazineScrap: 1
})

jericho_trade({
    Item.FavRubberyMen: -4,
    Item.FlourishingRibcage: 2,
    Item.BasketOfRubberyPies: 1,
})

jericho_trade({
    Item.FavSociety: -4,
    Item.FavourInHighPlaces: 2,
    Item.NightOnTheTown: 1
})

jericho_trade({
    Item.FavTombColonies: -4,
    Item.AntiqueMystery: 2,
    Item.UnprovenancedArtefact: 1,
})

jericho_trade({
    Item.FavUrchins: -4,
    Item.StormThrenody: 2,
    Item.AeolianScream: 1
})

# --------------
# Evenlode
# -------------


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


# --------------
# Balmoral
# -------------

# 2x (1 action, 4 research) to enter
# 1 action to go to glade
# 3x (1 action, 3 bombazine) to darken
# 1 action wander
# 1 action locate red deer
# 1 action cash out with keeper

# TODO: double check action counts for these
# Mammoth Ribcage
trade(9, {
    Item.VolumeOfCollatedResearch: -8,
    Item.ThirstyBombazineScrap: -9,

    Item.MammothRibcage: 1,
    Item.HolyRelicOfTheThighOfStFiacre: 1,
    Item.FemurOfAJurassicBeast: 2,
    Item.BoneFragments: 400
})

# Skeleton with 7 Necks
trade(7, {
    Item.VolumeOfCollatedResearch: -8,
    Item.UnprovenancedArtefact: -4,

    Item.SkeletonWithSevenNecks: 1,
    Item.WingOfAYoungTerrorBird: 3,
    Item.BoneFragments: 200
})

# --------------
# Station VIII
# -------------

trade(2, {
    Item.ExtraordinaryImplication: -2,
    Item.HalcyonicTonic: 1,
    Item.FillipOfEffervescence: 1
})

trade(1, {
    Item.OilOfCompanionship: -1,
    Item.RumourOfTheUpperRiver: -98,

    Item.PrismaticFrame: 1
})

# Handwaving the UR/London transition
trade(3, {
    Item.CrystallizedEuphoria: 1
})

trade(3, {
    Item.AntiqueMystery: -2,
    Item.ConsignmentOfScintillackSnuff: -2,

    Item.OilOfCompanionship: 1
})

# Mr Wines
trade(1, {
    Item.SolacefruitChampagneSorbet: -1,

    Item.BottleOfStranglingWillowAbsinthe: 66,
    Item.BottelofMorelways1872: 328,
    Item.HinterlandScrip: 5
})

# Fish broth
trade(1, {
    Item.HandPickedPeppercaps: -5,
    Item.WitheredTentacle: -2,
    Item.FinBonesCollected: -5,

    Item.VibrantPepperyFishBroth: 1
})

trade(1, {
    Item.VibrantPepperyFishBroth: -1,
    Item.RemainsOfAPinewoodShark: -1,
    Item.CrateOfIncorruptibleBiscuits: -1,

    Item.SharkBouillabaisseWithCroutons: 1
})

trade(1, {
    Item.VibrantPepperyFishBroth: -1,
    Item.PerfumedGunpowder: -1,
    Item.TinOfZzoup: -1,

    Item.CaduceanZzoupWithGunpowderAndSicklyRose: 1
})

trade(1, {
    Item.MemoryOfDistantShores: -2,
    Item.AmberCrustedFin: -1,
    Item.WitheredTentacle: -6,

    Item.CulinaryTributeToTheSeaOfSpines: 1
})

# Liqueur

# placeholder for costermonger
trade(1, {
    Item.Echo: -28,
    Item.SolaceFruit: 28,
    Item.DarkDewedCherry: 20
})

trade(1, {
    Item.Echo: -12.5,
    Item.MemoryOfDiscordance: 1
})

trade(1, {
    Item.DarkDewedCherry: -3,
    Item.BottleOfBrokenGiant1844: -1,

    Item.DarkDewedCherryLiquer: 1
})

trade(1, {
    Item.DarkDewedCherryLiquer: -1,
    Item.FillipOfEffervescence: -1,
    Item.CrystallizedEuphoria: -1,
    Item.SolaceFruit: -5,

    Item.SparklingSolacefruitRoyale: 1
})

trade(1, {
    Item.SparklingSolacefruitRoyale: -1,
    Item.ConcentrateOfSelf: -1,
    Item.MemoryOfDistantShores: -100,
    
    Item.CuratorialCocktail: 1
})

trade(1, {
    Item.SparklingSolacefruitRoyale: -1,
    Item.MemoryOfDiscordance: -1,
    # Item.SuddenInsight: -1,
    # Item.Moonlit: -3,

    Item.SolacefruitChampagneSorbet: 1
})

# Pate
trade(1, {
    Item.HandPickedPeppercaps: -5,
    Item.PotOfVenisonMarrow: -2,
    Item.PreservedSurfaceBlooms: -1,

    Item.AnEnticingFungalPate: 1
})

trade(1, {
    Item.AnEnticingFungalPate: -1,
    Item.SausageAboutWhichNoOneComplains: -1,
    Item.TinnedHam: -1,

    Item.APlatterOfMixedCharcuterie: 1
})

trade(1, {
    Item.AnEnticingFungalPate: -1,
    Item.HandPickedPeppercaps: -1,
    Item.BottleOfStranglingWillowAbsinthe: -1,

    Item.ATowerOfFungalPateFlambe: 1
})

# Tapenade
trade(1, {
    Item.ParabolanOrangeApple: -2,

    Item.SelfReflectiveTapenadeOfParabolanOrangeApple: 1
})

trade(1, {
    Item.SelfReflectiveTapenadeOfParabolanOrangeApple: -1,
    Item.DropOfPrisonersHoney: -1,

    Item.MarmaladeOfParabolanOrangeAppleHoneyAndRoseateAttar: 1
})

trade(1, {
    Item.SelfReflectiveTapenadeOfParabolanOrangeApple: -1,    
    Item.JasmineLeaves: -15,
    Item.MagisterialLager: -2,

    Item.SourPickleOfParabolanOrangeAppleAndVinegar: 1
})

trade(1, {
    Item.SelfReflectiveTapenadeOfParabolanOrangeApple: -1,    
    Item.MuscariaBrandy: -1,

    Item.OrangeAppleJamSpikedWithMuscariaBrandy: 1
})


# ----------------
# --- The Hurlers
# ----------------


# Licensed by Mr Stones

trade(1, {
    Item.FlawedDiamond: -100,
    Item.HinterlandScrip: 30
})

trade(1, {
    Item.OstentatiousDiamond: -25,
    Item.CrateOfIncorruptibleBiscuits: 6
})

trade(1, {
    Item.MagnificentDiamond: -1,
    Item.TouchingLoveStory: 5.5 # assumes uniform 5 or 6
})

trade(1, {
    Item.FabulousDiamond: -1,
    Item.HinterlandScrip: 625,
    Item.StolenKiss: 2
})

# Statues
# TODO enable only one at a time

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


# trade(5, {
#     Item.NightOnTheTown: 12
# })


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

# per_day(card_exchange)

# trade(20.42, {
#     Item.Echo: -1.05,
#     Item.Wounds: 0.84,
#     Item.Scandal: 3.43,
#     Item.Suspicion: 0.84,
#     Item.FavBohemians: 3.78,
#     Item.FavChurch: 2.52,
#     Item.FavCriminals: 2.5,
#     Item.FavDocks: 0.84,
#     Item.FavGreatGame: 1.78,
#     Item.FavRevolutionaries: 2.08,
#     Item.FavSociety: 3.36,
#     Item.FavTombColonies: 0.84,
#     Item.FavUrchins: 0.84,
#     Item.CertifiableScrap: 0.84,
#     Item.PieceOfRostygold: 1260.50,
#     Item.CompromisingDocument: -0.84,
#     Item.CrypticClue: 193.28,
#     Item.TaleOfTerror: -0.84,
#     Item.VisionOfTheSurface: -0.84,
#     Item.JetBlackStinger: 4.20,
#     Item.ScrapOfIncendiaryGossip: 11.76,
#     Item.RumourOfTheUpperRiver: -4.20,
#     Item.AeolianScream: 0.04
# })

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
