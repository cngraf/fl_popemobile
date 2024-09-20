from enums import *
import config

def add_trades(config: config.Config):
    # Send Disquieting Missive
    # if player_profession == Profession.CrookedCross:
    trade = config.trade

    trade(1, {
        Item.VerseOfCounterCreed: -1,
        Item.Corresponding: 3
    })

    trade(1, {
        Item.ExtraordinaryImplication: -2,
        Item.VolumeOfCollatedResearch: -2,
        Item.Echo: -3, # 0.6 x5 for the paper
        Item.Corresponding: 3
    })

    trade(1, {
        Item.Corresponding: -10,
        Item.VitalIntelligence: 1,
        Item.MovesInTheGreatGame: 46
    })

    # if player_profession == Profession.CrookedCross:
    trade(1, {
        Item.Corresponding: -10,
        Item.SilentSoul: 1,
        Item.Soul: 1150
    })

    # requires recipient to be Licentiate
    # dang this is pretty good?
    trade(1, {
        Item.PieceOfRostygold: -500,
        Item.Suspicion: -6,
        Item.Scandal: -6  
    })

    # poetic 
    trade(1, {
        Item.Investigating: 46
    })    

    trade(1, {
        Item.Inspired: 46 # 0.2 *
    })

    # # if player_profession == Profession.Licentiate:
    # trade(1, {
    #     Item.PieceOfRostygold: 500,
    #     Item.MovesInTheGreatGame: 2
    # })

    # Ignnorng betrayal options w/ weekly cap

    trade(1, {
        Item.Wounds: -6
    })

    trade(1, {
        Item.Wounds: -4,
        Item.HardEarnedLesson: 1
    })

    trade(1, {
        Item.Scandal: -4
    })

    trade(1, {
        Item.Suspicion: -4
    })

    trade(1, {
        Item.Nightmares: -6
    })

    trade(1, {
        Item.Nightmares: -4,
        Item.SuddenInsight: 1
    })

    trade(1, {
        Item.HastilyScrawledWarningNote: 3
    })

    # house of chimes? think this works, some other stuff too
    trade(1, {
        Item.ConfidentSmile: 3
    })


