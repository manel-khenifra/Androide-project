from pyroborobo import Pyroborobo, Controller, CircleObject, SquareObject
import copy
from random import *

class Feuille(CircleObject):


    def __init__(self, id=-1, data={}):
        super().__init__(id,data)
        self.set_color(0, 255, 0)
        self.type = 4
        self.regrow_time = 50
        self.cur_regrow = 0
        self.data = data
        self.x = 0
        self.y = 0
        self.new_x = 0
        self.new_y = 0
        self.take = True
        
        #self.default_x = copy.copy(data["x"])
        #self.default_y = copy.copy(data["y"])
        self.rob = Pyroborobo.get() # Get pyroborobo singleton
        
        self.dropped_in_nest = False
        self.dropped = False
        self.nbRobot = 0 # nombre de robot qui l'ont transporté jusqu'a présent

    def reset(self):
        #self.show()
        #self.register()
        self.dropped_in_nest = False
        self.dropped = False
        self.cur_regrow = 0
        self.nbRobot = 0
        self.take = True



    def step(self):
        
        if self.dropped:
            self.cur_regrow -= 1
            if self.cur_regrow <= 0:
                self.hide()
                self.unregister()
                self.set_coordinates(self.new_x, self.new_y+30)
                self.x = self.new_x
                self.y = self.new_y+30
                self.register()
                self.show()
                self.cur_regrow = 0
                self.dropped = False
                self.take = True
        
        if self.dropped_in_nest:
            
            self.cur_regrow -= 1
            if self.cur_regrow <= 0:
                x = randint(100, 650)
                y = randint(120, 450) 
                self.hide();
                self.unregister();
                self.set_coordinates(x, y)
                b = self.can_register()
                while(b==False):
                      x = randint(100, 650)
                      y = randint(120, 450) 
                      self.set_coordinates(x, y)                      
                      b = self.can_register()
                self.x = x
                self.y = y
                self.register()
                self.show()
                self.dropped_in_nest = False
                self.take = True
                 
    def respawn(self, x, y):
        self.new_x = x
        self.new_y = y

    def is_walked(self, robid):
        for c in self.rob.controllers:
            if(c.get_id() == robid):
                if(c.getCanCollect() == True and c.getWantTake() and self.take == True):
                    c.setObjCollected(True)
                    c.setCanInstantDrop(True)
                    c.id_object_transported = self.id # on donne l'identifiant de l'objet au robot qui le transporte
                    if not (self.id in c.objects_transported):
                        c.objects_transported.append(self.id)
                    #self.nbRobot +=1 # elle a été pris par un robot supplémentaire
                    #self.cur_regrow = self.regrow_time
                    self.hide()
                    self.unregister()
                    self.take = False
                    break
                else:
                    pass
                    #print("non collecté")
        
    """def isTouched(self,robid) : 
        for c in self.rob.controllers:
            if(c.get_id() == robid):
                if(c.getCanCollect() == True and c.getWantTake()):
                    #print("Collected")
                    c.setObjCollected(True)
                    c.setCanInstantDrop(True)
                    c.id_object_transported= self.id # on donne l'identifiant de l'objet au robot qui le transporte
                    
                   # self.nbRobot +=1 # elle a été pris par un robot supplémentaire
                    self.triggered = True
                    self.cur_regrow = self.regrow_time
                    self.hide()
                    self.unregister()
                else : 
                    pass
                    #print("non collecté")"""



class BlockObject(SquareObject):
    def __init__(self, id=-1, data={}):
        super().__init__(id, data)
        self.type = -1

    def step(self):
        return

    def is_walked(self, id_):
        return

            
class SwitchObject(CircleObject):
    def __init__(self, id, data):
        CircleObject.__init__(self, id)  # Do not forget to call super constructor
        self.regrow_time = data['regrowTimeMax']
        self.cur_regrow = 0
        self.triggered = False
        self.gate_id = data['sendMessageTo']
        self.rob = Pyroborobo.get()  # Get pyroborobo singleton

    def reset(self):
        self.show()
        self.register()
        self.triggered = False
        self.cur_regrow = 0

    def step(self):
        if self.triggered:
            self.cur_regrow -= 1
            if self.cur_regrow <= 0 and self.can_register():
                self.show()
                self.register()
                self.triggered = False

    def is_walked(self, rob_id):
        self.triggered = True
        self.rob.objects[self.gate_id].open()
        self.cur_regrow = self.regrow_time
        self.hide()
        self.unregister()

    def inspect(self, prefix=""):
        return "I'm a switch!"

class UWallObject(SquareObject):
    def __init__(self, id, data):
        super().__init__(id)
        self.data = data
        self.unregister()
        if data["side"] == "left":
            self.solid_height = 100
            self.solid_width = 10
            self.soft_width = 0
            self.soft_height = 0
            self.set_coordinates(200, 300)
        elif data["side"] == "right":
            self.solid_height = 100
            self.solid_width = 10
            self.soft_width = 0
            self.soft_height = 0
            self.set_coordinates(300, 300)
        elif data["side"] == "bottom":
            self.solid_height = 10
            self.solid_width = 90
            self.soft_width = 0
            self.soft_height = 0
            self.set_coordinates(250, 345)
        self.register()

    def step(self):
        pass

    def inspect(self, prefix=""):
        return str(self.position)


class ResourceObject(CircleObject):
    def __init__(self, id_, data):
        CircleObject.__init__(self, id_)  # Do not forget to call super constructor
        self.regrow_time = 100
        self.cur_regrow = 0
        self.triggered = False
        self.rob = Pyroborobo.get()  # Get pyroborobo singleton

    def reset(self):
        self.show()
        self.register()
        self.triggered = False
        self.cur_regrow = 0

    def step(self):
        if self.triggered:
            self.cur_regrow -= 1
            if self.cur_regrow <= 0:
                self.show()
                self.register()
                self.triggered = False

    def is_walked(self, rob_id):
        self.triggered = True
        self.cur_regrow = self.regrow_time
        self.hide()
        self.unregister()


            

        
        
