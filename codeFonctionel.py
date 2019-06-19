from GPS import GPS
from projectionMercator import Projection_Mercator
import matplotlib.pyplot as plt
import numpy as np
import pyproj
from osgeo import osr
from osgeo import ogr
import gdal

#declaration des points de reference, 8000 et 9000
valVrai_9000 = [139.4655, 48.418407975, 4.474412007]
valVrai_8000 = [139.460, 48.418361635, 4.474421519]

#on effectue la conversion des donnees GPS vers des donnees wgs8
def convLambert(longitude, latitude):
    lam =  pyproj.Proj("+init=EPSG:2154")
    wgs8 =  pyproj.Proj("+init=EPSG:4326")
    return pyproj.transform(wgs8,lam, longitude, latitude)

gps = GPS("gstar")
gps.lectureFichier('ue24_9000_20190614_100000.txt')

#on charge l'image
x,y = convLambert(gps.Liste_valeurs[2][:], gps.Liste_valeurs[1][:])
print(x,y)
plt.scatter(x,y, marker='+')
plt.show()

im = gdal.Open('ensta_2015.jpg')
nx = im.RasterXSize
ny = im.RasterYSize
nb = im.RasterCount
image = np.zeros((ny,nx,nb))
image[:,:,0]=im.GetRasterBand(1).ReadAsArray()*255
image[:,:,1]=im.GetRasterBand(2).ReadAsArray()*255
image[:,:,2]=im.GetRasterBand(3).ReadAsArray()*255
plt.figure()
plt.xlim([500,1000])
plt.ylim([1200,800])
geo = im.GetGeoTransform()
origine = (geo[0], geo[3])  # origine de l'image 
print(origine)
taille_pixel = (geo[1], geo[5])
xpix = int((x[0] - origine[0]) / taille_pixel[0])
ypix = int((y[0] - origine[1]) / taille_pixel[1])
print(xpix, ypix)
plt.scatter(xpix, ypix)
image[0:100,0:100,:] = 0
plt.imshow(image)
plt.show()
plt.scatter(xpix+taille_pixel[0], ypix+taille_pixel[1])
plt.show()

"""
gps.acDonne()
#pour le point 9000
print(gps.calculFidelite(), "fidelite")
print(gps.calculPrecision(valVrai_9000), "Precision")
print(gps.calculJustesse(valVrai_9000), "justesse")
projection  = Projection_Mercator(4.474412007)
i = 0
altitude = np.zeros((1,10))
latitude = np.zeros((1,10))
longitude = np.zeros((1,10))
liste_abscisse=[]
liste_ordonnee=[]
gps =  GPS("gstar")
spacialRef = osr.SpatialReference()
spacialRef.ImportFromEPSG(2154)
i=0
while i <100000:
    [alti, lati, longi], nb_sat =gps.acDonneUnit()
    gps.save()
#    altitude[0,i]=alti
#    latitude[0,i]=lati
#    longi[0,i]=longi
#    x,y=projection.calcul(lati, longi)
#    liste_abscisse.append(x)
#    liste_ordonne.append(y)
    i+=1
    """