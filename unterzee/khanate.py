from enums import *
from utils import *

def add_trades(active_player, config):
    trade = config.trade

    # TODO: move this

    trade(1, {
        Item.CorrespondingSounder: -1,
        # Item.MirrorcatchBox: -1,
        # Item.ViolantMirrorcatchBox: 1,
        Item.NevercoldBrassSliver: 5000,
        Item.WhirringContraption: 1,
        Item.KhaganianLightbulb: 500,
        Item.CracklingDevice: 2,
        Item.FlaskOfAbominableSalts: 100
    })

    # TODO: cap per trip
    trade(1, {
        Item.FistfulOfSurfaceCurrency: -170,
        Item.UnassumingCrate: 1
    })

    trade(1, {
        Item.AssortmentOfKhaganianCoinage: -10,
        Item.UnassumingCrate: 1
    })

    trade(1, {
        Item.FavCriminals: -1,
        Item.UnassumingCrate: 1
    })

    # trade(1, {
    #     Item.UnassumingCrate: -1,
    #     Item.MagnificentDiamond: 1,
    #     Item.OstentatiousDiamond: 15
    # })

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
        Item.AssortmentOfKhaganianCoinage: -10,
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

    trade(0, {
        Item.Action: -1,
        Item.Infiltrating: 10
    })

    # TODO: various restrictions
    trade(0, {
        Item.Action: -1,
        Item.AssortmentOfKhaganianCoinage: -10,
        Item.Infiltrating: 16
    })

    trade(0, {
        Item.Action: -1,
        Item.WellPlacedPawn: -25,
        Item.Infiltrating: 13.5
    })

    trade(0, {
        Item.Action: -1,
        Item.QueenMate: -1,
        Item.Infiltrating: 38
    })

    trade(0, {
        Item.Action: -1,
        Item.Stalemate: -1,
        Item.Infiltrating: 150
    })

    trade(0, {
        Item.Action: -1,
        Item.MuchNeededGap: -1,
        Item.Infiltrating: 150
    })

    trade(0, {
        Item.Action: -1,
        Item.AssortmentOfKhaganianCoinage: -125,
        Item.Infiltrating: 150
    })

    trade(0, {
        Item.Action: -1,
        Item.OneiricPearl: -1,
        Item.Infiltrating: 150
    })

    trade(0, {
        Item.Action: -1,
        Item.SaltSteppeAtlas: -1,
        Item.Infiltrating: 150
    })    

    # Intercept a cablegram
    trade(2, {
        Item.Infiltrating: -20,
        Item.InterceptedCablegram: 5,
        Item.VitalIntelligence: 1
    })

    trade(2, {
        Item.Infiltrating: -130,

        Item.InterceptedCablegram: 50,
        Item.VitalIntelligence: 1,
        Item.QueenMate: 0.5,
        Item.EpauletteMate: 0.5
    })

    trade(2, {
        Item.Infiltrating: -20,
        Item.BlackmailMaterial: 1
    })

    trade(2, {
        Item.InterceptedCablegram: -2,
        Item.Infiltrating: -130,
        Item.OneiromanticRevelation: 1,
        Item.FavourFingerkings: 1
    })

    trade(2, {
        Item.InterceptedCablegram: -5,
        Item.Infiltrating: -750,
        Item.NightWhisper: 5
        # another version for Gant MCB
    })

    trade(2, {
        Item.InterceptedCablegram: -10,
        Item.Infiltrating: -750,
        Item.CorrespondingSounder: 1
        # another version for Gant MCB
    })

    # TODO: cycle of availability
    # An Opportunity + airs

    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.VitalIntelligence: 5
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.SaltSteppeAtlas: 1
    })    


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.BottleOfFourthCityAirag: 1
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.ParabolaLinenScrap: 1
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.FavourInHighPlaces: 4,
        Item.FistfulOfSurfaceCurrency: 415
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.SilentSoul: 2,
        Item.QueerSoul: 5,
        Item.BrilliantSoul: 45,
        Item.FavHell: 1
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.VitalIntelligence: 3,
        Item.ExtraordinaryImplication: 5,
        Item.ViennaOpening: 5
    })    
    

    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.OneiromanticRevelation: 1
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.OneiricPearl: 1
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.VitalIntelligence: 1,
        Item.Hillmover: 5,
        Item.PerfumedGunpowder: 5,
        Item.CorrespondencePlaque: 25,
        Item.MourningCandle: 5
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.VitalIntelligence: 2,
        Item.BlackmailMaterial: 2,
        Item.AnIdentityUncovered: 4,
        Item.FavRevolutionaries: 1
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.AssortmentOfKhaganianCoinage: 125
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.SearingEnigma: 1
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.BazaarPermit: 5
    })

    # trade(2, {
    #     Item.Infiltrating: -100,
    #     Item.SearingEnigma: 1
    # })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.BottleOfFourthCityAirag: 1
    })


    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.VitalIntelligence: 4,
        Item.MovesInTheGreatGame: 20,
        Item.FavSociety: 1
    })    

    # trade(2, {
    #     Item.Infiltrating: -100,
    #     Item.AssortmentOfKhaganianCoinage: 125
    # })

    # trade(2, {
    #     Item.Infiltrating: -100,
    #     Item.AssortmentOfKhaganianCoinage: 125
    # })

    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.BazaarPermit: 2,
        Item.MagnificentDiamond: 3
    })

 
    trade(2, {
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,
        Item.MuchNeededGap: 1
    })    