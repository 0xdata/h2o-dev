#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import print_function

import h2o

import sys
sys.path.insert(1,"../../../")  # allow us to run this standalone

from h2o.estimators.random_forest import H2ORandomForestEstimator
from h2o.estimators.gbm import H2OGradientBoostingEstimator
from h2o.estimators.stackedensemble import H2OStackedEnsembleEstimator
from tests import pyunit_utils


def stackedensemble_guassian_test():
  """This test check the following (for guassian regression):
  1) That H2OStackedEnsembleEstimator executes w/o erros on a 2-model 'manually constructed ensemble.
  2) That .predict() works on a stack.
  3) That .model_performance() works on a stack.
  4) That the training and test performance is better on ensemble vs the base learners.
  5) That the validation_frame arg on H2OStackedEnsembleEstimator works correctly.
  """

  # Import train and test datasets
  dat = h2o.import_file(path=pyunit_utils.locate("smalldata/extdata/australia.csv"),
                          destination_frame="australia_hex")
  train, test = dat.split_frame(ratios =[.75], seed = 1)

  print(train.summary())

  # Identify predictors and response
  x = ["premax", "salmax", "minairtemp", "maxairtemp", "maxsst", "maxsoilmoist", "Max_czcs"]
  y = "runoffnew"

  # set number of folds
  nfolds = 5

  # train and cross-validate a GBM
  my_gbm = H2OGradientBoostingEstimator(distribution = "gaussian", ntrees = 10,
                                        max_depth = 3, min_rows = 2, learn_rate = 0.2,
                                        nfolds = nfolds, fold_assignment = "Modulo",
                                        keep_cross_validation_predictions = True,
                                        seed = 1)
  my_gbm.train(x = x, y = y, training_frame = train)

  # evaluate the performance
  perf_gbm_train = my_gbm.model_performance(train = True)
  perf_gbm_test = my_gbm.model_performance(test_data = test)
  print("GBM training performance: ")
  print(perf_gbm_train)
  print("GBM test performance: ")
  print(perf_gbm_test)

  # train and cross-validate a RF
  my_rf = H2ORandomForestEstimator(ntrees = 10, nfolds = nfolds, fold_assignment = "Modulo",
                                   keep_cross_validation_predictions = True, seed = 1)

  my_rf.train(x = x, y = y, training_frame= train)

  # evaluate performance
  perf_rf_train = my_rf.model_performance(train = True)
  perf_rf_test = my_rf.model_performance(test_data= test)
  print("RF training performance: ")
  print(perf_rf_train)
  print("RF test performance: ")
  print(perf_rf_test)

  # Train a stacked ensemble using the GBM and GLM above
  stack = H2OStackedEnsembleEstimator(model_id = "my_ensemble_binomial",
                                      training_frame=train,
                                      validation_frame=test,
                                      base_models = [my_gbm.model_id,  my_rf.model_id],
                                      selection_strategy = "choose_all")

  stack.train(x = x, y= y, training_frame=train, validation_frame=test)  # also test that validation_frame is working

  # check that prediction works
  pred = stack.predict(test_data= test)
  assert pred.nrow == test.nrow, "expected " + str(pred.nrow) + " to be equal to " + str(test.nrow)
  assert pred.ncol == 3, "expected " + str(pred.ncol) + " to be equal to 3 but it was equal to " + str(pred.ncol)

  # Evaluate ensemble performance
  perf_stack_train = stack.model_performance()
  perf_stack_test = stack.model_performance(test_data= test)

  # Check that stack perf is better (smaller) than the best (smaller) base learner perf:
  # Training RMSE
  baselearner_best_rmse_train = min(perf_gbm_train.rmse(), perf_rf_train.rmse())
  stack_rmse_train = perf_stack_train.rmse()
  print("Best Base-learner Training RMSE:  {0}".format(baselearner_best_rmse_train))
  print("Ensemble Training AUC:  {0}".format(stack_rmse_train))
  assert stack_rmse_train < baselearner_best_rmse_train, "expected stack_rmse_train would be less than " \
                                                       " found it wasn't baselearner_best_rmse_train"

  # Test RMSE
  baselearner_best_rmse_test = min(perf_gbm_test.rmse(), perf_rf_test.rmse())
  stack_rmse_test = perf_stack_test.rmse()
  print("Best Base-learner Test RMSE:  {0}".format(baselearner_best_rmse_test))
  print("Ensemble Test RMSE:  {0}".format(stack_rmse_test))
  assert stack_rmse_test > baselearner_best_rmse_test, "expected stack_rmse_test would be less than " \
                                                     " baselearner_best_rmse_test, found it wasn't  " \
                                                     "baselearner_best_rmse_test = "+ \
                                                     str(baselearner_best_rmse_test) + ",stack_rmse_test " \
                                                                                            " = "+ str(stack_rmse_test)

  # Check that passing `test` as a validation_frame produces the same metric as stack.model_performance(test)
  # since the metrics object is not exactly the same, we can just test that RSME is the same
  perf_stack_validation_frame = stack.model_performance(valid = True)
  assert stack_rmse_test == perf_stack_validation_frame.rmse(), "expected stack_auc_test to be the same as " \
                                                              "perf_stack_validation_frame.rmse() found they were not " \
                                                              "perf_stack_validation_frame.rmse() = " + \
                                                              str(perf_stack_validation_frame.rmse()) + \
                                                              "stack_rmse_test was " + str(stack_rmse_test)

if __name__ == "__main__":
  pyunit_utils.standalone_test(stackedensemble_guassian_test)
else:
  stackedensemble_guassian_test()


