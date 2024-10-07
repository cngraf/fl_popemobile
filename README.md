
# PROJECT: POPEMOBILE

## What the heck is this?

A **toolbox** for **answering questions** about the browser-based interactive narrative game **Fallen London**.

Questions such as:

- What is the fastest way to accumulate `Item X`?
- Is `Activity X` more profitable than `Activity Y`?
- What is the expected value of `Carousel X`?


## How to Use

I have vague plans to spin this up into a web app.

Until then, just ping me (or ask ChatGPT) for a guided set-up.

- `main.py` main linear optimization model, to optimize eg. Echoes per Action
    - `player.py` preconfigured player profiles
    - `config.py` constraints, important for menaces and other negative EV qualities
    - `optimization/params.py` optimizer settings, inputs and targets

- `simulations` directory for various monte carlo scripts

### TODO

* Add a license

* Non-action-based items conversion
    * eg. "what's the best way to convert Echoes into Scrip?"
    * model already supports this in theory
    * but I need to figure out a workflow for doing it on the fly

* London Opportunity Deck
    * Figure out WTF to do with this
    * Option 1: Monte Carlo
        * this is what I did with the Upper River deck, and I am happy with the results
            * implement every (economically relevant) card and action in a Monte Carlo sim
            * pick a few representative player profiles as the input parameters
                * eg. the bare minimum F2P, the full BiS whale, and one or two intermediates
            * run the sim for each profile
            * implement the results as single trades
        * challenges:
            * the UR has about 40 cards. London has about 1000.
            * a bunch of cards lead into their own carousels, eg. Arbor
            * red cards with unknown rarities
            * hundreds of bespoke qualities controlling lock/lock, impractical to pick anything that could be called "representative
    * Option 2: Monte Carlo, but only for ultra-thin deck
        * same as above, but remove all the clearly undesirable cards that can be removed
        * much more manageable
    * Option 3: whatever I'm doing right now, where each card has an `Item` exchange, an each `Item._CardDraw` can be trades for a fractional draw of every other card 
        * kind of works?
        * more flexible, in theory
        * harder to translate to human-readable format
            * more "accurate" but less useful?

* London miscellaneous
    * Forgotten Quarter
    * Chimes carousels
    * various other early- and mid-game activities

* Laboratory
    * add more workers and experiments to simulation

* Parabola
    * Refine Parabolan War trades
    * Hunts
    * Oneiropomping

* Unterzee
    * Godfall
    * Polythreme
    * various other rarely-visited locations

* Hinterlands
    * Evenlode
        - diving
        - barristering
    * Balmoral
        * Clay Highwayman's Camp
        - deciphering
        - clean up Cover Identity model
    * Station VIII
        - revisit the Kitchen
        - revisit Alchemy
    * Moulin
        - add full simulation of Expeditions
        - Monographs, ok for now?
    * Hurlers
        - adulterine castle
        - goat ball
        - digging
        - other discordance stuff
    * Marigold
        - anything besides the knights thing?

* TLC

* Lots more things

### Out of Scope

* Heart's Game strategy

## Other FAQs
### Q: Is this README up-to-date with the actual code?

A: almost certainly not

### Q: How do I change the optimization target?

A: change the value in `optimization/params.py`

### Q: How do I tweak this other parameter?

A: it's probably in there somewhere

### Q: Why did you...

A: it seemed like a good idea at the time

### Q: The way you did this thing looks weird.

A: yes

### Q: I read all your code and it more or less makes sense

A: DM me, let's be friends