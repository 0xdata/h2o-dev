#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#
from .estimator_base import H2OEstimator


class H2OKMeansEstimator(H2OEstimator):
    """
    K-means

    Performs k-means clustering on an H2O dataset.

    Parameters
    ----------
      model_id : str
        Destination id for this model; auto-generated if not specified.

      training_frame : str
        Id of the training data frame (Not required, to allow initial validation of model parameters).

      validation_frame : str
        Id of the validation data frame.

      nfolds : int
        Number of folds for N-fold cross-validation (0 to disable or >= 2).
        Default: 0

      keep_cross_validation_predictions : bool
        Whether to keep the predictions of the cross-validation models.
        Default: False

      keep_cross_validation_fold_assignment : bool
        Whether to keep the cross-validation fold assignment.
        Default: False

      fold_assignment : "AUTO" | "Random" | "Modulo" | "Stratified"
        Cross-validation fold assignment scheme, if fold_column is not specified. The 'Stratified' option will stratify
        the folds based on the response variable, for classification problems.
        Default: "AUTO"

      fold_column : VecSpecifier
        Column with cross-validation fold index assignment per observation.

      ignored_columns : list(str)
        Names of columns to ignore for training.

      ignore_const_cols : bool
        Ignore constant columns.
        Default: True

      score_each_iteration : bool
        Whether to score during each iteration of model training.
        Default: False

      k : int, required
        Number of clusters
        Default: 1

      user_points : str
        User-specified points

      max_iterations : int
        Maximum training iterations
        Default: 1000

      standardize : bool
        Standardize columns
        Default: True

      seed : int
        RNG Seed
        Default: -1

      init : "Random" | "PlusPlus" | "Furthest" | "User"
        Initialization mode
        Default: "Furthest"

      max_runtime_secs : float
        Maximum allowed runtime in seconds for model training. Use 0 to disable.
        Default: 0.0

    """
    def __init__(self, **kwargs):
        super(H2OKMeansEstimator, self).__init__()
        self._parms = {}
        for name in ["model_id", "training_frame", "validation_frame", "nfolds", "keep_cross_validation_predictions",
                     "keep_cross_validation_fold_assignment", "fold_assignment", "fold_column", "ignored_columns",
                     "ignore_const_cols", "score_each_iteration", "k", "user_points", "max_iterations", "standardize",
                     "seed", "init", "max_runtime_secs"]:
            pname = name[:-1] if name[-1] == '_' else name
            self._parms[pname] = kwargs[name] if name in kwargs else None

    @property
    def training_frame(self):
        return self._parms["training_frame"]

    @training_frame.setter
    def training_frame(self, value):
        self._parms["training_frame"] = value

    @property
    def validation_frame(self):
        return self._parms["validation_frame"]

    @validation_frame.setter
    def validation_frame(self, value):
        self._parms["validation_frame"] = value

    @property
    def nfolds(self):
        return self._parms["nfolds"]

    @nfolds.setter
    def nfolds(self, value):
        self._parms["nfolds"] = value

    @property
    def keep_cross_validation_predictions(self):
        return self._parms["keep_cross_validation_predictions"]

    @keep_cross_validation_predictions.setter
    def keep_cross_validation_predictions(self, value):
        self._parms["keep_cross_validation_predictions"] = value

    @property
    def keep_cross_validation_fold_assignment(self):
        return self._parms["keep_cross_validation_fold_assignment"]

    @keep_cross_validation_fold_assignment.setter
    def keep_cross_validation_fold_assignment(self, value):
        self._parms["keep_cross_validation_fold_assignment"] = value

    @property
    def fold_assignment(self):
        return self._parms["fold_assignment"]

    @fold_assignment.setter
    def fold_assignment(self, value):
        self._parms["fold_assignment"] = value

    @property
    def fold_column(self):
        return self._parms["fold_column"]

    @fold_column.setter
    def fold_column(self, value):
        self._parms["fold_column"] = value

    @property
    def ignored_columns(self):
        return self._parms["ignored_columns"]

    @ignored_columns.setter
    def ignored_columns(self, value):
        self._parms["ignored_columns"] = value

    @property
    def ignore_const_cols(self):
        return self._parms["ignore_const_cols"]

    @ignore_const_cols.setter
    def ignore_const_cols(self, value):
        self._parms["ignore_const_cols"] = value

    @property
    def score_each_iteration(self):
        return self._parms["score_each_iteration"]

    @score_each_iteration.setter
    def score_each_iteration(self, value):
        self._parms["score_each_iteration"] = value

    @property
    def k(self):
        return self._parms["k"]

    @k.setter
    def k(self, value):
        self._parms["k"] = value

    @property
    def user_points(self):
        return self._parms["user_points"]

    @user_points.setter
    def user_points(self, value):
        self._parms["user_points"] = value

    @property
    def max_iterations(self):
        return self._parms["max_iterations"]

    @max_iterations.setter
    def max_iterations(self, value):
        self._parms["max_iterations"] = value

    @property
    def standardize(self):
        return self._parms["standardize"]

    @standardize.setter
    def standardize(self, value):
        self._parms["standardize"] = value

    @property
    def seed(self):
        return self._parms["seed"]

    @seed.setter
    def seed(self, value):
        self._parms["seed"] = value

    @property
    def init(self):
        return self._parms["init"]

    @init.setter
    def init(self, value):
        self._parms["init"] = value

    @property
    def max_runtime_secs(self):
        return self._parms["max_runtime_secs"]

    @max_runtime_secs.setter
    def max_runtime_secs(self, value):
        self._parms["max_runtime_secs"] = value

    # overrides superclass
    def _compute_algo(self):
        return "kmeans"

