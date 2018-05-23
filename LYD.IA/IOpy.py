# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:55:37 2018
@author: anthony.woznica

Absolutely ANY USE of the following functions REQUIRE CREDIT IN THE HEADER OF THE FILE (WOZNICA Anthony).
There are NO exceptions.

This file contains all functions of the chatbot regarding to data loading.
"""


from datetime import datetime
from time import strftime
import sys
import Airports as ap






def writerecap(data, flightname, dialog):
    """String*String*String->None
    Ecrit les informations (data) relative au vol dans un fichier nommé suivant le nom du vol (flightname)
    et la date du passage de la commande. La fonction propose aussi d'ajouter le dialogue entre l'utilisateur
    et LYD.IA en fin de fichier.
    """


    now = str(datetime.now().strftime("%Y_%m_%d_%H_%M"))
    filename = "Outputs/" + flightname + " " + now + ".txt"
    try:
        with open(filename,"w+") as f:
            try:
                f.write("RECAPITULATIF DE VOTRE REQUÊTE DU " + now) 
                f.write("\n______________________________________________________________\n\n")
                f.write(data)
                f.write("\n\n\nVous retrouverez ci-dessous le récapitulatif de votre dialogue avec LYD.IA")
                f.write("\n\n______________________________________________________________\n\n")
                for line in dialog:
                    f.write(line+"\n")
                f.close()

            except:
                print("Writing exception")
                f.close()
                sys.exc_info()[0]
                sys.exit()
    except:
        print("Unable to open the file")
        sys.exc_info()[0]
        sys.exit()
        
    


def load_responses():
    """None->Dict{String: List[String]}
    Charge le fichier Prerecorded_responses.txt et initialise le dictionnaire (prerecorded_responses) dont les clés correspondent
    au type de phrase, et dont les valeurs correspondent aux phrases.
    """
    try:
        with open("Files/Prerecorded_responses.txt", "r") as f:
            prerecorded_responses = {}
            for line in f.readlines():
                newkey = line.split('_')[0].strip()
                if(newkey not in prerecorded_responses.keys()):
                    prerecorded_responses[newkey] = []
                prerecorded_responses[newkey].append(line.split('_')[1].strip())
                
    except:
        f.close()
        sys.exc_info()[0]
        sys.exit()
        
    return prerecorded_responses
    
    
    
    
def load_city_names():
    """None -> List[String]
    Charge la liste des noms de ville contenant au moins un aéroport à partir de la base de données
    chargée dans Airports.py
    """
    citiesList = [row[0].upper() for row in ap.cursor.execute("SELECT city FROM airports GROUP BY city")]
    return citiesList
    
    
    
    
def load_keywords(file):
    """String -> dict{String, List[String]}
    Charge la liste des mots-clés  et leur signification à partir du fichier (file)
    """
    try:
        with open("Files/"+file, "r") as f:
            keywords = {}
            for line in f.readlines():
                keywords[line.split(',')[0].strip()] = line.split(',')[1].strip()
            f.close()
    except:
        print("Unable to load " + file)
        f.close()
        sys.exc_info()[0]
        sys.exit()
    return keywords
    
    
    
    
def load_lefff():
    """None -> dict{String, List[String]}
    Charge dans un dictionnaire le Lexique des Formes Fléchies du Français (LEFFF) et le retourne rempli.
    A noter, LEFFF n'est ici pas pleinement exploité puisque le mode 3 se base sur des  mots-clés
    et non sur une construction sémantique de la phrase.
    """
    
    LEFFF = {}
    
    try:
        with open("Files/lefff-2.1.txt", "r") as f:
    
            lines = f.readlines()
            for line in lines:
                if("np" not in line and "pred=" in line): #Exclusion de tous les noms propres (Villes, Pays etc..)
                    
                    key = line.split("[pred='")[1].split("_")[0]
                    
                    if(key not in LEFFF.keys()): #Création d'une clé si l'entrée n'est pas présente dans le dictionnaire
                        LEFFF[key] = []
                        
                    LEFFF[key].append(line.split("	")[0].strip())

    except:
        print("Unable to load lefff-2.1.txt")
        f.close()
        sys.exc_info()[0]
        sys.exit()
        
    return LEFFF