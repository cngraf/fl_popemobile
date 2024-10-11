from enums import *
from helper.utils import *
from config import Config

def add_trades(config: Config):
    add = config.add
    # return

    for i in range(0, 7):
        visit_length = 2 ** i
        add({
            Item._UpperRiverRoundTrip: -1,
            Item.Action: -1 * visit_length,
            Item._BurrowAction: visit_length,
        })    

    add({
        Item._BurrowAction: -1,
        Item.VerseOfCounterCreed: -3,
        Item.PalimpsestScrap: -10,
        Item.ApostatesPsalm: -7,

        Item.FalseHagiotoponym: 1
    })
    
    ############################################################
    #           Museum of Souls
    ############################################################

    # TODO rare success options

    add({
        Item._BurrowAction: -1,
        Item.Soul: -800,
        Item.BrilliantSoul: -60,
        Item.InfernalContract: -50,

        Item.PortfolioOfSouls: 1
    })

    add({
        Item._BurrowAction: -1,
        Item.DiscordantSoul: -1,
        Item.SilentSoul: -5,
        Item.PortfolioOfSouls: -5,
        Item.BrilliantSoul: -125,
        Item.MuscariaBrandy: -125,
        
        Item.CoruscatingSoul: 1
    })    