from GPS import GPS
from projectionMercator import Projection_Mercator
import matplotlib.pyplot as plt
import numpy as np

gps =  GPS()
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

while i < 10:
    [alti, lati, longi], nb_sat =gps.acDonneUnit()
    altitude[0,i]=alti
    latitude[0,i]=lati
    longi[0,i]=longi
    x,y=projection.calcul(lati, longi)
    liste_abscisse.append(x)
    liste_ordonne.append(y)
    i+=1
plt.plot(liste_abscisse, liste_ordonne)
plt.show()
