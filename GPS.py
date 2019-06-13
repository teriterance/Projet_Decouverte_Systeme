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
        self.dernierevaleur = [0, 0, 0]#les derniere valeur en altitude latitude longitude
        self.valeursMoyenne = 0
        self.nb_satellite = 0
        self.Liste_valeurs = [[],[],[]]# en ordre , l'altitude, la latitude et la longitude 
    
    def save(self)
        l1=self.Liste_valeurs[0]
        

    def retirerVal(self):
        self.Liste_valeurs[0].pop(0)
        self.Liste_valeurs[1].pop(0)
        self.Liste_valeurs[2].pop(0)
    
    def ajouterVal(self, altitude, latitude, longitude):
        #permet d'ajouter une valeur ou un groupe de valeur a la liste de nos valeurs 
        if len(self.Liste_valeurs[0]) > 100: 
            #on limite la taille a 30 valeur
            self.retirerVal()
        self.dernierevaleur  = [altitude, latitude, longitude]
        self.Liste_valeurs[0].append(altitude)        
        self.Liste_valeurs[1].append(latitude)
        self.Liste_valeurs[2].append(longitude)


    def lectureSerie(self): 
        # fonction de lecture série
        return self.serialPort.readline().decode("ascii")# (auto)-rappelle la fonction dans 100ms

    def calculJustesse(self, Valeur_vraie):
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
        self.e_precision=[((self.e_justesse[0]**2)+(self.e_fidelite[0])**2)**(1/2), ((self.e_justesse[1]**2)+(self.e_fidelite[1])**2)**(1/2), ((self.e_justesse[2]**2)+(self.e_fidelite[2])**2)**(1/2)] 
        return self.e_precision

    def convMinutetoDegreLat(self,latitude):
        sortie = 0
        sortie = sortie+ int(latitude[0:2])
        sortie = sortie+ (1/60)*float(latitude[2:8])
        return sortie
    
    def convMinutetoDegreLong(self, longitude):
        sortie = 0
        sortie = sortie+ int(longitude[0:3])
        sortie = sortie+ (1/60)*float(longitude[3:9])
        return sortie

    def acDonne(self):
        self.nombreMesure = 0
        while self.nombreMesure < 20:
            line = self.lectureSerie().split(',')
            print(self.dernierevaleur, self.nombreMesure, self.nb_satellite)
            if  line[6]!=0 and line[0]=='$GPGGA':#On regarde la ligne contenant ttes les infos utiles
                line[2]
                self.ajouterVal(float(line[9]), self.convMinutetoDegreLat(line[2]), self.convMinutetoDegreLong(line[4]))
                self.nb_satellite = int(line[7])
                self.nombreMesure = self.nombreMesure + 1
            #elif line[6]!=0 and line[0]=='$GPRMC':#On regarde la ligne recommended minimum specific GPS/Transit data
             #   self.ajouterVal(float(line[9]), self.convMinutetoDegreLat(line[2]), self.convMinutetoDegreLong(line[4]))
             #   self.nb_satellite = int(line[7])
              #  self.nombreMesure = self.nombreMesure + 1
    
    def acDonneUnit(self):
        line = self.lectureSerie().split(',')
        print(self.dernierevaleur, self.nb_satellite)
        if  line[6]!=0 and line[0]=='$GPGGA':#On regarde la ligne contenant ttes les infos utiles
            self.ajouterVal(float(line[9]), self.convMinutetoDegreLat(line[2]), self.convMinutetoDegreLong(line[4]))
            self.nb_satellite = int(line[7])
        return self.dernierevaleur, self.nb_satellite
    
    def lectureReel(self):
        line = self.lectureSerie().split(',')
        return float(line[9]), float(line[2]), float(line[4])

if __name__ == "__main__":
    g = GPS()
    g.acDonne()
    print(g.calculFidelite())
