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

from sklearn.naive_bayes import BernoulliNB

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def bernoulliNB(args):

    """Uses scikit-learn's BernoulliNB, a naive bayes classifier for multinomial models
    
    Parameters
    ----------
  
    alpha : float
        Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).
    
    binarize : float or None
        Threshold for binarizing (mapping to booleans) of sample features. If None, input is presumed to already consist of binary vectors.

    fit_prior : boolean
        Whether to learn class prior probabilities or not. If false, a uniform prior will be used.

    """

    alp = 1.0
    if(args[2].find("None")==-1):
        alp = float(args[2])

    fit = False
    if(args[3].find("True")!=-1):
        fit = True

    bina = 0.0
    if(args[1].find("None")==-1):
        bina=float(args[1])

    return BernoulliNB(alpha=alp, binarize=bina, fit_prior=fit, class_prior=None)