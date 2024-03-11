from enums import *
from utils import *

def add_trades(active_player, trade):

    # -------------
    # Khaganian Markets
    # -------------

    # selling
    trade(0, {
        Item.DeepZeeCatch: -1,
        Item.AssortmentOfKhaganianCoinage: 1
    })

    trade(0, {
        Item.CarvedBallOfStygianIvory: -1,
        Item.AssortmentOfKhaganianCoinage: 5
    })

    trade(0, {
        Item.JasmineLeaves: -1,
        Item.MoonPearl: 10
    })

    trade(0, {
        Item.BottleOfFourthCityAirag: -1,
        Item.AssortmentOfKhaganianCoinage: 125
    })

    trade(0, {
        Item.CaptivatingBallad: -1,
        Item.AssortmentOfKhaganianCoinage: 125
    })

    trade(0, {
        Item.CracklingDevice: -1,
        Item.AssortmentOfKhaganianCoinage: 125
    })

    trade(0, {
        Item.MuchNeededGap: -1,
        Item.AssortmentOfKhaganianCoinage: 125
    })

    trade(0, {
        Item.OneiricPearl: -1,
        Item.AssortmentOfKhaganianCoinage: 125
    })

    trade(0, {
        Item.SaltSteppeAtlas: -1,
        Item.AssortmentOfKhaganianCoinage: 125
    })

    # -------------
    # Mightnight Market
    # -------------

    trade(0, {
        Item.AssortmentOfKhaganianCoinage: -2,
        Item.DeepZeeCatch: 1
    })

    trade(0, {
        Item.AssortmentOfKhaganianCoinage: -10,
        Item.CarvedBallOfStygianIvory: 1
    })

    trade(0, {
        Item.TouchingLoveStory: -10,
        Item.TouchingLoveStory: 1
    })

    trade(0, {
        Item.MoonPearl: -20,
        Item.JasmineLeaves: 1
    })

    trade(0, {
        Item.MoonPearl: -20,
        Item.KhaganianLightbulb: 1
    })

    trade(0, {
        Item.AssortmentOfKhaganianCoinage: -130,
        Item.CracklingDevice: 1
    })



    # -------------
    # Intrigues
    # -------------

    # Intercept a cablegram
    trade(2, {
        Item.Infiltrating: -20,
        Item.InterceptedCablegram: 5,
        Item.VitalIntelligence: 1
    })

