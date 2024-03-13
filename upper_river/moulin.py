from enums import *
from utils import *

def add_trades(active_player, trade):

    # Antiquarian's Shop

    trade(1, {
        Item.AnIdentityUncovered: -4,
        Item.IncisiveObservation: -1,
        Item.CorrectiveHistorialNarrative: 1
    })

    trade(1, {
        Item.NicatoreanRelic: -4,
        Item.IncisiveObservation: -1,
        Item.RevisionistHistoricalNarrative: 1
    })

    # --- Expeditions
    '''
    how many actions is the whole thing?
    - 2 to recruit 
    - embark
    - 1 per distance
    - dig
    - 1 per distance
    - cash out

    is it 4 + 2 * distance?
    confirm later

    assume each lucky find outcome is 25%

    wiki says this should be 4.5 and that's what we get
    with no additional modules, cool cool
    '''
    
    distance = 8
    gross_wages = distance * 11.5 * 100.5;
    lucky_finds = 4
    assistants_cut = 0.07 + 0.09
    net_wages = gross_wages * (1.0 - assistants_cut)

    # Upper Layer
    trade(distance * 2 + 4 + lucky_finds, {
        Item.ProscibedMaterial: (net_wages - 1250) * 0.25,
        Item.SilveredCatsClaw: 50 * lucky_finds * 0.25,
        Item.NicatoreanRelic: 3 * lucky_finds * 0.25,
        Item.FirstCityCoin: 20 * lucky_finds * 0.25,
        Item.UnlawfulDevice: 1 + (1 * lucky_finds * 0.25)
    })

    # Deep Layer
    trade(distance * 2 + 4 + lucky_finds, {
        Item.TraceOfTheFirstCity: net_wages / 200,
        Item.RelicOfTheSecondCity: net_wages / 60,
        Item.RelicOfTheThirdCity: net_wages / 60,
        Item.RelicOfTheFourthCity: net_wages / 60,

        Item.SilveredCatsClaw: 50 * lucky_finds * 0.25,
        Item.NicatoreanRelic: 3 * lucky_finds * 0.25,
        Item.FirstCityCoin: (net_wages / 100) + 20 * lucky_finds * 0.25,
        Item.UnlawfulDevice: lucky_finds * 0.25
    })    

    # Silvered Font
    trade(distance * 2 + 4 + lucky_finds, {
        Item.TraceOfViric: net_wages / 150,

        Item.SilveredCatsClaw: (net_wages / 15) + (50 * lucky_finds * 0.25),
        Item.NicatoreanRelic: 3 * lucky_finds * 0.25,
        Item.FirstCityCoin: 20 * lucky_finds * 0.25,
        Item.UnlawfulDevice: lucky_finds * 0.25
    })

    # Across the Zee
    trade(distance * 2 + 4 + lucky_finds, {
        Item.RustedStirrup: net_wages / 20,

        Item.SilveredCatsClaw: (net_wages / 40) + (50 * lucky_finds * 0.25),
        Item.NicatoreanRelic: (net_wages / 1000) + 3 * lucky_finds * 0.25,
        Item.FirstCityCoin: 20 * lucky_finds * 0.25,
        Item.UnlawfulDevice: lucky_finds * 0.25
    })

    # --- Monographs

    # loss of quality is skipped when the quality is already at 0
    # so just handwaving that part and hardcoding the recipe payouts
    # maybe figure out a pattern to sidestep that cleverly

    trade(1, {
        Item.TraceOfTheFirstCity: -25,
        Item.MonographCautionary: 1
    })

    trade(1, {
        Item.RelicOfTheSecondCity: -80,
        Item.MonographCautionary: 1
    })
    
    trade(1, {
        Item.RelicOfTheFourthCity: -250,
        Item.MonographCautionary: 1
    })

    trade(1, {
        Item.ProscibedMaterial: -200,
        Item.PalimpsestScrap: -8,
        Item.MonographCautionary: 1
    })

    trade(1, {
        Item.RustedStirrup: -125,
        Item.MonographCautionary: 1
    })

    trade(1, {
        Item.FirstCityCoin: -50,
        Item.MonographTragic: 1
    })

    trade(1, {
        Item.RelicOfTheThirdCity: -125,
        Item.MonographTragic: 1
    })

    trade(1, {
        Item.TraceOfViric: -25,
        Item.MonographIronic: 1
    })

    trade(1, {
        Item.NicatoreanRelic: -5,
        Item.MonographIronic: 1
    })

    trade(1, {
        Item.SilveredCatsClaw: -125,
        Item.MonographIronic: 1
    })

    trade(1, {
        Item.UnlawfulDevice: -1,
        Item.MonographIronic: 1
    })


    # Tragic, Ironic, Cautionary

    # History of the Arbor => Exiled Antiquarian
    # 500 ironic, 50 cautionary, 50 tragic
    # using the spiderpope guide order

    trade(3, {
        Item.MonographIronic: -5,
        Item.MonographCautionary: -1,

        Item.MemoryOfDistantShores: 1,
        Item.UnprovenancedArtefact: 2,
        Item.FinalBreath:  1,
        Item.ParabolanOrangeApple: 1
    })

    trade(3, {
        Item.MonographIronic: -5,
        Item.MonographTragic: -1,

        Item.MemoryOfDistantShores: 1,
        Item.UnprovenancedArtefact: 2,
        Item.FinalBreath:  1,
        Item.ParabolanOrangeApple: 1
    })

    return