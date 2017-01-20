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

from sklearn.preprocessing import StandardScaler, RobustScaler

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def scaler(args):

    """Uses scikit-learn's RobustScaler and StandardScaler:
        RobustScaler: Scale features using statistics that are robust to outliers.
        StandardScaler: Standardize features by removing the mean and scaling to unit variance
                
    Parameters
    ----------
    
    scaler: RobustScaler or StandardScaler
        Decides which scaler is used

        RobustScaler
        ---------------

        with_centering : boolean
            If True, center the data before scaling.

        with_scaling : boolean
            If True, scale the data to interquartile range.

        StandardScaler
        ----------------
        
            with_mean : boolean
                If True, center the data before scaling.

            with_std : boolean
                If True, scale the data to unit variance (or equivalently, unit standard deviation).
 
    """

    std_or_scaling = False
    if(args[1].find("True")!=-1):
        std_or_scaling = True

    centering = args[2]

    if(args[0].find("RobustScaler")!=-1):
        return RobustScaler(with_centering=centering, with_scaling=std_or_scaling, copy=True)
    elif(args[0].find("StandardScaler")!=-1):
        return StandardScaler(copy=True, with_mean=centering, with_std=std_or_scaling)