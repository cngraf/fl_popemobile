from enums import *
# from helper.utils import *
import helper.utils as utils
from config import Config
from player import Player
from decks.deck import *

def add_trades(config: Config):
    add = config.add
    player = config.player

    # VERY rough approximation

    favour_card_frequency = 0.334
    unique_favours = 12
    specific_favour_per_card = favour_card_frequency/unique_favours

    add({
        Item._CardDraws: -1,
        Item.CL_Bohemians:  specific_favour_per_card,
        Item.CL_Church:     specific_favour_per_card,
        Item.CL_Constables: specific_favour_per_card,
        Item.CL_Criminals:  specific_favour_per_card,
        Item.CL_Docks:      specific_favour_per_card,
        Item.CL_GreatGame:  specific_favour_per_card,
        Item.CL_Hell:       specific_favour_per_card,
        Item.CL_Revolutionaries: specific_favour_per_card,
        Item.CL_RubberyMen: specific_favour_per_card,
        Item.CL_Society:    specific_favour_per_card,                           
        Item.CL_TombColonies: specific_favour_per_card,                           
        Item.CL_Urchins:    specific_favour_per_card,       
    })

    add({
        Item.Action: -1,
        Item.CL_Bohemians: -1,
        Item.FavBohemians: 1
    })

    add({
        Item.Action: -1,
        Item.CL_Church: -1,
        Item.FavChurch: 1
    })

    add({
        Item.Action: -1,
        Item.CL_Constables: -1,
        Item.FavConstables: 1
    })

    add({
        Item.Action: -1,
        Item.CL_Criminals: -1,
        Item.FavCriminals: 1
    })

    add({
        Item.Action: -1,
        Item.CL_Docks: -1,
        Item.FavDocks: 1
    })

    add({
        Item.Action: -1,
        Item.CL_GreatGame: -1,
        Item.FavGreatGame: 1
    })

    add({
        Item.Action: -1,
        Item.CL_Hell: -1,
        Item.FavHell: 1
    })

    add({
        Item.Action: -1,
        Item.CL_Revolutionaries: -1,
        Item.FavRevolutionaries: 1
    })

    add({
        Item.Action: -1,
        Item.CL_RubberyMen: -1,
        Item.FavRubberyMen: 1
    })

    add({
        Item.Action: -1,
        Item.CL_Society: -1,
        Item.FavSociety: 1
    })

    add({
        Item.Action: -1,
        Item.CL_TombColonies: -1,
        Item.FavTombColonies: 1
    })

    add({
        Item.Action: -1,
        Item.CL_Urchins: -1,
        Item.FavUrchins: 1
    })