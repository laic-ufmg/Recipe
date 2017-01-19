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

from sklearn.feature_selection import SelectFromModel

def selectfm(args):

	"""Uses scikit-learn's SelectFromModel, a meta-transformer for selecting features based on importance weights.
		
	Parameters
	----------

	threshold : string, float
		The threshold value to use for feature selection.

	"""

	estimator = SVR(kernel="linear")

	if(args[1].find("None")!=-1):
		tshld = None
	elif(args[1].find("mean")!=-1):
		tshld = "mean"
	elif(args[1].find("median")!=-1):
		tshld = "median"
	else:
		tshld = float(args[1])

	pref = False
	if(args[2].find("True")!=-1):
		pref = True

	return SelectFromModel(estimator, threshold=tshld, prefit=False)