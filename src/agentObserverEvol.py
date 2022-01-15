
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 15:02:16 2021
@author: Damien
"""
from pyroborobo import  AgentObserver

import numpy as np

class EvolObserver(AgentObserver):


    def __init__(self, wm):
        super().__init__(wm)
        self.fitness = 0

    def reset(self):
        self.fitness = 0

    def step_post(self):
        speed = self.controller.translation
        rotspeed = np.abs(self.controller.rotation)
        dists = np.asarray(self.controller.get_all_distances())
        fitdelta = 5 * speed + np.min(dists) + 4 * np.exp(-10 * rotspeed)
        """if np.random.rand() < 0.0001:
            print(speed, rotspeed, dists)
            print(fitdelta)"""
        self.fitness += fitdelta
        #l'agent a collecte un objet
        if self.controller.getObjCollected(): 
            self.fitness+=10000
        # si l'agent est au niveau de la pente et a un objet sa fitness augmente si il le lache
        if (self.controller.getWantDrope() and self.controller.getCanDropSlope()) :
            self.fitness+=2000
        
        


