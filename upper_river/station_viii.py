from enums import *
from utils import *

def add_trades(active_player, trade):
    trade(2, {
        Item.ExtraordinaryImplication: -2,
        Item.HalcyonicTonic: 1,
        Item.FillipOfEffervescence: 1
    })

    trade(1, {
        Item.OilOfCompanionship: -1,
        Item.RumourOfTheUpperRiver: -98,

        Item.PrismaticFrame: 1
    })

    # Handwaving the UR/London transition
    trade(3, {
        Item.CrystallizedEuphoria: 1
    })

    trade(3, {
        Item.AntiqueMystery: -2,
        Item.ConsignmentOfScintillackSnuff: -2,

        Item.OilOfCompanionship: 1
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
    trade(1, {
        Item.Echo: -28,
        Item.SolaceFruit: 28,
        Item.DarkDewedCherry: 20
    })

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
