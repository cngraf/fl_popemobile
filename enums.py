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
    SeaOfVoices = auto()
    SaltSteppes = auto()
    PillaredSea = auto()
    Snares = auto()
    
    # railway
    EalingGardens = auto()
    JerichoLocks = auto()
    MagistracyOfTheEvenlode = auto()
    Balmoral = auto()
    StationVIII = auto()
    BurrowInfraMump = auto()
    Moulin = auto()
    Hurlers = auto()
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

# TODO obsolete
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

    _NoItem = auto()

    _CardDraws = auto()

    _ParabolaAction = auto()
    _ParabolaRoundTrip = auto()

    _EalingAction = auto()
    _JerichoAction = auto()
    _EvenlodeAction = auto()
    _BalmoralAction = auto()
    _StationViiiAction = auto()
    _BurrowAction = auto()
    _MoulinAction = auto()
    _HurlersAction = auto()
    _MarigoldAction = auto()
    
    _HeliconAction = auto()

    _JerichoFavourExchange = auto()

    _WakefulEyeAction = auto()
    _KhanateAction = auto()
    _SeaOfVoicesAction = auto()
    _PortCecilAction = auto()
    _MangroveAction = auto()

    _HallowsThroatAction = auto()
    _MidnightMoonAction = auto()
    _ZenithAction = auto()


    #######################################################
    #                       Stats
    #######################################################  

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
    
    _WoundsReduction = auto()
    _ScandalReduction = auto()
    _SuspicionReduction = auto()
    _NightmaresReduction = auto()

    # Second Chances
    SuddenInsight = auto()
    HastilyScrawledWarningNote = auto()
    HardEarnedLesson = auto()
    ConfidentSmile = auto()


    #######################################################
    #                       Story
    #######################################################

    # Ambition
    BagALegend = auto()
    HeartsDesire = auto()
    LightFingers = auto()
    Nemesis = auto()


    #######################################################
    #                       Menaces
    #######################################################

    # Menaces
    Wounds = auto()
    Scandal = auto()
    Suspicion = auto()
    Nightmares = auto()

    Irrigo = auto()
    TroubledWaters = auto()

    SeeingBanditryInTheUpperRiver = auto()
    InCorporateDebt = auto()
    AdvancingTheLiberationOfNight = auto()

    #######################################################
    #                       Rat Market
    #######################################################

    _RatMarketRotation = auto()
    
    _GeneralRatMarketSaturation1 = auto()
    SoftRatMarketSaturation1 = auto()
    SaintlyRatMarketSaturation1 = auto()
    MaudlinRatMarketSaturation1 = auto()
    InscrutableRatMarketSaturation1 = auto()
    TempestuousRatMarketSaturation1 = auto()
    IntricateRatMarketSaturation1 = auto()
    CalculatingRatMarketSaturation1 = auto()
    RuinousRatMarketSaturation1 = auto()

    _GeneralRatMarketSaturation2 = auto()
    SoftRatMarketSaturation2 = auto()
    SaintlyRatMarketSaturation2 = auto()
    MaudlinRatMarketSaturation2 = auto()
    InscrutableRatMarketSaturation2 = auto()
    TempestuousRatMarketSaturation2 = auto()
    IntricateRatMarketSaturation2 = auto()    
    CalculatingRatMarketSaturation2 = auto()
    RuinousRatMarketSaturation2 = auto()


    #######################################################
    #                       Bone Market
    #######################################################


    # Bone Market Hack
    _BoneMarketRotation = auto()
    _FourMoreJoints = auto()
    _ReduceAmalgamy = auto()
    _ReduceAntiquity = auto()
    _ReduceMenace = auto()

    _BoneMarketMegaShoppingList1 = auto()

    # Actions
    _BoneMarketAction = auto()

    _AntiquityReptileAction = auto()
    _AntiquityAmphibianAction = auto()    
    _AntiquityBirdAction = auto()
    _AntiquityFishAction = auto()
    _AntiquityArachnidAction = auto()
    _AntiquityInsectAction = auto()
    _AntiquityPrimateAction = auto()

    _AmalgamyReptileAction = auto()
    _AmalgamyAmphibianAction = auto()    
    _AmalgamyBirdAction = auto()
    _AmalgamyFishAction = auto()
    _AmalgamyArachnidAction = auto()
    _AmalgamyInsectAction = auto()
    _AmalgamyPrimateAction = auto()

    _MenaceReptileAction = auto()
    _MenaceAmphibianAction = auto()    
    _MenaceBirdAction = auto()
    _MenaceFishAction = auto()
    _MenaceArachnidAction = auto()
    _MenaceInsectAction = auto()      
    _MenacePrimateAction = auto()      

    _AntiquityGeneralAction = auto()
    _AmalgamyGeneralAction = auto()
    _MenaceGeneralAction = auto()

    _GeneralReptileAction = auto()
    _GeneralAmphibianAction = auto()    
    _GeneralBirdAction = auto()
    _GeneralFishAction = auto()
    _GeneralArachnidAction = auto()
    _GeneralInsectAction = auto()    
    _GeneralPrimateAction = auto()    

    # Exhaustion
    GenericBoneMarketExhaustion = auto()

    AntiquityReptileExhaustion = auto()
    AntiquityAmphibianExhaustion = auto()    
    AntiquityBirdExhaustion = auto()
    AntiquityFishExhaustion = auto()
    AntiquityArachnidExhaustion = auto()
    AntiquityInsectExhaustion = auto()
    AntiquityPrimateExhaustion = auto()

    AmalgamyReptileExhaustion = auto()
    AmalgamyAmphibianExhaustion = auto()    
    AmalgamyBirdExhaustion = auto()
    AmalgamyFishExhaustion = auto()
    AmalgamyArachnidExhaustion = auto()
    AmalgamyInsectExhaustion = auto()
    AmalgamyPrimateExhaustion = auto()

    MenaceReptileExhaustion = auto()
    MenaceAmphibianExhaustion = auto()    
    MenaceBirdExhaustion = auto()
    MenaceFishExhaustion = auto()
    MenaceArachnidExhaustion = auto()
    MenaceInsectExhaustion = auto()      
    MenacePrimateExhaustion = auto()      

    AntiquityGeneralExhaustion = auto()
    AmalgamyGeneralExhaustion = auto()
    MenaceGeneralExhaustion = auto()

    GeneralReptileExhaustion = auto()
    GeneralAmphibianExhaustion = auto()    
    GeneralBirdExhaustion = auto()
    GeneralFishExhaustion = auto()
    GeneralArachnidExhaustion = auto()
    GeneralInsectExhaustion = auto()    
    GeneralPrimateExhaustion = auto()   

    #######################################################
    #                       Factions
    #######################################################

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

    # Renown
    RenownBohemians = auto()
    RenownChurch = auto()
    RenownConstables = auto()
    RenownCriminals = auto()
    RenownDocks = auto()
    RenownGreatGame = auto()
    RenownHell = auto()
    RenownRevolutionaries = auto()
    RenownRubberyMen = auto()
    RenownSociety = auto()
    RenownTombColonies = auto()
    RenownUrchins = auto()


    # Connected
    ConnectedBenthic = auto()
    ConnectedSummerset = auto()
    ConnectedTheDuchess = auto()
    ConnectedWidow = auto()

    SympatheticAboutRatlyConcerns = auto()

    SupportingTheLiberationistTracklayers = auto()
    SupportingThePrehistoricistTracklayers = auto()
    SupportingTheEmancipationistTracklayers = auto()


    #######################################################
    #                       Economy
    #######################################################

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
    CorrectiveHistoricalNarrative = auto()
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
    ShrivelledBall = auto()
    RingOfStone = auto()
    DoveMaskShard = auto()
    FragmentOfWhiteGold = auto()
    HorseheadAmulet = auto()
    RatworkMechanism = auto()

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
    LondonStreetSign = auto()
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
    JustificandeCoin = auto()
    ForgedJustificandeCoin = auto()

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
    RelicOfTheFifthCity = auto()

    # Infernal
    Soul = auto()
    AmanitaSherry = auto()
    BrilliantSoul = auto()
    MuscariaBrandy = auto()
    BrassRing = auto()
    DevilboneDie = auto()
    PortfolioOfSouls = auto()
    QueerSoul = auto()
    SilentSoul = auto()
    BrightBrassSkull = auto()
    DevilishProbabilityDistributor = auto()
    DiscordantSoul = auto()
    InfernalMachine = auto()
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
    Anticandle = auto()
    MemoryOfMoonlight = auto()

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
    MemoryOfMuchLesserSelf = auto()

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
    PanopticalSkull = auto()
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
    UnidentifiedThighBone = auto()
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
    ProscribedMaterial = auto()
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
    LegendaCosmogone = auto()

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
    TantalisingPossibility = auto()
    GlimpseOfAnathema = auto()

    # Firmament - The Stacks
    RouteTracedThroughTheLibrary = auto()
    LibraryKey = auto()
    FragmentaryOntology = auto()
    DispositionOfTheCardinal = auto()

    ################################################################################
    ###                          Equipment                                       ###
    ################################################################################

    # Weapon
    ConsignmentOfScintillackSnuff = auto()
    IntricateKifers = auto()
    InfernalSharpshootersRifle = auto()

    # Companion
    LuckyWeasel = auto()
    SulkyBat = auto()
    WinsomeDispossessedOrphan = auto()
    CheerfulGoldfish = auto()
    UntrainedLyrebird = auto()
    TalkativeRattusFaber = auto()

    # Unsorted
    BundleOfRaggedClothing = auto()
    ScarletStockings = auto()
    StormInATeacup = auto()
    FacetedDecanterOfDrownieEffluvia = auto()

    # Tools
    NotchedBoneHarpoon = auto()
    ListOfAliasesWrittenInGant = auto()
    ShrineToSaintJoshua = auto()
    SetOfCosmogoneSpectacles = auto()
    PotOfViolantInk = auto()
    CrookedCross = auto()    

    # Treasures
    KittenSizedDiamond = auto()
    FalseStarOfYourOwn = auto()

    RobeOfMrCards = auto()
    NewlyCastCrownOfTheCityOfLondon = auto()
    LeaseholdOnAllOfLondon = auto()    
    PalatialHolidayHomeInArcticCircle = auto()
    TheMarvellous = auto()

    VastNetworkOfConnections = auto()
    WingedAndTalonedSteed = auto()
    SocietyOfTheThreeFingeredHand = auto()    
    LongDeadPriestsOfRedBird = auto()

    YourLovedOneReturned = auto() # any differences?
    BloodiedTravellingCoatOfMrCups = auto()    

    # -----
    # Qualities
    # -----

    # TODO: organize this section somehow
    ScholarOfTheCorrespondence = auto()

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
    SomeoneIsComing = auto()

    # Quriks
    Austere = auto()
    Hedonist = auto()

    ################################################################
    #                        Laboratory
    ################################################################

    ExperimentalObject = auto()

    LaboratoryResearch = auto()
    ParabolanResearch = auto()

    TotalLabResearchRequired = auto()
    TotalParabolanResearchRequired = auto()  

    ParabolanMethods = auto()
    ScienceExperimentalStage = auto()

    RedScienceFocus = auto()
    CorrespondenceFocus = auto()
    ToxicologicalFocus = auto()    
    ShapelingFocus = auto()
    MonstrousFocus = auto()
    NauticalFocus = auto()
    # HerpetologicalFocus = auto()
    # IcthyologicalFocus = auto()    

    NumismaticResearch = auto()
    # AmphibianResearch = auto()
    # PiscineResearch = auto()

    NoLongerReviewingLiterature = auto()
    NoLongerFormingHypotheses = auto()
    NoLongerResupplying = auto()
    NoLongerFatigued = auto()
    NoLongerWritingUp = auto()
    NoLongerConsultingMirrors = auto()

    ResearchPreparations = auto()
    UnlikelyConnection = auto()
    UnavoidableEpiphany = auto()
    UnwiseIdea = auto()
    UnexpectedResult = auto()


    PrestigeOfYourLaboratory = auto()
    NumberOfWorkersInYourLaboratory = auto()

    ExpectedLabRewardValue = auto()

    EquipmentForScientificExperimentation = auto()

    DisgruntlementAmongStudents = auto()

    LaboratoryServicesOfLetticeTheMercy = auto()
    LaboratoryServicesOfSilkCladExpert = auto()
    LaboratoryServicesFromHephaesta = auto()

    LaboratoryServicesFromGiftedStudent = auto()
    LaboratoryServicesFromVisionaryStudent = auto()


    ExpertiseOfTheFourthCity = auto()
    ExpertiseOfTheThirdCity = auto()
    ExpertiseOfTheSecondCity = auto()
    ExpertiseOfTheFirstCity = auto()


    _HandClear = auto()

    # IDK what to call these
    Casing = auto()
    Corresponding = auto()
    Fascinating = auto()
    Inspired = auto()
    Infiltrating = auto()
    _InfiltratingLong = auto()
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

    # Hellworm
    InTheCompanyOfAHellworm = auto()
    HellwormSaddle = auto()
    DispositionOfYourHellworm = auto()
    
    # miscellaneous
    ResearchOnAMorbidFad = auto()
    ApproximateValueOfYourSkeletonInPennies = auto()
    Tribute = auto()
    HeartsGameExploits = auto()
    ApproximateValueOfOutstandingInvoicesInPennies = auto()
    HinterlandProsperity = auto()
    HidingPlaceOfAPeculiarItem = auto()
    _WaswoodHeistCashOut = auto()
    _ApproximateEchoValue = auto()
    _SkeletonPennyValue = auto()

    TracklayersDispleasure = auto()

    ColourAtTheChessboard = auto()

    SeeingThroughTheEyesOfIcarus = auto()
    WalkingTheFallingCities = auto()

    # Piracy
    ChasingDownYourBounty = auto()
    StashedTreasure = auto()
    UnwelcomeOnTheWaters = auto()
    TimeSpentAtZee = auto()
    CreepingFear = auto()
    RosyColours = auto()

    # Upper River
    TrainDefences = auto()    
    TrainLuxuries = auto()    
    TrainBaggageAccomodations = auto()

    EalingGardensCommemorativeDevelopment = auto()
    JerichoLocksCommemorativeDevelopment = auto()
    MagistracyOfEvenlodeCommemorativeDevelopment = auto()
    BalmoralCommemorativeDevelopment = auto()
    BurrowInfraMumpCommemorativeDevelopment = auto()
    MoulinCommemorativeDevelopment = auto()
    StationVIIICommemorativeDevelopment = auto()
    HurlersCommemorativeDevelopment = auto()
    MarigoldCommemorativeDevelopment = auto()

    EalingGardensDarkness = auto()
    JerichoLocksDarkness = auto()
    MagistracyOfEvenlodeDarkness = auto()
    BalmoralDarkness = auto()
    BurrowInfraMumpDarkness = auto()
    MoulinDarkness = auto()
    StationVIIIDarkness = auto()
    HurlersDarkness = auto()
    MarigoldDarkness = auto()

    FittingInAtHeliconHouse = auto()
    TimeRemainingAtHeliconHouseTwoThruFive = auto()
    TimeRemainingAtHeliconHouseExactlyOne = auto()

    PalaeontologicalDiscovery = auto()
    EsteemOfTheGuild = auto()
    WagesOfADig = auto()

    Moonlit = auto()

    _CoverTiesGeneric = auto()
    CoverTiesSurface = auto()
    CoverTiesBazaar = auto()
    CoverTiesDispossessed = auto()

    CoverElaboration = auto()
    CoverNuance = auto()
    CoverWitnessnes = auto()
    CoverCredentials = auto()
    CoverBackstory = auto()

    PaintersProgress = auto()
    CompletedPainting = auto()
    _UnveilYourPaintingLondon = auto()
    PresentYourPaintingInHeliconHouse = auto()

    PaintingIncendiary = auto()
    PaintingLuminosity = auto()
    PaintingNostalgic = auto()
    _PaintingAnyQuality = auto()

    MonographCautionary = auto()
    MonographTragic = auto()
    MonographIronic = auto()

    DiscordantLaw = auto()
    CrystallisedCurio = auto()

    TheMindsAscent1 = auto()
    TheMindsAscent2 = auto()
    TheMindsAscent3 = auto()

    # Roof
    _RandomRoofEvent = auto()

    # ----- Psuedo Items
    _VisitFromTimeTheHealer = auto()

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

    # Location stuff
    _WakefulEyeRoundTrip = auto()
    _LondonKhanateRoundTrip = auto()
    _LondonSeaOfVoicesRoundTrip = auto()
    _UpperRiverRoundTrip = auto()
    _FirmamentRoundTrip = auto()

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
    PiecesOfPlunder = auto()
    SilentStalker = auto()
    UnaccountablyPeckish = auto()
    GroaningHull = auto()
    MutinousWhispers = auto()
    RumblingStomachs = auto()
    PageOfCryptopalaeontologicalNotes = auto()
    PageOfPrelapsarianArchaeologicalNotes = auto()
    PageOfTheosophisticalNotes = auto()
    DirectionsToAHiddenStash = auto()
    NorthernWind = auto()
    SouthernWind = auto()
    EasternWind = auto()
    ZeeLegs = auto()
    TendingTheColossus = auto()

    Fake_HiddenStash = auto()
    _AgentInTransit = auto()
    _UnassumingCratePickup = auto()
    _TriflingDiplomatSale = auto()

    _PullingThreads1 = auto()
    _PullingThreads2 = auto()
    _PullingThreads3 = auto()
    _PullingThreads4 = auto()
    _PullingThreads5 = auto()
    _PullingThreads6 = auto()
    _PullingThreads7 = auto()
    _PullingThreads8 = auto()
    _PullingThreads9 = auto()
    _PullingThreads10 = auto()
    _PullingThreads11 = auto()
    
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
 
    _LondonDraw = auto()
    
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

    # Simulation scratchpad

    # Heists
    PlanningAHeist = auto()
    TargetSecurity = auto()
    BurglarsProgress = auto()
    IntriguingKey = auto()
    InsideInformation = auto()
    CatlikeTread = auto()
    EscapeRoute = auto()

    _WellPlannedVillainy16Casing = auto()
    _BigRat9Casing = auto()
    _Parabolan28Casing = auto()
    _Heist15Casing = auto()
    _SuccesfulHeist = auto()
    _AllianceWithBigRat = auto()
    _ImprisonedInNewNegate = auto()

FAVOUR_ITEMS = [
    Item.FavBohemians,
    Item.FavChurch,
    Item.FavConstables,
    Item.FavCriminals,
    Item.FavDocks,
    Item.FavGreatGame,
    Item.FavHell,
    Item.FavRevolutionaries,
    Item.FavRubberyMen,
    Item.FavSociety,
    Item.FavTombColonies,
    Item.FavUrchins
]

RENOWN_ITEMS = [
    Item.RenownBohemians,
    Item.RenownChurch,
    Item.RenownConstables,
    Item.RenownCriminals,
    Item.RenownDocks,
    Item.RenownGreatGame,
    Item.RenownHell,
    Item.RenownRevolutionaries,
    Item.RenownRubberyMen,
    Item.RenownSociety,
    Item.RenownTombColonies,
    Item.RenownUrchins
]

BONE_MARKET_ACTIONS = [
    Item._BoneMarketAction,
    
    Item._AntiquityReptileAction,
    Item._AntiquityAmphibianAction,    
    Item._AntiquityBirdAction,
    Item._AntiquityFishAction,
    Item._AntiquityArachnidAction,
    Item._AntiquityInsectAction,
    Item._AntiquityPrimateAction,

    Item._AmalgamyReptileAction,
    Item._AmalgamyAmphibianAction,    
    Item._AmalgamyBirdAction,
    Item._AmalgamyFishAction,
    Item._AmalgamyArachnidAction,
    Item._AmalgamyInsectAction,
    Item._AmalgamyPrimateAction,

    Item._MenaceReptileAction,
    Item._MenaceAmphibianAction,    
    Item._MenaceBirdAction,
    Item._MenaceFishAction,
    Item._MenaceArachnidAction,
    Item._MenaceInsectAction,      
    Item._MenacePrimateAction,      

    Item._AntiquityGeneralAction,
    Item._AmalgamyGeneralAction,
    Item._MenaceGeneralAction,

    Item._GeneralReptileAction,
    Item._GeneralAmphibianAction,    
    Item._GeneralBirdAction,
    Item._GeneralFishAction,
    Item._GeneralArachnidAction,
    Item._GeneralInsectAction,    
    Item._GeneralPrimateAction,    
]

RAT_MARKET_SATURATION_1_TYPES = [
    Item.SoftRatMarketSaturation1,
    Item.SaintlyRatMarketSaturation1,
    Item.MaudlinRatMarketSaturation1,
    Item.InscrutableRatMarketSaturation1,
    Item.TempestuousRatMarketSaturation1,
    Item.IntricateRatMarketSaturation1,
    Item.CalculatingRatMarketSaturation1,
    Item.RuinousRatMarketSaturation1,
]

RAT_MARKET_SATURATION_2_TYPES = [
    Item.SoftRatMarketSaturation2,
    Item.SaintlyRatMarketSaturation2,
    Item.MaudlinRatMarketSaturation2,
    Item.InscrutableRatMarketSaturation2,
    Item.TempestuousRatMarketSaturation2,
    Item.IntricateRatMarketSaturation2,    
    Item.CalculatingRatMarketSaturation2,
    Item.RuinousRatMarketSaturation2,
]

SPECIAL_ACTION_TYPES = [
    Item._EalingAction,
    Item._JerichoAction,
    Item._BalmoralAction,
    Item._StationViiiAction,
    Item._BurrowAction,
    Item._MoulinAction,
    Item._HurlersAction,
    Item._MarigoldAction,

    Item._HeliconAction,
    Item._WakefulEyeAction,
    Item._KhanateAction,
    Item._SeaOfVoicesAction,
    Item._PortCecilAction,
    Item._MangroveAction,

    Item._HallowsThroatAction,
    Item._MidnightMoonAction,
    Item._ZenithAction,
]

BASIC_STATS = [
    Item.Watchful,
    Item.Shadowy,
    Item.Dangerous,
    Item.Persuasive,
]

ADVANCED_STATS = [
    Item.KatalepticToxicology,
    Item.MonstrousAnatomy,
    Item.APlayerOfChess,
    Item.Glasswork,
    Item.ArtisanOfTheRedScience,
    Item.Mithridacy,

    Item.ShapelingArts,
    Item.Zeefaring,

    Item.StewardOfTheDiscordance,
    Item.Chthonosophy,    
]

BDR_STATS = [
    Item.Respectable,
    Item.Dreaded,
    Item.Bizarre,
]

DEFENSIVE_STATS = [
    Item.Inerrant,
    Item.Insubstantial,
    Item.Neathproofed ,
]

ALL_STATS = BASIC_STATS + ADVANCED_STATS + BDR_STATS + DEFENSIVE_STATS

MENACE_REDUCTION_QUALITIES = [
    Item._WoundsReduction,
    Item._NightmaresReduction,
    Item._ScandalReduction,
    Item._SuspicionReduction,
]