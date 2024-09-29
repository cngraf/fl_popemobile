from enums import *
from utils import *
from config import Config

def add_trades(active_player, config: Config):
    add = config.add
    trade = config.trade

    # rough estimate from zailing sim
    # about 10 actions and 3000 plunder per leg
    add({
        Item.Action: -10 * 2,
        Item.StashedTreasure: 3000 * 2,
        Item._LondonKhanateRoundTrip: 1,
        Item._AgentInTransit: 1,
        Item._UnassumingCratePickup: 3,
        Item._TriflingDiplomatSale: 1
    })

    # TODO: move this
    for visit_length in (10, 20, 40, 80, 160):
        add({
            Item._LondonKhanateRoundTrip: -1,
            Item.Action: -1 * visit_length,
            Item._KhanateAction: visit_length
        })

    add({
        Item._KhanateAction: -1,
        Item._UnassumingCratePickup: -1,
        Item.FistfulOfSurfaceCurrency: -170,
        Item.UnassumingCrate: 1
    })

    add({
        Item._KhanateAction: -1,
        Item._UnassumingCratePickup: -1,
        Item.AssortmentOfKhaganianCoinage: -10,
        Item.UnassumingCrate: 1
    })

    add({
        Item._KhanateAction: -1,
        Item._UnassumingCratePickup: -1,
        Item.FavCriminals: -1,
        Item.UnassumingCrate: 1
    })

    add({
        Item.Action: -1,
        Item.UnassumingCrate: -1,
        Item.ConnectedWidow: 2,
        Item.MagnificentDiamond: 1,
        Item.OstentatiousDiamond: 15
    })

    add({
        Item.Action: -1,
        Item.UnassumingCrate: -1,
        Item.ConnectedWidow: -2,

        Item.Wounds: 0.2,
        Item.UnidentifiedThighBone: 0.1,
        Item.HumanArm: 0.1,
        Item.ConsignmentOfScintillackSnuff: 0.1,
        Item.SilentSoul: 0.1,
        Item.FourthCityEcho: 0.1,
        Item.BazaarPermit: 0.15,
        Item.UncannyIncunabulum: 0.3,
        Item.MagnificentDiamond: 0.3,
        Item.BottleOfFourthCityAirag: 0.1
    })    

    add({
        Item._KhanateAction: -1,
        Item.CorrespondingSounder: -1,
        # Item.MirrorcatchBox: -1,
        # Item.ViolantMirrorcatchBox: 1,
        Item.NevercoldBrassSliver: 5000,
        Item.WhirringContraption: 1,
        Item.KhaganianLightbulb: 500,
        Item.CracklingDevice: 2,
        Item.FlaskOfAbominableSalts: 100
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

    add({
        Item._KhanateAction: -1,
        Item.Infiltrating: 10
    })

    # TODO: various restrictions
    add({
        Item._KhanateAction: -1,
        Item.AssortmentOfKhaganianCoinage: -10,
        Item.Infiltrating: 16
    })

    add({
        Item._KhanateAction: -1,
        Item.WellPlacedPawn: -25,
        Item.Infiltrating: 13.5
    })

    add({
        Item._KhanateAction: -1,
        Item.QueenMate: -1,
        Item.Infiltrating: 38
    })

    add({
        Item._KhanateAction: -1,
        Item.Stalemate: -1,
        Item._InfiltratingLong: 150
    })

    add({
        Item._KhanateAction: -1,
        Item.MuchNeededGap: -1,
        Item._InfiltratingLong: 150
    })

    add({
        Item._KhanateAction: -1,
        Item.AssortmentOfKhaganianCoinage: -125,
        Item._InfiltratingLong: 150
    })

    add({
        Item._KhanateAction: -1,
        Item.OneiricPearl: -1,
        Item._InfiltratingLong: 150
    })

    add({
        Item._KhanateAction: -1,
        Item.SaltSteppeAtlas: -1,
        Item._InfiltratingLong: 150
    })    

    # Intercept a cablegram
    # TODO assume these weren't buffed
    add({
        Item._KhanateAction: -2,
        Item.Infiltrating: -20,
        Item.InterceptedCablegram: 5,
        Item.VitalIntelligence: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.Infiltrating: -130,

        Item.InterceptedCablegram: 50,
        Item.VitalIntelligence: 1,
        Item.QueenMate: 0.5,
        Item.EpauletteMate: 0.5
    })

    add({
        Item._KhanateAction: -2,
        Item.Infiltrating: -20,
        Item.BlackmailMaterial: 1,
    })

    add({
        Item._KhanateAction: -2,
        Item.InterceptedCablegram: -2,
        Item.Infiltrating: -130,
        Item.OneiromanticRevelation: 1,
        Item.FavourFingerkings: 1,
        # Item.VitalIntelligence: 1
    })

    # Added fake 2nd type of infiltrating to represent that the +150 false dawn options
    # can only be used on these longer intrigues, up to twice per run
    
    add({
        Item.Infiltrating: -150,
        Item._InfiltratingLong: 150
    })

    add({
        Item._KhanateAction: -2,
        Item.InterceptedCablegram: -5,
        Item.Infiltrating: -450,
        Item._InfiltratingLong: -300,
        Item.NightWhisper: 5,
        # Item.VitalIntelligence: 1
        # another version for Gant MCB
    })

    add({
        Item._KhanateAction: -2,
        Item.InterceptedCablegram: -10,
        Item.Infiltrating: -450,
        Item._InfiltratingLong: -300,
        Item.CorrespondingSounder: 1,
        # Item.VitalIntelligence: 1
        # another version for Gant MCB
    })

    # TODO check if these got buffed with +1 intel on sep 2 patch
    add({
        Item._KhanateAction: -2,
        Item.Infiltrating: -130,
        Item._AgentInTransit: -1,

        Item.BottleOfFourthCityAirag: 1,
    })

    add({
        Item._KhanateAction: -2,
        Item.Infiltrating: -130,
        Item._AgentInTransit: -1,

        Item.FavourInHighPlaces: 1,
        Item.MagnificentDiamond: 1,
        Item.PuzzleDamaskScrap: 3,
    })

    add({
        Item._KhanateAction: -2,
        Item.Infiltrating: -130,
        Item._AgentInTransit: -1,

        Item.UncannyIncunabulum: 2,
        Item.MourningCandle: 1,
        Item.Echo: 35 # TODO Item.RedFeatheredPin: 1,
    })        

    # add({
    #     Item.Action: -0.1,
    #     Item._PullingThreads1: 1
    # })

    # 1) Agent resurfaces
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 6,

        Item._PullingThreads1: -1,
        Item._PullingThreads2: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 6,
        
        Item._PullingThreads1: -1,
        Item._PullingThreads3: 1
    })

    # 2) Zailor defects
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.SaltSteppeAtlas: 1,
        Item.VitalIntelligence: 1,

        Item._PullingThreads2: -1,
        Item._PullingThreads4: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.BottleOfFourthCityAirag: 1,
        Item.VitalIntelligence: 1,

        Item._PullingThreads2: -1,
        Item._PullingThreads8: 1
    })

    # 3) Codebook misplaced
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.ParabolaLinenScrap: 1,

        Item._PullingThreads3: -1,
        Item._PullingThreads9: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.FavourInHighPlaces: 4,
        Item.FistfulOfSurfaceCurrency: 415,

        Item._PullingThreads3: -1,
        Item._PullingThreads5: 1
    })

    # 4) Blueprints missing
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.SilentSoul: 1,
        Item.QueerSoul: 5,
        Item.BrilliantSoul: 45,
        Item.FavHell: 1,

        Item._PullingThreads4: -1,
        Item._PullingThreads11: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 4,
        Item.ExtraordinaryImplication: 5,
        Item.ViennaOpening: 5,

        Item._PullingThreads4: -1,
        Item._PullingThreads3: 1
    })    

    # 5) Mirror
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.OneiromanticRevelation: 1,

        Item._PullingThreads5: -1,
        Item._PullingThreads4: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 4,
        Item.OneiricPearl: 1,

        Item._PullingThreads5: -1,
        Item._PullingThreads7: 1
    })
   
    # 6) Device completed
    # TODO: confirm these are already up to date on wiki
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.Hillmover: 1,
        Item.PerfumedGunpowder: 5,
        Item.CorrespondencePlaque: 25,
        Item.MourningCandle: 5,

        Item._PullingThreads6: -1,
        Item._PullingThreads2: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 2,
        Item.BlackmailMaterial: 2,
        Item.AnIdentityUncovered: 4,
        Item.FavRevolutionaries: 1,

        Item._PullingThreads6: -1,
        Item._PullingThreads5: 1
    })

    # 7) Trove
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.AssortmentOfKhaganianCoinage: 125,

        Item._PullingThreads7: -1,
        Item._PullingThreads9: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.SearingEnigma: 1,

        Item._PullingThreads7: -1,
        Item._PullingThreads10: 1
    })

    # 8) Mirror
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.BazaarPermit: 5,

        Item._PullingThreads8: -1,
        Item._PullingThreads7: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.SearingEnigma: 1,

        Item._PullingThreads8: -1,
        Item._PullingThreads6: 1
    })

    # 9) Mirror
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.BottleOfFourthCityAirag: 1,

        Item._PullingThreads9: -1,
        Item._PullingThreads6: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 5,
        Item.MovesInTheGreatGame: 20,
        Item.FavSociety: 1,

        Item._PullingThreads9: -1,
        Item._PullingThreads10: 1
    })

    # 10) Master covets
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.AssortmentOfKhaganianCoinage: 125,

        Item._PullingThreads10: -1,
        Item._PullingThreads11: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.AssortmentOfKhaganianCoinage: 125,

        Item._PullingThreads10: -1,
        Item._PullingThreads1: 1
    })

    # 11) Master plots
    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.BazaarPermit: 2,
        Item.MagnificentDiamond: 3,

        Item._PullingThreads11: -1,
        Item._PullingThreads8: 1
    })

    add({
        Item._KhanateAction: -2,
        Item.EmeticRevelation: -1,
        Item.Infiltrating: -100,

        Item.VitalIntelligence: 1,
        Item.MuchNeededGap: 1,

        Item._PullingThreads11: -1,
        Item._PullingThreads1: 1
    })