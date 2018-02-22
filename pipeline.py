#Pipeline automatically generated using RECIPE

from sklearn.pipeline import make_pipeline

from sklearn.preprocessing import LabelEncoder

import numpy as np
import pandas as pd

from sklearn.ensemble import GradientBoostingClassifier

def pipeline(dataTraining,dataTest):


	#Load the training and test datasets:
	training_df = pd.read_csv(dataTraining, header=0, delimiter=",")
	test_df = pd.read_csv(dataTest, header=0, delimiter=",")

	#Apply a filter if the data has categorical data (sklean does not accept this type of data):
	objectList = list(training_df.select_dtypes(include=['object']).columns)
	if ('class' in objectList and len(objectList)>=1):
		training_df = training_df.apply(LabelEncoder().fit_transform)
		test_df = test_df.apply(LabelEncoder().fit_transform)

	#Get the feature data and the class for training:
	train_data = training_df.ix[:,:-1].values
	train_target = training_df["class"].values

	# ... and test:
	test_data = test_df.ix[:,:-1].values
	test_target = test_df["class"].values

	#Validation -- Get a subsample of the training to get information about possible overfitting:
	X_train, X_validation, y_train, y_validation = train_test_split(train_data, train_target, train_size=0.7, test_size=0.3, random_state=dataSeed, stratify=train_target)

	step0 = GradientBoostingClassifier(criterion='friedman_mse', init=None,
              learning_rate=0.066789, loss='exponential', max_depth=55712,
              max_features=0.56515, max_leaf_nodes=None,
              min_impurity_decrease=0.0, min_impurity_split=None,
              min_samples_leaf=1, min_samples_split=2,
              min_weight_fraction_leaf=0.093157, n_estimators=35,
              presort='auto', random_state=42, subsample=0.92525,
              verbose=0, warm_start=True)

	methods = []
	methods.append(step0)

	pipeline = make_pipeline(*methods)

	return pipeline