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
    
    C : float
        Inverse of regularization strength; must be a positive float.

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

    warm = False
    if(args[1].find("True")!=-1):
        warm = True

    c=1.0
    if(args[2].find("None")!=-1):
        c = float(args[2])

    int_scal=1
    if(args[3].find("None")!=-1):
        int_scal = float(args[3])

    mi=100
    if(args[4].find("None")!=-1):
        mi = int(args[4])
    
    sol='liblinear'
    if(args[5].find("None")!=-1):
        sol = args[5]
    
    pen='l2'
    if(args[6].find("None")!=-1):
        pen = args[6]

    d = False
    if(args[7].find("True")!=-1):
        d = True

    if(args[8].find("balanced")!=-1):
        cw = "balanced"
    elif(args[8].find("None")!=-1):
        cw = None  

    mc='ovr'
    if(args[9].find("None")!=-1):
        mc = args[9]

    fi = False
    if(args[10].find("True")!=-1):
        fi = True

    t=0.0001  
    if(args[11].find("None")!=-1):
        t = float(args[11])

    return LogisticRegression(penalty=pen, dual=d, tol=t, C=c, fit_intercept=fi, 
        intercept_scaling=int_scal, class_weight=cw, random_state=42, solver=sol, max_iter=mi, 
        multi_class=mc, verbose=0, warm_start=warm, n_jobs=1)