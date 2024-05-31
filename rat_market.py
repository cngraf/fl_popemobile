from enums import *
import config

# Speculative until exact changes revealed

## ------------
## Rat Market
## ------------
def add_trades(config: config.Config):
    trade = config.trade
    add = config.add

    stage1_multiplier = 1.3 * 10
    stage2_multiplier = 1.2 * 10 # approx
    stage3_multiplier = 1.1 * 10

    # # TODO: Guessing at the groupings
    # add({
    #     Item.RatMarketExhaustion: 12,
    #     Item.RatMarketWeek1Exhaustion: -1,
    #     Item.RatMarketWeek2Exhaustion: -1,
    #     Item.RatMarketWeek3Exhaustion: -1,
    #     Item.RatMarketWeek4Exhaustion: -1,
    #     Item.RatMarketWeek5Exhaustion: -1,
    #     Item.RatMarketWeek6Exhaustion: -1,
    #     Item.RatMarketWeek7Exhaustion: -1,
    #     Item.RatMarketWeek8Exhaustion: -1,
    #     Item.RatMarketWeek9Exhaustion: -1,
    #     Item.RatMarketWeek10Exhaustion: -1,
    #     Item.RatMarketWeek11Exhaustion: -1,
    #     Item.RatMarketWeek12Exhaustion: -1,
    # })

    for exhaustionStage1, exhaustionStage2, exhaustionStage3, tier5, tier6, tier7 in (
        (Item.RatMarketWeek1ExhaustionStage1,
         Item.RatMarketWeek1ExhaustionStage2,
         Item.RatMarketWeek1ExhaustionStage3,
         Item.UncannyIncunabulum, Item.NightWhisper, Item.CorrespondingSounder),

        (Item.RatMarketWeek2ExhaustionStage1,
         Item.RatMarketWeek2ExhaustionStage2,
         Item.RatMarketWeek2ExhaustionStage3,
         Item.StormThrenody, Item.NightWhisper, Item.CorrespondingSounder),

        (Item.RatMarketWeek3ExhaustionStage1,
         Item.RatMarketWeek3ExhaustionStage2,
         Item.RatMarketWeek3ExhaustionStage3,         
         Item.StormThrenody, Item.ParabolaLinenScrap, Item.CorrespondingSounder),

        (Item.RatMarketWeek4ExhaustionStage1,
         Item.RatMarketWeek4ExhaustionStage2,
         Item.RatMarketWeek4ExhaustionStage3,         
         Item.StormThrenody, Item.ParabolaLinenScrap, Item.ScrapOfIvoryOrganza),

        (Item.RatMarketWeek5ExhaustionStage1,
         Item.RatMarketWeek5ExhaustionStage2,
         Item.RatMarketWeek5ExhaustionStage3,         
         Item.RattyReliquary, Item.ParabolaLinenScrap, Item.ScrapOfIvoryOrganza),

        (Item.RatMarketWeek6ExhaustionStage1,
         Item.RatMarketWeek6ExhaustionStage2,
         Item.RatMarketWeek6ExhaustionStage3,         
         Item.RattyReliquary, None, Item.ScrapOfIvoryOrganza),

        (Item.RatMarketWeek7ExhaustionStage1,
         Item.RatMarketWeek7ExhaustionStage2,
         Item.RatMarketWeek7ExhaustionStage3,         
         Item.RattyReliquary, None, Item.CartographersHoard),

        (Item.RatMarketWeek8ExhaustionStage1,
         Item.RatMarketWeek8ExhaustionStage2,
         Item.RatMarketWeek8ExhaustionStage3,         
         Item.UnlawfulDevice, None, Item.CartographersHoard),

        (Item.RatMarketWeek9ExhaustionStage1,
         Item.RatMarketWeek9ExhaustionStage2,
         Item.RatMarketWeek9ExhaustionStage3,         
         Item.UnlawfulDevice, Item.CaptivatingBallad, Item.CartographersHoard),

        (Item.RatMarketWeek10ExhaustionStage1,
         Item.RatMarketWeek10ExhaustionStage2,
         Item.RatMarketWeek10ExhaustionStage3,         
         Item.UnlawfulDevice, Item.CaptivatingBallad, Item.ParabolanParable),

        (Item.RatMarketWeek11ExhaustionStage1,
         Item.RatMarketWeek11ExhaustionStage2,
         Item.RatMarketWeek11ExhaustionStage3,         
         Item.UncannyIncunabulum, Item.CaptivatingBallad, Item.ParabolanParable),

        (Item.RatMarketWeek12ExhaustionStage1,
         Item.RatMarketWeek12ExhaustionStage2,
         Item.RatMarketWeek12ExhaustionStage3,         
         Item.UncannyIncunabulum, Item.NightWhisper, Item.ParabolanParable),
    ):
        for exhaustion, multiplier in (
            (exhaustionStage1, stage1_multiplier),
            (exhaustionStage2, stage2_multiplier),
            (exhaustionStage3, stage3_multiplier)
        ):
            add({
                tier5: -1,
                Item.RatShilling: 12.5 * multiplier,
                exhaustion: 1250
            })

            if tier6:
                add({
                    tier6: -1,
                    Item.RatShilling: 62.5 * multiplier,
                    exhaustion: 6250
                })

            add({
                tier7: -1,
                Item.RatShilling: 312 * multiplier,
                exhaustion: 31250
            })

    for tier5 in (Item.UncannyIncunabulum,
                  Item.StormThrenody,
                  Item.RattyReliquary,
                  Item.UnlawfulDevice):
        add({
            tier5: -1,
            Item.RatShilling: 125,
        })

    for tier6 in (Item.NightWhisper,
                  Item.ParabolaLinenScrap,
                #   Item.CracklingDevice,
                  Item.CaptivatingBallad):
        add({
            tier6: -1,
            Item.RatShilling: 625,
        })

    for tier7 in (Item.CorrespondingSounder,
                  Item.ScrapOfIvoryOrganza,
                  Item.CartographersHoard,
                  Item.ParabolanParable):
        add({
            tier7: -1,
            Item.RatShilling: 3125,
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

    # TODO: new auto-exchange is more complicated & random
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