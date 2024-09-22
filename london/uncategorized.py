from enums import *
from utils import *

from config import *
from player import *

def add_trades(_, config: Config):
    trade = config.trade
    player = config.player

    scandal_multi = player.scandal_reduction

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
        Item.Suspicion: 1 * menace_multiplier(config.player.suspicion_reduction),
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


    ## ----------------
    ## --- Unsorted ---
    ## ----------------

    # --- Railway Board Meeting Dividend
    
    # Add Entrepreneur and vote him off
    # TODO: confirm action cost
    config.add({
        Item.Action: -7,
        Item.InCorporateDebt: -15,
        Item.HinterlandScrip: 10
    })

    # TODO: check that this works
    # does TLC spur count as a station?

    # start at 0 debt & 4 members
    # vote dividend twice
    config.add({
        Item.Action: -1 * (6 + 6 + 1),

        Item.MoonPearl: 2 * (2000 + 9 * 250 + 6 * 50),
        Item.MagnificentDiamond: 4,
        Item.BottleOfBrokenGiant1844: 4,
        Item.InCorporateDebt: 5 + 7,
        Item.DelayUntilTheNextBoardMeeting: 1
    })


    # --- Starved cultural exchange ---
    config.uniform_random_trade(
        input={
            Item.Action: -1,
            Item.ExtraordinaryImplication: -1,
            Item.RecentParticipantInAStarvedCulturalExchange: 1
        },
        outputs=({
            Item.AeolianScream: 6,
            Item.Scandal: player.scandal_ev(1)
        },
        {
            Item.EmeticRevelation: 1,
            Item.VenomRuby: 50,
            Item.Scandal: player.scandal_ev(2)
        },
        {
            Item.HumanRibcage: 1,
            Item.HeadlessSkeleton: 5,
            Item.Scandal: player.scandal_ev(3)
        },
        {
            Item.StolenKiss: 8,
            Item.Scandal: player.scandal_ev(4)
        },
        {
            Item.NoduleOfDeepAmber: 2000,
            Item.Scandal: player.scandal_ev(5)
        },
        {
            Item.NoduleOfTremblingAmber: 2,
            Item.Scandal: player.scandal_ev(6)
        })
    )


    config.uniform_random_trade(
        input={
            Item.Action: -1,
            Item.BottleOfGreyfields1882: -375,
            Item.RecentParticipantInAStarvedCulturalExchange: 1
        },
        outputs=({
            Item.AeolianScream: 6,
        },
        {
            Item.EmeticRevelation: 1,
            Item.VenomRuby: 50,
        },
        {
            Item.HumanRibcage: 1,
            Item.HeadlessSkeleton: 5,
        },
        {
            Item.StolenKiss: 8,
        },
        {
            Item.NoduleOfDeepAmber: 2000,
        },
        {
            Item.NoduleOfTremblingAmber: 2,
            Item.Scandal: player.scandal_ev(2)
        })
    )

    config.uniform_random_trade(
        input={
            Item.Action: -1,
            Item.PuzzleDamaskScrap: -1,
            Item.RecentParticipantInAStarvedCulturalExchange: 1
        },
        outputs=({
            Item.AeolianScream: 6,
        },
        {
            Item.EmeticRevelation: 1,
            Item.VenomRuby: 50,
        },
        {
            Item.HumanRibcage: 1,
            Item.HeadlessSkeleton: 5,
        },
        {
            Item.StolenKiss: 8,
        },
        {
            Item.NoduleOfDeepAmber: 2000,
        },
        {
            Item.NoduleOfTremblingAmber: 2,
        })
    )    

    