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

def svc(args):

	"""Uses scikit-learn's SVC or NuSVC, classes capable of performing multi-class classification on a dataset.

    Parameters
    ----------

	kernel : string
	    Specifies the kernel type to be used in the algorithm. It must be one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable.

	degree : int
		Degree of the polynomial kernel function (‘poly’). Ignored by all other kernels.

	tol : float
	    Tolerance for stopping criterion.

	max_iter : int
	    Hard limit on iterations within solver, or -1 for no limit.

	class_weight : {dict, ‘balanced’}
	    Set the parameter C of class i to class_weight[i]*C for SVC. If not given, all classes are supposed to have weight one.

    """

	kern=args[1]
	deg=int(args[2])

	t = float(args[3])
	maxit = int(args[4])

	if(args[5].find("balanced")!=-1):
		cw = "balanced"
	elif(args[5].find("None")!=-1):
		cw = None

	if(args[0].find("SVC")!=-1):
		return SVC(kernel=kern,degree=deg,tol=t,max_iter=maxit,class_weight=cw,random_state=42)
	elif(args[0].find("NuSVC")!=-1):
		return NuSVC(kernel=kern,degree=deg,tol=t,max_iter=maxit,class_weight=cw,random_state=42)
