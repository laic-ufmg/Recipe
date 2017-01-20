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

from sklearn.kernel_approximation import Nystroem

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def nystroem(args):

	"""Uses scikit-learn's Nystroem to constructs an approximate feature map for an arbitrary kernel using a subset of the data as basis.
		
	Parameters
	----------
	kernel: int
        Kernel type is selected from scikit-learn's provided types:
            'sigmoid', 'polynomial', 'additive_chi2', 'poly', 'laplacian', 'cosine', 'linear', 'rbf', 'chi2'
        Input integer is used to select one of the above strings.
    
    gamma: float
        Gamma parameter for the kernels.
    
    n_components: int
        The number of components to keep

    degree: float
    	Degree of the polynomial kernel. Ignored by other kernels.

    coef0:
    	Zero coefficient for polynomial and sigmoid kernels. Ignored by other kernels.

	"""
		
	kern = args[1]
	g = float(args[2])
	deg = int(args[3])
	coef = float(args[4])
	comp = int(args[5])

	return Nystroem(kernel=kern, gamma=g, coef0=coef, degree=deg, kernel_params=None, n_components=comp, random_state=42)