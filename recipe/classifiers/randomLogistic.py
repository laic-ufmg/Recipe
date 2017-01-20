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

from sklearn.linear_model import RandomizedLogisticRegression

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def randomLogistic(args):

    """Uses scikit-learn's Randomized Logistic Regression, works by subsampling the training data and fitting a L1-penalized 
    LogisticRegression model where the penalty of a random subset of coefficients has been scaled.
        
    Parameters
    ----------

    C : float
        The regularization parameter C in the LogisticRegression.
    
    scaling : float
        The s parameter used to randomly scale the penalty of different features

    sample_fraction : float
        The fraction of samples to be used in each randomized design. Should be between 0 and 1. If 1, all samples are used.

    n_resampling : int
        Number of randomized models.

    selection_threshold : float
        The score above which features should be selected.

    normalize : boolean
        If True, the regressors X will be normalized before regression.

    fit_intercept : boolean
        whether to calculate the intercept for this model. If set to false, no intercept will be used in calculations (e.g. data is expected to be already centered).

    tol : float
        tolerance for stopping criteria of LogisticRegression


    """

    c = float(args[1])
    scal = float(args[2])
    s_frac = float(args[3])
    n_res = int(args[4])
    st = float(args[5])

    norm = False
    if(args[6].find("True")!=-1):
        norm = True

    fi = False
    if(args[7].find("True")!=-1):
        fi = True

    t = float(args[8])

    return RandomizedLogisticRegression(C=c, scaling=scal, sample_fraction=s_frac, n_resampling=n_res, 
        selection_threshold=st, tol=t, fit_intercept=fi, verbose=False, normalize=norm, 
        random_state=42, n_jobs=1, pre_dispatch='1*n_jobs')