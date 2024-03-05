import numbers
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix
from scipy.optimize import linprog
from enum import Enum, auto
from itertools import count

import numpy as np
import pprint

# Important Parameters
# actions doesn't matter on its own until I add some weekly+ stuff
actions_per_day = 120.0
# cards_seen_per_day = 96.0
cards_seen_per_day = 0

# placeholder for upconversions and stuff
# if anyone knows the real values please share
default_rare_success_rate = 0.05

# maybe improve slightly with EPA
zailing_epa = 3.2

# lab research per action
# somewhat optimistic
lab_rpa = 33

# for modeling actions that can grant more actions
# eg. the 30% success on the aunt card
replacement_epa = 6.5

# for modeling time spent outside london
replacement_good_card_density = 0.33

# 0.85, 0.74, 0.65
wounds_multiplier = 1.0
scandal_multiplier = 1.0
suspicion_multiplier = 1.0
nightmares_multiplier = 1.0


# Custom Player Stuff
# class ZeeRegion(Enum):
#     HomeWaters = auto()
#     ShepherdsWash = auto()

class Location(Enum):
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

class Rarity(Enum):
    Rare = 10
    Unusual = 20
    VeryInfrequent = 50
    Infrequent = 80
    Standard = 100
    Frequent = 200
    Abundant = 500
    Ubiquitous = 1000

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

class Ambition(Enum):
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
    Echo = 0

    Action = 1
    CardDraws = 2 # Fake item
    # DayOfCardDraws = 3 # Fake item

    # Menaces
    Wounds = auto()
    Scandal = auto()
    Suspicion = auto()
    Nightmares = auto()
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

    # Academic
    FoxfireCandleStub = auto()
    FlaskOfAbominableSalts = auto()
    MemoryOfDistantShores = auto()
    IncisiveObservation = auto()
    UnprovenancedArtefact = auto()
    VolumeOfCollatedResearch = auto()
    LostResearchAssistant = auto()

    # Curiosity
    StrongBackedLabour = auto()
    WhirringContraption = auto()
    OilOfCompanionship = auto()
    CracklingDevice = auto()
    ConcentrateOfSelf = auto()
    CounterfeitHeadOfJohnTheBaptist = auto()

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
    BrilliantSoul = auto()
    BrightBrassSkull = auto()
    QueerSoul = auto()

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

    # -----
    # Equipment
    # -----

    # Weapon
    ConsignmentOfScintillackSnuff = auto()

    # Companion
    SulkyBat = auto()
    WinsomeDispossessedOrphan = auto()

    # -----
    # Qualities
    # -----

    # TODO: organize this section somehow

    AConsequenceOfYourAmbition = auto()
    BraggingRightsAtTheMedusasHead = auto()

    HeartsGameExploits = auto()

    # Laboratory
    LaboratoryResearch = auto()
    ParabolanResearch = auto()

    Infiltrating = auto()

    ResearchOnAMorbidFad = auto()
    
    Tribute = auto()

    # Piracy
    ChasingDownYourBounty = auto()
    StashedTreasure = auto()

    # Upper River
    PalaeontologicalDiscovery = auto()
    EsteemOfTheGuild = auto()

    # ----- Psuedo Items
    VisitFromTimeTheHealer = auto()
    PortCecilCycles = auto()
    TimeAtJerichoLocks = auto()
    TimeAtWakefulCourt  = auto() # tribute grind
    ZailingDraws = auto() # self-explanatory
    SlightedAcquaintance = auto() # newspaper
    ParabolaRoundTrip = auto()

    ArbitraryPlaceholderItem = auto()

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

    # --- Bone Market Recipes
    ThreeLeggedMammoth = auto()
    MammothOfTheSky = auto()
    MammothOfTheDeep = auto()
    SpiderPope = auto()
    PrismaticWalrus = auto()
    MammothTheHedgehog = auto()
    WoolyGothmother = auto()

def pyramid(n): return n * (n+1) / 2

def per_day(exchanges):
    n = next(counter)
    b[n] = 1
    for item, value in exchanges.items():
        A[n, item.value] = value

def trade(actionCost, exchanges):
    n = next(counter)
    b[n] = 0
    A[n, Item.Action.value] = -1 * actionCost
    for item, value in exchanges.items():
        A[n, item.value] = value

def card(name, freq, isGood, exchanges):
    global LondonDeckSize
    global GoodCardsInDeck
    LondonDeckSize += freq.value
    if isGood:
        GoodCardsInDeck += freq.value
        for item, value in exchanges.items():
            LondonCardsByItem[item.value] += (value * freq.value)

def railway_card(name, freq, isGood, exchanges):
    # dummy alias for now
    trade(1, exchanges)

# hack
var_buffer = 1000
num_items = max(Item, key=lambda x: x.value).value
num_vars = num_items + 1 + var_buffer

A = lil_matrix((num_vars, num_vars))

b = [1]*num_vars
counter = count(start=-1)

bounds = [(0, None) for _ in range(num_vars)]

# in practice it seems this rarely affects the output, but it makes me feel better
# I don't know if this even works the way I think it does as far as modeling long-term stockpiling
# but if you set it too low, you will lock out certain trades
# eg setting the upper bound of Bohemian favours to 3 will lock out the Jericho option
# so really it's a source of bugs more than anything else
# still keeping it in

# menace bounds actually a little higher since you can overflow
# also should maybe have negative bound, since menace reduction is usually a side-effect rather than a cost
# tried setting it to (-100, 36) and EPA went down slightly so who the heck knows
bounds[Item.Wounds.value] = (0, 36)
bounds[Item.Scandal.value] = (0, 36)
bounds[Item.Suspicion.value] = (0, 36)
bounds[Item.Nightmares.value] = (0, 36)
bounds[Item.SeeingBanditryInTheUpperRiver.value] = (0, 36)

bounds[Item.ConnectedBenthic.value] = (0, 800)

bounds[Item.Tribute.value] = (0, 260)
bounds[Item.TimeAtWakefulCourt.value] = (0, 13)
bounds[Item.TimeAtJerichoLocks.value] = (0, 5)

bounds[Item.FavBohemians.value] = (0, 7)
bounds[Item.FavChurch.value] = (0, 7)
bounds[Item.FavConstables.value] = (0, 7)
bounds[Item.FavCriminals.value] = (0, 7)
bounds[Item.FavDocks.value] = (0, 7)
bounds[Item.FavGreatGame.value] = (0, 7)
bounds[Item.FavHell.value] = (0, 7)
bounds[Item.FavRevolutionaries.value] = (0, 7)
bounds[Item.FavRubberyMen.value] = (0, 7)
bounds[Item.FavSociety.value] = (0, 7)
bounds[Item.FavTombColonies.value] = (0, 7)
bounds[Item.FavUrchins.value] = (0, 7)

bounds[Item.ResearchOnAMorbidFad.value] = (0, 6)

# for card averages
LondonDeckSize = 0
GoodCardsInDeck = 0
LondonCardsByItem = [0] * num_vars


# Player Stuff
    
profession = Profession.NoProfession
treasure = Treasure.NoTreasure
player_location = Location.MolochStreet


# ---------------- Trades ----------------------------

# Plug in the basic economic contraints

per_day({
    Item.Action: actions_per_day,
    Item.CardDraws: cards_seen_per_day,
    Item.VisitFromTimeTheHealer: 1/7
})

trade(0, {
    Item.VisitFromTimeTheHealer: -1,
    # Item.AConsequenceOfYourAmbition: 1
})

# ambition_reward = rewards_of_ambition(treasure)
# ambition_reward[Item.AConsequenceOfYourAmbition] = -4
# trade(1, ambition_reward)

#  ██████╗ ██████╗ ██████╗     ██████╗ ███████╗ ██████╗██╗  ██╗
# ██╔═══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔════╝██╔════╝██║ ██╔╝
# ██║   ██║██████╔╝██████╔╝    ██║  ██║█████╗  ██║     █████╔╝ 
# ██║   ██║██╔═══╝ ██╔═══╝     ██║  ██║██╔══╝  ██║     ██╔═██╗ 
# ╚██████╔╝██║     ██║         ██████╔╝███████╗╚██████╗██║  ██╗
#  ╚═════╝ ╚═╝     ╚═╝         ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝

# ----------------------
# --- Cards: Lodgings
# ----------------------

# Lair in the Marshes
card("Lair in the Marshes", Rarity.Standard, True, {
    Item.FavSociety: 1,
    Item.CertifiableScrap: 1,
    Item.Nightmares: 1 * nightmares_multiplier
})

# The Tower of Knives: Difficulties at a Smoky Flophouse
# The next victim?
card("The Tower of Knives", Rarity.Standard, True, {
    Item.FavCriminals: 0.5 - default_rare_success_rate / 2.0,
    Item.FavRevolutionaries: 0.5 - default_rare_success_rate / 2.0,
    Item.AeolianScream: default_rare_success_rate
})

# The Tower of Eyes: Behind Closed Doors at a Handsome Townhouse
# scandalous party
card("The Tower of Eyes", Rarity.Frequent, True, {
  Item.FavBohemians: 0.5,
  Item.FavSociety: 0.5,
  Item.Scandal: 2 * scandal_multiplier
})

# The Tower of Sun and Moon: a Reservation at the Royal Bethlehem Hotel
card("Royal Beth lodings", Rarity.Frequent, False, {
    Item.CertifiableScrap: 3
})

# -----------------------------------------------------
# --- Cards: Companions
# ----------------------------------------------------

card("What will you do with your [connected pet]?", Rarity.Standard, True, {
    Item.FavBohemians: 1
})

# With Bewildering Procession
card("Attend to your spouses", Rarity.VeryInfrequent, True, {
    Item.FavBohemians: 1
})

# -----------------------------------------------------
# --- Cards: Other Equipment
# ----------------------------------------------------

# avoidable
card("A day out in your Clay Sedan Chair", Rarity.Standard, True, {
    Item.FavSociety: 1
})

# # avoidable? A: yes, with watchful gains
# card("Riding your Velocipede", Rarity.Standard, False, {
#     Item.ManiacsPrayer: -5,
#     Item.FavConstables: 1
# })

# -----------------------------------------------------
# --- Cards: Clubs
# ----------------------------------------------------

# # Sophia's
# # Can also be Tomb-Colony favour, maybe 50/50?
# card("Club: Sophia's", Rarity.Standard, True, {
#     Item.RumourOfTheUpperRiver: -5,
#     Item.PieceOfRostygold: 1500,
#     Item.JetBlackStinger: 5
# })

card("More Larks with the Young Stags", Rarity.Standard, True, {
    # Item.PieceOfRostygold: -500,
    Item.Echo: -5, # everyone has rostygold
    Item.FavSociety: 2,
    Item.FavBohemians: 1
})

# -----------------------------------------------------
# --- Cards: Dreams
# ----------------------------------------------------

# Not sure how to model this? Can they be locked out of altogether?
# Or just have one card for each of the four
# Guessing at rarity for the red cards

# card("A dream about a clouded place", Rarity.Unusual, {
#     # TODO
# })

# assuming you end up with 5 and they are all Unusual
card("omni-Dreams placeholder card", Rarity.Standard, False, {
    # TODO
})

# -----------------------------------------------------
# --- Cards: Factions
# ----------------------------------------------------

# Bohemians
card("Bohemians Faction", Rarity.Standard, True, {
    Item.Echo: -1.2,
    Item.FavBohemians: 1
})

# Church
card("Church Faction", Rarity.Standard, True, {
    Item.Echo: -0.1,
    Item.FavChurch: 1
})

# Constables
card("Constables Faction", Rarity.Standard, False, {
    Item.Echo: -0.1,
    Item.FavConstables: 1
})

# Criminals
card("Criminals Faction", Rarity.Standard, True, {
    Item.Suspicion: 1 * suspicion_multiplier,
    Item.FavCriminals: 1,
})

# Docks
card("Docks Faction", Rarity.Standard, True, {
    Item.Echo: -0.1,
    Item.FavDocks: 1
})

# GreatGame
card("Great Game Faction", Rarity.Standard, False, {
    Item.Wounds: 1 * wounds_multiplier,
    Item.FavGreatGame: 1
})

# Hell
card("Burning Shadows: the Devils of London", Rarity.Standard, False, {
    Item.Scandal: 1 * scandal_multiplier,
    Item.FavHell: 1
})

# Revolutionaries
card("Rev Faction", Rarity.Standard, False, {
    Item.Echo: -0.5,
    Item.FavRevolutionaries: 1 
})

# RubberyMen
card("Rubbery Faction", Rarity.Standard, False, {
    Item.Echo: -0.1,
    Item.FavRubberyMen: 1
})

# Society
card("Society Faction", Rarity.Standard, True, {
    Item.Echo: -0.5,
    Item.FavSociety: 1
})

# Tomb-Colonies
card("Tomb Colonies Faction", Rarity.Standard, False, {
    Item.FavTombColonies: 1
})

# # Urchins
# card("Urchins Faction", Rarity.Standard, False, {
#     Item.Echo: -0.4, # 1x lucky weasel
#     Item.FavUrchins: 1
# })

# With HOJOTOHO ending
card("Urchins Faction", Rarity.Standard, True, {
    Item.FavUrchins: 1,
    Item.Nightmares: -2
})

# ----------------------
# --- Cards: General London
# ----------------------

# A tournament of weasels
card("A tournament of weasels", Rarity.Unusual, False, {
    # TODO
})

# Nightmares >= 1
card("Orthographic Infection", Rarity.Standard, False, {
    # TODO
})

# FavBohe >= 1
card("City Vices: A rather decadent evening", Rarity.Standard, False, {
    # TODO
})

# Wounds >= 2
card("A Restorative", Rarity.Standard, False, {
    # TODO
})

# Scandal >= 2
# > an afternoon of mischief
card("An Afternoon of Good Deeds", Rarity.Standard, False, {
    Item.FavHell: 1,
    ## TODO
    # Item.ConfidentSmile: 1,
    # Item.JadeFragment: 10
})

# Nightmares >= 3
card("A Moment's Peace", Rarity.VeryInfrequent, False, {
    # TODO
})

# Nightmares >= 3
# Publish => War-games
# With testing, slightly lowers EPA
card("The interpreter of dreams", Rarity.Unusual, False, {
    # Success
    Item.Nightmares: -5 * 0.6,
    Item.FavGreatGame: 1 * 0.6,

    # Failure
    Item.Scandal: 1 * 0.4 * scandal_multiplier
})

card("An implausible penance", Rarity.Standard, False, {
    # TODO
})

# > Rependant forger
card("A visit", Rarity.Standard, True, {
    Item.CrypticClue: 230, # base shadowy,
    Item.FavBohemians: 1,
    Item.FavCriminals: 1
})

# > Entertain a curious crowd
card("The seekers of the garden", Rarity.Standard, False, {
    Item.ZeeZtory: -7,
    Item.FavBohemians: 1,
    Item.FavDocks: 0.5,
    Item.FavSociety: 0.5
})

card("devices and desires", Rarity.Standard, False, {
    # TODO
})


card("A Polite Invitation", Rarity.Standard, False, {
    # TODO: Separate entry for party carousel
})

card("Give a Gift!", Rarity.Standard, False, {
    # TODO
})

# > A disgraceful spectacle
card("A day at the races", Rarity.Standard, True, {
    Item.FavChurch: 1
})

# Avoidable!
# Sulky Bat >= 1
card("A parliament of bats", Rarity.Standard, False, {
    Item.VisionOfTheSurface: -1,
    Item.FavGreatGame: 1
})

card("One's public", Rarity.Standard, False, {
    # TODO    
})

card("A Day with God's Editors", Rarity.Standard, False, {
    Item.TaleOfTerror: -1,
    Item.FavChurch: 1
})

# Avoidable? unsure
card("Bringing the revolution", Rarity.Standard, False, {
    Item.CompromisingDocument: -1,
    Item.FavRevolutionaries: 1
})

# Time limited, also lots of good options?
# Maybe just leave it out?
# card("The Calendrical Confusion of 1899", Rarity.Standard, True, {
#     Item.ScrapOfIncendiaryGossip: 14
# })

card("Mirrors and Clay", Rarity.Standard, False, {
    # TODO
})

card("The Cities that Fell", Rarity.Standard, False, {
    # TODO
})

card("The Soft-Hearted Widow", Rarity.Standard, False, {
    # TODO
})

card("All fear the overgoat!", Rarity.Standard, False, {
    # TODO
})

card("The Northbound Parliamentarian", Rarity.Standard, False, {
    # TODO
})

card("A Dream of Roses", Rarity.Standard, False, {
    # TODO
})

card("Weather at last", Rarity.Standard, False, {
    # TODO
})

card("An unusual wager", Rarity.Standard, False, {
    # TODO
})

card("Mr Wines is holding a sale!", Rarity.Standard, False, {
    # TODO
})

card("The awful temptation of money", Rarity.Standard, False, {
    # TODO
})

# not sure if this can be avoided
card("Investigation the Affluent Photographer", Rarity.Standard, False, {
    # TODO
})

card("The Geology of Winewound", Rarity.Standard, False, {
    # TODO
})

# > Ask her about the sudden influx of bones
# Debatable whether this one is "good"
card("A Public Lecture", Rarity.Standard, False, {
    Item.CrypticClue: 100
    # also RoaMF for newspaper grind
})

# # avoidable with no Favours: Hell
# card("A consideration for services rendered", Rarity.Standard, {
#     # TODO
# })

card("Wanted: Reminders of Brighter Days", Rarity.Standard, False, {
    # TODO
})

# notability >= 1
card("An Unsigned Message", Rarity.VeryInfrequent, False, {
    # TODO
})

card("A Presumptuous Little Opportunity", Rarity.VeryInfrequent, False, {
    # TODO
})

card("A visit from slowcake's amanuensis", Rarity.Infrequent, False, {
    # TODO
})

# Shadowy >= 69, Renown Crims >= 20
card("A merry sort of crime", Rarity.VeryInfrequent, True, {
    Item.FavCriminals: 1
})

card("A dusty bookshop", Rarity.Rare, False, {
    # TODO
})

card("A little omen", Rarity.Rare, False, {
    # TODO
})

card("A disgraceful spectacle", Rarity.Rare, True, {
    Item.Echo: 12.5
})

card("A voice from a well", Rarity.Rare, False, {
    # TODO
})

card("A fine day in the flit", Rarity.Unusual, False, {
    # TODO
})

card("The Paranomastic Newshound", Rarity.Unusual, False, {
    # TODO
})

# ----------------------
# --- Cards: Relickers
# ----------------------

card("The curt relicker and montgomery are moving quietly past",
     Rarity.VeryInfrequent, False, {
         # TODO
     })

card("The Capering Relicker and Gulliver are outside in the street",
     Rarity.VeryInfrequent, False, {
         # TODO
     })

card("The Shivering Relicker and Pinnock are trundling by",
     Rarity.VeryInfrequent, False, {
         # TODO
     })

card("The Coquettish Relicker and Mathilde are making the rounds",
     Rarity.VeryInfrequent, False, {
         # TODO
     })

# ----------------------
# --- Cards: FATE-locked
# ----------------------

card("A Trade in Souls card", Rarity.Standard, True, {
    Item.Echo: -4, # 50 souls + 5 contracts
    Item.FavConstables: 1,
    Item.FavChurch: 1,
    Item.FavSociety: 1
})

# Society ending since that's what I have
# probably the best of the aunt-bitions anyway
card("The OP Aunt card", Rarity.Standard, True, {
    Item.BottleOfGreyfields1882: -50,

    # 0.7 Failure
    Item.FavSociety: 1 * 0.7,
    Item.ScrapOfIncendiaryGossip: 3 * 0.7,
    Item.InklingOfIdentity: 5 * 0.7,
    Item.Scandal: -2 * 0.7,
    
    # 0.3 success
    Item.Echo: 10 * replacement_epa * 0.3
})


# ----------------------
# --- Cards: Location-specific
# ----------------------

# so far no special location is positive EPA
# but these have potential 

# if (player_location == Location.BazaarSideStreet):
#     card("The Skin of the Bazaar", Rarity.Rare, False, {

#     })

if (player_location == Location.LadybonesRoad):
    card("1000 Nevercold Brass Silver Wanted!", Rarity.Standard, True, {
        Item.NevercoldBrassSliver: -1000,
        Item.CrypticClue: 500,
        Item.AppallingSecret: 10,
        Item.FavGreatGame: 1
    })

if (player_location == Location.Spite):
    card("2000 Foxfire Candles Wanted!", Rarity.Standard, True, {
        Item.FoxfireCandleStub: -2000,
        Item.PieceOfRostygold: 2000,
        Item.MysteryOfTheElderContinent: 1,
        Item.FavChurch: 1
    })

if (player_location == Location.TheUniversity):
    card("A peculiar practice", Rarity.Standard, True, {
        # Item.ConnectedSummerset: -5 # ignoring for now
        Item.FavTombColonies: 1,
        Item.Echo: 0.6 # bundle of oddities
    })

    card("Stone by stone", Rarity.Standard, False, {

    })

if (player_location == Location.YourLodgings):
    card("A commotion above", Rarity.Rare, False, {
        
    })    

    card("The Neath's Mysteries", Rarity.Standard, False, {
        
    })

    card("The Urchin and the Monkey", Rarity.VeryInfrequent, True, {
        Item.CompromisingDocument: -2,
        Item.FavUrchins: 1
    })

    card("Your Grubby Urchin is becoming troublesome", Rarity.VeryInfrequent, True, {
        Item.TaleOfTerror: -2,
        Item.FavUrchins: 1
    })    



# # TODO: check the actual rarity of this
# # also it adds that other rare card to the deck that clears all wounds
# card("Slavering Dream Hound", Rarity.Unusual, True, {
#     Item.DropOfPrisonersHoney: 200
# })


#  ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ██╗     
# ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗██║     
# ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║██║     
# ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║██║     
# ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║███████╗
#  ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                                                           

## ------------------------------
## -------- Menace Stuff --------
## ------------------------------

# Social Actions, ignoring the cost to the other party
# Better options for Scandal and Suspicion exist @ -6 (dupe/betrayal) but those have a weekly limit

trade(1, {
    Item.Wounds: -6
})

trade(1, {
    Item.Scandal: -5
})

trade(1, {
    Item.Suspicion: -5
})

trade(1, {
    Item.Nightmares: -6
})

# Not a real action, represents the fact that menace reduction is a side effect rather than a cost
# otherwise we might miss a grind that's net negative on a given menace

trade(1, {
    Item.Wounds: 10
})

trade(1, {
    Item.Scandal: 10
})

trade(1, {
    Item.Suspicion: 10
})

trade(1, {
    Item.Nightmares: 10
})

## -----------------------
## --- Selling to Bazaar
## ----------------------

# Academic
trade(0, {
    Item.MemoryOfDistantShores: -1,
    Item.Echo: 0.5
})

trade(0, {
    Item.IncisiveObservation: -1,
    Item.Echo: 0.5
})

trade(0, {
    Item.UnprovenancedArtefact: -1,
    Item.Echo: 2.5
})


# Cartography ------

trade(0, {
    Item.ShardOfGlim: -1,
    Item.Echo: 0.01
})

trade(0, {
    Item.MapScrap: -1,
    Item.Echo: 0.10
})

trade(0, {
    Item.ZeeZtory: -1,
    Item.Echo: 0.5
})

trade(0, {
    Item.PartialMap: -1,
    Item.Echo: 2.5
})

trade(0, {
    Item.PuzzlingMap: -1,
    Item.Echo: 12.5
})

trade(0, {
    Item.SaltSteppeAtlas: -1,
    Item.Echo: 62.5
})

trade(0, {
    Item.RelativelySafeZeeLane: -1,
    Item.Echo: 62.5
})

trade(0, {
    Item.SightingOfAParabolanLandmark: -1,
    Item.Echo: 0.1
})

trade(0, {
    Item.VitreousAlmanac: -1,
    Item.Echo: 12.5
})

trade(0, {
    Item.OneiromanticRevelation: -1,
    Item.Echo: 62.5
})

trade(0, {
    Item.ParabolanParable: -1,
    Item.Echo: 312.5
})

trade(0, {
    Item.CartographersHoard: -1,
    Item.Echo: 312.5
})

# Currency ------
trade(0, {
    Item.HinterlandScrip: -1,
    Item.Echo: 0.5
})

# Elder ---------

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
    Item.SilveredCatsClaw: -1,
    Item.Echo: 0.10
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
trade(0, {
    Item.CompromisingDocument: -1,
    Item.Echo: 0.5
})

trade(0, {
    Item.FavourInHighPlaces: -1,
    Item.Echo: 1
})

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

trade(0, {
    Item.LumpOfLamplighterBeeswax: -1,
    Item.Echo: 0.01
})

trade(0, {
    Item.PhosphorescentScarab: -1,
    Item.Echo: 0.10
})

trade(0, {
    Item.MemoryOfLight: -1,
    Item.CrypticClue: 25
})

trade(0, {
    Item.LumpOfLamplighterBeeswax: -1,
    Item.Echo: 0.01
})

trade(0, {
    Item.MourningCandle: -1,
    Item.Echo: 2.5
})

# Mysteries ---------

trade(0, {
    Item.CrypticClue: -1,
    Item.Echo: 0.02
})

trade(0, {
    Item.JournalOfInfamy: -1,
    Item.Echo: 0.5
})

trade(0, {
    Item.TaleOfTerror: -1,
    Item.Echo: 0.5
})

trade(0, {
    Item.ExtraordinaryImplication: -1,
    Item.Echo: 2.5
})

trade(0, {
    Item.UncannyIncunabulum: -1,
    Item.Echo: 12.50
})


# Nostalgia
trade(0, {
    Item.Echo: -0.04,
    Item.DropOfPrisonersHoney: 1
})

trade(0, {
    Item.RomanticNotion: -1,
    Item.Echo: 0.10
})

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

# Rumour ---------------------

trade(0, {
    Item.ScrapOfIncendiaryGossip: -1,
    Item.Echo: 0.5
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
    Item.Echo: -0.04,
    Item.BottleOfGreyfields1882: 1
})


# Equipment
trade(0, {
    Item.SulkyBat: -1,
    Item.Echo: 0.2
})

## --------------------------------------
## ----------- Connected
## --------------------------------------

# Benthic
trade(3, {
    Item.Echo: -3,
    Item.ConnectedBenthic: 75
})

## -------------------------
## Innate Item Conversions
## -------------------------

# ----- Academic
trade(1, {
    Item.MemoryOfDistantShores: -50,
    Item.ConnectedBenthic: -5,
    Item.VolumeOfCollatedResearch: 10,
    Item.CrypticClue: 50 * (0.6 - default_rare_success_rate),
    Item.UncannyIncunabulum: 2 * default_rare_success_rate
})

# requires urchin war active
# also other items hard to model
trade(1, {
    Item.LostResearchAssistant: -1,
    Item.Echo: 12.5 # blackmail material x1
})

# ----- Mysteries
# Journals to Implications @ 50:10
trade(1,{
    Item.JournalOfInfamy: -50,
    Item.ConnectedBenthic: -5,
    Item.ExtraordinaryImplication: 10,
    Item.ShardOfGlim: 100 * (0.6 - default_rare_success_rate),
    Item.StormThrenody: 2 * default_rare_success_rate
})

# # Implications to Incunabula @ 25:5
trade(1, {
    Item.ExtraordinaryImplication: -25,
    Item.ConnectedBenthic: -20,
    Item.UncannyIncunabulum: 5,
    Item.NevercoldBrassSliver: 200 * (0.6 - default_rare_success_rate),
    Item.Echo: 62.5 * default_rare_success_rate # Nodule of Pulsating Amber
})

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

# with SotD 13, not currently achievable, 16 * 38 => 608 confessions
trade(2+16+1, {
    Item.MountainSherd: 1,
    Item.ShardOfGlim: 80
})

## ------------
## Rat Market
## ------------

trade(0, {
    Item.RatShilling: -10,
    Item.Echo: 1
})


# Crow-Crease Cryptics

trade(0, {
    Item.RatShilling: -1,
    Item.InklingOfIdentity: 1
})

trade(0, {
    Item.RatShilling: -1,
    Item.ManiacsPrayer: 1
})

trade(0, {
    Item.RatShilling: -2,
    Item.AppallingSecret: 1
})

trade(0, {
    Item.RatShilling: -7,
    Item.CompromisingDocument: 1
})

trade(0, {
    Item.RatShilling: -7,
    Item.CorrespondencePlaque: 1
})

trade(0, {
    Item.RatShilling: -7,
    Item.JournalOfInfamy: 1
})

trade(0, {
    Item.RatShilling: -7,
    Item.TaleOfTerror: 1
})

trade(0, {
    Item.RatShilling: -50,
    Item.TouchingLoveStory: 1
})

trade(0, {
    Item.RatShilling: -1000,
    Item.BlackmailMaterial: 1
})

# Tier 4

trade(0, {
    Item.FourthCityEcho: -1,
    Item.RatShilling: 125
})

# Tier 5

trade(1, {
    Item.UncannyIncunabulum: -5,
    Item.RatShilling: 850
})

trade(1, {
    Item.StormThrenody: -5,
    Item.RatShilling: 850
})

trade(1, {
    Item.RattyReliquary: -5,
    Item.RatShilling: 850
})

trade(1, {
    Item.UnlawfulDevice: -5,
    Item.RatShilling: 850
})

# Tier 6

trade(1, {
    Item.NightWhisper: -1,
    Item.RatShilling: 850
})

trade(1, {
    Item.ParabolaLinenScrap: -1,
    Item.RatShilling: 850
})

trade(1, {
    Item.CracklingDevice: -1,
    Item.RatShilling: 850
})

trade(1, {
    Item.CaptivatingBallad: -1,
    Item.RatShilling: 850
})

# Tier 7

trade(1, {
    Item.CorrespondingSounder: -1,
    Item.RatShilling: 4000
})

trade(1, {
    Item.ScrapOfIvoryOrganza: -1,
    Item.RatShilling: 4000
})

trade(1, {
    Item.CartographersHoard: -1,
    Item.RatShilling: 4000
})

trade(1, {
    Item.ParabolanParable: -1,
    Item.RatShilling: 4000
})

## ------------
## Various London Carousels?
## ------------

# overnight trip
trade(40, {
    Item.ApostatesPsalm: 3,
    Item.NevercoldBrassSliver: ((38 * 40) - 50) * 10
})

# # ----------
# ██████╗  ██████╗ ███╗   ██╗███████╗    ███╗   ███╗ █████╗ ██████╗ ██╗  ██╗███████╗████████╗
# ██╔══██╗██╔═══██╗████╗  ██║██╔════╝    ████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██╔════╝╚══██╔══╝
# ██████╔╝██║   ██║██╔██╗ ██║█████╗      ██╔████╔██║███████║██████╔╝█████╔╝ █████╗     ██║   
# ██╔══██╗██║   ██║██║╚██╗██║██╔══╝      ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝     ██║   
# ██████╔╝╚██████╔╝██║ ╚████║███████╗    ██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗███████╗   ██║   
# ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   
#                                                                                            

# ealing butcher
trade(1, {
    Item.BoneFragments: -100,
    Item.NoduleOfWarmAmber: -25,
    Item.WingOfAYoungTerrorBird: 2
})

# bazaar
trade(0, {
    Item.Echo: -62.5,
    Item.BrightBrassSkull: 1
})


# Buy from patrons
trade(1, {
    Item.HinterlandScrip: -120,
    Item.SabreToothedSkull: 1
})

# -----------------
# Sell To Patrons
# ----------------

trade(1, {
    Item.HumanRibcage: -1,
    Item.IncisiveObservation: 30
})

# -----------------
# Recipes
# ----------------

# ----- Human Ribcage

# selling a chimera
# 3 implausibility sets the challenge at 225
# what shadowy level to use?
# maximum achievable w/o moods: +106
# - however that includes +13 from treasure
# - and +6 from profession
# - and also +2 from item unique to LF
# so that leaves +85 from non-exclusive sources
# - and the vake skull only works for BaL anyway
# fuck I forgot about destinies
# Okay +80 then
# 310 shadowy gives 82% success rate base
# that's about 0.218 failures per attempt
# multiply that by 1.2 to account for the suspicion gain at -5/action

'''
The thigh bone can be any limb with 0 antiquity & menace
- knotted humerus
- ivory humerus
- unidentified thigh bone
- helical thighbone
- holy relic of st fiacre
- ivory femur
- albatross wing
- fin bones, collected
'''

player_shadowy = 315

def actions_to_sell_skelly(shadowy, implausibility):
    if (implausibility < 1): return 1
    difficulty = 75 * implausibility
    success_rate = min(0.6 * shadowy/difficulty, 1.0)
    expected_failures = 1.0/success_rate - 1

    # assumes 5 clear per action
    suspicion_penalty = 0.2 * expected_failures
    return 1 + expected_failures + suspicion_penalty

trade(7 + actions_to_sell_skelly(player_shadowy, 3), {
    Item.HumanRibcage: -1,
    Item.BoneFragments: -6000, # vake skull
    Item.WingOfAYoungTerrorBird: -3,
    Item.UnidentifiedThighbone: -1,
    Item.HinterlandScrip: 192, # 194 minus 2 for buying the thigh bone
    Item.CarvedBallOfStygianIvory: 21,
})

# # non-BaL

trade(7 + actions_to_sell_skelly(player_shadowy, 3), {
    Item.HumanRibcage: -1,
    Item.SabreToothedSkull: -1,
    Item.WingOfAYoungTerrorBird: -3,
    Item.UnidentifiedThighbone: -1,
    Item.HinterlandScrip: 189,
    Item.CarvedBallOfStygianIvory: 18,
})

trade(7 + actions_to_sell_skelly(player_shadowy, 3), {
    Item.HumanRibcage: -1,
    Item.HornedSkull: -1,
    Item.WingOfAYoungTerrorBird: -2,
    Item.AmberCrustedFin: -2,
    Item.HinterlandScrip: 137,
    Item.CarvedBallOfStygianIvory: 21,
})

# trade(8, {
    
# })

# Generator Skeleton, various

# testing various balances of brass vs. sabre-toothed skull
# capping at 2 bc 3 brass skulls requires 375 shadowy to 100% the sale
for i in range(0, 3):
    zoo_bonus = 0.1

    brass_skulls = i
    sabre_toothed_skulls = 7 - i

    penny_value = 6250 + 2500
    penny_value += 6500 * brass_skulls
    penny_value += 6250 * sabre_toothed_skulls

    trade(11 + actions_to_sell_skelly(player_shadowy, brass_skulls * 2), {
        Item.SkeletonWithSevenNecks: -1,
        Item.BrightBrassSkull: -1 * brass_skulls,
        Item.NevercoldBrassSliver: -200 * brass_skulls,
        Item.SabreToothedSkull: -1 * sabre_toothed_skulls,
        Item.AlbatrossWing: -2,
        Item.MemoryOfDistantShores: 5 + (penny_value * (1 + zoo_bonus)/50),
        # amalgamy week
        Item.FinalBreath: 74
    })

# same as above but with 1x skull in coral and different wings
for i in range(0, 3):
    brass_skulls = i
    sabre_toothed_skulls = 6 - i

    penny_value = 6250 + 1750 + 500
    penny_value += 6500 * brass_skulls
    penny_value += 6250 * sabre_toothed_skulls

    zoo_bonus = 0.1

    trade(11 + actions_to_sell_skelly(player_shadowy, brass_skulls * 2), {
        Item.SkeletonWithSevenNecks: -1,
        Item.BrightBrassSkull: -1 * brass_skulls,
        Item.NevercoldBrassSliver: -200 * brass_skulls,
        Item.SabreToothedSkull: -1 * sabre_toothed_skulls,
        Item.SkullInCoral: -1,
        Item.KnobOfScintillack: -1,
        Item.WingOfAYoungTerrorBird: -2,
        Item.MemoryOfDistantShores: 5 + (penny_value * (1 + zoo_bonus)/50),
        # amalgamy week
        Item.FinalBreath: 74
    })

# Hoarding Palaeo
for i in range(0, 3):
    zoo_bonus = 0.1

    brass_skulls = i
    sabre_toothed_skulls = 7 - i

    penny_value = 0
    penny_value += 6250 # skelly
    penny_value += 6500 * brass_skulls
    penny_value += 6250 * sabre_toothed_skulls
    penny_value += 250 * 2 # wings

    trade(11 + actions_to_sell_skelly(player_shadowy, brass_skulls * 2), {
        Item.SkeletonWithSevenNecks: -1,
        Item.BrightBrassSkull: -1 * brass_skulls,
        Item.NevercoldBrassSliver: -200 * brass_skulls,
        Item.SabreToothedSkull: -1 * sabre_toothed_skulls,
        Item.WingOfAYoungTerrorBird: -2,
        Item.BoneFragments: penny_value * (1 + zoo_bonus),
        Item.UnearthlyFossil: 2
    })

# Zailor Particular
for i in range(0, 3):
    zoo_bonus = 0.1
    antiquity_bonus = 0.5
    amalgamy_bonus  = 0

    brass_skulls = i
    sabre_toothed_skulls = 7 - i

    penny_value = 0
    penny_value += 6250 # skelly
    penny_value += 6500 * brass_skulls
    penny_value += 6250 * sabre_toothed_skulls
    penny_value += 250 * 2 # wings

    antiquity = sabre_toothed_skulls + 2
    amalgamy = 2

    trade(11 + actions_to_sell_skelly(player_shadowy, brass_skulls * 2), {
        Item.SkeletonWithSevenNecks: -1,
        Item.BrightBrassSkull: -1 * brass_skulls,
        Item.NevercoldBrassSliver: -200 * brass_skulls,
        Item.SabreToothedSkull: -1 * sabre_toothed_skulls,
        Item.WingOfAYoungTerrorBird: -2,
        Item.NoduleOfWarmAmber: 25 + (penny_value * (1 + zoo_bonus))/10,
        Item.KnobOfScintillack: ((antiquity + amalgamy_bonus) * (amalgamy + antiquity_bonus))
    })    
    
# trade(12, {
#     Item.SkeletonWithSevenNecks: -1,
#     Item.BrightBrassSkull: -2,
#     Item.NevercoldBrassSliver: -400,
#     Item.SabreToothedSkull: -5,
#     Item.WingOfAYoungTerrorBird: -2,

#     Item.NoduleOfWarmAmber: 5635,
#     Item.KnobOfScintillack: 18
# })

# # antique birds week
# trade(12, {
#     Item.SkeletonWithSevenNecks: -1,
#     Item.BrightBrassSkull: -2,
#     Item.NevercoldBrassSliver: -400,
#     Item.SabreToothedSkull: -5,
#     Item.WingOfAYoungTerrorBird: -1,
#     Item.AlbatrossWing: -1,

#     Item.NoduleOfWarmAmber: 5745,
#     Item.KnobOfScintillack: 21
# })

# ██╗  ██╗██╗  ██╗ █████╗ ███╗   ██╗ █████╗ ████████╗███████╗
# ██║ ██╔╝██║  ██║██╔══██╗████╗  ██║██╔══██╗╚══██╔══╝██╔════╝
# █████╔╝ ███████║███████║██╔██╗ ██║███████║   ██║   █████╗  
# ██╔═██╗ ██╔══██║██╔══██║██║╚██╗██║██╔══██║   ██║   ██╔══╝  
# ██║  ██╗██║  ██║██║  ██║██║ ╚████║██║  ██║   ██║   ███████╗
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚══════╝

# -------------
# Khaganian Markets
# -------------

# selling
trade(0, {
    Item.DeepZeeCatch: -1,
    Item.AssortmentOfKhaganianCoinage: 1
})

trade(0, {
    Item.CarvedBallOfStygianIvory: -1,
    Item.AssortmentOfKhaganianCoinage: 5
})

trade(0, {
    Item.JasmineLeaves: -1,
    Item.MoonPearl: 10
})

trade(0, {
    Item.BottleOfFourthCityAirag: -1,
    Item.AssortmentOfKhaganianCoinage: 125
})

trade(0, {
    Item.CaptivatingBallad: -1,
    Item.AssortmentOfKhaganianCoinage: 125
})

trade(0, {
    Item.CracklingDevice: -1,
    Item.AssortmentOfKhaganianCoinage: 125
})

trade(0, {
    Item.MuchNeededGap: -1,
    Item.AssortmentOfKhaganianCoinage: 125
})

trade(0, {
    Item.OneiricPearl: -1,
    Item.AssortmentOfKhaganianCoinage: 125
})

trade(0, {
    Item.SaltSteppeAtlas: -1,
    Item.AssortmentOfKhaganianCoinage: 125
})

# -------------
# Mightnight Market
# -------------

trade(0, {
    Item.AssortmentOfKhaganianCoinage: -2,
    Item.DeepZeeCatch: 1
})

trade(0, {
    Item.AssortmentOfKhaganianCoinage: -10,
    Item.CarvedBallOfStygianIvory: 1
})

trade(0, {
    Item.TouchingLoveStory: -10,
    Item.TouchingLoveStory: 1
})

trade(0, {
    Item.MoonPearl: -20,
    Item.JasmineLeaves: 1
})

trade(0, {
    Item.MoonPearl: -20,
    Item.KhaganianLightbulb: 1
})

trade(0, {
    Item.AssortmentOfKhaganianCoinage: -130,
    Item.CracklingDevice: 1
})



# -------------
# Intrigues
# -------------

# Intercept a cablegram
trade(2, {
    Item.Infiltrating: -20,
    Item.InterceptedCablegram: 5,
    Item.VitalIntelligence: 1
})




# ███████╗ █████╗ ██╗██╗     ██╗███╗   ██╗ ██████╗ 
# ╚══███╔╝██╔══██╗██║██║     ██║████╗  ██║██╔════╝ 
#   ███╔╝ ███████║██║██║     ██║██╔██╗ ██║██║  ███╗
#  ███╔╝  ██╔══██║██║██║     ██║██║╚██╗██║██║   ██║
# ███████╗██║  ██║██║███████╗██║██║ ╚████║╚██████╔╝
# ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
    
# ballparking EPA for zailing with piracy
trade(0, {
    Item.ZailingDraws: -1,
    Item.Echo: zailing_epa
})

# rounding up for overflow
trade(2, {
    Item.ChasingDownYourBounty: -120,
    Item.StashedTreasure: 5500
})

# amortizing travel cost
trade(0, {
    Item.StashedTreasure: -1250,
    Item.MourningCandle: 5
})

trade(0, {
    Item.StashedTreasure: -1250,
    Item.CaveAgedCodeOfHonour: 1
})

trade(0, {
    Item.StashedTreasure: -6250,
    Item.RelativelySafeZeeLane: 1
})

trade(0, {
    Item.StashedTreasure: -6250,
    Item.SaltSteppeAtlas: 1
})

trade(0, {
    Item.StashedTreasure: -31250,
    Item.FabulousDiamond: 1
})

# optimistic 100% draw rate of chasing cards
# pessimistic no rare success
trade(0, {
    Item.HomeWatersZeeDraw: -1,
    Item.ChasingDownYourBounty: 8
})

trade(0, {
    Item.ShephersWashZeeDraw: -1,
    Item.ChasingDownYourBounty: 8.5
})

trade(0, {
    Item.StormbonesZeeDraw: -1,
    Item.ChasingDownYourBounty: 8.5
})

trade(0, {
    Item.SeaOfVoicesZeeDraw: -1,
    Item.ChasingDownYourBounty: 9
})

trade(0, {
    Item.SaltSteppesZeeDraw: -1,
    Item.ChasingDownYourBounty: 13.5
})

trade(0, {
    Item.PillaredSeaZeeDraw: -1,
    Item.ChasingDownYourBounty: 14.5
})

trade(0, {
    Item.StormbonesZeeDraw: -1,
    Item.ChasingDownYourBounty: 15.5
})


## ------------
## Court of the Wakeful Eye Grind
## ------------

# Just make it one big blob
# Can't be arsed to figure out the 240/260 leftovers thing
# 14 actions = 2x the following
# - 1 action to dock
# - 2 actions in home waters
# - 4 actions in shephers wash

trade(14 + 50.6, {
    Item.HomeWatersZeeDraw: 4,
    Item.ShephersWashZeeDraw: 8,
    # Psuedo item represents tribute cap of 260
    Item.Tribute: -253,
    Item.NightWhisper: 12.65
})

# Gaining tribute

trade(1, {
    Item.Echo: -25,
    Item.Tribute: 10
})

trade(1, {
    Item.MagnificentDiamond: -1,
    Item.Tribute: 5
})

trade(1, {
    Item.PuzzleDamaskScrap: -1,
    Item.Tribute: 5
})

trade(1, {
    Item.CellarOfWine: -1,
    Item.Tribute: 5
})

trade(1, {
    Item.FavBohemians: -7,
    Item.Tribute: 23
})

trade(1, {
    Item.FavChurch: -7,
    Item.Tribute: 23
})

trade(1, {
    Item.FavCriminals: -7,
    Item.Tribute: 23
})

trade(1, {
    Item.FavDocks: -7,
    Item.Tribute: 23
})

trade(1, {
    Item.FavSociety: -7,
    Item.Tribute: 23
})

trade(1, {
    Item.MemoryOfLight: -50,
    Item.Tribute: 10
})

trade(1, {
    Item.MountainSherd: -1,
    Item.Tribute: 35
})

trade(1, {
    Item.RoyalBlueFeather: -16,
    Item.Tribute: 4
})

trade(1, {
    Item.CorrespondencePlaque: -50,
    Item.Tribute: 10
})

trade(1, {
    Item.StrongBackedLabour: -1,
    Item.Tribute: 2
})

# trade(1, {
#     # throwing this random penalty in there arbitrarily
#     # to represent the fact that you're no longer bounded by cards
#     Item.CardDraws: -1,
#     Item.WinsomeDispossessedOrphan: -1,
#     Item.Tribute: 25
# })

# --------------
# Port Cecil
# -------------

# 7? actions to zail from london? 4 + 2 + 1
# TODO: check round trip length
trade(14, {
    Item.PortCecilCycles: 4, # arbitrary, how many times thru before home
    Item.ZailingDraws: 12
})

# ideal cycle w/ maxed stats
# - 13 AotRS (reliable but less profitable w less)
# - 334 Watchful (required to guarantee 50/50 split)
# - 334 Persuasive  (required to guarantee 50/50 split)
# 5x (red science miners => 7x map scrap, 1x knob scintillack)
# 1x (instruct the cats => 5x scrap of i.g., 7x romantic notion)
# 5x (prey on miners concerns => 6x journal ofinf)
# 2x (deploy cat wrangling => 30x silvered cats claw)
#   OR (distact w wildlife => 4x withered tentacle)

trade(14, {
    Item.PortCecilCycles: -1,
    Item.MapScrap: 35,
    Item.KnobOfScintillack: 5,
    Item.ScrapOfIncendiaryGossip: 5,
    Item.RomanticNotion: 7,
    Item.JournalOfInfamy: 30,
    Item.WitheredTentacle: 8,
    Item.LostResearchAssistant: 1,
    Item.SegmentedRibcage: 3
})

# alternative in carousel
trade(0, {
    Item.WitheredTentacle: -4,
    Item.SilveredCatsClaw: 30
})

# slightly less profitable but more achievable grind
# 5x direct miners toward dig site
# - doesn't derail on failure
# - 90% success w 273 P, 100% w 300
# 1x instruct cats in calc
# 3x liberate raw scintillack
# 3x bring refreshments
# 1x distract cats w/ wildlife

trade (14, {
    Item.PortCecilCycles: -1,
    Item.ZeeZtory: 6 * 5,
    Item.ScrapOfIncendiaryGossip: 5,
    Item.RomanticNotion: 7,
    Item.KnobOfScintillack: 3,
    Item.MemoryOfDistantShores: 4 * 3,
    Item.WitheredTentacle: 4,
    Item.LostResearchAssistant: 1, 
    Item.SegmentedRibcage: 3
})

# ███████╗ █████╗ ████████╗███████╗
# ██╔════╝██╔══██╗╚══██╔══╝██╔════╝
# █████╗  ███████║   ██║   █████╗  
# ██╔══╝  ██╔══██║   ██║   ██╔══╝  
# ██║     ██║  ██║   ██║   ███████╗
# ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝

# -------------------
# --- Upwards
# ------------------

# TODO: confirm all of this

trade(9, {
    Item.CartographersHoard: -1,
    Item.FivePointedRibcage: 1
})

trade(7, {
    Item.FavourInHighPlaces: -1,
    Item.CartographersHoard: -1,
    Item.FivePointedRibcage: 1
})

trade(9, {
    Item.PentagrammicSkull: 1,
    Item.BoneFragments: 1900
})

trade(7, {
    Item.FavourInHighPlaces: -1,
    Item.PentagrammicSkull: 1,
    Item.BoneFragments: 1900
})

# -------------------
# --- Philosofruits
# -------------------

# TODO: travel cost estimate
# using wiki values

trade(5, {
    Item.CardDraws: -5,
    Item.BlackmailMaterial: 1,
    Item.AnIdentityUncovered: 3
})

trade(5, {
    Item.CardDraws: -5,
    Item.AntiqueMystery: 1,
    Item.PresbyteratePassphrase: 3
})

trade(5, {
    Item.CardDraws: -5,
    Item.UncannyIncunabulum: 1,
    Item.ExtraordinaryImplication: 3
})

trade(13, {
    Item.CardDraws: -13,
    Item.ComprehensiveBribe: 4,
})

trade(10, {
    Item.CardDraws: -10,
    Item.CorrespondencePlaque: 90,
})

trade(20, {
    Item.CardDraws: -20,
    Item.BottleOfFourthCityAirag: 1,
    Item.CellarOfWine: 2
})

trade(11, {
    Item.CardDraws: -11,
    Item.StormThrenody: 4
})

#  █████╗  █████╗ ██╗██╗     ██╗    ██╗ █████╗ ██╗   ██╗
# ██╔══██╗██╔══██╗██║██║     ██║    ██║██╔══██╗╚██╗ ██╔╝
# ██████╔╝███████║██║██║     ██║ █╗ ██║███████║ ╚████╔╝ 
# ██╔══██╗██╔══██║██║██║     ██║███╗██║██╔══██║  ╚██╔╝  
# ██║  ██║██║  ██║██║███████╗╚███╔███╔╝██║  ██║   ██║   
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   

# Sets to 3
# In practice probably slightly better w overcap
trade(1, {
    Item.SeeingBanditryInTheUpperRiver: - (pyramid(8) - pyramid(3)),
    Item.Scandal: 12
})

# Card: Intervene in an Attack
trade(1, {
    Item.SeeingBanditryInTheUpperRiver: -1,
    Item.InCorporateDebt: -1 * default_rare_success_rate,
    Item.PieceOfRostygold: 400
})

# -----
# Board Member Stuff
# -----

# Tentacled Entrepreneur rotation
trade(7, {
    Item.InCorporateDebt: -15,
    Item.HinterlandScrip: 10
})

# --------------
# Shops
# -------------

trade(0, {
    Item.HinterlandScrip: -2,
    Item.UnidentifiedThighbone: 1,
})

trade(0, {
    Item.HinterlandScrip: -85,
    Item.FossilisedForelimb: 1
})

# ----- Selling
trade(0, {
    Item.AmbiguousEolith: -1,
    Item.HinterlandScrip: 1
})

trade(0, {
    Item.FinalBreath: -1,
    Item.HinterlandScrip: 1
})

trade(0, {
    Item.HandPickedPeppercaps: -1,
    Item.HinterlandScrip: 1
})

trade(0, {
    Item.MovesInTheGreatGame: -1,
    Item.HinterlandScrip: 1
})

trade(0, {
    Item.NightsoilOfTheBazaar: -1,
    Item.HinterlandScrip: 1
})


trade(0, {
    Item.PotOfVenisonMarrow: -1,
    Item.HinterlandScrip: 1
})

trade(0, {
    Item.RoyalBlueFeather: -1,
    Item.HinterlandScrip: 1
})

trade(0, {
    Item.SolaceFruit: -1,
    Item.HinterlandScrip: 1
})

trade(0, {
    Item.SurveyOfTheNeathsBones: -1,
    Item.HinterlandScrip: 1
})

trade(0, {
    Item.UnidentifiedThighbone: -1,
    Item.HinterlandScrip: 1
})

trade(0, {
    Item.PreservedSurfaceBlooms: -1,
    Item.HinterlandScrip: 3
})

trade(0, {
    Item.CarvedBallOfStygianIvory: -1,
    Item.HinterlandScrip: 5
})

trade(0, {
    Item.CrateOfIncorruptibleBiscuits: -1,
    Item.HinterlandScrip: 5
})

trade(0, {
    Item.KnobOfScintillack: -1,
    Item.HinterlandScrip: 5
})

trade(0, {
    Item.NicatoreanRelic: -1,
    Item.HinterlandScrip: 5
})

trade(0, {
    Item.TailfeatherBrilliantAsFlame: -1,
    Item.HinterlandScrip: 5
})

trade(0, {
    Item.ViennaOpening: -1,
    Item.HinterlandScrip: 5
})

trade(0, {
    Item.UnlawfulDevice: -1,
    Item.HinterlandScrip: 25
})

trade(0, {
    Item.VitalIntelligence: -1,
    Item.HinterlandScrip: 25
})

trade(0, {
    Item.QueenMate: -1,
    Item.HinterlandScrip: 50
})


trade(0, {
    Item.EpauletteMate: -1,
    Item.HinterlandScrip: 50
})

trade(0, {
    Item.SapOfTheCedarAtTheCrossroads: -1,
    Item.HinterlandScrip: 125
})

trade(0, {
    Item.Stalemate: -1,
    Item.HinterlandScrip: 125
})

trade(0, {
    Item.CartographersHoard: -1,
    Item.HinterlandScrip: 625
})


# --------------
# Ealing & Helicon
# -------------

# # TODO: fix total carousel stuff here
# trade(1, {
#     Item.FinBonesCollected: -10,
#     Item.AmberCrustedFin: 1
# })

# -- Butcher
trade(1, {
    Item.BoneFragments: -130,
    Item.NoduleOfWarmAmber: -2,
    Item.WarblerSkeleton: 2
})

trade(1, {
    Item.BoneFragments: -100,
    Item.NoduleOfWarmAmber: -2,
    Item.BatWing: 2
})

trade(1, {
    Item.BoneFragments: -2000,
    Item.NoduleOfWarmAmber: -25,
    Item.AlbatrossWing: 2
})

trade(1, {
    Item.BoneFragments: -4900,
    Item.NoduleOfWarmAmber: -125,
    Item.SabreToothedSkull: 1,
    Item.FemurOfASurfaceDeer: 0.5,
    Item.UnidentifiedThighbone: 0.5
})

trade(1, {
    Item.BoneFragments: -1000,
    Item.NoduleOfWarmAmber: -5,
    Item.HornedSkull: 1
})

trade(1, {
    Item.BoneFragments: -200,
    Item.NoduleOfWarmAmber: -2,
    Item.TombLionsTail: 2
})

trade(1, {
    Item.BoneFragments: -100,
    Item.NoduleOfWarmAmber: -25,
    Item.WingOfAYoungTerrorBird: 2
})

trade(1, {
    Item.BoneFragments: -1750,
    Item.NoduleOfWarmAmber: -25,
    Item.CrateOfIncorruptibleBiscuits: -1,
    Item.PlatedSkull: 1
})

# --- Sponsor a Dig
# NB: Wiki is uncertain about some ranges

trade(1, {
    Item.StrongBackedLabour: -1,
    Item.SurveyOfTheNeathsBones: -50,
    Item.HelicalThighbone: 3,
    Item.KnottedHumerus: 2.5,
    Item.HumanRibcage: 1,
    Item.BoneFragments: 385.5
})

trade(1, {
    Item.StrongBackedLabour: -1,
    Item.SurveyOfTheNeathsBones: -75,
    Item.ThornedRibcage: 1,
    Item.HornedSkull: 1,
    Item.FemurOfAJurassicBeast: 4,
    Item.JetBlackStinger: 4,
    Item.FinBonesCollected: 12.5
})


trade(1, {
    Item.StrongBackedLabour: -1,
    Item.SurveyOfTheNeathsBones: -163,
    Item.PalaeontologicalDiscovery: 7
})


trade(1, {
    Item.StrongBackedLabour: -1,
    Item.SurveyOfTheNeathsBones: 175,
    Item.MagisterialLager: -10,
    Item.PalaeontologicalDiscovery: 7,
    Item.Echo: 6.3 # estimated Rusted Stirrup value
})

trade(0, {
    Item.PalaeontologicalDiscovery: -25,
    Item.LeviathanFrame: 1
})

trade(0, {
    Item.PalaeontologicalDiscovery: -5,
    Item.MammothRibcage: 1
})

trade(0, {
    Item.PalaeontologicalDiscovery: -5,
    Item.SabreToothedSkull: 1
})

trade(0, {
    Item.PalaeontologicalDiscovery: -4,
    Item.FossilisedForelimb: 2
})

trade(0, {
    Item.PalaeontologicalDiscovery: -3,
    Item.HumanRibcage: 2,
    Item.HumanArm: 4
    # Item.TraceOfTheFirstCity: 5
})

# -----------------------------------
# ---- Jericho
# -----------------------------------

# --------- Canal Cruising

if profession == Profession.CrookedCross:
    trade(1, {
        Item.UnprovenancedArtefact: -4,
        Item.EsteemOfTheGuild: 1
    })

trade(1, {
    Item.VolumeOfCollatedResearch: -10,
    Item.EsteemOfTheGuild: 2
})

trade(1, {
    Item.PartialMap: -6,
    Item.AnIdentityUncovered: -4,
    Item.EsteemOfTheGuild: 2
})

# trade(1, {
#     Item.MemoryOfDistantShores: -40,
#     Item.SwornStatement: -2,
#     Item.EsteemOfTheGuild: 2
# })

trade(1, {
    Item.NightOnTheTown: -1,
    Item.ScrapOfIncendiaryGossip: -45,
    Item.EsteemOfTheGuild: 2
})

trade(1, {
    Item.FavDocks: -5,
    Item.EsteemOfTheGuild: 2
})

# assume ranges are evenly distributed
trade(2, {
    Item.EsteemOfTheGuild: -3,
    Item.VitalIntelligence: 2.5,
    Item.ViennaOpening: 6.5
})

trade(2, {
    Item.EsteemOfTheGuild: -3,
    Item.MirrorcatchBox: 1
})

trade(2, {
    Item.EsteemOfTheGuild: -3,
    Item.MoonlightScales: 50,
    Item.FinBonesCollected: 5,
    Item.SkullInCoral: 1.5,
    Item.UnprovenancedArtefact: 8.5
})

# upper river destinations

trade(2, {
    Item.EsteemOfTheGuild: -6,
    Item.BrightBrassSkull: 1,
    Item.ExtraordinaryImplication: 5.5,
    Item.VerseOfCounterCreed: 2.5
})

trade(2, {
    Item.EsteemOfTheGuild: -6,
    Item.MovesInTheGreatGame: 18.5,
    Item.PrimaevalHint: 1,
    Item.UncannyIncunabulum: 2.5
})

trade(2, {
    Item.EsteemOfTheGuild: -6,
    Item.NightWhisper: 1,
    Item.TaleOfTerror: 3.5,
    Item.FinalBreath: 12,
    Item.HumanRibcage: 2
})


# --------- Calling in Favours
# hack to model dipping into jericho to trade favours
# when you would otherwise not go there

jericho_add = 0.0
def jericho_trade(exchange):
    exchange[Item.RumourOfTheUpperRiver] = jericho_add
    trade(1 + jericho_add, exchange)

jericho_trade({
    Item.FavBohemians: -4,
    Item.HolyRelicOfTheThighOfStFiacre: 2,
    Item.WingOfAYoungTerrorBird: 1,
})

jericho_trade({
    Item.FavChurch: -4,
    Item.RattyReliquary: 2,
    Item.ApostatesPsalm: 1,
})

jericho_trade({
    Item.FavConstables: -4,
    Item.CaveAgedCodeOfHonour: 2,
    Item.SwornStatement: 1
})

jericho_trade({
    Item.FavCriminals: -4,
    Item.HumanRibcage: 2,
    Item.HumanArm: 1
})

jericho_trade({
    Item.FavDocks: -4,
    Item.UncannyIncunabulum: 2,
    Item.KnobOfScintillack: 1
})

jericho_trade({
    Item.FavGreatGame: -4,
    Item.ViennaOpening: 1,
    Item.QueenMate: 1
})

jericho_trade({
    Item.FavHell: -4,
    Item.ThornedRibcage: 2,
    Item.QueerSoul: 1
})

jericho_trade({
    Item.FavRevolutionaries: -4,
    Item.UnlawfulDevice: 2,
    Item.ThirstyBombazineScrap: 1
})

jericho_trade({
    Item.FavRubberyMen: -4,
    Item.FlourishingRibcage: 2,
    Item.BasketOfRubberyPies: 1,
})

jericho_trade({
    Item.FavSociety: -4,
    Item.FavourInHighPlaces: 2,
    Item.NightOnTheTown: 1
})

jericho_trade({
    Item.FavTombColonies: -4,
    Item.AntiqueMystery: 2,
    Item.UnprovenancedArtefact: 1,
})

jericho_trade({
    Item.FavUrchins: -4,
    Item.StormThrenody: 2,
    Item.AeolianScream: 1
})

# --------------
# Evenlode
# -------------


railway_card("Digs in the Magistracy of the Evenlode", Rarity.Standard, True, {
    Item.DigsInEvenlode: 1
})

trade(0, {
    Item.DigsInEvenlode: -1,
    Item.SurveyOfTheNeathsBones: -120,
    Item.PalaeontologicalDiscovery: 5
})


trade(0, {
    Item.DigsInEvenlode: -1,
    Item.SurveyOfTheNeathsBones: -140,
    Item.PalaeontologicalDiscovery: 6
})

# specific treasure only
trade(0, {
    Item.DigsInEvenlode: -1,
    Item.SurveyOfTheNeathsBones: -240,
    Item.PalaeontologicalDiscovery: 10
})


# --------------
# Balmoral
# -------------

# 2x (1 action, 4 research) to enter
# 1 action to go to glade
# 3x (1 action, 3 bombazine) to darken
# 1 action wander
# 1 action locate red deer
# 1 action cash out with keeper

# TODO: double check action counts for these
# Mammoth Ribcage
trade(9, {
    Item.VolumeOfCollatedResearch: -8,
    Item.ThirstyBombazineScrap: -9,

    Item.MammothRibcage: 1,
    Item.HolyRelicOfTheThighOfStFiacre: 1,
    Item.FemurOfAJurassicBeast: 2,
    Item.BoneFragments: 400
})

# Skeleton with 7 Necks
trade(7, {
    Item.VolumeOfCollatedResearch: -8,
    Item.UnprovenancedArtefact: -4,

    Item.SkeletonWithSevenNecks: 1,
    Item.WingOfAYoungTerrorBird: 3,
    Item.BoneFragments: 200
})

# --------------
# Station VIII
# -------------

trade(1, {
    Item.OilOfCompanionship: -1,
    Item.RumourOfTheUpperRiver: -98,

    Item.PrismaticFrame: 1
})

# guessing how this works, havent unlocked  yet
trade(2, {
    Item.AntiqueMystery: -2,
    Item.ConsignmentOfScintillackSnuff: -2,

    Item.OilOfCompanionship: 1
})


# ----------------
# --- The Hurlers
# ----------------


# Licensed by Mr Stones

trade(1, {
    Item.FlawedDiamond: -100,
    Item.HinterlandScrip: 30
})

trade(1, {
    Item.OstentatiousDiamond: -25,
    Item.CrateOfIncorruptibleBiscuits: 6
})

trade(1, {
    Item.MagnificentDiamond: -1,
    Item.TouchingLoveStory: 5.5 # assumes uniform 5 or 6
})

trade(1, {
    Item.FabulousDiamond: -1,
    Item.HinterlandScrip: 625,
    Item.StolenKiss: 2
})


# -------------------------------
# ---- Opportunity Deck Math ----
# -------------------------------

# subtract 400 for holding 4 bad standard freq cards in hand
deck_size = LondonDeckSize - 400;
good_card_density = GoodCardsInDeck / deck_size
good_cards_per_day = good_card_density * cards_seen_per_day
card_exchange = {}

for item in Item:
    if LondonCardsByItem[item.value] != 0:
        card_exchange[item] = cards_seen_per_day * (LondonCardsByItem[item.value] / deck_size)

card_exchange[Item.CardDraws] = -1 * cards_seen_per_day
# card_exchange[Item.Action] = -1 * good_cards_per_day

# print(card_exchange)
trade(good_cards_per_day, card_exchange)
# per_day(card_exchange)

# ------------------------------------------
# ---------------- Optimization ------------
# ------------------------------------------

optimize_for = Item.Echo

c = np.zeros(num_vars)
c[optimize_for.value] = -1

opt_result = linprog(c, A_ub=A.toarray(), b_ub=b, bounds=bounds, method='highs')
print(opt_result)

# print("Opp Deck")

# print(f"{'Item Name':^30}")
# # for item, quantity in zip(Item, opt_result.x):
# #     item_name = f"{item.name:30}"
# #     per_action = f"{(1.0/(quantity * actions_per_day) if quantity != 0 else 0.0):10.3f}"
# #     per_card = LondonCardsByItem[item.value] / LondonDeckSize
# #     per_day_of_draws = per_card * cards_seen_per_day
# #     print(item_name + per_action + ((f"{per_card:10.2f}" + f"{per_day_of_draws:10.2f}") if per_card != 0 else ""))


# for item, quantity in zip(Item, opt_result.x):
#     item_name = f"{item.name:30}"
#     index = item.value
#     print(item_name
#         + f"{quantity:10.3}"
#         # + f"{opt_result.lower.residual[index]:10.3}"
#         # + f"{opt_result.lower.marginals[index]:10.3}"
#         # + f"{opt_result.upper.residual[index]:10.3}"
#         # + f"{opt_result.upper.marginals[index]:10.3}"
#         )



print("------Assumptions-------")
print(f"Total Actions per Day:            {actions_per_day:10}")
print(f"Cards Drawn per Day:              {cards_seen_per_day:10}")
print(f"Optimize For:                     {optimize_for}")

print("------Summary-------")
print(f"Good Card Density:                {good_card_density:10.3f}")
print(f"Actions spent on Cards per Day:   {good_cards_per_day:10.3f}")
print(f"{str(optimize_for) + ' Per Day:':34}{-1.0/(opt_result.fun):10.3f}")
print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.3f}")

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(A)
# pp.pprint(A[0])
# pp.pprint(A[100, 0])

# print("-----Trades NOT USED-------")
# for i in range(0, len(opt_result.slack)):
#     slack = opt_result.slack[i]
#     marginal = opt_result.ineqlin.marginals[i]
#     if (slack != 1.0 and (slack > 1.0 or  marginal == 0)):
#         trade_items = ""
#         for ii in range(0, num_items):
#             if A[i, ii] != 0:
#                 trade_items += str(Item(ii)) + ":" + str(A[i, ii]) + "; "
#         print(f"Slack: {slack:3.3} " + trade_items)


print("-----Trades In Grind-------")
for i in range(0, len(opt_result.slack)):
    slack = opt_result.slack[i]
    marginal = opt_result.ineqlin.marginals[i]
    if (slack < 1.0 and marginal != 0):
        lose_items = ""
        gain_items = ""
        for ii in range(0, num_items):
            quantity = round(A[i, ii],2)
            if int(quantity) == quantity:
                quantity = int(quantity)
            if quantity < 0:
                lose_items += str(Item(ii)) + ":" + str(quantity) + "; "
            if quantity > 0:
                gain_items += str(Item(ii)) + ":" + str(quantity) + "; "
        trade_items = lose_items + " => " + gain_items            
        trade_items = trade_items.replace("Item.","");
        # print(trade_items)
        print(f"{marginal:.3}       " + trade_items)

print(f"{str(optimize_for) + ' Per Action':34}{-1.0/(opt_result.fun * actions_per_day):10.5f}")
