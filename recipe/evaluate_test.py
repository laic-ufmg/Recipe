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

from sklearn.preprocessing import LabelEncoder

import multiprocessing
from multiprocessing import Pool, TimeoutError, Queue

from time import sleep, time
import random

import printGeneration as printG

import testAlgorithm as test

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def evaluate_test(G, individuals, dataTraining, dataTest, seed, dataSeed,nCores,timeOut):

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
        #Generate all the algorithms to evaluate:
        algorithms =  individuals.strip().split(';')

        #Uses a pool with n process to evaluate the individuals:
        pool = Pool(processes=nCores)
        results = []
        output = []
        try:
            for alg in algorithms:
                #Apply the algorithm over the dataset with a multiprocess approach and get the return:
                results.append(pool.apply_async(test.testAlgorithm, args=(alg,dataTraining,dataTest,seed,dataSeed)))
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
                    output.append(r.get(timeout))
                    posTimeout = posTimeout + 1
                except TimeoutError as toe:
                    print "WARNING: Timeout reached for the algorithm ->", algorithms[posTimeout]
                    posTimeout = posTimeout + 1
                    output.append(0.0)


        except Exception as ei:
            print ei

        #Finish the pool:
        pool.terminate()
        pool.join()

        i = 0
        test_results = []
        for out in output:
            out = str(out)
            if(out.find(",")!=-1):
                test_res = out.split(',')
                if(len(test_res) > 1):
                    test_results.append(float(test_res[15]))
            else:
                test_results.append(0.0)   


        printG.printGeneration(G, seed, test_results, "Evolution-Test_")

        return "" 

    except (KeyboardInterrupt, SystemExit):
        return