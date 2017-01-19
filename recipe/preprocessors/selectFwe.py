# -*- coding: utf-8 -*-

"""
Copyright 2016 Walter José

This file is part of the RECIPE Algorithm.

The RECIPE is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

RECIPE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. See http://www.gnu.org/licenses/.

"""

from sklearn.feature_selection import f_classif, chi2, SelectFwe

def selectFwe(args):

    """Uses scikit-learn's SelectFWE, select the p-values corresponding to Family-wise error rate.
        
    Parameters
    ----------

    score_func : callable
        Function taking two arrays X and y, and returning a pair of arrays (scores, pvalues).

    alpha : float, optional
        The highest uncorrected p-value for features to keep.

    """

    if(args[2]=="chi2"):
        selector = SelectFwe(chi2, alpha=float(args[1]))
    elif(args[2]=="f_classif"):
        selector = SelectFwe(f_classif, alpha=float(args[1]))
                
    return selector