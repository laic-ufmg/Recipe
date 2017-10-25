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

import argparse
import os
from sys import platform
from subprocess import call

def verbosity_range(X):

	"""Function that evaluates if the verbosity level given by the user is at a certain range

    Parameters
    ----------

    X: int
       Range of the verbosity level

	"""

	x=int(X)
	if x>3:
		x=1
	return x

def track_range(X):

	"""Function that evaluates if the track level given by the user is at a certain range

    Parameters
    ----------

    X: int
       Range of the track level

	"""

	x=int(X)
	if x>1:
		x=0
	return x

def max_rate(X):

	"""Function that evaluates if the track level given by the user is at a certain range

    Parameters
    ----------

    X: float
       Range of the track level

	"""

	x=float(X)
	if x>1 or x<0:
		x=0.1
	return x

def main(args):

	cmd = './bin/automaticML '+args.config+" "+str(args.seed)+" "+args.dataTrain+" "+args.dataTest+"\
	 "+str(args.nCores)+" "+str(args.timeout)+" "+args.export_name+" "+str(args.verbosity)+" "+str(args.track_ind)+" "+str(args.mutation_rate)+"\
	  "+str(args.crossover_rate)+" "+str(args.population_size)+" "+str(args.generation_count)
	call(cmd,shell=True)

if __name__ == "__main__":

	if(os.path.isfile('./bin/automaticML')):

		parser = argparse.ArgumentParser(description = 'RECIPE - Algorithm to generate machine learning pipelines')
		parser.add_argument('-c', '--config', help= "configuration file of the GP", default ='./config/gecco2015-cfggp.ini', required=False)
		parser.add_argument('-s', '--seed' , help="seed value for the random functions",default=1,type=int,required=False)
		parser.add_argument('-dTr','--dataTrain',help="file to train the algorithm",required=True)
		parser.add_argument('-dTe','--dataTest',help="file to test the algorithm",required=True)
		parser.add_argument('-nc','--nCores',help="number of cores to be used on the algorithm execution",default=1,required=False, type=int)
		parser.add_argument('-t','--timeout',help="time to execute each individual of the GP on evaluation",default=300,required=False, type=int)
		parser.add_argument('-en','--export_name',help="file name for the exported pipeline",default='pipeline.py',required=False)
		parser.add_argument('-v','--verbosity',help="verbosity level of the output",default=1,required=False,type=verbosity_range)
		parser.add_argument('-ti','--track_ind',help="create a file to track the individuals of all generations(1-true|0-false)",default=0,required=False,type=track_range)
		parser.add_argument('-mr','--mutation_rate',help="define the mutation rate for the algorithm (max=1.0)",default=0.1,required=False,type=max_rate)
		parser.add_argument('-cr','--crossover_rate',help="define the crossover rate for the algorithm (max=1.0)",default=0.9,required=False,type=max_rate)
		parser.add_argument('-ps','--population_size',help="define the size for the inicial population for the algorithm",default=30,required=False)
		parser.add_argument('-gc','--generation_count',help="define the generation count for the algorithm",default=100,required=False)

		args = parser.parse_args()

		main(args)

	else:

		print "First is necessary to build the project. Run python setup.py build"
