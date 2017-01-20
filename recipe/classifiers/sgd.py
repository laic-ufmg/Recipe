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

from sklearn.linear_model import SGDClassifier

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def sgd(args):

    """Uses scikit-learn's SGDClassifier, this estimator implements regularized linear models with stochastic gradient descent (SGD) learning: 
    the gradient of the loss is estimated each sample at a time and the model is updated along the way with a decreasing strength schedule (aka learning rate)
        
    Parameters
    ----------

    loss : str, ‘hinge’, ‘log’, ‘modified_huber’, ‘squared_hinge’, ‘perceptron’, or a 
        regression loss: ‘squared_loss’, ‘huber’, ‘epsilon_insensitive’, or ‘squared_epsilon_insensitive’
        The loss function to be used.

    l1_ratio : float
        The Elastic Net mixing parameter,

    epsilon : float
        Epsilon in the epsilon-insensitive loss functions;

    learning_rate : string
        The learning rate schedule:

    power_t : double
        The exponent for inverse scaling learning rate [default 0.5].

    average : bool or int
        When set to True, computes the averaged SGD weights and stores the result in the coef_ attribute.
        If set to an int greater than 1, averaging will begin once the total number of samples seen reaches average.
  
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

    loss_sgd = args[1]
    l1 = float(args[2])
    ep = float(args[3])
    lr_sgd = args[4]
    pt = float(args[5])

    if(args[6].find("True")!=-1):
        av = True
    elif(args[6].find("False")!=-1):
        av = False
    else:
        av = int(args[6])

    penal = args[7]
    alp = float(args[8])

    fi = False
    if(args[9].find("True")!=-1):
        fi = True

    it = int(args[10])

    sffle = False
    if(args[11].find("True")!=-1):
        sffle = True

    eta = float(args[12])

    if(args[13].find("balanced")!=-1):
        cw = "balanced"
    elif(args[13].find("None")!=-1):
        cw = None  

    warm = False
    if(args[14].find("True")!=-1):
        warm = True

    return SGDClassifier(loss=loss_sgd, penalty=penal, alpha=alp, l1_ratio=l1, 
        fit_intercept=fi, n_iter=it, shuffle=sffle, verbose=0, epsilon=ep, n_jobs=1, 
        random_state=42, learning_rate=lr_sgd, eta0=eta, power_t=pt, 
        class_weight=cw, warm_start=warm, average=av)