from enums import *
from helper.utils import *
from config import Config

def add_trades(config: Config):
    add = config.add

    add({
        Item.Action: -20,
        Item._ImprisonedInNewNegate: -1
    })