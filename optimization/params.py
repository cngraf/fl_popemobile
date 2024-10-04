from enums import *
import player as player

input_per_cycle = 7 * 120

optimize_input = Item.Action
optimization_target = Item.Echo

# Core constraint setup
core_constraint = {
    Item.Constraint: 1,
    optimize_input: input_per_cycle,

    Item._RatMarketRotation: 1,
    Item._BoneMarketRotation: 1,
    Item._VisitFromTimeTheHealer: 1,

    Item._CardDraws: 7 * 30
}

active_player = player.player_generic_licentiate