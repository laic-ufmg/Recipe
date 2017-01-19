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

from sklearn.cluster import FeatureAgglomeration

def fag(args):

	"""Uses scikit-learn's FeatureAgglomeration agglomerate features.
		
	Parameters
	----------

	affinity : string
		Metric used to compute the linkage. Can be “euclidean”, “l1”, “l2”, “manhattan”, “cosine”, or ‘precomputed’. If linkage is “ward”, 
		only “euclidean” is accepted.

	linkage : {“ward”, “complete”, “average”}
		Which linkage criterion to use. 
		The linkage criterion determines which distance to use between sets of features. 
		The algorithm will merge the pairs of cluster that minimize this criterion.

	compute_full_tree : bool or ‘auto’
		Stop early the construction of the tree at n_clusters


	n_clusters : int
		The number of clusters to find.

	"""

	affi = args[1]
	link = args[2]

	cft = False
	if(args[3].find("True")!=-1):
		cft = True

	n_clust = int(args[4])

	return FeatureAgglomeration(n_clusters=n_clust, affinity=affi, 
		connectivity=None, n_components=None, 
		compute_full_tree=cft, linkage=link)