#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 13:00:34 2021
@author: Damien
"""

from pyroborobo import  Controller
import numpy as np
from tools import evaluate_network
import random

nestX=370
nestY=800
Rayon_nid = 50
Xmin = 0
Xmax = (0-nestY)**2



class EvolController(Controller):

    def __init__(self, wm):
        Controller.__init__(self, wm)
        self.nb_hiddens = 14
        self.nb_zones=6
        
        self.wantDrop=False
        self.wantTake = False
        self.setObjCollected(False)
        self.setCanInstantDrop(False)
        
        #x = random.randint(250, 650)
        #y = random.randint(120, 650)
        #self.set_position(x,y)
    

        self.setIsObserved(False)
        
        self.weights = [np.random.normal(0, 1, (self.nb_sensors+ 4, self.nb_hiddens)),
                        np.random.normal(0, 1, (self.nb_hiddens, 4))]
        self.tot_weights = np.sum([np.prod(layer.shape) for layer in self.weights])
        self.zones=np.zeros(self.nb_zones)
        
        self.fitness = 0
        self.s = 0 # pour stocker la distance euclidienne
        
        self.objects_transported = []
        self.object_fitness = np.zeros(25)
        
        self.id_object_transported= 0 # pour savoir quel objet on transporte actuellement
        
        

    def get_random_weights(self):
        return np.random.normal(0, 1, (self.tot_weights))

    def get_tot_weights(self):
        return self.tot_weights 
    
    def dist_eucl(self,x,y):
       p =self.absolute_position
       return ( p[0]-x)**2  + (p[1]-y)**2
    
    def reset(self):
       #pass
       self.fitness = 0
       self.s = 0
       self.objects_transported = []
       self.id_object_transported= 0
       
       self.wantDrop=False
       self.setObjCollected(False)
       self.setCanInstantDrop(False)
       self.setIsObserved(False)
       self.wantTake = False


    def step(self):
        self.lookForFood()

        input = np.concatenate((self.get_all_distances(),[self.getIsObserved(),self.getObjCollected(),self.absolute_orientation]))

        out = np.clip(evaluate_network(input, self.weights), -1, 1)
        normalT = out[0]
        self.set_rotation(out[1])
        self.setWantDrope(out[2])#depot ou non d objet
        self.setWantTake(out[3])

        
        # Quand le robot est sur la pente 
        coeffSpeedVariation = 0.3 #pour l'instant pas variation
        p = self.absolute_position
        
        maxRampSpeed = 0.3;
        minRampSpeed = -0.3;
        
        orientation = self.absolute_orientation
        y = p[1]
        
        if (y > 450 and y < 700 and orientation < 0.0):#oriente vers le haut
        
                if(normalT > maxRampSpeed):
                     self.set_translation(maxRampSpeed)
                     
                elif(normalT < minRampSpeed):
                     self.set_translation(minRampSpeed)
                     
                else:
                     self.set_translation(min(1,normalT))
            
            
        elif (y > 450 and y < 700 and orientation >= 0.0):#oriente vers le bas
            if (normalT<= 0.9):
                normalT += 0.2
            elif (normalT >= -0.9):
                normalT -= 0.2;
            self.set_translation(min(1,normalT))
            
        else:
            
            self.set_translation(min(1,normalT))
            
        
        speed = self.translation
        rotspeed = np.abs(self.rotation)
        dists = np.asarray(self.get_all_distances())

        #l'agent a collecte un objet distance euclidienne au nid
        
        if self.getObjCollected():
            if(y>=nestY): # on est dans la zone du nid donc la distance euclidienne est de 1
                self.fitness += 0
                self.s+=0
            else: # Sinon distance euclidienne classique
                d = (((y-nestY)**2)-Xmin)/(Xmax-Xmin) # on normalise
                self.s += 1-d #nid
                self.fitness += 1-d
            
            
        # fitness avec distance au zone des feuilles
        """else :
            s = self.dist_eucl(nestX,0) #zone de recup des feuilles
            self.fitness += 1/max(1e-8,s)"""
        
        # fitness avec le nombre de fois qu'un objet a été transporté
        """
        if self.getObjCollected():
            nb_taken = Feuille(self.id_object).nbRobot
            self.fitness += 10*nb_taken
        """


    def get_flat_weights(self):
        all_layers = []
        for layer in self.weights:
            all_layers.append(layer.reshape(-1))
        flat_layers = np.concatenate(all_layers)
        assert (flat_layers.shape == (self.tot_weights,))
        return flat_layers

    
    def set_weights(self, weights):
        j = 0
        for i, elem in enumerate(self.weights):
            shape = elem.shape
            size = elem.size
            #self.weights[i] = np.array(elem).reshape(shape)
            self.weights[i] = np.array(weights[j:(j + size)]).reshape(shape)
            j += size
        # assert that we have consume all the weights needed
        assert (j == self.tot_weights)
        assert (j == len(weights))
        
    def lookForFood(self):
        camera_dist = self.get_all_distances()
        for i in range(len(camera_dist)):
            if camera_dist[i] < 1:  # if we see something
                if self.get_object_at(i) != -1:  
                    if self.get_object_instance_at(i).type != -1:
                        self.setIsObserved(True)
                        break


        
	# Fonctions de ramassage et dépôt d'objets
    
    def getWantDrope(self):
        return self.wantDrop
    
    
    def getWantTake(self):
        return self.wantTake
    
    def getCanCollect(self):
        return self.canCollect
    
    def getCanDropSlope(self):
        return self.canDropSlope
        
    def getCanDropNest(self):
        return self.canDropNest
      
    def getCanInstantDrop(self):
        return self.instantDrop
    
    def getObjCollected(self):
        return self.objCollected

    def getIsObserved(self):
        return self.objObserved
    
	# Fonction set
    
    def setWantDrope(self,c):
        self.wantDrop = c
        
    def setWantTake(self,c):
        self.wantTake = c
    
    def setCanCollect(self,c):
        self.canCollect = c
    
    def setCanDropSlope(self,c):
        self.canDropSlope = c
        
    def setCanDropNest(self,c):
         self.canDropNest = c
      
    def setCanInstantDrop(self,c):
        self.instantDrop = c
        
    def setIsObserved(self,c):
        self.objObserved = c
    

    def setObjCollected(self,c):
        self.objCollected = c
        if(c == True):
            #print("Can not collect anymore")
            self.setCanCollect(False)
            self.setIsObserved(False)
            self.setCanDropSlope(True)
            self.setCanDropNest(True)
            self.setCanInstantDrop(True)
        if (c == False):
            #print("Can recollect")
            self.setCanCollect(True)
            self.setCanDropSlope(False)
            self.setCanDropNest(False)
            self.setCanInstantDrop(False)
