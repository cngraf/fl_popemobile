import pprint
from tabulate import tabulate
from termcolor import colored
import numpy as np
from scipy.optimize import linprog
from config import Config
from enums import Item, BONE_MARKET_ACTIONS, SPECIAL_ACTION_TYPES

# Example placeholder for BONE_MARKET_ACTIONS
# BONE_MARKET_ACTIONS = [Item.AntiquityReptileExhaustion, Item.AmalgamyReptileExhaustion]  # Add actual members

class ModelRunner:
    def __init__(self, optimize_input: Item, optimize_output: Item, config: Config):
        self.active_player = config.player
        self.optimize_input = optimize_input
        self.optimize_for = optimize_output
        self.config = config
        self.input_per_cycle = config.constraint[optimize_input]
        self.trades_used = []
        self.free_item_conversions = []
        self.items_surplus = []
        self.items_negative_surplus = [] # eg. market rotations that go unused
        self.bone_market_trades = []  # Store bone market trades
        self.rat_market_trades = []

        self.special_action_trades = {}

        self.opt_result = None

    def run_l1_optimization(self):
        # Define the problem size
        n = self.config.matrix_size

        # Original objective: Maximize a particular variable
        c = np.zeros(n)
        c[self.optimize_for.value] = -1  # Minimize negative for maximization

        # Regularization parameter
        lambda_ = 10000.0  # Strength of L1 regularization

        # New objective: Minimize c^T * x + λ * sum(|x_i|)
        # Introduce new variables u and v for L1 regularization
        c_extended = np.concatenate([c, lambda_ * np.ones(n)])  # Include regularization term

        # Modify the A_ub matrix to account for x_i = u_i - v_i (so the dimensions double)
        A_ub_extended = np.hstack([self.config.A.toarray(), np.zeros((self.config.A.shape[0], n))])  # Add zeros for new variables

        # Update the bounds: Ensure u_i and v_i are non-negative
        bounds_extended = self.config.bounds + [(0, None)] * n  # Add non-negative bounds for u_i and v_i

        # Perform linear programming optimization with extended variables
        self.opt_result = linprog(c_extended, A_ub=A_ub_extended, b_ub=self.config.b, bounds=bounds_extended, method='highs')
        print(self.opt_result)

    def run_optimization(self):
        """Set up and solve the linear programming problem."""

        try:
            c = np.zeros(self.config.matrix_size)
            c[self.optimize_for.value] = -1  # Minimize negative for maximization

            # Perform linear programming optimization
            self.opt_result = linprog(c, A_ub=self.config.A.toarray(), b_ub=self.config.b, bounds=self.config.bounds, method='highs')
            
            if self.opt_result.success:
                self.process_results()
            else:
                print(colored(f"Optimization failed: {self.opt_result.message}", "red", attrs=['bold']))
        except Exception as e:
            print(colored(f"An error occurred during optimization: {e}", "red", attrs=['bold']))

    # # TODO not sure what this does right now
    # def run_lasso_optimization(self):
    #     lasso = Lasso(0.1)
    #     lasso.fit(self.config.A.toarray(), self.config.b)
    #     x_lasso = lasso.coef_

    #     for i, coef in enumerate(x_lasso):
    #         if coef != 0.0:
    #             print(f"{self.config.A[i]}): {coef:.4f}")        

    def process_results(self):
        """Process the optimization results to determine trades and surplus items."""
        items_gained = []
        items_consumed = []

        for i in range(len(self.opt_result.slack)):
            slack = self.opt_result.slack[i]
            marginal = self.opt_result.ineqlin.marginals[i]
            if slack < 1.0 and marginal != 0:
                lose_items = ""
                gain_items = ""
                count_terms = 0
                is_bone_market_trade = False  # Flag to track if trade involves bone market items
                is_rat_market_trade = False
                is_special_action_trade = False
                special_action_type = None 
                for ii in range(self.config.num_items):
                    quantity = round(self.config.A[i, ii], 2)
                    item = Item(ii)
                    quantity = int(quantity) if int(quantity) == quantity else quantity

                    if quantity != 0:
                        if item in BONE_MARKET_ACTIONS:
                            is_bone_market_trade = True
                        elif item == Item.RatShilling:
                            is_rat_market_trade = True
                        elif item in SPECIAL_ACTION_TYPES:
                            special_action_type = item
                            is_special_action_trade = True

                        if quantity < 0:
                            count_terms += 1
                            lose_items += f"{item.name}:{quantity}; "
                            if item not in items_consumed:
                                items_consumed.append(item)
                        if quantity > 0:
                            count_terms += 1
                            gain_items += f"{item.name}:{quantity}; "
                            if item not in items_gained:
                                items_gained.append(item)

                action_cost = self.config.A[i, Item.Action.value]
                trade = [marginal * 1000, lose_items, gain_items]



                if is_bone_market_trade:
                    self.bone_market_trades.append(trade)
                elif is_rat_market_trade:
                    self.rat_market_trades.append(trade)
                elif is_special_action_trade:
                    if special_action_type not in self.special_action_trades.keys():
                        self.special_action_trades[special_action_type] = []
                    self.special_action_trades[special_action_type].append(trade)
                elif count_terms == 2 and action_cost == 0:
                    self.free_item_conversions.append(trade)
                else:

                    self.trades_used.append([marginal, lose_items, gain_items])

        self.trades_used.sort()
        self.items_surplus = [str(i) for i in items_gained if i not in items_consumed]
        self.items_negative_surplus = [str(i) for i in items_consumed if i not in items_gained]

    def wrap_text(self, text: str, width: int = 50) -> str:
        """Wraps text for better formatting in tables."""
        items = text.split('; ')
        wrapped_items = []
        for item in items:
            if len(item) > width:
                wrapped_items.append('\n'.join([item[i:i + width] for i in range(0, len(item), width)]))
            else:
                wrapped_items.append(item)
        return '\n'.join(wrapped_items)

    def display_player_stats(self):
        print(f"----- Player Items & Qualities ------")
        for key, val in self.active_player.qualities.items():
            print(f"{key.name:<24} {val:>4}")

    def display_assumptions(self):
        print(colored("\n------ Assumptions -------", "green", attrs=['bold']))
        print(f"Core Constraint:")
        pprint.pprint(self.config.constraint.items())

    def display_conversions(self):
        self._display_trade_data(self.free_item_conversions, "Conversions")

    def display_trades(self):
        self._display_trade_data(self.trades_used, "Actions")

    def display_special_action_trades(self):
        for key, value in self.special_action_trades.items():
            self._display_trade_data(value, key.name)

    def display_bone_market_trades(self):
        """Displays trades that involve Bone Market items in a separate table."""
        self._display_trade_data(self.bone_market_trades, "Bone Market Trades")

    def display_rat_market_trades(self):
        self._display_trade_data(self.rat_market_trades, "Rat Market Trades")

    def _display_trade_data(self, trade_data_list, header_title):
        """Helper method to display trade data in tabular format."""
        print(f"\n----- {header_title} -------")
        trade_data = []
        for trade in trade_data_list:
            wrapped_loss = self.wrap_text(trade[1], width=40)
            wrapped_gain = self.wrap_text(trade[2], width=40)
            trade_data.append([f"{trade[0]:.3f}", wrapped_loss, wrapped_gain])
        print(tabulate(trade_data, headers=["Marginal", "Loss", "Gain"], tablefmt="fancy_grid"))

    def display_surplus_items(self):
        print(colored("\n----- Gained & Unused Items -------", "cyan", attrs=['bold']))
        for item in self.items_surplus:
            print(item)

    def display_negative_surplus_items(self):
        print(colored("\n----- Lost & Unused Items -------", "cyan", attrs=['bold']))
        for item in self.items_negative_surplus:
            print(item)

    def display_optimization_results(self):
        print(colored("\n----- Optimization Target -------", "green", attrs=['bold']))
        items_per_input = -1.0 / (self.input_per_cycle * self.opt_result.fun)
        print(f"{self.optimize_for.name} per Cycle:  {-1.0 / self.opt_result.fun:10.3f}")
        print(f"{self.optimize_for.name} per {self.optimize_input.name}: {items_per_input:10.3f}")
        print(f"{self.optimize_input.name} per {self.optimize_for.name}: {1.0 / items_per_input:10.3f}")

    def display_summary(self):
        print(colored("\n------ Summary -------", "green", attrs=['bold']))
        self.display_assumptions()
        self.display_player_stats()
        self.display_conversions()
        self.display_trades()
        self.display_special_action_trades()
        self.display_bone_market_trades()
        self.display_rat_market_trades()
        self.display_surplus_items()
        self.display_negative_surplus_items()
        self.display_optimization_results()