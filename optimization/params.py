from enums import *
import player as player

actions_per_day = 120
cards_per_day = 40

# Optimize `solution_output` per `solution_input`
solution_input = Item.Action
solution_output = Item.Echo

active_player = player.player_endgame_f2p

story_qualities = {
    Item.BagALegend: 4000,

    # Item.ListOfAliasesWrittenInGant: 1,
    Item.SetOfCosmogoneSpectacles: 1,

    Item._AllianceWithBigRat: 1,
}

fate_qualities = {
    Item.AcquaintanceTheClamorousCartographer: 6
}

active_player.qualities.update(story_qualities)
active_player.qualities.update(fate_qualities)


# Core constraint setup
core_constraint = {
    Item.Constraint: 1,
    solution_input: actions_per_day * 7,

    Item.GlimEncrustedCarapace: 10,

    Item._RatMarketRotation: 1,
    Item._BoneMarketRotation: 1,
    Item._VisitFromTimeTheHealer: 1,

    Item._CardDraws: cards_per_day * 7,
}