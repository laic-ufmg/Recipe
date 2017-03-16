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

from sklearn.linear_model import RidgeClassifier

def ridge(args):

	"""Uses scikit-learn's RidgeClassifier using Ridge regression.
        
    Parameters
    ----------

    max_iter : int
	    Maximum number of iterations for conjugate gradient solver. The default value is determined by scipy.sparse.linalg.

	copy_X : boolean
	    If True, X will be copied; else, it may be overwritten.

	solver : {‘auto’, ‘svd’, ‘cholesky’, ‘lsqr’, ‘sparse_cg’, ‘sag’}
	    Solver to use in the computational routines:

	tol : float
	    Precision of the solution.

	alpha : float
	    Regularization strength; must be a positive float.

	normalize : boolean, optional, default False
	    If True, the regressors X will be normalized before regression.
  
  	fit_intercept : boolean
	    Whether to calculate the intercept for this model. If set to false, no intercept will be used in calculations (e.g. data is expected to be already centered).

    """

	mi = int(args[1])
	cp_x = False
	if(args[2].find("True")!=-1):
		cp_x = True

	sol = args[3]

	t = float(args[4])

	alp = float(args[5])

	if(args[6].find("balanced")!=-1):
		cw = "balanced"
	elif(args[6].find("None")!=-1):
		cw = None  

	norm = False
	if(args[7].find("True")!=-1):
		norm = True

	fi = False
	if(args[8].find("True")!=-1):
		fi = True

	return RidgeClassifier(alpha=alp, fit_intercept=fi, normalize=norm, copy_X=cp_x, 
		max_iter=mi, tol=t, class_weight=cw, solver=sol, random_state=42)