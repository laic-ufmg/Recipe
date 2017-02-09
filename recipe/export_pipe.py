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
from sklearn.pipeline import make_pipeline,Pipeline

import load_imports as load
import load_pipeline as loadp

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def export_pipe(_filename,pipeline):

	pipe = loadp.load_pipeline(pipeline)
	imports = []

	imports.append("from sklearn.pipeline import make_pipeline\n")

	imports.append("from sklearn.preprocessing import LabelEncoder\n")

	imports.append("import numpy as np")
	imports.append("import pandas as pd\n")

	steps_list = pipeline.strip().split('#')

	for steps in steps_list:
		algorithm = steps.strip().split()
		temporary_import=load.load_imports(algorithm[0])
		imports.append(temporary_import)

	#write imports to file
	with open(_filename,'w') as out:

		out.write("#Pipeline automatically generated using RECIPE\n\n")

		for imp in imports:
			out.write("%s\n" % (imp))

		out.write("\n")

		count = 0

		methods = []

		for p in pipe:

			str1 = "step"+str(count)+" = "+str(p)+"\n"
			methods.append(str1)
			count+=1

		out.write("\n".join(methods))

		out.write("\nmethods = []\n")

		for i in range(0,count):

			out.write("methods.append(step"+str(i)+")")

		out.write("\n\npipeline = make_pipeline(*methods)")
