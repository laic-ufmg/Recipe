# -*- coding: utf-8 -*-

"""
Copyright 2016 Walter José

This file is part of the RECIPE Algorithm.

The RECIPE is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

RECIPE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. See http://www.gnu.org/licenses/.

"""

import preprocessors as pre
import classifiers as clas

def load_method(algorithm_string):

  """Retunrn a scikit-learn's methods already configured to make the pipeline.

  Parameters
  ----------
  algorithm_string: string
    A string the contains the algorithm to be loaded

  """

  args=algorithm_string.strip().split();

  if((args[0] == "DecisionTreeClassifier") or (args[0] == "ExtraTreeClassifier")):
    return clas.treeEstimator(args)
  elif((args[0] == "RandomForestClassifier") or (args[0] == "ExtraTreesClassifier")):
    return clas.specificTree(args)
  elif(args[0] == "GradientBoostingClassifier"):
    return clas.gradientBC(args)
  elif(args[0] == "AdaBoostClassifier"):
    return clas.ada(args)

  elif(args[0] == "GaussianNB"):
    return clas.gaussianNB(args)
  elif(args[0] == "BernoulliNB"):
    return clas.bernoulliNB(args)
  elif(args[0] == "MultinomialNB"):
    return clas.multinomialNB(args)

  elif(args[0] == "NuSVC"):
    return clas.svc(args)
  elif(args[0] == "SVC"):
    return clas.svc(args)

  elif(args[0] == "KNeighborsClassifier"):
    return clas.kNeighboors(args)
  elif(args[0] == "RadiusNeighborsClassifier"):
    return clas.radiusNeighboors(args)
  elif(args[0] == "CentroidClassifier"):
    return clas.ncentroid(args)
  elif(args[0] == "LinearDiscriminantAnalysis"):
    return clas.lda(args)
  elif(args[0] == "QuadraticDiscriminantAnalysis"):
    return clas.qda(args)
  elif(args[0] == "LogisticRegression"):
    return clas.logistic(args)
  elif(args[0] == "LogisticCV"):
    return clas.logisticCV(args)
  elif(args[0] == "RandomizedLogistic"):
    return clas.randomLogistic(args)
  elif(args[0] == "PassiveAggressive"):
    return clas.passive(args)
  elif(args[0] == "Perceptron"):
    return clas.perceptron(args)
  elif(args[0] == "SGDClassifier"):
    return clas.sgd(args)
  elif(args[0] == "RidgeClassifier"):
    return clas.ridge(args)
  elif(args[0] == "RidgeCCV"):
    return clas.ridgeCV(args)

  elif(args[0] == "Binarizer"):
    return pre.binarizer(args)
  elif(args[0] == "Imputer"):
    return pre.imputer(args)
  elif(args[0] == "Normalizer"):
    return pre.normalizer(args)
  elif(args[0] == "MinMaxScaler"):
    return pre.minMax(args)
  elif(args[0] == "MaxAbsScaler"):
    return pre.maxAbs(args)
  elif((args[0] == "StandardScaler") or (args[0] == "RobustScaler")):
    return pre.scaler(args)

  elif(args[0] == "SelectKBest"):
    return pre.selectKBest(args)
  elif(args[0] == "VarianceThreshold"):
    return pre.threshold(args)
  elif(args[0] == "SelectPercentile"):
    return pre.percentile(args)
  elif(args[0] == "SelectFpr"):
    return pre.selectFpr(args)
  elif(args[0] == "SelectFdr"):
    return pre.selectFdr(args)
  elif(args[0] == "SelectFwe"):
    return pre.selectFwe(args)
  elif(args[0] == "RFE"):
    return pre.rfe(args)
  elif(args[0] == "RecursiveFE_CV"):
    return pre.rfecv(args)
  elif(args[0] == "SelectFromModel"):
    return pre.selectfm(args)

  elif(args[0] == "TraditionalPCA"):
    return pre.pca(args)
  elif(args[0] == "IncrementalPCA"):
    return pre.ipca(args)

  elif(args[0] == "FastICA"):
    return pre.fast_ica(args)
  elif(args[0] == "FeatureAgglomeration"):
    return pre.fag(args)
  elif(args[0] == "GaussianRandomProjection"):
    return pre.gaussianR(args)
  elif(args[0] == "SparseRandomProjection"):
    return pre.sparseR(args)

  elif(args[0] == "RBFSampler"):
    return pre.rbf_sampler(args)
  elif(args[0] == "Nystroem"):
    return pre.nystroem(args)

  elif(args[0] == "PolynomialFeatures"):
    return pre.polynomial_features(args)
