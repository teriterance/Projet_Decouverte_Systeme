import time
import serial
import numpy as np
import matplotlib.pyplot as plt

class GPS(object):
    def __init__(self, nom, adres_gps = '/dev/ttyUSB0', baudrate = 4800):
        '''La variable adres_gps est une adresse de port serie'''
        self.serialPort = serial.Serial(adres_gps, baudrate, parity= serial.PARITY_EVEN, rtscts=1)
        self.nombreMesure = 0
        self.moyene = [0,0,0]
        self.precision = [0,0,0]
        self.fidelite = [0,0,0]
        self.e_justesse = [0,0,0]
        self.dernierevaleur = [0, 0, 0]#les derniere valeur en altitude latitude longitude, 
        # C'est une liste que l'on mets à jour à chaque fois dans nos méthodes
        self.valeursMoyenne = 0
        self.nb_satellite = 0
        self.Liste_valeurs = [[],[],[]]# en ordre , l'altitude, la latitude et la longitude 
        self.f = open("mesuresave"+nom+".txt", "a")
        self.f2 = open("mesuresat"+nom+".txt", "a")
        

    def retirerVal(self):
        """Méthode permettant de retirer des valeurs de latitude, log et altitude
        lorsque la taille de Liste_valeurs atteint sa taille maximale
        On utilise cette méthode dans l'autre" méthode ajouterVal"""
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
        """fonction de lecture série, elle permet de retourner les trames NMEA"""
        return self.serialPort.readline().decode("ascii")# (auto)-rappelle la fonction dans 100ms
    
    
    
#---------------------------Méthodes servant à calculer les justesses, fidélité et precision des GPS -----------------
    
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
    

#--------------------On arrive aux méthodes générales rassemblant toutes les méthodes précédentes-----------------    
    
    def acDonne(self):
        self.nombreMesure = 0
        while self.nombreMesure < 20:
            line = self.lectureSerie().split(',')
            print(self.dernierevaleur, self.nombreMesure, self.nb_satellite)
            if len(line) > 6:
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
        """ méthode qui retourne la liste des dernières valeurs de longitude
        latitude et altitude ainsi que le nombre de satellites en temps réels""""
        line = self.lectureSerie().split(',')
        print(self.dernierevaleur, self.nb_satellite)
        if len(line) > 13:
            print(line)
            """On suprime les cas ou il n'y a rien entre les virgules qui nous donne une taille de ligne inferieure a 6"""
            if  line[6]!=0 and line[0]=='$GPGGA':#On regarde la ligne contenant ttes les infos utiles
                self.ajouterVal(float(line[9]), self.convMinutetoDegreLat(line[2]), self.convMinutetoDegreLong(line[4]))
                self.nb_satellite = int(line[7])
        return self.dernierevaleur, self.nb_satellite   
    
    
    
    #----------------Méthodes permettant de tracer la constellationn des satellites ---------
    
    def GPSGraphPrep(self,a):
        """"Méthode permettant de stocker les 20 élévations et azimuts d'un satellite
        de numéro "a" au cour du temps"""
        self.nombreMesure = 0
        GPSe=[]
        GPSa=[]
        GPSa_rad = []
        while self.nombreMesure < 20:# on enregistre que 20 mesures de position de satellites
            line = self.lectureSerie().split(',')
            if line[0]=='$GPGSV':
                if line[4] == a:
                    GPSe.append(5)
                    GPSa.append(6)
                if line[8] == a:
                    GPSe.append(9)
                    GPSa.append(10)
                if line[12] == a:
                    GPSe.append(13)
                    GPSa.append(14)
                if line[16] == a:
                    GPSe.append(17)
                    GPSa.append(18)
                self.nombreMesure+=1
        for i in GPSa:
            GPSa_rad.append(float(i) * np.pi / 180.0)
        return(GPSe,GPSa_rad)

    def GraphGPS(self):
        """"Méthode traçant les suivis au cours du temps des positions des 
        satellites dans le ciel"""
        liste=range(30) # On parcours tous les numéros de satellites  
        for i in liste:
            liste_e, liste_a = self.GPSGraphPrep(i)
            if liste_e==[]:
                print("satellite ",i," non detecté")
            else:
                ax = plt.plot(polar=True)
                ax.set_theta_zero_location('N')
                ax.set_theta_direction(-1)
                ax.set_rmax(90)
                ax.grid(True)
                ax.scatter(liste_a, liste_e, color='r', s=10, label=str(i))
                plt.show()

                
#--------- Méthodes sauvegardant dans des fichiers textes les différentes trames NMEA------------
                
    def save(self):
        """Méthodes sauvegardant dans des fichiers textes les différentes trames NMEA
        On stocke dans deux fichiers différents les trames concernant les positions des satellites
        et les trames concernant les positions du GPS"""
        line = self.lectureSerie()
        l = line.split(',')
        if len(l) > 13:
            if l[0]=='$GPGSV':#On regarde la ligne contenant les infos sur position Sat
                self.f2.write(line)
            elif l[0]=='$GPGGA':#On regarde la ligne contenant ttes les infos utiles
                if l[6]!=0:
                    self.f.write(line)

    
    def lectureReel(self):
        line = self.lectureSerie().split(',')
        return float(line[9]), float(line[2]), float(line[4])

if __name__ == "__main__":
    g = GPS()
    g.acDonne()
    print(g.calculFidelite())
