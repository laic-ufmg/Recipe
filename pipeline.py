#Pipeline automatically generated using RECIPE

from sklearn.pipeline import make_pipeline

from sklearn.preprocessing import LabelEncoder

import numpy as np
import pandas as pd

from sklearn.preprocessing import Imputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import f_classif, chi2, SelectFpr
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier

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

	step0 = Imputer(axis=0, copy=True, missing_values='NaN', strategy='mean', verbose=0)

	step1 = MinMaxScaler(copy=True, feature_range=(0, 1))

	step2 = SelectFpr(alpha=0.371134, score_func=<function f_classif at 0x7ff7f1c75b18>)

	step3 = PolynomialFeatures(degree=6, include_bias=False, interaction_only=False)

	step4 = ExtraTreeClassifier(class_weight=None, criterion='entropy', max_depth=None,
          max_features=None, max_leaf_nodes=74534,
          min_impurity_split=1e-07, min_samples_leaf=1,
          min_samples_split=2, min_weight_fraction_leaf=0.254394,
          random_state=42, splitter='random')

	methods = []
	methods.append(step0)
	methods.append(step1)
	methods.append(step2)
	methods.append(step3)
	methods.append(step4)

	pipeline = make_pipeline(*methods)

	return pipeline