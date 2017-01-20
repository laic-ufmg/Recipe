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
from sklearn.ensemble import AdaBoostClassifier

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def ada(args):

    """Uses scikit-learn's AdaBoostClassifier, an AdaBoostClassifier is a meta-estimator that begins by fitting a classifier on the original dataset and then fits additional 
    copies of the classifier on the same dataset but where the weights of incorrectly classified instances are adjusted such that subsequent classifiers focus more on difficult cases.
    
    Parameters
    ----------

    algorithm : {‘SAMME’, ‘SAMME.R’}
        If ‘SAMME.R’ then use the SAMME.R real boosting algorithm. base_estimator must support calculation of class probabilities.

    learning_rate : float
        learning rate shrinks the contribution of each tree by learning_rate. There is a trade-off between learning_rate and n_estimators.

    n_estimators : int
        The number of boosting stages to perform. Gradient boosting is fairly robust to over-fitting so a large number usually results in better performance.

    """
    
    alg = args[1]
    est = int(args[2])
    lr = float(args[3])

    return AdaBoostClassifier(n_estimators=est, learning_rate=lr, algorithm=alg, random_state=42)