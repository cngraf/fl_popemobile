from enums import *
import config

# Speculative until exact changes revealed

## ------------
## Rat Market
## ------------
def add_trades(config: config.Config):
    trade = config.trade
    add = config.add

    stage1_multiplier = 1.3
    
    for tier5 in (Item.UncannyIncunabulum,
                  Item.StormThrenody,
                  Item.RattyReliquary,
                  Item.UnlawfulDevice):
        add({
            tier5: -1,
            Item.RatShilling: 162,
            Item.RatMarketExhaustion: 1250
        })

    for tier6 in (Item.NightWhisper,
                  Item.ParabolaLinenScrap,
                #   Item.CracklingDevice,
                  Item.CaptivatingBallad):
        add({
            tier6: -1,
            Item.RatShilling: 812,
            Item.RatMarketExhaustion: 6250
        })

    for tier7 in (Item.CorrespondingSounder,
                  Item.ScrapOfIvoryOrganza,
                  Item.CartographersHoard,
                  Item.ParabolanParable):
        add({
            tier7: -1,
            Item.RatShilling: 4062,
            Item.RatMarketExhaustion: 31250
        })

    # if config.enable_all_rat_market_moons:
    #     for item, price in (
    #         (Item.RayDrenchedCinder, -3125),
    #         (Item.EyelessSkull, -625),
    #         (Item.StarstoneDemark, -3125),
    #         (Item.IntriguersCompendium, -3125),
    #         (Item.ElementalSecret, -3125),
    #         (Item.CoruscatingSoul, -3125),
    #         (Item.EdictsOfTheFirstCity, -3125),
    #         (Item.ReportedLocationOfAOneTimePrinceOfHell, -15625),
    #         # (Item.LegendaCosmogone, -3125),
    #         (Item.TearsOfTheBazaar, -3125),
    #         (Item.FabulousDiamond, -3125),
    #         (Item.NoduleOfFecundAmber, -3125)
    #     ):
    #         trade(0, { item: 1, Item.RatShilling: price})

    trade(0, { Item.RatShilling: -1, Item.PieceOfRostygold: 10 })

    # Crow-Crease Cryptics

    trade(0, {
        Item.RatShilling: -1,
        Item.InklingOfIdentity: 1
    })

    trade(0, {
        Item.RatShilling: -1,
        Item.ManiacsPrayer: 1
    })

    trade(0, {
        Item.RatShilling: -2,
        Item.AppallingSecret: 1
    })

    trade(0, {
        Item.RatShilling: -7,
        Item.CompromisingDocument: 1
    })

    trade(0, {
        Item.RatShilling: -7,
        Item.CorrespondencePlaque: 1
    })

    trade(0, {
        Item.RatShilling: -7,
        Item.JournalOfInfamy: 1
    })

    trade(0, {
        Item.RatShilling: -7,
        Item.TaleOfTerror: 1
    })

    trade(0, {
        Item.RatShilling: -50,
        Item.TouchingLoveStory: 1
    })

    trade(0, {
        Item.RatShilling: -250,
        Item.BlackmailMaterial: 1
    })

    # Extramurine Trading Company

    trade(0, {
        Item.RatShilling: -8,
        Item.RoyalBlueFeather: 1
    })

    trade(0, {
        Item.RatShilling: -8,
        Item.SolaceFruit: 1
    })

    trade(0, {
        Item.RatShilling: -10,
        Item.HandPickedPeppercaps: 1
    })

    trade(0, {
        Item.RatShilling: -10,
        Item.NightsoilOfTheBazaar: 1
    })

    trade(0, {
        Item.RatShilling: -25,
        Item.PreservedSurfaceBlooms: 1
    })

    trade(0, {
        Item.RatShilling: -45,
        Item.CarvedBallOfStygianIvory: 1
    })

    trade(0, {
        Item.RatShilling: -60,
        Item.CrateOfIncorruptibleBiscuits: 1
    })

    # Merru's Gun Exchange

    trade(0, {
        Item.RatShilling: -1,
        Item.AmanitaSherry: 1
    })

    trade(0, {
        Item.RatShilling: -1,
        Item.MapScrap: 1
    })

    trade(0, {
        Item.RatShilling: -1,
        Item.PhosphorescentScarab: 1
    })

    trade(0, {
        Item.RatShilling: -2,
        Item.FlawedDiamond: 1
    })

    trade(0, {
        Item.RatShilling: -7,
        Item.PalimpsestScrap: 1
    })

    # Nightclaw's Paw-Brokers

    trade(0, {
        Item.RatShilling: -2,
        Item.WellPlacedPawn: 1
    })

    # Tier 4

    trade(0, {
        Item.FourthCityEcho: -1,
        Item.RatShilling: 125
    })