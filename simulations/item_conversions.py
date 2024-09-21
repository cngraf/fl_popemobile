from enums import *

def conversion_rate(from_item: Item, to_item: Item) -> float:
    """
    Convert 'amount' of from_item to to_item using the conversion rates.

    Parameters:
    - from_item: the Item enum to convert from
    - to_item: the Item enum to convert to
    - amount: the amount of from_item to convert

    Returns:
    - The number of to_item you get after conversion
    """

    if from_item in item_conversion_rates and to_item in item_conversion_rates[from_item]:
        conversion_rate = item_conversion_rates[from_item][to_item]
        # return amount // conversion_rate  # Use floor division to convert
        # return amount / conversion_rate
        return conversion_rate
    
    # If no conversion is possible, return 0
    return 0

# TODO clean this up or sth
item_conversion_rates = {
    # Stacks items
    Item.LibraryKey: {Item.Echo: 0.0, Item.Stuiver: 0},
    Item.RouteTracedThroughTheLibrary: {Item.Echo: 0.0, Item.Stuiver: 0},
    Item.FragmentaryOntology: {Item.Echo: 0.0, Item.Stuiver: 0},
    Item.DispositionOfTheCardinal: {Item.Echo: 0.0, Item.Stuiver: 0},

    # Econ items
    Item.TantalisingPossibility: {Item.Echo: 0.1, Item.Stuiver: 2},
    Item.RatOnAString: {Item.Echo: 0.01, Item.Stuiver: 0},
    Item.DeepZeeCatch: {Item.Echo: 0.5, Item.Stuiver: 0},

    Item.FinBonesCollected: {Item.Echo: 0.5, Item.Stuiver: 0},
    Item.TempestuousTale: {Item.Echo: 0, Item.Stuiver: 10},
    Item.PartialMap: {Item.Echo: 2.5, Item.Stuiver: 0},
    Item.PuzzlingMap: {Item.Echo: 12.5, Item.Stuiver: 0},
    Item.FlaskOfAbominableSalts: {Item.Echo: 0.1, Item.Stuiver: 0},

    Item.CausticApocryphon: {Item.Echo: 15.5, Item.Stuiver: 250},
    Item.GlimEncrustedCarapace: {Item.Echo: 0, Item.Stuiver: 1250},
    Item.ShardOfGlim: {Item.Echo: 0.01, Item.Stuiver: 0},
    Item.RoofChart: {Item.Echo: 2.53, Item.Stuiver: 50},

    Item.Anticandle: {Item.Echo: 0, Item.Stuiver: 50},

    Item.FragmentOfTheTragedyProcedures: {Item.Echo: 62.5, Item.Stuiver: 0},
    Item.RelicOfTheFifthCity: {Item.Echo: 2.5, Item.Stuiver: 50},
    Item.MagnificentDiamond: {Item.Echo: 12.5, Item.Stuiver: 0},
    Item.OneiromanticRevelation: {Item.Echo: 62.5, Item.Stuiver: 0},
    Item.StormThrenody: {Item.Echo: 12.5, Item.Stuiver: 0},
    Item.VolumeOfCollatedResearch: {Item.Echo: 2.5, Item.Stuiver: 0},
    Item.GlimpseOfAnathema: {Item.Echo: 312.5, Item.Stuiver: 6250},

    Item.VolumeOfCollatedResearch: { 
        Item.Echo: 0.5
    },

    Item.IncisiveObservation: {
        Item.Echo: 0.5
    }

    # # Menaces
    # # Ballpark @ 1 action to clear 6 points with social alt
    # Item.Wounds: {Item.Echo: -1, Item.Stuiver: -20, Item.Action: 1/6},
    # Item.Nightmares: {Item.Echo: -1, Item.Stuiver: -20, Item.Action: 1/6},

    # # Second Chances
    # # Ballpark @ 2/action @ 6 EPA
    # Item.SuddenInsight: { Item.Echo: 3, Item.Action: 0.5 },
    # Item.HastilyScrawledWarningNote: {Item.Echo: 3, Item.Action: 0.5},
}