#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#
from .estimator_base import H2OEstimator


class H2OGradientBoostingEstimator(H2OEstimator):
    """
    Gradient Boosting Method

    Builds gradient boosted trees on a parsed data set, for regression or classification.
    The default distribution function will guess the model type based on the response column type.
    Otherwise, the response column must be an enum for "bernoulli" or "multinomial", and numeric
    for all other distributions.

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

      score_each_iteration : bool
        Whether to score during each iteration of model training.
        Default: False

      score_tree_interval : int
        Score the model after every so many trees. Disabled if set to 0.
        Default: 0

      fold_assignment : "AUTO" | "Random" | "Modulo" | "Stratified"
        Cross-validation fold assignment scheme, if fold_column is not specified. The 'Stratified' option will stratify
        the folds based on the response variable, for classification problems.
        Default: "AUTO"

      fold_column : VecSpecifier
        Column with cross-validation fold index assignment per observation.

      response_column : VecSpecifier
        Response variable column.

      ignored_columns : list(str)
        Names of columns to ignore for training.

      ignore_const_cols : bool
        Ignore constant columns.
        Default: True

      offset_column : VecSpecifier
        Offset column. This will be added to the combination of columns before applying the link function.

      weights_column : VecSpecifier
        Column with observation weights. Giving some observation a weight of zero is equivalent to excluding it from the
        dataset; giving an observation a relative weight of 2 is equivalent to repeating that row twice. Negative
        weights are not allowed.

      balance_classes : bool
        Balance training data class counts via over/under-sampling (for imbalanced data).
        Default: False

      class_sampling_factors : list(float)
        Desired over/under-sampling ratios per class (in lexicographic order). If not specified, sampling factors will
        be automatically computed to obtain class balance during training. Requires balance_classes.

      max_after_balance_size : float
        Maximum relative size of the training data after balancing class counts (can be less than 1.0). Requires
        balance_classes.
        Default: 5.0

      max_confusion_matrix_size : int
        Maximum size (# classes) for confusion matrices to be printed in the Logs
        Default: 20

      max_hit_ratio_k : int
        Max. number (top K) of predictions to use for hit ratio computation (for multi-class only, 0 to disable)
        Default: 0

      ntrees : int
        Number of trees.
        Default: 50

      max_depth : int
        Maximum tree depth.
        Default: 5

      min_rows : float
        Fewest allowed (weighted) observations in a leaf (in R called 'nodesize').
        Default: 10.0

      nbins : int
        For numerical columns (real/int), build a histogram of (at least) this many bins, then split at the best point
        Default: 20

      nbins_top_level : int
        For numerical columns (real/int), build a histogram of (at most) this many bins at the root level, then decrease
        by factor of two per level
        Default: 1024

      nbins_cats : int
        For categorical columns (factors), build a histogram of this many bins, then split at the best point. Higher
        values can lead to more overfitting.
        Default: 1024

      r2_stopping : float
        Stop making trees when the R^2 metric equals or exceeds this
        Default: 1.79769313486e+308

      stopping_rounds : int
        Early stopping based on convergence of stopping_metric. Stop if simple moving average of length k of the
        stopping_metric does not improve for k:=stopping_rounds scoring events (0 to disable)
        Default: 0

      stopping_metric : "AUTO" | "deviance" | "logloss" | "MSE" | "AUC" | "lift_top_group" | "r2" | "misclassification"
                        | "mean_per_class_error"
        Metric to use for early stopping (AUTO: logloss for classification, deviance for regression)
        Default: "AUTO"

      stopping_tolerance : float
        Relative tolerance for metric-based stopping criterion (stop if relative improvement is not at least this much)
        Default: 0.001

      max_runtime_secs : float
        Maximum allowed runtime in seconds for model training. Use 0 to disable.
        Default: 0.0

      seed : int
        Seed for pseudo random number generator (if applicable)
        Default: -1

      build_tree_one_node : bool
        Run on one node only; no network overhead but fewer cpus used.  Suitable for small datasets.
        Default: False

      learn_rate : float
        Learning rate (from 0.0 to 1.0)
        Default: 0.1

      learn_rate_annealing : float
        Scale the learning rate by this factor after each tree (e.g., 0.99 or 0.999)
        Default: 1.0

      distribution : "AUTO" | "bernoulli" | "multinomial" | "gaussian" | "poisson" | "gamma" | "tweedie" | "laplace" |
                     "quantile" | "huber"
        Distribution function
        Default: "AUTO"

      quantile_alpha : float
        Desired quantile for Quantile regression, must be between 0 and 1.
        Default: 0.5

      tweedie_power : float
        Tweedie power for Tweedie regression, must be between 1 and 2.
        Default: 1.5

      huber_alpha : float
        Desired quantile for Huber/M-regression (threshold between quadratic and linear loss, must be between 0 and 1).
        Default: 0.9

      checkpoint : str
        Model checkpoint to resume training with.

      sample_rate : float
        Row sample rate per tree (from 0.0 to 1.0)
        Default: 1.0

      sample_rate_per_class : list(float)
        Row sample rate per tree per class (from 0.0 to 1.0)

      col_sample_rate : float
        Column sample rate (from 0.0 to 1.0)
        Default: 1.0

      col_sample_rate_change_per_level : float
        Relative change of the column sampling rate for every level (from 0.0 to 2.0)
        Default: 1.0

      col_sample_rate_per_tree : float
        Column sample rate per tree (from 0.0 to 1.0)
        Default: 1.0

      min_split_improvement : float
        Minimum relative improvement in squared error reduction for a split to happen
        Default: 1e-05

      histogram_type : "AUTO" | "UniformAdaptive" | "Random" | "QuantilesGlobal" | "RoundRobin"
        What type of histogram to use for finding optimal split points
        Default: "AUTO"

      max_abs_leafnode_pred : float
        Maximum absolute value of a leaf node prediction
        Default: 1.79769313486e+308

    """
    def __init__(self, **kwargs):
        super(H2OGradientBoostingEstimator, self).__init__()
        self._parms = {}
        for name in ["model_id", "training_frame", "validation_frame", "nfolds", "keep_cross_validation_predictions",
                     "keep_cross_validation_fold_assignment", "score_each_iteration", "score_tree_interval",
                     "fold_assignment", "fold_column", "response_column", "ignored_columns", "ignore_const_cols",
                     "offset_column", "weights_column", "balance_classes", "class_sampling_factors",
                     "max_after_balance_size", "max_confusion_matrix_size", "max_hit_ratio_k", "ntrees", "max_depth",
                     "min_rows", "nbins", "nbins_top_level", "nbins_cats", "r2_stopping", "stopping_rounds",
                     "stopping_metric", "stopping_tolerance", "max_runtime_secs", "seed", "build_tree_one_node",
                     "learn_rate", "learn_rate_annealing", "distribution", "quantile_alpha", "tweedie_power",
                     "huber_alpha", "checkpoint", "sample_rate", "sample_rate_per_class", "col_sample_rate",
                     "col_sample_rate_change_per_level", "col_sample_rate_per_tree", "min_split_improvement",
                     "histogram_type", "max_abs_leafnode_pred"]:
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
    def score_each_iteration(self):
        return self._parms["score_each_iteration"]

    @score_each_iteration.setter
    def score_each_iteration(self, value):
        self._parms["score_each_iteration"] = value

    @property
    def score_tree_interval(self):
        return self._parms["score_tree_interval"]

    @score_tree_interval.setter
    def score_tree_interval(self, value):
        self._parms["score_tree_interval"] = value

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
    def response_column(self):
        return self._parms["response_column"]

    @response_column.setter
    def response_column(self, value):
        self._parms["response_column"] = value

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
    def offset_column(self):
        return self._parms["offset_column"]

    @offset_column.setter
    def offset_column(self, value):
        self._parms["offset_column"] = value

    @property
    def weights_column(self):
        return self._parms["weights_column"]

    @weights_column.setter
    def weights_column(self, value):
        self._parms["weights_column"] = value

    @property
    def balance_classes(self):
        return self._parms["balance_classes"]

    @balance_classes.setter
    def balance_classes(self, value):
        self._parms["balance_classes"] = value

    @property
    def class_sampling_factors(self):
        return self._parms["class_sampling_factors"]

    @class_sampling_factors.setter
    def class_sampling_factors(self, value):
        self._parms["class_sampling_factors"] = value

    @property
    def max_after_balance_size(self):
        return self._parms["max_after_balance_size"]

    @max_after_balance_size.setter
    def max_after_balance_size(self, value):
        self._parms["max_after_balance_size"] = value

    @property
    def max_confusion_matrix_size(self):
        return self._parms["max_confusion_matrix_size"]

    @max_confusion_matrix_size.setter
    def max_confusion_matrix_size(self, value):
        self._parms["max_confusion_matrix_size"] = value

    @property
    def max_hit_ratio_k(self):
        return self._parms["max_hit_ratio_k"]

    @max_hit_ratio_k.setter
    def max_hit_ratio_k(self, value):
        self._parms["max_hit_ratio_k"] = value

    @property
    def ntrees(self):
        return self._parms["ntrees"]

    @ntrees.setter
    def ntrees(self, value):
        self._parms["ntrees"] = value

    @property
    def max_depth(self):
        return self._parms["max_depth"]

    @max_depth.setter
    def max_depth(self, value):
        self._parms["max_depth"] = value

    @property
    def min_rows(self):
        return self._parms["min_rows"]

    @min_rows.setter
    def min_rows(self, value):
        self._parms["min_rows"] = value

    @property
    def nbins(self):
        return self._parms["nbins"]

    @nbins.setter
    def nbins(self, value):
        self._parms["nbins"] = value

    @property
    def nbins_top_level(self):
        return self._parms["nbins_top_level"]

    @nbins_top_level.setter
    def nbins_top_level(self, value):
        self._parms["nbins_top_level"] = value

    @property
    def nbins_cats(self):
        return self._parms["nbins_cats"]

    @nbins_cats.setter
    def nbins_cats(self, value):
        self._parms["nbins_cats"] = value

    @property
    def r2_stopping(self):
        return self._parms["r2_stopping"]

    @r2_stopping.setter
    def r2_stopping(self, value):
        self._parms["r2_stopping"] = value

    @property
    def stopping_rounds(self):
        return self._parms["stopping_rounds"]

    @stopping_rounds.setter
    def stopping_rounds(self, value):
        self._parms["stopping_rounds"] = value

    @property
    def stopping_metric(self):
        return self._parms["stopping_metric"]

    @stopping_metric.setter
    def stopping_metric(self, value):
        self._parms["stopping_metric"] = value

    @property
    def stopping_tolerance(self):
        return self._parms["stopping_tolerance"]

    @stopping_tolerance.setter
    def stopping_tolerance(self, value):
        self._parms["stopping_tolerance"] = value

    @property
    def max_runtime_secs(self):
        return self._parms["max_runtime_secs"]

    @max_runtime_secs.setter
    def max_runtime_secs(self, value):
        self._parms["max_runtime_secs"] = value

    @property
    def seed(self):
        return self._parms["seed"]

    @seed.setter
    def seed(self, value):
        self._parms["seed"] = value

    @property
    def build_tree_one_node(self):
        return self._parms["build_tree_one_node"]

    @build_tree_one_node.setter
    def build_tree_one_node(self, value):
        self._parms["build_tree_one_node"] = value

    @property
    def learn_rate(self):
        return self._parms["learn_rate"]

    @learn_rate.setter
    def learn_rate(self, value):
        self._parms["learn_rate"] = value

    @property
    def learn_rate_annealing(self):
        return self._parms["learn_rate_annealing"]

    @learn_rate_annealing.setter
    def learn_rate_annealing(self, value):
        self._parms["learn_rate_annealing"] = value

    @property
    def distribution(self):
        return self._parms["distribution"]

    @distribution.setter
    def distribution(self, value):
        self._parms["distribution"] = value

    @property
    def quantile_alpha(self):
        return self._parms["quantile_alpha"]

    @quantile_alpha.setter
    def quantile_alpha(self, value):
        self._parms["quantile_alpha"] = value

    @property
    def tweedie_power(self):
        return self._parms["tweedie_power"]

    @tweedie_power.setter
    def tweedie_power(self, value):
        self._parms["tweedie_power"] = value

    @property
    def huber_alpha(self):
        return self._parms["huber_alpha"]

    @huber_alpha.setter
    def huber_alpha(self, value):
        self._parms["huber_alpha"] = value

    @property
    def checkpoint(self):
        return self._parms["checkpoint"]

    @checkpoint.setter
    def checkpoint(self, value):
        self._parms["checkpoint"] = value

    @property
    def sample_rate(self):
        return self._parms["sample_rate"]

    @sample_rate.setter
    def sample_rate(self, value):
        self._parms["sample_rate"] = value

    @property
    def sample_rate_per_class(self):
        return self._parms["sample_rate_per_class"]

    @sample_rate_per_class.setter
    def sample_rate_per_class(self, value):
        self._parms["sample_rate_per_class"] = value

    @property
    def col_sample_rate(self):
        return self._parms["col_sample_rate"]

    @col_sample_rate.setter
    def col_sample_rate(self, value):
        self._parms["col_sample_rate"] = value

    @property
    def col_sample_rate_change_per_level(self):
        return self._parms["col_sample_rate_change_per_level"]

    @col_sample_rate_change_per_level.setter
    def col_sample_rate_change_per_level(self, value):
        self._parms["col_sample_rate_change_per_level"] = value

    @property
    def col_sample_rate_per_tree(self):
        return self._parms["col_sample_rate_per_tree"]

    @col_sample_rate_per_tree.setter
    def col_sample_rate_per_tree(self, value):
        self._parms["col_sample_rate_per_tree"] = value

    @property
    def min_split_improvement(self):
        return self._parms["min_split_improvement"]

    @min_split_improvement.setter
    def min_split_improvement(self, value):
        self._parms["min_split_improvement"] = value

    @property
    def histogram_type(self):
        return self._parms["histogram_type"]

    @histogram_type.setter
    def histogram_type(self, value):
        self._parms["histogram_type"] = value

    @property
    def max_abs_leafnode_pred(self):
        return self._parms["max_abs_leafnode_pred"]

    @max_abs_leafnode_pred.setter
    def max_abs_leafnode_pred(self, value):
        self._parms["max_abs_leafnode_pred"] = value

    # overrides superclass
    def _compute_algo(self):
        return "gbm"
