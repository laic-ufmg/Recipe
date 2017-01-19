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

from sklearn.neighbors import KNeighborsClassifier

def kNeighboors(args):

    """Uses scikit-learn's KNeighborsClassifier, classifier implementing the k-nearest neighbors vote.
    
    Parameters
    ----------
  
    n_neighbors : int
        Number of neighbors to use by default for k_neighbors queries.

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

    k=5
    if(args[1].find("None")==-1):
        k = int(args[1])
    
    weig='uniform'
    if(args[2].find("None")==-1):
        weig = args[2]
    
    algo='auto'
    if(args[3].find("None")==-1):
        algo = args[3]
    
    leaf=30
    if(args[4].find("None")==-1):
        leaf = int(args[4])
    
    pvalue=2
    if(args[5].find("None")==-1):
        pvalue = int(args[5])
    
    met='minkowski'
    if(args[6].find("None")==-1):
        met = args[6]
    
    return KNeighborsClassifier(n_neighbors=k, weights=weig, algorithm=algo, 
        leaf_size=leaf, p=pvalue, metric=met, metric_params=None)