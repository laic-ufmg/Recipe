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

from sklearn.feature_selection import RFE

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def rfe(args):

	"""Uses scikit-learn's RFECV, feature ranking with recursive feature elimination.
		
	Parameters
	----------

	n_features_to_select : int or None
		The number of features to select. If None, half of the features are selected.

	step : int or float
		If greater than or equal to 1, then step corresponds to the (integer) number of features to remove at each iteration. 
		If within (0.0, 1.0), then step corresponds to the percentage (rounded down) of features to remove at each iteration.

	"""

	estimator = SVR(kernel="linear")

	nfs = None
	if(args[1].find("None")==-1):
		nfs = int(args[1])

	s = float(args[2])
				
	return RFE(estimator, n_features_to_select=nfs, step=s, estimator_params=None)
