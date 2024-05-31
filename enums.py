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

class Grade(Enum):
    Avoid = -100
    Bad = 0
    Good = 100
    Excellent = 200

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
    Chthonosophy = auto()

    Respectable = auto()
    Dreaded = auto()
    Bizarre = auto()

    Inerrant = auto()
    Insubstantial = auto()
    Neathproofed  = auto()

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
    Constraint = 0
    Echo = auto()

    Action = auto()
    CardDraws = auto() # Fake item
    # DayOfCardDraws = 3 # Fake item

    # Actions
    RootAction = auto()

    LondonAction = auto()

    JerichoAction = auto()

    PortCecilAction = auto()
    MangroveAction = auto()

    # Rat Market Hack TODO figure out real groupings
    RatMarketWeek1ExhaustionStage1 = auto()
    RatMarketWeek2ExhaustionStage1 = auto()
    RatMarketWeek3ExhaustionStage1 = auto()
    RatMarketWeek4ExhaustionStage1 = auto()
    RatMarketWeek5ExhaustionStage1 = auto()
    RatMarketWeek6ExhaustionStage1 = auto()
    RatMarketWeek7ExhaustionStage1 = auto()
    RatMarketWeek8ExhaustionStage1 = auto()
    RatMarketWeek9ExhaustionStage1 = auto()
    RatMarketWeek10ExhaustionStage1 = auto()
    RatMarketWeek11ExhaustionStage1 = auto()
    RatMarketWeek12ExhaustionStage1 = auto()

    RatMarketWeek1ExhaustionStage2 = auto()
    RatMarketWeek2ExhaustionStage2 = auto()
    RatMarketWeek3ExhaustionStage2 = auto()
    RatMarketWeek4ExhaustionStage2 = auto()
    RatMarketWeek5ExhaustionStage2 = auto()
    RatMarketWeek6ExhaustionStage2 = auto()
    RatMarketWeek7ExhaustionStage2 = auto()
    RatMarketWeek8ExhaustionStage2 = auto()
    RatMarketWeek9ExhaustionStage2 = auto()
    RatMarketWeek10ExhaustionStage2 = auto()
    RatMarketWeek11ExhaustionStage2 = auto()
    RatMarketWeek12ExhaustionStage2 = auto()

    RatMarketWeek1ExhaustionStage3 = auto()
    RatMarketWeek2ExhaustionStage3 = auto()
    RatMarketWeek3ExhaustionStage3 = auto()
    RatMarketWeek4ExhaustionStage3 = auto()
    RatMarketWeek5ExhaustionStage3 = auto()
    RatMarketWeek6ExhaustionStage3 = auto()
    RatMarketWeek7ExhaustionStage3 = auto()
    RatMarketWeek8ExhaustionStage3 = auto()
    RatMarketWeek9ExhaustionStage3 = auto()
    RatMarketWeek10ExhaustionStage3 = auto()
    RatMarketWeek11ExhaustionStage3 = auto()
    RatMarketWeek12ExhaustionStage3 = auto()


    # Bone Market Hack
    AntiquityReptileAction = auto()
    AntiquityAmphibianAction = auto()    
    AntiquityBirdAction = auto()
    AntiquityFishAction = auto()
    AntiquityArachnidAction = auto()
    AntiquityInsectAction = auto()

    AmalgamyReptileAction = auto()
    AmalgamyAmphibianAction = auto()    
    AmalgamyBirdAction = auto()
    AmalgamyFishAction = auto()
    AmalgamyArachnidAction = auto()
    AmalgamyInsectAction = auto()

    MenaceReptileAction = auto()
    MenaceAmphibianAction = auto()    
    MenaceBirdAction = auto()
    MenaceFishAction = auto()
    MenaceArachnidAction = auto()
    MenaceInsectAction = auto()      

    AntiquityGeneralAction = auto()
    AmalgamyGeneralAction = auto()
    MenaceGeneralAction = auto()

    GeneralReptileAction = auto()
    GeneralAmphibianAction = auto()    
    GeneralBirdAction = auto()
    GeneralFishAction = auto()
    GeneralArachnidAction = auto()
    GeneralInsectAction = auto()    

    # Menaces
    Wounds = auto()
    Scandal = auto()
    Suspicion = auto()
    Nightmares = auto()

    Irrigo = auto()
    TroubledWaters = auto()

    BoneMarketExhaustion = auto()
    RatMarketExhaustion = auto()
    SeeingBanditryInTheUpperRiver = auto()
    InCorporateDebt = auto()

    # Second Chances
    SuddenInsight = auto()
    HastilyScrawledWarningNote = auto()
    HardEarnedLesson = auto()
    ConfidentSmile = auto()

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

    FavourFingerkings = auto()

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
    UnusualLoveStory = auto()
    SlimVolumeOfBazaarinePoetry = auto()

    # Curiosity
    ABlueAndShiningStone = auto()
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
    CollectionOfCuriosities = auto() # not a curiosity???

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
    UnassumingCrate = auto()

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
    ObsidianChitinTail = auto()
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

    # Psueo-items for failed assembly checks
    FailedStygianIvorySkull = auto()
    FailedHornedSkull = auto()
    FailedPentagrammaticSkull = auto()
    FailedSkullInCoral = auto()
    FailedPlatedSkull = auto()
    FailedDoubledSkull = auto()
    FailedSabreToothedSkull = auto()
    FailedBrightBrassSkull = auto()

    FailedKnottedHumerus = auto()
    FailedFossilisedForelimb = auto()
    FailedIvoryHumerus = auto()

    FailedFemurOfAJurassicBeast = auto()
    FailedHelicalThighbone = auto()
    FailedHolyRelicOfTheThighOfStFiacre = auto()
    FailedIvoryFemur = auto()

    FailedBatWing = auto()
    FailedWingOfAYoungTerrorBird = auto()
    FailedAlbatrossWing = auto()
    FailedFinBonesCollected = auto()
    FailedAmberCrustedFin = auto()

    FailedJetBlackStinger = auto()
    FailedObsidianChitinTail = auto()
    FailedPlasterTailBones = auto()
    FailedTombLionsTail = auto()

    FailedWitheredTentacleLimb = auto()
    FailedWitheredTentacleTail = auto()

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
    RumourmongersNetwork = auto()

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

    # Firmament Stuff
    Stuiver = auto()
    AscendedAmbergris = auto()
    CausticApocryphon = auto()
    MemoryOfAMuchStrangerSelf = auto()
    RoofChart = auto()
    SampleOfRoofDrip = auto()
    StarvedExpression = auto()
    TempestuousTale = auto()
    GlimEncrustedCarapace = auto()

    # -----
    # Equipment
    # -----

    # Weapon
    ConsignmentOfScintillackSnuff = auto()

    # Companion
    LuckyWeasel = auto()
    SulkyBat = auto()
    WinsomeDispossessedOrphan = auto()
    CheerfulGoldfish = auto()

    # Unsorted
    BundleOfRaggedClothing = auto()

    # -----
    # Qualities
    # -----

    # TODO: organize this section somehow

    # Weekly Stuff
    FreeEvening = auto()
    FavourableCircumstance = auto()
    AnEarnestOfPayment = auto()
    AConsequenceOfYourAmbition = auto()
    BraggingRightsAtTheMedusasHead = auto()
    DelayUntilTheNextBoardMeeting = auto()
    RecentParticipantInAStarvedCulturalExchange = auto()
    RavagesOfParabolanWarfare = auto()
    FleetingRecollections = auto()
    AGiftFromBalmoral = auto()
    GlowingViric = auto()
    MiredInMail = auto()
    AReportFromTheKhagansPalace = auto()

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

    Attar = auto()
    
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
    HeartsGameExploits = auto()
    ApproximateValueOfOutstandingInvoicesInPennies = auto()
    HinterlandProsperity = auto()

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

    Moonlit = auto()

    CoverTiesGeneric = auto()
    CoverTiesSurface = auto()
    CoverTiesBazaar = auto()
    CoverTiesDispossessed = auto()

    CoverElaboration = auto()
    CoverNuance = auto()
    CoverWitnessnes = auto()
    CoverCredentials = auto()
    CoverBackstory = auto()

    CompletedPainting = auto()
    PresentYourPaintingInLondon = auto()
    PresentYourPaintingInHeliconHouse = auto()

    PaintingIncendiary = auto()
    PaintingLuminosity = auto()
    PaintingNostalgic = auto()
    PaintingAnyQuality = auto()

    MonographCautionary = auto()
    MonographTragic = auto()
    MonographIronic = auto()

    DiscordantLaw = auto()

    TheMindsAscent1 = auto()
    TheMindsAscent2 = auto()
    TheMindsAscent3 = auto()

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
    DuplicatedCounterfeitHeadOfJohnTheBaptist = auto()
    VictimsSkull = auto()
    ASkeletonOfYourOwn = auto()

    Placeholder = auto()

    # Zailing
    ZailingProgress = auto()
    HomeWatersZeeDraw = auto()
    ShephersWashZeeDraw = auto()
    StormbonesZeeDraw = auto()
    SeaOfVoicesZeeDraw = auto()
    SaltSteppesZeeDraw = auto()
    PillaredSeaZeeDraw = auto()
    SnaresZeeDraw = auto()

    # Upper River
    DigsInEvenlode = auto()

    # FATE
    MythicPotential = auto()
    MoralisingDevelopment = auto()
    HeroicRally = auto()
    InscrutableTwist = auto()
    WhiskerwaysSecondaryPayout = auto()

    FruitfulAsceticism = auto()
    FruitfulCuriosity = auto()
    FruitfulFrivolity = auto()
    FruitfulRot = auto()
    PhilsofruitYield = auto()

    # ---------------------------------
    # ---------- Cards ----------------
    # ---------------------------------

    '''
    CXY_CardName
    X is a character for the broader location
    - L for London
    - H for Hinterlands / Railway
    - F for Firmament / Roof
    - Z for Unterzee
    avoiding R bc ambiguous between railway and roof

    Y is optional character(s) for sub-location that has transit costs
    - Ea for Ealing
    - Je for Jericho
    - ME for Magistracy of Evenlode
    - Ba for Balmoral
    - St for Station VIII
    - Bu for Burrow
    - Mo for Moulin
    - Hu for Hurlers
    - MS for Marigold

    idk man this is a lot maybe just use the full names

    '''
    LondonDraw = auto()
    
    # Lodgings
    CL_LairInTheMarshes = auto()
    CL_CottageByTheObservatory = auto()
    CL_RoomsInAHalfAbandonedMansion = auto()
    CL_RoomsAboveABookshop = auto()
    CL_RoomsAboveAGamblingDen = auto()
    CL_HandsomeTownhouse = auto()
    CL_RooftopShack = auto()
    CL_DecommissionedSteamer = auto()
    CL_SmokyFlophouse = auto()
    CL_AGuestRoomAtTheBrassEmbassy = auto()
    CL_ARoomAtTheRoyalBethlehemHotel = auto()
    CL_PremisesAtTheBazaar = auto()

    CL_AVisit = auto()
    CL_ConnectedPet = auto()

    CL_ClaySedanChair = auto()
    CL_GodsEditors = auto() # TODO

    CL_BewilderingProcessionSpouse = auto()
    
    CL_YoungStags = auto()

    CL_Bohemians = auto()
    CL_Church = auto()    
    CL_Constables = auto()
    CL_Criminals = auto()
    CL_Docks = auto()
    CL_GreatGame = auto()
    CL_Hell = auto()
    CL_Revolutionaries = auto()
    CL_RubberyMen = auto()
    CL_Society = auto()                            
    CL_TombColonies = auto()                            
    CL_Urchins = auto()                            

    # TODO
    CL_Dreams1 = auto()
    CL_Dreams2 = auto()
    CL_Dreams3 = auto()
    CL_Dreams4 = auto()
    CL_Dreams5 = auto()

    # All TODO
    CL_Arbor = auto()
    CL_TournamentOfWeasels = auto()
    CL_OrthographicInfection = auto()
    CL_CityVicesDecadentEvening = auto()
    CL_ARestorative = auto()
    CL_AfternoonOfGoodDeeds = auto()
    CL_AMomentsPeace = auto()
    CL_TheInterpreterOfDreams = auto()
    CL_AnImplausiblePenance = auto()
    CL_TheSeekersOfTheGarden = auto()
    CL_DevicesAndDesires = auto()
    CL_APoliteInvitation = auto()
    CL_GiveAGift = auto()
    CL_ADayAtTheRaces = auto()
    CL_OnesPublic = auto()
    CL_BringingTheRevolution = auto()
    CL_MirrorsAndClay = auto()
    CL_TheCitiesThatFell = auto()
    CL_TheSoftHeartedWidow = auto()
    CL_AllFearTheOvergoat = auto()
    CL_TheNorthboundParliamentarian = auto()
    CL_WeatherAtLast = auto()
    CL_AnUnusualWager = auto()
    CL_MrWinesIsHoldingASale = auto()
    CL_TheAwfulTemtpationfMoney = auto()
    CL_InvestigatingTheAffluentPhotographer = auto()
    CL_TheGeologyOfWinewound = auto()
    CL_APublicLecture = auto()
    CL_WantedRemindersOfBrighterDays = auto()
    CL_AnUnsignedMessage = auto()
    CL_APresumptuousLittleOpportunity = auto()
    CL_SLowcakesAmanuensis = auto()
    CL_AMerrySortOfCrime = auto()
    CL_ADustyBookshop = auto()
    CL_ALittleOmen = auto()
    CL_ADisgracefulSpectacle = auto()
    CL_AVoiceFromAWell = auto()
    CL_AFineDayInTheFlit = auto()
    CL_TheParanomasticNewshound = auto()

    CL_Relicker1 = auto()
    CL_Relicker2 = auto()
    CL_Relicker3 = auto()
    CL_Relicker4 = auto()

    # Fate Cards
    CL_ATradeInSouls = auto()
    CL_YourAunt = auto()

    # Zailing
    Card_NavigationError = auto()

    # Philsofruits
    # named after the png icons

    CZP_TreeBlue = auto()
    CZP_Blemmigan = auto()
    CZP_Passerby = auto()
    CZP_Argument = auto()
    CZP_Crowd2 = auto()     
    CZP_Jungle = auto()     
    CZP_Stick = auto()     
    CZP_Cherries = auto()     
    CZP_MangroveCollegeInterior = auto()     
    CZP_ElegaicCockatoo = auto()     
    CZP_Drowned = auto()     
    CZP_SpiderTree = auto()     
    CZP_Parrot = auto()