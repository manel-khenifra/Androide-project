#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 00:57:55 2021
@author: Damien
"""
from pyroborobo import Pyroborobo, Controller, WorldObserver
from controllerEvol import EvolController
import numpy as np
from objects import SwitchObject, UWallObject, Feuille, BlockObject

from random import *


#Variables globales
#Zone de jeu
zoneCollectMin = 50
depotMin = 400
depotMax = 450
rampeYMin=450
rampeYMax=700
#nestX=370
nestY=800
Rayon_nid = 50
Xmin = 0
Xmax = (0-nestY)**2


arena = [
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

offset_x = 36
offset_y = 36
edge_width = 28
edge_height = 28





class WorldObserverEvol(WorldObserver):

    def __init__(self, world):
        super().__init__(world)
        self.rob = Pyroborobo.get()
        self.global_fit = 0
        self.pointCount = 0
        self.reference_function = 0
        self.next_id_obj = 8
        self.nb_objects = 25
        self.feuille = []
        
    def init_post(self):
        
        super().init_post()
        
        for i in range(len(arena)):
            for j in range(len(arena[0])):
                if arena[i][j] == 1:
                    block = BlockObject()
                    block = self.rob.add_object(block)
                    block.soft_width = 0
                    block.soft_height = 0
                    block.solid_width = edge_width
                    block.solid_height = edge_height
                    block.set_color(164, 128, 0)
                    block.set_coordinates(offset_x + j * edge_width, offset_y + i * edge_height)
                    retValue = block.can_register()
                    # print("Register block (",block.get_id(),") :", retValue)
                    block.register()
                    block.show()
        
        for i in range (self.nb_objects):
            obj = Feuille(self.next_id_obj)
            
            obj.hide()
            obj.unregister()

            x = randint(100, 650)
            y = randint(120, 450) 
            
            for f in self.feuille:
                p = f.position
                while (p[0] == x and p[1] == y):
                     x = randint(100, 650)
                     y = randint(120, 450)
                           
            
            obj.set_coordinates(x, y)
            b = obj.can_register()
            while(b==False):
                  x = randint(100, 650)
                  y = randint(120, 450) 
                  obj.set_coordinates(x, y)
                  b = obj.can_register()   
                  
            obj = self.rob.add_object(obj)
            obj.x = x
            obj.y = y
            obj.show()
            obj.register()
            self.next_id_obj += 1
            self.feuille.append(obj)

        for robot in self.rob.controllers:
            x = randint(100, 650)
            y = randint(700, 870)
            robot.set_position(x, y)
            
            


        arena_size = np.asarray(self.rob.arena_size)
        landmark = self.rob.add_landmark()
        landmark.radius = 20
        landmark.set_coordinates(370,nestY)
        landmark.show()
        
    def step_pre(self):
        super().step_pre()
        for c in self.rob.controllers:
            p = c.absolute_position
            x = p[0]
            y = p[1]
            
            """
            for obj in self.feuille:
                for id in c.objects_transported :
                    if (obj.id == id):
                         #p = obj.position
                         if (obj.dropped_in_nest == True):
                             d = 0
                         else :
                             d = (((obj.y-nestY)**2)-Xmin)/(Xmax-Xmin)
                         i = c.objects_transported.index(id)
                         c.object_fitness[i] = max(1-d, c.object_fitness[i])
                         
            c.fitness = np.sum(c.object_fitness)
            """             

            if(c.getCanInstantDrop()==True and c.getObjCollected()): # Si on a un objet on peut le lacher 

                ori = c.absolute_orientation
                
                # on est dans la zone du nid
                if(nestY <= y and c.getWantDrope()):
                        c.setObjCollected(False)
                        c.setCanInstantDrop(False)
                        for obj in self.feuille:
                            if (obj.id == c.id_object_transported):
                                #print("obj_id:", obj.id)
                                obj.dropped_in_nest = True 
                                obj.cur_regrow = obj.regrow_time
                         
                        #c.id_object = 0
                        c.fitness += 3500
                        c.fitness -= c.s
                        c.s = 0
                        self.reference_function += 1
                        c.id_object_transported=0
                
                # on est dans la zone de la pente
                elif(y>depotMin and y < depotMax and c.getWantDrope()):
                    p =c.absolute_position
                    #obj = Feuille(c.id_object_transported)
                    for obj in self.feuille:
                        if (obj.id == c.id_object_transported):
                            #print("obj_id:", obj.id)
                            obj.dropped_in_nest = True 
                            x = p[0]
                            y = 700
                            obj.hide()
                            obj.unregister()
                            obj.set_coordinates(x, y)
                            obj.x = x
                            obj.y = y
                            obj.register()
                            obj.show()
                            obj.take = True
                    c.s = 0
                    c.setObjCollected(False)
                    c.setCanInstantDrop(False)
                    c.id_object_transported=0
                             
                elif(c.getWantDrope()):
                    p =c.absolute_position
                    c.setObjCollected(False)
                    #obj = Feuille(c.id_object_transported)
                    for obj in self.feuille:
                        if (obj.id == c.id_object_transported):
                            #print("obj_id:", obj.id)
                            x = p[0]
                            y = p[1]
                            obj.dropped = True
                            obj.cur_regrow = obj.regrow_time
                            obj.respawn(x,y)                            
                            obj.take = True
                    c.s = 0
                    c.setObjCollected(False)
                    c.setCanInstantDrop(False)
                    c.id_object_transported=0
                    
                        
    def addPoint(self,p):
        self.pointCount+= p
   
        
    def step_post(self):
       # on récupère la liste des robots
       
       super().step_post()
       #for c in self.rob.controllers:
            #if c.getObjCollected():
                #self.global_fit+=1000
        # et augmenter global_fit ( de bcp ) en fonction du nb d'objet dans le nid
        
    def reset(self):
        
       self.global_fit = 0
       self.pointCount = 0
       self.reference_function = 0
       
                    
       for obj in self.feuille:
            x = randint(100, 650)
            y = randint(120, 450) 
            obj.hide()
            obj.unregister()
            
            obj.set_coordinates(x, y)
            
            
            b = obj.can_register()
            while(b==False):
                  x = randint(100, 650)
                  y = randint(120, 450) 
                  obj.set_coordinates(x, y)
                  b = obj.can_register()
            
            obj.x = x
            obj.y = y      
            obj.register()
            obj.show()
            obj.reset()

       for robot in self.rob.controllers:
            x = randint(100, 650)
            y = randint(700, 870)
            robot.set_position(x, y)
            
