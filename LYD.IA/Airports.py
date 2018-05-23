# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:55:37 2018
@author: anthony.woznica

Absolutely ANY USE of the following functions REQUIRE CREDIT IN THE HEADER OF THE FILE (WOZNICA Anthony).
There are NO exceptions.

This file contains all databases methods used in the chatbot.
"""


import sqlite3
import sys

indb = r'Files/airports.dat'

try:
    with open(indb, "r") as f:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS airports(
             id INTEGER,
             name TEXT,
             city TEXT,
             country TEXT,
             short_name TEXT,
             ide TEXT,
             lat FLOAT,
             lng FLOAT,
             altitude INTEGER,
             open INTEGER,
             unknown TEXT,
             company TEXT,
             type TEXT,
             registered TEXT
        )
        """)
        
        for line in f.readlines():
            line = line[:-2]
            lineTab = line.split(',')
            for i in range(0, len(lineTab)):
                lineTab[i] = lineTab[i].strip()
            if(len(lineTab) == 15):
                lineTab.remove(lineTab[3])
            cursor.execute("""
            INSERT INTO airports(id, name, city, country, short_name, ide, lat, lng, altitude, open, unknown, company, type, registered) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", lineTab)
except:
    print("Unable to load " + indb)
    f.close()
    sys.exc_info()[0]
    sys.exit()
    
f.close()

def get_codes(city):
    """String -> List[String]
    Retourne la liste des aéroports présents dans la ville (city).
    """
    return [row[0] for row in cursor.execute("SELECT short_name FROM airports WHERE UPPER(city) = UPPER('"+city+"')") if len(row[0])==3]
