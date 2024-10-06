from enums import *
from helper.utils import *

def add_trades(config):
    trade = config.trade
    add = config.add
    
    # # TODO: upper river deck stuff
    # trade.railway_card("Digs in the Magistracy of the Evenlode",
    #     Rarity.Standard,
    #     Location.TheMagistracyOfTheEvenlode,
    #     True, {
    #     Item.DigsInEvenlode: 1
    # })

    # trade(1, {
    #     # Item.DigsInEvenlode: -1,
    #     Item.SurveyOfTheNeathsBones: -120,
    #     Item.PalaeontologicalDiscovery: 5
    # })

    # trade(1, {
    #     # Item.DigsInEvenlode: -1,
    #     Item.SurveyOfTheNeathsBones: -140,
    #     Item.PalaeontologicalDiscovery: 6
    # })

    # # specific treasure only
    # trade(1, {
    #     # Item.DigsInEvenlode: -1,
    #     Item.SurveyOfTheNeathsBones: -240,
    #     Item.PalaeontologicalDiscovery: 10
    # })