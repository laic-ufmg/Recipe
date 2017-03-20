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

import multiprocessing
from multiprocessing import Pool, TimeoutError, Queue

from time import sleep, time

import numpy as np
import pandas as pd

import evaluate_algorithm as evaluate
import printGeneration as printG

def evaluate_individuals(G, individuals, dataTraining, seed, dataSeed, internalCV,nCores,timeOut):
    
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
        algorithms =  individuals.strip().split(';')

        #Uses a pool with n process to evaluate the individuals:
        pool = Pool(processes=nCores)
        results = []
        output_training = []
        try:
            for alg in algorithms:
                #Apply the algorithm over the dataset with a multiprocess approach and get the return:
                results.append(pool.apply_async(evaluate.evaluate_algorithm, args=(alg,dataTraining,seed,dataSeed,internalCV)))
        except Exception as ei:
            print ei

        #position of the individual that suffers timeout:
        posTimeout = 0

        #To control the timeout to finish the method in a proper time:
        start = time()
        #Timeout=300s for each process:
        wait_until = start + timeOut

        try:
            for r in results:
                try:
                    #Controls the timeout in order to kill the method in a proper time:
                    timeout = wait_until - time()
                    if timeout < 0:
                        timeout = 0

                    #Apply the algorithm over the dataset with a multiprocess approach and get the return:
                    output_training.append(r.get(timeout))
                    posTimeout = posTimeout + 1
                except TimeoutError as toe:
                    warnings.warn("WARNING: Timeout reached for the algorithm -> "+ algorithms[posTimeout],UserWarning)
                    posTimeout = posTimeout + 1
                    output_training.append(0.0)

        except Exception as ei:
            print "Exception: ",ei

        #Finish the pool:
        pool.terminate()
        pool.join()

        #Get the evaluations:
        evaluations = ""
        for i in range(len(algorithms)):
            #eval = runAlgorithmAndEvaluate(algorithms[i], dataTraining)  # iterative
            evalTraining = output_training[i]
            evaluations += str(round(evalTraining,6))
            if (i is not (len(algorithms)-1)):
                evaluations += ";"

        filename = dataTraining.split("/")[-1]
        filename = filename.replace(".csv","")
        printG.printGeneration(G, seed, output_training, "EvoTraining_"+filename)

        #Return the evaluations separated by semicolons:
        return evaluations
    except (KeyboardInterrupt, SystemExit):
        return