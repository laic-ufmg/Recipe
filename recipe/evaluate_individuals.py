# -*- coding: utf-8 -*-

"""
Copyright 2016 Walter José and Alex de Sá

This file is part of the RECIPE Algorithm.

The RECIPE is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

RECIPE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. See http://www.gnu.org/licenses/.

"""

import warnings

from sklearn.preprocessing import LabelEncoder

from pebble import concurrent
from concurrent.futures import TimeoutError

from time import sleep, time

import numpy as np
import pandas as pd

import evaluate_algorithm as evaluate
import printGeneration as printG
from fit_map import *

def evaluate_individuals(G, individuals, dataTraining, seed, dataSeed, internalCV,nCores,timeOut,mutation_rate,crossover_rate):

    """Evaluate all individuals of a generation using a seed and a Training method. Uses multiprocessing

    Parameters
    ----------

    G: int
        Number of the generation

    individuals: string
        A string containing all individuals of a generation

    dataTraining: numpy data
        Data used to train the methods and evaluate each individual

    seed: int
        Seed used in the random processes

    dataSeed: int
        The seed to control the data resample each x generations.

    internalCV: int
       The number of folds in the internal cross-validation procedure.

    """

    try:
        #Generate all the algorithms to evaluate:
        filename = dataTraining.split("/")[-1]
        filename = filename.replace(".csv","")

        filename_map = filename+"s"+str(seed)+'m'+str(mutation_rate).replace('.','_')+'c'+str(crossover_rate).replace('.',"_")

        algorithms =  individuals.strip().split(';')
        output_training = [0.0] * len(algorithms)
        fitness_map = get_fitness_map(filename_map)

        for index,alg in enumerate(algorithms):
            if(alg in fitness_map):
                output_training[index] = fitness_map[alg]
            else:
                try:
                    result = 0.0

                    @concurrent.process(timeout=timeOut)
                    def evaluate_alg(alg,dataTraining,seed,dataSeed,internalCV):
                        return evaluate.evaluate_algorithm(alg,dataTraining,seed,dataSeed,internalCV)

                    future = evaluate_alg(alg,dataTraining,seed,dataSeed,internalCV)

                    try:
                        result = future.result()
                    except TimeoutError as error:
                        result = 0.0
                    except Exception as error:
                        result = 0.0
                except e:
                    result = 0.0

                output_training[index] = result
                fitness_map[alg] = output_training[index]

        save_fitness_map(fitness_map,filename_map)

        #Get the evaluations:
        evaluations = ""
        for i in range(len(algorithms)):
            evalTraining = output_training[i]
            evaluations += str(round(evalTraining,6))
            if (i is not (len(algorithms)-1)):
                evaluations += ";"

        printG.printGeneration(G, seed, output_training, "EvoTraining_"+filename)

        #Return the evaluations separated by semicolons:
        return evaluations
    except (KeyboardInterrupt, SystemExit):
        return
