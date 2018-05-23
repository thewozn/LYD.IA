# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:55:37 2018
@author: anthony.woznica

Absolutely ANY USE of the following functions REQUIRE CREDIT IN THE HEADER OF THE FILE (WOZNICA Anthony).
There are NO exceptions.

This file contains all methods regarding the dialog part of the chatbot.
"""


import lexical_analysis as lex
import Airports as apt
import scrape as sc
import IOpy as io
import utils as ut
from random import randint as rd
from datetime import datetime
from time import strftime
import sys






def generate_response(response_type, bank):
    """String*Dict{String, List[String]}->String
    La fonction prend en paramètre une chaîne de caractères correspondant au type de réponse
    attendu ainsi que le dictionnaire contenant l'ensemble des types de réponse possibles
    """
    if(len(bank) == 0): #On utilise des phrases déjà toutes faites dans les cas d'erreur pour éviter l'erreur inhérente à la lecture de fichiers
        print("Je crois avoir été victime d'un bug informatique, je n'ai aucune réponse à apporter...")
        sys.exit()
    elif(response_type not in bank.keys()): #idem
        print("Je crois avoir été victime d'un bug informatique, je ne connais pas le type de réponse à apporter.")
        sys.exit()
    else:
        return bank[response_type][rd(0, len(bank[response_type])-1)]





def get_missing(request, bank):
    """Dict{String, Int}*Dict{String, String}->String
    Détecte les éléments manquants dans la requête de l'utilisateur et génère une phrase aléatoire
    en sortie afin de récupérer des renseignements
    """
    
    response = generate_response("PRC", bank) + " "
    
    #On définit des priorités dans l'ordre des informations à récolter afin d'avoir une certaine cohérence    
    priority_set = ["destination_location", "depart_date", "origin_location", "return_date"]

    for elem in priority_set:
        if(request[elem] == '' or request[elem] == '2018'):
            if(elem == "return_date"):
                return response+generate_response("RED", bank)+"?"
            elif(elem == "depart_date"):
                return response+generate_response("DPD", bank)+"?"
            elif(elem == "destination_location"):
                return response+generate_response("DST", bank)+"?"
            if(elem == "origin_location"):
                return response+generate_response("ORI", bank)+"?"
            else: #Cas d'erreur où rien n'aurait été trouvé mais qu'il manquerait quand même quelque chose.
                return "Veuillez répéter, je crois avoir été victime d'un bug informatique."
    
    return generate_response("COM", bank)
    





def request_toString(request, tmprequest):
    """dict*dict->String
    Compare le contenu de la demande précédente (request) avec la requête actuelle (tmprequest) et
    reformule l'ensemble sous la forme d'une chaîne de caractères compréhensible par l'utilisateur
    afin de s'assurer de la viabilité des données saisies.
    """
    
    response = "Vouliez-vous dire" #Phrase de base
    response_adapt = False #Booléen portant sur la nécessité d'adapter la réponse en fonction du contexte
    
    if(tmprequest['origin_location'] != request['origin_location']):
        response += " que vous partez de " + tmprequest['origin_location'].lower()
        response_adapt = True
        
    if(tmprequest['depart_date'] != request['depart_date']):
        if(response_adapt):
            response += " le " + tmprequest['depart_date']
        else:
            response += " que vous voulez partir le " + tmprequest['depart_date'].lower()
            
    if(tmprequest['destination_location'] != request['destination_location']):
        if(response_adapt):
            response += " pour aller à " + tmprequest['destination_location'].lower()
        else:
            response += " que vous souhaitez aller à " + tmprequest['destination_location'].lower()
        response_adapt = True
        
    if(tmprequest['return_date'] != request['return_date']):
        if(response_adapt):
            response += " pour revenir le " + tmprequest['return_date']
        else:
            response += " que vous souhaitez revenir le " + tmprequest['return_date']
            
    response += "?"
    
    return response
    



def Lydia(message, log):
    """String*String -> String
    Retourne une phrase formatée contenant un message et sa date.
    """
    response = ("["+datetime.now().strftime('%H:%M:%S')+"] LID.IA : " + message)
    log.append(response)
    return response


def main():
    lefff = io.load_lefff()    
    citiesList = io.load_city_names()
    
    keywords = io.load_keywords("Keywords.txt")
    keywords2 = io.load_keywords("Keywords2.txt")
    bank = io.load_responses()
    
    #Dictionnaires utilisés 
    request = ut.resetdict()        #Dictionnaire principal           
    tmprequest = ut.resetdict()     #Dictionnaire de la dernière saisie utilisateur
    prerequest = ut.resetdict()     #Trace
    
    #Historique
    log = []  

    #Variables de choix
    ask = 0     #1 si l'utilisateur doit répondre à une question du bot, 0 sinon
    phase = 0   #Phase dans laquelle se situe le bot
    
    #Tablaux temporaires
    generated_tokens = []   #Tokens générés lors de la phase 2
    TravelList = []         #Liste des vols trouvés
    
    
    print(Lydia(generate_response("FRM", bank), log))
    print(Lydia(generate_response("ASK", bank), log))
    
    while(1):
        userid = "["+ datetime.now().strftime('%H:%M:%S')+"] " + '> '
        response = input(userid)
        log.append(userid + response)
        
        #Cas de sortie de programme
        if(response == "q"):
            break

        #Cas d'une réponse non vide
        if(response.strip() != ''):
            
            #Tokenisation de la phrase (commune pour toutes les phases)
            token_user = lex.tokenise(response, 1)
           
            #Phase de récolte d'informations
            if(phase == 0):
                
                if(TravelList != []): #Réinitialisaton des vols si régression de phase
                    TravelList = [] 
                
                normalised_tokens = lex.normalise(token_user, lefff, citiesList, keywords)
                tmprequest = lex.semantic_analysis(normalised_tokens, tmprequest) #Création de la nouvelle requête
                        
                if(ut.comparedict(request, tmprequest) == False and ask == 0): #Si aucun changement n'a été apporté à la demande précédente
                    print(Lydia(generate_response("NOP", bank), log))          #et que l'utilisateur ne devait pas fournir une réponse 
                    print(Lydia(generate_response("ASK", bank), log))
            
            
                else:
                    #Si l'utilisateur doit confirmer son choix
                    if(ask == 1):

                        if(("K____NEG____",0.3) not in normalised_tokens and ask==1): #Si absence de réponse négative
                            request = prerequest.copy()
                            
                            if(("K____AFF____", 0.2222222222222222) in normalised_tokens): #Si positif
                                print(Lydia(generate_response("FIL", bank), log))
                                print(Lydia(get_missing(request, bank), log))
                        else:
                            print(Lydia(generate_response("NFI", bank), log))
                            print(Lydia(get_missing(request, bank), log))
                            tmprequest = request.copy()
                        ask = 0
                        
                    #Sinon, c'est que son choix doit être élargi:
                    else:
                        if(ask == 1):
                            print(Lydia(get_missing(request, bank), log))
                            ask = 0
                        else:
                            print(Lydia(request_toString(request, tmprequest), log))
                            prerequest = tmprequest.copy()
                            ask = 1
                    if(ut.isFull(request)):
                        phase = 1
                        
                        
            if(phase == 1): #Seconde phase du chatbot
                
                normalised_tokens = lex.normalise(token_user, lefff, citiesList, keywords)
                
                #Initialisation de la phase 2
                if(request['origin_code']==[] or request['destination_code']==[]):
                    
                    generated_tokens = ["OUI", "NON"] #Création de nouveaux tokens
                    request['origin_code'] = apt.get_codes(request['origin_location'])
                    request['destination_code'] = apt.get_codes(request['destination_location'])
                    
                    if(request['origin_code'] == []):   #Rollback si requête insatisfaisable
                        print(Lydia("Navrée, il n'y a pas d'aéroports à proximité de " + request['origin_location'] + " .Veuillez faire un autre choix ", log))
                        request = ut.resetdict()
                        phase = 0
                    elif(request['destination_code'] == []): #idem
                        print(Lydia("Navrée, il n'y a pas d'aéroports à proximité de " + request['destination_location'] + " .Veuillez faire un autre choix ", log))
                        request = ut.resetdict()
                        phase = 0
                    else:
                        print(Lydia(sc.getWeather(request['destination_location']), log))
                        print(Lydia("Voici les aéroports disponibles à l'aller:", log))
                        for code in request['origin_code']:
                            print("-- " + code)
                            generated_tokens.append(code)
                        print(Lydia("Avez vous-une préférence pour l'un de ces aéroports?", log))  
                
                
                else: #Une fois que tout est initialisé
                    token_user = lex.tokenise(response.upper(), 1)
                    
                    #Demande de précisions si oui avec différents types de réponses possibles: adaptée ou auto-générée
                    if(lex.analysis_simpletoken(token_user, generated_tokens) == "OUI"):
                        if(rd(1,2) == 2):
                            print(Lydia(generate_response("PRC2", bank), log))
                        else:
                            print(Lydia(generate_response("PRC2SPEC", bank) + " " +generated_tokens[rd(2,len(generated_tokens)-1)] + "!", log))
                    elif(lex.analysis_simpletoken(token_user, generated_tokens) == "NON"):
                        print(Lydia(generate_response("FIL", bank), log))
                        phase = 2
                    elif(lex.analysis_simpletoken(token_user, generated_tokens) in generated_tokens[2:]):
                        ut.setPriority(request, lex.analysis_simpletoken(token_user, generated_tokens))                    
                        print(Lydia(generate_response("FIL", bank), log))
                        print(Lydia(generate_response("RECH", bank) + " " + lex.analysis_simpletoken(token_user, generated_tokens), log))
                        phase = 2
                    else:
                        print(Lydia(generate_response("UNK", bank), log))
                        
            #Phase 2 on utilise le web-scraping pour récupérer les vols concernant les saisies de l'utilisateur
            #Nécessite un appareil connecté à Internet
            if(phase == 2):
                normalised_tokens = lex.normalise(token_user, lefff, citiesList, keywords2)
                if(TravelList == []):
                    ask = 0
                    print(Lydia(generate_response("WAIT", bank), log))
                    if(rd(1,3) >= 2):
                        print(Lydia(generate_response("GAM", bank), log))
                    else:
                        print(Lydia(generate_response("GAM2", bank), log))
                        
                    TravelList = sc.getAllFlights(request) #Scraping des données de Kayak
                    
                    print(Lydia("J'ai trouvé " + str(len(TravelList)) + " plans de voyage correspondant à vos attentes.", log))
                    print(Lydia("Celui qui me semble le mieux répondre à vos attentes est celui-ci:", log))
                    try:
                        print(sc.Travel.toString(TravelList[0]))
                    except:
                        print(Lydia("Attendez, j'ai un petit souçis technique...", log))
                        TravelList = []
                    print(Lydia("Cela vous convient-il?", log))
                    
                    ask = 1
                    
                else:
                    if(ask == 1):
                        #Si absence de réponse négative
                        if(("K____NEG____",0.3) not in normalised_tokens and ask==1):
                            print(Lydia("Parfait. Vous trouverez le récapitulatif dans le fichier FLIGHT-date.txt", log))
                            print(Lydia(generate_response("END", bank), log))
                            data = sc.Travel.toString(TravelList[0])
                            io.writerecap(data, "FLIGHT", log)
                            break
                        else:
                            print(Lydia(generate_response("PRC3", bank), log))    
                        ask = 0
                    else:
                        TravelList = lex.semantic_analysis_phase3(normalised_tokens, TravelList)
                        print(Lydia(generate_response("WAIT", bank), log))    
                        print(sc.Travel.toString(TravelList[0]))
                        print(Lydia("Ce vol-ci vous convient-il mieux?", log))    
                        ask = 1