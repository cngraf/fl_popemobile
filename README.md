
# PROJECT: POPEMOBILE

## TL;DR Best Grind

Everything is in flux until we learn how the new rat market works. 5 EPA is the new 6 EPA.

As of 21 May 24:

### 1. Commune with TLC, aka The New Benchmark

5.68 EPA

1. Commune with City or Creditor.
1. Sell the item you get.

PRO
* Extremely simple
* No randomness, no special items or qualities

CON
* Requires 15 in three advanced stats and completed railway


### 2. TLC Deck

~5.2 EPA

1. Draw cards in Hinterland City.
2. Play cards for Prosperity
3. Exchange Prosperity for items

PRO
* Pretty simple
* Flexible payouts
* Requires completed railway


### 3. Hearts' Game

5.2+ EPA

1. Farm Hearts' Game for Leviathan Frames
3. Sell Fish skeletons during Fish weeks

PRO
* Accessible with unfinished railway
* Clears 5.4 EPA with all the bells and whistles
* Minimal stat barriers

CON
* Requires several interlocking carousels to supply ideal bone market recipes
* Takes weeks or months to realize gains


### 4. Advanced Grinds

5.7+ EPA?

WIP

PRO
* more fun
* more profitable

CON
* require specific ambitions, professions, items, FATE-locked locations, etc.

## How to Run
1. download
2. navigate to the directory
3. run `python3 optimize.py`

## TODO

* Rework how London deck is modeled
    * Create dummy items for each card
    * Trade one generic action for like, a collection of card actions
    * Look I have a model in my head, it's hard to explain
    * Do the same thing for Hinterland deck

* Move to a per-week framing
    * New Rat Market
    * Bone Market Exhaustion
    * Other stuff on a weekly cycle

* Khanate
    * Intrigues
    * Smuggling
    * Widow crates

* Parabola
    * Better model of Parabolan War
    * More/better model of hunts, heists

* Unterzee
    * Most of the islands
    * Zailing deck

* Hinterlands
    * Clay Highwayman's Camp
    * Jericho Library
    * Clean up Helicon House
    * Evenlode diving
    * Evenlode barristering
    * Cabinet Noir deciphering
    * Hurlers stuff
    * Marigold stuff?
    * all the location decks

* General
    * Railway statues
    * TLC params
    * Expand professional activities
    * Other mutually exclusive items & qualities

* Figure out a way to model the unlimited draw decks with plain matrixes, aka one that doesn't require a monte carlo simulation

* Lots more things

## FAQ
### Q: Is this README up-to-date with the actual code?

A: almost certainly not

### Q: How do I change the optimization target?

A: set `optimize_for` in `optimize.py`

### Q: How do I tweak this other parameter?

A: it's probably in there somewhere

### Q: Why did you...

A: it seemed like a good idea at the time

### Q: The way you did this thing looks weird.

A: yes

### Q: I read all your code and it more or less makes sense

A: DM me, let's be friends