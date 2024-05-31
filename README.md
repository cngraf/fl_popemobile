
# PROJECT: POPEMOBILE

31 May 24: Everything is in flux until we figure out exactly how the New Rat Market works.

Reliable 5+ EPA grinds in the meantime:

### Commune with TLC

5.68 EPA

1. Commune with City or Creditor.
1. Sell the item you get.

* Requires 15 in three advanced stats and completed railway

### TLC Deck

~5.2 EPA

1. Draw cards in Hinterland City.
2. Play cards for Prosperity
3. Exchange Prosperity for items

* Requires completed railway

### 3. Hearts' Game

5.2+ EPA

1. Play Hearts' Game
2. Trade Exploits for `Leviathan Frame`
3. Hunt and dissect Pinewood Sharks for `Fin Bones, Collected`
4. Sell Fish skeletons during Fish weeks

* Default recipe is 1 Bright Brass Skull and 2 Fin Bones Collected.
    * BaL players can get better payouts using the duplicated Vake skull with any Menace-scaling buyer
* Swap in 1 or 2 Amber-Crusted Fins to access Amalgamy buyers
    * obtained by up-converting fin bones at Helicon House

## How to Run
1. download
2. navigate to the directory
3. run `python3 optimize.py`
4. ask your preferred LLM to explain everything

## TODO

* Rework how London deck is modeled (IN PROGRESS)
    * Create dummy items for each card
    * Trade one generic action for like, a collection of card actions
    * Look I have a model in my head, it's hard to explain
    * Do the same thing for Hinterland deck

* Move to a per-week framing (IN PROGRESS)
    * New Rat Market
    * Bone Market Exhaustion
        * sanity check this later. model currently recommends some 6, 12 exhaustion recipes. not obviously wrong, but it doesn't know that you can't use 0-exhaustion recipes while at 4+. will probably end up just hard-coding a limit of 4 or 7
    * Other stuff on a weekly cycle

* Khanate (DONE)
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