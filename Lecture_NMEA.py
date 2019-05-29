
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 08:48:34 2019
@author: Cléris
"""
def lecturefichier():    
    #-------Ouverture et création d'une liste data----
    #-------------contenant les infos-------------
    in_file = open('data_uv24.nmea', 'r')
    data = []
    for line in in_file:
        data_txt = line.split(',')
        try:
            datal = [str(x) for x in data_txt]
            data.append(datal)
        except Exception:
            print("Données non conformes : ", line)
    in_file.close()
    #-------------Analyse des données GPS------------
    Liste_time_pos=[]
    for line in data:#on parcours toutes les lignes du fichier
        if line[0]=='$GPGGA':#On regarde la ligne contenant ttes les infos utiles
            Ligne=[]#On crée une liste contenant les infos temps et position
            Ligne.append('Temps:')
            Ligne.append(line[1])
            Ligne.append('Latitude:')
            Ligne.append(line[2])
            Ligne.append('Longitude:')
            Ligne.append(line[4])
            Ligne.append('Altitude:')
            Ligne.append(line[9])
            Ligne.append('Nb satellites:')
            Ligne.append(line[7])
            Liste_time_pos.append(Ligne)
    print(Liste_time_pos)
