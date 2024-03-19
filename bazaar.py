from enums import *
from config import *

def buy_sell(config: Config, item: Item, buy: float, sell: float):
    config.trade(0, {
        Item.Echo: buy,
        item: 1
    })

    config.trade(0, {
        item: -1,
        Item.Echo: sell 
    })

def add_trades(config: Config):
    trade = config.trade

    trade(0, {
        Item.Echo: -64.80,
        Item.WinsomeDispossessedOrphan: 1
    })

    # Academic
    buy_sell(config, Item.FoxfireCandleStub, -0.03, 0.01)
    buy_sell(config, Item.FlaskOfAbominableSalts, -0.2, 0.1)

    trade(0, { Item.MemoryOfDistantShores: -1, Item.Echo: 0.5 })
    trade(0, { Item.MemoryOfDistantShores: -1, Item.Echo: 0.5 })
    trade(0, { Item.IncisiveObservation: -1, Item.Echo: 0.5 })
    trade(0, { Item.UnprovenancedArtefact: -1, Item.Echo: 2.5 })
    trade(0, { Item.VolumeOfCollatedResearch: -1, Item.Echo: 2.5 })
    trade(0, { Item.MirthlessCompendium: -1, Item.Echo: 12.5 })
    trade(0, { Item.JudgementsEgg: -1, Item.Echo: 12.5 })
    trade(0, { Item.SecretCollege: -1, Item.SearingEnigma: 25 })

    # Cartography ------
    buy_sell(config, Item.ShardOfGlim, -0.03, 0.01)

    trade(0, { Item.MapScrap: -1, Item.Echo: 0.1 })
    trade(0, { Item.ZeeZtory: -1, Item.Echo: 0.5 })
    trade(0, { Item.PartialMap: -1, Item.Echo: 2.5 })
    trade(0, { Item.PuzzlingMap: -1, Item.Echo: 12.5 })
    trade(0, { Item.SaltSteppeAtlas: -1, Item.Echo: 62.5 })
    trade(0, { Item.RelativelySafeZeeLane: -1, Item.Echo: 62.5 })

    trade(0, { Item.SightingOfAParabolanLandmark: -1, Item.Echo: 0.1 })
    trade(0, { Item.VitreousAlmanac: -1, Item.Echo: 12.5 })
    trade(0, { Item.OneiromanticRevelation: -1, Item.Echo: 62.5 })
    trade(0, { Item.ParabolanParable: -1, Item.Echo: 312.5 })
    trade(0, { Item.CartographersHoard: -1, Item.Echo: 312.5 })
    trade(0, { Item.WaswoodAlmanac: -1, Item.Echo: 312.5 })

    # Currency ------
    trade(0, {
        Item.FirstCityCoin: -1,
        Item.Echo: 0.25
    })

    trade(0, {
        Item.FistfulOfSurfaceCurrency: -1,
        Item.Echo: 0.03
    })

    trade(0, {
        Item.HinterlandScrip: -1,
        Item.Echo: 0.5
    })

    # Elder ---------
    trade(0, {
        Item.RelicOfTheThirdCity: -1,
        Item.Echo: 0.1
    })

    trade(0, {
        Item.MysteryOfTheElderContinent: -1,
        Item.Echo: 0.5
    })

    trade(0, {
        Item.PresbyteratePassphrase: -1,
        Item.Echo: 2.5
    })

    trade(0, {
        Item.AntiqueMystery: -1,
        Item.Echo: 12.5
    })

    # Goods ----------

    trade(0, {
        Item.NevercoldBrassSliver: -1,
        Item.Echo: 0.01
    })

    trade(0, {
        Item.PieceOfRostygold: -1,
        Item.Echo: 0.01
    })

    trade(0, {
        Item.PreservedSurfaceBlooms: -1,
        Item.Echo: 2.5
    })

    trade(0, {
        Item.KnobOfScintillack: -1,
        Item.Echo: 2.5
    })

    # ----- Great Game
    trade(0, {
        Item.FinalBreath: -1,
        Item.HinterlandScrip: 1
    })

    trade(0, {
        Item.ViennaOpening: -1,
        Item.HinterlandScrip: 5
    })

    trade(0, {
        Item.QueenMate: -1,
        Item.HinterlandScrip: 50
    })


    # Historical -----

    trade(0, {
        Item.RelicOfTheFourthCity: -1,
        Item.Echo: 0.05
    })

    trade(0, {
        Item.RustedStirrup: -1,
        Item.Echo: 0.10
    })

    trade(0, {
        Item.SilveredCatsClaw: -1,
        Item.Echo: 0.10
    })

    trade(0, {
        Item.TraceOfViric: -1,
        Item.Echo: 0.5
    })

    trade(0, {
        Item.RelicOfTheSecondCity: -1,
        Item.Echo: 0.15
    })

    trade(0, {
        Item.NicatoreanRelic: -1,
        Item.Echo: 2.5
    })

    trade(0, {
        Item.UnlawfulDevice: -1,
        Item.Echo: 12.5
    })

    trade(0, {
        Item.UnlawfulDevice: -1,
        Item.HinterlandScrip: 25
    })

    # Infernal
    trade(0, {
        Item.QueerSoul: -1,
        Item.Echo: 2.5
    })

    # Influence
    buy_sell(config, Item.StolenCorrespondence, -0.10, 0.05)

    trade(0, { Item.IntriguingSnippet: -1,      Item.Echo: 0.2 })
    trade(0, { Item.CompromisingDocument: -1,   Item.Echo: 0.5 })
    trade(0, { Item.SecludedAddress: -1,        Item.Echo: 0.5 })
    trade(0, { Item.StolenKiss: -1,             Item.Echo: 2.5 })
    trade(0, { Item.FavourInHighPlaces: -1,     Item.Echo: 12.5 })
    trade(0, { Item.PersonalRecommendation: -1, Item.Echo: 6 })
    
    # Legal
    trade(0, {
        Item.CaveAgedCodeOfHonour: -1,
        Item.LegalDocument: 1,
    })

    trade(0, {
        Item.LegalDocument: -1,
        Item.Echo: 12.5
    })

    # Luminosity ---------
    buy_sell(config, Item.LumpOfLamplighterBeeswax, -0.02, 0.01)

    trade(0, { Item.PhosphorescentScarab: -1, Item.Echo: 0.1})
    trade(0, { Item.MemoryOfLight: -1, Item.CrypticClue: 25})
    trade(0, { Item.MourningCandle: -1, Item.Echo: 2.5})

    trade(0, { Item.TailfeatherBrilliantAsFlame: -1, Item.Echo: 2.5 })
    trade(0, { Item.EyelessSkull: -1, Item.Echo: 30 })
    trade(0, { Item.ElementOfDawn: -1, Item.Echo: 62.5 })
    trade(0, { Item.MountainSherd: -1, Item.Echo: 62.5 })
    trade(0, { Item.RayDrenchedCinder: -1, Item.Echo: 312.5 })


    # Mysteries ---------

    buy_sell(config, Item.WhisperedHint, -0.02, 0.01)

    trade(0, { Item.CrypticClue: -1,            Item.Echo: 0.02 })
    trade(0, { Item.AppallingSecret: -1,        Item.Echo: 0.15 })
    trade(0, { Item.JournalOfInfamy: -1,        Item.Echo: 0.5 })
    trade(0, { Item.TaleOfTerror: -1,           Item.Echo: 0.5 })
    trade(0, { Item.ExtraordinaryImplication: -1, Item.Echo: 2.5 })
    trade(0, { Item.UncannyIncunabulum: -1,     Item.Echo: 12.5 })
    trade(0, { Item.DirefulReflection: -1,      Item.Echo: 12.5 })
    trade(0, { Item.SearingEnigma: -1,          Item.Echo: 62.5 })
    trade(0, { Item.DreadfulSurmise: -1,        Item.Echo: 312.5 })
    trade(0, { Item.ImpossibleTheorem: -1,      Item.Echo: 1562.60 })

    # Nostalgia
    buy_sell(config, Item.DropOfPrisonersHoney, -0.04, 0.02)

    trade(0, { Item.RomanticNotion: -1,         Item.Echo: 0.10 })
    trade(0, { Item.VisionOfTheSurface: -1,     Item.Echo: 0.50 })
    trade(0, { Item.TouchingLoveStory: -1,      Item.Echo: 2.5 })
    trade(0, { Item.BazaarPermit: -1,           Item.Echo: 12.5 })
    trade(0, { Item.EmeticRevelation: -1, Item.CrypticClue: 625 })
    trade(0, { Item.CaptivatingBallad: -1,      Item.Echo: 62.5 })

    # Osteology

    # worth ~3.05 echoes with horsebitrage
    trade(0, {
        Item.CarvedBallOfStygianIvory: -1,
        Item.Echo: 2.5
    })

    # Rag Trade
    trade(0, {
        Item.ThirstyBombazineScrap: -1,
        Item.RatShilling: 2.5
    })

    # Ratness
    trade(1, {
        Item.RattyReliquary: -5,
        Item.RatShilling: 850
    })

    # --- Rubbery
    buy_sell(config, Item.NoduleOfDeepAmber, -0.03, 0.01)

    trade(0, { Item.UnearthlyFossil: -1,            Item.Echo: 2.5 })
    trade(0, { Item.NoduleOfTremblingAmber: -1,     Item.Echo: 12.5 })
    trade(0, { Item.NoduleOfPulsatingAmber: -1,     Item.Echo: 62.5 })
    trade(0, { Item.NoduleOfFecundAmber: -1,        Item.Echo: 312.5 })
    trade(0, { Item.FlukeCore: -1,                  Item.Echo: 1560 })




    # Rumour ---------------------
    trade(0, {
        Item.ProscibedMaterial: -1,
        Item.Echo: 0.04
    })

    trade(0, {
        Item.InklingOfIdentity: -1,
        Item.Echo: 0.10
    })

    trade(0, {
        Item.ScrapOfIncendiaryGossip: -1,
        Item.Echo: 0.5
    })

    trade(0, {
        Item.AnIdentityUncovered: -1,
        Item.Echo: 2.5
    })

    trade(0, {
        Item.BlackmailMaterial: -1,
        Item.Echo: 12.5
    }) 

    trade(0, {
        Item.RumourOfTheUpperRiver: -1,
        Item.Echo: 2.5
    })

    trade(0, {
        Item.NightOnTheTown: -1,
        Item.Echo: 2.5
    })

    # Sustenance ----------------
    trade(0, {
        Item.JasmineLeaves: -1,
        Item.Echo: 0.1
    })

    trade(0, {
        Item.BasketOfRubberyPies: -1,
        Item.Echo: 2.5
    })

    trade(0, {
        Item.HinterlandScrip: -125,
        Item.TinnedHam: 1
    })

    trade(0, {
        Item.TinnedHam: -1,
        Item.Echo: 63.5
    })

    # Theological
    trade(0, {
        Item.ApostatesPsalm: -1,
        Item.Echo: 2.5
    })

    # Wild Words ----------

    trade(0, {
        Item.AeolianScream: -1,
        Item.Echo: 2.5
    })

    trade(0, {
        Item.StormThrenody: -1,
        Item.Echo: 12.50
    })

    trade(0, {
        Item.NightWhisper: -1,
        Item.Echo: 62.5
    })

    # Wines
    trade(0, {
        Item.BottleOfGreyfields1879: 1,
        Item.Echo: -0.02
    })

    trade(0, {
        Item.BottleOfGreyfields1879: -1,
        Item.Echo: 0.01
    })

    trade(0, {
        Item.Echo: -0.04,
        Item.BottleOfGreyfields1882: 1
    })

    trade(0, {
        Item.BottleOfGreyfields1882: -1,
        Item.Echo: 0.02
    })

    trade(0, {
        Item.BottelofMorelways1872: -1,
        Item.Echo: 0.1
    })

    trade(0, {
        Item.BottleOfStranglingWillowAbsinthe: -1,
        Item.Echo: -0.5
    })

    # Equipment


    buy_sell(config, Item.SulkyBat, -0.4, 0.2)

    buy_sell(config, Item.LuckyWeasel, -0.4, 0.2)