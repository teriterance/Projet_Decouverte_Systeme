from GPS import GPS
import matplotlib.pyplot as plt
import numpy as np
import pyproj
from osgeo import osr
from osgeo import ogr
import gdal

class Visualiseur:
    def __init__(self, image):
        """cette fonciton attend en entree l'image sur la quel sera representee le graphique"""
        plt.figure(1)
        plt.ion()
        self.im = gdal.Open(image)
        nx = self.im.RasterXSize
        ny = self.im.RasterYSize
        nb = self.im.RasterCount
        self.image = np.zeros((ny,nx,nb))
        self.image[:,:,0]=self.im.GetRasterBand(1).ReadAsArray()*255
        self.image[:,:,1]=self.im.GetRasterBand(2).ReadAsArray()*255
        self.image[:,:,2]=self.im.GetRasterBand(3).ReadAsArray()*255
        geo = self.im.GetGeoTransform()
        self.origine = (geo[0], geo[3])  # origine de l'image 
        self.limitesXY = [[500,1000], [1200,800]]
        plt.xlim(self.limitesXY[0])
        plt.ylim(self.limitesXY[1])
        plt.imshow(self.image)
    
    def convLambert(self, longitude, latitude):
        """"Projection via lambert"""
        lam =  pyproj.Proj("+init=EPSG:2154")
        wgs8 =  pyproj.Proj("+init=EPSG:4326")
        return pyproj.transform(wgs8,lam, longitude, latitude)

    def affichepointsurimage(self, xpix, ypix):
        """on ajoute sur l'image"""
        print(xpix, ypix)
        plt.scatter(xpix,  ypix, s= 1,c='r')
        plt.show()
        plt.pause(0.01)

    def positionPix(self, lat, lon):
        """On obtient ici la position d'un pixel sur l'image"""
        x, y = self.convLambert(lon, lat)
        geo = self.im.GetGeoTransform()
        origine = (geo[0], geo[3])  # origine de l'image 
        taille_pixel = (geo[1], geo[5])
        print(x,y)
        xpix = int((x - origine[0]) / taille_pixel[0])
        ypix = int((y - origine[1]) / taille_pixel[1])
        self.affichepointsurimage(xpix, ypix)

    def positionPixliste(self, listeLat, listeLon):
        """On obtient ici l'affichage d'un certain nombre de lieux sur l'image"""
        geo = self.im.GetGeoTransform()
        origine = (geo[0], geo[3])  # origine de l'image 
        taille_pixel = (geo[1], geo[5])
        for i in range(len(lat)):
            for i in range(listeLat):
                x, y = self.convLambert(lon, lat)
                xpix = int((x - origine[0]) / taille_pixel[0])
                ypix = int((y - origine[1]) / taille_pixel[1])
                # pause de 0.5 s
                plt.pause(0.5)
                plt.scatter(xpix, ypix,s = 1, c ='r')