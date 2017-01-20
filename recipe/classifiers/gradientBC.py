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
from sklearn.ensemble import GradientBoostingClassifier

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def gradientBC(args):

	"""Uses scikit-learn's GradientBoostingClassifier, GB builds an additive model in a forward stage-wise fashion; it allows for the optimization of arbitrary differentiable loss functions.
    
    Parameters
    ----------

    loss : {‘deviance’, ‘exponential’}
	    loss function to be optimized. ‘deviance’ refers to deviance (= logistic regression) for classification with probabilistic outputs.

	learning_rate : float
	    learning rate shrinks the contribution of each tree by learning_rate. There is a trade-off between learning_rate and n_estimators.

	n_estimators : int
	    The number of boosting stages to perform. Gradient boosting is fairly robust to over-fitting so a large number usually results in better performance.

	subsample : float
	    The fraction of samples to be used for fitting the individual base learners.

	presort : bool or ‘auto’
	    Whether to presort the data to speed up the finding of best splits in fitting.

	warm_start : bool
	    When set to True, reuse the solution of the previous call to fit and add more estimators to the ensemble, otherwise, just erase the previous solution.

	max_features : int, float, string or None
	    The number of features to consider when looking for the best split:

	max_depth : integer
	    maximum depth of the individual regression estimators. The maximum depth limits the number of nodes in the tree.
    
	min_weight_fraction_leaf : float
	    The minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node.

	max_leaf_nodes : int or None
	    Grow trees with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity.

    """
	
	loss_gb="deviance"
	if(args[1].find("None")==-1): 	
		loss_gb = args[1]

	lr=0.1  
	if(args[2].find("None")==-1):
		lr = float(args[2])

	ss=1.0
	if(args[3].find("None")==-1):
		ss = float(args[3])

	psort = False
	if(args[4].find("True")!=-1):
		psort = True
	elif(args[4].find("auto")!=-1):
		psort = "auto"

	est=100
	if(args[5].find("None")==-1):
		est = int(args[5])

	ws = bool(0)
	if(args[6].find("True")!=-1):
		ws = bool(1)

	if(args[7].find("sqrt")!=-1):
		mf = "sqrt"
	elif(args[7].find("log2")!=-1):
		mf = "log2"
	elif(args[7].find("None")!=-1):
		mf = None
	else:
		mf = float(args[7])

	if(args[8].find("None")!=-1):
		md = None
	else:
		md = int(args[8])

	mwfl = float(args[9])
	if(args[9].find("None")==-1):
		mwfl = float(args[9])

	if(args[10].find("None")!=-1):
		mln = None
	else:
		mln = int(args[10])
		

	return GradientBoostingClassifier(loss=loss_gb, learning_rate=lr, n_estimators=est, 
		subsample=ss, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=mwfl, 
		max_depth=md, init=None, random_state=42, max_features=mf, verbose=0, max_leaf_nodes=mln, 
		warm_start=ws, presort=psort)