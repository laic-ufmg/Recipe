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

from sklearn.linear_model import LogisticRegressionCV

def logisticCV(args):

    """Uses scikit-learn's Logistic Regression CV, this class implements logistic regression using liblinear, newton-cg, sag of lbfgs optimizer.

    Parameters
    ----------

    cv : integer or cross-validation generator
        The default cross-validation generator used is Stratified K-Folds.

    refit : bool
        If set to True, the scores are averaged across all folds, and the coefs and the C that corresponds to the best score is taken, and a final refit is done using these parameters.

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
    if(args[1].find("None")!=-1):
        cross_valid = None
    else:
        cross_valid = int(args[1])

    ref = False
    if(args[2].find("True")!=-1):
        ref = True

    mi = int(args[3])
    sol = args[4]

    cw = None
    if(args[5].find("balanced")!=-1):
        cw = "balanced"
    elif(args[5].find("None")!=-1):
        cw = None

    fi = False
    if(args[6].find("True")!=-1):
        fi = True

    t = float(args[7])

    return LogisticRegressionCV(fit_intercept=fi, cv=cross_valid,
        scoring=None, solver=sol, tol=t, max_iter=mi, class_weight=cw, n_jobs=1,
        verbose=0, refit=ref, random_state=42)
