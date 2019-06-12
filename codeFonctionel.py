from GPS import GPS
from projectionMercator import Projection_Mercator
import matplotlib.pyplot as plt
import numpy as np

gps =  GPS()
valVrai_9000 = [139.4655, 48.418407975, 4.474412007]
valVrai_8000 = [139.460, 48.418361635, 4.4744215119]
gps.acDonne()
#pour le point 9000
print(gps.calculFidelite(), "fidelite")
print(gps.calculPrecision(valVrai_9000), "Precision")
print(gps.calculJustesse(valVrai_9000), "justesse")
projection  = Projection_Mercator(4.474412007)
i = 0
altitude = np.zeros([1,10])
latitude = np.zeros([1,10])
longitude = np.zeros([1,10])
while i < 10:
    [altitude[i], latitude[i], longitude[i]], nb_sat =gps.acDonneUnit()
plt.plot()
