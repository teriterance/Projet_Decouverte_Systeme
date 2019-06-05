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
    def __init__(self, latitude, longitude, lambda0):
        self.rayon_terre=6378.137#En km
        self.excentricite=0.0818192
        self.phi=latitude
        self.lambd=longitude
        self.lambd_0=lambda0
        
    def nhu():
        return 1/((1-(self.excentricite*np.sin(self.phi))**2)**(-2))
    def Var_A():
        return (self.lambd-self.lambd_0)*np.cos(self.phi)
    def Var_T():
        return (np.tan(self.phi))**2
    def Var_C():
        return ((self.excentricite)**2/(1-self.excentricite)**2)*((np.cos(self.phi))**2)
    def S():
        e=self.excentricite
        terme1=(1-((e)**2/4)-(3*(e)**4/64)-(5*(e)**6/256))*np.sin(self.phi)
        terme2=((3*(e)**2/8)+(3*(e)**4/32)+(45*(e)**6/1024))*np.sin(2*self.phi)
        terme3=((15*(e)**4/256)+(45*(e)**6/1024))*np.sin(4*self.phi)
        terme4=((35*(e)**6/3072))*np.sin(6*self.phi)
        solution= terme1-terme2+terme3-terme4
        return solution
