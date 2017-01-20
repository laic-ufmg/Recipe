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

def main(args):

	cmd = './bin/automaticML '+args.config+" "+str(args.seed)+" "+args.dataTrain+" "+args.dataTest
	call(cmd,shell=True)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = 'RECIPE - Algorithm to generate machine learning pipelines')

	parser.add_argument('-c', '--config', help= "configuration file of the GP", default = './config/gecco2015-cfggp.ini', required=False)
	parser.add_argument('-s', '--seed' , help="seed value for the random functions",default=1,type=int,required=False)
	parser.add_argument('-dTr','--dataTrain',help="file to train the algorithm",required=True)
	parser.add_argument('-dTe','--dataTest',help="file to test the algorithm",required=True)	

	args = parser.parse_args()

	main(args)