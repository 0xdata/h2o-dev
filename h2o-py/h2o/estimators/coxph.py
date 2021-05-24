#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#
from __future__ import absolute_import, division, print_function, unicode_literals

from h2o.estimators.estimator_base import H2OEstimator
from h2o.exceptions import H2OValueError
from h2o.frame import H2OFrame
from h2o.utils.typechecks import assert_is_type, Enum, numeric


class H2OCoxProportionalHazardsEstimator(H2OEstimator):
    """
    Cox Proportional Hazards

    Trains a Cox Proportional Hazards Model (CoxPH) on an H2O dataset.
    """

    algo = "coxph"

    def __init__(self, model_id=None, training_frame=None, start_column=None, stop_column=None, response_column=None,
                 ignored_columns=None, weights_column=None, offset_column=None, stratify_by=None, ties="efron", init=0,
                 lre_min=9, max_iterations=20, interactions=None, interaction_pairs=None, interactions_only=None,
                 use_all_factor_levels=False, export_checkpoints_dir=None, single_node_mode=False):
        """
        :param str model_id: Destination id for this model; auto-generated if not specified. (default:None).
        :param H2OFrame training_frame: Id of the training data frame. (default:None).
        :param str start_column: Start Time Column. (default:None).
        :param str stop_column: Stop Time Column. (default:None).
        :param str response_column: Response variable column. (default:None).
        :param List[str] ignored_columns: Names of columns to ignore for training. (default:None).
        :param str weights_column: Column with observation weights. Giving some observation a weight of zero is
               equivalent to excluding it from the dataset; giving an observation a relative weight of 2 is equivalent
               to repeating that row twice. Negative weights are not allowed. Note: Weights are per-row observation
               weights and do not increase the size of the data frame. This is typically the number of times a row is
               repeated, but non-integer values are supported as well. During training, rows with higher weights matter
               more, due to the larger loss function pre-factor. (default:None).
        :param str offset_column: Offset column. This will be added to the combination of columns before applying the
               link function. (default:None).
        :param List[str] stratify_by: List of columns to use for stratification. (default:None).
        :param Enum["efron", "breslow"] ties: Method for Handling Ties. (default:"efron").
        :param float init: Coefficient starting value. (default:0).
        :param float lre_min: Minimum log-relative error. (default:9).
        :param int max_iterations: Maximum number of iterations. (default:20).
        :param List[str] interactions: A list of predictor column indices to interact. All pairwise combinations will be
               computed for the list. (default:None).
        :param List[tuple] interaction_pairs: A list of pairwise (first order) column interactions. (default:None).
        :param List[str] interactions_only: A list of columns that should only be used to create interactions but should
               not itself participate in model training. (default:None).
        :param bool use_all_factor_levels: (Internal. For development only!) Indicates whether to use all factor levels.
               (default:False).
        :param str export_checkpoints_dir: Automatically export generated models to this directory. (default:None).
        :param bool single_node_mode: Run on a single node to reduce the effect of network overhead (for smaller
               datasets) (default:False).
        """
        sig_params = {k:v for k, v in locals().items() if k != 'self' and not k.startswith('__')}
        super(H2OCoxProportionalHazardsEstimator, self).__init__()
        self._parms = {}
        for pname, pvalue in sig_params.items():
            if pname == 'model_id':
                self._id = self._parms['model_id'] = pvalue
            else:
                # Using setattr(...) will invoke type-checking of the arguments
                setattr(self, pname, pvalue)

    @property
    def training_frame(self):
        """
        Id of the training data frame.

        Type: ``H2OFrame``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> train, valid = heart.split_frame(ratios=[.8])
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=train,
        ...                   validation_frame=valid)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("training_frame")

    @training_frame.setter
    def training_frame(self, training_frame):
        self._parms["training_frame"] = H2OFrame._validate(training_frame, 'training_frame')


    @property
    def start_column(self):
        """
        Start Time Column.

        Type: ``str``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> train, valid = heart.split_frame(ratios=[.8])
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=train,
        ...                   validation_frame=valid)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("start_column")

    @start_column.setter
    def start_column(self, start_column):
        assert_is_type(start_column, None, str)
        self._parms["start_column"] = start_column


    @property
    def stop_column(self):
        """
        Stop Time Column.

        Type: ``str``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> train, valid = heart.split_frame(ratios=[.8])
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=train,
        ...                   validation_frame=valid)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("stop_column")

    @stop_column.setter
    def stop_column(self, stop_column):
        assert_is_type(stop_column, None, str)
        self._parms["stop_column"] = stop_column


    @property
    def response_column(self):
        """
        Response variable column.

        Type: ``str``.
        """
        return self._parms.get("response_column")

    @response_column.setter
    def response_column(self, response_column):
        assert_is_type(response_column, None, str)
        self._parms["response_column"] = response_column


    @property
    def ignored_columns(self):
        """
        Names of columns to ignore for training.

        Type: ``List[str]``.
        """
        return self._parms.get("ignored_columns")

    @ignored_columns.setter
    def ignored_columns(self, ignored_columns):
        assert_is_type(ignored_columns, None, [str])
        self._parms["ignored_columns"] = ignored_columns


    @property
    def weights_column(self):
        """
        Column with observation weights. Giving some observation a weight of zero is equivalent to excluding it from the
        dataset; giving an observation a relative weight of 2 is equivalent to repeating that row twice. Negative
        weights are not allowed. Note: Weights are per-row observation weights and do not increase the size of the data
        frame. This is typically the number of times a row is repeated, but non-integer values are supported as well.
        During training, rows with higher weights matter more, due to the larger loss function pre-factor.

        Type: ``str``.
        """
        return self._parms.get("weights_column")

    @weights_column.setter
    def weights_column(self, weights_column):
        assert_is_type(weights_column, None, str)
        self._parms["weights_column"] = weights_column


    @property
    def offset_column(self):
        """
        Offset column. This will be added to the combination of columns before applying the link function.

        Type: ``str``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  offset_column="transplant")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("offset_column")

    @offset_column.setter
    def offset_column(self, offset_column):
        assert_is_type(offset_column, None, str)
        self._parms["offset_column"] = offset_column


    @property
    def stratify_by(self):
        """
        List of columns to use for stratification.

        Type: ``List[str]``.
        """
        return self._parms.get("stratify_by")

    @stratify_by.setter
    def stratify_by(self, stratify_by):
        assert_is_type(stratify_by, None, [str])
        self._parms["stratify_by"] = stratify_by


    @property
    def ties(self):
        """
        Method for Handling Ties.

        One of: ``"efron"``, ``"breslow"``  (default: ``"efron"``).

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> train, valid = heart.split_frame(ratios=[.8])
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  ties="breslow")
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=train,
        ...                   validation_frame=valid)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("ties")

    @ties.setter
    def ties(self, ties):
        assert_is_type(ties, None, Enum("efron", "breslow"))
        self._parms["ties"] = ties


    @property
    def init(self):
        """
        Coefficient starting value.

        Type: ``float``  (default: ``0``).

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  init=2.9)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("init")

    @init.setter
    def init(self, init):
        assert_is_type(init, None, numeric)
        self._parms["init"] = init


    @property
    def lre_min(self):
        """
        Minimum log-relative error.

        Type: ``float``  (default: ``9``).

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  lre_min=5)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("lre_min")

    @lre_min.setter
    def lre_min(self, lre_min):
        assert_is_type(lre_min, None, numeric)
        self._parms["lre_min"] = lre_min


    @property
    def max_iterations(self):
        """
        Maximum number of iterations.

        Type: ``int``  (default: ``20``).

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  max_iterations=50)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("max_iterations")

    @max_iterations.setter
    def max_iterations(self, max_iterations):
        assert_is_type(max_iterations, None, int)
        self._parms["max_iterations"] = max_iterations


    @property
    def interactions(self):
        """
        A list of predictor column indices to interact. All pairwise combinations will be computed for the list.

        Type: ``List[str]``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> interactions = ['start','stop']
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  interactions=interactions)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("interactions")

    @interactions.setter
    def interactions(self, interactions):
        assert_is_type(interactions, None, [str])
        self._parms["interactions"] = interactions


    @property
    def interaction_pairs(self):
        """
        A list of pairwise (first order) column interactions.

        Type: ``List[tuple]``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> interaction_pairs = [("start","stop")]
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  interaction_pairs=interaction_pairs)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("interaction_pairs")

    @interaction_pairs.setter
    def interaction_pairs(self, interaction_pairs):
        assert_is_type(interaction_pairs, None, [tuple])
        self._parms["interaction_pairs"] = interaction_pairs


    @property
    def interactions_only(self):
        """
        A list of columns that should only be used to create interactions but should not itself participate in model
        training.

        Type: ``List[str]``.

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> interactions = ['start','stop']
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  interactions_only=interactions)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("interactions_only")

    @interactions_only.setter
    def interactions_only(self, interactions_only):
        assert_is_type(interactions_only, None, [str])
        self._parms["interactions_only"] = interactions_only


    @property
    def use_all_factor_levels(self):
        """
        (Internal. For development only!) Indicates whether to use all factor levels.

        Type: ``bool``  (default: ``False``).

        :examples:

        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> heart_coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                                  stop_column="stop",
        ...                                                  use_all_factor_levels=True)
        >>> heart_coxph.train(x=predictor,
        ...                   y=response,
        ...                   training_frame=heart)
        >>> heart_coxph.scoring_history()
        """
        return self._parms.get("use_all_factor_levels")

    @use_all_factor_levels.setter
    def use_all_factor_levels(self, use_all_factor_levels):
        assert_is_type(use_all_factor_levels, None, bool)
        self._parms["use_all_factor_levels"] = use_all_factor_levels


    @property
    def export_checkpoints_dir(self):
        """
        Automatically export generated models to this directory.

        Type: ``str``.

        :examples:

        >>> import tempfile
        >>> from os import listdir
        >>> heart = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/coxph_test/heart.csv")
        >>> predictor = "age"
        >>> response = "event"
        >>> checkpoints_dir = tempfile.mkdtemp()
        >>> coxph = H2OCoxProportionalHazardsEstimator(start_column="start",
        ...                                            stop_column="stop",
        ...                                            export_checkpoints_dir=checkpoints_dir)
        >>> coxph.train(x=predictor,
        ...             y=response,
        ...             training_frame=heart)
        >>> len(listdir(checkpoints_dir))
        """
        return self._parms.get("export_checkpoints_dir")

    @export_checkpoints_dir.setter
    def export_checkpoints_dir(self, export_checkpoints_dir):
        assert_is_type(export_checkpoints_dir, None, str)
        self._parms["export_checkpoints_dir"] = export_checkpoints_dir


    @property
    def single_node_mode(self):
        """
        Run on a single node to reduce the effect of network overhead (for smaller datasets)

        Type: ``bool``  (default: ``False``).
        """
        return self._parms.get("single_node_mode")

    @single_node_mode.setter
    def single_node_mode(self, single_node_mode):
        assert_is_type(single_node_mode, None, bool)
        self._parms["single_node_mode"] = single_node_mode


    @property
    def baseline_hazard_frame(self):
        if (self._model_json is not None
                and self._model_json.get("output", {}).get("baseline_hazard", {}).get("name") is not None):
            baseline_hazard_name = self._model_json["output"]["baseline_hazard"]["name"]
            return H2OFrame.get_frame(baseline_hazard_name)

    @property
    def baseline_survival_frame(self):
        if (self._model_json is not None
                and self._model_json.get("output", {}).get("baseline_survival", {}).get("name") is not None):
            baseline_survival_name = self._model_json["output"]["baseline_survival"]["name"]
            return H2OFrame.get_frame(baseline_survival_name)
