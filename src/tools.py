#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 13:02:00 2021
@author: Damien
"""
#set of methods used for learning with neuron networks

import numpy as np
from pyroborobo import Pyroborobo
import scipy
import scipy.stats
from scipy.stats import rankdata
import pickle
import os.path


def evaluate_network(input_, network):
    out = np.concatenate([[1], input_])
    for elem in network[:-1]:
        out = np.tanh(out @ elem)
    out = out @ network[-1]  # linear output for last layer    
    out[-2:] = np.where(np.tanh(out[-2:])>0,1,0)
    return out


def get_weights(rob: Pyroborobo):
    weights = []
    for ctl in rob.controllers:
        weights.append(ctl.get_flat_weights())
    return weights


def get_fitnesses_ded(rob: Pyroborobo):
    fitnesses = []
    #for observer in rob.agent_observers:
    for ctl in rob.controllers:
        fitnesses.append(ctl.fitness)
    return fitnesses

def get_global_fitnesses(rob: Pyroborobo):
    global_fitnesses = rob.world_observer.global_fit
    return global_fitnesses


def fitprop(weights, fitnesses,sigma=0.01):
    adjust_fit = rankdata(fitnesses)
    # adjust_fit = np.clip(fitnesses, 0.00001, None)
    normfit = adjust_fit / np.sum(adjust_fit)
    # select
    new_weights_i = np.random.choice(len(weights), len(weights), replace=True, p=normfit)
    new_weights = np.asarray(weights)[new_weights_i]
    # mutate
    new_weights_mutate = np.random.normal(new_weights, sigma)
    return new_weights_mutate

def mu_comma_lambda_nextgen(weights, fitnesses,mu,lambda_,sigma=0.01):
    # select
    index_mu_best=np.argsort(-np.array(fitnesses))[:mu]
   # print("meilleur index :", index_mu_best)
    bestParents = np.asarray(weights)[index_mu_best]
   # print("meilleur parents :", bestParents)
    # mutate
    new_weights_mutate = np.array([np.random.normal(bestParents[np.random.randint(mu)],sigma) for i in range(lambda_)])
    #print("taille:",len(new_weights_mutate))
    return new_weights_mutate

def apply_weights(rob, weights):
    for ctl, weight in zip(rob.controllers, weights):
        ctl.set_weights(weight)

def apply_weight_clonal(rob, weight):
    for ctl in rob.controllers:
        ctl.set_weights(weight)
        
def init_random_gen(rob,lambda_):
    ctl = rob.controllers[0]
    res=np.zeros((lambda_,ctl.get_tot_weights()))
    for i in range(lambda_):
        res[i,:]=ctl.get_random_weights()
    return res
        
def reset_agent_observers(rob):
    for obs in rob.agent_observers:
        obs.reset()
        
def reset_agent_controllers(rob):
     for ctl in rob.controllers:
        ctl.reset()

def reset_world_observer(rob):
     rob.world_observer.reset()
     
def reset_object(rob):
    for obj in rob.objects:
        obj.hide()
        obj.unregister()
    

def get_reference_function(rob: Pyroborobo):
    reference_function  = rob.world_observer.reference_function 
    return reference_function

def saveList(l,fileName):
    with open(fileName, "wb") as fp:   #Pickling
        pickle.dump(l, fp)
        fp.close()

def clearFile(fileName):
    with open(fileName, "wb") as fp:   # Unpickling
        fp.truncate(0)
        fp.close()
        
def loadList(fileName):
    with open(fileName, "rb") as fp:   # Unpickling
        res = pickle.load(fp)
        fp.close()
    return res

def updateHoF(weights, fitnesses):
    """
    mets a jour le HoF si un genome a eu un meilleur score que le precedent meilleur ( creer un fichier HoF sinon)
    je pense qu'il est plus coherent de d'utiliser la fitness de REFERENCE ici en fitnesses
    
    """
    bestIndex = np.argsort(fitnesses)[-1]
    bestWeights = weights[bestIndex]
    assert fitnesses[bestIndex]==np.max(fitnesses)
    if os.path.isfile("HallOfFame"):
        #le fichier existe deja
        if fitnesses[bestIndex]>loadList("HallOfFame")[0]:
            #print("Le HoF est maj")
            clearFile("HallOfFame")
            scoreAndWeights=[fitnesses[bestIndex],bestWeights]
            saveList(scoreAndWeights,"HallOfFame")
    else:
        #le fichier n'existe pas encore
        scoreAndWeights=[fitnesses[bestIndex],bestWeights]
        saveList(scoreAndWeights,"HallOfFame")

def apply_HoF(rob:Pyroborobo):
    hoF=loadList("HallOfFame")
    bestWeights=np.array(hoF[1])
    apply_weight_clonal(rob,bestWeights)

def init_from_file(rob,fileName,lambda_):
    ctl = rob.controllers[0]
    res=np.zeros((lambda_,ctl.get_tot_weights()))
    genome=loadList(fileName)[1]
    assert ctl.get_tot_weights()==len(genome)
    for i in range(lambda_):
        res[i,:]=genome[:]
    return res
