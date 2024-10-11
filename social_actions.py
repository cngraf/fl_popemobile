from enums import *
import config

def add_trades(config: config.Config):
    add = config.add
    trade = config.trade

    add({
        Item.Action: -1,
        Item._SocialAction: 1
    })

    add({
        Item._SocialAction: -1,
        Item.VerseOfCounterCreed: -1,
        Item.Corresponding: 3
    })

    add({
        Item._SocialAction: -1,
        Item.ExtraordinaryImplication: -2,
        Item.VolumeOfCollatedResearch: -2,
        Item.Echo: -3, # 0.6 x5 for the paper
        Item.Corresponding: 3
    })

    add({
        Item._SocialAction: -1,
        Item.Corresponding: -10,
        Item.VitalIntelligence: 1,
        Item.MovesInTheGreatGame: 46
    })

    # if player_profession == Profession.CrookedCross:
    add({
        Item._SocialAction: -1,
        Item.Corresponding: -10,
        Item.SilentSoul: 1,
        Item.Soul: 1150
    })

    # requires recipient to be Licentiate
    # dang this is pretty good?
    add({
        Item._SocialAction: -1,
        Item.PieceOfRostygold: -500,
        Item.Suspicion: -6,
        Item.Scandal: -6  
    })

    # poetic 
    add({
        Item._SocialAction: -1,
        Item.Investigating: 46
    })    

    add({
        Item._SocialAction: -1,
        Item.Inspired: 46 # 0.2 *
    })

    # # if player_profession == Profession.Licentiate:
    # trade(1, {
    #     Item.PieceOfRostygold: 500,
    #     Item.MovesInTheGreatGame: 2
    # })

    # Ignnorng betrayal options w/ weekly cap

    add({
        Item._SocialAction: -1,
        Item.Wounds: -6
    })

    add({
        Item._SocialAction: -1,
        Item.Wounds: -4,
        Item.HardEarnedLesson: 1
    })

    add({
        Item._SocialAction: -1,
        Item.Scandal: -4
    })

    add({
        Item._SocialAction: -1,
        Item.Suspicion: -4
    })

    add({
        Item._SocialAction: -1,
        Item.Nightmares: -6
    })

    add({
        Item._SocialAction: -1,
        Item.Nightmares: -4,
        Item.SuddenInsight: 1
    })

    add({
        Item._SocialAction: -1,
        Item.HastilyScrawledWarningNote: 3
    })

    # house of chimes? think this works, some other stuff too
    add({
        Item._SocialAction: -1,
        Item.ConfidentSmile: 3
    })

    ###########################################
    #               Matters of the Heart
    ###########################################

    add({
        Item._SocialAction: -1,
        Item.FreeEvening: -1,

        Item.RomanticNotion: 5,
        Item.MemoryOfLight: 2,
        Item.Scandal: -3
    })

    add({
        Item._SocialAction: -1,
        Item.FreeEvening: -1,

        Item.RomanticNotion: 5,
        Item.ZeeZtory: 2,
        Item.Wounds: -3
    })

    add({
        Item._SocialAction: -1,
        Item.FreeEvening: -1,

        Item.RomanticNotion: 5,
        Item.MemoryOfDistantShores: 2,
        Item.Nightmares: -3
    })

    add({
        Item._SocialAction: -1,
        Item.FreeEvening: -1,

        Item.RomanticNotion: 5,
        Item.TaleOfTerror: 2,
        Item.Suspicion: -3
    })

    add({
        Item._SocialAction: -1,
        Item.FreeEvening: -1,

        Item.RomanticNotion: 5,
        Item.SuddenInsight: 2,
        Item.HastilyScrawledWarningNote: 2,
    })

    add({
        Item._SocialAction: -1,
        Item.FreeEvening: -1,

        Item.RomanticNotion: 5,
        Item.HardEarnedLesson: 2,
        Item.ConfidentSmile: 2,
    })    