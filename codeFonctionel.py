from GPS import GPS
from projectionMercator import Projection_Mercator
import matplotlib.pyplot as plt
import numpy as np
import gdal

"""im = gdal.Open('ensta_2015.jpg')
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
plt.imshow(image)

valVrai_9000 = [139.4655, 48.418407975, 4.474412007]
valVrai_8000 = [139.460, 48.418361635, 4.474421519]
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
"""
gps =  GPS()


i=0
while i <10000:
    [alti, lati, longi], nb_sat =gps.acDonneUnit()
    gps.save()
#    altitude[0,i]=alti
#    latitude[0,i]=lati
#    longi[0,i]=longi
#    x,y=projection.calcul(lati, longi)
#    liste_abscisse.append(x)
#    liste_ordonne.append(y)
    i+=1
#plt.plot(liste_abscisse, liste_ordonne)
plt.show()