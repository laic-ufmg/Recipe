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
import warnings, sys,os
from time import gmtime, strftime

def customwarn(message, category, filename, lineno, file=None, line=None):
	with open("log.txt","a+") as file:
		file.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) +" : "+  warnings.formatwarning(message, category, filename, lineno)+"\n")

warnings.showwarning = customwarn
#warnings.filterwarnings('ignore')

import evaluate_individuals as evaluate
import evaluate_test as evaluateT
import testAlgorithm as test
import export_pipe as export
import progress

def evaluate_inds(G, individuals, dataTraining, seed, dataSeed, internalCV,nCores,timeout,mutation_rate,crossover_rate):

    return evaluate.evaluate_individuals(G,individuals,dataTraining,seed,dataSeed,internalCV,nCores,timeout,mutation_rate,crossover_rate)

def evaluate_on_test(G, individuals, dataTraining, dataTest, seed, dataSeed,nCores,timeout,mutation_rate,crossover_rate):

	return evaluateT.evaluate_test(G,individuals,dataTraining,dataTest,seed,dataSeed,nCores,timeout,mutation_rate,crossover_rate)

def test_algorithm(mlAlgorithm, dataTraining, dataTest, seed, dataSeed):

	return test.testAlgorithm(mlAlgorithm,dataTraining,dataTest,seed,dataSeed)

def export_pipe(_filename,individual):

	if(_filename.endswith(".py")==False):
		_filename=_filename+'.py'

	export.export_pipe(_filename,individual)

def print_progress(generation,total,best,individual):

	suff = '{message: <{width}}'.format(message="Best found: "+str(best)+ " -> " + individual, width=150)

	progress.printProgress (generation,total, prefix = 'Processing '+str(generation)+' of '+str(total), suffix = suff)

def export_result(test_result,seed,individual,input_file):

	if not os.path.exists('results'):
		os.makedirs('results')

	filename = input_file.split("/")[-1]

	filename = filename.replace(".csv","")

	with open('results/Result_'+filename+'.csv',"a") as out:
		out.write(test_result+","+str(seed)+","+individual+"\n")

def save_individuals(individuals,generation,input_file,seed):

	indi_list = individuals.split(';')

	if not os.path.exists('individuals'):
		os.makedirs('individuals')

	filename = input_file.split("/")[-1]

	filename = filename.split("-")[0]

	with open('individuals/'+filename+'_s'+str(seed)+'.csv',"a+") as out:
		out.write(strftime("%Y-%m-%d %H:%M:%S ", gmtime())+"Generation "+str(generation)+"\n")
		out.write("\n".join(indi_list))
		out.write("\n\n")
