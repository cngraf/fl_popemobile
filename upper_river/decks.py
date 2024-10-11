from enums import *
from helper.utils import *

def add_trades(config):
    add = config.add

    ################################################################################
    ###                          Batch 1                                         ###
    ################################################################################
    # "Graduate Whale" setup
    # - no hellworm
    # - statues, even where suboptimal
    # - no Clay Highwayman card
    # - whatever darkness value I felt like having
    # - 0 banditry, -1 banditry EV
    # - 5.68 EV threshold
    # - all favours valued @ 5.59 E ea.
    # - econ input clamping disabled
    # - favour input clamping enabled
    # - item-based unlock requirements disabled 

    # 100 runs of 1000 actions ea.
    # rounded when I felt like it
    
    # Player Max Stats:
    # Stat                          Value
    # ----------------------------------------
    # dangerous                     334
    # watchful                      334
    # persuasive                    334
    # shadowy                       334
    # player_of_chess               18
    # zeefaring                     18
    # monstrous_anatomy             18
    # mithridacy                    18
    # artisan_of_the_red_science    18
    # kataleptic_toxicology         18
    # shapeling_arts                18
    # glasswork                     18
    # reduce_wounds                 0
    # reduce_nightmares             0
    # reduce_scandal                0
    # reduce_suspicion              0
    # zailing_speed                 55
    # zubmersibility                1
    # luxurious                     0
    # reduce_tw                     0

    # Initial Items & Qualities:
    # ----------------------------------------
    # ColourAtTheChessboard                        1
    # TrainLuxuries                                6
    # TrainDefences                                6
    # TrainBaggageAccomodations                    6
    # SeeingBanditryInTheUpperRiver                0
    # EalingGardensCommemorativeDevelopment        99
    # JerichoLocksCommemorativeDevelopment         99
    # MagistracyOfEvenlodeCommemorativeDeve...     99
    # BalmoralCommemorativeDevelopment             99
    # StationVIIICommemorativeDevelopment          99
    # BurrowInfraMumpCommemorativeDevelopment      99
    # MoulinCommemorativeDevelopment               99
    # HurlersCommemorativeDevelopment              99
    # MarigoldCommemorativeDevelopment             99
    # EalingGardensDarkness                        28.0
    # JerichoLocksDarkness                         28.0
    # MagistracyOfEvenlodeDarkness                 28.0
    # BalmoralDarkness                             1.0
    # StationVIIIDarkness                          1.0
    # BurrowInfraMumpDarkness                      15.0
    # MoulinDarkness                               15.0
    # HurlersDarkness                              15.0


    add({
        Item._MarigoldAction: -1000,
        Item._CardDraws: -6000,
        
        Item.ProscribedMaterial: 75000,
        Item.FavChurch: 1000
    })

    add({
        Item._HurlersAction: -1000,
        Item._CardDraws: -5650,
        
        Item.ProscribedMaterial: 60000,
        Item.VolumeOfCollatedResearch: -2400,
    })

    add({
        Item._MoulinAction: -1000,
        Item._CardDraws: -7000,
        
        Item.ProscribedMaterial: 75000,
        Item.FavChurch: 1000
    })

    add({
        Item._BurrowAction: -1000,
        Item._CardDraws: -3500,
        Item.MoonPearl: -325_000,
        
        Item.ProscribedMaterial: 37500,
        Item.FavChurch: 500,
        Item.VerseOfCounterCreed: 500
    })

    add({
        Item._StationViiiAction: -1000,
        Item._CardDraws: -7000,
        
        Item.ProscribedMaterial: 75000,
        Item.FavChurch: 1000
    })

    add({
        Item._BalmoralAction: -1000,
        Item._CardDraws: -6000,
        
        Item.ProscribedMaterial: 75000,
        Item.FavChurch: 1000
    })

    add({
        Item._JerichoAction: -10.00,
        Item._CardDraws: -41.00,
        
        Item.ProscribedMaterial: 38.400,
        Item.StrongBackedLabour: 24.35,
        Item.FavChurch: 0.24
    })

    add({
        Item._EalingAction: -1000,
        Item._CardDraws: -9600,
        
        Item.ProscribedMaterial: 75000,
        Item.FavChurch: 1000
    })

    ################################################################################
    ###                          Batch 2                                         ###
    ################################################################################
    # same as Batch 1, except:
    # - ev threshold is 5.5
    # - 1.2 scrip EV multiplier
    # - only did 200 actions per run

    # tried to make the rounding work, but not that hard
    # if two locations have the same ratios of played cards, copied their outputs

    # 72 jurisdictional dispute
    # 72 halfway to hell
    # 56 fungiculturalist
    add({
        Item._EalingAction: -200,
        Item._CardDraws: -700,
        Item.VerseOfCounterCreed: -72,
        Item.NightsoilOfTheBazaar: -560,
        
        Item.HinterlandScrip: 2600,
        Item.HandPickedPeppercaps: 1176,
        Item.MovesInTheGreatGame: 685,
        Item.Nightmares: 10,
    })

    # plays the exact same cards as ealing, with smaller deck
    add({
        Item._JerichoAction: -200,
        Item._CardDraws: -580,
        Item.VerseOfCounterCreed: -72,
        Item.NightsoilOfTheBazaar: -560,
        
        Item.HinterlandScrip: 2600,
        Item.HandPickedPeppercaps: 1176,
        Item.MovesInTheGreatGame: 685,
        Item.Nightmares: 10,
    })

    # 54 jurisdictional dispute
    # 53 halfway to hell
    # 52 balmoral in gaslight
    # 41 fungiculturalist
    add({
        Item._BalmoralAction: -200,
        Item._CardDraws: -320,
        Item.VerseOfCounterCreed: -54,
        Item.NightsoilOfTheBazaar: -408,
        
        Item.HinterlandScrip: 2523,
        Item.HandPickedPeppercaps: 857,
        Item.MovesInTheGreatGame: 505,
        Item.Nightmares: 7,
    })

    # same split as ealing, jericho
    add({
        Item._StationViiiAction: -200,
        Item._CardDraws: -510,
        Item.VerseOfCounterCreed: -72,
        Item.NightsoilOfTheBazaar: -560,
        
        Item.HinterlandScrip: 2600,
        Item.HandPickedPeppercaps: 1176,
        Item.MovesInTheGreatGame: 685,
        Item.Nightmares: 10
    })

    # 53 jurisdictional dispute
    # 53 halfway to hell
    # 53 burrow in heavenly light
    # 41 fungiculturalist
    add({
        Item._BurrowAction: -200,
        Item._CardDraws: -375,
        Item.NightsoilOfTheBazaar: -414,
        Item.MoonPearl: -34650,
        
        Item.HinterlandScrip: 1910,
        Item.HandPickedPeppercaps: 870,
        Item.MovesInTheGreatGame: 500,
        Item.Nightmares: 7,
    })

    # Same ratios as Burrow, but with statue instead of lighting
    add({
        Item._MoulinAction: -200,
        Item._CardDraws: -375,
        Item.NightsoilOfTheBazaar: -414,
        Item.VerseOfCounterCreed: -53,
        
        Item.HinterlandScrip: 1910,
        Item.HandPickedPeppercaps: 870,
        Item.MovesInTheGreatGame: 500,
        Item.FavTombColonies: 53,
        Item.Nightmares: 7,
    })        

    # ealing split
    add({
        Item._EalingAction: -200,
        Item._CardDraws: -700,
        Item.VerseOfCounterCreed: -72,
        Item.NightsoilOfTheBazaar: -560,
        
        Item.HinterlandScrip: 2600,
        Item.HandPickedPeppercaps: 1176,
        Item.MovesInTheGreatGame: 685,
        Item.Nightmares: 10,
    })

    # ealing split
    add({
        Item._HurlersAction: -200,
        Item._CardDraws: -510,
        Item.VerseOfCounterCreed: -72,
        Item.NightsoilOfTheBazaar: -560,
        
        Item.HinterlandScrip: 2600,
        Item.HandPickedPeppercaps: 1176,
        Item.MovesInTheGreatGame: 685,
        Item.Nightmares: 10,
    })

    # ealing split
    add({
        Item._MarigoldAction: -200,
        Item._CardDraws: -430,
        Item.VerseOfCounterCreed: -72,
        Item.NightsoilOfTheBazaar: -560,
        
        Item.HinterlandScrip: 2600,
        Item.HandPickedPeppercaps: 1176,
        Item.MovesInTheGreatGame: 685,
        Item.Nightmares: 10,
    })