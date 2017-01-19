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

def treeEstimator(args):

    """Uses scikit-learn's ExtraTreeClassifier or DecisionTreeClassifier
    
    Parameters
    ----------

    criterion : string
        The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “entropy” for the information gain.

    splitter : string
        The strategy used to choose the split at each node. Supported strategies are “best” to choose the best split and “random” to choose the best random split.

    class_weight : dict, list of dicts, “balanced”,
        “balanced_subsample” or None, optional (default=None) Weights associated with classes in the form {class_label: weight}.
    
    presort : bool
        Whether to presort the data to speed up the finding of best splits in fitting.

    max_features : int, float, string or None
        The number of features to consider when looking for the best split:
    
    max_depth : int or None
        The maximum depth of the tree.

    min_weight_fraction_leaf : float
        The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node.
    
    max_leaf_nodes : int or None
        Grow a tree with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes.


    """


    crit = "gini"
    if(args[1].find("None")==-1):
        crit=args[1]

    split="best"
    if(args[2].find("None")==-1):
        split=args[2]

    if(args[3].find("balanced")!=-1):
        cw = "balanced"
    elif(args[3].find("None")!=-1):
        cw = None  

    psort = False
    if(args[4].find("True")!=-1):
        psort = True
    elif(args[4].find("auto")!=-1):
        psort = "auto"

    if(args[5].find("sqrt")!=-1):
        mf = "sqrt"
    elif(args[5].find("log2")!=-1):
        mf = "log2"
    elif(args[5].find("None")!=-1):
        mf = None
    else:
        mf = float(args[5])

    if(args[6].find("None")!=-1):
        md = None
    else:
        md = int(args[6])

    mwfl = 0.0
    if(args[7].find("None")==-1):
        mwfl=float(args[7])

    if(args[8].find("None")!=-1):
        mln = None
    else:
        mln = int(args[8])

    if(args[0].find("DecisionTreeClassifier")!=-1):
        return DecisionTreeClassifier(criterion=crit, splitter=split, 
            max_depth=md, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=mwfl, 
            max_features=mf, random_state=42, max_leaf_nodes=mln, class_weight=cw, presort=psort)
    else:
        return ExtraTreeClassifier(criterion=crit, splitter=split, 
            max_depth=md, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=mwfl, 
            max_features=mf, random_state=42, max_leaf_nodes=mln, class_weight=cw)