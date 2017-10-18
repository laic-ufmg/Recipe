#Pipeline automatically generated using RECIPE

from sklearn.pipeline import make_pipeline

from sklearn.preprocessing import LabelEncoder

import numpy as np
import pandas as pd

from sklearn.preprocessing import Imputer
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegressionCV

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

	step0 = Imputer(axis=0, copy=True, missing_values='NaN', strategy='median', verbose=0)

	step1 = VarianceThreshold(threshold=0.0)

	step2 = PolynomialFeatures(degree=2, include_bias=True, interaction_only=False)

	step3 = LogisticRegressionCV(Cs=10, class_weight=None, cv=None, dual=False,
           fit_intercept=True, intercept_scaling=1.0, max_iter=300,
           multi_class='ovr', n_jobs=1, penalty='l2', random_state=42,
           refit=True, scoring=None, solver='liblinear', tol=0.057839,
           verbose=0)

	methods = []
	methods.append(step0)
	methods.append(step1)
	methods.append(step2)
	methods.append(step3)

	pipeline = make_pipeline(*methods)

	return pipeline