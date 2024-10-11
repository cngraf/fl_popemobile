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

    ############################################################
    #                  Passenger Dining Room
    ############################################################

    culinary_values = {
        Item.VibrantPepperyFishBroth: 850,
        Item.SharkBouillabaisseWithCroutons: 850 + 1750,
        Item.CaduceanZzoupWithGunpowderAndSicklyRose: 850 + 1750,
        Item.CulinaryTributeToTheSeaOfSpines: 850 + 1900,

        Item.DarkDewedCherryLiquer: 710,
        Item.SparklingSolacefruitRoyale: 710 + 2250,
        Item.CuratorialCocktail: 710 + 2250 + 36500,
        Item.SolacefruitChampagneSorbet: 710 + 2250 + 2500,

        Item.SharplyFlavoredPickleAsYetUnpoisoned: 750,
        Item.JetBlackPickleRelishDosedWithHillchangerScorpionVenom: 750 + 500,
        Item.EnvenomedPicklesSuspendedInVenisonAspic: 750 + 350,

        Item.AnEnticingFungalPate: 900,
        Item.APlatterOfMixedCharcuterie: 900 + 7750,
        Item.ATowerOfFungalPateFlambe: 900 + 600,

        Item.SelfReflectiveTapenadeOfParabolanOrangeApple: 2750,
        Item.MarmaladeOfParabolanOrangeAppleHoneyAndRoseateAttar: 2750 + 500,
        Item.SourPickleOfParabolanOrangeAppleAndVinegar: 2750 + 500,
        Item.OrangeAppleJamSpikedWithMuscariaBrandy: 2750 + 500,
    }

    ################# Fish Broth

    add({
        Item._StationViiiAction: -1,

        Item.HandPickedPeppercaps: -5,
        Item.WitheredTentacle: -2,
        Item.FinBonesCollected: -5,

        Item.VibrantPepperyFishBroth: 1,
        # Item.CulinaryIngredientValue: 500,
        # Item._CulinaryConcoction: 1
    })

    # add({
    #     Item._StationViiiAction: -1,
    #     Item.DeepZeeCatch: -5,
    #     Item.CulinaryIngredientValue: 500
    # })

    add({
        Item._StationViiiAction: -1,
        Item.VibrantPepperyFishBroth: -1,

        Item.RemainsOfAPinewoodShark: -1,
        Item.CrateOfIncorruptibleBiscuits: -1,

        Item.SharkBouillabaisseWithCroutons: 1,
        # Item.CulinaryIngredientValue: 1750
    })

    add({
        Item._StationViiiAction: -1,
        Item.VibrantPepperyFishBroth: -1,

        Item.PerfumedGunpowder: -5,
        Item.TinOfZzoup: -1,

        Item.CaduceanZzoupWithGunpowderAndSicklyRose: 1,
        # Item.CulinaryIngredientValue: 1750
    })

    add({
        Item._StationViiiAction: -1,
        Item.VibrantPepperyFishBroth: -1,

        Item.MemoryOfDistantShores: -2,
        Item.AmberCrustedFin: -1,
        Item.WitheredTentacle: -6,

        Item.CulinaryTributeToTheSeaOfSpines: 1,
        # Item.CulinaryIngredientValue: 1900
    })

    ################ Dark-Dewed Cherry Liquer

    add({
        Item._StationViiiAction: -1,
        Item.DarkDewedCherry: -3,
        Item.BottleOfBrokenGiant1844: -1,

        Item.DarkDewedCherryLiquer: 1,
        # Item.CulinaryIngredientValue: 710,
        # Item._CulinaryConcoction: 1        
    })

    add({
        Item._StationViiiAction: -1,
        Item.DarkDewedCherryLiquer: -1,
        Item.FillipOfEffervescence: -1,
        Item.CrystallizedEuphoria: -1,
        Item.SolaceFruit: -5,

        Item.SparklingSolacefruitRoyale: 1,
        # Item.CulinaryIngredientValue: 2250,
    })

    add({
        Item._StationViiiAction: -1,
        Item.SparklingSolacefruitRoyale: -1,
        Item.ConcentrateOfSelf: -1,
        Item.MemoryOfDistantShores: -100,
        
        Item.CuratorialCocktail: 1,
        # Item.CulinaryIngredientValue: 36500
    })

    add({
        Item._StationViiiAction: -1,
        Item.SparklingSolacefruitRoyale: -1,
        Item.MemoryOfDiscordance: -1,
        # Item.SuddenInsight: -1, # TODO source these
        Item.Moonlit: -3,

        Item.SolacefruitChampagneSorbet: 1,
        # Item.CulinaryIngredientValue: 2500
    })

    ################ Pate

    add({
        Item._StationViiiAction: -1,
        Item.HandPickedPeppercaps: -5,
        Item.PotOfVenisonMarrow: -2,
        Item.PreservedSurfaceBlooms: -1,

        Item.AnEnticingFungalPate: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.AnEnticingFungalPate: -1,
        Item.SausageAboutWhichNoOneComplains: -1,
        Item.TinnedHam: -1,

        Item.APlatterOfMixedCharcuterie: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.AnEnticingFungalPate: -1,
        Item.HandPickedPeppercaps: -5,
        Item.BottleOfStranglingWillowAbsinthe: -1,

        Item.ATowerOfFungalPateFlambe: 1
    })

    # Tapenade
    add({
        Item._StationViiiAction: -1,
        Item.ParabolanOrangeApple: -2,

        Item.SelfReflectiveTapenadeOfParabolanOrangeApple: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.SelfReflectiveTapenadeOfParabolanOrangeApple: -1,
        Item.DropOfPrisonersHoney: -100,

        Item.MarmaladeOfParabolanOrangeAppleHoneyAndRoseateAttar: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.SelfReflectiveTapenadeOfParabolanOrangeApple: -1,    
        Item.JasmineLeaves: -15,
        Item.MagisterialLager: -2,

        Item.SourPickleOfParabolanOrangeAppleAndVinegar: 1
    })

    add({
        Item._StationViiiAction: -1,
        Item.SelfReflectiveTapenadeOfParabolanOrangeApple: -1,    
        Item.MuscariaBrandy: -1,

        Item.OrangeAppleJamSpikedWithMuscariaBrandy: 1
    })


    ############################################################
    #                  Kitchen cashing out
    ############################################################

    ############ Serve up dish
    add({
        Item._StationViiiAction: -1,
        Item.DeepZeeCatch: -5,
        Item.HinterlandScrip: 16,
    })

    for dish, value in culinary_values.items():
        add({
            Item._StationViiiAction: -1,
            dish: -1,

            Item.HinterlandScrip: 6 + value / 50,
        })    

    ############ Costermonger
    add({
        Item._StationViiiAction: -1,
        Item.DeepZeeCatch: -5,
        Item.SolaceFruit: 5,
        Item.DarkDewedCherry: 3.57 # TODO rounding?
    })

    for dish, value in culinary_values.items():
        add({
            Item._StationViiiAction: -1,
            dish: -1,

            Item.SolaceFruit: value / 100,
            Item.DarkDewedCherry: value / 140,
        })

    ############ Schlomo
    for dish in (
        Item.SelfReflectiveTapenadeOfParabolanOrangeApple,
        Item.SourPickleOfParabolanOrangeAppleAndVinegar,
        Item.OrangeAppleJamSpikedWithMuscariaBrandy,
        Item.MarmaladeOfParabolanOrangeAppleHoneyAndRoseateAttar,
        Item.CuratorialCocktail
    ):
        add({
            Item._StationViiiAction: -1,
            dish: -1,

            Item.AnIdentityUncovered: culinary_values.get(dish, 0) / 250,
            Item.HinterlandScrip: 5
        })

    ############ Dose yourself
    for dish in (
        Item.VibrantPepperyFishBroth,
        Item.CaduceanZzoupWithGunpowderAndSicklyRose,
        Item.SharkBouillabaisseWithCroutons,
        Item.CulinaryTributeToTheSeaOfSpines,
    ):
        value = culinary_values.get(dish, 0)
        add({
            Item._StationViiiAction: -1,
            dish: -1,

            Item.Wounds: - (4 + value/125)
        })

    add({
        Item._StationViiiAction: -1,
        Item.DeepZeeCatch: -5,
        Item.Wounds: -4,
    })

    add({
        Item._StationViiiAction: -1,
        Item.DarkDewedCherryLiquer: -1,

        Item.Nightmares: -10
    })

    add({
        Item._StationViiiAction: -1,
        Item.SparklingSolacefruitRoyale: -1,

        Item.Nightmares: -28
    })    


    ########## Masters
    add({
        Item._StationViiiAction: -1,
        Item.SparklingSolacefruitRoyale: -1,

        Item.BottelofMorelways1872: 326,
        Item.HinterlandScrip: 5
    })

    add({
        Item._StationViiiAction: -1,
        Item.SolacefruitChampagneSorbet: -1,

        Item.BottleOfStranglingWillowAbsinthe: 66,
        Item.BottelofMorelways1872: 328,
        Item.HinterlandScrip: 5
    })

    add({
        Item._StationViiiAction: -1,
        Item.CuratorialCocktail: -1,

        Item.BottleOfFourthCityAirag: 1
    })    

    add({
        Item._StationViiiAction: -1,
        Item.EnvenomedPicklesSuspendedInVenisonAspic: -1,

        Item.ExtraordinaryImplication: 5,
        Item.ScrapOfIncendiaryGossip: 5,
    })   

    add({
        Item._StationViiiAction: -1,
        Item.ATowerOfFungalPateFlambe: -1,

        Item.BazaarPermit: 1,
        Item.HinterlandScrip: 5,
    })

    # Helicon
    add({
        Item._StationViiiAction: -1,
        Item.DeepZeeCatch: -5,
        Item.HinterlandScrip: 10
    })