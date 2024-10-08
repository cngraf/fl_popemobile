from enums import *
from typing import Tuple, Dict
import math

def pyramid(n): return n * (n+1) / 2

def level_to_cp(n): return pyramid(n)
def cp_to_level(n): return math.floor(math.sqrt(2 * n)) if n > 0 else 0

def clamp(n, floor, ceiling): return min(ceiling, max(floor, n))

def broad_challenge_pass_rate(stat_value, difficulty):
    if difficulty <= 0:
        return 1.0
    return clamp(0.6 * stat_value/difficulty, 0.0, 1.0)

def narrow_challenge_pass_rate(stat, difficulty): return clamp(0.5 + (stat - difficulty)/10, 0.1, 1.0)

def expected_failures(success_rate): return 1.0/success_rate - 1 if success_rate < 1.0 else 0

def menace_multiplier(reduction_points):
    # formula per wiki
    # return 1 - (0.6 * (1 - 0.75**reduction_points))
    return 0.85**reduction_points

# def pass_rate(player, stat, difficulty, modifier = 0):
#     player_level = player.qualities[stat] + modifier
#     if difficulty <= 0:
#         return 1.0
#     elif stat in (Item.Watchful, Item.Shadowy, Item.Dangerous, Item.Persuasive):
#         return broad_challenge_pass_rate(player_level, difficulty)
#     else:
#         return narrow_challenge_pass_rate(player_level, difficulty)

def challenge_ev(player_stat, difficulty, success, failure):
    success_rate = broad_challenge_pass_rate(player_stat, difficulty)
    return success_rate * success + (1.0 - success_rate) * failure

def weighted_exchange(*weighted_trades: Tuple[float, Dict]):
    net_trade = {}

    for weight, trade in weighted_trades:
        for key, val in trade.items():
            net_trade[key] = net_trade.get(key, 0) + val * weight
    
    return net_trade

def skelly_value_in_items(skelly_value, item_value, zoo_bonus_active):
    zoo_multiplier = 1.1 if zoo_bonus_active else 1.0
    return skelly_value * zoo_multiplier / item_value

def add_items(base_dict: dict, add_dict: dict, weight: float = 1.0):
    for key, val in add_dict.items():
        base_dict[key] = base_dict.get(key, 0) + val * weight
    return base_dict

def sum_dicts(*dicts):
    result = {}
    for i in dicts:
        for key, val in i.items():
            result[key] = result.get(key, 0) + val

    return result