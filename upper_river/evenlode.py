from enums import *
from helper.utils import *
from config import Config

def renown_scaling(renown: int):
    pow = -0.2 * (renown - 22)
    return 200/(1 + math.pow(math.e, pow))

def add_trades(config: Config):
    trade = config.trade
    add = config.add
    player = config.player

    add({
        Item._UpperRiverRoundTrip: -1,
        Item.Action: -40,
        Item._EvenlodeAction: 40
    })
    
    # # TODO: upper river deck stuff
    # trade.railway_card("Digs in the Magistracy of the Evenlode",
    #     Rarity.Standard,
    #     Location.TheMagistracyOfTheEvenlode,
    #     True, {
    #     Item.DigsInEvenlode: 1
    # })

    # trade(1, {
    #     # Item.DigsInEvenlode: -1,
    #     Item.SurveyOfTheNeathsBones: -120,
    #     Item.PalaeontologicalDiscovery: 5
    # })

    # trade(1, {
    #     # Item.DigsInEvenlode: -1,
    #     Item.SurveyOfTheNeathsBones: -140,
    #     Item.PalaeontologicalDiscovery: 6
    # })

    # # specific treasure only
    # trade(1, {
    #     # Item.DigsInEvenlode: -1,
    #     Item.SurveyOfTheNeathsBones: -240,
    #     Item.PalaeontologicalDiscovery: 10
    # })

    ###############################################
    #               Barristering
    ###############################################

    # TODO wiki inconsistent re: whether rewards scale above 9
    # check what's achievable for each case
    prestige = 9

    # TODO various unique resolution bonuses

    # Magistracy v Accused
    add({
        Item._EvenlodeAction: -6,
        
        Item.LegalDocument: 2,
        Item.FoxfireCandleStub: renown_scaling(player.get(Item.RenownConstables)),

        Item.JournalOfInfamy: prestige,
        Item.DubiousTestimony: prestige - 25,
        Item.SwornStatement: 1
    })

    add({
        Item._EvenlodeAction: -6,
        
        Item.ComprehensiveBribe: 2,
        Item.WhisperedHint: renown_scaling(player.get(Item.RenownCriminals)),

        Item.JournalOfInfamy: prestige - 25,
        Item.DubiousTestimony: prestige,
        Item.SwornStatement: 1
    })

    # Rats v Urchins
    add({
        Item._EvenlodeAction: -6,
        
        Item.VengeRatCorpse: 25,
        Item.JadeFragment: renown_scaling(player.get(Item.SympatheticAboutRatlyConcerns)),

        Item.JournalOfInfamy: prestige,
        Item.DubiousTestimony: prestige,
        Item.SwornStatement: 1
    })

    add({
        Item._EvenlodeAction: -6,
        
        Item.StormThrenody: 1,
        Item.RatOnAString: renown_scaling(player.get(Item.RenownUrchins)),

        Item.JournalOfInfamy: prestige,
        Item.DubiousTestimony: prestige,
        Item.SwornStatement: 1
    })

    # Tomb-Colonists vs Devils
    add({
        Item._EvenlodeAction: -6,
        
        Item.PresbyteratePassphrase: 5,
        Item.DropOfPrisonersHoney: 0.5 * renown_scaling(player.get(Item.RenownTombColonies)),

        Item.JournalOfInfamy: prestige,
        Item.DubiousTestimony: prestige,
        Item.SwornStatement: 1
    })

    add({
        Item._EvenlodeAction: -6,
        
        Item.MuscariaBrandy: 5,
        Item.NevercoldBrassSliver: renown_scaling(player.get(Item.RenownHell)),

        Item.JournalOfInfamy: prestige,
        Item.DubiousTestimony: prestige,
        Item.SwornStatement: 1
    })


    # Gondoliers vs Society
    add({
        Item._EvenlodeAction: -6,
        Item.PreservedSurfaceBlooms: -20,
        
        Item.MortificationOfAGreatPower: 1,
        Item.ShardOfGlim: renown_scaling(player.get(Item.RenownDocks)),

        Item.JournalOfInfamy: prestige,
        Item.DubiousTestimony: prestige,
        Item.SwornStatement: 1
    })

    add({
        Item._EvenlodeAction: -6,
        
        Item.MirrorcatchBox: 1,
        Item.ExtraordinaryImplication: 4,
        Item.MoonPearl: renown_scaling(player.get(Item.RenownSociety)),

        Item.JournalOfInfamy: prestige,
        Item.DubiousTestimony: prestige,
        Item.SwornStatement: 1
    })               
