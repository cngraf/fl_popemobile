from enums import *
from utils import *

def add_trades(config):
    add = config.add
    
    for i in range(0, 11):
        visit_length = 2 ** i
        add({
            Item._UpperRiverRoundTrip: -1,
            Item.Action: -1 * visit_length,
            Item._MarigoldAction: visit_length,
        })

    for item in (
        Item.MourningCandle,
        Item.HeadlessSkeleton,
        Item.ViennaOpening
    ):
        add({
            Item._MarigoldAction: -1,
            item: 1
        })