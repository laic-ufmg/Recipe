#Pipeline automatically generated using RECIPE

from sklearn.pipeline import make_pipeline

from sklearn.preprocessing import LabelEncoder

import numpy as np
import pandas as pd

from sklearn.preprocessing import Imputer
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
None

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

	step0 = Imputer(axis=0, copy=True, missing_values='NaN', strategy='most_frequent',
    verbose=0)

	step1 = StandardScaler(copy=True, with_mean='False', with_std=True)

	step2 = FeatureUnion(n_jobs=1,
       transformer_list=[('votingclassifier', VotingClassifier(estimators=[('alg0', GradientBoostingClassifier(criterion='friedman_mse', init=None,
              learning_rate=0.033942, loss='deviance', max_depth=32581,
              max_features=None, max_leaf_nodes=76264,
              min_impurity_split...6ad050>, inv_kw_args=None,
          inverse_func=None, kw_args=None, pass_y=False, validate=True))],
       transformer_weights=None)

	step3 = RadiusNeighborsClassifier(algorithm='brute', leaf_size=71, metric='manhattan',
             metric_params=None, outlier_label=100000, p=10,
             radius=1.751848, weights='uniform')

	methods = []
	methods.append(step0)
	methods.append(step1)
	methods.append(step2)
	methods.append(step3)

	pipeline = make_pipeline(*methods)

	return pipeline