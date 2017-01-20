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

from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def specificTree(args):

    """Uses scikit-learn's ExtraTreesClassifier or RandomForestClassifier:
        ExtraTreesClassifier: This class implements a meta estimator that fits a number of randomized decision trees
        RandomForestClassifier: A random forest is a meta estimator that fits a number of decision tree classifiers on various sub-samples of the dataset and use averaging to improve the predictive accuracy and control over-fitting.
    
    Parameters
    ----------

    criterion : string
        The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “entropy” for the information gain.

    bootstrap : bool
        Whether bootstrap samples are used when building trees.

    oob_score : bool
        Whether to use out-of-bag samples to estimate the generalization accuracy.

    class_weight : dict, list of dicts, “balanced”,
        “balanced_subsample” or None, optional (default=None) Weights associated with classes in the form {class_label: weight}.

    n_estimators : integer
        The number of trees in the forest.

    warm_start : bool
        When set to True, reuse the solution of the previous call to fit and add more estimators to the ensemble, otherwise, just fit a whole new forest.

    max_features : int, float, string or None
        The number of features to consider when looking for the best split:

    max_depth : integer or None
        The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.

    min_weight_fraction_leaf : float
        The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node.
    
    max_leaf_nodes : int or None
        Grow trees with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes.

    """

    crit='gini'
    if(args[1].find("None")==-1):
        crit=args[1]

    bstp = False
    if(args[2].find("True")!=-1):
        bstp = True

    os = False
    if(args[3].find("True")!=-1):
        os = True

    if(args[4].find("balanced")!=-1):
        cw = "balanced"
    elif(args[4].find("balanced_subsample")!=-1):
        cw = "balanced_subsample"
    elif(args[4].find("None")!=-1):
        cw = None

    est=10
    if(args[5].find("None")==-1):
        est = int(args[5])

    ws = bool(0)
    if(args[6].find("True")!=-1):
        ws = bool(1)

    if(args[7].find("sqrt")!=-1):
        mf = "sqrt"
    elif(args[7].find("log2")!=-1):
        mf = "log2"
    elif(args[7].find("None")!=-1):
        mf = None
    elif(args[7].find("auto")!=-1):
        mf = "auto"  
    else:
        mf = float(args[7])

    if(args[8].find("None")!=-1):
        md = None
    else:
        md = int(args[8])

    mwfl=0.0
    if(args[9].find("None")==-1):
        mwfl = float(args[9])

    if(args[10].find("None")!=-1):
        mln = None
    else:
        mln = int(args[10])

    if(args[0].find("RandomForestClassifier")!=-1):     
        return RandomForestClassifier(n_estimators=est, criterion=crit, max_depth=md, 
            min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=mwfl, max_features=mf, 
            max_leaf_nodes=mln, bootstrap=bstp, oob_score=os, n_jobs=1, random_state=42, 
            verbose=0, warm_start=ws, class_weight=cw)
    else:
        return ExtraTreesClassifier(n_estimators=est, criterion=crit, max_depth=md, 
            min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=mwfl, max_features=mf, 
            max_leaf_nodes=None, bootstrap=False, oob_score=False, n_jobs=1, random_state=42, verbose=0, 
            warm_start=False, class_weight=None)