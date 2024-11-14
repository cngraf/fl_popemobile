from enums import *
from config import Config 

# Speculative until exact changes revealed

## ------------
## Rat Market
## ------------

def add_ratly_demand_trades(config : Config, saturation1, saturation2, item, echo_value):
        config.add({
            item: -1,
            saturation1: echo_value * 100,
            Item._GeneralRatMarketSaturation1: echo_value * 100,
            Item.RatShilling: echo_value * 10 * 1.32
        })

        config.add({
            item: -1,
            saturation2: echo_value * 100,
            Item._GeneralRatMarketSaturation2: echo_value * 100,
            Item.RatShilling: echo_value * 10 * 1.12
        })

        config.add({
            item: -1,
            Item.RatShilling: echo_value * 10
        })

def add_trades(config: Config):
    add = config.add

    # Rough approximation
    demands_per_week = 2
    total_demand_types = 8
    demand_frequency = demands_per_week / total_demand_types

    add({
        Item._RatMarketRotation: -1,

        Item._GeneralRatMarketSaturation1: -65_000,

        # 0 to 65k
        Item.SoftRatMarketSaturation1: -65_000 * demand_frequency,
        Item.SaintlyRatMarketSaturation1: -65_000 * demand_frequency,
        Item.MaudlinRatMarketSaturation1: -65_000 * demand_frequency,
        Item.InscrutableRatMarketSaturation1: -65_000 * demand_frequency,
        Item.TempestuousRatMarketSaturation1: -65_000 * demand_frequency,
        Item.IntricateRatMarketSaturation1: -65_000 * demand_frequency,
        Item.CalculatingRatMarketSaturation1: -65_000 * demand_frequency,
        Item.RuinousRatMarketSaturation1: -65_000 * demand_frequency,

        Item._GeneralRatMarketSaturation2: -115_000,

        # 65k to 180k
        Item.SoftRatMarketSaturation2: -115_000 * demand_frequency,
        Item.SaintlyRatMarketSaturation2: -115_000 * demand_frequency,
        Item.MaudlinRatMarketSaturation2: -115_000 * demand_frequency,
        Item.InscrutableRatMarketSaturation2: -115_000 * demand_frequency,
        Item.TempestuousRatMarketSaturation2: -115_000 * demand_frequency,
        Item.IntricateRatMarketSaturation2: -115_000 * demand_frequency,       
        Item.CalculatingRatMarketSaturation2: -115_000 * demand_frequency,       
        Item.RuinousRatMarketSaturation2: -115_000 * demand_frequency,       
    })

    # Release valves for bounded qualities
    add({
        Item._GeneralRatMarketSaturation1: 1000
    })

    add({
        Item._GeneralRatMarketSaturation2: 1000
    })

    for type in RAT_MARKET_SATURATION_1_TYPES:
        add({
            type: 1_000,
        })

    for type in RAT_MARKET_SATURATION_2_TYPES:
        add({
            type: 1_000,
        })

    add_ratly_demand_trades(config,
        saturation1=Item.SoftRatMarketSaturation1,
        saturation2=Item.SoftRatMarketSaturation2,
        item=Item.ParabolaLinenScrap,
        echo_value=62.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.SoftRatMarketSaturation1,
        saturation2=Item.SoftRatMarketSaturation2,
        item=Item.ScrapOfIvoryOrganza,
        echo_value=312.50)
    

    add_ratly_demand_trades(config,
        saturation1=Item.SaintlyRatMarketSaturation1,
        saturation2=Item.SaintlyRatMarketSaturation2,
        item=Item.RattyReliquary,
        echo_value=12.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.SaintlyRatMarketSaturation1,
        saturation2=Item.SaintlyRatMarketSaturation2,
        item=Item.FalseHagiotoponym,
        echo_value=62.50)
    

    add_ratly_demand_trades(config,
        saturation1=Item.MaudlinRatMarketSaturation1,
        saturation2=Item.MaudlinRatMarketSaturation2,
        item=Item.CaptivatingBallad,
        echo_value=62.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.MaudlinRatMarketSaturation1,
        saturation2=Item.MaudlinRatMarketSaturation2,
        item=Item.ParabolanParable,
        echo_value=312.50)
    

    add_ratly_demand_trades(config,
        saturation1=Item.InscrutableRatMarketSaturation1,
        saturation2=Item.InscrutableRatMarketSaturation2,
        item=Item.UncannyIncunabulum,
        echo_value=12.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.InscrutableRatMarketSaturation1,
        saturation2=Item.InscrutableRatMarketSaturation2,
        item=Item.ChimericalArchive,
        echo_value=62.50)    
    
    add_ratly_demand_trades(config,
        saturation1=Item.InscrutableRatMarketSaturation1,
        saturation2=Item.InscrutableRatMarketSaturation2,
        item=Item.CartographersHoard,
        echo_value=312.50)
    

    add_ratly_demand_trades(config,
        saturation1=Item.TempestuousRatMarketSaturation1,
        saturation2=Item.TempestuousRatMarketSaturation2,
        item=Item.StormThrenody,
        echo_value=12.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.TempestuousRatMarketSaturation1,
        saturation2=Item.TempestuousRatMarketSaturation2,
        item=Item.NightWhisper,
        echo_value=62.50)
    

    add_ratly_demand_trades(config,
        saturation1=Item.IntricateRatMarketSaturation1,
        saturation2=Item.IntricateRatMarketSaturation2,
        item=Item.UnlawfulDevice,
        echo_value=12.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.IntricateRatMarketSaturation1,
        saturation2=Item.IntricateRatMarketSaturation2,
        item=Item.CracklingDevice,
        echo_value=62.50)

    add_ratly_demand_trades(config,
        saturation1=Item.IntricateRatMarketSaturation1,
        saturation2=Item.IntricateRatMarketSaturation2,
        item=Item.CorrespondingSounder,
        echo_value=312.50)
    
    # TODO exact numbers
    # New trades coming weekend of 30 Sep 24
    add_ratly_demand_trades(config,
        saturation1=Item.CalculatingRatMarketSaturation1,
        saturation2=Item.CalculatingRatMarketSaturation2,
        item=Item.VitalIntelligence,
        echo_value=12.50)
    
    add_ratly_demand_trades(config,
        saturation1=Item.CalculatingRatMarketSaturation1,
        saturation2=Item.CalculatingRatMarketSaturation2,
        item=Item.CorrespondingSounder,
        echo_value=312.50)
    
    paired_mate_echo_value = 50
    config.add({
        Item.QueenMate: -1,
        Item.EpauletteMate: -1,
        Item._GeneralRatMarketSaturation1: paired_mate_echo_value * 100,
        Item.CalculatingRatMarketSaturation1: paired_mate_echo_value * 100,
        Item.RatShilling: paired_mate_echo_value * 10 * 1.32
    })

    config.add({
        Item.QueenMate: -1,
        Item.EpauletteMate: -1,
        Item._GeneralRatMarketSaturation2: paired_mate_echo_value * 100,
        Item.CalculatingRatMarketSaturation2: paired_mate_echo_value * 100,
        Item.RatShilling: paired_mate_echo_value * 10 * 1.12
    })
    
    config.add({
        Item.QueenMate: -1,
        Item.EpauletteMate: -1,
        Item.RatShilling: paired_mate_echo_value * 10
    })    

    # HACK
    # add({
    #       Item.Action: -4,
    #       Item.LegalDocument: -5,
    #       Item.ComprehensiveBribe: -6, 
    #       Item.BazaarPermit: -6, 
    #       Item.BlackmailMaterial: -6,
    #       Item.ParabolanOrangeApple: -1,
    #       Item.DistillationOfRetribution: 1
    # })

    add_ratly_demand_trades(config,
        saturation1=Item.RuinousRatMarketSaturation1,
        saturation2=Item.RuinousRatMarketSaturation2,
        item=Item.DistillationOfRetribution,
        echo_value=312.50)

    add_ratly_demand_trades(config,
        saturation1=Item.RuinousRatMarketSaturation1,
        saturation2=Item.RuinousRatMarketSaturation2,
        item=Item.MortificationOfAGreatPower,
        echo_value=62.50)

    add_ratly_demand_trades(config,
        saturation1=Item.RuinousRatMarketSaturation1,
        saturation2=Item.RuinousRatMarketSaturation2,
        item=Item.DreadfulSurmise,
        echo_value=312.50)

    

    # Always available
    
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
    add({ Item.RatShilling: -1, Item.PieceOfRostygold: 10 })

    add({
        # Ranges per wiki
        Item._RatNoLonger: -1,
        Item.RatShilling: -371.4,

        Item.FourthCityEcho: 1.5,
        Item.FirstCityCoin: 2,
        Item.JustificandeCoin: 1,
        Item.HinterlandScrip: 10,
        Item.FistfulOfSurfaceCurrency: 163,
        Item.AssortmentOfKhaganianCoinage: 11
    })


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