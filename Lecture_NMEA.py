# -*- coding: utf-8 -*-
"""
Created on Wed May 29 08:48:34 2019

@author: Cléris
"""

if __name__ == '__main__':
    
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
    Liste_position=[]
    for line in data:
        if line[0]=='$GPGGA':
            