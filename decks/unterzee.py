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
                stat=Stat.Persuasive,
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
                stat=Stat.MonstrousAnatomy,
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
                stat=Stat.Zeefaring,
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
                stat=Stat.Shadowy,
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
                stat=Stat.Dangerous,
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
                stat=Stat.MonstrousAnatomy,
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