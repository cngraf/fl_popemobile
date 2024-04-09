import numbers
import player as Player
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix
from scipy.optimize import linprog
from enum import Enum, auto
from itertools import count

from enums import *
import utils as utils

class Config:
    player: Player.Player

    def __init__(self, num_vars, player):
        self.player = player
        self.A = lil_matrix((num_vars, num_vars))
        self.b = [1]*num_vars
        
        self.counter = count(start=-1)

        self.bounds = [(0, None) for _ in range(num_vars)]

        # in practice it seems this rarely affects the output, but it makes me feel better
        # I don't know if this even works the way I think it does as far as modeling long-term stockpiling
        # but if you set it too low, you will lock out certain trades
        # eg setting the upper bound of Bohemian favours to 3 will lock out the Jericho option
        # so really it's a source of bugs more than anything else
        # still keeping it in

        # important that menace is capped at 0
        # ensures any gains are pre-paid for
        self.bounds[Item.Wounds.value] = (None, 0)
        self.bounds[Item.Scandal.value] = (None, 0)
        self.bounds[Item.Suspicion.value] = (None, 0)
        self.bounds[Item.Nightmares.value] = (None, 0)

        self.bounds[Item.TroubledWaters.value] = (None, 35)

        self.bounds[Item.Hedonist.value] = (0, 55)

        self.bounds[Item.SeeingBanditryInTheUpperRiver.value] = (0, 36)

        self.bounds[Item.ConnectedBenthic.value] = (0, 800)

        self.bounds[Item.Tribute.value] = (0, 260)
        self.bounds[Item.TimeAtWakefulCourt.value] = (0, 13)
        self.bounds[Item.TimeAtJerichoLocks.value] = (0, 5)

        self.bounds[Item.FavBohemians.value] = (0, 7)
        self.bounds[Item.FavChurch.value] = (0, 7)
        self.bounds[Item.FavConstables.value] = (0, 7)
        self.bounds[Item.FavCriminals.value] = (0, 7)
        self.bounds[Item.FavDocks.value] = (0, 7)
        self.bounds[Item.FavGreatGame.value] = (0, 7)
        self.bounds[Item.FavHell.value] = (0, 7)
        self.bounds[Item.FavRevolutionaries.value] = (0, 7)
        self.bounds[Item.FavRubberyMen.value] = (0, 7)
        self.bounds[Item.FavSociety.value] = (0, 7)
        self.bounds[Item.FavTombColonies.value] = (0, 7)
        self.bounds[Item.FavUrchins.value] = (0, 7)

        self.bounds[Item.ResearchOnAMorbidFad.value] = (0, 6)

        self.enable_all_rat_market_moons = True

    def add(self, exchanges: dict):
        n = next(self.counter)
        self.b[n] = exchanges.get(Item.Constraint, 0)
        for key, value in exchanges.items():
            if key != Item.Constraint:
                self.A[n, key.value] = value

    # def per_day(self, exchanges):
    #     n = next(self.counter)
    #     self.b[n] = 1
    #     for item, value in exchanges.items():
    #         self.A[n, item.value] = value

    def trade(self, actionCost, exchanges):
        n = next(self.counter)
        self.b[n] = 0
        self.A[n, Item.Action.value] = -1 * actionCost
        for item, value in exchanges.items():
            self.A[n, item.value] = value

    def railway_card(self, name, freq, location, isGood, exchanges):
        # dummy alias for now
        self.trade(1, exchanges)

    def add_weighted_trade(self, actions, *weighted_trades):
        net_trade = {}

        for weight, trade in weighted_trades:
            for key, val in trade.items():
                net_trade[key] = net_trade.get(key, 0) + val * weight

        self.trade(actions, net_trade)

    def challenge_ev(self, stat: Stat, dc: int, on_pass: dict, on_fail: dict):
        pass_rate = self.player.pass_rate(stat, dc)

        return utils.weighted_exchange(
            (pass_rate, on_pass),
            (1.0 - pass_rate, on_fail)
        )

    def add_challenge(self, actions: int, stat: Stat, dc: int, on_pass, on_fail):
        pass_rate = self.player.pass_rate(self.player.stats[stat], dc)

        self.add_weighted_trade(actions,
            (pass_rate, on_pass),
            (1.0 - pass_rate, on_fail)
        )