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

from sklearn.linear_model import Perceptron

def perceptron(args):

    """Uses scikit-learn's Perceptron, a classification algorithm that makes its predictions based on a linear predictor function combining a set of weights with the feature vector. 
    
    Parameters
    ----------
  
    penalty : str, ‘none’, ‘l2’, ‘l1’, or ‘elasticnet’
        The penalty (aka regularization term) to be used.

    alpha : float
        Constant that multiplies the regularization term. 

    fit_intercept : bool
        Whether the intercept should be estimated or not. If False, the data is assumed to be already centered.

    n_iter : int
        The number of passes over the training data (aka epochs).

    shuffle : bool
        Whether or not the training data should be shuffled after each epoch. Defaults to True.

    eta0 : double
        The initial learning rate for the ‘constant’ or ‘invscaling’ schedules.

    class_weight : dict, {class_label: weight} or “balanced” or None
        Preset for the class_weight fit parameter. Weights associated with classes. If not given, all classes are supposed to have weight one.

    warm_start : bool
        When set to True, reuse the solution of the previous call to fit as initialization, otherwise, just erase the previous solution.

    """

    penal = args[1]
    alp = float(args[2])

    fi = False
    if(args[3].find("True")!=-1):
        fi = True

    it = int(args[4])

    sffle = False
    if(args[5].find("True")!=-1):
        sffle = True

    eta = float(args[6])

    if(args[7].find("balanced")!=-1):
        cw = "balanced"
    elif(args[7].find("None")!=-1):
        cw = None  

    warm = False
    if(args[8].find("True")!=-1):
        warm = True

    return Perceptron(penalty=penal, alpha=alp, fit_intercept=fi, n_iter=it, 
        shuffle=sffle, verbose=0, eta0=eta, n_jobs=1, random_state=42, class_weight=cw, warm_start=warm)