from enums import *
from config import Config
from player import Player
from decks.deck import *
import utils

import random

class ZeeRegion:
    def __init__(self, location, peril, narrow_dc,
                 plunder_dc_basic, plunder_dc_advanced,
                 plunder_gain_basic, plunder_gain_advanced,
                 chasing_gain_basic, chasing_gain_advanced, bounty):
        self.location = location
        self.peril = peril
        self.narrow = narrow_dc
        self.plunder_dc_basic = plunder_dc_basic
        self.plunder_dc_advanced = plunder_dc_advanced
        self.plunder_gain_basic = plunder_gain_basic
        self.plunder_dc_advanced = plunder_gain_advanced
        self.chasing_gain_basic = chasing_gain_basic
        self.chasing_gain_advanced = chasing_gain_advanced
        self.bounty = bounty

    # def

home_waters = ZeeRegion(Location.HomeWaters,
                        peril=100,
                        narrow_dc=3,
                        plunder_dc_basic= 160,
                        plunder_dc_advanced= 5,
                        plunder_gain_basic= 300, 
                        plunder_gain_advanced= 250,
                        chasing_gain_basic= 8,
                        chasing_gain_advanced= 8,
                        bounty=5334)

shepherds_wash = ZeeRegion(Location.ShepherdsWash,
                        peril=110,
                        narrow_dc=3,

                        plunder_dc_basic= 160,
                        plunder_dc_advanced= 6,
                        plunder_gain_basic= 300, 
                        plunder_gain_advanced= 300,
                        chasing_gain_basic= 8,
                        chasing_gain_advanced= 9,
                        bounty=5350)
         
stormbones = ZeeRegion(Location.Stormbones,
                        peril=110,
                        narrow_dc=3,

                        plunder_dc_basic= 160,
                        plunder_dc_advanced= 6,
                        plunder_gain_basic= 300, 
                        plunder_gain_advanced= 300,
                        chasing_gain_basic= 8,
                        chasing_gain_advanced= 9,
                        bounty=5350)

sea_of_voices = ZeeRegion(Location.TheSeaOfVoices, 150, 5,
                        plunder_dc_basic= 160,
                        plunder_dc_advanced= 7,
                        plunder_gain_basic= 300, 
                        plunder_gain_advanced= 350,
                        chasing_gain_basic= 8,
                        chasing_gain_advanced= 10,
                        bounty=5403)

the_salt_steppe = ZeeRegion(Location.TheSaltSteppes, 200, 9,
                        plunder_dc_basic= 210,
                        plunder_dc_advanced= 11,
                        plunder_gain_basic= 400, 
                        plunder_gain_advanced= 400,
                        chasing_gain_basic= 13,
                        chasing_gain_advanced= 14,
                        bounty=5568)
   
pillared_sea = ZeeRegion(Location.ThePillaredSea, 210, 9,
                        plunder_dc_basic= 220,
                        plunder_dc_advanced= 12,
                        plunder_gain_basic= 450,
                        plunder_gain_advanced= 450,
                        chasing_gain_basic= 14,
                        chasing_gain_advanced= 15,
                        bounty=5597)   
the_snares = ZeeRegion(Location.TheSnares, 250, 12,
                        plunder_dc_basic= 260,
                        plunder_dc_advanced= 13,
                        plunder_gain_basic= 500,
                        plunder_gain_advanced= 500,
                        chasing_gain_basic= 15,
                        chasing_gain_advanced= 16,
                        bounty=5659)   

def create_deck(config: Config, location: Location):
    # quick and dirty version
    pass