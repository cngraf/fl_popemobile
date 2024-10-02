from enums import *
from utils import *

def add_trades(active_player, lab_rpa, config):
    trade = config.trade
    add = config.add

    trade(1, {
        Item.LaboratoryResearch: lab_rpa
    })

    # TODO better estimate

    trade(1, {
        Item.ParabolanResearch: 12
    })

    # Cartographic Projects -----------

    trade(2, {
        Item.LaboratoryResearch: -2700,
        Item.CartographersHoard: 1
    })

    # Small Gazette
    trade(2, {
        Item.LaboratoryResearch: -60,
        Item.GlassGazette: 5
    })

    # Big Gazette
    trade(2, {
        Item.LaboratoryResearch: -2500,
        Item.GlassGazette: 125
    })

    # Biological Projects ------------

    # False Snake
    trade(2, {
        Item.LaboratoryResearch: -100,
        Item.MemoryOfDistantShores: 20,
        Item.UnearthlyFossil: 1
    })

    # Dissect the Pinewood Shark
    trade(2, {
        Item.RemainsOfAPinewoodShark: -1,
        Item.LaboratoryResearch: -100,
        Item.IncisiveObservation: 2,
        Item.FinBonesCollected: 38,
        Item.BoneFragments: 500
    })

    # Geology Projects --------------

    add({
        # Item.LaboratoryResearch: -100,
        Item.Action: -6,
        Item.SurveyOfTheNeathsBones: 25
    })

    trade(2, {
        Item.LaboratoryResearch: -2700,
        Item.SurveyOfTheNeathsBones: 125
    })

    # Mathematical Projects ------------

    trade(2, {
        Item.LaboratoryResearch: -13000,
        Item.ImpossibleTheorem: 1,
    })

    # -------------
    # Laboratory
    # -------------

    trade(1, {
        Item.PreservedSurfaceBlooms: -1,
        Item.KnobOfScintillack: -8,
        Item.ConsignmentOfScintillackSnuff: 2
    })

    # PerfumedGunpowder per Action:    2.10293
    add({
        Item.Action: -1,
        Item.NightsoilOfTheBazaar: -40,
        Item.PreservedSurfaceBlooms: -1,
        Item.PerfumedGunpowder: 10
    })

    # estimated actions
    trade(4, {
        Item.RemainsOfAPinewoodShark: -1,
        Item.FinBonesCollected: 38,
        Item.BoneFragments: 500,
        Item.IncisiveObservation: 2
    })

    add({
        Item.Action: -1,
        Item.PerfumedGunpowder: -4,
        Item.VitalIntelligence: 1,
        Item.WellPlacedPawn: 2
    })