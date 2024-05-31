from enums import *
from utils import *

def add_trades(active_player, config):
    trade = config.trade
    add = config.add

    # -------------------
    # --- Philosofruits
    # -------------------

    # TODO: travel cost estimate
    # using wiki values
    
    trade(5, {
        Item.BlackmailMaterial: 1,
        Item.AnIdentityUncovered: 3
    })

    trade(5, {
        Item.AntiqueMystery: 1,
        Item.PresbyteratePassphrase: 3
    })

    trade(5, {
        Item.UncannyIncunabulum: 1,
        Item.ExtraordinaryImplication: 3
    })

    trade(13, {
        Item.ComprehensiveBribe: 4,
    })

    trade(10, {
        Item.CorrespondencePlaque: 90,
    })

    trade(20, {
        Item.BottleOfFourthCityAirag: 1,
        Item.CellarOfWine: 2
    })

    trade(11, {
        Item.StormThrenody: 4
    })

    # # Cards
    # # Challenges (default DC 180 or 5)
    # # If you could draw whatever you wanted

    # add({
    #     Item.RootAction: -40,
    #     Item.MangroveAction: 40
    # })

    # add({
    #     Item.MangroveAction: -1,
    #     Item.FruitfulAsceticism: 1
    # })

    # add({
    #     Item.MangroveAction: -1,
    #     Item.FruitfulCuriosity: 1
    # })

    # add({
    #     Item.MangroveAction: -1,
    #     Item.FruitfulFrivolity: 1
    # })

    # add({
    #     Item.MangroveAction: -1,
    #     Item.PhilsofruitYield: 1
    # })

    # add({
    #     Item.MangroveAction: -1,
    #     Item.FruitfulRot: 1
    # })

    # add({
    #     Item.MangroveAction: -1,
    #     Item.FruitfulCuriosity: 2
    # })

    # add({
    #     Item.MangroveAction: -1,
    #     Item.FruitfulCuriosity: 2
    # })

    # add({
    #     Item.MangroveAction: -1,
    #     Item.FruitfulCuriosity: -3,
    #     Item.PhilsofruitYield: 3
    # })

    # add({
    #     Item.MangroveAction: -1,
    #     Item.PhilsofruitYield: -8,
    #     Item.FruitfulCuriosity: -1,
    #     Item.FruitfulFrivolity: -1,

    #     Item.StormThrenody: 4
    # })