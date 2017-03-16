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

from sklearn.random_projection import GaussianRandomProjection

def gaussianR(args):

	"""Uses scikit-learn's GaussianRandomProjection to reduce dimensionality through Gaussian random projection.
		
	Parameters
	----------

	n_components: int
		The number of components to keep

	eps : strictly positive float
		Parameter to control the quality of the embedding according to the Johnson-Lindenstrauss lemma when n_components is set to ‘auto’.

	"""

	epsilon = float(args[1])
	n_comp = int(args[2])

	return GaussianRandomProjection(n_components=n_comp, eps=epsilon, random_state=42)