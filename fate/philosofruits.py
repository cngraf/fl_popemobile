from enums import *
from utils import *

def add_trades(active_player, trade):
    # -------------------
    # --- Philosofruits
    # -------------------

    # TODO: travel cost estimate
    # using wiki values
    
    lost_draw_cost = 0

    trade(5, {
        Item.Echo: lost_draw_cost * 5,
        Item.BlackmailMaterial: 1,
        Item.AnIdentityUncovered: 3
    })

    trade(5, {
        Item.Echo: lost_draw_cost * 5,
        Item.AntiqueMystery: 1,
        Item.PresbyteratePassphrase: 3
    })

    trade(5, {
        Item.Echo: lost_draw_cost * 5,
        Item.UncannyIncunabulum: 1,
        Item.ExtraordinaryImplication: 3
    })

    trade(13, {
        Item.Echo: lost_draw_cost * 13,
        Item.ComprehensiveBribe: 4,
    })

    trade(10, {
        Item.Echo: lost_draw_cost * 10,
        Item.CorrespondencePlaque: 90,
    })

    trade(20, {
        Item.Echo: lost_draw_cost * 20,
        Item.BottleOfFourthCityAirag: 1,
        Item.CellarOfWine: 2
    })

    trade(11, {
        Item.Echo: lost_draw_cost * 11,
        Item.StormThrenody: 4
    })