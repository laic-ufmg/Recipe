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

from sklearn.decomposition import IncrementalPCA

def ipca(args):

	"""Uses scikit-learn's IncrementalPCA, a linear dimensionality reduction using Singular Value Decomposition of centered data,
	keeping only the most significant singular vectors to project the data to a lower dimensional space.
		
	Parameters
	----------

	whiten : boolean
		When True the components_ vectors are divided by n_samples times components_ to ensure uncorrelated outputs with unit component-wise variances.

	n_components : int
		Number of components to keep.

	"""

	whit = False
	if(args[1].find("True")!=-1):
		whit = True

	comp = int(args[2])


	ipca = IncrementalPCA(n_components=comp,whiten=whit) 

	return ipca
