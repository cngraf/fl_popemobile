from enums import *
from utils import *

def add_trades(active_player, trade):
    # -----------------
    # --- Underclay
    # ----------------

    trade(2+20+1, {
        Item.MountainSherd: 1,
    })
    # # with FATE clay arm, 19 * 33 => 627 confessions
    trade(2+19+1, {
        Item.MountainSherd: 1,
        Item.ShardOfGlim: 270
    })

    # # with SotD 13, not currently achievable, 16 * 38 => 608 confessions
    # trade(2+16+1, {
    #     Item.MountainSherd: 1,
    #     Item.ShardOfGlim: 80
    # })

    ## ------------
    ## Various London Carousels?
    ## ------------

    # overnight trip
    trade(40, {
        Item.ApostatesPsalm: 3,
        Item.NevercoldBrassSliver: ((38 * 40) - 50) * 10
    })

    # 50:51 Cross-Conversion Carousel
    trade(1, {
        Item.JournalOfInfamy: -50,
        Item.CorrespondencePlaque: 51
    })

    trade(1, {
        Item.CorrespondencePlaque: -50,
        Item.VisionOfTheSurface: 51
    })

    trade(1, {
        Item.VisionOfTheSurface: -50,
        Item.MysteryOfTheElderContinent: 51
    })

    trade(1, {
        Item.MysteryOfTheElderContinent: -50,
        Item.ScrapOfIncendiaryGossip: 51
    })

    trade(1, {
        Item.ScrapOfIncendiaryGossip: -50,
        Item.MemoryOfDistantShores: 51
    })

    trade(1, {
        Item.MemoryOfDistantShores: -50,
        Item.BrilliantSoul: 51
    })

    trade(1, {
        Item.BrilliantSoul: -50,
        Item.TaleOfTerror: 51
    })

    trade(1, {
        Item.TaleOfTerror: -50,
        Item.CompromisingDocument: 51
    })

    trade(1, {
        Item.CompromisingDocument: -50,
        Item.MemoryOfLight: 51
    })

    trade(1, {
        Item.MemoryOfLight: -50,
        Item.ZeeZtory: 51
    })

    trade(1, {
        Item.ZeeZtory: -50,
        Item.BottleOfStranglingWillowAbsinthe: 51
    })

    trade(1, {
        Item.BottleOfStranglingWillowAbsinthe: -50,
        Item.WhisperSatinScrap: 51
    })

    trade(1, {
        Item.WhisperSatinScrap: -50,
        Item.JournalOfInfamy: 51
    })

    ## ------------
    ## Department of Menace Eradication
    ## ------------

    # moonlight scales not even close to worth it

    ## ------------
    ## Shuttered Palace
    ## ------------

    # Inspired
    # ignoring rare successes

    trade(1, {
        Item.Inspired: 15
    })

    trade(1, {
        Item.FavBohemians: -1,
        Item.Inspired: 30
    })

    trade(1, {
        Item.FavSociety: -1,
        Item.Inspired: 30
    })

    trade(1, {
        Item.FavRevolutionaries: -1,
        Item.Suspicion: 1 * menace_multiplier(active_player.suspicion_reduction),
        Item.Inspired: 35,
    })

    trade(1, {
        Item.FavHell: -1,
        Item.Inspired: 25
    })

    trade(1, {
        Item.FavChurch: -1,
        Item.Inspired: 35
    })

    # need 11 Austere to 100%
    trade(1, {
        Item.JadeFragment: -10,
        Item.Austere: -3,
        Item.Inspired: 20
    })

    trade(1, {
        Item.DropOfPrisonersHoney: -25,
        Item.Inspired: 20
    })
