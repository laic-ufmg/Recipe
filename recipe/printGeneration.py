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

import numpy as np

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def printGeneration(G, seed, output, file_name):

	try:

		output.sort()

		best = output[len(output)-1]
		worst = output[0]
		average = np.mean(output)

		file_t = file_name+str(seed)+".csv"
		evolution_file = open(file_t,'a+')

		evolution_file.write(str(G)+';'+str(worst)+';'+str(average)+';'+str(best)+'\n')
		evolution_file.close()
	except IOError as e:
		print "WARNING: ", e

	#print str(G)+';'+str(worst_training)+';'+str(average_training)+';'+str(best_training)
	#print str(G)+';'+str(worst_test)+';'+str(average_test)+';'+str(best_test)