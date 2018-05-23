# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:55:37 2018
@author: anthony.woznica

BASED ON AchintyaAshok's work: https://github.com/AchintyaAshok/Kayak-Scraper/tree/aef1f8f29f8c586e5ad8f644b2f6490c3d87501c

Absolutely ANY USE of the following functions REQUIRE CREDIT IN THE HEADER OF THE FILE (WOZNICA Anthony).
There are NO exceptions.

This file contains all methods concerning kayak.com scraping.
"""



import requests
import sys
from datetime import datetime



try: #L'appareil doit être connecté à internet pour pouvoir utiliser le mode
    request = requests.get("https://www.kayak.fr")
except:
    print("["+datetime.now().strftime('%H:%M:%S')+"] LID.IA : vous devez être connexté à Internet pour utiliser ce mode")    
    sys.exit()
    
    
    
headers = { #Headers de la requête
    'Host': 'www.kayak.fr',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Referer': '',
    'X-Requested-With': 'XMLHttpRequest',
    "Content-type": "application/x-www-form-urlencoded"
    }




class Travel:
    """
    La classe Travel correspond à l'aller-retour. Elle contient donc:
        - Le prix du trajet
        - Les étapes du trajet (aller/retour)
        - La date de départ (contenu dans self.etapes aussi, mais par commodité on met aussi cela ici)
        - Le nombre d'escales (idem)
        - La durée totale (idem)
    """
    
    def __init__(self, etapes, price):
        self.price = price
        self.etapes = etapes
        self.departureTime = int(etapes[0].departureTime.split(":")[0])*100 + int(etapes[0].departureTime.split(":")[1])
        self.escales = etapes[0].escales
        self.totalDuration = int(etapes[0].totalDuration.split("h")[0].strip())*100 + int(etapes[0].totalDuration.split("h")[1].split("min")[0].strip())
    
    
    def toString(self):
        s = "Prix: " + str(self.price) + " €\n"
        n = 1
        for etape in self.etapes:
            s += "Etape " + str(n) + "\n"
            s += etape.toString() + "\n"
            n += 1
        s += '\n'
        return s
        
        
        
        
    
class Step:
    """
    La classe Step() correspond à chaque étape du voyage, c'est à dire l'aller ou le retour.
    Elle contient donc:
        - La compagnie responsable de l'étape
        - Le lieu de départ
        - L'heure de départ
        - La date de départ
        - Le lieu d'arrivée
        - L'heure d'arrivée
        - La date d'arrivée
        - Le nombre d'escales
        - La durée totale
    """
    
    def __init__(self, company, departure, departureDate, departureTime, arrival, arrivalDate, arrivalTime, escalesList, totalDuration):
        self.company = company
        self.departure = departure
        self.departureTime = departureTime
        self.departureDate = departureDate
        self.arrival = arrival
        self.arrivalTime = arrivalTime
        self.arrivalDate = arrivalDate
        self.escales = escalesList[1:-1].split(", ")
        self.totalDuration = totalDuration
        
        
    def toString(self):
        s = "\t Proposé par " + self.company + "\n"
        s += "\t De " + self.departure + " le " + self.departureDate + " à " + self.departureTime + "\n"
        s += "\t De " + self.arrival + " le " + self.arrivalDate + " à " + self.arrivalTime + "\n"
        s += "\t Avec " + str(len(self.escales)) + " escales." + "\n"
        s += "\t Durée totale : " + str(self.totalDuration) + "\n"
        return s
        




        
def getFlights(origin_code, origin_location, destination_code,
               destination_location, depart_date, return_date):
    """String**6 -> List[Flights]
    Effectue une requête sur le site kayak.fr avec les paramètres de la fonction. La
    fonction retourne une liste de vols.
    """
    
    TravelsList = []
    
    data = {'url':'',} #Paramètres de la requête
    
    #Paramétrage de la requête
    headers['Referer'] = 'https://www.kayak.fr/flights/'+origin_code+'-'+destination_code+'/'+depart_date+'/'+return_date
    url = 'https://www.kayak.fr/s/horizon/flights/results/FlightSearchPoll'
    data['url'] = 'flights/'+origin_code+'-'+destination_code+'/'+depart_date+'/'+return_date
    
    request = requests.post(url, headers = headers, data = data)
    
    #Récupération de la réponse du serveur
    flights = str(request.json()).split("Base-Results-HorizonResult Flights-Results-FlightResultItem")
    
    #Traitement des données
    for flight in flights:
        TravelsList.append(parseJson(flight))
        
    TravelsList = TravelsList[1::]
    
    return TravelsList




def getAllFlights(request):
    """dict -> Llist[Flights]
    Lance la récupération des vols à partir du dictionnaire (request). La fonction teste toutes
    les combinaisons possibles entre les codes d'origine et les codes de destination.
    """
    TravelList = []
    travels = ''
    for origin_code in request['origin_code']:

        for destination_code in request['destination_code']:

            try:
                travels = getFlights(origin_code, request['origin_location'], destination_code,
                   request["destination_location"], request["depart_date"], request["return_date"])
            except:
                pass
            for travel in travels:
                TravelList.append(travel)
                
    return TravelList





def parseFlightPlan(data):
    """String -> List[Step]
    Parse les données reçues (data) pour initialiser l'objet Step. La fonction retourne
    une liste d'étapes de taille (théorique) 2, correspondant à l'aller/retour.
    """
    etapes = []
    
    for etape in data.split("Étape de vol")[1::]:
        company = etape.split("opéré par ")[1].split(".")[0]
        departure = etape.split("Part de ")[1].split(" le ")[0]
        departureDate = etape.split("Part de ")[1].split(" le ")[1].split(" à ")[0]
        departureTime = etape.split("Part de ")[1].split(" le ")[1].split(" à ")[1].split(" et arrive")[0]
        arrival = etape.split(" et arrive à ")[1].split(" le ")[0]
        arrivalDate = etape.split(" et arrive à ")[1].split(" le ")[1].split(" à ")[0]
        arrivalTime = etape.split(" et arrive à ")[1].split(" le ")[1].split(" à ")[1].split(". ")[0]
        if(len(etape.split(" et arrive à ")[1].split(" le ")[1].split(" à ")[1].split(". ")[1].split(" escales "))>1):
            escalesList = etape.split(" et arrive à ")[1].split(" le ")[1].split(" à ")[1].split(". ")[1].split(" escales ")[1].split(".")[0]
        else:
            escalesList = ""
        totalDuration = etape.split("Durée totale : ")[1].split(".")[0]
        etapes.append(Step(company, departure, departureDate, departureTime, arrival, arrivalDate, arrivalTime, escalesList, totalDuration))
            
    return etapes



def parseJson(data):
    """String -> new Travel
    Prend en argument un vol sous forme littérale et renvoie un objet Travel
    """
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    priceParser = data.split("<span class=\"price option-text\">\\n")
    if(len(priceParser) > 1):
        priceParser = data.split("<span class=\"price option-text\">\\n")[1]
        price = ""    
        for char in priceParser:
            if(char in numbers):
                price += char
            else:
                break;
            
        data = data.split("style=\"display: none\"> ")[1].split("</p>")[0]
        return Travel(parseFlightPlan(data), (price))
    else:
        return



def getWeather(city):
    """
    String*String -> String
    Retourne une phrase formatée contenant un message et sa date.

    """
    api_adress = 'http://api.openweathermap.org/data/2.5/weather?appid=f42f7ab362062f2b86725ecdcc1bdd01&lang=fr&units=metric&q='
    url = api_adress+city
    data = requests.get(url).json()
        
    if(data['cod'] == str(404)):
        return("")
        
    #description de la météo
    description = data['weather'][0]['description']
    
    #temeprature max
    temperature = data['main']['temp_max']
    
    #concatenation des informations obtenus pour afficher les string finaux
    description_str = "La meteo sur "+city+" en ce moment est: "+description+". "
    temperature = "Il y fait environ "+str(int(temperature))+" aujourd'hui."
    
    return (description_str + temperature)