from enums import *
from helper.utils import *
from player import Player
import config

# class Services(Enum):
#     # Rostygold = auto()
#     # Steel = auto()
#     # Bones = auto()
#     # Food = auto()
#     Hell = auto()
#     Zailors = auto()
#     TheGreatGame = auto()
#     Bohemians = auto()
#     Society = auto()
#     TheGraciousWidow = auto()
#     TheHoneyAddledDetective = auto()
#     TombColonists = auto()
#     Benthic = auto()
#     TheChurch = auto()
#     Constables = auto()
#     Clay = auto()

# def profession_options(player):
#     list = []
#     if player.profession == Profession.Silverer:
#         list += [Services.Hell, Services.Bohemians, Services.TombColonists]
#         if player.specialization == Specialization.Oneirotect:
#             list += Services.TheGreatGame
#         elif player.specialization == Specialization.OntologicalCartographer:
#             list += Services.TheHoneyAddledDetective

#     elif player.profession == Profession.MonsterHunter:
#         list =+ [Services.Hell, Services.Society, Services.TheHoneyAddledDetective]
#         if player.specialization == Specialization.HeirarchOfTheHunt:
#             list += Services.TheGreatGame
#         elif player.specialization == Specialization.Teratomancer:
#             list += Services.Benthic

#     elif player.profession == Profession.Correspondent:
#         list =+ [Services.Hell, Services.Bohemians, Services.Society]
#         if player.specialization == Specialization.CrimsonEngineer:
#             list += Services.Zailors
#         elif player.specialization == Specialization.Epistolant:
#             list += Services.Benthic            

#     elif player.profession == Profession.CrookedCross:
#         list =+ [Services.Hell, Services.Zailors, Services.TheChurch]
#         if player.specialization == Specialization.Beatificator:
#             list += Services.TombColonists
#         elif player.specialization == Specialization.Schismatic:
#             list += Services.Clay

#     elif player.profession == Profession.Midnighter:
#         list =+ [Services.Hell, Services.Zailors, Services.TheGraciousWidow]
#         if player.specialization == Specialization.Iniquitor:
#             list += Services.TheGreatGame
#         elif player.specialization == Specialization.Letheologist:
#             list += Services.Bohemians                  

#     elif player.profession == Profession.Licentiate:
#         list =+ [Services.TheGreatGame, Services.TheGraciousWidow, Services.Constables]
#         if player.specialization == Specialization.Fractionist:
#             list += Services.Hell
#         elif player.specialization == Specialization.Siopian:
#             list += Services.Zailors

#     return list

def add_trades(config: config.Config):
    trade = config.trade
    active_player = config.player
    # spec = active_player.specialization

    trade(0, {
        Item.ApproximateValueOfOutstandingInvoicesInPennies: -500,
        Item.PieceOfRostygold: 500
    })

    trade(0, {
        Item.ApproximateValueOfOutstandingInvoicesInPennies: -1250,
        Item.BessemerSteelIngot: 25
    })

    trade(0, {
        Item.ApproximateValueOfOutstandingInvoicesInPennies: -3100,
        Item.FemurOfAJurassicBeast: 2,
        Item.FinBonesCollected: 2,
        Item.HornedSkull: 2 * 1/6,
        Item.PlatedSkull: 1 * 1/6,
        Item.AlbatrossWing: 2 * 1/6,
        Item.FossilisedForelimb: 1 * 1/6,
        Item.FlourishingRibcage: 2 * 1/6
    })

    # TODO refactor to use special _Action types
    trade(10, {
        Item.AirsOfIndustry1to10: 1,
        Item.AirsOfIndustry11to20: 1,
        Item.AirsOfIndustry21to30: 1,
        Item.AirsOfIndustry31to40: 1,
        Item.AirsOfIndustry41to50: 1,
        Item.AirsOfIndustry51to60: 1,
        Item.AirsOfIndustry61to70: 1,
        Item.AirsOfIndustry71to80: 1,
        Item.AirsOfIndustry81to90: 1,
        Item.AirsOfIndustry91to100: 1,
    })

    airs_list = [
        Item.AirsOfIndustry1to10,   # 0
        Item.AirsOfIndustry11to20,  # 1
        Item.AirsOfIndustry21to30,
        Item.AirsOfIndustry31to40,
        Item.AirsOfIndustry41to50,
        Item.AirsOfIndustry51to60,
        Item.AirsOfIndustry61to70,
        Item.AirsOfIndustry71to80,
        Item.AirsOfIndustry81to90,
        Item.AirsOfIndustry91to100
        ]


    if active_player.get(Item.SetOfCosmogoneSpectacles):
        for airs in airs_list[0:4]:
            rate1 = broad_challenge_pass_rate(active_player.qualities[Item.Dangerous], 90)
            rate2 = narrow_challenge_pass_rate(active_player.qualities[Item.Glasswork], 0)
            pass_rate = rate1 * rate2
            config.add_weighted_trade(0, 
                (pass_rate, {
                    airs: -1,
                    Item.ApproximateValueOfOutstandingInvoicesInPennies: 410
                }),
                (1.0 - pass_rate, {
                    airs: -1,
                    Item.ApproximateValueOfOutstandingInvoicesInPennies: 200
                })
            )
        for airs in airs_list[0:5]:
            trade(0, {
                airs: -1,
                Item.ApproximateValueOfOutstandingInvoicesInPennies: 320,
                Item.ServicesBohemians: 1
            })

        for airs in airs_list[3:7]:
            trade(0, {
                airs: -1,
                Item.ApproximateValueOfOutstandingInvoicesInPennies: 320,
                Item.ServicesTombColonists: 1
            })

        for airs in airs_list[4:6]:
            trade(0, {
                airs: -1,
                Item.ApproximateValueOfOutstandingInvoicesInPennies: 410,
            })

        for airs in airs_list[5:7]:
            trade(0, {
                airs: -1,
                Item.ApproximateValueOfOutstandingInvoicesInPennies: 410,
                Item.ServicesHell: 1
            })

        for airs in airs_list[6:]:
            trade(0, {
                airs: -1,
                Item.ApproximateValueOfOutstandingInvoicesInPennies: 320
            })            

        for airs in (Item.AirsOfIndustry81to90,
                    Item.AirsOfIndustry91to100):
            trade(0, {
                airs: -1,
                Item.ApproximateValueOfOutstandingInvoicesInPennies: 410
            })            

        # if spec == Specialization.OntologicalCartographer:
        #     for airs in airs_list[:5]:
        #         trade(0, {
        #             airs: -1,
        #             Item.ApproximateValueOfOutstandingInvoicesInPennies: 450,
        #             Item.ServicesBohemians: 1
        #         })

        #     for airs in airs_list[:4]:
        #         trade(0, {
        #             airs: -1,
        #             Item.ApproximateValueOfOutstandingInvoicesInPennies: 410,
        #             Item.ServicesTheHoneyAddledDetective: 1
        #         })

        # if spec == Specialization.Oneirotect:
        #     for airs in airs_list[5:]:
        #         trade(0, {
        #             airs: -1,
        #             Item.ApproximateValueOfOutstandingInvoicesInPennies: 450
        #         })

        #     for airs in airs_list[7:]:
        #         trade(0, {
        #             airs: -1,
        #             Item.ApproximateValueOfOutstandingInvoicesInPennies: 410,
        #             Item.ServicesTheGreatGame: 1
        #         })    
                
    # if profession == Profession.MonsterHunter:


    # if (spec == Specialization.HeirarchOfTheHunt):
    #     trade(100, )