#Pipeline automatically generated using RECIPE

from sklearn.pipeline import make_pipeline

from sklearn.preprocessing import LabelEncoder

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.svm import NuSVC, SVC
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
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

	step0 = RobustScaler(copy=True, quantile_range=(25.0, 75.0), with_centering='True',
       with_scaling=False)

	step1 = FeatureUnion(n_jobs=1,
       transformer_list=[('votingclassifier', VotingClassifier(estimators=[('alg0', SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape=None, degree=7, gamma='auto', kernel='linear',
  max_iter=2500, probability=False, random_state=42, shrinking=True,
  tol=0.088854, verbose=...f49050>, inv_kw_args=None,
          inverse_func=None, kw_args=None, pass_y=False, validate=True))],
       transformer_weights=None)

	step2 = QuadraticDiscriminantAnalysis(priors=None, reg_param=0.098743,
               store_covariances=False, tol=0.072336)

	methods = []
	methods.append(step0)
	methods.append(step1)
	methods.append(step2)

	pipeline = make_pipeline(*methods)

	return pipeline