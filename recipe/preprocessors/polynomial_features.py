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

from sklearn.preprocessing import PolynomialFeatures

def polynomial_features(args):

	"""Uses scikit-learn's PolynomialFeatures to generate a new feature matrix consisting of all polynomial combinations of the features with 
	degree less than or equal to the specified degree.
	
	Parameters
	----------
	degree : int
		The degree of the polynomial features.

	interaction_only : bool
		If true, only interaction features are produced.

	include_bias : bool
		If true, then include a bias column, the feature in which all polynomial powers are zero

	"""
	deg = int(args[1])

	io = False
	if(args[2].find("True")!=-1):
		io = True

	ib = False
	if(args[3].find("True")!=-1):
		ib = True

	poly = PolynomialFeatures(degree=deg, interaction_only=io, include_bias=ib)

	return poly
