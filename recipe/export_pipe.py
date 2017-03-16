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

		out.write("def pipeline(dataTraining,dataTest):\n\n")

		out.write('''
\t#Load the training and test datasets:
\ttraining_df = pd.read_csv(dataTraining, header=0, delimiter=",")
\ttest_df = pd.read_csv(dataTest, header=0, delimiter=",") 

\t#Apply a filter if the data has categorical data (sklean does not accept this type of data):
\tobjectList = list(training_df.select_dtypes(include=['object']).columns)
\tif ('class' in objectList and len(objectList)>=1):
\t\ttraining_df = training_df.apply(LabelEncoder().fit_transform)
\t\ttest_df = test_df.apply(LabelEncoder().fit_transform)

\t#Get the feature data and the class for training:
\ttrain_data = training_df.ix[:,:-1].values
\ttrain_target = training_df["class"].values    
        
\t# ... and test:
\ttest_data = test_df.ix[:,:-1].values
\ttest_target = test_df["class"].values

\t#Validation -- Get a subsample of the training to get information about possible overfitting:
\tX_train, X_validation, y_train, y_validation = train_test_split(train_data, train_target, train_size=0.7, test_size=0.3, random_state=dataSeed, stratify=train_target)\n
''')

		count = 0

		methods = []

		for p in pipe:

			str1 = "\tstep"+str(count)+" = "+str(p)+"\n"
			methods.append(str1)
			count+=1

		out.write("\n".join(methods))

		out.write("\n\tmethods = []")

		for i in range(0,count):

			out.write("\n\tmethods.append(step"+str(i)+")")

		out.write("\n\n\tpipeline = make_pipeline(*methods)")

		
