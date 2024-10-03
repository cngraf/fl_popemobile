from enums import *
from config import Config
from player import Player
from decks.deck import *
import helper.utils as utils

import random

with_current = 160
against_current = 220

class ZeeRegion(Enum):
    HOME_WATERS = "Home Waters"
    SHEPHERDS_WASH = "Shepherd's Wash"
    SEA_OF_VOICES = "The Sea of Voices"
    SALT_STEPPES = "The Salt Steppes"
    PILLARED_SEA = "The Pillared Sea"
    STORMBONES = "Stormbones"
    THE_SNARES = "The Snares"

class ZeeRegionData:
    def __init__(self, location, peril, narrow_dc,
                 dc_basic, dc_advanced,
                 plunder_gain_basic, plunder_gain_advanced,
                 chasing_gain_basic, chasing_gain_advanced, bounty,
                 distance_to):
        self.location = location
        self.peril = peril
        self.narrow = narrow_dc
        self.dc_basic = dc_basic
        self.dc_advanced = dc_advanced
        self.plunder_gain_basic = plunder_gain_basic
        self.plunder_gain_advanced = plunder_gain_advanced
        self.chasing_gain_basic = chasing_gain_basic
        self.chasing_gain_advanced = chasing_gain_advanced
        self.bounty = bounty
        self.distance_to = distance_to


home_waters = ZeeRegionData(Location.HomeWaters,
                        peril=100,
                        narrow_dc=3,
                        dc_basic= 160,
                        dc_advanced= 5,
                        plunder_gain_basic= 300, 
                        plunder_gain_advanced= 250,
                        chasing_gain_basic= 8,
                        chasing_gain_advanced= 8,
                        bounty=5334,
                        distance_to={
                            ZeeRegion.SHEPHERDS_WASH: with_current,
                            ZeeRegion.STORMBONES: against_current,
                            ZeeRegion.THE_SNARES: with_current
                        })

shepherds_wash = ZeeRegionData(Location.ShepherdsWash,
                        peril=110,
                        narrow_dc=3,

                        dc_basic= 160,
                        dc_advanced= 6,
                        plunder_gain_basic= 300, 
                        plunder_gain_advanced= 300,
                        chasing_gain_basic= 8,
                        chasing_gain_advanced= 9,
                        bounty=5350,
                        distance_to={
                            ZeeRegion.SEA_OF_VOICES: with_current,
                            ZeeRegion.HOME_WATERS: against_current,
                            ZeeRegion.THE_SNARES: with_current
                        })                        
         
stormbones = ZeeRegionData(Location.Stormbones,
                        peril=110,
                        narrow_dc=3,

                        dc_basic= 160,
                        dc_advanced= 6,
                        plunder_gain_basic= 300, 
                        plunder_gain_advanced= 300,
                        chasing_gain_basic= 8,
                        chasing_gain_advanced= 9,
                        bounty=5350,
                        distance_to={
                            ZeeRegion.HOME_WATERS: with_current,
                            ZeeRegion.PILLARED_SEA: against_current,
                            ZeeRegion.THE_SNARES: with_current
                        })                        

sea_of_voices = ZeeRegionData(Location.SeaOfVoices,
                        peril= 150,
                        narrow_dc=5,
                        dc_basic= 160,
                        dc_advanced= 7,
                        plunder_gain_basic= 300, 
                        plunder_gain_advanced= 350,
                        chasing_gain_basic= 8,
                        chasing_gain_advanced= 10,
                        bounty=5403,
                        distance_to={
                            ZeeRegion.SALT_STEPPES: with_current,
                            ZeeRegion.SHEPHERDS_WASH: against_current,
                            ZeeRegion.THE_SNARES: with_current
                        })                        

the_salt_steppe = ZeeRegionData(Location.SaltSteppes,
                        peril = 200,
                        narrow_dc=9,
                        dc_basic= 210,
                        dc_advanced= 11,
                        plunder_gain_basic= 400, 
                        plunder_gain_advanced= 400,
                        chasing_gain_basic= 13,
                        chasing_gain_advanced= 14,
                        bounty=5568,
                        distance_to={
                            ZeeRegion.PILLARED_SEA: with_current,
                            ZeeRegion.SEA_OF_VOICES: against_current,
                            ZeeRegion.THE_SNARES: with_current
                        })                        
   
pillared_sea = ZeeRegionData(Location.PillaredSea,
                        peril=210,
                        narrow_dc=9,
                        dc_basic= 220,
                        dc_advanced= 12,
                        plunder_gain_basic= 450,
                        plunder_gain_advanced= 450,
                        chasing_gain_basic= 14,
                        chasing_gain_advanced= 15,
                        bounty=5597,
                        distance_to={
                            ZeeRegion.STORMBONES: with_current,
                            ZeeRegion.SALT_STEPPES: against_current,
                            ZeeRegion.THE_SNARES: with_current
                        })
                        
the_snares = ZeeRegionData(Location.Snares, 250, 12,
                        dc_basic= 260,
                        dc_advanced= 13,
                        plunder_gain_basic= 500,
                        plunder_gain_advanced= 500,
                        chasing_gain_basic= 15,
                        chasing_gain_advanced= 16,
                        bounty=5659,
                        distance_to={
                            ZeeRegion.HOME_WATERS: with_current,
                            ZeeRegion.STORMBONES: with_current,
                            ZeeRegion.PILLARED_SEA: with_current,
                            ZeeRegion.SALT_STEPPES: with_current,
                            ZeeRegion.SEA_OF_VOICES: with_current,
                            ZeeRegion.SHEPHERDS_WASH: with_current                            
                        })                        

zee_regions = {
    ZeeRegion.HOME_WATERS: home_waters,
    ZeeRegion.SHEPHERDS_WASH: shepherds_wash,
    ZeeRegion.SEA_OF_VOICES: sea_of_voices,
    ZeeRegion.SALT_STEPPES: the_salt_steppe,
    ZeeRegion.PILLARED_SEA: pillared_sea,
    ZeeRegion.STORMBONES: stormbones,
    ZeeRegion.THE_SNARES: the_snares
}

def create_deck(config: Config, location: Location):
    '''
    Probably don't need the grades here?
    Can just have an algo check the exchanges on each card
    1. TW reduction when TW is high
    2. chasing gain
    3. plunder gain
    4. minimize TW
    '''


    # TODO
    # - one for each region
    # - depends on ship type

    region = the_salt_steppe

    cards = [
        Card(
            name="A Corvette (Piracy)",
            freq=Rarity.Standard,
            grade=Grade.Good,
            discardable=False,
            exchange=config.challenge_ev(
                stat=Item.Persuasive,
                dc=160,
                on_pass={
                    Item.TroubledWaters: -2,
                    Item.ZailingProgress: 1
                },
                on_fail={
                    Item.TroubledWaters: 6,
                    Item.Suspicion: 2,
                    Item.ZailingProgress: 0.5
                }
            )
        ),

        Card(
            name="Giant Enemy Crab",
            freq=Rarity.Infrequent,
            grade=Grade.Good,
            discardable=False,
            exchange=config.challenge_ev(
                stat=Item.MonstrousAnatomy,
                dc=3,
                on_pass={
                    Item.TroubledWaters: -2,
                    Item.ZailingProgress: 1
                },
                on_fail={
                    Item.TroubledWaters: 8
                }
            )
        ),

        Card(
            name="A Huge Terrible Beast",
            freq=Rarity.Infrequent,
            grade=Grade.Bad,
            discardable=False,
            exchange={
                Item.TroubledWaters: 3,
                Item.ZailingProgress: 1
            }
        ),

        # TODO: Add False-Star treasure option for -5 TW and no chasing
        # needs token card item
        Card(
            name="A Navigation Error",
            freq=Rarity.Infrequent,
            grade=Grade.Excellent,
            discardable=False,
            exchange=config.challenge_ev(
                stat=Item.Zeefaring,
                dc=5,
                on_pass={
                    Item.TroubledWaters: 2,
                    Item.ChasingDownYourBounty: region.chasing_gain_advanced,
                    Item.ZailingProgress: 1
                }
            )
        ),

        Card(
            name="A Spit of Land",
            freq=Rarity.Infrequent,
            grade=Grade.Bad,
            discardable=False,
            exchange={
                Item.TroubledWaters: 1,
                Item.ZailingProgress: 1
            }
        ),

        Card(
            name="Passing a Lightship",
            freq=Rarity.Infrequent,
            grade=Grade.Excellent,
            discardable=False,
            exchange=config.challenge_ev(
                stat=Item.Shadowy,
                dc=260,
                on_pass={
                    Item.ChasingDownYourBounty: region.chasing_gain_basic,
                    Item.ZailingProgress: 1
                },
                on_fail={
                    Item.TroubledWaters: 7,
                    Item.ZailingProgress: 0.5,
                }
            )
        ),

        # add rare success? eh
        Card(
            name="Rats in the hold",
            freq=Rarity.Infrequent,
            grade=Grade.Good,
            discardable=False,
            exchange=config.challenge_ev(
                stat=Item.Dangerous,
                dc=160,
                on_pass={
                    Item.TroubledWaters: 2,
                    Item.ChasingDownYourBounty: region.chasing_gain_basic,
                    Item.ZailingProgress: 1
                }
            )
        ),

        # only TW 4-7 so fudging the frequency from Standard to lower
        Card(
            name="The Killing Wind",
            freq=Rarity.VeryInfrequent,
            grade=Grade.Good,
            discardable=False,
            exchange={
                    Item.TroubledWaters: 2,
                    Item.ZeeZtory: 4.5,
                    Item.ZailingProgress: 1
                }
        ),

        Card(
            name="What do the Drownies sing?",
            freq=Rarity.Standard,
            grade=Grade.Good,
            discardable=False,
            exchange=config.challenge_ev(
                stat=Item.MonstrousAnatomy,
                dc=13,
                on_pass={
                    Item.TroubledWaters: 2,
                    Item.ChasingDownYourBounty: region.chasing_gain_advanced,
                    Item.ZailingProgress: 1
                }
            )
        ),
    ]

    if (config.player.treasure == Treasure.FalseStartOfYourOwn):
        cards.append(
            Card(
                name="Your False-Star",
                freq=Rarity.Standard,
                grade=Grade.Good,
                exchange={
                    Item.TroubledWaters: -5,
                    Item.ZailingProgress: 1
                }
            )
        )