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
from sklearn.decomposition import FastICA

#Ignoring the warnings:
import warnings
warnings.filterwarnings("ignore")

def fast_ica(args):

  """Uses scikit-learn's FastICA, a fast algorithm for Independent Component Analysis..
    
  Parameters
  ----------

  algorithm : {‘parallel’, ‘deflation’}
    Apply parallel or deflational algorithm for FastICA.

  fun : string or function, optional. Default: ‘logcosh’
    The functional form of the G function used in the approximation to neg-entropy. Could be either ‘logcosh’, ‘exp’, or ‘cube’.

  max_iter : int
    Maximum number of iterations during fit.

  tol : float
    Tolerance on update at each iteration.

  whiten : boolean
    If whiten is false, the data is already considered to be whitened, and no whitening is performed.

  n_components : int
    Number of components to use. If none is passed, all are used.

  """

  alg = args[1]
  funct = args[2]
  mi = int(args[3])
  t = float(args[4])

  whit = False
  if(args[5].find("True")!=-1):
    whit = True

  comp = None
  if(args[6].find("None")==-1):
  	comp = int(args[6])

  fica = FastICA(n_components=comp, algorithm=alg, whiten=whit, fun=funct, fun_args=None, max_iter=mi, tol=t, w_init=None, random_state=42)

  return fica