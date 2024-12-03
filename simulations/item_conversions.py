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

action_echo_value = 6

# TODO clean this up or sth
item_conversion_rates = {
    Item.Echo: { Item.Echo: 1},

    # Tinned Ham laundering
    Item.HinterlandScrip: { Item.Echo: 63.5/125, Item.HinterlandScrip: 1 },
    
    # Moon Pearl laundering
    Item.Stuiver: { Item.Echo: 2.53/100, Item.Stuiver: 1 },

    ################################################################################
    ###                                 Menaces                                  ###
    ################################################################################
    # With social action from an alt
    Item.Wounds: { Item._ApproximateEchoValue: -action_echo_value/6 },
    Item.Nightmares: { Item._ApproximateEchoValue: -action_echo_value/6},
    Item.Scandal: { Item._ApproximateEchoValue: -action_echo_value/5 },
    Item.Suspicion: { Item._ApproximateEchoValue: -action_echo_value/4 },

    Item.InCorporateDebt: { Item._ApproximateEchoValue: -(12.5 + action_echo_value)/3 },

    ################################################################################
    ###                                 Connected                                ###
    ################################################################################

    # 1 Society favour + 1 action = 50 CP
    Item.ConnectedTheDuchess: { Item._ApproximateEchoValue: action_echo_value * 0.04 },


    ################################################################################
    ###                                 The Stacks                               ###
    ################################################################################

    # Stacks items
    Item.LibraryKey: {Item.Echo: 0.0, Item.Stuiver: 0},
    Item.RouteTracedThroughTheLibrary: {Item.Echo: 0.0, Item.Stuiver: 0},
    Item.FragmentaryOntology: {Item.Echo: 0.0, Item.Stuiver: 0},
    Item.DispositionOfTheCardinal: {Item.Echo: 0.0, Item.Stuiver: 0},

    # Econ items
    Item.RatOnAString: {Item.Echo: 0.01, Item.Stuiver: 0},

    Item.FinBonesCollected: {Item.Echo: 0.5, Item.Stuiver: 0},
    Item.PartialMap: {Item.Echo: 2.5, Item.Stuiver: 0},
    Item.PuzzlingMap: {Item.Echo: 12.5, Item.Stuiver: 0},
    Item.FlaskOfAbominableSalts: {Item.Echo: 0.1, Item.Stuiver: 0},

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

    Item._BannedWorksPrize: { Item.Stuiver: 2320 },
    Item._DeadStarsPrize: { Item.Stuiver: 2000, Item.Echo: 101.2 },
    Item._UnrealPlacesPrize: { Item._ApproximateEchoValue: 116 },

    # # Second Chances
    # # Ballpark @ 2/action @ 6 EPA
    # Item.SuddenInsight: { Item.Echo: 3, Item.Action: 0.5 },
    # Item.HastilyScrawledWarningNote: {Item.Echo: 3, Item.Action: 0.5},


    ################################################################################
    ###                                 Academic                                 ###
    ################################################################################
    Item.FoxfireCandleStub: { Item.Echo: 0.01 },
    Item.FlaskOfAbominableSalts: { Item.Echo: 0.10 },
    Item.MemoryOfDistantShores: { Item.Echo: 0.50 },
    Item.IncisiveObservation: { Item.Echo: 0.50 },
    Item.UnprovenancedArtefact: { Item.Echo: 2.50 },
    Item.VolumeOfCollatedResearch: { Item.Echo: 2.50 },
    Item.MirthlessCompendium: { Item.Echo: 12.50 },
    Item.BreakthroughInCurrencyDesign: { Item.Echo: 12.50 },
    Item.JudgementsEgg: { Item.Echo: 62.50 },

    Item.MemoryOfDiscordance: { Item._ApproximateEchoValue: 12.50 },

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
    ###                                  Curiosity                               ###
    ################################################################################    

    Item.VenomRuby: { Item.Echo: 0.10 },
    Item.Sapphire: { Item.Echo: 0.12 },
    Item.StrongBackedLabour: { Item.Echo: 2.5 },

    # TODO these all give 1 action 7 CP menace reduction, worth >1 action
    Item.ShrivelledBall: { Item.Echo: 0.30 },
    Item.RingOfStone: { Item.Echo: 0.30 },
    Item.DoveMaskShard: { Item.Echo: 0.30 },
    Item.FragmentOfWhiteGold: { Item.Echo: 0.30 },

    ################################################################################
    ###                               Elder                                      ###
    ################################################################################

    Item.AntiqueMystery: { Item.Echo: 12.50 },

    ################################################################################
    ###                                  Goods                                   ###
    ################################################################################

    Item.NevercoldBrassSliver: { Item.Echo: 0.01 },
    Item.PieceOfRostygold: { Item.Echo: 0.01 },
    Item.NightsoilOfTheBazaar: { Item.HinterlandScrip: 1 },

    Item.PreservedSurfaceBlooms: { Item.Echo: 2.5, Item.HinterlandScrip: 3 },

    Item.KnobOfScintillack: { Item.Echo: 2.5, Item.HinterlandScrip: 5 },

    Item.PerfumedGunpowder: {
        Item._ApproximateEchoValue: 2.5 # TODO
    },
    
    Item.RailwaySteel: {
        Item.HinterlandScrip: 19
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
    },

    ################################################################################
    ###                                 Infernal                                ###
    ################################################################################

    # Items with regular Echo values
    Item.Soul: { Item.Echo: 0.02 },
    Item.AmanitaSherry: { Item.Echo: 0.10 },
    Item.BrilliantSoul: { Item.Echo: 0.50 },
    Item.MuscariaBrandy: { Item.Echo: 2.50 },
    Item.BrassRing: { Item.Echo: 12.50 },
    Item.DevilboneDie: { Item.Echo: 0.90 },
    Item.QueerSoul: { Item.Echo: 2.50 },
    Item.SilentSoul: { Item.Echo: 12.50 },
    Item.PortfolioOfSouls: { Item.Echo: 12.50 },
    Item.BrightBrassSkull: { Item.Echo: 60.00 },
    Item.DevilishProbabilityDistributor: { Item.Echo: 62.50 },
    Item.CoruscatingSoul: { Item.Echo: 312.50 },
    Item.ReportedLocationOfAOneTimePrinceOfHell: { Item.Echo: 1560.00 },

    # Items with approximate Echo values
    Item.DiscordantSoul: { Item._ApproximateEchoValue: 50.00 },
    Item.InfernalMachine: { Item._ApproximateEchoValue: 66.00 },

    ################################################################################
    ###                               Mysteries                                  ###
    ################################################################################

    Item.WhisperedHint: { Item.Echo: 0.01 },
    Item.CrypticClue: { Item.Echo: 0.02 },
    Item.TantalisingPossibility: { Item.Echo: 0.1, Item.Stuiver: 2 },
    Item.AppallingSecret: { Item.Echo: 0.15 },
    Item.JournalOfInfamy: { Item.Echo: 0.50 },
    Item.TaleOfTerror: { Item.Echo: 0.50 },
    Item.ExtraordinaryImplication: { Item.Echo: 2.50 },
    Item.UncannyIncunabulum: { Item.Echo: 12.50 },
    Item.DirefulReflection: { Item.Echo: 12.50 },
    Item.MemoryOfAMuchStrangerSelf: { Item.Stuiver: 250 },
    Item.SearingEnigma: { Item.Echo: 62.50 },
    Item.DreadfulSurmise: { Item.Echo: 312.50 },
    Item.ImpossibleTheorem: { Item.Echo: 1562.60 },

    # Echo value from Oneiropomp conversion
    # Item.CausticApocryphon: { Item.Echo: 11.0, Item.Stuiver: 250 },
    Item.CausticApocryphon: { Item.Echo: 0.0, Item.Stuiver: 250 },
    Item.GlimpseOfAnathema: {Item.Echo: 312.5, Item.Stuiver: 6250},

    Item.MemoryOfMuchLesserSelf: { Item._ApproximateEchoValue: 2.50 },

    ################################################################################
    ###                               Nostalgia                                  ###
    ################################################################################

    Item.DropOfPrisonersHoney: { Item.Echo: 0.02 },
    Item.RomanticNotion: { Item.Echo: 0.10 },
    Item.VisionOfTheSurface: { Item.Echo: 0.50 },
    Item.TouchingLoveStory: { Item.Echo: 2.5 },
    Item.BazaarPermit: { Item.Echo: 12.50 },
    Item.EmeticRevelation: { Item.CrypticClue: 625, Item.Echo: 12.5 },
    Item.CaptivatingBallad: { Item.Echo: 62.50, Item.AssortmentOfKhaganianCoinage: 125 },

    ################################################################################
    ###                               Osteology                                  ###
    ################################################################################
    
    Item.AlbatrossWing: { Item.Echo: 12.50 },
    Item.BoneFragments: { Item.Echo: 0.01 },

    Item.FemurOfAJurassicBeast: { Item.HinterlandScrip: 2 },
    Item.FemurOfASurfaceDeer: { Item.Echo: 0.1 },
    Item.FossilisedForelimb: { Item.HinterlandScrip: 25 },
    Item.GlimEncrustedCarapace: { Item.Stuiver: 1250 },
    Item.HelicalThighbone: { Item.HinterlandScrip: 2 },
    Item.IvoryHumerus: { Item.HinterlandScrip: 25 },
    Item.UnidentifiedThighBone: { Item.HinterlandScrip: 1 },
    Item.SurveyOfTheNeathsBones: { Item.HinterlandScrip: 1 },


    ################################################################################
    ###                                 Rag Trade                                ###
    ################################################################################
    
    Item.SilkScrap: { Item.Echo: 0.01 },
    Item.SurfaceSilkScrap: { Item.Echo: 0.10 },
    Item.WhisperSatinScrap: { Item.Echo: 0.50 },
    Item.ThirstyBombazineScrap: { Item.Echo: 2.50 },
    Item.PuzzleDamaskScrap: { Item.Echo: 12.50 },
    Item.ParabolaLinenScrap: { Item.Echo: 62.50 },
    Item.ScrapOfIvoryOrganza: { Item.Echo: 312.50 },


    ################################################################################
    ###                                 Rubbery                                  ###
    ################################################################################

    Item.NoduleOfDeepAmber: { Item.Echo: 0.01 },
    Item.NoduleOfWarmAmber: { Item.Stuiver: 1 },
    Item.UnearthlyFossil: { Item.Echo: 2.5 },
    Item.NoduleOfTremblingAmber: { Item.Echo: 12.50 },
    Item.NoduleOfPulsatingAmber: { Item.Echo: 62.5 },
    Item.NoduleOfFecundAmber: { Item.Echo: 62.5 },
    Item.FlukeCore: { Item.Echo: 1560.00 },

    ################################################################################
    ###                                 Rumour                                   ###
    ################################################################################

    # Items with regular Echo values
    Item.ProscribedMaterial: { Item.Echo: 0.04 },
    Item.InklingOfIdentity: { Item.Echo: 0.10 },
    Item.ScrapOfIncendiaryGossip: { Item.Echo: 0.50 },
    Item.AnIdentityUncovered: { Item.Echo: 2.50 },
    Item.BlackmailMaterial: { Item.Echo: 12.50 },
    Item.NightOnTheTown: { Item.Echo: 2.50 },
    Item.RumourOfTheUpperRiver: { Item.Echo: 2.50 },
    Item.DiaryOfTheDead: { Item.Echo: 60.00 },
    Item.IntriguersCompendium: { Item.Echo: 312.50 },
    Item.RumourmongersNetwork: { Item.Echo: 1560.00 },

    # Items with approximate Echo values
    Item.MortificationOfAGreatPower: { Item._ApproximateEchoValue: 62.50 },

    ################################################################################
    ###                                 Sustenance                               ###
    ################################################################################

    # Items with regular Echo values

    Item.JasmineLeaves: {
        Item.Echo: 0.1,
        Item.MoonPearl: 10,
        Item.JadeFragment: 13 # Widow bulk card
    },

    Item.PotOfVenisonMarrow: { Item.Echo: 0.50, Item.HinterlandScrip: 1 },
    Item.SolaceFruit: { Item.Echo: 0.50, Item.HinterlandScrip: 1 },
    Item.DarkDewedCherry: { Item.Echo: 0.70 },
    Item.BasketOfRubberyPies: { Item.Echo: 2.50 },
    Item.CrateOfIncorruptibleBiscuits: { Item.Echo: 2.50, Item.HinterlandScrip: 5 },
    Item.HellwormMilk: { Item._ApproximateEchoValue: 62.50 },
    Item.TinOfZzoup: { Item.Echo: 2.50, Item.HinterlandScrip: 2 },
    Item.SausageAboutWhichNoOneComplains: { Item.Echo: 12.50, Item.HinterlandScrip: 5 },
    Item.TinnedHam: { Item.Echo: 63.50, Item.HinterlandScrip: 62 },
    Item.HandPickedPeppercaps: { Item.HinterlandScrip: 1 },
    Item.MagisterialLager: { Item.HinterlandScrip: 1 },

    ################################################################################
    ###                             Theological
    ################################################################################

    Item.PalimpsestScrap: { Item.Echo: 0.50 },
    Item.ApostatesPsalm: { Item.Echo: 2.50 },
    Item.VerseOfCounterCreed: { Item._ApproximateEchoValue: 12.50 },
    Item.FalseHagiotoponym: { Item.Echo: 62.50 },
    Item.LegendaCosmogone: { Item.Echo: 312.50 },

    ################################################################################
    ###                             Wild Words
    ################################################################################
    
    Item.PrimordialShriek: { Item.Echo: 0.02 },
    Item.ManiacsPrayer: { Item.Echo: 0.10 },
    Item.CorrespondencePlaque: { Item.Echo: 0.50 },
    Item.AeolianScream: { Item.Echo: 2.50 },
    Item.TempestuousTale: { Item.Stuiver: 10 },
    Item.StormThrenody: { Item.Stuiver: 12.50 },
    Item.NightWhisper: { Item.Echo: 62.5 },
    Item.StarstoneDemark: { Item.Echo: 312.5 },
    Item.BreathOfTheVoid: { Item.Echo: 15600.0 },


    ################################################################################
    ###                             Wines
    ################################################################################
    
    Item.BottleOfFourthCityAirag: { Item.Echo: 62.5,
                                   Item.AssortmentOfKhaganianCoinage: 125 },


    ################################################################################
    ###                              Zee-Treasures                               ###
    ################################################################################
    
    Item.MoonPearl: {
        Item.Echo: 0.01,
    },

    Item.DeepZeeCatch: {
        Item.Echo: 0.5,
        Item.AssortmentOfKhaganianCoinage: 1
    },

    Item.RoyalBlueFeather: {
        Item.Echo: 0.5,
        Item.HinterlandScrip: 1
    },

    Item.AmbiguousEolith: {
        Item.Echo: 0.5,
        Item.HinterlandScrip: 1
    },

    Item.CarvedBallOfStygianIvory: {
        Item.Echo: 2.5,
        Item.AssortmentOfKhaganianCoinage: 5,
        Item.HinterlandScrip: 5
    },

    Item.LiveSpecimen: {
        Item.Echo: 2.5,
    },

    Item.MemoryOfAShadowInVarchas: {
        Item.HinterlandScrip: 25,
    },

    Item.OneiricPearl: {
        Item.AssortmentOfKhaganianCoinage: 125,
    },

    # Weapons

    Item.ConsignmentOfScintillackSnuff: {
        # Manufacture in lab
        # ~22.5e in materials + 1 action = 2 units
        Item._ApproximateEchoValue: 14
    },


    # Favours
}

# 4 favours + 1 action = 30E turn in at jericho
# 3 turn ins per 2-action jericho round trip + 2 rumours
favour_eev = (2.5 * 2 + 30 * 3)/(5 * 3 + 2)
for favour in FAVOUR_ITEMS:
    item_conversion_rates[favour] = { Item._ApproximateEchoValue: favour_eev }