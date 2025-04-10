import numbers
import player as Player
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse import csc_matrix
from scipy.optimize import linprog
from enum import Enum, auto
from itertools import count

from sklearn.linear_model import Lasso

from enums import *
import helper.utils as utils

class Config:
    player: Player.Player

    def __init__(self, player, constraint):
        self.player = player
        self.constraint = constraint

        self.num_items = max(Item, key=lambda x: x.value).value
        print(f"max(Item): {self.num_items}")

        # HACK
        # increase this if you get `IndexError: list assignment index out of range`        
        var_buffer = 5_000
        num_vars = self.num_items + 1 + var_buffer

        self.matrix_size = num_vars
        self.A = lil_matrix((self.matrix_size, self.matrix_size))
        self.b = [1]*num_vars
        
        self.counter = count(start=-1)

        self.bounds = [(0, None) for _ in range(self.matrix_size)]

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

        self.bounds[Item._ImprisonedInNewNegate.value] = (None, 1)

        self.bounds[Item.TroubledWaters.value] = (None, 0)

        exhaustion_lower_bounds = -100
        exhaustion_upper_bounds = 12
        self.bounds[Item.GenericBoneMarketExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)

        self.bounds[Item.AntiquityReptileExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AntiquityAmphibianExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AntiquityBirdExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AntiquityFishExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AntiquityArachnidExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AntiquityInsectExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AntiquityPrimateExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)

        self.bounds[Item.AmalgamyReptileExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AmalgamyAmphibianExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AmalgamyBirdExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AmalgamyFishExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AmalgamyArachnidExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AmalgamyInsectExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AmalgamyPrimateExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)

        self.bounds[Item.MenaceReptileExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.MenaceAmphibianExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.MenaceBirdExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.MenaceFishExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.MenaceArachnidExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.MenaceInsectExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.MenacePrimateExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)

        self.bounds[Item.AntiquityGeneralExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.AmalgamyGeneralExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.MenaceGeneralExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)

        self.bounds[Item.GeneralReptileExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.GeneralAmphibianExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.GeneralBirdExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.GeneralFishExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.GeneralArachnidExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.GeneralInsectExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)
        self.bounds[Item.GeneralPrimateExhaustion.value] = (exhaustion_lower_bounds, exhaustion_upper_bounds)


        self.bounds[Item.Hedonist.value] = (0, 55)

        self.bounds[Item.InCorporateDebt.value] = (None, 15)
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

        self.bounds[Item.RecentParticipantInAStarvedCulturalExchange.value] = (-1, 0)

        self.bounds[Item.DelayUntilTheNextBoardMeeting.value] = (-1, 0)

        self.bounds[Item.ReportFromTheKhagansPalace.value] = (-1, 0)

        self.bounds[Item._CoverTiesGeneric.value] = (0, 1)
        self.bounds[Item.CoverTiesSurface.value] = (0, 1)
        self.bounds[Item.CoverTiesBazaar.value] = (0, 1)
        self.bounds[Item.CoverTiesDispossessed.value] = (0, 1)

        # self.bounds[Item.RatMarketExhaustion.value] = (-50_000, 0)
        self.bounds[Item.SoftRatMarketSaturation1.value] = (-65_000, 0)
        self.bounds[Item.SaintlyRatMarketSaturation1.value] = (-65_000, 0)
        self.bounds[Item.MaudlinRatMarketSaturation1.value] = (-65_000, 0)
        self.bounds[Item.InscrutableRatMarketSaturation1.value] = (-65_000, 0)
        self.bounds[Item.TempestuousRatMarketSaturation1.value] = (-65_000, 0)
        self.bounds[Item.IntricateRatMarketSaturation1.value] = (-65_000, 0)
        self.bounds[Item.CalculatingRatMarketSaturation1.value] = (-65_000, 0)
        self.bounds[Item.RuinousRatMarketSaturation1.value] = (-65_000, 0)

        self.bounds[Item.SoftRatMarketSaturation2.value] = (-155_000, 0)
        self.bounds[Item.SaintlyRatMarketSaturation2.value] = (-115_000, 0)
        self.bounds[Item.MaudlinRatMarketSaturation2.value] = (-155_000, 0)
        self.bounds[Item.InscrutableRatMarketSaturation2.value] = (-115_000, 0)
        self.bounds[Item.TempestuousRatMarketSaturation2.value] = (-115_000, 0)
        self.bounds[Item.IntricateRatMarketSaturation2.value] = (-115_000, 0)
        self.bounds[Item.CalculatingRatMarketSaturation2.value] = (-115_000, 0)
        self.bounds[Item.RuinousRatMarketSaturation2.value] = (-115_000, 0)

        self.bounds[Item.WhiskerwaysSecondaryPayout.value] = (None, 0)  

        self.bounds[Item.ReportFromTheKhagansPalace.value] = (-1, 0)
        self.bounds[Item.ViolantSights.value] = (-1, 0)

        self.enable_all_rat_market_moons = True

        self.add(constraint)
        
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

    def uniform_random_trade(self, input, outputs):
        net_output = {}
        num = len(outputs)

        for i in outputs:
            for key, val in i.items():
                net_output[key] = net_output.get(key, 0) + (val / num)

        net_trade = utils.sum_dicts(input, net_output)
        self.trade(0, net_trade)        
    
    def weighted_trade(self, cost, *weighted_trades):
        weighted_outcome = {}

        for weight, trade in weighted_trades:
            for key, val in trade.items():
                weighted_outcome[key] = weighted_outcome.get(key, 0) + val * weight

        net_trade = utils.sum_dicts(cost, weighted_outcome)
        self.trade(0, net_trade)

    def challenge_ev(self, stat: Item, dc: int, on_pass: dict, on_fail: dict):
        pass_rate = self.player.pass_rate(stat, dc)

        return utils.weighted_exchange(
            (pass_rate, on_pass),
            (1.0 - pass_rate, on_fail)
        )
    
    def challenge_trade(self, stat: Item, dc: int, cost, on_pass, on_fail):
        pass_rate = self.player.pass_rate(stat, dc)

        self.weighted_trade(
            cost,
            (pass_rate, on_pass),
            (1.0 - pass_rate, on_fail)
        )