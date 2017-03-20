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

from sklearn.feature_selection import f_classif, chi2, SelectKBest

def selectKBest(args):

    """Uses scikit-learn's SelectKBest, select features according to the k highest scores.
                
    Parameters
    ----------

    score_func : callable
        Function taking two arrays X and y, and returning a pair of arrays (scores, pvalues).

    k : int or “all”
        Number of top features to select. The “all” option bypasses selection, for use in a parameter search.

    """
    
    if(args[2]=="chi2"):
        selector = SelectKBest(chi2, k=int(args[1]))
    elif(args[2]=="f_classif"):
        selector = SelectKBest(f_classif, k=int(args[1]))

    return selector