from enums import *
from helper.utils import *

def add_trades(config):
    add = config.add
    trade = config.trade

    for i in range(0, 7):
        visit_length = 2 ** i
        add({
            Item._UpperRiverRoundTrip: -1,
            Item.Action: -1 * visit_length,
            Item._StationViiiAction: visit_length,

            # Item._UnveilYourPaintingLondon: 1
        })


    ################################################
    #               Collecting Reagents
    ################################################
    add({
        Item._StationViiiAction: -1,
        Item.CollectionNotePackageInLondon: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.CollectionNotePackageInLondon: -1,
        Item.SwornStatement: -3,

        Item.ObliviscereMori: 1
    })

    # Collect from Pinnock & return
    add({
        Item._StationViiiAction: -1,
        Item.Action: -2,
 
        Item.RumourOfTheUpperRiver: 2,
        Item.ObliviscereMori: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.Action: -2,
        Item.AntiqueMystery: -2,
        Item.ConsignmentOfScintillackSnuff: -2,
    
        Item.RumourOfTheUpperRiver: 2,
        Item.ElationAtFelineOration: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.Action: -2,
        Item.DirefulReflection: -2,
        Item.ComprehensiveBribe: -2,
    
        Item.RumourOfTheUpperRiver: 2,
        Item.VindicationOfFaith: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.Action: -2,
        Item.BazaarPermit: -6,
        Item.BlackmailMaterial: -6,
        Item.ComprehensiveBribe: -6,
        Item.LegalDocument: -6,
        Item.ParabolanOrangeApple: -1,
    
        Item.RumourOfTheUpperRiver: 2,
        Item.ExhilarationFromAchievingJustice: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.Action: -2,
        Item.TouchingLoveStory: -10,
        Item.FavourInHighPlaces: -2,
        Item.SearingEnigma: -2,
        Item.NoduleOfPulsatingAmber: -2,
    
        Item.RumourOfTheUpperRiver: 2,
        Item.HorrifyingConfirmationThatYouWereRightAllAlong: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.Action: -2,
        Item.BlackmailMaterial: -22,
        Item.DiaryOfTheDead: -5,
        Item.DreadfulSurmise: -1,
        Item.TinOfZzoup: -10,
        Item.TinnedHam: -10,
    
        Item.RumourOfTheUpperRiver: 2,
        Item.UnthinkableHope: 1
    })

    ################################################
    #               Extracting Sentiment
    ################################################

    for reagent, sentiment in (
        (Item.ObliviscereMori, Item.CrystallizedEuphoria),
        (Item.ElationAtFelineOration, Item.OilOfCompanionship),
        (Item.VindicationOfFaith, Item.SalveOfRighteousness),
        (Item.HorrifyingConfirmationThatYouWereRightAllAlong, Item.ConcentrateOfSelf),
        (Item.UnthinkableHope, Item.PowderOfRenewal),
    ):
        add({
            Item._StationViiiAction: -1,
            reagent: -1,
            sentiment: 1
        })


    # Mark a Crate
    add({
        Item._StationViiiAction: -3,
        Item.ExtraordinaryImplication: -1,
        Item.HalcyonicTonic: 0.5,
        Item.FillipOfEffervescence: 0.5
    })

    # Card
    # TODO move this
    trade(1, {
        Item.OilOfCompanionship: -1,
        Item.RumourOfTheUpperRiver: -98,

        Item.PrismaticFrame: 1
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
    # trade(1, {
    #     Item.Echo: -28,
    #     Item.SolaceFruit: 28,
    #     Item.DarkDewedCherry: 20
    # })

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
