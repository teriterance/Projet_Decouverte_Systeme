import time
import serial
import numpy as np

class GPS(object):
    def __init__(self, adres_gps = '/dev/ttyUSB0', baudrate = 4800):
        '''La variable adres_gps est une adresse de prot serie'''
        self.serialPort = serial.Serial(adres_gps, baudrate, parity= serial.PARITY_EVEN, rtscts=1)
        self.nombreMesure = 0
        self.moyene = [0,0,0]
        self.precision = [0,0,0]
        self.fidelite = [0,0,0]
        self.e_justesse = [0,0,0]
        self.dernierevaleur = [0, 0, 0]#les derniere valeur en altitude longitude altitude
        self.valeursMoyenne = 0
        self.nb_satellite = 0
        self.Liste_valeurs = [[],[],[]]# en ordre , l'altitude, la longitude et la latitude 

    def retirerVal(self):
        self.Liste_valeurs[0].pop(0)
        self.Liste_valeurs[1].pop(0)
        self.Liste_valeurs[2].pop(0)
    
    def ajouterVal(self, altitude, latitude, longitude):
        #permet d'ajouter une valeur ou un groupe de valeur a la liste de nos valeurs 
        if len(self.Liste_valeurs[0]) > 100: 
            #on limite la taille a 30 valeur
            self.retirerVal()
        self.dernierevaleur  = [altitude, longitude, latitude]
        self.Liste_valeurs[0].append(altitude)
        self.Liste_valeurs[1].append(longitude)
        self.Liste_valeurs[2].append(latitude)

    def lectureSerie(self): 
        # fonction de lecture série
        return self.serialPort.readline().decode("ascii")# (auto)-rappelle la fonction dans 100ms

    def calculJustesse(self, Valeurs_vraies):
        #il calcule la justesse, il attend la valeur vraie, celle du proflex 
        self.moyene = [sum(self.Liste_valeurs[0] , 0.0) / len(self.Liste_valeurs[0]), sum(self.Liste_valeurs[1] , 0.0) / len(self.Liste_valeurs[1]),sum(self.Liste_valeurs[2] , 0.0) / len(self.Liste_valeurs[2])]
        self.e_justesse = [abs(self.moyene[0]-Valeur_vraie[0]),abs(self.moyene[1]-Valeur_vraie[1]),abs(self.moyene[2]-Valeur_vraie[2])]
        return self.e_justesse

    def calculFidelite(self):
        #il calcule la fidelite
        self.fidelite = [np.std(self.Liste_valeurs[0]), np.std(self.Liste_valeurs[1]), np.std(self.Liste_valeurs[2])]
        return self.fidelite

    def calculPrecision(self,Valeur_vraie):
        #il calcule la precision
        self.e_justesse= self.calculJustesse(Valeur_vraie)
        self.e_fidelite= self.calculFidelite()
        self.e_precision=[((self.e_justesse[0]**2)+(self.e_fidelite[0])**2)**(-2), ((self.e_justesse[1]**2)+(self.e_fidelite[1])**2)**(-2), ((self.e_justesse[2]**2)+(self.e_fidelite[2])**2)**(-2)] 
        return self.e_precision
    
    def acDonne(self):
        while self.nombreMesure < 100:
            line = self.lectureSerie().split(',')
            print(self.dernierevaleur, self.nombreMesure, self.nb_satellite)
            if  line[6]!=0 and line[0]=='$GPGGA':#On regarde la ligne contenant ttes les infos utiles
                self.ajouterVal(float(line[9]), float(line[2]), float(line[4]))
                self.nb_satellite = int(line[7])
                self.nombreMesure = self.nombreMesure + 1
    
    def lectureReel(self):
        line = self.lectureSerie().split(',')
        return float(line[9]), float(line[2]), float(line[4])

if __name__ == "__main__":
    g = GPS()
    g.acDonne()
    print(g.calculFidelite())
