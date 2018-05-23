# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:55:37 2018
@author: anthony.woznica

Absolutely ANY USE of the following functions REQUIRE CREDIT IN THE HEADER OF THE FILE (WOZNICA Anthony).
There are NO exceptions.

This file contains A SAMPLE of a graphic interface for the chatbot.
"""


import pygame
from pygame.locals import *
import os
from datetime import datetime
from time import strftime
import sys
from textbox import TextBox
import lexical_analysis as lex
import IOpy as io
import utils as ut
from random import randint as rd




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
    response = (message)
    log.append(response)
    return response
    
hist = [" "," "," "," "," "," "," "]  

   


def main():
    
    lefff = io.load_lefff()    
    citiesList = io.load_city_names()
    
    keywords = io.load_keywords("Keywords.txt")
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
    TravelList = []         #Liste des vols trouvés

    #Initialisation
    pygame.init()
    clock = pygame.time.Clock()
    FPS = 30
    
    #Window
    fenetre = pygame.display.set_mode((1280, 720))
    pygame.font.init()
    speech = pygame.font.SysFont('Trebuchet MS', 25)
    currtime = pygame.font.SysFont('Trebuchet MS', 50)
    history = pygame.font.SysFont('Trebuchet MS', 20)
    
    #Variable qui continue la boucle si = 1, stoppe si = 0
    loop = 1
    index = 0
    alpha = 80
    coeff = 1
    
    
    images = []
    lydia = pygame.image.load("GraphicalContent/interface.png").convert_alpha()
    loadingscreen = pygame.image.load("GraphicalContent/blackscreen.png").convert()
    loadingmessage = pygame.image.load("GraphicalContent/loadingmessage.png").convert_alpha()
    s = pygame.Surface((1280, 720))
    
    for imgno  in os.listdir("GraphicalContent/backgroundAnim/"):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        image = pygame.image.load("GraphicalContent/backgroundAnim/" + imgno).convert()
        images.append(image)
        
        s.set_alpha(alpha)
        s.fill((0,0,0)) 
        fenetre.blit(loadingscreen, (0,0))
        fenetre.blit(loadingmessage, (0,0))
        fenetre.blit(s, (0,0)) 
        pygame.display.flip()
        
        alpha += coeff
        
        if(alpha <= 80):
            print(imgno)
            coeff = 5
        elif(alpha >= 240):
            coeff = -5
              
    print("Successfully loaded!")
    
    
    textsurface = speech.render('Bonjour, je suis LYD.IA', False, (246, 246, 246))
    text_rect = textsurface.get_rect(center=(640, 210))
    textsurface2 = speech.render("", False, (246, 246, 246))                    
    text_rect2 = textsurface2.get_rect(center=(640, 250))
    
    def submit_answer(id, txt):
        text = "".join(inputbox.buffer)
        if(text.strip() != ""):
            hist.append(text)
            
    inputbox = TextBox((440,540,400,50),command=submit_answer, clear_on_enter=True,inactive_on_enter=False)
    
    last_entry = " "
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            inputbox.get_event(event)
        inputbox.update()
        fenetre.blit(images[index], (0,0))
        fenetre.blit(lydia, (0,0))
        text_rect = textsurface.get_rect(center=(640, 210))
        fenetre.blit(textsurface, text_rect)
        text_rect2 = textsurface2.get_rect(center=(640, 250))
        fenetre.blit(textsurface2, text_rect2)
            


        datesurface = currtime.render(datetime.now().strftime('%H:%M:%S'), False, (246, 246, 246))
        fenetre.blit(datesurface, (20, 50))
        
    
    
        index = (index+1)%1350
        
        if(last_entry != hist[len(hist)-1]): #Si il y a eu une saisie
            
            last_entry = hist[len(hist)-1]
            response = last_entry
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
                        textsurface = speech.render(Lydia(generate_response("NOP", bank), log), False, (246, 246, 246))                    
                        text_rect = textsurface.get_rect(center=(640, 210))
                        fenetre.blit(textsurface, text_rect)
                        textsurface2 = speech.render(Lydia(generate_response("ASK", bank), log), False, (246, 246, 246))                    
                        text_rect2 = textsurface2.get_rect(center=(640, 250))
                        fenetre.blit(textsurface2, text_rect2)
                    else:
                        #Si l'utilisateur doit confirmer son choix
                        if(ask == 1):
    
                            if(("K____NEG____",0.3) not in normalised_tokens and ask==1): #Si absence de réponse négative
                                request = prerequest.copy()
                                
                                if(("K____AFF____", 0.2222222222222222) in normalised_tokens): #Si positif
                                    textsurface = speech.render(Lydia(generate_response("FIL", bank), log), False, (246, 246, 246))
                                    text_rect = textsurface.get_rect(center=(640, 210))
                                    fenetre.blit(textsurface, text_rect)
                                    textsurface2 = speech.render(Lydia(get_missing(request, bank), log), False, (246, 246, 246))                    
                                    text_rect2 = textsurface2.get_rect(center=(640, 250))
                                    fenetre.blit(textsurface2, text_rect2)
                            else:
                                textsurface = speech.render(Lydia(generate_response("NFI", bank), log), False, (246, 246, 246))
                                text_rect = textsurface.get_rect(center=(640, 210))
                                fenetre.blit(textsurface, text_rect)
                                textsurface2 = speech.render(Lydia(get_missing(request, bank), log), False, (246, 246, 246))                    
                                text_rect2 = textsurface2.get_rect(center=(640, 250))
                                fenetre.blit(textsurface2, text_rect2)
                                tmprequest = request.copy()
                            ask = 0
                            
                        #Sinon, c'est que son choix doit être élargi:
                        else:
                            if(ask == 1):
                                textsurface = speech.render(Lydia(get_missing(request, bank), log), False, (246, 246, 246))                                
                                text_rect = textsurface.get_rect(center=(640, 210))
                                textsurface2 = speech.render("", False, (246, 246, 246))
                                fenetre.blit(textsurface, text_rect)                            
                                ask = 0
                            else:
                                textsurface = speech.render(Lydia(request_toString(request, tmprequest), log), False, (246, 246, 246))                                
                                text_rect = textsurface.get_rect(center=(640, 210))
                                fenetre.blit(textsurface, text_rect)
                                textsurface2 = speech.render("", False, (246, 246, 246))                              
                                prerequest = tmprequest.copy()
                                ask = 1
                        if(ut.isFull(request)):
                            phase = 1 
                          
                          
                if(phase == 1): #Seconde phase du chatbot
                    textsurface = speech.render(Lydia("Je suis navrée, mon développeur n'a pas eu lle temps de me terminer...", log), False, (246, 246, 246))                                
                    text_rect = textsurface.get_rect(center=(640, 210))
                    textsurface2 = speech.render("", False, (246, 246, 246))
                    fenetre.blit(textsurface, text_rect)
                        
        for i in range (0,3):
            tmp = history.render(hist[len(hist)-i-1], False, (246-i*30, 246-i*30, 246))
            tmp_rect = tmp.get_rect(center=(640, 520-i*30))
            fenetre.blit(tmp, tmp_rect)
        inputbox.draw(fenetre)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()


