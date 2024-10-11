from enums import *
from helper.utils import *
from config import Config

# TODO: multiple files?

def add_trades(config: Config):
    trade = config.trade
    add = config.add
    player = config.player

    # Player Unlocks
    has_spur_line = player.get(Item.InvolvedInARailwayVenture) >= 140
    has_seal = player.get(Item.SealOfStJoshua) > 0

    # TODO confirm these numbers from Oct 11 update
    deer_prosperity = 1260 if has_spur_line else 0
    grouse_prosperity = 1110 if has_spur_line else 0
    fox_prosperity = 1220 if has_spur_line else 0

    for i in range(0, 7):
        visit_length = 2 ** i
        add({
            Item._UpperRiverRoundTrip: -1,
            Item.Action: -1 * visit_length,
            Item._BalmoralAction: visit_length,

            # TODO unsure this ties out
            Item._UnveilYourPaintingLondon: 1
        })

    #####################
    # Weekly Stuff
    #####################
    add({
        Item._BalmoralAction: -2,
        Item.GiftFromBalmoral: -1,

        Item.HinterlandScrip: 125
    })

    #####################
    # Entering the Woods
    #####################

    add({
        Item._BalmoralAction: -3,
        Item.VitalIntelligence: -2,
        Item._MoonlitWoodsEntry: 1
    })

    if has_seal:
        add({
            Item._BalmoralAction: -3,
            Item.VolumeOfCollatedResearch: -8,
            Item._MoonlitWoodsEntry: 1
        })

    #####################
    # Seven-Necked Skelly
    #####################        

    # Fringes, Trail, Wander x2, Track
    add({
        Item._BalmoralAction: -5,
        Item.UnprovenancedArtefact: -4,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 1,
        Item.ObservationGrouse: 1
    })

    # Fringes, Trail x2, Track
    add({
        Item._BalmoralAction: -4,
        Item.UnprovenancedArtefact: -8,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 2,
        Item.ObservationGrouse: 1
    })

    # Glades, Darken x2, Fringes, Track
    add({
        Item._BalmoralAction: -5,
        Item.ThirstyBombazineScrap: -6,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 2,
        Item.ObservationGrouse: 1
    })

    add({
        Item._BalmoralAction: -1,
        Item.ObservationGrouse: -1,

        Item.SkeletonWithSevenNecks: 1,
        Item.WingOfAYoungTerrorBird: 3,
        Item.BoneFragments: 200,
        Item.HinterlandProsperity: grouse_prosperity
    })

    #####################
    # Mammoth Ribcage
    #####################

    # Glades, Darken x3, Wander, Track
    add({
        Item._BalmoralAction: -6,
        Item.ThirstyBombazineScrap: -9,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 4,
        Item.ObservationRedDeer: 1
    })

    # Fringes, Trail x3, Glades, Track
    add({
        Item._BalmoralAction: -6,
        Item.UnprovenancedArtefact: -12,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 3,
        Item.ObservationRedDeer: 1
    })

    # Fringes, Trail x2, Glades, Darken, Track
    add({
        Item._BalmoralAction: -6,
        Item.UnprovenancedArtefact: -12,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 3,
        Item.ObservationRedDeer: 1
    })

    # Fringes, Trail x2, Glades, Wander x2, Track
    add({
        Item._BalmoralAction: -7,
        Item.UnprovenancedArtefact: -8,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 4,
        Item.ObservationRedDeer: 1
    })    

    # Fringes, Trail, Glades, Darken x2, Track
    add({
        Item._BalmoralAction: -6,
        Item.UnprovenancedArtefact: -4,
        Item.ThirstyBombazineScrap: -6,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 3,
        Item.ObservationRedDeer: 1
    })

    # Moonlit grind?
    # Glades, Wander x10, Track
    add({
        Item._BalmoralAction: -12,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 10,
        Item.ObservationRedDeer: 1
    })

    add({
        Item._BalmoralAction: -1,
        Item.ObservationRedDeer: -1,

        Item.MammothRibcage: 1,
        Item.HolyRelicOfTheThighOfStFiacre: 1,
        Item.FemurOfAJurassicBeast: 2,
        Item.BoneFragments: 400,

        Item.HinterlandProsperity: deer_prosperity
    })    


    #####################
    # Doubled Skull
    #####################

    # Glades, Darken x2, Moonlight, Track
    add({
        Item._BalmoralAction: -5,
        Item.ThirstyBombazineScrap: -6,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 3,
        Item.ObservationFox: 1
    })

    # Glades, Darken, Wander x3, Moonlight, Track
    add({
        Item._BalmoralAction: -7,
        Item.ThirstyBombazineScrap: -3,
        Item._MoonlitWoodsEntry: -1,

        Item.Moonlit: 4,
        Item.ObservationFox: 1
    })    

    add({
        Item._BalmoralAction: -1,
        Item.ObservationFox: -1,
        Item.Moonlit: -5,

        Item.DoubledSkull: 1,
        Item.ThornedRibcage: 1,
        Item.KnottedHumerus: 2,

        Item.HinterlandProsperity: fox_prosperity
    })    

    # ---------------------------------
    # ------- Cabinet Noir ------------
    # ---------------------------------
    # TODO: check for leftovers on various sales

    for ties in (
        Item.CoverTiesBazaar,
        Item.CoverTiesDispossessed,
        Item.CoverTiesSurface,
    ):
        add({ ties: -1, Item._CoverTiesGeneric: 1 })

    add({
    Item._BalmoralAction: -1,
        Item._CoverTiesGeneric: 1
    })

    # --- Surface ties ---

    add({Item._BalmoralAction: -1,
        Item.FavGreatGame: -1,
        Item.CoverTiesSurface: 1,
        Item.CoverElaboration: 1,
    })

    # Canny Cuttlefish
    add({
        Item._BalmoralAction: -1,
        Item.CrypticClue: -250,
        Item.CoverTiesSurface: 1,
        Item.CoverElaboration: 1,
        Item.CoverBackstory: 1
    })

    if (player.get(Item.PalatialHolidayHomeInArcticCircle)):
        add({
        Item._BalmoralAction: -1,
            Item.CoverTiesSurface: 1,
            Item.CoverElaboration: 1,
            Item.CoverNuance: 1
        })

    if (player.get(Item.SocietyOfTheThreeFingeredHand)):
        add({
        Item._BalmoralAction: -1,
            Item.CoverTiesSurface: 1,
            Item.CoverElaboration: 1,
            Item.CoverWitnessnes: 1
        })

    # --- Bazaar ties ---

    add({
        Item._BalmoralAction: -1,
        Item.FavSociety: -1,
        Item.CoverTiesBazaar: 1,
        Item.CoverElaboration: 1
    })

    # Surveiling Spindlewolf
    add({
        Item._BalmoralAction: -1,
        Item.CrypticClue: -250,
        Item.CoverTiesSurface: 1,
        Item.CoverElaboration: 1,
        Item.CoverBackstory: 1
    })

    # --- Dispossessed ties ---
    add({
        Item._BalmoralAction: -1,
        Item.FavUrchins: -1,
        Item.CoverTiesDispossessed: 1,
        Item.CoverElaboration: 1
    })

    if (player.get(Item.TheMarvellous)):
        add({
        Item._BalmoralAction: -1,
            Item.CoverTiesDispossessed: 1,
            Item.CoverElaboration: 1,
            Item.CoverWitnessnes: 1
        })

    # TODO: Increase cost for higher counts
    add({
        Item._BalmoralAction: -1,
        Item.CoverElaboration: 1
    })

    add({
        Item._BalmoralAction: -1,
        Item.CoverNuance: 1
    })

    add({
        Item._BalmoralAction: -1,
        Item.CoverWitnessnes: 1
    })

    add({
        Item._BalmoralAction: -1,
        Item.CoverCredentials: 1
    })

    add({
        Item._BalmoralAction: -1,
        Item.WellPlacedPawn: -25,
        Item.CoverBackstory: 2
    })

    trade(2, {
        Item.WellPlacedPawn: -250,
        Item.CoverBackstory: 12
    })

    add({
        Item._BalmoralAction: -1,
        Item.ViennaOpening: -5,
        Item.CoverBackstory: 6
    })

    add({
        Item._BalmoralAction: -1,
        Item.FinalBreath: -50,
        Item.CoverBackstory: 11
    })

    add({
        Item._BalmoralAction: -1,
        Item.MovesInTheGreatGame: -50,
        Item.CoverBackstory: 11
    })

    add({
        Item._BalmoralAction: -1,
        Item.UnusualLoveStory: -100,
        Item.CoverBackstory: 22
    })

    add({
        Item._BalmoralAction: -1,
        Item.MortificationOfAGreatPower: -1,
        Item.CoverBackstory: 26
    })

    # Selling Identities

    add({
        Item._BalmoralAction: -1,
        Item.CoverTiesBazaar: -1,
        Item.CoverElaboration: -10,
        Item.CoverCredentials: -4,
        Item.CoverNuance: -4,
        Item.CoverWitnessnes: -4,
        Item.CoverBackstory: -10,

        Item.RailwaySteel: 11
    })

    # # Card
    # add({
    #     Item._BalmoralAction: -1,
    #     Item.CoverTiesSurface: -1,
    #     Item.CoverElaboration: -4,

    #     Item.FavRevolutionaries: 2
    # })

    # # Card
    # add({
    # Item._BalmoralAction: -1,
    #     Item.CoverTiesBazaar: -1,
    #     Item.CoverElaboration: -4,

    #     Item.FavUrchins: 2
    # })

    # # Card
    # add({
    #     Item._BalmoralAction: -1,
    #     Item.CoverTiesDispossessed: -1,
    #     Item.CoverElaboration: -4,

    #     Item.FavConstables: 2,
    #     Item.HinterlandScrip: 2.5
    # })

    # # Card
    # add({
    #     Item._BalmoralAction: -1,
    #     Item.CoverElaboration: -10,
    #     Item.CoverCredentials: -6,
    #     Item.CoverNuance: -6,
    #     Item.CoverWitnessnes: -6,      
    #     Item.CoverBackstory: -500

    #     # TODO: Document for deciphering
    # })

    # # Card
    # add({
    #     Item._BalmoralAction: -1,
    #     Item.CoverTiesSurface: -1
    #     Item.CoverElaboration: -10,
    #     Item.CoverCredentials: -6,
    #     Item.CoverNuance: -6,
    #     Item.CoverWitnessnes: -6,      
    #     Item.CoverBackstory: -500

    #     # TODO: Document for deciphering
    # })

    # # Respectable Passengers card
    # add({
    #     Item._BalmoralAction: -1,
    #     Item.CoverElaboration: -10,
    #     Item.CoverCredentials: -5,
    #     Item.CoverBackstory: -100,
    #     Item.EdictsOfTheFirstCity: 1
    # })

    # University
    add({
        Item.Action: -1,
        Item.CoverElaboration: -10,
        Item.CoverCredentials: -4,
        Item.CoverNuance: -6,
        Item.CoverBackstory: -100,
        Item.DreadfulSurmise: 1
    })

    # TODO must sell full identity, so free trades are too permissive

    add({
        Item._BalmoralAction: -1,
        Item._CoverTiesGeneric: -1,
        Item.CoverElaboration: -1,
        Item.CoverBackstory: -78,
        Item.MemoryOfMuchLesserSelf: 80
    })

    add({
        Item._BalmoralAction: -1,
        Item._CoverTiesGeneric: -1,
        Item.CoverElaboration: -1,
        Item.CoverBackstory: -78,
        Item.MagnificentDiamond: 16
    })



    # trade(0, {
    #     Item.CoverElaboration: -1,
    #     Item.ThirstyBombazineScrap: 1
    # })

    # trade(0, {
    #     Item.CoverElaboration: -1,
    #     Item.TouchingLoveStory: 1
    # })

    # trade(0, {
    #     Item.CoverElaboration: -1,
    #     Item.SwornStatement: 1
    # })

    # # Credenitals
    # trade(0, {
    #     Item.CoverCredentials: -1,
    #     Item.MemoryOfMuchLesserSelf: 1
    # })
    
    # trade(0, {
    #     Item.CoverCredentials: -1,
    #     Item.ThirstyBombazineScrap: 1
    # })

    # trade(0, {
    #     Item.CoverCredentials: -1,
    #     Item.TouchingLoveStory: 1
    # })

    # trade(0, {
    #     Item.CoverCredentials: -1,
    #     Item.SwornStatement: 1
    # })

    # # Nuance
    # trade(0, {
    #     Item.CoverNuance: -1,
    #     Item.MemoryOfMuchLesserSelf: 1
    # })

    # trade(0, {
    #     Item.CoverNuance: -1,
    #     Item.ThirstyBombazineScrap: 1
    # })

    # trade(0, {
    #     Item.CoverNuance: -1,
    #     Item.TouchingLoveStory: 1
    # })

    # trade(0, {
    #     Item.CoverNuance: -1,
    #     Item.SwornStatement: 1
    # })

    # # Witnesses
    # trade(0, {
    #     Item.CoverWitnessnes: -1,
    #     Item.MemoryOfMuchLesserSelf: 1
    # })

    # trade(0, {
    #     Item.CoverWitnessnes: -1,
    #     Item.ThirstyBombazineScrap: 1
    # })

    # trade(0, {
    #     Item.CoverWitnessnes: -1,
    #     Item.TouchingLoveStory: 1
    # })

    # trade(0, {
    #     Item.CoverWitnessnes: -1,
    #     Item.SwornStatement: 1
    # })

    # # Backstory
    # trade(0, {
    #     Item.CoverBackstory: -1,
    #     Item.MemoryOfMuchLesserSelf: 1
    # })

    # trade(0, {
    #     Item.CoverBackstory: -5,
    #     Item.MagnificentDiamond: 1
    # })

    # Grand Larcenies
    # check action costs

    add({
        Item._BalmoralAction: -1,
        Item.CoverTiesBazaar: -1,
        Item.CoverElaboration: -10,
        Item.CoverCredentials: -5,
        Item.CoverNuance: -5,
        Item.CoverBackstory: -80,

        Item.ScrapOfIvoryOrganza: 1
    })

    add({
        Item._BalmoralAction: -1,
        Item.Casing: -10,
        Item._CoverTiesGeneric: -1,
        Item.CoverBackstory: -80,
        Item.CoverElaboration: -10,
        Item.CoverNuance: -5,
        Item.CoverCredentials: -5,
        Item.PrismaticFrame: 1
    })

    # TODO: other cash outs

    ########################################################
    #                       Painting
    ########################################################

    # Start + finish costs
    # Does not include travel, present
    # add({
    #     Item._BalmoralAction: -2,
    #     Item.PaintersProgress: -6,
    #     Item.CompletedPainting: 1
    # })

    add({Item.PaintingIncendiary: -1, Item._PaintingAnyQuality: 1})
    add({Item.PaintingLuminosity: -1, Item._PaintingAnyQuality: 1})
    add({Item.PaintingNostalgic: -1, Item._PaintingAnyQuality: 1})

    # TODO: Nontrivial challenges (Persuasive 200)

    ###### Moonlight #####
    add({
        Item._BalmoralAction: -1,
        Item.Moonlit: -2,
        Item.MemoryOfMuchLesserSelf: -2,
        Item.MemoryOfLight: -10,

        Item.PaintingLuminosity: 1,
        Item.Inspired: 1
    })

    add({
        Item._BalmoralAction: -1,
        Item.Moonlit: -2,
        Item.MemoryOfMuchLesserSelf: -2,
        Item.MemoryOfLight: -10,

        Item.PaintingNostalgic: 1
    })

    ###### Subversive #####
    add({
        Item._BalmoralAction: -1,
        Item.VitalIntelligence: -1,

        Item.PaintingIncendiary: 1,
        Item.RomanticNotion: 15
    })

    add({
        Item._BalmoralAction: -1,
        Item.VitalIntelligence: -1,

        Item.PaintingNostalgic: 1
    })

    ###### Paint! #####
    add({
        Item._BalmoralAction: -1,
        Item.TouchingLoveStory: -5,

        Item.PaintingNostalgic: 1,
        Item.RomanticNotion: 15
    })

    add({
        Item._BalmoralAction: -1,
        Item.TouchingLoveStory: -3,

        Item.PaintingIncendiary: 1
    })

    # TODO: Confirm action costs for full carousel
    # 

    # 1 to start carousel
    # 6 to paint
    # 1 to finalize
    # 1 to travel to London
    # 1 to present
    # 1 to return back to Balmoral (or to get there, if start/end in London)

    add({
        Item._BalmoralAction: -2,
        Item.Action: -1,
        Item._UnveilYourPaintingLondon: -1,

        Item.PaintingNostalgic: -4,
        Item._PaintingAnyQuality: -2,
    
        Item.BottleOfFourthCityAirag: 1,
        Item.CellarOfWine: 1,
        Item.SwornStatement: 2
    })

    add({
        Item._BalmoralAction: -2,
        Item.Action: -1,
        Item._UnveilYourPaintingLondon: -1,
        
        Item.PaintingLuminosity: -4,
        Item._PaintingAnyQuality: -2,
    
        Item.ViennaOpening: 5,
        Item.SwornStatement: 5,
        Item.ParabolaLinenScrap: 1,
        Item.BazaarPermit: 1
    })

    add({
        Item._BalmoralAction: -2,
        Item.Action: -1,
        Item._UnveilYourPaintingLondon: -1,        
        
        Item.PaintingIncendiary: -4,
        Item._PaintingAnyQuality: -2,
    
        Item.SkeletonWithSevenNecks: 1,
        Item.SilentSoul: 1,
        Item.ThirstyBombazineScrap: 2
    })

    add({
        Item._BalmoralAction: -2,
        Item.Action: -1,
        Item._UnveilYourPaintingLondon: -1,        
        
        Item.PaintingIncendiary: -3,
        Item.PaintingNostalgic: -3,
    
        Item.DiscordantSoul: 1,
        Item.DirefulReflection: 1,
        Item.MourningCandle: 2
    })

    add({
        Item._BalmoralAction: -2,
        Item.Action: -1,
        Item._UnveilYourPaintingLondon: -1,        
        
        Item.PaintingIncendiary: -3,
        Item.PaintingLuminosity: -3,
    
        Item.NightWhisper: 1,
        Item.ViennaOpening: 5,
        Item.ThirstyBombazineScrap: 5,
        Item.BlackmailMaterial: 1
    })

    add({
        Item._BalmoralAction: -2,
        Item.Action: -1,
        Item._UnveilYourPaintingLondon: -1,        
        
        Item.PaintingNostalgic: -3,
        Item.PaintingLuminosity: -3,
    
        Item.BottleOfFourthCityAirag: 1,
        Item.MourningCandle: 10,
        Item.FavourInHighPlaces: 1
    })



    # TODO: Move to helicon house
    add({
        Item.Action: -1,
        Item.CompletedPainting: -1,
        Item._UnveilYourPaintingLondon: -1,
        Item._PaintingAnyQuality: -6,

        Item.HinterlandScrip: 125
    })