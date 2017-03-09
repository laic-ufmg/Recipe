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

import load_pipeline as load

from sklearn.cross_validation import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder

import numpy as np
import pandas as pd

import load_pipeline as load
from sklearn.pipeline import make_pipeline

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def testAlgorithm(mlAlgorithm, dataTraining, dataTest, seed, dataSeed):
    try:
        #Load the training and test datasets:
        training_df = pd.read_csv(dataTraining, header=0, delimiter=",")
        test_df = pd.read_csv(dataTest, header=0, delimiter=",")

        class_name = test_df.columns.values.tolist()[-1] 

        #Apply a filter if the data has categorical data (sklean does not accept this type of data):
        objectList = list(training_df.select_dtypes(include=['object']).columns)
        if (class_name in objectList and len(objectList)>=1):
            training_df = training_df.apply(LabelEncoder().fit_transform)
            test_df = test_df.apply(LabelEncoder().fit_transform)

        #Get the feature data and the class for training:
        train_data = training_df.ix[:,:-1].values
        train_target = training_df[class_name].values    
        
        # ... and test:
        test_data = test_df.ix[:,:-1].values
        test_target = test_df[class_name].values

        #Validation -- Get a subsample of the training to get information about possible overfitting:
        X_train, X_validation, y_train, y_validation = train_test_split(train_data, train_target, train_size=0.7, test_size=0.3, random_state=dataSeed, stratify=train_target)

        pipe = load.load_pipeline(mlAlgorithm)
        try:
            pipeline=make_pipeline(*pipe)
        except Exception as exc:
            print exc
            return "0.0"

        pipelineTraining = pipeline
        pipelineWholeTraining = pipeline

        #Fit the final model with all the steps:
        pipelineTraining.fit(X_train, y_train)
        #Predict for the training set to evaluate the error on training:
        predictedTraining = pipelineTraining.predict(X_train)
        expectedTraining = y_train
        #Predict for the validation to evaluate the error on validation:
        predictedValidation = pipelineTraining.predict(X_validation)
        expectedValidation = y_validation

        pipelineWholeTraining.fit(train_data, train_target)
        #Predict for the whole training set to evaluate the error on training during test phase:
        predictedWholeTraining = pipelineWholeTraining.predict(train_data)
        expectedWholeTraining = train_target
        #Predict for the test to evaluate the error on test:
        predictedTest = pipelineTraining.predict(test_data)
        expectedTest = test_target

        #classification metrics:
        #accuracyTraining = metrics.accuracy_score(expectedTraining, predictedTraining)
        accuracyTraining = pipeline.fit(X_train, y_train).score(X_train, y_train)
        precisionTraining = metrics.precision_score(expectedTraining, predictedTraining, average='weighted')
        recallTraining = metrics.recall_score(expectedTraining, predictedTraining, average='weighted')
        f1Training = metrics.f1_score(expectedTraining, predictedTraining, average='weighted')

        accuracyValidation = metrics.accuracy_score(expectedValidation, predictedValidation)
        precisionValidation = metrics.precision_score(expectedValidation, predictedValidation, average='weighted')
        recallValidation = metrics.recall_score(expectedValidation, predictedValidation, average='weighted')
        f1Validation = metrics.f1_score(expectedValidation, predictedValidation, average='weighted')

        accuracyWholeTraining = metrics.accuracy_score(expectedWholeTraining, predictedWholeTraining)
        precisionWholeTraining = metrics.precision_score(expectedWholeTraining, predictedWholeTraining, average='weighted')
        recallWholeTraining = metrics.recall_score(expectedWholeTraining, predictedWholeTraining, average='weighted')
        f1WholeTraining = metrics.f1_score(expectedWholeTraining, predictedWholeTraining, average='weighted')

        accuracyTest = metrics.accuracy_score(expectedTest, predictedTest)
        precisionTest = metrics.precision_score(expectedTest, predictedTest, average='weighted')
        recallTest = metrics.recall_score(expectedTest, predictedTest, average='weighted')
        f1Test = metrics.f1_score(expectedTest, predictedTest, average='weighted')
        #classification metrics concatenation:
        resultMetrics = str(accuracyTraining) + "," + str(precisionTraining) + "," + str(recallTraining) + "," + str(f1Training) + "," + str(accuracyValidation) + "," + str(precisionValidation) + "," + str(recallValidation) + "," + str(f1Validation) + "," +str(accuracyWholeTraining) + "," + str(precisionWholeTraining) + "," + str(recallWholeTraining) + "," + str(f1WholeTraining) + "," + str(accuracyTest) + "," + str(precisionTest) + "," + str(recallTest) + "," + str(f1Test)
        
        return resultMetrics
    except Exception as e:
        print "WARNING: ", e, "->", mlAlgorithm
        return "0.0" 