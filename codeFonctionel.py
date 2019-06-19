from GPS import GPS
from projectionMercator import Projection_Mercator
import matplotlib.pyplot as plt
import numpy as np
import pyproj
from osgeo import osr
from osgeo import ogr
import gdal
from affichagetempreel import Visualiseur

#declaration des points de reference, 8000 et 9000
valVrai_9000 = [139.4655, 48.418407975, 4.474412007]
valVrai_8000 = [139.460, 48.418361635, 4.474421519]

#on effectue la conversion des donnees GPS vers des donnees wgs8
def convLambert(longitude, latitude):
    lam =  pyproj.Proj("+init=EPSG:2154")
    wgs8 =  pyproj.Proj("+init=EPSG:4326")
    return pyproj.transform(wgs8,lam, longitude, latitude)

#creation du gps et initialisation de son nom qui permet de definire le fichier a gerer
def acFichier(file = 'ue24_9000_20190614_100000.txt'):
    gps = GPS("gstar")
    gps.lectureFichier('file')
    af = Visualiseur('ensta_2015.jpg')
    af.positionPix(gps.Liste_valeurs[1][:], gps.dernierevaleur[2][:])

def acDeplacement():
    gps = GPS("gstar")
    af = Visualiseur('ensta_2015.jpg')
    while True:
        gps.acDonneUnit()
        af.positionPix(gps.dernierevaleur[1], gps.dernierevaleur[2])

if __name__ == "__main__":
    acDeplacement()
    