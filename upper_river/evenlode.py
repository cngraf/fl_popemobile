from enums import *
from helper.utils import *
from config import Config

def renown_scaling(renown: int):
    pow = -0.2 * (renown - 22)
    return 200/(1 + math.pow(math.e, pow))

def add_trades(config: Config):
    add = config.add
    player = config.player

    add({
        Item._UpperRiverRoundTrip: -1,
        Item.Action: -40,
        Item._EvenlodeAction: 40
    })

    ###############################################
    #               Barristering
    ###############################################

    # TODO wiki inconsistent re: whether rewards scale above 9
    # check what's achievable for each case
    prestige = 9

    # TODO various unique resolution bonuses from items
    # TODO confirm prosperity values from Oct 11 patch
    prosperity_per_prestige = 25 if player.get(Item.InvolvedInARailwayVenture) >= 140 else 0

    #########################
    # Magistracy v Accused
    #########################

    '''
    Prosecution (3)
    0 - Either option (+1)
    1 - Form of honour (+3) (Cave-Aged Code of Honour)
    2 - Quiz the accused (+1)
    3 - Close out (+2)
    100% @ Mith 17
    '''

    prosection_1_prestige = 9
    add({
        Item._EvenlodeAction: -6,
        
        Item.LegalDocument: 2,
        Item.FoxfireCandleStub: renown_scaling(player.get(Item.RenownConstables)),

        Item.JournalOfInfamy: prosection_1_prestige,
        Item.DubiousTestimony: prosection_1_prestige - 25,
        Item.Suspicion: - (prosection_1_prestige + 5),
        Item.SwornStatement: 1,
        Item.HinterlandProsperity: prosection_1_prestige * prosperity_per_prestige
    })

    '''
    Defense (3)
    0 - Either option (+1)
    1 - Most rigorous judge (+2) (An Assuming Judge)
    2 - Explore (+2)
    3 - Dismantle (+2)
    max 10 with judge, 9 without
    '''

    defense_1_prestige = 10
    add({
        Item._EvenlodeAction: -6,
        
        Item.ComprehensiveBribe: 2,
        Item.WhisperedHint: renown_scaling(player.get(Item.RenownCriminals)),

        Item.JournalOfInfamy: defense_1_prestige - 25,
        Item.DubiousTestimony: defense_1_prestige,
        Item.SwornStatement: 1,
        Item.HinterlandProsperity: defense_1_prestige * prosperity_per_prestige
    })


    #########################
    # Rats v Urchins
    #########################

    # Rats v Urchins

    '''
    Prosecution (0)
    0 - Either option (+1)
    1 - Oath or Hell (+3)
    2 - Speak freely (+1)
    3 - Close out (+2)
    100% @ Mith 17
    '''

    prosection_2_prestige = 7
    add({
        Item._EvenlodeAction: -6,
        
        Item.VengeRatCorpse: 25,
        Item.JadeFragment: renown_scaling(player.get(Item.SympatheticAboutRatlyConcerns)),

        Item.JournalOfInfamy: prosection_2_prestige,
        Item.DubiousTestimony: prosection_2_prestige,
        Item.SwornStatement: 1,
        Item.HinterlandProsperity: prosection_2_prestige * prosperity_per_prestige
    })


    defense_2_prestige = 7
    add({
        Item._EvenlodeAction: -6,
        
        Item.StormThrenody: 1,
        Item.RatOnAString: renown_scaling(player.get(Item.RenownUrchins)),

        Item.JournalOfInfamy: defense_2_prestige,
        Item.DubiousTestimony: defense_2_prestige,
        Item.SwornStatement: 1,
        Item.HinterlandProsperity: defense_2_prestige * prosperity_per_prestige
    })


    #########################
    # Tomb vs Hell
    #########################

    prosection_2_prestige = 9
    add({
        Item._EvenlodeAction: -6,
        
        Item.PresbyteratePassphrase: 5,
        Item.DropOfPrisonersHoney: 0.5 * renown_scaling(player.get(Item.RenownTombColonies)),

        Item.JournalOfInfamy: prosection_2_prestige,
        Item.DubiousTestimony: prosection_2_prestige,
        Item.SwornStatement: 1,
        Item.HinterlandProsperity: prosection_2_prestige * prosperity_per_prestige
    })

    defense_2_prestige = 8
    add({
        Item._EvenlodeAction: -6,
        
        Item.MuscariaBrandy: 5,
        Item.NevercoldBrassSliver: renown_scaling(player.get(Item.RenownHell)),

        Item.JournalOfInfamy: defense_2_prestige,
        Item.DubiousTestimony: defense_2_prestige,
        Item.SwornStatement: 1,
        Item.HinterlandProsperity: defense_2_prestige * prosperity_per_prestige
    })


    #########################
    # Gondoliers v Society
    #########################

    prosection_4_prestige = 9
    add({
        Item._EvenlodeAction: -6,
        Item.PreservedSurfaceBlooms: -20,
        
        Item.MortificationOfAGreatPower: 1,
        Item.ShardOfGlim: renown_scaling(player.get(Item.RenownDocks)),

        Item.JournalOfInfamy: prosection_4_prestige,
        Item.DubiousTestimony: prosection_4_prestige,
        Item.SwornStatement: 1,
        Item.HinterlandProsperity: prosection_4_prestige * prosperity_per_prestige
    })

    defense_4_prestige = 7
    add({
        Item._EvenlodeAction: -6,
        
        Item.MirrorcatchBox: 1,
        Item.ExtraordinaryImplication: 4,
        Item.MoonPearl: renown_scaling(player.get(Item.RenownSociety)),

        Item.JournalOfInfamy: defense_4_prestige,
        Item.DubiousTestimony: defense_4_prestige,
        Item.SwornStatement: 1,
        Item.HinterlandProsperity: defense_4_prestige * prosperity_per_prestige
    })               


    ###############################################
    #               Diving
    ###############################################

    add({
        Item._EvenlodeAction: -8,
        Item.FinalBreath: -75,
        Item.MortificationOfAGreatPower: 1
    })

    # Dive to depth 5/6
    # When Airs 25-50, Observe a gilled lamp-cat
    # When Airs 51-75, Go spear-fishing
    # When Airs 76-100, Study drowned architecture (not 100%) 
    # Else, cycle airs with ascend/descend

    diving_length = 100
    add({
        Item._EvenlodeAction: - (6 + diving_length),
        Item.IncisiveObservation: 9.5 * diving_length/4,
        Item.DeepZeeCatch: 6.5 * diving_length/4,
        Item.FinBonesCollected: 2 * diving_length/4,
        Item.ExtraordinaryImplication: 0.75 * diving_length/4,
        Item.Nightmares: 2 * 0.25 * diving_length/4,
        
        Item.FinalBreath: -75,
        Item.MortificationOfAGreatPower: 1
    })

    # add({
    #     Item._EvenlodeAction: -1,
    #     Item.IncisiveObservation: 10
    # })

    # add({
    #     Item._EvenlodeAction: -1,
    #     Item.DeepZeeCatch: 7,
    #     Item.FinBonesCollected: 2
    # })