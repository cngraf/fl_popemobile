from enums import *
from helper.utils import *
from config import Config

def add_trades(config: Config):
    add = config.add
    trade = config.trade

    for favour in (
        Item.FavBohemians,
        Item.FavChurch,
        Item.FavCriminals,
        Item.FavDocks,
        Item.FavSociety):
        add({
            favour: -7,
            Item.Tribute: 11
        })

    for item, cost, tribute in (
        (Item.WinsomeDispossessedOrphan, 1, 20),
        (Item.MountainSherd, 1, 22),

        # TODO check tapering on the rest of these
        (Item.Echo, 25, 10),
        (Item.MagnificentDiamond, 1, 5),
        (Item.PuzzleDamaskScrap, 1, 5),
        (Item.CellarOfWine, 1, 5),
        # (Item.OdeToElderContinent, 1, 5),
        (Item.MemoryOfLight, 50, 10),
        (Item.MountainSherd, 1, 35),
        (Item.RoyalBlueFeather, 16, 4),
        (Item.CorrespondencePlaque, 50, 10),
        (Item.StrongBackedLabour, 1, 2),
        (Item.LuckyWeasel, 30, 5),
        # (Item.DeshriekedMandrake, 1, 5),
        # (Item.StarvelingCat, 1, -5)
    ):
        add({
            Item.Action: -1,
            item: -cost,
            Item.Tribute: tribute
        })

    # London => CWE: ~1500 plunder, 6.25 actions
    # CWE => London: ~1600 plunder, 7.25 actions

    add({
        Item.Action: -13.5,
        Item.StashedTreasure: 3100,
        Item._WakefulEyeRoundTrip: 1,
        Item.ZeeLegs: 2
    })

    visit_length = 13
    add({
        Item._WakefulEyeRoundTrip: -1,
        Item.Action: -visit_length,
        Item._WakefulEyeAction: visit_length
    })

    add({
        Item._WakefulEyeAction: -1,
        Item.Tribute: -20,
        Item.SearingEnigma: 1
    })

    add({
        Item._WakefulEyeAction: -1,
        Item.Tribute: -20,
        Item.NightWhisper: 1
    })

    add({
        Item._WakefulEyeAction: -1,
        Item.Tribute: -20,
        Item.PrimaevalHint: 1
    })

    add({
        Item._WakefulEyeAction: -1,
        Item.Tribute: -20,
        Item.FavourInHighPlaces: 5
    })    