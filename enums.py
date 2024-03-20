from enum import Enum, auto

class Location(Enum):
    NoLocation = auto()
    # London
    BazaarSideStreet = auto()
    LadybonesRoad = auto()
    YourLodgings = auto()
    MahoganyHall = auto()
    MolochStreet = auto()
    MrsPlentysCarnival = auto()
    Spite = auto()
    TheFlit = auto()
    TheShutteredPalace = auto()
    TheUniversity = auto()
    Veilgarden = auto()
    WatchmakersHill = auto()
    WilmotsEnd = auto()
    WolfstackDocks = auto()

    # zailing
    HomeWaters = auto()
    ShepherdsWash = auto()
    Stormbones = auto()
    TheSeaOfVoices = auto()
    TheSaltSteppes = auto()
    ThePillaredSea = auto()
    TheSnares = auto()
    
    # railway
    EalingGardens = auto()
    JerichoLocks = auto()
    TheMagistracyOfTheEvenlode = auto()
    Balmoral = auto()
    StationVIII = auto()
    BurrowInfraMump = auto()
    Moulin = auto()
    TheHurlers = auto()
    MarigoldStation = auto()

class Deck(Enum):
    London = auto()
    UpperRiver = auto()
    Zailing = auto()
    Laboratory = auto()

class Rarity(Enum):
    Rare = 10
    Unusual = 20
    VeryInfrequent = 50
    Infrequent = 80
    Standard = 100
    Frequent = 200
    Abundant = 500
    Ubiquitous = 1000

class Score(Enum):
    NeverPlay = -100
    Bad = -50
    Zero = 0
    Okay = 50
    Good = 100
    Amazing = 200

class Profession(Enum):
    NoProfession = auto()
    CrookedCross = auto()
    Correspondent = auto()
    Licentiate = auto()
    Midnighter = auto()
    MonsterHunter = auto()
    Silverer = auto()
    Notary = auto()
    Doctor = auto()

class Specialization(Enum):
    NoSpecializaiton = auto()
    Epistolant = auto()
    CrimsonEngineer = auto()
    Fractionist = auto()
    Siopian = auto()
    HeirarchOfTheHunt = auto()
    Teratomancer = auto()
    Iniquitor = auto()
    Letheologist = auto()
    Oneirotect = auto()
    OntologicalCartographer = auto()
    Beatificator = auto()
    Schismatic = auto()


class Ambition(Enum):
    NoAmbition = auto()
    BagALegend = auto()
    HeartsDesire = auto()
    LightFingers = auto()
    Nemesis = auto()

class Stat(Enum):
    Watchful = auto()
    Shadowy = auto()
    Dangerous = auto()
    Persuasive = auto()
    KatalepticToxicology = auto()
    MonstrousAnatomy = auto()
    APlayerOfChess = auto()
    Glasswork = auto()
    ShapelingArts = auto()
    ArtisanOfTheRedScience = auto()
    Mithridacy = auto()
    StewardOfTheDiscordance = auto()
    Zeefaring = auto()

class Treasure(Enum):
    NoTreasure = auto()

    VastNetworkOfConnections = auto()
    WingedAndTalonedSteed = auto()
    SocietyOfTheThreeFingeredHand = auto()
    LongDeadPriestsOfTheRedBird = auto()

    TheRobeOfMrCards = auto()
    NewlyCastCrownOfTheCityOfLondon = auto()
    LeaseholdOnAllOfLondon = auto()
    PalatialHomeInTheArcticCircle = auto()
    TheMarvellous = auto()

    KittenSizedDiamond = auto()
    FalseStartOfYourOwn = auto()

    YourLovedOneReturned = auto() # any differences?
    BloodiedTravellingCoatOfMrCups = auto()

class Item(Enum):
    Echo = 0

    Action = 1
    CardDraws = 2 # Fake item
    # DayOfCardDraws = 3 # Fake item

    # Menaces
    Wounds = auto()
    Scandal = auto()
    Suspicion = auto()
    Nightmares = auto()

    Irrigo = auto()
    TroubledWaters = auto()

    SeeingBanditryInTheUpperRiver = auto()
    InCorporateDebt = auto()

    # Favours
    FavBohemians = auto()
    FavChurch = auto()
    FavConstables = auto()
    FavCriminals = auto()
    FavDocks = auto()
    FavGreatGame = auto()
    FavHell = auto()
    FavRevolutionaries = auto()
    FavRubberyMen = auto()
    FavSociety = auto()
    FavTombColonies = auto()
    FavUrchins = auto()

    # Connected
    ConnectedBenthic = auto()
    ConnectedSummerset = auto()

    # Academic
    FoxfireCandleStub = auto()
    FlaskOfAbominableSalts = auto()
    MemoryOfDistantShores = auto()
    IncisiveObservation = auto()
    UnprovenancedArtefact = auto()
    VolumeOfCollatedResearch = auto()
    MirthlessCompendium = auto()
    BreakthroughInCurrencyDesign = auto()
    JudgementsEgg = auto()
    SecretCollege = auto()
    MemoryOfDiscordance = auto()
    LostResearchAssistant = auto()

    # Book
    RevisionistHistoricalNarrative = auto()
    CorrectiveHistorialNarrative = auto()

    # Curiosity
    VenomRuby = auto()
    Sapphire = auto()
    StrongBackedLabour = auto()
    WhirringContraption = auto()
    CracklingDevice = auto()
    CounterfeitHeadOfJohnTheBaptist = auto()

    # Curiosity - reagents
    ObliviscereMori = auto()
    ElationAtFelineOration = auto()
    VindicationOfFaith = auto()
    ExhilarationFromAchievingJustice= auto()
    HorrifyingConfirmationThatYouWereRightAllAlong= auto()
    UnthinkableHope = auto()
    HalcyonicTonic = auto()
    FillipOfEffervescence = auto()
    HolySanguinarineOintment = auto()
    DiscriminatingAconite = auto()

    CrystallizedEuphoria = auto()
    OilOfCompanionship = auto()
    SalveOfRighteousness = auto()
    DistillationOfRetribution = auto()
    ConcentrateOfSelf = auto()
    PowderOfRenewal = auto()

    # Cartography
    ShardOfGlim = auto()
    MapScrap = auto()
    ZeeZtory = auto()
    PartialMap = auto()
    PuzzlingMap = auto()
    SaltSteppeAtlas = auto()
    RelativelySafeZeeLane = auto()
    SightingOfAParabolanLandmark = auto()
    GlassGazette = auto()
    VitreousAlmanac = auto()
    OneiromanticRevelation = auto()
    ParabolanParable = auto()
    CartographersHoard = auto()
    WaswoodAlmanac = auto()

    # Contraband
    FlawedDiamond = auto()
    OstentatiousDiamond = auto()
    MagnificentDiamond = auto()
    FabulousDiamond = auto()
    LondondStreetSign = auto()
    UseOfVillains = auto()
    ComprehensiveBribe = auto()
    MirrorcatchBox = auto()
    Hillmover = auto()

    # Currency
    FirstCityCoin = auto()
    FistfulOfSurfaceCurrency = auto()
    HinterlandScrip = auto()
    RatShilling = auto()
    AssortmentOfKhaganianCoinage = auto()
    FourthCityEcho = auto()

    # Elder
    JadeFragment = auto()
    RelicOfTheThirdCity = auto()
    MysteryOfTheElderContinent = auto()
    PresbyteratePassphrase = auto()
    AntiqueMystery = auto()
    PrimaevalHint = auto()
    ElementalSecret = auto()

    # Goods
    CertifiableScrap = auto()
    NevercoldBrassSliver = auto()
    PreservedSurfaceBlooms = auto()
    KnobOfScintillack = auto()
    PieceOfRostygold = auto()
    BessemerSteelIngot = auto()
    NightsoilOfTheBazaar = auto()
    PerfumedGunpowder = auto()
    RailwaySteel = auto()

    # Great Game
    WellPlacedPawn = auto()
    FinalBreath = auto()
    MovesInTheGreatGame = auto()
    VitalIntelligence = auto()
    CopperCipherRing = auto()
    CorrespondingSounder = auto()

    ViennaOpening = auto()
    EpauletteMate = auto()
    QueenMate = auto()
    Stalemate = auto()
    MuchNeededGap = auto()
    InterceptedCablegram = auto()

    # Historical
    RelicOfTheFourthCity = auto()
    RustedStirrup = auto()
    SilveredCatsClaw = auto()
    RelicOfTheSecondCity = auto()
    TraceOfViric = auto()
    TraceOfTheFirstCity = auto()
    NicatoreanRelic = auto()
    UnlawfulDevice = auto()
    FlaskOfWaswoodSpringWater = auto()
    ChimericalArchive = auto()

    # Infernal
    Soul = auto()
    AmanitaSherry = auto()
    BrilliantSoul = auto()
    MuscariaBrandy = auto()
    BrassRing = auto()
    DevilboneDice = auto()
    PortfolioOfSouls = auto()
    QueerSoul = auto()
    SilentSoul = auto()
    BrightBrassSkull = auto()
    DiscordantSoul = auto()
    CoruscatingSoul = auto()
    ReportedLocationOfAOneTimePrinceOfHell = auto()

    # Influence
    StolenCorrespondence = auto()
    IntriguingSnippet = auto()
    CompromisingDocument = auto()
    SecludedAddress = auto()
    StolenKiss = auto()
    FavourInHighPlaces = auto()
    PersonalRecommendation = auto()
    ExigentNote = auto()

    # Legal
    InfernalContract = auto()
    DubiousTestimony = auto()
    SwornStatement = auto()
    CaveAgedCodeOfHonour = auto()
    LegalDocument = auto()
    FragmentOfTheTragedyProcedures = auto()
    SapOfTheCedarAtTheCrossroads = auto()
    EdictsOfTheFirstCity = auto()

    # Luminosity
    LumpOfLamplighterBeeswax = auto()
    PhosphorescentScarab = auto()
    MemoryOfLight = auto()
    MourningCandle = auto()
    KhaganianLightbulb = auto()
    ChrysalisCandle = auto()
    TailfeatherBrilliantAsFlame = auto()
    SnuffersGratitude = auto()
    BejewelledLens = auto()
    EyelessSkull = auto()
    ElementOfDawn = auto()
    MountainSherd = auto()
    RayDrenchedCinder = auto()

    # Mysteries
    WhisperedHint = auto()
    CrypticClue = auto()
    AppallingSecret = auto()
    JournalOfInfamy = auto()
    TaleOfTerror = auto()
    ExtraordinaryImplication = auto()
    UncannyIncunabulum = auto()
    DirefulReflection = auto()
    SearingEnigma = auto()
    DreadfulSurmise = auto()
    ImpossibleTheorem = auto()
    MemoryOfALesserSelf = auto()

    # Nostalgia
    DropOfPrisonersHoney = auto()
    RomanticNotion = auto()
    VisionOfTheSurface = auto()
    TouchingLoveStory = auto()
    BazaarPermit = auto()
    EmeticRevelation = auto()
    CaptivatingBallad = auto()

    # Osteology
    AlbatrossWing = auto()
    AmberCrustedFin = auto()
    BatWing = auto()
    BoneFragments = auto()
    CrustaceanPincer = auto()
    DoubledSkull = auto()
    FemurOfAJurassicBeast = auto()
    FemurOfASurfaceDeer = auto()
    FinBonesCollected = auto()
    FivePointedRibcage = auto()
    FlourishingRibcage = auto()
    FossilisedForelimb = auto()
    HeadlessSkeleton = auto()
    HelicalThighbone = auto()
    HolyRelicOfTheThighOfStFiacre = auto()
    HornedSkull = auto()
    HumanArm = auto()
    HumanRibcage = auto()
    IvoryFemur = auto()
    IvoryHumerus = auto()
    JetBlackStinger = auto()
    KnottedHumerus = auto()
    LeviathanFrame = auto()
    MammothRibcage = auto()
    MoonlightScales = auto()
    PentagrammicSkull = auto()
    PlasterTailBones = auto()
    PlatedSkull = auto()
    PrismaticFrame = auto()
    RibcageWithABoutiqueOfEightSpines = auto()
    SabreToothedSkull = auto()
    SegmentedRibcage = auto()
    SkeletonWithSevenNecks = auto()
    SkullInCoral = auto()
    SurveyOfTheNeathsBones = auto()
    ThornedRibcage = auto()
    TombLionsTail = auto()
    UnidentifiedThighbone = auto()
    WarblerSkeleton = auto()
    WingOfAYoungTerrorBird = auto()
    WitheredTentacle = auto()

    # Rag Trade
    SilkScrap = auto()
    SurfaceSilkScrap = auto()
    WhisperSatinScrap = auto()
    ThirstyBombazineScrap = auto()
    PuzzleDamaskScrap = auto()
    ParabolaLinenScrap = auto()
    ScrapOfIvoryOrganza = auto()
    VeilsVelvetScrap = auto()

    # Ratness
    RatOnAString = auto()
    VengeRatCorpse = auto()
    BaptisedRattusFaberCorpse = auto()
    RattyReliquary = auto()

    # Rubbery
    NoduleOfDeepAmber = auto()
    NoduleOfWarmAmber = auto()
    UnearthlyFossil = auto()
    NoduleOfTremblingAmber = auto()
    NoduleOfPulsatingAmber = auto()
    NoduleOfFecundAmber = auto()
    FlukeCore = auto()
    RubberySkull = auto()

    # Rumour
    ProscibedMaterial = auto()
    InklingOfIdentity = auto()
    ScrapOfIncendiaryGossip = auto()
    AnIdentityUncovered = auto()
    BlackmailMaterial = auto()
    NightOnTheTown = auto()
    RumourOfTheUpperRiver = auto()
    DiaryOfTheDead = auto()
    MortificationOfAGreatPower = auto()
    IntriguersCompendium = auto()

    # Sustenance
    ParabolanOrangeApple = auto()
    RemainsOfAPinewoodShark = auto()
    JasmineLeaves = auto()
    PotOfVenisonMarrow = auto()
    SolaceFruit = auto()
    DarkDewedCherry = auto()
    BasketOfRubberyPies = auto()
    CrateOfIncorruptibleBiscuits = auto()
    HellwormMilk = auto()
    TinOfZzoup = auto()
    SausageAboutWhichNoOneComplains = auto()
    TinnedHam = auto()
    HandPickedPeppercaps = auto()
    MagisterialLager = auto()

    # Theological
    PalimpsestScrap = auto()
    ApostatesPsalm = auto()
    VerseOfCounterCreed = auto()
    FalseHagiotoponym = auto()

    # Wines
    BottleOfGreyfields1879 = auto()
    BottleOfGreyfields1882 = auto()
    BottelofMorelways1872 = auto()
    BottleOfStranglingWillowAbsinthe = auto()
    BottleOfBrokenGiant1844 = auto()
    CellarOfWine = auto()
    BottleOfFourthCityAirag = auto()
    TearsOfTheBazaar = auto()
    VialOfMastersBlood = auto()
    BottledOblivion = auto()
    BottleOfGreyfields1868FirstSporing = auto()

    # Wild Words
    PrimordialShriek = auto()
    ManiacsPrayer = auto()
    CorrespondencePlaque = auto()
    AeolianScream = auto( )
    StormThrenody = auto()
    NightWhisper = auto()
    StarstoneDemark = auto()
    BreathOfTheVoid = auto()

    # Zee-Treasures
    MoonPearl = auto()
    DeepZeeCatch = auto()
    RoyalBlueFeather = auto()
    AmbiguousEolith = auto()
    CarvedBallOfStygianIvory = auto()
    LiveSpecimen = auto()
    MemoryOfAShadowInVarchas = auto()
    OneiricPearl = auto()

    # Culinary Concoction
    SharplyFlavoredPickleAsYetUnpoisoned = auto()
    JetBlackPickleRelishDosedWithHillchangerScorpionVenom = auto()
    EnvenomedPicklesSuspendedInVenisonAspic = auto()    
    AnEnticingFungalPate = auto()
    APlatterOfMixedCharcuterie = auto()
    ATowerOfFungalPateFlambe = auto()
    VibrantPepperyFishBroth = auto()
    CaduceanZzoupWithGunpowderAndSicklyRose = auto()
    SharkBouillabaisseWithCroutons = auto()
    CulinaryTributeToTheSeaOfSpines = auto()
    DarkDewedCherryLiquer = auto()
    SparklingSolacefruitRoyale = auto()
    SolacefruitChampagneSorbet = auto()
    SelfReflectiveTapenadeOfParabolanOrangeApple = auto()
    SourPickleOfParabolanOrangeAppleAndVinegar = auto()
    OrangeAppleJamSpikedWithMuscariaBrandy = auto()
    MarmaladeOfParabolanOrangeAppleHoneyAndRoseateAttar = auto()
    CuratorialCocktail = auto()

    # -----
    # Equipment
    # -----

    # Weapon
    ConsignmentOfScintillackSnuff = auto()

    # Companion
    LuckyWeasel = auto()
    SulkyBat = auto()
    WinsomeDispossessedOrphan = auto()

    # -----
    # Qualities
    # -----

    # TODO: organize this section somehow

    # Quriks
    Austere = auto()
    Hedonist = auto()

    # Laboratory
    LaboratoryResearch = auto()
    ParabolanResearch = auto()

    # IDK what to call these
    Casing = auto()
    Corresponding = auto()
    Fascinating = auto()
    Inspired = auto()
    Infiltrating = auto()
    Investigating = auto()
    
    DramaticTension = auto()

    # Professional Activities
    ServicesHell = auto()
    ServicesZailors = auto()
    ServicesTheGreatGame = auto()
    ServicesBohemians = auto()
    ServicesSociety = auto()
    ServicesTheGraciousWidow = auto()
    ServicesTheHoneyAddledDetective = auto()
    ServicesTombColonists = auto()
    ServicesBenthic = auto()
    ServicesTheChurch = auto()
    ServicesConstables = auto()
    ServicesClay = auto()    

    # miscellaneous
    ResearchOnAMorbidFad = auto()
    Tribute = auto()
    AConsequenceOfYourAmbition = auto()
    BraggingRightsAtTheMedusasHead = auto()
    HeartsGameExploits = auto()
    ApproximateValueOfOutstandingInvoicesInPennies = auto()

    # Piracy
    ChasingDownYourBounty = auto()
    StashedTreasure = auto()

    # Upper River
    FittingInAtHeliconHouse = auto()
    TimeRemainingAtHeliconHouseTwoThruFive = auto()
    TimeRemainingAtHeliconHouseExactlyOne = auto()

    PalaeontologicalDiscovery = auto()
    EsteemOfTheGuild = auto()
    WagesOfADig = auto()

    MonographCautionary = auto()
    MonographTragic = auto()
    MonographIronic = auto()

    DiscordantLaw = auto()

    # ----- Psuedo Items
    VisitFromTimeTheHealer = auto()

    AirsOfLondonChange = auto()

    AirsOfIndustry1to10 = auto()
    AirsOfIndustry11to20 = auto() # should be 10-20?
    AirsOfIndustry21to30 = auto()
    AirsOfIndustry31to40 = auto()
    AirsOfIndustry41to50 = auto()
    AirsOfIndustry51to60 = auto()
    AirsOfIndustry61to70 = auto()
    AirsOfIndustry71to80 = auto()
    AirsOfIndustry81to90 = auto()
    AirsOfIndustry91to100 = auto()


    PortCecilCycles = auto()
    TimeAtJerichoLocks = auto()
    TimeAtWakefulCourt  = auto() # tribute grind
    ZailingDraws = auto() # self-explanatory
    SlightedAcquaintance = auto() # newspaper
    ParabolaRoundTrip = auto()

    DuplicatedVakeSkull = auto()
    ASkeletonOfYourOwn = auto()

    # Cards
    Card_AVisit = auto()
    Card_ConnectedPet = auto()
    Card_NavigationError = auto()

    # Zailing
    HomeWatersZeeDraw = auto()
    ShephersWashZeeDraw = auto()
    StormbonesZeeDraw = auto()
    SeaOfVoicesZeeDraw = auto()
    SaltSteppesZeeDraw = auto()
    PillaredSeaZeeDraw = auto()
    SnaresZeeDraw = auto()

    # Upper River
    DigsInEvenlode = auto()