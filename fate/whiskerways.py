from enums import *
from utils import *
from config import Config

'''
# TODO: not properly constrained
need to revisit this later and figure out a better way to handle variable length
'''

def add_trades(config: Config):
    player = config.player
    trade = config.trade

    trade(1, {
        Item.MythicPotential: 25
    })

    # assumes 50% alternate success rate
    trade(1, {
        Item.MythicPotential: -10,
        Item.MoralisingDevelopment: 3.5
    })

    trade(1, {
        Item.ExtraordinaryImplication: -2,
        Item.MoralisingDevelopment: 5
    })

    trade(1, {
        Item.EmeticRevelation: -1,
        Item.MoralisingDevelopment: 8.5
    })

    trade(1, {
        Item.MythicPotential: -10,
        Item.HeroicRally: 3.5
    })

    trade(1, {
        Item.MemoryOfMuchLesserSelf: -2,
        Item.HeroicRally: 5
    })

    trade(1, {
        Item.MagnificentDiamond: -1,
        Item.MoralisingDevelopment: 8.5
    })

    trade(1, {
        Item.MythicPotential: -10,
        Item.InscrutableTwist: 3.5
    })

    trade(1, {
        Item.MourningCandle: -2,
        Item.InscrutableTwist: 5
    })

    trade(1, {
        Item.PuzzlingMap: -1,
        Item.InscrutableTwist: 8.5
    })

    # Payouts
    trade(1, {
        Item.MythicPotential: -100,
        Item.AntiqueMystery: 1,
        Item.ExtraordinaryImplication: 3,
        Item.CrypticClue: 300,
        Item.WhiskerwaysSecondaryPayout: 24
    })

    trade(1, {
        Item.MythicPotential: -100,
        Item.BejewelledLens: 1,
        Item.VolumeOfCollatedResearch: 3,
        Item.CrypticClue: 300,
        Item.WhiskerwaysSecondaryPayout: 24
    })

    trade(1, {
        Item.MythicPotential: -100,
        Item.StormThrenody: 1,
        Item.TouchingLoveStory: 3,
        Item.CrypticClue: 300,
        Item.WhiskerwaysSecondaryPayout: 24
    })

    trade(0, {
        Item.MoralisingDevelopment: -24,
        Item.WhiskerwaysSecondaryPayout: -24,
        Item.BlackmailMaterial: 3,
        Item.ScrapOfIncendiaryGossip: 21
    })

    trade(0, {
        Item.MoralisingDevelopment: -24,
        Item.WhiskerwaysSecondaryPayout: -24,
        Item.DirefulReflection: 3,
        Item.TaleOfTerror: 21
    })

    trade(0, {
        Item.MoralisingDevelopment: -24,
        Item.WhiskerwaysSecondaryPayout: -24,
        Item.PuzzleDamaskScrap: 3,
        Item.JournalOfInfamy: 21
    })

    trade(0, {
        Item.InscrutableTwist: -1,
        Item.ScrapOfIncendiaryGossip: 4
    })

    trade(0, {
        Item.InscrutableTwist: -25,
        Item.BlackmailMaterial: 4
    })            

    trade(0, {
        Item.InscrutableTwist: -1,
        Item.TaleOfTerror: 4
    })

    trade(0, {
        Item.InscrutableTwist: -25,
        Item.DirefulReflection: 4
    })        

    trade(0, {
        Item.InscrutableTwist: -1,
        Item.JournalOfInfamy: 4
    })

    trade(0, {
        Item.InscrutableTwist: -25,
        Item.PuzzleDamaskScrap: 4
    })    