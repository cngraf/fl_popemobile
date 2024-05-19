from enums import *
from utils import *
from config import Config

def add_trades(active_player, config: Config):
    trade = config.trade
    player = config.player

    # each starts with same 3 actions:
    # - compel x2
    # - enter woods x1

    # --- Seven Necked Skeleton

    # fringes x1, lay trail x1, wander fringes x2, track x1, report x1
    trade(9, {
        Item.VolumeOfCollatedResearch: -8,
        Item.UnprovenancedArtefact: -4,

        Item.Moonlit: 1,
        Item.SkeletonWithSevenNecks: 1,
        Item.WingOfAYoungTerrorBird: 3,
        Item.BoneFragments: 200
    })

    # fringes x1, lay trail x2, track x1, report x1
    trade(8, {
        Item.VolumeOfCollatedResearch: -8,
        Item.UnprovenancedArtefact: -8,

        Item.Moonlit: 2,
        Item.SkeletonWithSevenNecks: 1,
        Item.WingOfAYoungTerrorBird: 3,
        Item.BoneFragments: 200
    })

    # glades x1, darken x2, return (free), fringes x1, track x1, report x1
    trade(9, {
        Item.VolumeOfCollatedResearch: -8,
        Item.ThirstyBombazineScrap: -6,

        Item.Moonlit: 2,
        Item.SkeletonWithSevenNecks: 1,
        Item.WingOfAYoungTerrorBird: 3,
        Item.BoneFragments: 200
    })    

    # --- Mammoth Ribcage

    # glades x1, darken x3, wander glades x1, track x1, report x1
    trade(10, {
        Item.VolumeOfCollatedResearch: -8,
        Item.ThirstyBombazineScrap: -9,

        Item.Moonlit: 4,
        Item.MammothRibcage: 1,
        Item.HolyRelicOfTheThighOfStFiacre: 1,
        Item.FemurOfAJurassicBeast: 2,
        Item.BoneFragments: 400
    })

    # fringes x1, lay trail x3, return (0), gladex x1, darken x2, track x1, report x1
    trade(10, {
        Item.VolumeOfCollatedResearch: -8,
        Item.ThirstyBombazineScrap: -6,
        Item.UnprovenancedArtefact: -4,

        Item.Moonlit: 3,
        Item.MammothRibcage: 1,
        Item.HolyRelicOfTheThighOfStFiacre: 1,
        Item.FemurOfAJurassicBeast: 2,
        Item.BoneFragments: 400
    })    


    # --- Doubled Skull & Thorned Ribcage

    # fringes x1, lay trail x1, wander glades x2, return, moonlight x1, track x1, report x1
    trade(10, {
        Item.VolumeOfCollatedResearch: -8,
        Item.UnprovenancedArtefact: -4,

        Item.Moonlit: -5 + 1,
        Item.DoubledSkull: 1,
        Item.ThornedRibcage: 1,
        Item.KnottedHumerus: 2
    })

    # glades x1, darken x2, return (free), moonlight x1, track x1, report x1
    trade(9, {
        Item.VolumeOfCollatedResearch: -8,
        Item.ThirstyBombazineScrap: -6,

        Item.Moonlit: -5 + 3,
        Item.DoubledSkull: 1,
        Item.ThornedRibcage: 1,
        Item.KnottedHumerus: 2
    })    

    # ------- Cabinet Noir
    # TODO: check for leftovers on various sales

    trade(1, {
        Item.CoverTiesGeneric: 1
    })

    trade(1, {
        Item.FavGreatGame: -1,

        Item.CoverTiesSurface: 1,
        Item.CoverElaboration: 1,
    })

    # Canny Cuttlefish
    trade(1, {
        Item.CrypticClue: -250,

        Item.CoverTiesSurface: 1,
        Item.CoverElaboration: 1,
        Item.CoverBackstory: 1
    })

    if (player.treasure == Treasure.PalatialHomeInTheArcticCircle):
        trade(1, {
            Item.CoverTiesSurface: 1,
            Item.CoverElaboration: 1,
            Item.CoverNuance: 1
        })

    if (player.treasure == Treasure.SocietyOfTheThreeFingeredHand):
        trade(1, {
            Item.CoverTiesSurface: 1,
            Item.CoverElaboration: 1,
            Item.CoverWitnessnes: 1
        })

    trade(1, {
        Item.FavSociety: -1,

        Item.CoverTiesBazaar: 1,
        Item.CoverElaboration: 1
    })

    # Surveiling Spindlewolf
    trade(1, {
        Item.CrypticClue: -250,

        Item.CoverTiesSurface: 1,
        Item.CoverElaboration: 1,
        Item.CoverBackstory: 1
    })

    trade(1, {
        Item.FavUrchins: -1,

        Item.CoverTiesDispossessed: 1,
        Item.CoverElaboration: 1
    })

    if (player.treasure == Treasure.TheMarvellous):
        trade(1, {
            Item.CoverTiesDispossessed: 1,
            Item.CoverElaboration: 1,
            Item.CoverWitnessnes: 1
        })

    # TODO: Increase cost for higher counts
    trade(1, {
        Item.CoverElaboration: 1
    })

    trade(1, {
        Item.CoverNuance: 1
    })

    trade(1, {
        Item.CoverWitnessnes: 1
    })

    trade(1, {
        Item.CoverCredentials: 1
    })

    trade(1, {
        Item.WellPlacedPawn: -25,
        Item.CoverBackstory: 2
    })

    trade(2, {
        Item.WellPlacedPawn: -250,
        Item.CoverBackstory: 12
    })

    trade(1, {
        Item.ViennaOpening: -5,
        Item.CoverBackstory: 6
    })

    trade(1, {
        Item.FinalBreath: -50,
        Item.CoverBackstory: 11
    })

    trade(1, {
        Item.MovesInTheGreatGame: -50,
        Item.CoverBackstory: 11
    })

    trade(1, {
        Item.UnusualLoveStory: -100,
        Item.CoverBackstory: 22
    })

    trade(1, {
        Item.MortificationOfAGreatPower: -1,
        Item.CoverBackstory: 26
    })

    # Selling Identities

    trade(1, {
        Item.CoverTiesBazaar: -1,
        Item.CoverElaboration: -10,
        Item.CoverCredentials: -4,
        Item.CoverNuance: -4,
        Item.CoverWitnessnes: -4,
        Item.CoverBackstory: -10,

        Item.RailwaySteel: 11
    })

    # # Card
    # trade(1, {
    #     Item.CoverTiesSurface: -1,
    #     Item.CoverElaboration: -4,

    #     Item.FavRevolutionaries: 2
    # })

    # # Card
    # trade(1, {
    #     Item.CoverTiesBazaar: -1,
    #     Item.CoverElaboration: -4,

    #     Item.FavUrchins: 2
    # })

    # # Card
    # trade(1, {
    #     Item.CoverTiesDispossessed: -1,
    #     Item.CoverElaboration: -4,

    #     Item.FavConstables: 2,
    #     Item.HinterlandScrip: 2.5
    # })

    # # Card
    # trade(1, {
    #     Item.CoverElaboration: -10,
    #     Item.CoverCredentials: -6,
    #     Item.CoverNuance: -6,
    #     Item.CoverWitnessnes: -6,      
    #     Item.CoverBackstory: -500

    #     # TODO: Document for deciphering
    # })

    # # Card
    # trade(1, {
    #     Item.CoverTiesSurface: -1
    #     Item.CoverElaboration: -10,
    #     Item.CoverCredentials: -6,
    #     Item.CoverNuance: -6,
    #     Item.CoverWitnessnes: -6,      
    #     Item.CoverBackstory: -500

    #     # TODO: Document for deciphering
    # })

    # Card
    trade(1, {
        Item.CoverElaboration: -10,
        Item.CoverCredentials: -5,
        Item.CoverBackstory: -100,

        Item.EdictsOfTheFirstCity: 1
    })

    trade(1, {
        Item.CoverElaboration: -10,
        Item.CoverCredentials: -4,
        Item.CoverNuance: -6,
        Item.CoverBackstory: -100,

        Item.DreadfulSurmise: 1
    })

    # Elaboration conversion
    trade(0, {
        Item.CoverElaboration: -1,
        Item.MemoryOfALesserSelf: 1
    })

    trade(0, {
        Item.CoverElaboration: -1,
        Item.ThirstyBombazineScrap: 1
    })

    trade(0, {
        Item.CoverElaboration: -1,
        Item.TouchingLoveStory: 1
    })

    trade(0, {
        Item.CoverElaboration: -1,
        Item.SwornStatement: 1
    })

    # Credenitals
    trade(0, {
        Item.CoverCredentials: -1,
        Item.MemoryOfALesserSelf: 1
    })
    
    trade(0, {
        Item.CoverCredentials: -1,
        Item.ThirstyBombazineScrap: 1
    })

    trade(0, {
        Item.CoverCredentials: -1,
        Item.TouchingLoveStory: 1
    })

    trade(0, {
        Item.CoverCredentials: -1,
        Item.SwornStatement: 1
    })

    # Nuance
    trade(0, {
        Item.CoverNuance: -1,
        Item.MemoryOfALesserSelf: 1
    })

    trade(0, {
        Item.CoverNuance: -1,
        Item.ThirstyBombazineScrap: 1
    })

    trade(0, {
        Item.CoverNuance: -1,
        Item.TouchingLoveStory: 1
    })

    trade(0, {
        Item.CoverNuance: -1,
        Item.SwornStatement: 1
    })

    # Witnesses
    trade(0, {
        Item.CoverWitnessnes: -1,
        Item.MemoryOfALesserSelf: 1
    })

    trade(0, {
        Item.CoverWitnessnes: -1,
        Item.ThirstyBombazineScrap: 1
    })

    trade(0, {
        Item.CoverWitnessnes: -1,
        Item.TouchingLoveStory: 1
    })

    trade(0, {
        Item.CoverWitnessnes: -1,
        Item.SwornStatement: 1
    })

    # Backstory
    trade(0, {
        Item.CoverBackstory: -1,
        Item.MemoryOfALesserSelf: 1
    })

    trade(0, {
        Item.CoverBackstory: -5,
        Item.MagnificentDiamond: 1
    })

    # Grand Larcenies
    # check action costs

    trade(1, {
        Item.CoverTiesBazaar: -1,
        Item.CoverElaboration: -10,
        Item.CoverCredentials: -5,
        Item.CoverNuance: -5,
        Item.CoverBackstory: -80,

        Item.ScrapOfIvoryOrganza: 1
    })

    # TODO: other cash outs