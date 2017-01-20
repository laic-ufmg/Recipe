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

from sklearn.feature_selection import VarianceThreshold

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def threshold(args):

	"""Uses scikit-learn's VarianceThreshold, feature selector that removes all low-variance features.
                
    Parameters
    ----------
    	None
    """

	return VarianceThreshold()