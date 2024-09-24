import random
from enums import *

from collections import defaultdict
from enum import Enum, auto

'''
to get enums module import to work, need to run like so:
`python3 -m simulations.stacks2`

Simple version with more human-legible strategy

Group actions

# High progress
    A Locked Gate
        Use a key
            - 1 key => 15 prog

    A Librarian's Office
        Unlock the cart
            - 1 key => 15 prog
            - with big surplus of keys

    A Stone Gallery
        Follow a borehole through the back of...
            - 2 routes => 10 prog
            - only available at certain times
                - dead stars 2
                - precipice 1/2
                - carto 1

    A God's Eye View
        Focus on the path ahead
            - 5 frags => 15 prog
            - only worth using spare frags from Librarian's Office

    A Tea Room?



# Hand clear + progress
    A Dead End?
        Tie a rope to the railing and descend

    A Grand Staircase
        Make an informed decision
            - costs 1 route

    The Shape of the Labyrinth
        Rethink your movements
            - 10 progress
            - costs between 2 and 5 routes

# Econ + routes + 0 progress
    A Map Room
        Look for maps of the library
    A Dead End?
        Take advantage of the vantage point


# Free* 5 progress
    A Poison-Gallery
        Use furniture as stepping stones

    The Grey Cardinal
        Offer the cardinal a furry lunch

    A Gaoler-Librarian
        An intervention from the Grey Cardinal

    A Glimpse through a Window
        Move on quickly

    A Black Gallery
        Both options
            - depends on HitL

    A Flowering Gallery
        Keep going
            - depends on HitL

            

# Progress + noise
    A Black Gallery
        Light a lantern
            - Fail with woesel
            - 2? cp noise, NO menaces

    A Dead End?
        Tie a rope to the railing and descend
            - Fail with woesel
            - Adds wounds
            - Also clears hand
        
# Keys
    A Gaoler-Librarian
        - Try to lift one of its keys


# Cards to avoid entirely
- Both Cartographer cards
- An Atrium
- A Discarded Ladder
- An Index
- A Terrible Shushing



Example output
Progress: [==================================================] 100.00% (5000/5000)
ApocryphaSought: ApocryphaSought.SomeFrenchBullshit
Cartographer Enabled: False
Total runs: 5000
Successes: 5000 (100.00%)
Failures: 0 (0.00%)
Average actions per run: 23.26
Keys collected: 6219
Routes collected: 15279
Frag. Ontologies collected: 1317

Card and Action Play Counts:
Card                 Per Run Played/Drawn Action                                   Per Run    Success%
-----------------------------------------------------------------------------------------------
The Reading Room               1.00/1.00  (100.00%)
                                          Open the book                            1.0        100.0%
A Dead End?                    2.27/2.27  (100.00%)
                                          Tie a rope to the railing and descend    0.3        100.0%
                                          (WOESEL) Tie a rope to the railing an... 0.263
                                          Take advantage of the vantage point      1.7        63.0%
                                          See through the Cartographer's eyes      0
A Map Room                     2.30/2.30  (100.00%)
                                          Look for maps of the library             2.3        83.3%
                                          Look for maps of the Neath               0
                                          Get a lead from the Cartographer         0
A Librarian's Office           0.80/0.80  (100.00%)
                                          Pick through the drawers                 0.8        89.6%
                                          Take the opposite door                   0
                                          Unlock the cart                          0
A Gaoler-Librarian             1.30/1.30  (99.94%)
                                          Distract the Gaoler                      0
                                          Try to lift one of its keys              1.3        77.8%
                                          An intervention from the Grey Cardina... 0.0        100.0%
A Chained Octavo               0.07/0.07  (99.70%)
                                          Unchain it                               0.1        100.0%
                                          Examine this section, then move on       0.0        35.0%
Apocrypha Found                0.94/0.94  (99.60%)
                                          Claim the book                           0.9        100.0%
A Stone Gallery                1.89/2.18  (86.48%)
                                          Make your way through the silent gall... 0.4        51.2%
                                          Stop and examine the ancient volumes     0
                                          (WOESEL) Stop and examine the ancient... 0.002
                                          Follow a borehole through the back of... 1.5        100.0%
A Black Gallery                1.83/2.14  (85.45%)
                                          Light a lantern                          0
                                          (WOESEL) Light a lantern                 0.286
                                          Navigate by alternate senses             1.5        100.0%
A Glimpse through a Window     0.19/0.23  (83.97%)
                                          Stop and look through                    0.1        100.0%
                                          Move on quickly                          0.1        100.0%
A Tea Room?                    1.39/1.73  (80.15%)
                                          Take a moment to regroup                 0
                                          Consult your maps of the library         1.3        86.7%
                                          Try to make sense of what you've seen    0.0        59.1%
A God's Eye View               0.05/0.06  (78.35%)
                                          Try to hold it all in your mind at on... 0.0        55.6%
                                          Focus on the path ahead                  0.0        100.0%
The Grey Cardinal              1.52/1.95  (77.92%)
                                          Offer the cardinal a furry lunch         1.5        100.0%
                                          Offer the cardinal a tin of something... 0
                                          Engage the Cardinal in conversation      0.0        100.0%
A Locked Gate                  1.18/1.66  (71.42%)
                                          Use a key                                1.2        100.0%
The Shape of the Labyrinth     0.28/0.40  (68.75%)
                                          Rethink your movements                   0.3        100.0%
                                          Reject the significance of shape         0.0        60.0%
A Poison-Gallery               0.96/1.71  (55.91%)
                                          Use furniture as stepping stones         1.0        90.1%
                                          Prepare an antidote                      0
A Terrible Shushing            0.05/0.09  (55.25%)
                                          Find a hiding place                      0.1        82.9%
                                          Hurry along                              0
                                          Quiet the Cartographer                   0
A Grand Staircase              0.74/1.60  (46.60%)
                                          Make an informed decision                0.7        100.0%
An Atrium                      0.04/1.44  (2.70%)
                                          Continue on the same heading             0.0        99.3%
                                          Atrium Action 2                          0.0        59.2%
A Discarded Ladder             0.02/1.42  (1.62%)
                                          Climb                                    0.0        87.0%
An Index                       0.01/0.98  (1.10%)
                                          Search for a reference card              0.0        100.0%
                                          Try to understand the organization of... 0
                                          Situate yourself within the greater w... 0
A Flowering Gallery            0
                                          Keep going                               0
                                          Eat the fruit of knowledge               0
Snuffbox.png                   0
                                          Computernofigure.png                     0
                                          Implication.png                          0
Compass.png                    0
                                          Camera2.png                              0
                                          Chart2.png                               0
-----------------------------------------------------------------------------------------------
Item                           Net/Run    Echoes/Action          Stuivers/Action
-----------------------------------------------------------------------------------------------
LibraryKey                     0.001      0.0000
RouteTracedThroughTheLibrar... 0.001      0.0000
FragmentaryOntology            0.001      0.0000
TantalisingPossibility         217.201    0.9338                 18.6752
RatOnAString                   -1.518     -0.0007
DeepZeeCatch                   0.281      0.0060
FinBonesCollected              0.224      0.0048
Anticandle                     9.406      1.0109                 20.2185
FragmentOfTheTragedyProcedu... 0.941      2.5273
RelicOfTheFifthCity            9.406      1.0109                 20.2185
GlimpseOfAnathema              0.059      0.7980                 15.9603
Wounds                         0.812      -0.0349                 -0.6982
Nightmares                     0.643      -0.0276                 -0.5525
-----------------------------------------------------------------------------------------------
Echoes Only Per Action                    6.2286 E
Stuivers Only Per Action                                         73.8217 S
Echoes/Stuivers Per Action                6.2286 E

'''

ev_progress = 1
ev_key_base = ev_progress * 10
ev_route_base = ev_progress * 2
# ev_frag_base = ev_progress * 1.2
ev_frag_base = 0
ev_hand_clear = ev_progress * 1
ev_noises_base = -1
ev_gaoler = 3

simple_ev_gain_key = 200
simple_ev_map_room = 100
simple_first_noise_ev = 1
simple_ev_frag = 0
simple_ev_route = 2

ev_echo = 1
ev_stuiver = ev_echo * 0.05
ev_tant = ev_stuiver * 2
ev_wounds = -1 * ev_echo
ev_nightmares = -1 * ev_echo

simple_ev_echo = 1
# simple_evs = {
#     Item.Echo: simple_ev_echo,
#     Item.TantalisingPossibility: simple_ev_echo * 0.1
#     Item.LibraryKey: simple_ev_echo
# }


item_values = {
    # Stacks items
    Item.LibraryKey: {Item.Echo: 0.01, Item.Stuiver: 0},
    Item.RouteTracedThroughTheLibrary: {Item.Echo: 0.01, Item.Stuiver: 0},
    Item.FragmentaryOntology: {Item.Echo: 0.01, Item.Stuiver: 0},
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

    Item.CausticApocryphon: {Item.Echo: 0, Item.Stuiver: 250},
    Item.GlimEncrustedCarapace: {Item.Echo: 0, Item.Stuiver: 1250},
    Item.ShardOfGlim: {Item.Echo: 0.01, Item.Stuiver: 0},
    Item.RoofChart: {Item.Echo: 2.53, Item.Stuiver: 50},

    # Big assumption, no sale value atm
    Item.Anticandle: {Item.Echo: 2.5, Item.Stuiver: 50},
    Item.FragmentOfTheTragedyProcedures: {Item.Echo: 62.5, Item.Stuiver: 0},
    Item.RelicOfTheFifthCity: {Item.Echo: 2.5, Item.Stuiver: 50},
    Item.MagnificentDiamond: {Item.Echo: 12.5, Item.Stuiver: 0},
    Item.OneiromanticRevelation: {Item.Echo: 62.5, Item.Stuiver: 0},
    Item.StormThrenody: {Item.Echo: 12.5, Item.Stuiver: 0},
    Item.VolumeOfCollatedResearch: {Item.Echo: 2.5, Item.Stuiver: 0},
    Item.GlimpseOfAnathema: {Item.Echo: 312.5, Item.Stuiver: 6250},

    # Menaces
    # Ballpark @ 1 action to clear 6 points with social alt
    Item.Wounds: {Item.Echo: -1, Item.Stuiver: -20, Item.Action: 1/6},
    Item.Nightmares: {Item.Echo: -1, Item.Stuiver: -20, Item.Action: 1/6},

    # Second Chances
    # Ballpark @ 2/action @ 6 EPA
    Item.SuddenInsight: { Item.Echo: 3, Item.Action: 0.5 },
    Item.HastilyScrawledWarningNote: {Item.Echo: 3, Item.Action: 0.5},
}

class OutfitList:
    def __init__(self, woesel_mode: False):
        # atrum2
        self.watchful = 332

        # atrium1, index1
        self.watchful_plus_inerrant15 = 311 + 5 * 15

        # deadend1
        self.watchful_plus_shadowy = 332 + 247

        # stonegallery3
        self.watchful_plus_dangerous = 332 + 261

        # deadend2
        self.watchful_plus_cthonosophy15 = 323 + 8 * 15

        # gaoler1, shushing1, shushing2
        self.shadowy = 323

        # posiongallery1
        self.shadowy_plus_neathproofed15 = 278 + 8 * 15

        # unwound thread
        self.shadowy_plus_inerrant15 = 290 + 6 * 15

        # blackGallery1, gaoler2
        self.shadowy_plus_insubstantial15 = 306 + 4 * 15

        # stonegallery2, shape2, octavo2
        self.cthonosophy = 9

        # greycaridnal3
        self.persuasive_plus_bizarre10 = 260 + 28 * 10

        # blackgallery2
        self.watchful_plus_monstrous10_inerrant15 = 295 + 13 * 10 + 6 * 15

        # poisongallery2
        self.kataleptic_toxicology = 16

        # flowering1
        self.neathproofed_plus_inerrant = 8 + 3

        if (woesel_mode):
            for attr in self.__dict__:
                setattr(self, attr, 0)

# no fate, no seasonal items, no exclusives, etc.
# not calculating this all out
# assume each secondary stat slot costs -5 in the base stat
f2p_min_endgame = OutfitList(False)
f2p_min_endgame_base_stats = 230
f2p_min_endgame.watchful = f2p_min_endgame_base_stats + 74
f2p_min_endgame.shadowy = f2p_min_endgame_base_stats + 78
f2p_min_endgame.cthonosophy = 5 + 1
f2p_min_endgame.kataleptic_toxicology = 7 + 4
f2p_min_endgame.neathproofed_plus_inerrant = 5 + 3
f2p_min_endgame.persuasive_plus_bizarre10 = f2p_min_endgame_base_stats + 76 + 17 * (10 - 5)
f2p_min_endgame.shadowy_plus_inerrant15 = f2p_min_endgame.shadowy + (3 * (15 - 5)) 
f2p_min_endgame.shadowy_plus_insubstantial15 = f2p_min_endgame.shadowy + (2 * (15 - 5))
f2p_min_endgame.shadowy_plus_neathproofed15 = f2p_min_endgame.shadowy + (5 * (15 - 5)) 
f2p_min_endgame.watchful_plus_cthonosophy15 = f2p_min_endgame.watchful + (5 * 10) + (15 - 5)
f2p_min_endgame.watchful_plus_dangerous = f2p_min_endgame.watchful + f2p_min_endgame_base_stats
f2p_min_endgame.watchful_plus_shadowy = f2p_min_endgame.watchful + f2p_min_endgame_base_stats
f2p_min_endgame.watchful_plus_inerrant15 = f2p_min_endgame.watchful + (3 * (15 - 5)) 
f2p_min_endgame.watchful_plus_monstrous10_inerrant15 = \
    f2p_min_endgame.watchful + (5 * 10) + (3 * 5) + (3 * 10)

class ApocryphaSought(Enum):
    BannedWorks = 201
    DeadStars = 202
    SomeFrenchBullshit = 203
    UnrealPlaces = 204
    # ChainedOctavo = 1001

class Action:
    def __init__(self, name):
        self.name = name
        self.rare_success_rate = 0.0

    def can_perform(self, state: 'LibraryState'):
        return True

    def perform(self, state: 'LibraryState'):
        rate = self.pass_rate(state)
        if random.random() < rate:
            self.perform_success(state)
            return "Success"
        else:
            self.perform_failure(state)
            return "Failure"

    def ev(self, state: 'LibraryState'):
        pass_rate = min(1.0, max(0.0, self.pass_rate(state)))
        success_ev = self.success_ev(state)
        failure_ev = self.failure_ev(state)


        if pass_rate is None:
            print(f"Debug: {self.name} - pass_rate: {pass_rate}, success_ev: {success_ev}, failure_ev: {failure_ev}")
            pass_rate = 0.0
        if success_ev is None:
            print(f"Debug: {self.name} - pass_rate: {pass_rate}, success_ev: {success_ev}, failure_ev: {failure_ev}")
            success_ev = 0.0
        if failure_ev is None:
            print(f"Debug: {self.name} - pass_rate: {pass_rate}, success_ev: {success_ev}, failure_ev: {failure_ev}")
            failure_ev = 0.0

        return pass_rate * success_ev + (1.0 - pass_rate) * failure_ev

    def pass_rate(self, state: 'LibraryState'):
        return 1.0
    
    def perform_success(self, state: 'LibraryState'):
        pass

    def success_ev(self, state: 'LibraryState'):
        return 1.0
    
    def perform_failure(self, state: 'LibraryState'):
        pass

    def failure_ev(self, state: 'LibraryState'):
        return 0.0
    
    def broad_success_rate(self, dc, stat_value):
        return 0.6 * stat_value/dc
    
    def narrow_success_rate(self, dc, stat_value):
        return 0.5 + (stat_value - dc) * 0.1

class LibraryState:
    def __init__(self):

        # self.normal_outfit = OutfitList(woesel_mode = False)
        self.normal_outfit = f2p_min_endgame
        self.woesel_outfit = OutfitList(woesel_mode = True)

        self.outfits = self.normal_outfit

        self.items = {
            # Stacks items
            Item.LibraryKey: 5,
            Item.RouteTracedThroughTheLibrary: 20,
            Item.FragmentaryOntology: 25,
            Item.DispositionOfTheCardinal: 5,

            # Econ items
            Item.TantalisingPossibility: 0,
            Item.RatOnAString: 0,
            Item.DeepZeeCatch: 0,
            Item.FinBonesCollected: 0,
            Item.TempestuousTale: 0,
            Item.PartialMap: 0,
            Item.PuzzlingMap: 0,
            Item.FlaskOfAbominableSalts: 0,

            Item.CausticApocryphon: 0,
            Item.GlimEncrustedCarapace: 0,
            Item.ShardOfGlim: 0,
            Item.RoofChart: 0,
            Item.Anticandle: 0,
            Item.FragmentOfTheTragedyProcedures: 0,
            Item.RelicOfTheFifthCity: 0,
            Item.MagnificentDiamond: 0,
            Item.OneiromanticRevelation: 0,
            Item.StormThrenody: 0,
            Item.VolumeOfCollatedResearch: 0,
            Item.GlimpseOfAnathema: 0,

            # Menaces
            Item.Wounds: 0,
            Item.Nightmares: 0,

            Item.HastilyScrawledWarningNote: 0
        }
        
        # Carried over
        # self.library_keys = 0  # Count of keys collected
        # self.routes_traced = 0
        # self.fragmentary_ontologies = 0        
        # self.tantalizing_possibilities = 0
        # self.disposition_of_the_cardinal = 0

        self.wounds = 0
        self.nightmares = 0

        self.completed_normal_runs = 0
        self.completed_anathema_runs = 0
        self.failed_runs = 0

        self.gross_keys = 0
        self.gross_routes = 0
        self.gross_frags = 0 

        self.hour_in_the_library = 0
        self.apocrypha_sought = 0

        self.cartographer_enabled = False
        self.in_search_of_lost_time = 1
        self.progress = 0
        self.noises = 0
        self.anathema_unchained = 0

        self.refill_action = RefillHandAction()
        self.hand = []
        self.actions = 0
        self.deck = [
            ApocryphaFound(),
            ReadingRoom(),

            Atrium(),
            DeadEnd(),
            DiscardedLadder(),
            GrandStaircase(),
            LockedGate(),
            MapRoom(),
            PoisonGallery(),
            StoneGallery(),
            Index(),
            LibrariansOffice(),
            FloweringGallery(),
            BlackGallery(),
            GaolerLibrarian(),
            TerribleShushing(),
            GodsEyeView(),
            ShapeOfTheLabyrinth(),
            GreyCardinal(),
            GlimpseThroughAWindow(),
            TeaRoom(),

            CartographerSnuffbox(),
            CartographerCompass(),
            
            ChainedOctavo()
        ]

        self.card_draw_counts = {card.name: 0 for card in self.deck}
        self.card_play_counts = {card.name: 0 for card in self.deck}
        # self.action_play_counts = {self.refill_action.name: 0}
        self.action_success_counts = defaultdict(int)
        self.action_failure_counts = defaultdict(int)
        self.action_woesel_counts = defaultdict(int)


    def total_runs(self):
        return self.failed_runs + self.completed_normal_runs + self.completed_anathema_runs

    def start_new_run(self, apocrypha_sought, cartographer_enabled):
        self.actions += 1
        self.progress = 0
        self.noises = 0
        self.hand.clear()
        self.in_search_of_lost_time = 1

        self.apocrypha_sought = apocrypha_sought
        self.cartographer_enabled = cartographer_enabled

        if apocrypha_sought == ApocryphaSought.BannedWorks:
            self.hour_in_the_library = 1

        if apocrypha_sought == ApocryphaSought.DeadStars:
            self.hour_in_the_library = 2

        if apocrypha_sought == ApocryphaSought.SomeFrenchBullshit:
            self.hour_in_the_library = 3

        if apocrypha_sought == ApocryphaSought.UnrealPlaces:
            self.hour_in_the_library = 4

    # def add_route(self, val):
    #     pass

    def ev_key(self, val = 1):
        unit_ev = ev_key_base
        keys = self.items[Item.LibraryKey]

        if keys == 0 and self.anathema_unchained == 0:
            unit_ev *= 2
        elif keys > 5:
            unit_ev *= 0.2
        
        return unit_ev * val
    
    def ev_key_simple(self, val = 1):
        keys = self.items[Item.LibraryKey]

        if keys == 0 and self.anathema_unchained == 0:
            unit_ev *= 2
        elif keys > 5:
            unit_ev *= 0.2
        
        return unit_ev * val    

    def ev_progress(self, val):
        if self.progress >= 40:
            return 0

        if val == 15:
            if self.progress < 29:
                return val * ev_progress
            else:
                return 2 * ev_progress
        elif val == 10:
            if self.progress < 34:
                return val * ev_progress
            else:
                return 3 * ev_progress
        elif val == 5:
            if self.progress < 39:
                return val * ev_progress
            else:
                return 4 * ev_progress 
        elif val == 1:
            if self.progress % 5 == 4:
                return ev_progress * 5
            else:
                return val * ev_progress

        gain = min(40 - self.progress, val)
        return gain * ev_progress
    
    def ev_route(self, val=1):
        # prob coulda done it the dumb way for less work & better results 
        # assume you never go below N and treat the challenges as 100%
        # return simple_ev_route * val

        # need 5 to 100% TeaRoom2, +6 to buffer biggest single cost
        target = 20
        unit_ev = simple_ev_route
        current = self.items[Item.RouteTracedThroughTheLibrary]

        # if (self.in_search_of_lost_time == 1 and self.hour_in_the_library in [2,3]) \
        #     or (self.in_search_of_lost_time == 2 and self.hour_in_the_library in [3,4]):
        #     unit_ev = max(ev_route_base, ev_progress * 2.5)

        if current < target:
            unit_ev += 10

        return unit_ev * val
    
    def ev_frag(self, val):
        # need 14 to 100% atrium2 with 300 watchful
        # plus 5 for biggest single spend, round up
        # target = 25
        # unit_ev = ev_frag_base
        # current = self.items[Item.FragmentaryOntology]

        # if current < target:
        #     unit_ev += 1

        # return unit_ev * val
        return simple_ev_frag * val
    
    def ev_noises(self, val):
        if val == 0: return 0

        deck_ev = 0
        unit_ev = ev_noises_base
        current = self.noises
        next = current + val

        gaoler_threshold = 1
        shushing_threshold = 10
        you_died = 36

        gaoler_ev = self.ev_key(1) * 0.33
        shushing_ev = -4

        if self.in_search_of_lost_time == 2:
            gaoler_ev /= 2
            shushing_ev /= 2

        if next > gaoler_threshold and current < gaoler_threshold:
            deck_ev += gaoler_ev

        if current + val >= you_died:
            return -100_000
        elif current < shushing_threshold and next >= shushing_threshold:
            deck_ev += shushing_ev
        elif current >= shushing_threshold and next < shushing_threshold:
            deck_ev -= shushing_ev

        return deck_ev + unit_ev * val

    def ev_hand_clear(self):
        ev_discard_good_card = -10
        ev_octavo_in_deck = 10
        # if any(card.name == "A Chained Octavo" for card in self.hand): 
        #     ev -= 100

        # not including hand clear cards themselves
        good_cards = [
            ReadingRoom,
            MapRoom,
            LibrariansOffice,
            GaolerLibrarian,
            ApocryphaFound,
            ChainedOctavo,
            BlackGallery,
            TeaRoom
        ]

        if self.items[Item.LibraryKey] > 0:
            good_cards.append(LockedGate)

        for held_card in self.hand:
            for good_card in good_cards:
                if isinstance(held_card, good_card):
                    return ev_discard_good_card

        if self.octavo_in_deck():
            return ev_hand_clear + ev_octavo_in_deck

        return ev_hand_clear
    
    def octavo_in_deck(self):
        return self.in_search_of_lost_time == 1 \
            and self.anathema_unchained == 0 \
            and not any(card.name == "A Chained Octavo" for card in self.hand)
    
    def draw_card(self):
        drawn, lowest = None, float('inf')
        for card in self.deck:
            if card not in self.hand and card.can_draw(self):
                rand = random.random() / card.weight
                if rand < lowest:
                    drawn = card
                    lowest = rand

        self.card_draw_counts[drawn.name] += 1
        self.hand.append(drawn)

    def best_action_by_simple_ranking(self):
        progress = self.progress
        keys = self.items[Item.LibraryKey]
        routes = self.items[Item.RouteTracedThroughTheLibrary]
        frags = self.items[Item.FragmentaryOntology]

        high_prio = [
            ChainedOctavoAction1,
        ]

        # Add actions based on the current state
        if keys < 50:
            high_prio.extend([LibrariansOfficeAction1])
            if self.noises < 30:
                high_prio.append(GaolerLibrarianAction2)

        high_prio.extend([
            ReadingRoomAction1,
            ApocryphaFoundAction1,
        ])

        if progress < 30:
            high_prio.extend([
                LockedGateAction1,
                LibrariansOfficeAction3,
                GodsEyeViewAction2
            ])

        high_prio.append(MapRoomAction1)
        
        if routes < 20:
            high_prio.append(DeadEndAction2)

        # group_1.append(RefillHandAction)

        low_prio = []
        if progress < 35:
            if routes >= 5:
                low_prio.append(TeaRoomAction2)
            low_prio.append(StoneGalleryAction3)
            if routes >= 30:
                high_prio.append(ShapeOfTheLabyrinthAction1)

        if keys < 50 and self.noises == 0:
            low_prio.extend([
                BlackGalleryAction1Woesel,
                DeadEndAction1Woesel
            ])

        if routes < 20:
            low_prio.append(DeadEndAction2)        

        low_prio.append(DeadEndAction1)

        if routes >= 20:
            low_prio.append(GrandStaircaseAction1)

        # Basic options that are always valid
        low_prio.extend([            
            GlimpseThroughAWindowAction2,
            FloweringGalleryAction1,
            GreyCardinalAction1,
            BlackGalleryAction1,
            BlackGalleryAction2,
            StoneGalleryAction1,
            GaolerLibrarianAction3,
            PoisonGalleryAction1,
            LibrariansOfficeAction2,
            TerribleShushingAction2,
            ShapeOfTheLabyrinthAction2,
            AtriumAction2,
            IndexAction3,

            DiscardedLadderAction1,

            AtriumAction1,
            ChainedOctavoAction2,
            GrandStaircaseAction1,
            GrandStaircaseAction2,
            IndexAction1,
            GrandStaircaseAction1,
            TeaRoomAction3
        ])

        # Find the best action from the ranked list that is in the hand
        for ranked_action in high_prio:
            for card in self.hand:
                for card_action in card.actions:
                    if isinstance(card_action, ranked_action) and card_action.can_perform(self):
                        return (card, card_action)

        # If no card matches, check the refill action
        if self.refill_action.can_perform(self):
            return (None, self.refill_action)
        
        for ranked_action in low_prio:
            for card in self.hand:
                for card_action in card.actions:
                    if isinstance(card_action, ranked_action) and card_action.can_perform(self):
                        return (card, card_action)


        # If no action can be performed, return None
        return (None, None)

    def step(self):
        # print("Cards in hand: " + str(len(self.hand)))
        # print("Progress: " + str(self.progress))

        if self.in_search_of_lost_time > 2:
            self.start_new_run(self.apocrypha_sought, self.cartographer_enabled)

        if len(self.hand) == 0:
            self.refill_action.perform(self)
            self.action_success_counts[self.refill_action.name] += 1
            return

        # Evaluate the best action across all cards in hand
        best_card, best_action, best_action_ev = None, None, -float('inf')
        use_woesel = False

        best_card, best_action = self.best_action_by_simple_ranking()

        if (isinstance(best_action, DeadEndAction1) or isinstance(best_action, BlackGalleryAction1)) \
            and self.noises == 0:
                use_woesel = True

        # Fallback on complex algo if simple ranking fails
        if best_action == None:
            if self.refill_action.can_perform(self):
                best_action = self.refill_action
                best_action_ev = self.refill_action.ev(self)
            else:
                self.outfits = self.normal_outfit
                for card in self.hand:
                    for action in card.actions:
                        if action.can_perform(self):
                            action_ev = action.ev(self)
                            if action_ev > best_action_ev:
                                best_card, best_action, best_action_ev = card, action, action_ev

                self.outfits = self.woesel_outfit
                for card in self.hand:
                    for action in card.actions:
                        if action.can_perform(self):
                            action_ev = action.ev(self)
                            if action_ev > best_action_ev:
                                use_woesel = True
                                best_card, best_action, best_action_ev = card, action, action_ev

                if card is not None:
                    print("Cards in hand: " + str(len(self.hand)))
                    for card in self.hand:
                        print(card.name)
                    print("Best action: " + best_action.name)
        if use_woesel:
            self.outfits = self.woesel_outfit
            best_action.perform(self)
            self.action_woesel_counts[best_action.name] += 1

        else:
            self.outfits = self.normal_outfit
            outcome = best_action.perform(self)
            if outcome == "Success":
                self.action_success_counts[best_action.name] += 1
            else:
                self.action_failure_counts[best_action.name] += 1

        if best_card is not None:
            self.actions += 1
            self.card_play_counts[best_card.name] += 1

            if best_card in self.hand:
                self.hand.remove(best_card)

        self.hand = [card for card in self.hand if card.can_draw(self)]

        # Check for failure condition
        if self.noises >= 36:
            self.failed_runs += 1
            self.hand.clear()
            self.progress = 0
            self.noises = 0
            self.in_search_of_lost_time = 1
            self.actions += 1

    def run(self, steps):
        while self.actions < steps:
            self.step()

class LibraryCard:
    def __init__(self, name, weight=1.0):
        self.name = name
        self.weight = weight
        self.actions = []  # List of possible actions

    def can_draw(self, state: LibraryState):
        return True
    
class RefillHandAction(Action):
    def __init__(self):
        super().__init__("Redraw")

    def can_perform(self, state: LibraryState):
        return len(state.hand) < 4

    def perform_success(self, state: LibraryState):
        while len(state.hand) < 4:
            state.draw_card()

    def success_ev(self, state: LibraryState):
        if state.in_search_of_lost_time == 1 and state.anathema_unchained <= 0:
            return 20
        
        if state.progress >= 40:
            return ev_progress * 6
        
        return ev_progress * 5.1

# Specific card implementations with actions
class ApocryphaFound(LibraryCard):
    def __init__(self):
        super().__init__("Apocrypha Found", 10_000.0)
        self.actions = [ApocryphaFoundAction1()]

    def can_draw(self, state: LibraryState):
        return state.progress >= 40 and state.in_search_of_lost_time == 1

class ApocryphaFoundAction1(Action):
    def __init__(self):
        super().__init__("Claim the book")

    def perform_success(self, state: LibraryState):
        state.in_search_of_lost_time = 2
        state.progress = 0
        state.hour_in_the_library = (state.hour_in_the_library + 1) % 5

    def success_ev(self, state: LibraryState):
        return 20
    
class ReadingRoom(LibraryCard):
    def __init__(self):
        super().__init__("The Reading Room", 10_000.0)
        self.actions = [ReadingRoomAction1()]

    def can_draw(self, state: LibraryState):
        return state.progress >= 40 and state.in_search_of_lost_time == 2
    
class ReadingRoomAction1(Action):
    def __init__(self):
        super().__init__("Open the book")

    def perform_success(self, state: LibraryState):
        # TODO separate flag for octavo to be safe
        # TODO other reward options

        state.completed_normal_runs += 1

        if state.anathema_unchained == 10:
            state.items[Item.GlimpseOfAnathema] += 1
        elif state.apocrypha_sought == ApocryphaSought.BannedWorks:
            state.items[Item.CausticApocryphon] += 9
            state.items[Item.TantalisingPossibility] += 35
        elif state.apocrypha_sought == ApocryphaSought.DeadStars:
            state.items[Item.GlimEncrustedCarapace] += 1
            state.items[Item.TantalisingPossibility] += 495
            state.items[Item.ShardOfGlim] += 400
            # state.items[Item.RoofChart] += 40
        elif state.apocrypha_sought == ApocryphaSought.SomeFrenchBullshit:
            state.items[Item.Anticandle] += 10
            state.items[Item.FragmentOfTheTragedyProcedures] += 1
            state.items[Item.RelicOfTheFifthCity] += 10
            state.items[Item.TantalisingPossibility] += 35
        elif state.apocrypha_sought == ApocryphaSought.UnrealPlaces:
            state.items[Item.OneiromanticRevelation] += 1
            state.items[Item.StormThrenody] += 2
            state.items[Item.PuzzlingMap] += 1
            state.items[Item.VolumeOfCollatedResearch] += 6
            state.items[Item.TantalisingPossibility] += 10

        state.actions += 1 # collect loot

        state.in_search_of_lost_time = 3

        # TODO make this its own action(s)

        # Winding Back the thread
        rate = self.broad_success_rate(250, state.outfits.shadowy_plus_inerrant15)

        # wild guess
        overdue_chance = min(0.5, state.items[Item.LibraryKey] * 0.02)

        # TODO: DC shadowy 200 + 10 DC per noises level
        second_failure_chance = 0.9

        rate *= (1.0 - overdue_chance/second_failure_chance)

        avg_attempts = 1.0 / rate if rate >  0 else 3
        state.actions += avg_attempts
        state.actions += 1 # return to midnight moon

        # pretty sure the octavo run itself reduces this
        state.anathema_unchained = max(0, state.anathema_unchained - 1)

    def success_ev(self, state: LibraryState):
        return ev_echo * 6

class Atrium(LibraryCard):
    def __init__(self):
        super().__init__("An Atrium")
        self.actions = [AtriumAction1(), AtriumAction2()]

class AtriumAction1(Action):
    def __init__(self):
        super().__init__("Continue on the same heading")

    def can_perform(self, state: LibraryState):
        return state.items[Item.RouteTracedThroughTheLibrary] > 0

    def pass_rate(self, state: LibraryState):
        # return 1.0
        bonus = state.items[Item.RouteTracedThroughTheLibrary] * 15
        return self.broad_success_rate(220, state.outfits.watchful_plus_inerrant15 + bonus)

    def perform_success(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] -= 1
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return ev_progress * 5 + state.ev_route(-1)

    def perform_failure(self, state: LibraryState):
        state.noises += 6

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(6)

class AtriumAction2(Action):
    def __init__(self):
        super().__init__("Atrium Action 2")

    def can_perform(self, state: LibraryState):
        return state.in_search_of_lost_time == 1 and state.items[Item.FragmentaryOntology] > 0

    def ev(self, state: LibraryState):
        return 0

    def pass_rate(self, state: LibraryState):
        # return 1.0
        bonus = state.items[Item.FragmentaryOntology] * 15
        return self.broad_success_rate(300, state.outfits.watchful + bonus)

    def perform_success(self, state: LibraryState):
        routes = random.choice([1,2])
        state.progress += 5
        state.items[Item.RouteTracedThroughTheLibrary] += routes
        state.items[Item.FragmentaryOntology] -= 1

        state.gross_routes += routes

    def success_ev(self, state: LibraryState):
        avg_route_ev = (state.ev_route(1) + state.ev_route(2))/2.0
        return state.ev_progress(5) + avg_route_ev + state.ev_frag(-1)

    def perform_failure(self, state: LibraryState):
        state.progress += 1
        state.noises += 1

    def failure_ev(self, state: LibraryState):
        return 0

class DeadEnd(LibraryCard):
    def __init__(self):
        super().__init__("A Dead End?")
        self.actions = [DeadEndAction1(),
                        DeadEndAction1Woesel(),                  
                        DeadEndAction2(),
                        DeadEndAction3()]
                        # DeadEndAction4()]

class DeadEndAction1(Action):
    def __init__(self):
        super().__init__("(WOESEL) Tie a rope to the railing and descend")

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.broad_success_rate(300, state.outfits.watchful_plus_shadowy)

    def perform_success(self, state: LibraryState):
        state.progress += 5
        state.hand.clear()

    def success_ev(self, state: LibraryState):
        return ev_progress * 5 + state.ev_hand_clear()

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.items[Item.Wounds] += 2
        state.noises += random.randint(1,6)

    def failure_ev(self, state: LibraryState):
        if state.noises == 0:
            return state.ev_progress(5) + state.ev_hand_clear() + simple_first_noise_ev
        else:
            return state.ev_progress(5) - 1

class DeadEndAction1Woesel(Action):
    def __init__(self):
        super().__init__("Tie a rope to the railing and descend")

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.broad_success_rate(300, state.outfits.watchful_plus_shadowy)

    def perform_success(self, state: LibraryState):
        state.progress += 5
        state.hand.clear()

    def success_ev(self, state: LibraryState):
        return ev_progress * 5 + state.ev_hand_clear()

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.items[Item.Wounds] += 2
        state.noises += random.randint(1,6)

    def failure_ev(self, state: LibraryState):
        if state.noises == 0:
            return state.ev_progress(5) + state.ev_hand_clear() + simple_first_noise_ev
        else:
            return state.ev_progress(5) - 1

        # ev_noises = sum([state.ev_noises(i) for i in range(1, 7)]) / 6.0
        # return state.ev_progress(5) + ev_wounds * 2 + ev_noises

class DeadEndAction2(Action):
    def __init__(self):
        super().__init__("Take advantage of the vantage point")

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.broad_success_rate(350, state.outfits.watchful_plus_cthonosophy15)

    def perform_success(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] += 2
        state.items[Item.TantalisingPossibility] += 50
        state.gross_routes += 2

    def success_ev(self, state: LibraryState):
        if state.noises > 0:
            return simple_ev_map_room
        else:
            return 0

    def success_ev(self, state: LibraryState):
        return ev_tant * 50 + state.ev_route(2)

    def perform_failure(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] += 1
        state.gross_routes += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_route()
    
class DeadEndAction3(Action):
    def __init__(self):
        super().__init__("See through the Cartographer's eyes")

    def can_perform(self, state: LibraryState):
        return state.cartographer_enabled

    def pass_rate(self, state: LibraryState):
        return 1.0

    def perform_success(self, state: LibraryState):
        state.items[Item.TempestuousTale] += 10

    def success_ev(self, state: LibraryState):
        return ev_stuiver * item_values[Item.TempestuousTale][Item.Stuiver] * 10

class DiscardedLadder(LibraryCard):
    def __init__(self):
        super().__init__("A Discarded Ladder")
        self.actions = [DiscardedLadderAction1()]

class DiscardedLadderAction1(Action):
    def __init__(self):
        super().__init__("Climb")

    def pass_rate(self, state: LibraryState):
        # return 0.99
        return self.broad_success_rate(200, state.outfits.watchful)
    
    def ev(self, state: LibraryState):
        return 0    

    def perform_success(self, state: LibraryState):
        routes = random.choice([1,2])
        state.items[Item.RouteTracedThroughTheLibrary] += routes
        state.gross_routes += routes

    def success_ev(self, state: LibraryState):
        return (state.ev_route(1) + state.ev_route(2))/2.0

    def perform_failure(self, state: LibraryState):
        state.items[Item.Wounds] += 1
        state.noises += 6

    def failure_ev(self, state: LibraryState):
        return ev_wounds + state.ev_noises(6)

class GrandStaircase(LibraryCard):
    def __init__(self):
        super().__init__("A Grand Staircase")
        # TODO: other actions locked by having any Routes
        self.actions = [GrandStaircaseAction1(), GrandStaircaseAction2()]

class GrandStaircaseAction1(Action):
    def __init__(self):
        super().__init__("Make an informed decision")

    def can_perform(self, state: LibraryState):
        return state.items[Item.RouteTracedThroughTheLibrary] > 0

    def perform_success(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] -= 1
        state.progress += 5
        state.hand.clear()

    def success_ev(self, state: LibraryState):
        return state.ev_hand_clear() + state.ev_progress(5) + state.ev_route(-1)

class GrandStaircaseAction2(Action):
    def __init__(self):
        super().__init__("Go up/Go down")

    def can_perform(self, state: LibraryState):
        return state.items[Item.RouteTracedThroughTheLibrary] == 0

    def pass_rate(self, state: LibraryState):
        return 0.5

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)
    
    def perform_failure(self, state: LibraryState):
        state.progress += 1
        state.noises += 1
    
    def failure_ev(self, state: LibraryState):
        return state.ev_progress(1) + state.ev_noises(1)

class LockedGate(LibraryCard):
    def __init__(self):
        super().__init__("A Locked Gate", 0.8)
        self.actions = [LockedGateAction1()]

class LockedGateAction1(Action):
    def __init__(self):
        super().__init__("Use a key")

    def can_perform(self, state: LibraryState):
        return state.items[Item.LibraryKey] > 0

    def perform_success(self, state: LibraryState):
        state.items[Item.LibraryKey] -= 1
        state.progress += 15

    def ev(self, state: LibraryState):
        return state.ev_progress(15) + state.ev_key(-1)

class MapRoom(LibraryCard):
    def __init__(self):
        super().__init__("A Map Room")
        self.actions = [MapRoomAction1(), MapRoomAction2(), MapRoomAction3()]

class MapRoomAction1(Action):
    def __init__(self):
        super().__init__("Look for maps of the library")

    def pass_rate(self, state: LibraryState):
        # return 0.9
        return self.broad_success_rate(220, state.outfits.watchful)

    def perform_success(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] += random.choice([1,2])
        state.items[Item.TantalisingPossibility] += 50

    def ev(self, state: LibraryState):
        return simple_ev_map_room

    def success_ev(self, state: LibraryState):
        return (state.ev_route(1) + state.ev_route(2))/2.0 + ev_tant * 50

    def perform_failure(self, state: LibraryState):
        # TODO: wiki says this caps at level 5?
        state.items[Item.Nightmares] += 1
        state.noises += random.choice([1,2])
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        ev_noises = sum([state.ev_noises(i) for i in range(1, 3)]) / 2.0
        return ev_nightmares + ev_noises + state.ev_progress(1)

class MapRoomAction2(Action):
    def __init__(self):
        super().__init__("Look for maps of the Neath")
        # TODO unknown, wild guess
        self.rare_success_rate = 0.1

    def pass_rate(self, state: LibraryState):
        # return 0.79
        return self.broad_success_rate(250, state.outfits.watchful)

    def perform_success(self, state: LibraryState):
        if random.random() < self.rare_success_rate:
            state.items[Item.PuzzlingMap] += 1
        else:
            state.items[Item.PartialMap] += 2


    def success_ev(self, state: LibraryState):
        echo_normal = item_values[Item.PartialMap][Item.Echo] * 2 * (1.0 - self.rare_success_rate)
        echo_rare = item_values[Item.PuzzlingMap][Item.Echo] * self.rare_success_rate

        return (echo_normal + echo_rare) * ev_echo
    
    def perform_failure(self, state: LibraryState):
        state.items[Item.Nightmares] += 1 # TODO caps at 5 per wiki, still true?
        state.progress += 1
        state.noises += 1

    def failure_ev(self, state: LibraryState):
        return ev_nightmares + state.ev_progress(1) + state.ev_noises(1)
        
class MapRoomAction3(Action):
    def __init__(self):
        super().__init__("Get a lead from the Cartographer")

    def can_perform(self, state: LibraryState):
        return state.cartographer_enabled

    def perform_success(self, state: LibraryState):
        state.noises += 2
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_noises(2) + state.ev_progress(5)

class PoisonGallery(LibraryCard):
    def __init__(self):
        super().__init__("A Poison-Gallery")
        self.actions = [PoisonGalleryAction1(), PoisonGalleryAction2()]

class PoisonGalleryAction1(Action):
    def __init__(self):
        super().__init__("Use furniture as stepping stones")

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.broad_success_rate(240, state.outfits.shadowy_plus_neathproofed15)

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.noises += 6
        state.items[Item.Wounds] += 3

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(6) + ev_wounds * 3

class PoisonGalleryAction2(Action):
    def __init__(self):
        super().__init__("Prepare an antidote")

    def pass_rate(self, state: LibraryState):
        # return 0.9
        return self.narrow_success_rate(10, state.outfits.kataleptic_toxicology)

    def perform_success(self, state: LibraryState):
        state.items[Item.FlaskOfAbominableSalts] -= 1
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5) - ev_echo * 0.10

    def perform_failure(self, state: LibraryState):
        state.noises += 1
        state.items[Item.Wounds] += 2
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(1) + ev_wounds * 2 + state.ev_progress(1)

class StoneGallery(LibraryCard):
    def __init__(self):
        super().__init__("A Stone Gallery")
        self.actions = [StoneGalleryAction1(),
                        StoneGalleryAction2(),
                        StoneGalleryAction3()]
                        # StoneGalleryAction4()]
        
class StoneGalleryAction1(Action):
    def __init__(self):
        super().__init__("Make your way through the silent gallery")

    def pass_rate(self, state: LibraryState):
        # Luck
        # TODO: can prepare with menace reduction gear, put in outfit somehow?
        return 0.5

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        nightmare_multiplier = 0.85 ** 3        
        state.items[Item.Nightmares] += 2 * nightmare_multiplier
        state.progress += 5

    def failure_ev(self, state: LibraryState):
        nightmare_multiplier = 0.85 ** 3
        return state.ev_progress(5) + ev_nightmares * 2 * nightmare_multiplier

class StoneGalleryAction2(Action):
    def __init__(self):
        super().__init__("Stop and examine the ancient volumes")

    def pass_rate(self, state: LibraryState):
        # return 0.8
        return self.narrow_success_rate(7, state.outfits.cthonosophy)
    
    def perform_success(self, state: LibraryState):
        frag = random.randint(1,2)
        state.items[Item.FragmentaryOntology] += frag
        state.gross_frags += 2

    def success_ev(self, state: LibraryState):
        return (state.ev_frag(1) + state.ev_frag(2))/2.0

    def perform_failure(self, state: LibraryState):
        state.noises += random.choice([1,2])
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return ev_progress + state.ev_noises(2)

class StoneGalleryAction3(Action):
    def __init__(self):
        super().__init__("Follow a borehole through the back of a bookcase")

    def can_perform(self, state: LibraryState):
        return state.items[Item.RouteTracedThroughTheLibrary] >= 2 and state.hour_in_the_library in (3, 4)

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.broad_success_rate(300, state.outfits.watchful_plus_dangerous)

    def perform_success(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] -= 2
        state.progress += 10

    def success_ev(self, state: LibraryState):
        # ignore/reduce route cost since this is best use?
        return state.ev_progress(10) # + state.ev_route(-2)

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.noises += 6
        state.items[Item.RouteTracedThroughTheLibrary] -= 1

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) + state.ev_route(-1) + state.ev_noises(6)

class Index(LibraryCard):
    def __init__(self):
        super().__init__("An Index")
        self.actions = [IndexAction1(),
                        IndexAction2(),
                        IndexAction3()]
        
    def can_draw(self, state: LibraryState):
        return state.in_search_of_lost_time == 1

class IndexAction1(Action):
    def __init__(self):
        super().__init__("Search for a reference card")

    def pass_rate(self, state: LibraryState):
        # return 1.0
        # lower epa?
        return self.broad_success_rate(200, state.outfits.watchful_plus_inerrant15)

    def ev(self, state: LibraryState):
        return 0
    
    def perform_success(self, state: LibraryState):
        routes = random.choice([1,2,3])
        state.items[Item.RouteTracedThroughTheLibrary] += routes
        state.gross_routes += routes

    def success_ev(self, state: LibraryState):
        average = sum([state.ev_route(i) for i in range(1, 4)]) / 3.0
        return average

    def perform_failure(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] += 1
        state.noises += 2
        state.progress += 1

        state.gross_routes += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(1) + state.ev_route() + state.ev_noises(2)
    
class IndexAction2(Action):
    def __init__(self):
        super().__init__("Try to understand the organization of the library")

    def pass_rate(self, state: LibraryState):
        # return 0.8
        # lower epa?
        return self.narrow_success_rate(7, state.outfits.cthonosophy)

    def perform_success(self, state: LibraryState):
        frags = random.choice([1,2,3])        
        state.items[Item.FragmentaryOntology] += frags
        state.gross_frags += frags

    def ev(self, state: LibraryState):
        return 0        

    def success_ev(self, state: LibraryState):
        return sum(state.ev_frag(i) for i in [1,2,3])/3.0

    def perform_failure(self, state: LibraryState):
        state.items[Item.FragmentaryOntology] += 1
        state.noises += random.choice([1,2])
        state.progress += 1

        state.gross_frags += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(1) + state.ev_route() + state.ev_noises(2)
    
class IndexAction3(Action):
    def __init__(self):
        super().__init__("Situate yourself within the greater whole")

    def ev(self, state: LibraryState):
        return 0

    def can_perform(self, state: LibraryState):
        return state.items[Item.FragmentaryOntology] > 0

    def perform_success(self, state: LibraryState):
        state.items[Item.FragmentaryOntology] -= 1
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5) + state.ev_frag(-1)


class LibrariansOffice(LibraryCard):
    def __init__(self):
        super().__init__("A Librarian's Office", 0.8)
        self.actions = [LibrariansOfficeAction1(),
                        LibrariansOfficeAction2(),
                        LibrariansOfficeAction3()]
        
    def can_draw(self, state: LibraryState):
        return state.in_search_of_lost_time == 2

class LibrariansOfficeAction1(Action):
    def __init__(self):
        super().__init__("Pick through the drawers")

    def pass_rate(self, state: LibraryState):
        return 0.9

    def perform_success(self, state: LibraryState):
        state.items[Item.TantalisingPossibility] += 40
        drawer = random.choice([1,2,3])
        if drawer == 1:
            state.items[Item.LibraryKey] += 1
            state.gross_keys += 1
        if drawer == 2:
            state.items[Item.RouteTracedThroughTheLibrary] += 1
            state.gross_routes += 1
        if drawer == 3:
            state.items[Item.FragmentaryOntology] += 1
            state.gross_frags += 1

    def success_ev(self, state: LibraryState):
        return simple_ev_gain_key
        # return ev_tant * 40 + (state.ev_key() + state.ev_route() + state.ev_frag(1))/3.0

    def perform_failure(self, state: LibraryState):
        drawer = random.choice([4,5])
        if drawer == 4:
            state.items[Item.FinBonesCollected] += random.randint(2,10)
        if drawer == 5:
            state.items[Item.DeepZeeCatch] += random.randint(3,10)

    def failure_ev(self, state: LibraryState):
        return ev_echo * 3
    
class LibrariansOfficeAction2(Action):
    def __init__(self):
        super().__init__("Take the opposite door")

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)
    
class LibrariansOfficeAction3(Action):
    def __init__(self):
        super().__init__("Unlock the cart")

    def can_perform(self, state: LibraryState):
        return state.items[Item.LibraryKey] > 0

    def perform_success(self, state: LibraryState):
        state.items[Item.LibraryKey] -= 1
        state.progress += 15

    def success_ev(self, state: LibraryState):
        return state.ev_progress(15) + state.ev_key(-1)
    

class FloweringGallery(LibraryCard):
    def __init__(self):
        super().__init__("A Flowering Gallery")
        self.actions = [FloweringGalleryAction1(),
                        FloweringGalleryAction2()]
        
    def can_draw(self, state: LibraryState):
        return state.hour_in_the_library in [1,2]

class FloweringGalleryAction1(Action):
    def __init__(self):
        super().__init__("Keep going")

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.narrow_success_rate(0, state.outfits.neathproofed_plus_inerrant)

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        # TODO: wiki doesn't have exact num for nightmares, +2 is a guess
        state.items[Item.Nightmares] += 2
        state.noises += 6

    def failure_ev(self, state: LibraryState):
        return ev_nightmares * 2 + state.ev_noises(6)
    
class FloweringGalleryAction2(Action):
    def __init__(self):
        super().__init__("Eat the fruit of knowledge")

    def pass_rate(self, state: LibraryState):
        # return 0.9
        return self.narrow_success_rate(12, state.outfits.kataleptic_toxicology)

    def perform_success(self, state: LibraryState):
        state.items[Item.FragmentaryOntology] += 2
        state.gross_frags += 2

    def success_ev(self, state: LibraryState):
        return state.ev_frag(2)

    def perform_failure(self, state: LibraryState):
        state.items[Item.Wounds] += 2
        state.noises += 1
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return ev_wounds * 2 + state.ev_noises(2) + state.ev_progress(1)


class BlackGallery(LibraryCard):
    def __init__(self):
        super().__init__("A Black Gallery")
        self.actions = [BlackGalleryAction1(),
                        BlackGalleryAction1Woesel(),
                        BlackGalleryAction2()]
                        # BlackGalleryAction3()]
        
    def can_draw(self, state: LibraryState):
        return state.hour_in_the_library in [3,4,5]

class BlackGalleryAction1(Action):
    def __init__(self):
        super().__init__("Light a lantern")

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.broad_success_rate(240, state.outfits.shadowy_plus_insubstantial15)

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.noises += 2

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) + state.ev_noises(2)
    
class BlackGalleryAction1Woesel(Action):
    def __init__(self):
        super().__init__("(WOESEL) Light a lantern")

    def pass_rate(self, state: LibraryState):
        return 0.0
        # return self.broad_success_rate(240, state.outfits.shadowy_plus_insubstantial15)

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.progress += 5
        state.noises += 2

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) + state.ev_noises(2)    
    
class BlackGalleryAction2(Action):
    def __init__(self):
        super().__init__("Navigate by alternate senses")

    def pass_rate(self, state: LibraryState):
        return 1.0
        # return self.broad_success_rate(
        #     240, state.outfits.watchful_plus_monstrous10_inerrant15)

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

    def perform_failure(self, state: LibraryState):
        state.progress += 1
        state.noises += 2

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(1) + state.ev_noises(2)

class GaolerLibrarian(LibraryCard):
    def __init__(self):
        super().__init__("A Gaoler-Librarian")
        self.actions = [GaolerLibrarianAction1(),
                        GaolerLibrarianAction2(),
                        # GaolerLibrarianAction2SecondChanceRetry(),
                        # GaolerLibrarianAction2SecondChanceBail(),
                        GaolerLibrarianAction3()]

    def can_draw(self, state: LibraryState):
        return state.noises > 0

class GaolerLibrarianAction1(Action):
    def __init__(self):
        super().__init__("Distract the Gaoler")

    def can_perform(self, state: LibraryState):
        return state.noises > 0  # Action only available if there's noise

    def pass_rate(self, state: LibraryState):
        # return 0.96
        return self.broad_success_rate(200, state.outfits.shadowy)

    def perform_success(self, state: LibraryState):
        # Does nothing
        pass

    def success_ev(self, state: LibraryState):
        return 0

    def perform_failure(self, state: LibraryState):
        state.items[Item.Wounds] += 4 # TODO wiki is unsure
        state.noises += 1
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return ev_wounds * 4 + state.ev_noises(1) + state.ev_progress(1)

class GaolerLibrarianAction2(Action):
    def __init__(self):
        super().__init__("Try to lift one of its keys")

    def pass_rate(self, state: LibraryState):
        # return 0.87
        return self.broad_success_rate(250, state.outfits.shadowy_plus_insubstantial15)

    def perform_success(self, state: LibraryState):
        state.items[Item.LibraryKey] += 1
        state.gross_keys += 1

    def ev(self, state: LibraryState):
        # return state.ev_key()
        if state.noises >= 20:
            return 0
        else:
            return simple_ev_gain_key

    def perform_failure(self, state: LibraryState):
        state.noises += 6

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(6)
    
# class GaolerLibrarianAction2SecondChanceRetry(Action):
#     def __init__(self):
#         super().__init__("(SC + RETRY) Try to lift one of its keys")

#     def pass_rate(self, state: LibraryState):
#         rate = self.broad_success_rate(250, state.outfits.shadowy_plus_insubstantial15) 
#         return 1.0 - (1.0 - rate) ** 2

#     def perform_success(self, state: LibraryState):
#         state.items[Item.LibraryKey] += 1
#         state.items[Item.HastilyScrawledWarningNote] -= 1
#         state.gross_keys += 1

#     def ev(self, state: LibraryState):
#         # return state.ev_key()
#         if state.noises >= 30 or state.noises < 20:
#             return 0
#         else:
#             return simple_ev_gain_key        

#     def perform_failure(self, state: LibraryState):
#         state.items[Item.HastilyScrawledWarningNote] -= 1
#         state.noises += 6

# class GaolerLibrarianAction2SecondChanceBail(Action):
#     def __init__(self):
#         super().__init__("(SC + BAIL) Try to lift one of its keys")

#     def pass_rate(self, state: LibraryState):
#         return self.broad_success_rate(250, state.outfits.shadowy_plus_insubstantial15)

#     def perform_success(self, state: LibraryState):
#         state.items[Item.LibraryKey] += 1
#         state.items[Item.HastilyScrawledWarningNote] -= 1
#         state.gross_keys += 1

#     def ev(self, state: LibraryState):
#         # return state.ev_key()
#         if state.noises >= 30 or state.noises < 20:
#             return 0
#         else:
#             return simple_ev_gain_key        
        
#     def perform_failure(self, state: LibraryState):
#         state.items[Item.HastilyScrawledWarningNote] -= 1
#         # state.actions -= 1 # HACK
    
class GaolerLibrarianAction3(Action):
    def __init__(self):
        super().__init__("An intervention from the Grey Cardinal")

    def can_perform(self, state: LibraryState):
        return state.items[Item.DispositionOfTheCardinal] > 0

    def perform_success(self, state: LibraryState):
        state.progress += 5
        state.items[Item.DispositionOfTheCardinal] -= 1

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)
    
class TerribleShushing(LibraryCard):
    def __init__(self):
        super().__init__("A Terrible Shushing")
        self.actions = [TerribleShushingAction1(),
                        TerribleShushingAction2(),
                        TerribleShushingAction3()]

    def can_draw(self, state: LibraryState):
        return state.noises >= 10

class TerribleShushingAction1(Action):
    def __init__(self):
        super().__init__("Find a hiding place")

    def pass_rate(self, state: LibraryState):
        # return 0.87
        return self.broad_success_rate(220, state.outfits.shadowy)

    def perform_success(self, state: LibraryState):
        state.noises -= 3

    def success_ev(self, state: LibraryState):
        return state.ev_noises(-3)

    def perform_failure(self, state: LibraryState):
        state.noises -= 1

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(-1)
    
class TerribleShushingAction2(Action):
    def __init__(self):
        super().__init__("Hurry along")

    def pass_rate(self, state: LibraryState):
        # return 0.65
        return self.broad_success_rate(295, state.outfits.shadowy)

    def perform_success(self, state: LibraryState):
        state.noises += 2
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_noises(2) + state.ev_progress(5)
 
    def perform_failure(self, state: LibraryState):
        state.noises += 4
        state.progress += 5

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(4) + state.ev_progress(5)

# TODO: wiki is unsure about exact range of outcomes
class TerribleShushingAction3(Action):
    def __init__(self):
        super().__init__("Quiet the Cartographer")

    def can_perform(self, state: LibraryState):
        return state.cartographer_enabled

    def perform_success(self, state: LibraryState):
        state.noises = max(0, state.noises - random.randint(3, 10))

    def success_ev(self, state: LibraryState):
        return state.ev_noises(-6)

class GodsEyeView(LibraryCard):
    def __init__(self):
        super().__init__("A God's Eye View")
        self.actions = [GodsEyeViewAction1(), GodsEyeViewAction2()]

    def can_draw(self, state: LibraryState):
        return state.items[Item.FragmentaryOntology] >= 5

class GodsEyeViewAction1(Action):
    def __init__(self):
        super().__init__("Try to hold it all in your mind at once")

    def pass_rate(self, state: LibraryState):
        return 0.4

    def perform_success(self, state: LibraryState):
        state.items[Item.TantalisingPossibility] += 60
        state.items[Item.FragmentaryOntology] = max(0, state.items[Item.FragmentaryOntology] - 6)

    def success_ev(self, state: LibraryState):
        return ev_tant * 60 - state.ev_frag(6)

    def perform_failure(self, state: LibraryState):
        state.items[Item.TantalisingPossibility] += 40
        state.items[Item.Nightmares] += random.randint(2,4)
        state.noises += random.randint(1,2)
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return ev_tant * 40 + ev_nightmares * 3 \
            + state.ev_noises(2) + state.ev_progress(1)

class GodsEyeViewAction2(Action):
    def __init__(self):
        super().__init__("Focus on the path ahead")

    def perform_success(self, state: LibraryState):
        state.progress += 15
        state.items[Item.FragmentaryOntology] -= 5
    
    def success_ev(self, state: LibraryState):
        # Ignore frag cost since this is the best use for them
        return state.ev_progress(15) # + state.ev_frag(-5)

class ShapeOfTheLabyrinth(LibraryCard):
    def __init__(self):
        super().__init__("The Shape of the Labyrinth")
        self.actions = [ShapeOfTheLabyrinthAction1(), ShapeOfTheLabyrinthAction2()]

    # TODO: figure out how good this card is and tweak stateful route ev accordingly
    def can_draw(self, state: LibraryState):
        return state.items[Item.RouteTracedThroughTheLibrary] >= 6 and state.in_search_of_lost_time == 2

class ShapeOfTheLabyrinthAction1(Action):
    def __init__(self):
        super().__init__("Rethink your movements")

    def perform_success(self, state: LibraryState):
        state.hand.clear()
        state.progress += 10
        state.items[Item.RouteTracedThroughTheLibrary] -= random.randint(2,5)

    def success_ev(self, state: LibraryState):
        # reduce route ev penalty since this is 2nd best use for them?
        # route_avg_ev = sum([state.ev_route(-i) for i in range(2, 6)]) / 4.0
        # route_avg_ev *= 0.5
        return state.ev_progress(10) + state.ev_hand_clear() + state.ev_route(-4)

class ShapeOfTheLabyrinthAction2(Action):
    def __init__(self):
        super().__init__("Reject the significance of shape")
        
    def can_perform(self, state: LibraryState):
        return state.items[Item.FragmentaryOntology] > 0

    def pass_rate(self, state: LibraryState):
        # return 0.9
        return self.narrow_success_rate(5, state.outfits.cthonosophy)

    def perform_success(self, state: LibraryState):
        state.items[Item.FragmentaryOntology] -= 1
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5) + state.ev_frag(-1)

    def perform_failure(self, state: LibraryState):
        state.noises += 1
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(1) + state.ev_progress(1)

# TODO: fine tune EVs and item tracking
class GreyCardinal(LibraryCard):
    def __init__(self):
        super().__init__("The Grey Cardinal")
        self.actions = [GreyCardinalAction1(),
                        GreyCardinalAction2(),
                        GreyCardinalAction3()]

class GreyCardinalAction1(Action):
    def __init__(self):
        super().__init__("Offer the cardinal a furry lunch")

    def perform_success(self, state: LibraryState):
        state.items[Item.DispositionOfTheCardinal] += 1
        state.items[Item.RatOnAString] -= 1

        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5) - ev_echo * 0.01

class GreyCardinalAction2(Action):
    def __init__(self):
        super().__init__("Offer the cardinal a tin of something fishy")

    def perform_success(self, state: LibraryState):
        state.items[Item.DispositionOfTheCardinal] += random.randint(1,2)
        state.items[Item.DeepZeeCatch] -= 1
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5) - ev_echo * 0.05

class GreyCardinalAction3(Action):
    def __init__(self):
        super().__init__("Engage the Cardinal in conversation")

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.broad_success_rate(250, state.outfits.persuasive_plus_bizarre10)

    def perform_success(self, state: LibraryState):
        state.items[Item.TantalisingPossibility] += 50
        state.items[Item.DispositionOfTheCardinal] += 1

    def success_ev(self, state: LibraryState):
        return ev_tant * 50

    def perform_failure(self, state: LibraryState):
        state.items[Item.TantalisingPossibility] += 40

    def failure_ev(self, state: LibraryState):
        return ev_tant * 40

class GlimpseThroughAWindow(LibraryCard):
    def __init__(self):
        super().__init__("A Glimpse through a Window", 0.1)
        self.actions = [GlimpseThroughAWindowAction1(), GlimpseThroughAWindowAction2()]

class GlimpseThroughAWindowAction1(Action):
    def __init__(self):
        super().__init__("Stop and look through")

    def can_perform(self, state: LibraryState):
        return state.hour_in_the_library != 4
    
    def perform_success(self, state: LibraryState):
        state.items[Item.TantalisingPossibility] += 50

    def success_ev(self, state: LibraryState):
        return ev_tant * 50

class GlimpseThroughAWindowAction2(Action):
    def __init__(self):
        super().__init__("Move on quickly")

    def perform_success(self, state: LibraryState):
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5)

class TeaRoom(LibraryCard):
    def __init__(self):
        super().__init__("A Tea Room?", 0.8)
        self.actions = [TeaRoomAction1(), TeaRoomAction2(), TeaRoomAction3()]

class TeaRoomAction1(Action):
    def __init__(self):
        super().__init__("Take a moment to regroup")

    def perform_success(self, state: LibraryState):
        # TODO
        pass

    def success_ev(self, state: LibraryState):
        # TODO
        return 0

class TeaRoomAction2(Action):
    def __init__(self):
        super().__init__("Consult your maps of the library")

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.narrow_success_rate(0, state.items[Item.RouteTracedThroughTheLibrary])

    def perform_success(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] -= 1
        state.progress += 10

    def success_ev(self, state: LibraryState):
        return state.ev_progress(10) #+ state.ev_route(-1)

    def perform_failure(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] -= 1
        state.progress += 5

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5) + state.ev_route(-1)

class TeaRoomAction3(Action):
    def __init__(self):
        super().__init__("Try to make sense of what you've seen")

    def can_perform(self, state: LibraryState):
        return state.items[Item.FragmentaryOntology] > 0

    def pass_rate(self, state: LibraryState):
        # return 1.0
        return self.narrow_success_rate(2, state.items[Item.FragmentaryOntology])

    def perform_success(self, state: LibraryState):
        state.items[Item.FragmentaryOntology] -= 1
        state.items[Item.TantalisingPossibility] += 50

    def success_ev(self, state: LibraryState):
        return ev_tant * 50

    def perform_failure(self, state: LibraryState):
        state.items[Item.FragmentaryOntology] += 1
        state.gross_frags += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_frag(1)

# TODO Check rarity on these
class CartographerSnuffbox(LibraryCard):
    def __init__(self):
        super().__init__("Snuffbox.png")
        self.actions = [CartographerSnuffboxAction1(),
                        CartographerSnuffboxAction2()]

    def can_draw(self, state: LibraryState):
        # TODO confirm this requires routes to draw
        return state.cartographer_enabled and state.items[Item.RouteTracedThroughTheLibrary] > 0

class CartographerSnuffboxAction1(Action):
    def __init__(self):
        super().__init__("Computernofigure.png")

    def can_perform(self, state: LibraryState):
        return state.items[Item.RouteTracedThroughTheLibrary] > 0

    def perform_success(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] -= 1
        state.progress += 5

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5) + state.ev_route(-1)

class CartographerSnuffboxAction2(Action):
    def __init__(self):
        super().__init__("Implication.png")

    def can_perform(self, state: LibraryState):
        return state.items[Item.RouteTracedThroughTheLibrary] >= 3

    def perform_success(self, state: LibraryState):
        state.items[Item.RouteTracedThroughTheLibrary] -= 3
        state.items[Item.FragmentaryOntology] += 5
        state.gross_frags += 5

    def success_ev(self, state: LibraryState):
        return state.ev_frag(5) + state.ev_route(-3)

class CartographerCompass(LibraryCard):
    def __init__(self):
        super().__init__("Compass.png")
        self.actions = [CartographerCompassAction1(),
                        CartographerCompassAction2()]
        
    def can_draw(self, state: LibraryState):
        return state.cartographer_enabled     

class CartographerCompassAction1(Action):
    def __init__(self):
        super().__init__("Camera2.png")

    def pass_rate(self, state: LibraryState):
        # TODO need exact DC
        return self.broad_success_rate(220, state.outfits.watchful_plus_inerrant15)

    def perform_success(self, state: LibraryState):
        routes = random.randint(1, 3)
        state.items[Item.RouteTracedThroughTheLibrary] += routes
        state.gross_routes += routes

    def success_ev(self, state: LibraryState):
        return state.ev_route() * 2

    def perform_failure(self, state: LibraryState):
        state.noises += 2
        state.progress += 1

    def failure_ev(self, state: LibraryState):
        return state.ev_noises(2) + state.ev_progress(1)

class CartographerCompassAction2(Action):
    def __init__(self):
        super().__init__("Chart2.png")

    def can_perform(self, state: LibraryState):
        return state.items[Item.RouteTracedThroughTheLibrary] >= 3

    def perform_success(self, state: LibraryState):
        state.progress += random.choice([5, 10, 15])
        state.items[Item.RouteTracedThroughTheLibrary] -= 3

    def success_ev(self, state: LibraryState):
        return (state.ev_progress(5) + state.ev_progress(10) + state.ev_progress(15)) / 3.0

# TODO requires True Denizen
class ChainedOctavo(LibraryCard):
    def __init__(self):
        super().__init__("A Chained Octavo", 0.1)
        self.actions = [ChainedOctavoAction1(),
                        ChainedOctavoAction2()]
    
    def can_draw(self, state: LibraryState):
        return state.anathema_unchained <= 0 and state.in_search_of_lost_time == 1

class ChainedOctavoAction1(Action):
    def __init__(self):
        super().__init__("Unchain it")

    def can_perform(self, state: LibraryState):
        return state.items[Item.LibraryKey] > 1 and state.noises < 28

    def perform_success(self, state: LibraryState):
        state.items[Item.LibraryKey] -= 1
        state.noises += random.randint(5,7)
        
        state.progress = 0
        state.in_search_of_lost_time = 2

        state.anathema_unchained = 10

        # TODO: confirm this advances Hour, vs sets to specific value
        state.hour_in_the_library = (state.hour_in_the_library + 1) % 5

    def success_ev(self, state: LibraryState):
        return 10_000

class ChainedOctavoAction2(Action):
    def __init__(self):
        super().__init__("Examine this section, then move on")

    def pass_rate(self, state: LibraryState):
        # TODO: set a floor so we can always pass this?
        bonus = state.items[Item.FragmentaryOntology]
        return self.narrow_success_rate(10, state.outfits.cthonosophy + bonus)

    def perform_success(self, state: LibraryState):
        state.progress += 5
        state.items[Item.TantalisingPossibility] += 10

    def success_ev(self, state: LibraryState):
        return state.ev_progress(5) + ev_tant * 10

    def perform_failure(self, state: LibraryState):
        state.progress += 5

    def failure_ev(self, state: LibraryState):
        return state.ev_progress(5)

def simulate_runs(num_runs):
    """
    Simulates a large number of runs of the game and prints the results.
    
    Args:
    - num_runs (int): Number of runs to simulate.
    
    Returns:
    - None
    """

    print("=" * 80)
    print(f"{'SIMULATION RESULTS':^80}")
    print("=" * 80)

    state = LibraryState()
    state.apocrypha_sought = ApocryphaSought.SomeFrenchBullshit
    state.cartographer_enabled = False

    # Progress bar setup
    progress_template = "\rProgress: [{:<50}] {:.2f}% ({}/{})"
    print(progress_template.format("", 0, 0, num_runs), end='')

    while state.total_runs() < num_runs:
        state.step()
        # Update progress bar
        progress = (state.total_runs() / num_runs) * 100
        bar_length = int(progress / 2)
        print(progress_template.format("=" * bar_length, progress, state.total_runs(), num_runs), end='')

    print()  # Move to the next line after completing the progress bar

    total_steps = state.actions

    total_runs = state.total_runs()

    print(f"ApocryphaSought: {state.apocrypha_sought}")
    print(f"Cartographer Enabled: {state.cartographer_enabled}")

    # Calculate and print statistics
    print(f"Total runs: {num_runs}")
    print(f"Successes: {total_runs} ({(total_runs / num_runs) * 100:.2f}%)")
    print(f"Failures: {state.failed_runs} ({(state.failed_runs / num_runs) * 100:.2f}%)")
    print(f"Average actions per run: {total_steps / num_runs:.2f}")

    print(f"Keys collected: {state.gross_keys}")
    print(f"Routes collected: {state.gross_routes}")
    print(f"Frag. Ontologies collected: {state.gross_frags}")

    print("\nCard and Action Play Counts:")
    print(f"{'Card':<20} {'Per Run Played/Drawn':<10} {'Action':<40} {'Per Run':<10} {'Success%':<5}")
    print("-" * 95)

    # Sort the deck by the card play counts in descending order
    sorted_deck = sorted(state.deck,
                         key=lambda card: state.card_play_counts[card.name] / max(1, state.card_draw_counts[card.name]),
                         reverse=True)

    for card in sorted_deck:
        card_name = card.name
        truncated_card_name = (card_name[:27] + '...') if len(card_name) > 27 else card_name
        card_play_count = state.card_play_counts[card_name]
        card_draw_count = state.card_draw_counts[card_name]

        card_plays_per_run = card_play_count / total_runs if total_runs > 0 else 0
        card_draws_per_run = card_draw_count / total_runs if total_runs > 0 else 0
        card_plays_per_draw = card_plays_per_run / card_draws_per_run if card_draws_per_run > 0 else 0

        if card_plays_per_run == 0:
            print(f"{truncated_card_name:<30} {card_plays_per_run:<10.0f}")
        else:
            print(f"{truncated_card_name:<30} {card_plays_per_run:.2f}/{card_draws_per_run:<5.2f} ({100 * card_plays_per_draw:.2f}%)")

        for action in card.actions:
            action_name = action.name
            # Truncate action name if it exceeds max length
            truncated_action_name = (action_name[:37] + '...') if len(action_name) > 37 else action_name
            action_success_count = state.action_success_counts[action_name]
            action_failure_count = state.action_failure_counts[action_name]
            total_action_count = action_success_count + action_failure_count

            action_count_per_run = total_action_count / total_runs if total_runs > 0 else 0
            action_success_rate = (action_success_count / total_action_count) if total_action_count > 0 else 0

            if action_count_per_run > 0:
                if action_count_per_run < 0.01:
                    print(f"{'':<30} {'':<10} {truncated_action_name:<39} {'<0.01':<10} {action_success_rate * 100:.1f}%")                
                else:
                    print(f"{'':<30} {'':<10} {truncated_action_name:<40} {action_count_per_run:<10.2f} {action_success_rate * 100:.1f}%")
            # else:
            #     print(f"{'':<30} {'':<10} {truncated_action_name:<40} {action_count_per_run:<10.0f}")


            woesel_name = "(WOESEL) " + action_name
            woesel_count = state.action_woesel_counts[action_name]    
            woesel_count_per_run = woesel_count / total_runs if total_runs > 0 else 0
            if (woesel_count_per_run > 0):
                truncated_woesel_name = (woesel_name[:37] + '...') if len(woesel_name) > 37 else woesel_name
                print(f"{'':<30} {'':<10} {truncated_woesel_name:<40} {woesel_count_per_run:<15.3f}")

        print()

    echoes_only_total = 0
    stuivers_only_total = 0
    all_currency_total = 0

    # Process items for individual totals
    print("-" * 95)
    print(f"{'Item':<30} {'Net/Run':<10} {'Echoes/Action':<22} {'Stuivers/Action':<25}")
    print("-" * 95)

    for item, count in state.items.items():
        value_data = item_values.get(item, {})
        echo_value = value_data.get(Item.Echo, None)
        stuiver_value = value_data.get(Item.Stuiver, None)

        count = int(count)
        count_per_run = count / num_runs
        # Calculate echoes and stuivers per action
        echoes_per_action = (count * echo_value) / total_steps if total_steps > 0 and echo_value is not None else 0
        stuivers_per_action = (count * stuiver_value) / total_steps if total_steps > 0 and stuiver_value is not None else 0

        # Truncate item name if it is too long
        truncated_item_name = (item.name[:27] + '...') if len(item.name) > 27 else item.name

        if echoes_per_action != 0 and stuivers_per_action == 0:
            echoes_only_total += count * echo_value
            all_currency_total += count * echo_value
            print(f"{truncated_item_name:<30} {count_per_run:<10.3f} {echoes_per_action:.4f} {'':<25}")
        elif echoes_per_action == 0 and stuivers_per_action != 0:
            stuivers_only_total += count * stuiver_value
            all_currency_total += count * stuiver_value * 0.05
            print(f"{truncated_item_name:<30} {count_per_run:<10.3f} {'':<22} {stuivers_per_action:.4f}")
        elif echoes_per_action != 0 and stuivers_per_action != 0:
            echoes_only_total += count * echo_value
            stuivers_only_total += count * stuiver_value
            all_currency_total += max(count * echo_value, count * stuiver_value * 0.05)
            print(f"{truncated_item_name:<30} {count_per_run:<10.3f} {echoes_per_action:.4f} {'':<15} {stuivers_per_action:.4f}")

    print("-" * 95)

    echoes_only_per_action = echoes_only_total / total_steps if total_steps > 0 else 0
    print(f"{'Echoes Only Per Action':<30} {'':<10} {echoes_only_per_action:.4f} E{'':<25}")

    stuivers_only_per_action = stuivers_only_total / total_steps if total_steps > 0 else 0
    print(f"{'Stuivers Only Per Action':<30} {'':<10} {'':<22} {stuivers_only_per_action:.4f} S")

    total_per_action = all_currency_total / total_steps if total_steps > 0 else 0
    print(f"{'Echoes/Stuivers Per Action':<30} {'':<10} {total_per_action:.4f} E")

simulate_runs(5_000)
