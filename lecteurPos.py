from threading import Timer
import time
import serial
import numpy as np

# fonction principale
def main():
    global serialPort
    serialPort=serial.Serial('/dev/ttyUSB0', 4800, parity= serial.PARITY_EVEN, rtscts=1)
    Timer(1, lectureSerie).start() # 1er appel de la fonction dans 1 seconde
    while True:
    #for i in range(50): # saisie en boucle
        lectureSerie()
        time.sleep(0.5)

def lectureSerie(): # fonction de lecture série
    while serialPort.inWaiting():
        print (serialPort.readline().decode("ascii")), Timer(0.1, lectureSerie).start() # (auto)-rappelle la fonction dans 100ms
        
        
def collecte_data():
    data=[],Latitude=[],Longitude=[],Altitude=[]
    while serialPort.inWaiting():
        line=[]
        line.append(serialPort.readline().decode("ascii").split(','))
        if line[0]=='$GPGGA' and line[6]!=0:#On regarde la ligne contenant ttes les infos utiles
            Ligne=[]#On crée une liste contenant les infos temps et position
            Ligne.append('Temps:')
            Ligne.append(line[1])
            Ligne.append('Latitude:')
            Latitude.append(line[2])
            Ligne.append(line[2])
            Ligne.append('Longitude:')
            Longitude.append(line[4])
            Ligne.append(line[4])
            Ligne.append('Altitude:')
            Altitude.append(line[9])
            Ligne.append(line[9])
            Ligne.append('Nb satellites:')
            Ligne.append(line[7])
            data.append(Ligne)
    #return Latitude, Longitude, Altitude
    print(data)
    
def justesse(Liste_valeurs, Valeur_vraie):
    m=sum(Liste_valeurs, 0.0) / len(Liste_valeurs)
    e_justesse=abs(m-Valeur_vraie)
    return e_justesse
def fidelite(Liste_valeurs):
    return np.std(Liste_valeurs)
def precision(Liste_valeurs, Valeur_vraie):
    e_justesse=justesse(Liste_valeurs, Valeur_vraie)
    e_fidelite=fidelite(Liste_valeurs)
    e_precision=((e_justesse**2)+(e_fidelite)**2)**(-2)
    return e_precision

#--- obligatoire pour rendre code exécutable ---
if __name__ == "__main__": # cette condition est vraie si le fichier est le programme exécuté
    main()# appelle la fonction principale
