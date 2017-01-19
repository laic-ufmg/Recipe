# -*- coding: utf-8 -*-

"""
Copyright 2016 Walter José

This file is part of the RECIPE Algorithm.

The RECIPE is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

RECIPE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. See http://www.gnu.org/licenses/.

"""

from sklearn.random_projection import SparseRandomProjection

def sparseR(args):

	"""Uses scikit-learn's SparseRandomProjection to reduce dimensionality through sparse random projection.
		
	Parameters
	----------

   	density : float in range [0, 1]
		Ratio of non-zero component in the random projection matrix.
    
    n_components: int
        The number of components to keep

    eps : strictly positive float
		Parameter to control the quality of the embedding according to the Johnson-Lindenstrauss lemma when n_components is set to ‘auto’.

	dense_output : bool

		If True, ensure that the output of the random projection is a dense numpy array even if the input and random projection matrix are both sparse. In practice, if the number of components is small the number of zero components in the projected data will be very small and it will be more CPU and memory efficient to use a dense representation.
		If False, the projected data uses a sparse representation if the input is sparse.

	"""

	if(args[1].find("auto")!=-1):
		dense = "auto"
	else:
		dense = float(args[1])

	dens_out = False
	if(args[2].find("True")!=-1):
		dens_out = True

	epsilon = float(args[3])
	n_comp = int(args[4])

	return SparseRandomProjection(n_components=n_comp, density=dense, eps=epsilon, dense_output=dens_out, random_state=42)
