from enums import *
from helper.utils import *

def add_trades(config):
    trade = config.trade
    trade(1, {
        Item.HeartsGameExploits: 1
    })

    trade(1, {
        Item.HeartsGameExploits: -5,
        Item.Echo: 12.5,
        Item.WhirringContraption: 1
    })

    trade(1, {
        Item.HeartsGameExploits: -14,
        Item.BessemerSteelIngot: 100
    })

    trade(1, {
        Item.HeartsGameExploits: -18,
        Item.MortificationOfAGreatPower: 1
    })

    trade(1, {
        Item.HeartsGameExploits: -25,
        Item.SaltSteppeAtlas: 1,
        Item.PuzzlingMap: 4,
        Item.PartialMap: 4,
        Item.MapScrap: 5
    })

    trade(1, {
        Item.HeartsGameExploits: -65,
        Item.IntriguersCompendium: 1
    })

    trade(1, {
        Item.HeartsGameExploits: -65,
        Item.LeviathanFrame: 1
    })

    trade(1, {
        Item.HeartsGameExploits: -65,
        Item.ElementalSecret: 1
    })

    trade(1, {
        Item.HeartsGameExploits: -65,
        Item.StarstoneDemark: 1
    })

    trade(1, {
        Item.HeartsGameExploits: -80,
        Item.ScrapOfIvoryOrganza: 1
    })
