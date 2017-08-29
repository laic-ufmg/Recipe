# -*- coding: utf-8 -*-

import sys
import arff

from os import listdir
import os
import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold

import progress

def to_csv(filename):

	data = arff.load(open(filename, 'rb'))

	name = filename.strip().split('.')[0]

	header = ','.join(str(x[0]) for x in data['attributes'])

	with open(name+'.csv','w') as output:

		output.write(header+'\n')
		
		for dados in data['data']:
			line = ','.join(str(x) for x in dados)
			line = line.replace("None","NaN")
			
			output.write(line+'\n')

def find_filenames(path_to_dir, suffix=".csv" ):

	filenames = listdir(path_to_dir)
	files = set([ filename for filename in filenames if filename.endswith( suffix ) ])
	return files 

def kfolds(filename,nfolds,broken_datasets):

	dname = filename.strip().split('.')

	try:
		dataset = pd.read_csv(filename)
	except Exception as e:
		return

	headers = dataset.dtypes.index
	targetH = headers[-1]

	target = dataset[targetH]
	#data = dataset.drop(targetH,axis = 1)

	if(count_target(target,nfolds)):
		directory = dname[0]
		if not os.path.exists(directory):
			os.makedirs(directory)
		
		folds = create_folds(target,nfolds)
		for i in range (0,len(folds)):
			train_index = folds[i]
			test_index = []
			for j in range(0,len(folds)):
				if(j!=i):
					test_index.extend(folds[j])
			train, test = dataset.iloc[train_index], dataset.iloc[test_index]
			train.to_csv(directory+'/'+dname[0]+'-Training'+str(i)+'.csv', sep=',', encoding='utf-8',index = False)
			test.to_csv(directory+'/'+dname[0]+'-Test'+str(i)+'.csv', sep=',', encoding='utf-8',index = False)

	else:
		broken_datasets.append(dname[0])
		#print "Dataset "+ dname[0] +" has a class with fewer instances than the number of folds"

def create_folds(target,nfolds):

	values ={}
	folds = {}

	for i in range(0,nfolds):
		folds[i]=[]

	for i in range(0,len(target)):
		value = target[i]
		if(values.has_key(value)):
			values[value].append(i)
		else:
			values[value]=[]
			values[value].append(i)

	fold_aux = 0
	for key,value in values.items():
		for v in value:
			folds[fold_aux].append(v)
			if(fold_aux==nfolds-1):
				fold_aux=0
			else:
				fold_aux+=1

	return folds

def count_target(target,nfolds):

	values = {}
	for value in target:
		if(values.has_key(value)):
			values[value]+=1
		else:
			values[value]=1

	for key,value in values.items():
		if(value<nfolds):
			return False

	return True

def main():

	broken_datasets = []

	arff_files = find_filenames("./",suffix='.arff')

	files = find_filenames("./",suffix='.csv')

	print "Transforming from .arff to .csv"

	i=0
	for af in arff_files:
		suff = '{message: <{width}}'.format(message=af, width=60)
		progress.printProgress (i+1,len(arff_files), prefix = 'Processing', suffix = suff)
		arff_name = af.split('.')

		i+=1
		try:
			if( arff_name[0]+".csv" not in files):
				to_csv(af)
		except Exception as e:
			continue
		

	print "\nFind all files with .csv"
	files = find_filenames("./",suffix='.csv')

	i=0

	for file in files:
		suff = '{message: <{width}}'.format(message=file, width=60)
		progress.printProgress (i+1,len(files), prefix = 'Processing', suffix = suff)
		kfolds(file,10,broken_datasets)
		i+=1

	print "\nBroken Datasets ("+str(len(broken_datasets))+"):"

	print broken_datasets
	
if __name__ == "__main__":

	main()
