#!/usr/bin/env python2
import numpy as np
import pylab as pl
import svmlight_loader as io
import sys

from sklearn import datasets, svm
from sklearn.feature_selection import SelectPercentile, chi2

###############################################################################
# import some data to play with

X, y = io.load_svmlight_file('mergedCPK-TP/output_bound10_ps4_f427_cyclic.AvsI')
# X, y = io.load_svmlight_file(sys.argv[1])


# ###############################################################################
pl.figure(1)
pl.clf()

X_indices = np.arange(X.shape[-1])

###############################################################################
# Univariate feature selection with F-test for feature scoring
# We use the default selection function: the 10% most significant features
selector = SelectPercentile(chi2, percentile=10)
selector.fit(X, y)
scores = -np.log10(selector.pvalues_)
scores /= scores.max()
pl.bar(X_indices - .45, scores, width=.2,
       label=r'Univariate score ($-Log(p_{value})$)', 
       color='g')

pl.show()

# ###############################################################################
# # Compare to the weights of an SVM
# clf = svm.SVC(kernel='linear')
# clf.fit(X, y)

# svm_weights = (clf.coef_ ** 2).sum(axis=0)
# svm_weights /= svm_weights.max()

# pl.bar(X_indices - .25, svm_weights, width=.2, label='SVM weight', color='r')

# clf_selected = svm.SVC(kernel='linear')
# clf_selected.fit(selector.transform(X), y)

# svm_weights_selected = (clf_selected.coef_ ** 2).sum(axis=0)
# svm_weights_selected /= svm_weights_selected.max()

# pl.bar(X_indices[selector.get_support()] - .05, svm_weights_selected, width=.2,
#        label='SVM weights after selection', color='b')


# pl.title("Comparing feature selection")
# pl.xlabel('Feature number')
# pl.yticks(())
# pl.axis('tight')
# pl.legend(loc='upper right')
# pl.show()

