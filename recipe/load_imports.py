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

from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def load_imports(_method):

    if((_method == "DecisionTreeClassifier") or (_method == "ExtraTreeClassifier")):
        return "from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier"
    elif((_method == "RandomForestClassifier") or (_method == "ExtraTreesClassifier")):
        return "from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier"
    elif(_method == "GradientBoostingClassifier"):
        return "from sklearn.ensemble import GradientBoostingClassifier"
    elif(_method == "AdaBoostClassifier"):
        return "from sklearn.ensemble import AdaBoostClassifier"

    elif(_method == "GaussianNB"):
        return "from sklearn.naive_bayes import GaussianNB"
    elif(_method == "BernoulliNB"):
        return "from sklearn.naive_bayes import BernoulliNB"
    elif(_method == "MultinomialNB"):
        return "from sklearn.naive_bayes import MultinomialNB"

    elif(_method == "NuSVC"):
        return "from sklearn.svm import NuSVC, SVC"
    elif(_method == "SVC"):
        return "from sklearn.svm import NuSVC, SVC"

    elif(_method == "KNeighborsClassifier"):
        return "from sklearn.neighbors import KNeighborsClassifier"
    elif(_method == "RadiusNeighborsClassifier"):
        return "from sklearn.neighbors import RadiusNeighborsClassifier"
    elif(_method == "CentroidClassifier"):
        return "from sklearn.neighbors import NearestCentroid"
    elif(_method == "LinearDiscriminantAnalysis"):
        return "from sklearn.discriminant_analysis import LinearDiscriminantAnalysis"
    elif(_method == "QuadraticDiscriminantAnalysis"):
        return "from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis"
    elif(_method == "LogisticRegression"):
        return "from sklearn.linear_model import LogisticRegression"
    elif(_method == "LogisticCV"):
        return "from sklearn.linear_model import LogisticRegressionCV"
    elif(_method == "RandomizedLogistic"):
        return "from sklearn.linear_model import RandomizedLogisticRegression"
    elif(_method == "PassiveAggressive"):
        return "from sklearn.linear_model import PassiveAggressiveClassifier"
    elif(_method == "Perceptron"):
        return "from sklearn.linear_model import Perceptron"
    elif(_method == "SGDClassifier"):
        return "from sklearn.linear_model import SGDClassifier"
    elif(_method == "RidgeClassifier"):
        return "from sklearn.linear_model import RidgeClassifier"
    elif(_method == "RidgeCCV"):
        return "from sklearn.linear_model import RidgeClassifierCV"

    elif(_method == "Binarizer"):
        return "from sklearn.preprocessing import Binarizer"
    elif(_method == "Imputer"):
        return "from sklearn.preprocessing import Imputer"
    elif(_method == "Normalizer"):
        return "from sklearn.preprocessing import Normalizer"
    elif(_method == "MinMaxScaler"):
        return "from sklearn.preprocessing import MinMaxScaler"
    elif(_method == "MaxAbsScaler"):
        return "from sklearn.preprocessing import MaxAbsScaler"
    elif((_method == "StandardScaler") or (_method == "RobustScaler")):
        return "from sklearn.preprocessing import StandardScaler, RobustScaler"

    elif(_method == "SelectKBest"):
        return "from sklearn.feature_selection import f_classif, chi2, SelectKBest"
    elif(_method == "VarianceThreshold"):
        return "from sklearn.feature_selection import VarianceThreshold"
    elif(_method == "SelectPercentile"):
        return "from sklearn.feature_selection import f_classif, chi2, SelectPercentile"
    elif(_method == "SelectFpr"):
        return "from sklearn.feature_selection import f_classif, chi2, SelectFpr"
    elif(_method == "SelectFdr"):
        return "from sklearn.feature_selection import f_classif, chi2, SelectFdr"
    elif(_method == "SelectFwe"):
        return "from sklearn.feature_selection import f_classif, chi2, SelectFwe"
    elif(_method == "RFE"):
        return "from sklearn.feature_selection import RFE\nfrom sklearn.svm import SVR"
    elif(_method == "RecursiveFE_CV"):
        return "from sklearn.feature_selection import RFECV\nfrom sklearn.svm import SVR"
    elif(_method == "SelectFromModel"):
        return "from sklearn.feature_selection import SelectFromModel"

    elif(_method == "TraditionalPCA"):
        return "from sklearn.decomposition import PCA"
    elif(_method == "IncrementalPCA"):
        return "from sklearn.decomposition import IncrementalPCA"

    elif(_method == "FastICA"):
        return "from sklearn.decomposition import FastICA"
    elif(_method == "FeatureAgglomeration"):
        return "from sklearn.cluster import FeatureAgglomeration"
    elif(_method == "GaussianRandomProjection"):
        return "from sklearn.random_projection import GaussianRandomProjection"
    elif(_method == "SparseRandomProjection"):
        return "from sklearn.random_projection import SparseRandomProjection"

    elif(_method == "RBFSampler"):
        return "from sklearn.kernel_approximation import RBFSampler"
    elif(_method == "Nystroem"):
        return "from sklearn.kernel_approximation import Nystroem"

    elif(_method == "PolynomialFeatures"):
        return "from sklearn.preprocessing import PolynomialFeatures"
            