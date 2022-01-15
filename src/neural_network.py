import numpy as np 
class NeuronNetworkOneHiddenLayer:
    def __init__(self,nb_x,nb_h,nb_y):
        """nb_x number of inputs
        nb_h number of hidden neurons
        nb_y number of output"""
        self.parameters = self.init_random_parameters(nb_x,nb_h,nb_y)

    def init_random_parameters(self,nb_x,nb_h,nb_y):
        w1=np.random.rand(nb_h,nb_x)
        b1=np.random.rand(nb_h,1)
        w2=np.random.rand(nb_y,nb_h)
        b2=np.random.rand(nb_y,1)
        parameters = {
            "w1" : w1,
            "b1" : b1,
            "w2": w2,
            "b2": b2
            }
        return parameters
            
    def get_parameters(self):
        return self.parameters
    
    #to compute intermediate neurons values
    def compute_a_values(self,x,w,b):
        z = w@x+b
        return np.tanh(z)

    #we could use this but the teacher asked for tanh function instead
    def sigmoid(self,x):
        return 1/(1 + np.exp(-x)) 

    def compute_network_response(self,x):
        """return an numpy array corresponding to the column vector response of the network to the input x"""
        tmp = self.compute_a_values(x,self.parameters.get("w1"),self.parameters.get("b1"))
        return self.compute_a_values(tmp,self.parameters.get("w2"),self.parameters.get("b2"))


#example for 8 input (sensors), 4 hidden neurons and 2 return values (orientation, translation). All of this is arbitrary.
n_n= NeuronNetworkOneHiddenLayer(8,4,2)
param = n_n.get_parameters()
x=np.random.rand(8,1)
print("the values of the hidden layers neurons are:") #this is just for testing purposes, don't use this method
print(n_n.compute_a_values(x,param.get("w1"),param.get("b1")))
print("the neuron network response is:")
print(n_n.compute_network_response(x)) # this is THE response method, not compute_a_values

