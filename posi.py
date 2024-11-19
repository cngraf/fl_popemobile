from enums import *
from helper.utils import *
from config import Config

# TODO: multiple files?

def add_trades(config: Config):
    trade = config.trade
    add = config.add
    player = config.player

    # HACK you don't actually lose most items/qualities; one-time thing

    # BSS - Are We Done?
    add(({
        Item.Action: -1,
        Item._PersonOfSomeLittleConsequence12: -1,
        Item.PersonOfSomeImportance: 1
    }))

    # BSS - Velocipede
    add({
        Item.Action: -1,
        # Item.Velocipede: 1,
        Item.BazaarPermit: -1,
        Item.StrongBackedLabour: -1,
        Item._PersonOfSomeLittleConsequence11: -1,
        Item._PersonOfSomeLittleConsequence12: 1,
    })

    # BSS - Morning for Business
    add({
        Item.Action: -1,
        Item._PersonOfSomeLittleConsequence10: -1,
        Item._PersonOfSomeLittleConsequence11: 1,
    })

    # Lodgings - A most interesting briefcase
    add({
        Item.Action: -1,
        Item._PersonOfSomeLittleConsequence9: -1,
        Item._PersonOfSomeLittleConsequence10: 1,
        # Item.Route_BazaarSideStreets: 1,
    })

    ################################################################
    #                     7 to 8
    ################################################################

    add({
        Item.Action: -1,
        Item.BringerOfDeath: -1,
        Item.FearsomeDuelist: -1,
        Item.ProcurerOfSavageBeasts: -1,

        Item._PersonOfSomeLittleConsequence8: -1,
        Item._PersonOfSomeLittleConsequence9: 1,
    })

    add({
        Item.Action: -1,
        Item.DarlingOfAmbassadorsBall: -1,
        Item.MementoOfPassion: -1,
        Item.BanishedFromCourt: -1,

        Item._PersonOfSomeLittleConsequence8: -1,
        Item._PersonOfSomeLittleConsequence9: 1,
    })

    add({
        Item.Action: -1,
        Item.ScholarOfTheCorrespondence: -1,
        Item.AppallingSecret: -20,
        Item.Nightmares: -15, # pyramidal level 5
        Item.FeaturingInTalesOfUniversity: -25,

        Item._PersonOfSomeLittleConsequence8: -1,
        Item._PersonOfSomeLittleConsequence9: 1,
    })

    add({
        Item.Action: -1,
        Item.MasterThief: -1,
        Item.FinePieceInTheGame: -1,

        Item._PersonOfSomeLittleConsequence8: -1,
        Item._PersonOfSomeLittleConsequence9: 1,
    })

    ################################################################
    #                     7 to 8
    ################################################################

    # CARD - A matter of the wardrobe (2.0x)
    # same total cost, no viable alternate sources
    # TODO buy these earlier for some benefit?
    add({
        Item.Action: -1,
        Item.Echo: -388.8,

        Item._PersonOfSomeLittleConsequence7: -1,
        Item._PersonOfSomeLittleConsequence8: 1,
    })

    # CARD - A respectable address (2.0)
    add({
        Item.Action: -1,
        Item.KeyToHandsomeTownhouse: -1,

        Item._PersonOfSomeLittleConsequence7: -1,
        Item._PersonOfSomeLittleConsequence8: 1,
    })

    add({
        Item.RomanticNotion: -500,
        Item.KeyToHandsomeTownhouse: 1
    })

    # CARD - A little hideaway (1.0x)
    # TODO skipping the 4-card options; assume they are not optimal

    # Around 50e in items
    # Little places to hide
    add({
        Item.Action: -1,
        Item.KeyToLairInMarshes: -1,
        Item.KeyToRooftopShack: -1,
        Item.KeyToSmokyFlophouse: -1,
        Item.KeyToCottageByObservatory: -1,
        Item.KeytoRoomsAboveBookshop: -1,
        Item.KeytoRoomsAboveGamblingDen: -1,

        Item._PersonOfSomeLittleConsequence7: -1,
        Item._PersonOfSomeLittleConsequence8: 1,        
    })

    add({
        Item.RatOnAString: -300,
        Item.KeyToLairInMarshes: 1
    })

    add({
        Item.PrimordialShriek: -300,
        Item.KeyToRooftopShack: 1
    })
    add({
        Item.PieceOfRostygold: -200,
        Item.KeyToSmokyFlophouse: 1
    })
    add({
        Item.JadeFragment: -300,
        Item.KeyToCottageByObservatory: 1
    })

    add({
        Item.WhisperedHint: -450,
        Item.KeytoRoomsAboveBookshop: 1
    })

    add({
        Item.NoduleOfDeepAmber: -300,
        Item.KeytoRoomsAboveGamblingDen: 1
    })

    # CARD - Friends and acquaintances (2.0x)
    # TODO skipping this one for now
    # Need 35 favours to go from 5 to 10
    # get ConnectedMasters at Christmas?
    # acquaintance option needs looking in to
    # Soldier - standard card with Dangerous 45
    # Functionary - rare success on Persuasive options (too random)
    # Singer - a couple options. Ending of MYN Watchful case, others
    # Forger - Prison, again
    # No way this is better than one of the housing options, right


    ################################################################
    #                     3 4 5 6
    ################################################################

    # Need 100 in each base stat WITH gear

    # Ladybones - Watchful
    add({
        Item.Action: -1,

        Item._PersonOfSomeLittleConsequence6: -1,
        Item._PersonOfSomeLittleConsequence7: 1,
    })

    # Spite - Shadowy
    add({
        Item.Action: -1,

        Item._PersonOfSomeLittleConsequence5: -1,
        Item._PersonOfSomeLittleConsequence6: 1,
    })

    # Veilgarden - Persuasive
    add({
        Item.Action: -1,

        Item._PersonOfSomeLittleConsequence4: -1,
        Item._PersonOfSomeLittleConsequence5: 1,
    })

    # Watchmaker's - Dangerous
    add({
        Item.Action: -1,

        Item._PersonOfSomeLittleConsequence3: -1,
        Item._PersonOfSomeLittleConsequence4: 1,
    })

    # Lodgings - Tea witht he Ambitious Barrister
    add({
        Item.Action: -1,

        Item._PersonOfSomeLittleConsequence2: -1,
        Item._PersonOfSomeLittleConsequence3: 1,
    })

    # Lodgins - Who is she?
    add({
        Item.Action: -1,

        Item._PersonOfSomeLittleConsequence1: -1,
        Item._PersonOfSomeLittleConsequence2: 1,
    })

    # Lodgins - Who is she?
    add({
        Item.Action: -1,

        Item._PersonOfSomeLittleConsequence1: 1,
    })


    ################################################################
    #                     Sufficient Importance options
    ################################################################

    '''
    Bringer of Death
    - End of cheesemonger storyline
        - not including these
        - assume easier to do Master Thief + Piece in the Game
    - Vendrick duel to the death
        - requires doing the Errant Duelist anyway

    Mr Inch / MYN 6 unlock
    - Fearsome Duelist 5

    Black Ribbon / MYN 5 unlock
    - Arachnologist 3

    Arachnologist unlock / 

    MYN 4 unlocks Silken Chapel

    MYN 3 unlocks Fighting Rings
    '''

    # Confont the Errant Duelist
    # Need 134 for 100%
    add({
        Item.Action: -1,
        Item._DuelingBlackRibbon_3: -1,

        Item._DuelingBlackRibbon_4: 1,
        Item.BringerOfDeath: 1,
    })

    # Need RB 28 (lvl 7) for 100% 
    add({
        Item.RunningBattle: -15,
        Item.PieceOfRostygold: 432,
        Item.FearsomeDuelist: 2
    })
    
    # Need 28/7 for 100%
    add({
        Item.TheHuntIsOn: -15,

        Item.PrimordialShriek: 270,
        Item.ProcurerOfSavageBeasts: 1 
    })