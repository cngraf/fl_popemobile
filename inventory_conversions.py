from enums import *
import optimization.params as params
from helper.utils import *

def add_trades(config, default_rare_success_rate = 0.05):
    add = config.add
    trade = config.trade
    
    ## --------------------------------------
    ## ----------- Connected
    ## --------------------------------------

    trade(3, {
        Item.FlaskOfAbominableSalts: -15,
        Item.ConnectedBenthic: 75
    })

    trade(3, {
        Item.FlaskOfAbominableSalts: -15,
        Item.ConnectedSummerset: 75
    })

    ## -------------------------
    ## Innate Item Conversions
    ## -------------------------

    normal_upconvert_success_rate = 0.6 - default_rare_success_rate

    # ----- Academic
    trade(1, {
        Item.FoxfireCandleStub: -1000,
        Item.FlaskOfAbominableSalts: 105
    })

    trade(1, {
        Item.FlaskOfAbominableSalts: -500,
        Item.MemoryOfDistantShores: 105
    })

    trade(1, {
        Item.MemoryOfDistantShores: -50,
        Item.ConnectedBenthic: -5,
        Item.VolumeOfCollatedResearch: 10,
        Item.CrypticClue: 50 * normal_upconvert_success_rate,
        Item.UncannyIncunabulum: 2 * default_rare_success_rate
    })

    # # requires urchin war active
    # # also other items hard to model
    # trade(1, {
    #     Item.LostResearchAssistant: -1,
    #     Item.Echo: 12.5 # blackmail material x1
    # })

    # ----- Cartography

    trade(1, {
        Item.ShardOfGlim: -1000,
        Item.MapScrap: 105
    })

    trade(1, {
        Item.MapScrap: -500,
        Item.ZeeZtory: 105
    })

    trade(1, {
        Item.ZeeZtory: -50,
        Item.PartialMap: 10,
        Item.MysteryOfTheElderContinent: 1 * normal_upconvert_success_rate,
        Item.Echo: 25 * default_rare_success_rate # 2x Brass Ring
    })

    trade(1, {
        Item.SaltSteppeAtlas: -1,
        Item.PuzzlingMap: -5,
        Item.PartialMap: -25,
        Item.VitreousAlmanac: -5,
        Item.GlassGazette: -25,
        # Item.ZeeLegs: -25, # TODO
        Item.CartographersHoard: 1
    })

    add({
        Item.Action: -1,
        Item.OneiromanticRevelation: -5,
        Item.ParabolanParable: 1
    })

    add({
        Item.Action: -1,
        Item.OneiromanticRevelation: -1,
        Item.VitreousAlmanac: 5,
        Item.GlassGazette: 1
    })    

    # ----- Mysteries

    # Journals to Implications @ 50:10
    trade(1,{
        Item.JournalOfInfamy: -50,
        Item.ConnectedBenthic: -5,
        Item.ExtraordinaryImplication: 10,
        Item.ShardOfGlim: 100 * normal_upconvert_success_rate,
        Item.StormThrenody: 2 * default_rare_success_rate
    })

    trade(1,{
        Item.TaleOfTerror: -50,
        Item.ConnectedSummerset: -5,
        Item.ExtraordinaryImplication: 10,
        Item.BottleOfStranglingWillowAbsinthe: 1 * normal_upconvert_success_rate,
        Item.FavourInHighPlaces: 2 * default_rare_success_rate
    })

    # # Implications to Incunabula @ 25:5
    trade(1, {
        Item.ExtraordinaryImplication: -25,
        Item.ConnectedBenthic: -20,
        Item.UncannyIncunabulum: 5,
        Item.NevercoldBrassSliver: 200 * normal_upconvert_success_rate,
        Item.Echo: 62.5 * default_rare_success_rate # Nodule of Pulsating Amber
    })

    # ----- Rumor

    trade(1, {
        Item.ProscribedMaterial: -250,
        Item.InklingOfIdentity: 105
    })

    trade(1, {
        Item.InklingOfIdentity: -500,
        Item.ScrapOfIncendiaryGossip: 105
    })

    trade(1, {
        Item.ScrapOfIncendiaryGossip: -50,
        Item.AnIdentityUncovered: 10,
        Item.ProscribedMaterial: 13 * normal_upconvert_success_rate,
        Item.FavourInHighPlaces: 2 * default_rare_success_rate
    })

    trade(1, {
        Item.AnIdentityUncovered: -25,
        Item.FavSociety: -1,
        Item.BlackmailMaterial: 5,
        Item.RatOnAString: 400 * normal_upconvert_success_rate,
        Item.BottleOfFourthCityAirag: 1 * default_rare_success_rate
    })

    # ----- Wines

    trade(1, {
        Item.BottleOfStranglingWillowAbsinthe: -50,

        Item.BottleOfBrokenGiant1844: 10,
        Item.IntriguingSnippet: 3 * normal_upconvert_success_rate,
        Item.UncannyIncunabulum: 2 * default_rare_success_rate
    })
