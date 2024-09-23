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
    add = config.add

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

    # Contraband
    trade(0, { Item.FlawedDiamond: -1, Item.Echo: 0.12 })
    trade(0, { Item.OstentatiousDiamond: -1, Item.Echo: 0.5 })
    trade(0, { Item.MagnificentDiamond: -1, Item.Echo: 12.50 })
    trade(0, { Item.FabulousDiamond: -1, Item.Echo: 312.12 })

    buy_sell(config, Item.LondonStreetSign, -5, 2.5)

    trade(0, { Item.UseOfVillains: -1, Item.Echo: 6 })
    trade(0, { Item.ComprehensiveBribe: -1, Item.Echo: 12.5 })

    # Curiosity
    trade(0, { Item.VenomRuby: -1, Item.Echo: 0.1 })
    trade(0, { Item.Sapphire: -1, Item.Echo: 0.12 })

    # Currency ------
    buy_sell(config, Item.FistfulOfSurfaceCurrency, -0.06, 0.03)
    trade(0, { Item.FirstCityCoin: -1, Item.Echo: 0.25 })

    # Elder ---------
    buy_sell(config, Item.JadeFragment, -0.02, 0.01)
    buy_sell(config, Item.RelicOfTheThirdCity, -0.2, 0.1)
    trade(0, { Item.MysteryOfTheElderContinent: -1, Item.Echo: 0.5 })
    trade(0, { Item.PresbyteratePassphrase: -1, Item.Echo: 2.5 })
    trade(0, { Item.AntiqueMystery: -1, Item.Echo: 12.5 })
    trade(0, { Item.PrimaevalHint: -1, Item.Echo: 62.5 })
    trade(0, { Item.ElementalSecret: -1, Item.Echo: 312.5 })


    # Goods ----------

    buy_sell(config, Item.NevercoldBrassSliver, -0.03, 0.01)
    buy_sell(config, Item.PieceOfRostygold, -0.03, 0.01)
    trade(0, { Item.PreservedSurfaceBlooms: -1, Item.Echo: 2.5 })
    trade(0, { Item.KnobOfScintillack: -1, Item.Echo: 2.5 })

    # ----- Great Game

    trade(0, { Item.FinalBreath: -1, Item.Echo: 0.5 })
    trade(0, { Item.MovesInTheGreatGame: -1, Item.Echo: 0.5 })
    trade(0, { Item.VitalIntelligence: -1, Item.Echo: 12.5 })

    # Historical -----

    buy_sell(config, Item.RelicOfTheFourthCity, -0.1, 0.05)
    trade(0, { Item.RustedStirrup: -1, Item.Echo: 0.1 })
    trade(0, { Item.SilveredCatsClaw: -1, Item.Echo: 0.1 })
    trade(0, { Item.RelicOfTheSecondCity: -1, Item.Echo: 0.15 })
    trade(0, { Item.TraceOfViric: -1, Item.Echo: 0.5 })
    trade(0, { Item.NicatoreanRelic: -1, Item.Echo: 2.5 })
    trade(0, { Item.UnlawfulDevice: -1, Item.Echo: 12.5 })
    trade(0, { Item.ChimericalArchive: -1, Item.Echo: 62.5 })
    trade(0, { Item.RelicOfTheFifthCity: -1, Item.Echo: 2.5 })


    # Infernal
    buy_sell(config, Item.Soul, -0.04, 0.02)
    trade(0, { Item.AmanitaSherry: -1, Item.Echo: 0.1 })
    trade(0, { Item.BrilliantSoul: -1, Item.Echo: 0.5 })
    trade(0, { Item.MuscariaBrandy: -1, Item.Echo: 2.5 })
    trade(0, { Item.BrassRing: -1, Item.Echo: 12.5 })
    trade(0, { Item.DevilboneDice: -1, Item.Echo: 0.9 })
    trade(0, { Item.QueerSoul: -1, Item.Echo: 2.5 })
    trade(0, { Item.SilentSoul: -1, Item.Echo: 12.5 })
    trade(0, { Item.PortfolioOfSouls: -1, Item.Echo: 12.5 })
    buy_sell(config, Item.BrightBrassSkull, -62.5, 60)
    trade(0, { Item.CoruscatingSoul: -1, Item.Echo: 312.5 })
    trade(0, { Item.ReportedLocationOfAOneTimePrinceOfHell: -1, Item.Echo: 1560 })

    # Influence
    buy_sell(config, Item.StolenCorrespondence, -0.10, 0.05)

    trade(0, { Item.IntriguingSnippet: -1,      Item.Echo: 0.2 })
    trade(0, { Item.CompromisingDocument: -1,   Item.Echo: 0.5 })
    trade(0, { Item.SecludedAddress: -1,        Item.Echo: 0.5 })
    trade(0, { Item.StolenKiss: -1,             Item.Echo: 2.5 })
    trade(0, { Item.FavourInHighPlaces: -1,     Item.Echo: 12.5 })
    trade(0, { Item.PersonalRecommendation: -1, Item.Echo: 6 })
    
    # Legal
    buy_sell(config, Item.InfernalContract, -0.4, 0.2)
    trade(0, { Item.DubiousTestimony: -1, Item.Echo: 0.5 })
    trade(0, { Item.SwornStatement: -1, Item.Echo: 2.5 })
    trade(0, { Item.CaveAgedCodeOfHonour: -1, Item.LegalDocument: 1 })
    trade(0, { Item.LegalDocument: -1, Item.LegalDocument: 12.5 })
    trade(0, { Item.FragmentOfTheTragedyProcedures: -1, Item.LegalDocument: 62.5 })
    trade(0, { Item.EdictsOfTheFirstCity: -1, Item.LegalDocument: 312.5 })

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
    trade(0, { Item.BoneFragments: -1, Item.Echo: 0.01 })
    trade(0, { Item.FemurOfASurfaceDeer: -1, Item.Echo: 0.1 })
    trade(0, { Item.AlbatrossWing: -1, Item.Echo: 12.50 })

    # Rag Trade
    buy_sell(config, Item.SilkScrap, -0.02, 0.01)
    trade(0, { Item.SurfaceSilkScrap: -1, Item.Echo: 0.1 })
    trade(0, { Item.WhisperSatinScrap: -1, Item.Echo: 0.5 })
    trade(0, { Item.ThirstyBombazineScrap: -1, Item.Echo: 2.5 })
    trade(0, { Item.PuzzleDamaskScrap: -1, Item.Echo: 12.5 })
    trade(0, { Item.ParabolaLinenScrap: -1, Item.Echo: 62.5 })
    trade(0, { Item.ScrapOfIvoryOrganza: -1, Item.Echo: 312.5 })
    trade(0, { Item.VeilsVelvetScrap: -1, Item.Echo: 1560 })

    # Ratness
    buy_sell(config, Item.RatOnAString, -0.02, 0.01)
    trade(0, { Item.VengeRatCorpse: -1, Item.Echo: 0.5 })
    trade(0, { Item.BaptisedRattusFaberCorpse: -1, Item.Echo: 2.5 })
    trade(0, { Item.RattyReliquary: -1, Item.Echo: 1 })

    # --- Rubbery
    buy_sell(config, Item.NoduleOfDeepAmber, -0.03, 0.01)

    trade(0, { Item.UnearthlyFossil: -1,            Item.Echo: 2.5 })
    trade(0, { Item.NoduleOfTremblingAmber: -1,     Item.Echo: 12.5 })
    trade(0, { Item.NoduleOfPulsatingAmber: -1,     Item.Echo: 62.5 })
    trade(0, { Item.NoduleOfFecundAmber: -1,        Item.Echo: 312.5 })
    trade(0, { Item.FlukeCore: -1,                  Item.Echo: 1560 })


    # Rumour ---------------------
    buy_sell(config, Item.ProscribedMaterial, -0.08, 0.04)
    trade(0, { Item.InklingOfIdentity: -1, Item.Echo: 0.1 })
    trade(0, { Item.ScrapOfIncendiaryGossip: -1, Item.Echo: 0.5 })
    trade(0, { Item.AnIdentityUncovered: -1, Item.Echo: 2.5 })
    trade(0, { Item.BlackmailMaterial: -1, Item.Echo: 12.5 })
    trade(0, { Item.NightOnTheTown: -1, Item.Echo: 2.5 })
    trade(0, { Item.RumourOfTheUpperRiver: -1, Item.Echo: 2.5 })
    trade(0, { Item.IntriguersCompendium: -1, Item.Echo: 312.50 })

    # Sustenance ----------------
    trade(0, { Item.JasmineLeaves: -1, Item.Echo: 0.1 })
    trade(0, { Item.PotOfVenisonMarrow: -1, Item.Echo: 0.5 })
    trade(0, { Item.SolaceFruit: -1, Item.Echo: 0.5 })
    trade(0, { Item.DarkDewedCherry: -1, Item.Echo: 0.7 })
    trade(0, { Item.BasketOfRubberyPies: -1, Item.Echo: 2.5 })
    trade(0, { Item.CrateOfIncorruptibleBiscuits: -1, Item.Echo: 2.5 })
    trade(0, { Item.TinOfZzoup: -1, Item.Echo: 2.5 })
    trade(0, { Item.SausageAboutWhichNoOneComplains: -1, Item.Echo: 12.5 })
    trade(0, { Item.TinnedHam: -1, Item.Echo: 63.5 })

    # Theological
    trade(0, { Item.PalimpsestScrap: -1, Item.Echo: 0.5 })
    trade(0, { Item.ApostatesPsalm: -1, Item.Echo: 2.5 })
    trade(0, { Item.FalseHagiotoponym: -1, Item.Echo: 62.5 })
    # trade(0, { Item.LegendaCosmogone: -1, Item.Echo: 312.5 })

    # Wild Words ----------
    buy_sell(config, Item.PrimordialShriek, -0.04, 0.02)
    trade(0, { Item.ManiacsPrayer: -1, Item.Echo: 0.1 })
    trade(0, { Item.CorrespondencePlaque: -1, Item.Echo: 0.5 })
    trade(0, { Item.AeolianScream: -1, Item.Echo: 2.5 })
    trade(0, { Item.StormThrenody: -1, Item.Echo: 12.5 })
    trade(0, { Item.NightWhisper: -1, Item.Echo: 62.5 })
    trade(0, { Item.StarstoneDemark: -1, Item.Echo: 312.5 })
    trade(0, { Item.BreathOfTheVoid: -1, Item.Echo: 1560 })

    # Wines
    buy_sell(config, Item.BottleOfGreyfields1882, -0.02, 0.01)
    buy_sell(config, Item.BottleOfGreyfields1882, -0.04, 0.02)
    trade(0, { Item.BottelofMorelways1872: -1, Item.Echo: 0.1 })
    trade(0, { Item.BottleOfStranglingWillowAbsinthe: -1, Item.Echo: 0.5 })
    trade(0, { Item.BottleOfBrokenGiant1844: -1, Item.Echo: 2.5 })
    trade(0, { Item.CellarOfWine: -1, Item.Echo: 12.5 })
    trade(0, { Item.BottleOfFourthCityAirag: -1, Item.Echo: 62.5 })
    trade(0, { Item.TearsOfTheBazaar: -1, Item.Echo: 312.5 })
    trade(0, { Item.VialOfMastersBlood: -1, Item.Echo: 1562.6 })
    trade(0, { Item.BottledOblivion: -1, Item.Echo: 0.01 })
    trade(0, { Item.BottleOfGreyfields1868FirstSporing: -1, Item.Echo: 0.2 })
    
    # Zee Treasures
    buy_sell(config, Item.MoonPearl, -0.03, 0.01)
    trade(0, { Item.DeepZeeCatch: -1, Item.Echo: 0.5 })
    trade(0, { Item.RoyalBlueFeather: -1, Item.Echo: 0.5 })
    trade(0, { Item.AmbiguousEolith: -1, Item.Echo: 0.5 })
    trade(0, { Item.CarvedBallOfStygianIvory: -1, Item.Echo: 2.5 })
    trade(0, { Item.LiveSpecimen: -1, Item.Echo: 2.5 })

    # Equipment
    buy_sell(config, Item.SulkyBat, -0.4, 0.2)
    buy_sell(config, Item.LuckyWeasel, -0.4, 0.2)
    buy_sell(config, Item.BundleOfRaggedClothing, -0.03, 0.01)
    buy_sell(config, Item.CheerfulGoldfish, -0.40, 0.04)
    
    # Unsorted
    trade(0, { Item.CracklingDevice: -1, Item.Echo: 62.5 })