from enums import *

def conversion_rate(from_item: Item, to_item: Item) -> float:
    """
    Convert 'amount' of from_item to to_item using the conversion rates.

    Parameters:
    - from_item: the Item enum to convert from
    - to_item: the Item enum to convert to
    - amount: the amount of from_item to convert

    Returns:
    - The number of to_item you get after conversion
    """

    if from_item in item_conversion_rates and to_item in item_conversion_rates[from_item]:
        conversion_rate = item_conversion_rates[from_item][to_item]
        # return amount // conversion_rate  # Use floor division to convert
        # return amount / conversion_rate
        return conversion_rate
    
    # If no conversion is possible, return 0
    return 0

# TODO clean this up or sth
item_conversion_rates = {
    # Stacks items
    Item.LibraryKey: {Item.Echo: 0.0, Item.Stuiver: 0},
    Item.RouteTracedThroughTheLibrary: {Item.Echo: 0.0, Item.Stuiver: 0},
    Item.FragmentaryOntology: {Item.Echo: 0.0, Item.Stuiver: 0},
    Item.DispositionOfTheCardinal: {Item.Echo: 0.0, Item.Stuiver: 0},

    # Econ items
    Item.TantalisingPossibility: {Item.Echo: 0.1, Item.Stuiver: 2},
    Item.RatOnAString: {Item.Echo: 0.01, Item.Stuiver: 0},
    Item.DeepZeeCatch: {Item.Echo: 0.5, Item.Stuiver: 0},

    Item.FinBonesCollected: {Item.Echo: 0.5, Item.Stuiver: 0},
    Item.TempestuousTale: {Item.Echo: 0, Item.Stuiver: 10},
    Item.PartialMap: {Item.Echo: 2.5, Item.Stuiver: 0},
    Item.PuzzlingMap: {Item.Echo: 12.5, Item.Stuiver: 0},
    Item.FlaskOfAbominableSalts: {Item.Echo: 0.1, Item.Stuiver: 0},

    Item.CausticApocryphon: {Item.Echo: 15.5, Item.Stuiver: 250},
    Item.GlimEncrustedCarapace: {Item.Echo: 0, Item.Stuiver: 1250},
    Item.ShardOfGlim: {Item.Echo: 0.01, Item.Stuiver: 0},
    Item.RoofChart: {Item.Echo: 2.53, Item.Stuiver: 50},

    Item.Anticandle: {Item.Echo: 0, Item.Stuiver: 50},

    Item.FragmentOfTheTragedyProcedures: {Item.Echo: 62.5, Item.Stuiver: 0},
    Item.RelicOfTheFifthCity: {Item.Echo: 2.5, Item.Stuiver: 50},

    Item.OneiromanticRevelation: {Item.Echo: 62.5, Item.Stuiver: 0},
    Item.StormThrenody: {Item.Echo: 12.5, Item.Stuiver: 0},
    Item.VolumeOfCollatedResearch: {Item.Echo: 2.5, Item.Stuiver: 0},
    Item.GlimpseOfAnathema: {Item.Echo: 312.5, Item.Stuiver: 6250},

    Item.VolumeOfCollatedResearch: { 
        Item.Echo: 0.5
    },

    Item.IncisiveObservation: {
        Item.Echo: 0.5
    },

    Item.JasmineLeaves: {
        Item.Echo: 0.1,
        Item.MoonPearl: 10,
        Item.JadeFragment: 13
    },

    # # Menaces
    # # Ballpark @ 1 action to clear 6 points with social alt
    # Item.Wounds: {Item.Echo: -1, Item.Stuiver: -20, Item.Action: 1/6},
    # Item.Nightmares: {Item.Echo: -1, Item.Stuiver: -20, Item.Action: 1/6},

    # # Second Chances
    # # Ballpark @ 2/action @ 6 EPA
    # Item.SuddenInsight: { Item.Echo: 3, Item.Action: 0.5 },
    # Item.HastilyScrawledWarningNote: {Item.Echo: 3, Item.Action: 0.5},

    ################################################################################
    ###                                 Contraband                               ###
    ################################################################################
    Item.FlawedDiamond: { 
        Item.Echo: 0.12 
    },
    Item.OstentatiousDiamond: { 
        Item.Echo: 0.50 
    },
    Item.MagnificentDiamond: { 
        Item.Echo: 12.50,
        Item.Stuiver: 0.0
    },
    Item.FabulousDiamond: { 
        Item.Echo: 312.50 
    },
    Item.AscendedAmbergris: { 
        Item.Stuiver: 51
    },
    Item.LondonStreetSign: { 
        Item.Echo: 2.50 
    },
    Item.UseOfVillains: { 
        Item.Echo: 6.00 
    },
    Item.ComprehensiveBribe: { 
        Item.Echo: 12.50 
    },
    # Item.RookeryPassword: { 
    #     Item.Echo: 60.00 
    # },
    # Item.SealedCopyOfTheCrimsonBook: { 
    #     Item.TouchingLoveStory: 625 
    # }
    # Contraband
    Item.Hillmover: {
        Item._ApproximateEchoValue: 12.5
    },

    ################################################################################
    ###                                  Goods                                   ###
    ################################################################################
    Item.PieceOfRostygold: {
        Item.Echo: 0.01
    },

    Item.NightsoilOfTheBazaar: {
        Item.HinterlandScrip: 1
    },

    Item.PreservedSurfaceBlooms: {
        Item.Echo: 2.5,
        Item.HinterlandScrip: 3
    },

    Item.KnobOfScintillack: {
        Item.Echo: 2.5,
        Item.HinterlandScrip: 5
    },

    Item.PerfumedGunpowder: {
        Item._ApproximateEchoValue: 2.5 # TODO
    },

    # TODO move category, better estimate
    Item.ConsignmentOfScintillackSnuff: {
        Item._ApproximateEchoValue: 12.5
    },
    ################################################################################
    ###                        Great Game                                        ###
    ################################################################################
    
    Item.WellPlacedPawn: {
        Item._ApproximateEchoValue: 0.1
    },

    Item.FinalBreath: {
        Item.Echo: 0.5,
        Item.HinterlandScrip: 1
    },

    Item.MovesInTheGreatGame: {
        Item.Echo: 0.5,
        Item.HinterlandScrip: 1
    },

    Item.VitalIntelligence: {
        Item.Echo: 12.5,
        Item.HinterlandScrip: 25
    },

    Item.CopperCipherRing: {
        Item.Echo: 37.5
    },

    Item.ViennaOpening: {
        Item.HinterlandScrip: 5
    },

    Item.EpauletteMate: {
        Item.HinterlandScrip: 50
    },

    Item.QueenMate: {
        Item.HinterlandScrip: 50
    },

    Item.Stalemate: {
        Item.HinterlandScrip: 125
    },

    Item.MuchNeededGap: {
        Item.AssortmentOfKhaganianCoinage: 125
    },
    ################################################################################
    ###                                 Influence                               ###
    ################################################################################
    
    Item.StolenCorrespondence: { 
        Item.Echo: 0.05 
    },
    Item.IntriguingSnippet: { 
        Item.Echo: 0.20 
    },
    Item.CompromisingDocument: { 
        Item.Echo: 0.50 
    },
    Item.SecludedAddress: { 
        Item.Echo: 0.50 
    },
    Item.StolenKiss: { 
        Item.Echo: 2.50 
    },
    Item.FavourInHighPlaces: { 
        Item.Echo: 12.50 
    },
    Item.PersonalRecommendation: { 
        Item.Echo: 6.00 
    },


    # Legal
    Item.InfernalContract: {
        Item.Echo: 0.2
    },
    Item.DubiousTestimony: {
        Item.Echo: 0.5
    },
    Item.SwornStatement: {
        Item.Echo: 2.5
    },
    Item.CaveAgedCodeOfHonour: {
        Item.LegalDocument: 1,
        Item.Echo: 12.5
    },
    Item.LegalDocument: {
        Item.Echo: 12.5
    },
    Item.FragmentOfTheTragedyProcedures: {
        Item.Echo: 62.5
    },
    Item.SapOfTheCedarAtTheCrossroads: {
        Item.HinterlandScrip: 125
    },
    Item.EdictsOfTheFirstCity: {
        Item.Echo: 312.5
    }
}

def estimated_conversion_rate(from_item: Item, to_item: Item) -> float:
    if from_item in estimated_conversions and to_item in estimated_conversions[from_item]:
        conversion_rate = estimated_conversions[from_item][to_item]
        return conversion_rate

    return 0

estimated_conversions = {
    # Favours
    Item.FavBohemians: {
        Item.Echo: 5
    },
    Item.FavChurch: {
        Item.Echo: 5
    },
    Item.FavConstables: {
        Item.Echo: 5
    },
    Item.FavCriminals: {
        Item.Echo: 5
    },
    Item.FavDocks: {
        Item.Echo: 5
    },
    Item.FavGreatGame: {
        Item.Echo: 5
    },
    Item.FavHell: {
        Item.Echo: 5
    },
    Item.FavRevolutionaries: {
        Item.Echo: 5
    },
    Item.FavRubberyMen: {
        Item.Echo: 5
    },
    Item.FavSociety: {
        Item.Echo: 5
    },
    Item.FavTombColonies: {
        Item.Echo: 5
    },
    Item.FavUrchins: {
        Item.Echo: 5
    },

    Item.PerfumedGunpowder: {
        Item.Echo: 2.5
    },
}