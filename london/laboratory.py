from enums import *
from helper.utils import *

def add_trades(config):
    add = config.add

    ########################################################
    #               Scientific Investivations
    ########################################################

    '''
    Action costs are rough estimates from incomplete simulation
    Lab Setup:
        EquipmentForScientificExperimentation        9
        PrestigeOfYourLaboratory                     100
        NumberOfWorkersInYourLaboratory              4
        ScholarOfTheCorrespondence                   21
        LaboratoryServicesOfLetticeTheMercy          1
        LaboratoryServicesOfSilkCladExpert           1
        LaboratoryServicesFromGiftedStudent          5
        LaboratoryServicesFromVisionaryStudent       5
        SecretCollege                                1

    might be too high because
    - handwaving student disgruntlement
    - not properly modeling parabolan research
    - bugs
    
    might be too low because
    - card selection algorithm has lots of room for improvement
    - not taking full advantage of worker synergies
    - not using certain items/qualities that add good cards
    - bugs

    '''
    # Cartographic

    add({
        Item.Action: -86,
        Item.CartographersHoard: 1,
        Item.VolumeOfCollatedResearch: 4
    })

    # Small Gazette
    add({
        Item.Action: -4,
        Item.GlassGazette: 5
    })

    # Big Gazette
    add({
        Item.Action: -84,
        Item.GlassGazette: 125,
        Item.VolumeOfCollatedResearch: 4
    })

    add({
        Item.Action: -21,
        Item.RoofChart: 16,
        Item.ExtraordinaryImplication: 9,
        Item.VolumeOfCollatedResearch: 1
    })

    # Biological

    # False Snake
    add({
        Item.Action: -5.5,
        Item.MemoryOfDistantShores: 20,
        Item.UnearthlyFossil: 1
    })

    # Dissect the Pinewood Shark
    add({
        Item.Action: -5.4,
        Item.RemainsOfAPinewoodShark: -1,
        Item.FinBonesCollected: 38,
        Item.BoneFragments: 500,
        Item.IncisiveObservation: 2
    })


    ########################################################
    #               Osteology & Palaeontology
    ########################################################

    add({
        Item.Action: -16,
        Item.HumanRibcage: -1,
        Item.MammothRibcage: 1,
        Item.VolumeOfCollatedResearch: 1
    })

    add({
        Item.Action: -16,
        Item.NevercoldBrassSliver: -1000,
        Item.WarblerSkeleton: -1,
        Item.MammothRibcage: 1
    })


    # Geology

    add({
        Item.Action: -5.3,
        Item.SurveyOfTheNeathsBones: 25
    })

    add({
        Item.Action: -86,
        Item.SurveyOfTheNeathsBones: 625,
        Item.VolumeOfCollatedResearch: 4
    })

    # Mathematical Projects ------------

    add({
        Item.Action: -395,
        Item.ImpossibleTheorem: 1,
        Item.VolumeOfCollatedResearch: 2
    })

    ########################################################
    #               Manufacture Supplies
    ########################################################
    
    # Create a double consignment of Scintillack Snuff
    add({
        Item.Action: -1,
        Item.PreservedSurfaceBlooms: -1,
        Item.KnobOfScintillack: -8,
        Item.ConsignmentOfScintillackSnuff: 2
    })

    add({
        Item.Action: -1,
        Item.BessemerSteelIngot: -90,
        Item.JustificandeCoin: -1,
        Item.RailwaySteel: 4
    })

    add({
        Item.Action: -3,
        Item.BessemerSteelIngot: -345,
        Item.JustificandeCoin: -3,
        Item.RailwaySteel: 15
    })        

    # Create a lot of Perfumed Gunpowder
    add({
        Item.Action: -1,
        Item.NightsoilOfTheBazaar: -40,
        Item.PreservedSurfaceBlooms: -1,
        Item.PerfumedGunpowder: 10
    })