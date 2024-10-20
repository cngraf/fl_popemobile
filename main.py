from config import *
from enums import *
from helper.utils import *

from optimization.model_runner import *
import optimization.params
import player as player

import decks.london_deck
import decks.nadir

import time_the_healer

import social_actions as SocialActions
import bazaar as Bazaar
import inventory_conversions as InventoryConversions

import rat_market

import professional_activities

import london.uncategorized
import london.laboratory
import london.newspaper
import london.hearts_game
import london.heists
import london.arbor
import london.deck_approximation
import london.forgotten_quarter

import bone_market.trades

import parabola

import unterzee.gaiders_mourn
import unterzee.khanate
import unterzee.wakeful_eye
import unterzee.port_cecil

import upper_river.uncategorized
import upper_river.upper_river_exchange
import upper_river.ealing_gardens
import upper_river.jericho
import upper_river.evenlode
import upper_river.balmoral
import upper_river.burrow
import upper_river.station_viii
import upper_river.moulin
import upper_river.hurlers
import upper_river.marigold
import upper_river.tracklayers_city
import upper_river.decks

import firmament.hallows_throat
import firmament.midnight_moon
import firmament.zenith
import firmament.stacks

import uncategorized.menace_locations

import fate.philosofruits
import fate.upwards
import fate.whiskerways

# --------------------------------------------
# -------------- Parameters    ---------------
# --------------------------------------------

config = Config(
    player = optimization.params.active_player,
    constraint = optimization.params.core_constraint
    )

# -----------------------------------------------------
# --- Modules
# ----------------------------------------------------

# doing some goofy inversion of control stuff here so that I can just copy paste everything

time_the_healer.add_trades(config)

SocialActions.add_trades(config)
Bazaar.add_trades(config)

rat_market.add_trades(config)

professional_activities.add_trades(config)

InventoryConversions.add_trades(config)

# decks.london_deck.add_trades(config)

london.uncategorized.add_trades(config)
london.newspaper.add_trades(config)

london.laboratory.add_trades(config)
london.hearts_game.add_trades(config)
london.arbor.add_trades(config)
london.heists.add_trades(config)
london.deck_approximation.add_trades(config)
london.forgotten_quarter.add_trades(config)

bone_market.trades.add_trades(config)

unterzee.khanate.add_trades(config)
unterzee.wakeful_eye.add_trades(config)
unterzee.port_cecil.add_trades(config)
unterzee.gaiders_mourn.add_trades(config)

parabola.add_trades(config)

upper_river.upper_river_exchange.add_trades(config)
upper_river.uncategorized.add_trades(config)
upper_river.ealing_gardens.add_trades(config)
upper_river.jericho.add_trades(config)
upper_river.evenlode.add_trades(config)
upper_river.balmoral.add_trades(config)
upper_river.burrow.add_trades(config)
upper_river.station_viii.add_trades(config)
upper_river.moulin.add_trades(config)
upper_river.hurlers.add_trades(config)
upper_river.marigold.add_trades(config)
upper_river.decks.add_trades(config)

upper_river.tracklayers_city.add_trades(config)

firmament.hallows_throat.add_trades(config)
firmament.midnight_moon.add_trades(config)
firmament.zenith.add_trades(config)
firmament.stacks.add_trades(config)

uncategorized.menace_locations.add_trades(config)

fate.philosofruits.add_trades(config)
fate.upwards.add_trades(config)
fate.whiskerways.add_trades(config)


runner = ModelRunner(
    optimize_input=optimization.params.solution_input,
    optimize_output=optimization.params.solution_output,
    config=config)

# Run the optimization and display the results
runner.run_optimization()
runner.display_summary()