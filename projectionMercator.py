# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 09:06:43 2019
@author: Cléris
"""
#

import numpy as np

#Lien bibliographie:
#https://fr.wikipedia.org/wiki/Transverse_universelle_de_Mercator 

class Projection_Mercator():
    
    def __init__(self,latitude, longitude, lambda0):
        self.rayon_terre=6378.137#En km
        self.excentricite=0.0818192
        self.phi= 0
        self.lambd= 0
        self.lambd_0=lambda0
        self.k0=0.996
    
    def nhu(self):
        return 1/((1-(self.excentricite*np.sin(self.phi))**2)**(-2))
    
    def Var_A(self):
        return (self.lambd-self.lambd_0)*np.cos(self.phi)
    
    def Var_T(self):
        return (np.tan(self.phi))**2
    
    def Var_C(self):
        return ((self.excentricite)**2/(1-self.excentricite)**2)*((np.cos(self.phi))**2)
    
    def S(self):
        e=self.excentricite
        terme1=(1-((e)**2/4)-(3*(e)**4/64)-(5*(e)**6/256))*np.sin(self.phi)
        terme2=((3*(e)**2/8)+(3*(e)**4/32)+(45*(e)**6/1024))*np.sin(2*self.phi)
        terme3=((15*(e)**4/256)+(45*(e)**6/1024))*np.sin(4*self.phi)
        terme4=((35*(e)**6/3072))*np.sin(6*self.phi)
        solution= terme1-terme2+terme3-terme4
        return solution

    def abscisse(self):
        a=self.rayon_terre
        k0=self.k0
        A=self.Var_A()
        T=self.Var_T()
        C=self.Var_C()
        nhu=self.nhu()
        terme1=A+(1-T+C)*(A**3)/6
        terme2=(5-18*T+T**2)*(A**5)/120
        E=500+k0*a*nhu*(terme1+terme2)
        return E

    def ordonne(self):
        a=self.rayon_terre
        k0=self.k0
        A=self.Var_A()
        T=self.Var_T()
        C=self.Var_C()
        nhu=self.nhu()
        S=self.S()
        phi=self.phi
        terme1=(A**2/2)+(5-T+9*C+4*C**2)*(A**4/24)
        terme2=(61-58*T+T**2)*(A**6/720)
        N=k0*a*(S+nhu*np.tan(phi)*(terme1+terme2))
        return N
    
    def calcul(self, latitude, longitude):
        """en plus de calcul des coordonee, il permet de mettre a jour la latitude et la longitude"""
        self.phi= latitude
        self.lambd= longitude
        return self.abscisse(), self.ordonne()

