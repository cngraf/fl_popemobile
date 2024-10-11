from enums import *
import helper.utils as utils

class Player:
    def __init__(self,
        qualities: dict = {},
        basic_stats_val: int = 310,
        advanced_stats_val: int = 15,
        bdr_stats_val: int = 18,
        defensive_stats_val: int = 3):

        self.qualities = {}

        for stat in BASIC_STATS:
            self.qualities[stat] = basic_stats_val

        for stat in ADVANCED_STATS:
            self.qualities[stat] = advanced_stats_val

        for stat in BDR_STATS:
            self.qualities[stat] = bdr_stats_val

        for stat in DEFENSIVE_STATS:
            self.qualities[stat] = defensive_stats_val

        for stat in RENOWN_ITEMS:
            self.qualities[stat] = 40

        # Cap to current in-game max from quickchange slots
        self.qualities[Item.StewardOfTheDiscordance] = min(advanced_stats_val, 8)
        self.qualities[Item.Chthonosophy] = min(advanced_stats_val, 9)

        for key, value in qualities.items():
            self.qualities[key] = value

        self.wounds_reduction = 2
        self.scandal_reduction = 2
        self.suspicion_reduction = 2
        self.nightmares_reduction = 2
        self.troubled_waters_reduction = 2

    def get(self, item: Item):
        return self.qualities.get(item, 0)

    # TODO this logic is duplicated in a bazillion different places
    # TODO: add a threshold to auto-use a second chance item?
    def pass_rate(self, stat, difficulty):
        player_level = self.qualities[stat]
        if stat in (Item.Watchful, Item.Shadowy, Item.Dangerous, Item.Persuasive):
            return utils.broad_challenge_pass_rate(player_level, difficulty)
        else:
            return utils.narrow_challenge_pass_rate(player_level, difficulty)
        
    # def challenge_ev(self, stat, difficulty, on)

    def wounds_ev(self, int):
        blocked = min(2, int * utils.menace_multiplier(self.wounds_reduction))
        return max(0, int - blocked)

    def scandal_ev(self, int):
        blocked = min(2, int * utils.menace_multiplier(self.scandal_reduction))
        return max(0, int - blocked)

    def nightmares_ev(self, int):
        blocked = min(2, int * utils.menace_multiplier(self.nightmares_reduction))
        return max(0, int - blocked)                

    def suspicion_ev(self, int):
        blocked = min(2, int * utils.menace_multiplier(self.suspicion_reduction))
        return max(0, int - blocked)
    
    @staticmethod
    def copy_with_added(player, qualities):
        """
        Static method to create a new Player object by summing the qualities of the input Player object
        with the values from the provided dictionary.

        :param player: Player object whose qualities will be summed with the dictionary.
        :param qualities: Dictionary with Item keys and int values to add to the player's qualities.
        :return: A new Player object with updated qualities.
        """
        # Create a copy of the original player's qualities to avoid modifying the original object
        new_qualities = player.qualities.copy()

        # Iterate over the dictionary and sum values to the new_qualities
        for item, value in qualities.items():
            if item in new_qualities:
                new_qualities[item] += value  # Add value if the item already exists
            else:
                new_qualities[item] = value  # Add the new item if it doesn't exist

        # Return a new Player object with the updated qualities
        return Player(new_qualities)



player_endgame_f2p = Player(
    basic_stats_val=310,
    advanced_stats_val=12,
    qualities={
        Item.SealOfStJoshua: 1,
        Item.InvolvedInARailwayVenture: 140,
    }
)

player_generic_endgame_whale = Player(
    basic_stats_val=334,
    advanced_stats_val=18,
    bdr_stats_val=20,
    qualities={
        Item.Neathproofed: 8,
        Item.Insubstantial: 4,
        Item.Inerrant: 6,

        Item.SealOfStJoshua: 1,
        Item.InvolvedInARailwayVenture: 140,
    }
)


# aka "cosmogone silvererhand"
player_third_city_silverer = Player.copy_with_added(
    player=player_generic_endgame_whale,
    qualities={
        Item.SetOfCosmogoneSpectacles: 1,

        Item.BagALegend: 1,
        Item.LongDeadPriestsOfRedBird: 1,
    })

player_generic_bal = Player.copy_with_added(
    player=player_generic_endgame_whale,
    qualities={
        Item.BagALegend: 1
    }
)

player_generic_licentiate = Player.copy_with_added(
    player=player_generic_endgame_whale,
    qualities={
        Item.ListOfAliasesWrittenInGant: 1,
    })

player_bal_licentiate = Player.copy_with_added(
    player=player_generic_licentiate,
    qualities={
        Item.ListOfAliasesWrittenInGant: 1,
        
        Item.BagALegend: 1,
    })