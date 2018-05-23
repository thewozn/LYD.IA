# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:55:37 2018
@author: anthony.woznica

Absolutely ANY USE of the following functions REQUIRE CREDIT IN THE HEADER OF THE FILE (WOZNICA Anthony).
There are NO exceptions.

This file contains all methods regarding basic functions.
"""


import datetime
import operator
    
def isFull(dict1):
    """dict->Bool
    Retourne True si le dictionnaire est plein, False sinon.
    """
    if(len(dict1.keys()) == 0):
        return True
    for elem in dict1.keys():
        if(dict1[elem] == '' or dict1[elem] == '2018'):
            return False
    return True
    
    

def comparedict(d1, d2):
    """dict*dict->Boolean
    Compare les valeurs de deux dictionnaires. Retourne True si ils sont différents, False sinon.
    """
    for key in d1.keys():
        if(d1[key] != d2[key]):
            return True
    
    return False
    
    
    
def resetdict():
    """None -> dict()
    Retourne un dictionnaire vide
    """
    now = datetime.datetime.now()
    return {"origin_code" : [],
           "origin_location" : '',
           "destination_code": [],
           "destination_location" : '',
           "depart_date" : str(now.year),
           "return_date" : str(now.year)
           }



def setPriority(request, fav):
    """dict()*String -> None
    Place l'aéroport (fav) en premier élément de la liste
    """
    tmp = request['origin_code'][0]
    index = request['origin_code'].index(fav)
    request['origin_code'][index] = tmp
    request['origin_code'][0] = fav
    
    
    
    
def fsortby(rq, travellist):
    """dict*list -> list
    Prend en paramètre un dictionnaire comprenant des paramètres et trie la liste
    en fonction de ces paramètres.
    """
    data = []
    data = travellist
    
    if(rq["current_instruction"] == "PRX"):
        data.sort(key=operator.attrgetter('price'))

    elif(rq["current_instruction"] == "ETP"):
        data.sort(key=operator.attrgetter('escales'))
        
    elif(rq["current_instruction"] == "TOT"):
        data.sort(key=operator.attrgetter('departureTime'))
        data = data[::-1]
        
    elif(rq["current_instruction"] == "TAR"):
        data.sort(key=operator.attrgetter('departureTime'))
        
    elif(rq["current_instruction"] == "SPD"):
        data.sort(key=operator.attrgetter('totalDuration'))
        data = data[::-1]
        
    elif(rq["current_instruction"] == "SLW"):
        data.sort(key=operator.attrgetter('totalDuration'))
        
    if(rq["current_superlative"] == "MAX"):
        return list(reversed(data))
        
    else:
        return data
        
        
        
def cmpstr(str1, str2):
    """String*String->float
    Renvoie le coefficient de ressemblance entre deux chaînes de caractères.
    L'algorithme est LOIN d'être parfait, ceci dit. En effet, pour qu'il soit
    davantage efficace, il aurait fallu calculer les distances entre les lettres
    afin de déterminer de quel terme il s'agit. Toutefois, la solution fournie
    reste acceptable puisque son taux de succès est satisfaisant dans les cas étudiés.
    """
    
    common_letters = 0.0
    longest = ""
    shortest = ""
    
    if(len(str1) > len(str2)): #1) On souhaite une iteration sur la chaîne la plus courte
        longest = str1
        shortest = str2
    else:
        longest = str2
        shortest = str1
        
    for i in range(0, len(shortest)):   #On compte le nombre de lettres en commun
        if(shortest[i] == longest[i]):
            common_letters += 1
    
    return 2*common_letters/(len(str2)+len(longest))