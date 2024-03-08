def pyramid(n): return n * (n+1) / 2
def clamp(n, floor, ceiling): return min(ceiling, max(floor, n))

def broad_challenge_success_rate(stat, difficulty): return clamp(0.6 * stat/difficulty, 0.0, 1.0)

def narrow_challenge_success_rate(stat, difficulty): return clamp(0.5 + (stat - difficulty)/10, 0.1, 1.0)

def expected_failures(success_rate): return 1.0/success_rate - 1 if success_rate < 1.0 else 0

def challenge_ev(player_stat, difficulty, success, failure):
    success_rate = broad_challenge_success_rate(player_stat, difficulty)
    return success_rate * success + (1.0 - success_rate) * failure

def skelly_value_in_items(skelly_value, item_value, zoo_bonus_active):
    zoo_multiplier = 1.1 if zoo_bonus_active else 1.0
    return skelly_value * zoo_multiplier / item_value
    