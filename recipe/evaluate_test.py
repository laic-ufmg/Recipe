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

from time import sleep, time
import random

import printGeneration as printG
import testAlgorithm as test
from fit_map import *

from stopit import threading_timeoutable, TimeoutException

@threading_timeoutable(default=0.0)
def run_test(alg,dataTraining,dataTest,seed,dataSeed,index):
    try:
        result = test.testAlgorithm(alg,dataTraining,dataTest,seed,dataSeed)
        return float(result.strip().split(',')[-1]),index
    except TimeoutException:
        return 0.0,index
    except Exception as e:
        return 0.0,index

def evaluate_test(G, individuals, dataTraining, dataTest, seed, dataSeed,nCores,timeOut,mutation_rate,crossover_rate):

    """Evaluate the test individuals

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

    """

    #print "#####TESTE##### \n"
    try:

        filename = dataTest.split("/")[-1]
        filename = filename.replace(".csv","")
        #Generate all the algorithms to evaluate:
        algorithms =  individuals.strip().split(';')
        output_test= [0.0] * len(algorithms)

        filename_map = filename+"s"+str(seed)+'m'+str(mutation_rate).replace('.','_')+'c'+str(crossover_rate).replace('.',"_")

        fitness_map = get_fitness_map(filename_map)

        for index,alg in enumerate(algorithms):
            if(alg in fitness_map):
                output_test[index] = fitness_map[alg]
            else:

                result,index = run_test(alg,dataTraining,dataTest,seed,dataSeed,index,timeout=timeOut)
                
                output_test[index] = result
                fitness_map[alg] = output_test[index]

        save_fitness_map(fitness_map,filename_map)

        printG.printGeneration(G, seed, output_test, "EvoTest_"+filename)

        return ""

    except (KeyboardInterrupt, SystemExit):
        return
