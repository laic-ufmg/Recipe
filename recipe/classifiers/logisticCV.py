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

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def logisticCV(args):

    """Uses scikit-learn's Logistic Regression CV, this class implements logistic regression using liblinear, newton-cg, sag of lbfgs optimizer.
        
    Parameters
    ----------

    Cs : list of floats | int
        Each of the values in Cs describes the inverse of regularization strength.
    
    cv : integer or cross-validation generator
        The default cross-validation generator used is Stratified K-Folds.

    refit : bool
        If set to True, the scores are averaged across all folds, and the coefs and the C that corresponds to the best score is taken, and a final refit is done using these parameters. 

    intercept_scaling : float
        Useful only when the solver ‘liblinear’ is used and self.fit_intercept is set to True.
    
    max_iter : int
        Maximum number of iterations of the optimization algorithm.

    solver : {‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’}
        Algorithm to use in the optimization problem.

    penalty : str, ‘l1’ or ‘l2’
        Used to specify the norm used in the penalization.

    dual : bool
        Dual or primal formulation.

    class_weight : dict or ‘balanced’, optional
        Weights associated with classes in the form {class_label: weight}.

    multi_class : str, {‘ovr’, ‘multinomial’}
        Multiclass option can be either ‘ovr’ or ‘multinomial’.

    fit_intercept : bool
        Specifies if a constant (a.k.a. bias or intercept) should be added to the decision function.

    tol : float
        Tolerance for stopping criteria of LogisticRegression


    """

    cs = int(args[1])
    if(args[2].find("None")!=-1):
        cross_valid = None
    else:
        cross_valid = int(args[2])

    ref = False
    if(args[3].find("True")!=-1):
        ref = True

    int_scal = float(args[4])

    mi = int(args[5])
    sol = args[6]
    pen = args[7]

    d = False
    if(args[8].find("True")!=-1):
        d = True

    if(args[9].find("balanced")!=-1):
        cw = "balanced"
    elif(args[9].find("None")!=-1):
        cw = None  

    mc = args[10]

    fi = False
    if(args[11].find("True")!=-1):
        fi = True

    t = float(args[12])

    return LogisticRegressionCV(Cs=cs, fit_intercept=fi, cv=cross_valid, dual=d, penalty=pen, 
        scoring=None, solver=sol, tol=t, max_iter=mi, class_weight=cw, n_jobs=1, 
        verbose=0, refit=ref, intercept_scaling=int_scal, multi_class=mc, random_state=42)