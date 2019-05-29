from threading import Timer
import time
import serial


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

#--- obligatoire pour rendre code exécutable ---
if __name__ == "__main__": # cette condition est vraie si le fichier est le programme exécuté
    main()# appelle la fonction principale