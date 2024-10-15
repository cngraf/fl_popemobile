from enums import *
import player as player

actions_per_day = 120
cards_per_day = 40

# Optimize `solution_output` per `solution_input`
solution_input = Item.Action
solution_output = Item.Echo

active_player = player.player_endgame_f2p

add_qualities = {
    # Item.BagALegend: 4000,

    # Item.ListOfAliasesWrittenInGant: 1,

    # Item._AllianceWithBigRat: 1,
}

active_player.qualities.update(add_qualities)


# Core constraint setup
core_constraint = {
    Item.Constraint: 1,
    solution_input: actions_per_day * 7,

    Item._RatMarketRotation: 1,
    Item._BoneMarketRotation: 1,
    Item._VisitFromTimeTheHealer: 1,

    Item._CardDraws: cards_per_day * 7,
}