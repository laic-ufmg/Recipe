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

from sklearn.naive_bayes import MultinomialNB

def multinomialNB(args):

    """Uses scikit-learn's MultinomialNB, a naive bayes classifier for multinomial models
    
    Parameters
    ----------
  
    alpha : float
        Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).

    fit_prior : bool
        Whether to learn class prior probabilities or not. If false, a uniform prior will be used.

    """

    alp = float(args[1])
    fit = False
    if(len(args) >= 3 and args[2].find("fit_prior")!=-1):
        fit = True

    return MultinomialNB(alpha=alp, fit_prior=fit)