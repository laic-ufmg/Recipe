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

from sklearn.linear_model import LogisticRegression

def logistic(args):

    """Uses scikit-learn's Logistic Regression, this class implements logistic regression using liblinear, newton-cg, sag of lbfgs optimizer.

    Parameters
    ----------

    warm_start : bool
        When set to True, reuse the solution of the previous call to fit as initialization, otherwise, just erase the previous solution. Useless for liblinear solver.

    max_iter : int
        Maximum number of iterations of the optimization algorithm.

    solver : {‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’}
        Algorithm to use in the optimization problem.


    class_weight : dict or ‘balanced’, optional
        Weights associated with classes in the form {class_label: weight}.

    fit_intercept : bool
        Specifies if a constant (a.k.a. bias or intercept) should be added to the decision function.

    tol : float
        Tolerance for stopping criteria of LogisticRegression

    """

    warm = False
    if(args[1].find("True")!=-1):
        warm = True

    mi=100
    if(args[2].find("None")!=-1):
        mi = int(args[2])

    sol='liblinear'
    if(args[3].find("None")!=-1):
        sol = args[3]

    cw=None
    if(args[4].find("balanced")!=-1):
        cw = "balanced"
    elif(args[4].find("None")!=-1):
        cw = None

    fi = False
    if(args[5].find("True")!=-1):
        fi = True

    t=0.0001
    if(args[6].find("None")!=-1):
        t = float(args[6])

    return LogisticRegression(tol=t, fit_intercept=fi,class_weight=cw, random_state=42,
    solver=sol, max_iter=mi, verbose=0, warm_start=warm)
