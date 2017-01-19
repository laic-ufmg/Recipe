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

from sklearn.neighbors import RadiusNeighborsClassifier

def radiusNeighboors(args):
    
    """Uses scikit-learn's RadiusNeighborsClassifier, a classifier implementing a vote among neighbors within a given radius.
    
    Parameters
    ----------
  
    radius : float
        Range of parameter space to use by default for :meth`radius_neighbors` queries.

    weights : str or callable
        weight function used in prediction.

    algorithm : {‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’}
        Algorithm used to compute the nearest neighbors

    leaf_size : int
        Leaf size passed to BallTree or KDTree. This can affect the speed of the construction and query, as well as the memory required to store the tree.

    metric : string 
        The distance metric to use for the tree.

    p : integer
        Power parameter for the Minkowski metric.

    """

    r = float(args[1])
    weig = args[2]
    algo = args[3]
    leaf = int(args[4])
    pvalue = int(args[5])
    met = args[6]
    
    return RadiusNeighborsClassifier(radius=r, weights=weig, algorithm=algo, leaf_size=leaf, p=pvalue, 
        metric=met, outlier_label=100000, metric_params=None)