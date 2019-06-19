from GPS import GPS
import matplotlib.pyplot as plt
import numpy as np
import pyproj
from osgeo import osr
from osgeo import ogr
import gdal

class visualiseur():
    def __init(self, image):
        """cette fonciton attend en entree l'image sur la quel sera representee le graphique"""
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
    
    def convLambert(self, longitude, latitude):
        lam =  pyproj.Proj("+init=EPSG:2154")
        wgs8 =  pyproj.Proj("+init=EPSG:4326")
        return pyproj.transform(wgs8,lam, longitude, latitude)

    def affichepointsurimage(self, xpix, ypix):
        """on ajoute sur l'image"""
        plt.scatter(xpix, ypix)

    def positionPix(self, lat, lon):
    """On obtient ici la position d'un pixel sur l'image"""
        x, y = self.convLambert(lon, lat)
        geo = self.im.GetGeoTransform()
        origine = (geo[0], geo[3])  # origine de l'image 
        taille_pixel = (geo[1], geo[5])
        xpix = int((x[0] - origine[0]) / taille_pixel[0])
        ypix = int((y[0] - origine[1]) / taille_pixel[1])
        self.image[xpix, ypix, :] = 255

    
