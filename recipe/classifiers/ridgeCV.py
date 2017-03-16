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

from sklearn.linear_model import RidgeClassifierCV

def ridgeCV(args):

    """Uses scikit-learn's Ridge classifier with built-in cross-validation..
        
    Parameters
    ----------

    cv : int
        Determines the cross-validation splitting strategy.

    alphas : numpy array of shape [n_alphas]
        Array of alpha values to try. Regularization strength; must be a positive float. 

    class_weight : dict or ‘balanced’
        Weights associated with classes in the form {class_label: weight}. If not given, all classes are supposed to have weight one.

    normalize : boolean
        If True, the regressors X will be normalized before regression.
    
    fit_intercept : boolean
        Whether to calculate the intercept for this model.

    """

    if(args[1].find("None")!=-1):
        cross_valid = None
    else:
        cross_valid = int(args[1])

    alp = float(args[2])
    alp10 = alp*10
    alp100 = alp*100
    alpD10 = alp/10
    alpD100 = alp/100

    if(args[3].find("balanced")!=-1):
        cw = "balanced"
    elif(args[3].find("None")!=-1):
        cw = None  

    norm = False
    if(args[4].find("True")!=-1):
        norm = True

    fi = False
    if(args[5].find("True")!=-1):
        fi = True

    return RidgeClassifierCV(alphas=(alp, alp10, alp100, alpD10, alpD100), fit_intercept=fi, normalize=norm, 
        scoring=None, cv=cross_valid, class_weight=cw)