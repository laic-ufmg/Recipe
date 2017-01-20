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

from sklearn.linear_model import PassiveAggressiveClassifier

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def passive(args):

    """Uses scikit-learn's Passive Aggressive Classifier
        
    Parameters
    ----------

    C : float
        Maximum step size (regularization).

    fit_intercept : bool
        Whether the intercept should be estimated or not. If False, the data is assumed to be already centered.

    n_iter : int
        The number of passes over the training data (aka epochs). Defaults to 5.

    shuffle : bool
        Whether or not the training data should be shuffled after each epoch.

    loss : string
        The loss function to be used: hinge: equivalent to PA-I in the reference paper. squared_hinge: equivalent to PA-II in the reference paper.

    warm_start : bool
        When set to True, reuse the solution of the previous call to fit as initialization, otherwise, just erase the previous solution.
  
    class_weight : dict, {class_label: weight} or “balanced” or None, 
        Preset for the class_weight fit parameter.
    """

    c=1.0
    if(args[1].find("None")!=-1):
        c=float(args[1])

    fi = False
    if(args[2].find("True")!=-1):
        fi = True

    it=5
    if(args[3].find("None")!=-1):
        it = int(args[3])

    sffle = False
    if(args[4].find("True")!=-1):
        sffle = True

    loss_sgd='hinge'
    if(args[5].find("None")!=-1):
        loss_sgd = args[5]

    warm = False
    if(args[6].find("True")!=-1):
        warm = True

    if(args[7].find("balanced")!=-1):
        cw = "balanced"
    elif(args[7].find("None")!=-1):
        cw = None  

    return PassiveAggressiveClassifier(C=c, fit_intercept=fi, n_iter=it, shuffle=sffle, 
        verbose=0, loss=loss_sgd, n_jobs=1, random_state=42, warm_start=warm, class_weight=cw)