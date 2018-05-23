# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:55:37 2018
@author: anthony.woznica

Absolutely ANY USE of the following functions REQUIRE CREDIT IN THE HEADER OF THE FILE (WOZNICA Anthony).
There are NO exceptions.

This file contains main selection method.
"""




if __name__=="__main__":
    print("""

    ___                  ___                       
   (   )                (   )        .-.           
    | |   ___  ___    .-.| |        ( __)   .---.  
    | |  (   )(   )  /   \ |        (''")  / .-, \ 
    | |   | |  | |  |  .-. |         | |  (__) ; | 
    | |   | |  | |  | |  | |         | |    .'`  | 
    | |   | '  | |  | |  | |         | |   / .'| | 
    | |   '  `-' |  | |  | |         | |  | /  | | 
    | |    `.__. |  | '  | |   .-.   | |  ; |  ; | 
    | |    ___ | |  ' `-'  /  (   )  | |  ' `-'  | 
   (___)  (   )' |   `.__,'    `-'  (___) `.__.'_. 
           ; `-' '                                 
            .__.'                                  
      
____________________________________________________________

W O Z N I C A   A n t h o n y
""")

print("Bonjour, pour lancer le bot, saisissez le type de mode que vous souhaitez utiliser:")
print("0 - Mode support console, complet et fonctionnel")
print("1 - Mode graphique, uniquement phase 1 de disponible")
print("2 - Quitter le programme")

loop = True

while(loop):
        response = input('> ')
        if(response == "0"):
            import Interface

            Interface.main()
            print("Vous revoici à l'écran de sélection")
            print("0 - Mode support console, complet et fonctionnel")
            print("1 - Mode graphique, uniquement phase 1 de disponible")
            print("2 - Quitter le programme")
            
        elif(response == "1"):
            import graphical_content
            graphical_content.main()
            print("Vous revoici à l'écran de sélection")
            print("0 - Mode support console, complet et fonctionnel")
            print("1 - Mode graphique, uniquement phase 1 de disponible")
            print("2 - Quitter le programme")
        elif(response == "2"):
            loop = False
        else:
            print("Réponse inconnue")
