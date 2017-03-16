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

from sklearn.svm import NuSVC, SVC

def SVC(args):

	"""Uses scikit-learn's SVC or NuSVC, classes capable of performing multi-class classification on a dataset.
    
    Parameters
    ----------
  
    nu or C : float
		Penalty parameter C of the error term.

	kernel : string
	    Specifies the kernel type to be used in the algorithm. It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable.
    
	degree : int
		Degree of the polynomial kernel function (‘poly’). Ignored by all other kernels.

	gamma : float
	    Kernel coefficient for ‘rbf’, ‘poly’ and ‘sigmoid’. If gamma is ‘auto’ then 1/n_features will be used instead.

	coef0 : float
	    Independent term in kernel function. It is only significant in ‘poly’ and ‘sigmoid’.

	probability : boolean
	    Whether to enable probability estimates. This must be enabled prior to calling fit, and will slow down that method.

	shrinking : boolean
	    Whether to use the shrinking heuristic.

	decision_function_shape : ‘ovo’, ‘ovr’ or None
	    Whether to return a one-vs-rest (‘ovr’) decision function of shape (n_samples, n_classes) as all other classifiers

	tol : float
	    Tolerance for stopping criterion.

	max_iter : int
	    Hard limit on iterations within solver, or -1 for no limit.

	class_weight : {dict, ‘balanced’}
	    Set the parameter C of class i to class_weight[i]*C for SVC. If not given, all classes are supposed to have weight one.

    """

	nu_or_c = float(args[1])
	kern=args[2]
	deg=int(args[3])
	
	if(args[4].find("auto")!=-1):
		gm = "auto"
	else:
		gm = float(args[4])
	
	coef = float(args[5])

	prob = False
	if(args[6].find("True")!=-1):
		prob = True

	shkng = False
	if(args[7].find("True")!=-1):
		shkng = True

	if(args[8].find("ovo")!=-1):
		dfs = "ovo"
	elif(args[8].find("ovr")!=-1):
		dfs = "ovr"
	elif(args[8].find("None")!=-1):
		dfs = None

	t = float(args[9])
	maxit = int(args[10])

	if(args[11].find("balanced")!=-1):
		cw = "balanced"
	elif(args[11].find("None")!=-1):
		cw = None  

	if(args[0].find("SVC")!=-1): 
		return SVC(C=nu_or_c, kernel=kern, degree=deg, gamma=gm, coef0=coef, shrinking=shkng, 
			probability=prob, tol=t, cache_size=200, class_weight=cw, verbose=False, max_iter=-1, 
			decision_function_shape=dfs, random_state=42)
	elif(args[0].find("NuSVC")!=-1):
		return NuSVC(nu=nu_or_c, kernel=kern, degree=deg, gamma=gm, coef0=coef, shrinking=shkng, 
			probability=prob, tol=t, cache_size=200, class_weight=cw, verbose=False, max_iter=maxit, 
			decision_function_shape=dfs, random_state=42)