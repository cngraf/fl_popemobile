dumping this here from player.py

Defining the baseline endgame player
- excludes boons and moods
- excludes Ambition stuff
    - Treasure
    - ambition-exclusive items
- excludes SMEN & Retired items (irrelevant anyway?)
- excludes item slots that can't be easily swapped
    - Destiny
        - also excludes Mark of Acceptance
        - but allows Memory of Much Greater Self?
    - Ship
    - Spouse
    - Club
    - Profession item

- double check these, just count programmatically
- numbers for "soft F2P"?
    - allow exceptional story, memory of a tale stuff
    - allow Ubergoat, other 1 FATE items

with FATE & Seasonal:
Watchful:   +92 => 322
Shadowy:    +73 => 303
Dangerous:  +83 => 313
Persuasive: +85 => 315

KT:     +10
MA:     +10
APoC:   +10
GW:     +11
SA:     +10
AotRS:  +10
Mith:   +10
SotD:   +1
Zee:    +10

without FATE and Seasonal:
Watchful:   +76
Shadowy:    +65
Dangerous:  +72
Persuasive: +71

KT:     +6
MA:     +4
APoC:   +3
GW:     +5
SA:     +2
AotRS:  +2
Mith:   +3
SotD:   +1
Zee:    +5

so to really get into the nitty gritty, are we gonna need some concept of outfits?
thinking of scandal multiplier

List of Mutually-Exclusive Item & Quality Groups (WIP)
- Treasures
- Destinies + Mark of Acceptance
- Tools of the Trade
- Ships
- Spouses
- Clubs
- Airships
- Tattoos

- Ambition-specific items
- notable branching choices WITHIN Ambitions
    - LF: Lyon Pursuivant vs. Tatterskin Shawl
    - Nem: Dream-Shadow vs. Dream-Shard
    - BAL: trapping 3CV in parabola vs. not
    - HD: none?
- rewards of ambition

- Unburdened Imp & Deviless variants
    - Imp is the only BiS option
- Salon & Orphanage
- Sacksmas Quest Rewards
    - not exclusive but takes several years to complete

- Lab staffing

- Khaganian Network configuration
    - Ties
    - Methods
    - was there a third thing?

- GHR board members
- GHR statues
- GHR station darkness 
- TLC stuff
    - Location
    - Founding Body
    - Currency
    - Leader
    - Political Alignment
- "Closest To" faction

- numerous ES branching choices
    - trade in souls
    - aunt


```
def min_endgame_f2p_bonuses():
    # Excludes
    # - anything FATE-locked
    # - Mr Chimes' Lost & Found
    # - hellworm
    # - ubergoat 
    # - annual seasonal items
    # - ambitions
    # - professions
    # - any slots with swap costs (ship, spouse, destiny, etc.)
    # - any items from a mutually exclusive set (eg. salon/orphanage, unburdened imp)
    # - mark of acceptance
    # - boons & moods
    # - SMEN
    # - retired items
    # - ubergoat (borderline?)
    # - anything in-game but not currently obtainable

    # Includes
    # - faction renown items
    # - Sacroboscan calendar items
    # - Evolution
    # - Railway & TLC
    # - Firmanent
    # - non-seasonal HG items
    return {
        Item.Watchful: 8 + 11 + 8 + 8 + 10 + 7 + 10 + 5 + 7, # 74
        Item.Shadowy: 6 + 6 + 7 + 10 + 10 + 10 + 6 + 10 + 5 + 8, # 78
        Item.Dangerous:  6 + 8 + 5 + 8 + 12 + 8 + 10 + 4 + 8 + 4, # 73
        Item.Persuasive: 10 + 10 + 8 + 5 + 10 + 5 + 10 + 2 + 8 + 8, # 76

        Item.Bizarre: 1 + 2 + 2 + 2 + 1 + 1 + 1 + 2 + 1 + 2 + 2, # 17
        Item.Dreaded: 2 + 2 + 1 + 1 + 1 + 1 + 1 + 4 + 2 + 2, # 17
        Item.Respectable: 1 + 1 + 2 + 1 + 1 + 1 + 1 + 4 + 2 + 2, # 16

        # Labcoat or Shell, Work Gloves, Butcher's Tool, Perfumer's Arts
        Item.KatalepticToxicology: 4,

        # Illuminating Cap, Shell or Ribcage, Naturalist's Map
        Item.MonstrousAnatomy: 3,

        # Director's Overcoat, Infiltrator's Footsteps, FFG's Address Book
        Item.APlayerOfChess: 3,

        # Parabola Suit or Viric Frock, VC's Collar, Honey-Mazed Bear, OP Stave (+2)
        Item.Glasswork: 5,

        # Tunip, Amber Vision
        Item.ShapelingArts: 2,

        # Misplaced Ring, Flower from Hell, Lowell's Locks and Cages
        Item.ArtisanOfTheRedScience: 3,

        # Viscount's Collar, Stalking Shadow, Memory of Much Greater Self
        Item.Mithridacy: 3,

        # imp is from an exclusive set
        Item.StewardOfTheDiscordance: 0,

        # Captain's or Admiral's Hat, Mostly-Cooperative Chart, Blue Prophet,
        # HMS Ramilies, Amber Vision
        Item.Zeefaring: 5,

        # earring not obtainable
        Item.Chthonosophy: 0,

        # Glim Earring, Carpetbag, Cinnabar Compass
        Item.Inerrant: 3,

        # Carryall or Suitcase, Nod from Mr Hearts
        Item.Insubstantial: 2,

        # Illuminating Cap or Hymn, Ratskin Suit, Devil's Dictionary, Ratskin Boots,
        # Indestructible Trunk
        Item.Neathproofed: 5,
    }

def advanced_endgame_f2p_bonuses():
    # Includes
    # - everything in min set
    # - seasonal non-FATE items
    # - ubergoat
    # - unburdened imp

    return {
        Item.Watchful: 8 + 11 + 8 + 8 + 10 + 7 + 20 + 5 + 3 + 8,
        Item.Shadowy: 8 + 6 + 7 + 10 + 10 + 10 + 6 + 10 + 5 + 4 + 8,
        Item.Dangerous:  8 + 8 + 5 + 8 + 12 + 8 + 10 + 4 + 4 + 8 + 4,
        Item.Persuasive: 10 + 10 + 8 + 8 + 10 + 5 + 10 + 5 + 8 + 8,
        # done

        Item.Bizarre: 4 + 2 + 2 + 2 + 3 + 1 + 1 + 3 + 4 + 3 + 2,
        Item.Dreaded: 4 + 2 + 1 + 2 + 2 + 1 + 1 + 3 + 4 + 2 + 2,
        Item.Respectable: 4 + 4 + 2 + 2 + 2 + 1 + 1 + 3 + 4 + 2 + 2,

        # Hat, Clothes, Gloves, Weapon, Boots, Companion, Affil, Transport, HC
        Item.KatalepticToxicology: 9,

        # Hat, Clothes, Gloves, Wep, Boots, Comp, Transport, HC
        Item.MonstrousAnatomy: 8,

        # Hat, Clothes, Gloves, Wep, Boots, Luggage, Comp, Affil, Trans
        Item.APlayerOfChess: 9,

        # Hat, Clothes, Adorn, Gloves, Wep, Boots, Comp+2, HC+2
        Item.Glasswork: 10,

        # Hat, Wep, Booys, Comp, Affil, HC
        Item.ShapelingArts: 6,

        # Hat, Clo, Adorn, Gloves, Wep, Boots, Comp+2, Affil, Trans, HC
        Item.ArtisanOfTheRedScience: 11,

        # Hat, Adorn, Wep, Boots, Comp, Affil, Trans, HC
        Item.Mithridacy: 8,

        # Companion
        Item.StewardOfTheDiscordance: 1,

        # Hat, Clo, Gloves, Wep, Boots, Comp, Affil, Trans, HC
        Item.Zeefaring: 9,

        # Companion
        Item.Chthonosophy: 1,

        # Weapon, Luggage, HC
        Item.Inerrant: 3,

        # Luggage, Affil
        Item.Insubstantial: 2,

        # Hat, Clo+2, Gloves, Wep, Boots, Lugg, Comp
        Item.Neathproofed: 8,
    }
```