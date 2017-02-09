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

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

import evaluate_individuals as evaluate
import evaluate_test as evaluateT
import testAlgorithm as test
import export_pipe as export

def evaluate_inds(G, individuals, dataTraining, seed, dataSeed, internalCV,nCores,timeout):

    return evaluate.evaluate_individuals(G,individuals,dataTraining,seed,dataSeed,internalCV,nCores,timeout)

def evaluate_on_test(G, individuals, dataTraining, dataTest, seed, dataSeed,nCores,timeout):

	return evaluateT.evaluate_test(G,individuals,dataTraining,dataTest,seed,dataSeed,nCores,timeout)

def test_algorithm(mlAlgorithm, dataTraining, dataTest, seed, dataSeed):

	return test.testAlgorithm(mlAlgorithm,dataTraining,dataTest,seed,dataSeed)

def export_pipe(_filename,individual):
	
	export.export_pipe("pipeline.py",individual)