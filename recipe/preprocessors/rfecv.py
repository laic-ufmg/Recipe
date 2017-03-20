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

from sklearn.feature_selection import RFECV
from sklearn.svm import SVR


def rfecv(args):

	"""Uses scikit-learn's RFECV, feature ranking with recursive feature elimination and cross-validated selection of the best number of features..
		
	Parameters
	----------

	cv : int, cross-validation generator or an iterable
		Determines the cross-validation splitting strategy.

	scoring : string
		A string (see model evaluation documentation) or a scorer callable object / function with signature scorer

	step : int or float
		If greater than or equal to 1, then step corresponds to the (integer) number of features to remove at each iteration. 
		If within (0.0, 1.0), then step corresponds to the percentage (rounded down) of features to remove at each iteration.

	"""

	estimator = SVR(kernel="linear")

	cross_valid = int(args[1])

	if(args[2].find("None")!=-1):
		score = None
	else:
		score = args[2]

	s = float(args[3])      
	return RFECV(estimator, step=s, cv=cross_valid, scoring=score)