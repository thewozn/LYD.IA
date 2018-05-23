# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:55:37 2018
@author: anthony.woznica

Absolutely ANY USE of the following functions REQUIRE CREDIT IN THE HEADER OF THE FILE (WOZNICA Anthony).
There are NO exceptions.

This file contains all methods concerning text analysis.
"""


import utils as ut

import re
import datetime

    
    
    
    
def tokenise(sentence, language):
    """String * Integer -> List[String]
    Prend un texte en paramètre et renvoie une liste de mots suivant la langue sélectionnée.
    A noter, le chatbot était initialement prévu pour être en français et en anglais,
    mais suite à des contraintes temporelles nous n'en avons choisi qu'un seul, à savoir
    le français puisque plus intéressant à analyser en raison de ses règles de conjugaison.
    """
    
    if(language == 0): #Anglais
        regx = re.compile("[A-Z\-\'\.]{2,}(?![a-z])|[A-Z\-\'][a-z\-\']+(?=[A-Z])|[\'\w\-]+")
    elif(language == 1): #Français
        regx = re.compile("[A-Z\-\'\.]{2,}(?![a-z])|[A-Z\-\'][a-z\']+(?=[A-Z])|[\w\-\']+")
    return regx.findall(sentence)
    




def normalise(tokens, lefff, cities_list, keywords):
    """list[String]*dict{String, list[String]}*list[String]*list[String] -> list(tuple())
    Transforme les tokens de la phrase (tokens) en forme normale, avant de
    comparer à la liste de mots clés et de remplacer les formes normalisées par des
    mots-clés affectés/des noms de ville/des dates. 
    On dispose des balises suivantes pour caractériser un mot:
        K____word____ correspondant aux mots-clés
        W____word____ correspondant aux mots reconnus
        C____word____ correspondant à un nom de ville
        D____word____ correspondant à une date
        ____UNK____ correspondant à un terme inconnu
    
    A noter, la fonction en elle-même aurait pu être auxilliaire, mais son avantage 
    réside dans sa maintenabilité. En effet, si l'on souhaite ajouter des mots-clés,
    il suffit d'ajouter une unique forme normalisée au fichier contenant les mots-clés
    plutôt que l'ensemble de ses déclinaisons.
    """
    
    normalised_tokens = list(tuple())
    tokens[0] = tokens[0].lower()
    
    for word in tokens:
        normalised_tokens.append((word,1))  #Création d'une liste de mots avec un coefficient de 1
    #Le coefficient dans le tuple correspond à la probabilité que le mot soit un nom de ville
    
    
    for i in range(0, len(tokens)): #Remplacement du token par sa forme normalisée et balisage
        for key in lefff.keys():
            if(tokens[i] in lefff[key]):
                if(key in keywords.keys()):
                    normalised_tokens[i] = ("K____" + keywords[key] + "____", 0)
                else:
                    normalised_tokens[i] = ("W____" + key + "____", 1)
                
                
    for i in range(0, len(normalised_tokens)): #Traitement des symboles
        normalised_tokens[i] = (normalised_tokens[i][0].replace('-', ' ').upper(), 1)
        
        probability = 0
        new_city = ""
        
        
        for city in cities_list: #Détection de la ville ressemblant le plus au nom propre fourni (les noms propres n'étant pas traités jusqu'à présent).
            if(ut.cmpstr(normalised_tokens[i][0], city) > probability):
                probability = ut.cmpstr(normalised_tokens[i][0], city)
                new_city = city
        normalised_tokens[i] = (normalised_tokens[i][0], probability)
        
        
        if("W____" not in normalised_tokens[i][0] and "K____" not in normalised_tokens[i][0] ):
            if(normalised_tokens[i][1] > 0.5): #On considère qu'il s'agit d'une ville dès lors que le mot ressemble à plus de 50% à un nom de ville
                normalised_tokens[i] = ("C____"+new_city.upper()+"____", probability)
            else: #Sinon, il s'agit soit d'un nombre, d'un mot-clé contenant un caractère spécial, soit d'un mot inconnu
                if(normalised_tokens[i][0].isdigit()):
                    normalised_tokens[i] = ("D____"+normalised_tokens[i][0].upper()+"____", 0)
                elif(normalised_tokens[i][0].lower() in keywords.keys()):
                    normalised_tokens[i] = ("K____" + keywords[normalised_tokens[i][0].lower()] + "____", 1)
                else:
                    normalised_tokens[i] = ("__UNK__", 0) 
            
            
    return normalised_tokens
        
      
      
      
def analysis_simpletoken(tokens, generated_tokens):
    """List[String]*List[String]->String
    Détecte les mots communs à une liste de tokens générés, et renvoie celui apparaissant
    en dernier dans la phrase.
    """
    favourite = ""    
    for tkn in tokens:
        if(tkn in generated_tokens):
            if(tkn != "OUI" or tkn != "NON"):
                favourite = tkn
            elif(favourite == ""):
                favourite = tkn
    return favourite


          
def semantic_analysis(normalised_tokens, request):
    """List[tuple(String, float)]*dict->dict
    Initialise le dictionnaire request à partir des mots-clés contenus. Les clés de ce dictionnaire
    sont les suivantes:
        origin_code             - Code de l'aéroport de départ (Non initialisable à ce stade)
        origin_location         - Ville de départ
        destination_code        - Code de l'aéroport de destination (Non initialisable à ce stade)
        destination_location    - Ville d'arrivée
        depart_date             - Date de départ au format AAAA-MM-JJ
        return_date             - Date d'arrivée au format AAAA-MM-JJ
        
    A partir de la signification des mots-clés et de leur ordre, les 
    champs sont initialisés. Les dates doivent être saisies au format MM/JJ ou MM JJ.
    """
    
    
    now = datetime.datetime.now()
    plain_token = []
    
    for token in normalised_tokens:     #Epuration de la liste de tokens (On ne conserve pas les
        if(token[0][0] != 'W'):         #mots avec une balise W____
            plain_token.append(token[0])


    command = ""
    
    for token in plain_token:
        
        if(token[0] == "K"):    #Traitement des mots clés
            if(token.split("____")[1] == "NOW"):
                request["depart_date"] = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
            command = token.split("____")[1]
            
        if(token[0] == 'C'):    #Traitement des villes
            if(command == "DEST"):
                request["destination_location"] = token.split("____")[1]
            elif(command == "DEPT"):
                request["origin_location"] = token.split("____")[1]
            else:
                if(request["destination_location"] == ''):
                    request["destination_location"] = token.split("____")[1]
                elif(request["origin_location"] == ''):
                    request["origin_location"] = token.split("____")[1]
                else:
                    request["destination_location"] = ''
                    request["origin_location"] = ''
                
        if(token[0] == 'D'):    #Traitement des dates
            if(command == "DEPT" or command == "DEST"):
                request["depart_date"] += "-"+token.split("____")[1]
            elif(command == "RET"):
                request["return_date"] += "-"+token.split("____")[1]
            else:
                if(len(request["depart_date"])<10):
                    request["depart_date"] += "-"+token.split("____")[1]
                elif(len(request["return_date"])<10):
                    request["return_date"] += "-"+token.split("____")[1]
                else:
                    request["return_date"] = "2018"
                    request["return_date"] = "2018"
                
    return request


def semantic_analysis_phase3(normalised_tokens, flights):
    """List[tuple(String, float)]*List[Flights]->List[Flights]
    Initialise les dictionnaires sortby et filters à partir d'instructions. Les clés des dictionnaires
    sont les suivantes:
        
        sortby                          DICTIONNAIRE DE TRI
            current_superlative         - Adjectif qualificatif (PLUS ou MOINS)
            current_qualificative       - Complément à l'adject (type UN PEU plus) | Non implémenté
            current_instruction         - Complément d'objet direct concerné par l'adjectif
        
        filters                         DICTIONNAIRE DE FILTRES - Non implémenté
            keywords                    - Mot concerné par le critère (Destination? Départ? Compagnie?)
            criteria                    - Critère de séléction: AUTRE ou MÊME

    La liste renvoyée est une liste triée selon les qualifficatifs forunis et (non implémenté)
    ordonnée selon les filtres donnés.
    """
    
    instruction_tokens = ["PRX", "TOT", "TAR", "SPD", "SLW", "ETP"]    #Types de tris possibles
    type_tokens = ["CPY", "DEP", "DST"] #Types de filtres possibles    
    
    sortby = {"current_superlative" : "",
              "current_qualificative" : "",
              "current_instruction" : ""
              }
    
    filters = {"keyword" : "",
               "criteria" : "",
               }
    
    
    flights_purposed = flights
    
    plain_token = []
    for token in normalised_tokens:         #On conserve uniquement les mots-clés
        if(token[0][0] == 'K'):
            plain_token.append(token[0])



    for token in plain_token:
        if(token.split("____")[1] == "MIN" or token.split("____")[1] == "MAX"):
            sortby['current_superlative'] = token.split("____")[1]
        if(token.split("____")[1] == "LOW"):
            sortby['current_qualificative'] = token.split("____")[1]
        if(token.split("____")[1] in instruction_tokens):
            sortby['current_instruction'] = token.split("____")[1]
        if(token.split("____")[1] == "SAM" or token.split("____")[1] == "OTH"):
            filters['keyword'] = token.split("____")[1]
        if(token.split("____")[1] in type_tokens):
            filters['criteria'] = token.split("____")[1]
        
        if(sortby['current_superlative'] != '' and sortby['current_instruction'] != ''):
            flights_purposed = ut.fsortby(sortby, flights_purposed)
            sortby['current_instruction'] = ''
            
        if(filters['criteria'] != '' and filters['keyword'] != ''):
            #flights_purposed = []
            filters['criteria'] = ''
        
    return flights_purposed
    


