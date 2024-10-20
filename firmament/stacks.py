import math
from enum import Enum, auto

from enums import *
import helper.utils as utils
from config import Config
from player import Player

def add_trades(config: Config):
    add = config.add

    add({
        Item._MidnightMoonAction: -1,
        Item._StacksAction: 1
    })
    add({
        Item._ZenithAction: -1,
        Item._StacksAction: 1
    })

    # Results from simulations/stacks2 using my own stats, mostly ~330/15
    # W/o cartographer unless required
    # ignoring items less than +/- 0.01 EPA i.e. bones and rats
    # also ignored menaces when they were less than 2 per run

    # TODO double check these. ran again and got somewhat diff results

    # Banned Works
    add({
        Item._StacksAction: -23.2,
        Item.CausticApocryphon: 8.55,
        Item.TantalisingPossibility: 210,
        Item.GlimpseOfAnathema: 0.045,
        Item.Wounds: 1,
        Item.Nightmares: 1
    })

    # Dead Stars 1
    add({
        Item._StacksAction: -23,        
        Item.GlimEncrustedCarapace: 0.95,
        Item.TantalisingPossibility: 655,
        Item.ShardOfGlim: 380,
        Item.GlimpseOfAnathema: 0.045,
        Item.Wounds: 1,
        Item.Nightmares: 1,        
    })    

    # Dead Stars 2
    add({        
        Item._StacksAction: -23,        
        Item.RoofChart: 38,
        Item.TantalisingPossibility: 180,
        Item.GlimpseOfAnathema: 0.045,
        Item.Wounds: 1,
        Item.Nightmares: 1,        
    })

    # Precipice 1
    add({        
        Item._StacksAction: -23,        
        Item.Anticandle: 9.5,
        Item.FragmentOfTheTragedyProcedures: 0.95,
        Item.RelicOfTheFifthCity: 9.5,
        Item.TantalisingPossibility: 215,
        Item.GlimpseOfAnathema: 0.05,
        Item.Nightmares: 1,
    })
    
    # Precipice 2
    add({        
        Item._StacksAction: -23,        
        Item.Anticandle: 9.5,
        Item.TempestuousTale: 9.5,
        Item.TantalisingPossibility: 190,
        Item.RelicOfTheFifthCity: 5.7,
        Item.MagnificentDiamond: 4.7,
        Item.GlimpseOfAnathema: 0.05,
        Item.Nightmares: 1,  
    })

    # Cartographer
    if config.player.get(Item.AcquaintanceTheClamorousCartographer):
        add({        
            Item._StacksAction: -23.5,        
            Item.TantalisingPossibility: 171,
            Item.PuzzlingMap: 0.95,
            Item.OneiromanticRevelation: 0.95,
            Item.StormThrenody: 1.9,
            Item.VolumeOfCollatedResearch: 5.7,
            Item.GlimpseOfAnathema: 0.05,
            Item.Nightmares: 1,
        })

    # add({
    #     Item.Anticandle: -1,
    #     Item.Echo: 2.5
    # })