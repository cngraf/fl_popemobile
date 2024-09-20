from enums import *
from config import Config 

# Speculative until exact changes revealed

## ------------
## Rat Market
## ------------

def add_ratly_demand_trades(config : Config, saturation1, saturation, item, echo_value):
        config.add({
            item: -1,
            saturation1: echo_value * 100,
            Item.RatShilling: echo_value * 10 * 1.32
        })

        config.add({
            item: -1,
            saturation: echo_value * 100,
            Item.RatShilling: echo_value * 10 * 1.12
        })

        config.add({
            item: -1,
            Item.RatShilling: echo_value * 10
        })

def add_trades(config: Config):
    trade = config.trade
    add = config.add

    add_ratly_demand_trades(config,
        saturation1=Item.SoftRatMarketSaturation1,
        saturation=Item.SoftRatMarketSaturation2,
        item=Item.ParabolaLinenScrap,
        echo_value=62.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.SoftRatMarketSaturation1,
        saturation=Item.SoftRatMarketSaturation2,
        item=Item.ScrapOfIvoryOrganza,
        echo_value=312.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.SaintlyRatMarketSaturation1,
        saturation=Item.SaintlyRatMarketSaturation2,
        item=Item.RattyReliquary,
        echo_value=12.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.SaintlyRatMarketSaturation1,
        saturation=Item.SaintlyRatMarketSaturation2,
        item=Item.FalseHagiotoponym,
        echo_value=62.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.MaudlinRatMarketSaturation1,
        saturation=Item.MaudlinRatMarketSaturation2,
        item=Item.CaptivatingBallad,
        echo_value=62.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.MaudlinRatMarketSaturation1,
        saturation=Item.MaudlinRatMarketSaturation2,
        item=Item.ParabolanParable,
        echo_value=312.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.InscrutableRatMarketSaturation1,
        saturation=Item.InscrutableRatMarketSaturation2,
        item=Item.UncannyIncunabulum,
        echo_value=12.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.InscrutableRatMarketSaturation1,
        saturation=Item.InscrutableRatMarketSaturation2,
        item=Item.CartographersHoard,
        echo_value=312.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.TempestuousRatMarketSaturation1,
        saturation=Item.TempestuousRatMarketSaturation2,
        item=Item.StormThrenody,
        echo_value=12.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.TempestuousRatMarketSaturation1,
        saturation=Item.TempestuousRatMarketSaturation2,
        item=Item.NightWhisper,
        echo_value=62.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.IntricateRatMarketSaturation1,
        saturation=Item.IntricateRatMarketSaturation2,
        item=Item.UnlawfulDevice,
        echo_value=12.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.IntricateRatMarketSaturation1,
        saturation=Item.IntricateRatMarketSaturation2,
        item=Item.CorrespondingSounder,
        echo_value=312.50)
    
    add({
          Item.FourthCityEcho: -1,
          Item.RatShilling: 125
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

    ratty_bazaar_prices = {
        Item.InklingOfIdentity: 1,
        Item.ManiacsPrayer: 1,
        Item.AppallingSecret: 2,
        Item.CompromisingDocument: 7,
        Item.CorrespondencePlaque: 7,
        Item.JournalOfInfamy: 7,
        Item.TaleOfTerror: 7,
        Item.TouchingLoveStory: 50,
        Item.BlackmailMaterial: 250,
        Item.RoyalBlueFeather: 8,
        Item.SolaceFruit: 8,
        Item.HandPickedPeppercaps: 10,
        Item.NightsoilOfTheBazaar: 10,
        Item.PreservedSurfaceBlooms: 25,
        Item.CarvedBallOfStygianIvory: 45,
        Item.CrateOfIncorruptibleBiscuits: 60,
        Item.AmanitaSherry: 1,
        Item.MapScrap: 1,
        Item.PhosphorescentScarab: 1,
        Item.FlawedDiamond: 2,
        Item.PalimpsestScrap: 7,
        # Item.RattusFaberRifle: 50,
        # Item.SkyglassKnife: 63,
        # Item.SetOfKifers: 640,
        # Item.RavenglassKnife: 1000,
        # Item.SetOfIntricateKifers: 3999,
        # Item.RatworkDerringer: 4000,
        Item.WellPlacedPawn: 2,
        # Item.ScarletStockingsOfDubiousOrigin: 4,
        # Item.AntiqueConstablesBadge: 30,
        # Item.CopperCipherRing: 40,
        # Item.RedFeatheredPin: 40,
        # Item.TinyJewelledReliquary: 40,
        # Item.EngravedPewterTankard: 50,
        # Item.OldBoneSkeletonKey: 63,
        # Item.OrnateTypewriter: 60
    }

    for item, price in ratty_bazaar_prices.items():
          add({
                item: 1,
                Item.RatShilling: -1 * price
          })


    # # Crow-Crease Cryptics

    # trade(0, {
    #     Item.RatShilling: -1,
    #     Item.InklingOfIdentity: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -1,
    #     Item.ManiacsPrayer: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -2,
    #     Item.AppallingSecret: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -7,
    #     Item.CompromisingDocument: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -7,
    #     Item.CorrespondencePlaque: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -7,
    #     Item.JournalOfInfamy: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -7,
    #     Item.TaleOfTerror: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -50,
    #     Item.TouchingLoveStory: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -250,
    #     Item.BlackmailMaterial: 1
    # })

    # # Extramurine Trading Company

    # trade(0, {
    #     Item.RatShilling: -8,
    #     Item.RoyalBlueFeather: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -8,
    #     Item.SolaceFruit: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -10,
    #     Item.HandPickedPeppercaps: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -10,
    #     Item.NightsoilOfTheBazaar: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -25,
    #     Item.PreservedSurfaceBlooms: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -45,
    #     Item.CarvedBallOfStygianIvory: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -60,
    #     Item.CrateOfIncorruptibleBiscuits: 1
    # })

    # # Merru's Gun Exchange

    # trade(0, {
    #     Item.RatShilling: -1,
    #     Item.AmanitaSherry: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -1,
    #     Item.MapScrap: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -1,
    #     Item.PhosphorescentScarab: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -2,
    #     Item.FlawedDiamond: 1
    # })

    # trade(0, {
    #     Item.RatShilling: -7,
    #     Item.PalimpsestScrap: 1
    # })

    # # Nightclaw's Paw-Brokers

    # trade(0, {
    #     Item.RatShilling: -2,
    #     Item.WellPlacedPawn: 1
    # })

    # # Tier 4

    # trade(0, {
    #     Item.FourthCityEcho: -1,
    #     Item.RatShilling: 125
    # })