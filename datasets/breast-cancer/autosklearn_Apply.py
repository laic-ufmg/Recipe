import autosklearn.classification

from sklearn.datasets import load_digits
from sklearn.cross_validation import train_test_split

#Used for preprocessing if the variable is categorical
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics

import pandas as pd

import sys 

import warnings
warnings.filterwarnings("ignore")


def evaluate_fold(_name,fold_number,seed):

	name = _name

	i=fold_number

	print "FOLD"+str(i)

	dataTraining=name+"-Training"+str(i)+'.csv'
	dataTest=name+"-Test"+str(i)+'.csv'
		
	training_df = pd.read_csv(dataTraining, header=0, delimiter=",")
	test_df = pd.read_csv(dataTest, header=0, delimiter=",") 

	#Apply a filter if the data has categorical data (sklean does not accept this type of data):
	objectList = list(training_df.select_dtypes(include=['object']).columns)
	if ('class' in objectList and len(objectList)>1):
		training_df = training_df.apply(LabelEncoder().fit_transform)
		test_df = test_df.apply(LabelEncoder().fit_transform)

	#Get the feature data and the class for training:
	train_data = training_df.ix[:,:-1].values
	train_target = training_df["class"].values    
		    
	# ... and test:
	test_data = test_df.ix[:,:-1].values
	test_target = test_df["class"].values
	            
	autosk = autosklearn.classification.AutoSklearnClassifier(time_left_for_this_task=1800,seed=seed)
	autosk.fit(train_data, train_target)

	predictedTest = autosk.predict(test_data)
	expectedTest = test_target

	accuracyTest = metrics.accuracy_score(expectedTest, predictedTest)
	precisionTest = metrics.precision_score(expectedTest, predictedTest, average='weighted')
	recallTest = metrics.recall_score(expectedTest, predictedTest, average='weighted')
	f1Test = metrics.f1_score(expectedTest, predictedTest, average='weighted')

	print(str(i)+','+str(accuracyTest)+','+str(precisionTest)+','+str(recallTest)+','+
		str(f1Test)+'\n')



if __name__ == "__main__":

	name = sys.argv[1]
	fold_number = int(sys.argv[2])
	seed = int(sys.argv[3])

	evaluate_fold(name,fold_number,seed)
