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

from sklearn.kernel_approximation import RBFSampler


def rbf_sampler(args):

	"""Uses scikit-learn's RBFSampler to constructs an approximate feature map for an arbitrary kernel using a subset of the data as basis.
		
	Parameters
	----------		
	gamma: float
		Gamma parameter for the kernels.
	
	n_components: int
		The number of components to keep
		
	"""

	g = float(args[1])
	comp = int(args[2])

	return RBFSampler(gamma=g, n_components=comp, random_state=42)