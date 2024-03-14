from enums import *
from utils import *

def add_trades(active_player, config):
    trade = config.trade
    
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