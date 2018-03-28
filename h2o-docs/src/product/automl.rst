AutoML: Automatic Machine Learning
==================================

In recent years, the demand for machine learning experts has outpaced the supply, despite the surge of people entering the field.  To address this gap, there have been big strides in the development of user-friendly machine learning software that can be used by non-experts.  The first steps toward simplifying machine learning involved developing simple, unified interfaces to a variety of machine learning algorithms (e.g. H2O).

Although H2O has made it easy for non-experts to experiment with machine learning, there is still a fair bit of knowledge and background in data science that is required to produce high-performing machine learning models.  Deep Neural Networks in particular are notoriously difficult for a non-expert to tune properly.  In order for machine learning software to truly be accessible to non-experts, we have designed an easy-to-use interface which automates the process of training a large selection of candidate models.  H2O's AutoML can also be a helpful tool for the advanced user, by providing a simple wrapper function that performs a large number of modeling-related tasks that would typically require many lines of code, and by freeing up their time to focus on other aspects of the data science pipeline tasks such as data-preprocessing, feature engineering and model deployment.

H2O's AutoML can be used for automating the machine learning workflow, which includes automatic training and tuning of many models within a user-specified time-limit.  `Stacked Ensembles <http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/stacked-ensembles.html>`__ will be automatically trained on collections of individual models to produce highly predictive ensemble models which, in most cases, will be the top performing models in the AutoML Leaderboard.  


AutoML Interface
----------------

The H2O AutoML interface is designed to have as few parameters as possible so that all the user needs to do is point to their dataset, identify the response column and optionally specify a time constraint or limit on the number of total models trained. 

In both the R and Python API, AutoML uses the same data-related arguments, ``x``, ``y``, ``training_frame``, ``validation_frame``, as the other H2O algorithms.  Most of the time, all you'll need to do is specify the data arguments. You can then configure values for ``max_runtime_secs`` and/or ``max_models`` to set explicit time or number-of-model limits on your run.  

Required Parameters
~~~~~~~~~~~~~~~~~~~

Required Data Parameters
''''''''''''''''''''''''

- `y <data-science/algo-params/y.html>`__: This argument is the name (or index) of the response column. 

- `training_frame <data-science/algo-params/training_frame.html>`__: Specifies the training set. 

Required Stopping Parameters
''''''''''''''''''''''''''''

One of the following stopping strategies (time or number-of-model based) must be specified.  When both options are set, then the AutoML run will stop as soon as it hits one of either of these limits. 

- `max_runtime_secs <data-science/algo-params/max_runtime_secs.html>`__: This argument controls how long the AutoML run will execute for. This defaults to 3600 seconds (1 hour).

- **max_models**: Specify the maximum number of models to build in an AutoML run, excluding the Stacked Ensemble models.  Defaults to ``NULL/None``. 


Optional Parameters
~~~~~~~~~~~~~~~~~~~

Optional Data Parameters
''''''''''''''''''''''''

- `x <data-science/algo-params/x.html>`__: A list/vector of predictor column names or indexes.  This argument only needs to be specified if the user wants to exclude columns from the set of predictors.  If all columns (other than the response) should be used in prediction, then this does not need to be set.

- `validation_frame <data-science/algo-params/validation_frame.html>`__: This argument is used to specify the validation frame used for early stopping of individual models and early stopping of the grid searches (unless ``max_models`` or ``max_runtime_secs`` overrides metric-based early stopping).  

- **leaderboard_frame**: This argument allows the user to specify a particular data frame use to score & rank models on the leaderboard. This frame will not be used for anything besides leaderboard scoring. If a leaderboard frame is not specified by the user, then the leaderboard will use cross-validation metrics instead (or if cross-validation is turned off by setting ``nfolds = 0``, then a leaderboard frame will be generated automatically from the validation frame (if provided) or the training frame).

- `fold_column <data-science/algo-params/fold_column.html>`__: Specifies a column with cross-validation fold index assignment per observation. This is used to override the default, randomized, 5-fold cross-validation scheme for individual models in the AutoML run.

- `weights_column <data-science/algo-params/weights_column.html>`__: Specifies a column with observation weights. Giving some observation a weight of zero is equivalent to excluding it from the dataset; giving an observation a relative weight of 2 is equivalent to repeating that row twice. Negative weights are not allowed.

-  `ignored_columns <data-science/algo-params/ignored_columns.html>`__: (Optional, Python only) Specify the column or columns (as a list/vector) to be excluded from the model.  This is the converse of the ``x`` argument.

Optional Miscellaneous Parameters
'''''''''''''''''''''''''''''''''

- `nfolds <data-science/algo-params/nfolds.html>`__:  Number of folds for k-fold cross-validation of the models in the AutoML run. Defaults to 5. Use 0 to disable cross-validation; this will also disable Stacked Ensembles (thus decreasing the overall best model performance).

-  `stopping_metric <data-science/algo-params/stopping_metric.html>`__: Specifies the metric to use for early stopping of the grid searches and individual models. Defaults to ``"AUTO"``.  The available options are:

    - ``AUTO``: This defaults to ``logloss`` for classification, ``deviance`` for regression
    - ``deviance``
    - ``logloss``
    - ``mse``
    - ``rmse``
    - ``mae``
    - ``rmsle``
    - ``auc``
    - ``lift_top_group``
    - ``misclassification``
    - ``mean_per_class_error``

-  `stopping_tolerance <data-science/algo-params/stopping_tolerance.html>`__: This option specifies the relative tolerance for the metric-based stopping criterion to stop a grid search and the training of individual models within the AutoML run. This value defaults to 0.001 if the dataset is at least 1 million rows; otherwise it defaults to a bigger value determined by the size of the dataset and the non-NA-rate.  In that case, the value is computed as 1/sqrt(nrows * non-NA-rate).

- `stopping_rounds <data-science/algo-params/stopping_rounds.html>`__: This argument is used to stop model training when the stopping metric (e.g. AUC) doesn’t improve for this specified number of training rounds, based on a simple moving average.   In the context of AutoML, this controls early stopping both within the random grid searches as well as the individual models.  Defaults to 3 and must be an non-negative integer.  To disable early stopping altogether, set this to 0. 

- `seed <data-science/algo-params/seed.html>`__: Integer. Set a seed for reproducibility. AutoML can only guarantee reproducibility if ``max_models`` is used because ``max_runtime_secs`` is resource limited, meaning that if the available compute resources are not the same between runs, AutoML may be able to train more models on one run vs another.  Defaults to ``NULL/None``.

- **project_name**: Character string to identify an AutoML project. Defaults to ``NULL/None``, which means a project name will be auto-generated based on the training frame ID.  More models can be trained and added to an existing AutoML project by specifying the same project name in muliple calls to the AutoML function (as long as the same training frame is used in subsequent runs).

- **exclude_algos**: List/vector of character strings naming the algorithms to skip during the model-building phase.  An example use is ``exclude_algos = ["GLM", "DeepLearning", "DRF"]`` in Python or ``exclude_algos = c("GLM", "DeepLearning", "DRF")`` in R.  Defaults to ``None/NULL``, which means that all appropriate H2O algorithms will be used, if the search stopping criteria allow.  The algorithm names are:

    - ``GLM``
    - ``DeepLearning``
    - ``GBM``
    - ``DRF`` (This includes both the Random Forest and Extremely Randomized Trees (XRT) models. Refer to the :ref:`xrt` section in the DRF chapter and the `histogram_type <http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/algo-params/histogram_type.html>`__ parameter description for more information.)
    - ``StackedEnsemble``


Auto-Generated Frames
~~~~~~~~~~~~~~~~~~~~~

If the user doesn't specify a ``validation_frame``, then one will be created automatically by randomly partitioning the training data.  The validation frame is required for early stopping of the individual algorithms, the grid searches and the AutoML process itself.  

By default, AutoML uses cross-validation for all models, and therefore we can use cross-validation metrics to generate the leaderboard.  If the ``leaderboard_frame`` is explicitly specified by the user, then that frame will be used to generate the leaderboard metrics instead of using cross-validation metrics. 

For cross-validated AutoML, when the user specifies:

   1. **training**: The ``training_frame`` is split into training (80%) and validation (20%).  
   2. **training + leaderboard**:  The ``training_frame`` is split into training (80%) and validation (20%).  
   3. **training + validation**: Leave frames as-is.
   4. **training + validation + leaderboard**: Leave frames as-is.


If not using cross-validation (by setting ``nfolds = 0``) in AutoML, then we need to make sure there is a test frame (aka. the "leaderboard frame") to score on because cross-validation metrics will not be available.  So when the user specifies:

   1. **training**: The ``training_frame`` is split into training (80%), validation (10%) and leaderboard/test (10%).
   2. **training + leaderboard**:  The ``training_frame`` is split into training (80%) and validation (20%).  Leaderboard frame as-is.
   3. **training + validation**: The ``validation_frame`` is split into validation (50%) and leaderboard/test (50%).  Training frame as-is.
   4. **training + validation + leaderboard**: Leave frames as-is.


Code Examples
~~~~~~~~~~~~~

Here’s an example showing basic usage of the ``h2o.automl()`` function in *R* and the ``H2OAutoML`` class in *Python*.  For demonstration purposes only, we explicitly specify the the `x` argument, even though on this dataset, that's not required.  With this dataset, the set of predictors is all columns other than the response.  Like other H2O algorithms, the default value of ``x`` is "all columns, excluding ``y``", so that will produce the same result.

.. example-code::
   .. code-block:: r

    library(h2o)

    h2o.init()

    # Import a sample binary outcome train/test set into H2O
    train <- h2o.importFile("https://s3.amazonaws.com/erin-data/higgs/higgs_train_10k.csv")
    test <- h2o.importFile("https://s3.amazonaws.com/erin-data/higgs/higgs_test_5k.csv")

    # Identify predictors and response
    y <- "response"
    x <- setdiff(names(train), y)

    # For binary classification, response should be a factor
    train[,y] <- as.factor(train[,y])
    test[,y] <- as.factor(test[,y])

    aml <- h2o.automl(x = x, y = y, 
                      training_frame = train,
                      leaderboard_frame = test,
                      max_runtime_secs = 30)

    # View the AutoML Leaderboard
    lb <- aml@leaderboard
    lb

    #                                                       model_id      auc  logloss
    #  1          StackedEnsemble_AllModels_0_AutoML_20171121_012135 0.788321 0.554019
    #  2       StackedEnsemble_BestOfFamily_0_AutoML_20171121_012135 0.783099 0.559286
    #  3                   GBM_grid_0_AutoML_20171121_012135_model_1 0.780554 0.560248
    #  4                   GBM_grid_0_AutoML_20171121_012135_model_0 0.779713 0.562142
    #  5                   GBM_grid_0_AutoML_20171121_012135_model_2 0.776206 0.564970
    #  6                   GBM_grid_0_AutoML_20171121_012135_model_3 0.771026 0.570270

    #  [10 rows x 3 columns] 

    # The leader model is stored here
    aml@leader


    # If you need to generate predictions on a test set, you can make 
    # predictions directly on the `"H2OAutoML"` object, or on the leader 
    # model object directly

    pred <- h2o.predict(aml, test)  # predict(aml, test) also works

    # or:
    pred <- h2o.predict(aml@leader, test)



   .. code-block:: python

    import h2o
    from h2o.automl import H2OAutoML

    h2o.init()

    # Import a sample binary outcome train/test set into H2O
    train = h2o.import_file("https://s3.amazonaws.com/erin-data/higgs/higgs_train_10k.csv")
    test = h2o.import_file("https://s3.amazonaws.com/erin-data/higgs/higgs_test_5k.csv")

    # Identify predictors and response
    x = train.columns
    y = "response"
    x.remove(y)

    # For binary classification, response should be a factor
    train[y] = train[y].asfactor()
    test[y] = test[y].asfactor()
    
    # Run AutoML for 30 seconds
    aml = H2OAutoML(max_runtime_secs = 30)
    aml.train(x = x, y = y, 
              training_frame = train, 
              leaderboard_frame = test)

    # View the AutoML Leaderboard
    lb = aml.leaderboard
    lb

    #  model_id                                                    auc    logloss
    #  ----------------------------------------------------   --------  ---------
    #  StackedEnsemble_AllModels_0_AutoML_20171121_010846     0.786063   0.555833
    #  StackedEnsemble_BestOfFamily_0_AutoML_20171121_010846  0.783367   0.558511
    #  GBM_grid_0_AutoML_20171121_010846_model_1              0.779242   0.562157
    #  GBM_grid_0_AutoML_20171121_010846_model_0              0.778855   0.562648
    #  GBM_grid_0_AutoML_20171121_010846_model_3              0.769666   0.572165
    #  GBM_grid_0_AutoML_20171121_010846_model_2              0.769147   0.572064
    #  XRT_0_AutoML_20171121_010846                           0.744612   0.593885
    #  DRF_0_AutoML_20171121_010846                           0.733039   0.608609
    #  GLM_grid_0_AutoML_20171121_010846_model_0              0.685211   0.635138

    #  [9 rows x 3 columns]

    # The leader model is stored here
    aml.leader


    # If you need to generate predictions on a test set, you can make 
    # predictions directly on the `"H2OAutoML"` object, or on the leader 
    # model object directly

    preds = aml.predict(test)

    # or:
    preds = aml.leader.predict(test)



AutoML Output
-------------

The AutoML object includes a "leaderboard" of models that were trained in the process, including the performance of the model on the ``leaderboard_frame`` test set.  If the user did not specify the ``leaderboard_frame`` argument, then a frame will be automatically partitioned, as explained in the `Auto-Generated Frames <#auto-generated-frames>`__ section.  In the `future <https://0xdata.atlassian.net/browse/PUBDEV-5071>`__, the leaderboard will be created using cross-validation metrics, unless a scoring frame is provided explicitly by the user.

The models are ranked by a default metric based on the problem type (the second column of the leaderboard). In binary classification problems, that metric is AUC, and in multiclass classification problems, the metric is mean per-class error. In regression problems, the default sort metric is deviance.  Some additional metrics are also provided, for convenience.

Here is an example leaderboard for a binary classification task:

+-------------------------------------------------------------+----------+----------+
|                                                    model_id |      auc |  logloss |
+=============================================================+==========+==========+
| StackedEnsemble_AllModels_0_AutoML_20171121_012135          | 0.788321 | 0.554019 | 
+-------------------------------------------------------------+----------+----------+
| StackedEnsemble_BestOfFamily_0_AutoML_20171121_012135       | 0.783099 | 0.559286 |
+-------------------------------------------------------------+----------+----------+
| GBM_grid_0_AutoML_20171121_012135_model_1                   | 0.780554 | 0.560248 |
+-------------------------------------------------------------+----------+----------+
| GBM_grid_0_AutoML_20171121_012135_model_0                   | 0.779713 | 0.562142 |
+-------------------------------------------------------------+----------+----------+
| GBM_grid_0_AutoML_20171121_012135_model_2                   | 0.776206 | 0.564970 |
+-------------------------------------------------------------+----------+----------+
| GBM_grid_0_AutoML_20171121_012135_model_3                   | 0.771026 | 0.570270 |
+-------------------------------------------------------------+----------+----------+
| DRF_0_AutoML_20171121_012135                                | 0.734653 | 0.601520 |
+-------------------------------------------------------------+----------+----------+
| XRT_0_AutoML_20171121_012135                                | 0.730457 | 0.611706 |
+-------------------------------------------------------------+----------+----------+
| GBM_grid_0_AutoML_20171121_012135_model_4                   | 0.727098 | 0.666513 |
+-------------------------------------------------------------+----------+----------+
| GLM_grid_0_AutoML_20171121_012135_model_0                   | 0.685211 | 0.635138 |
+-------------------------------------------------------------+----------+----------+


FAQ
~~~

-  **Which models are trained in the AutoML process?**

  The current version of AutoML trains and cross-validates a default Random Forest (DRF), Extremely Randomized Trees (XRT), a random grid of Gradient Boosting Machines (GBMs), a random grid of Deep Neural Nets, a fixed grid of GLMs, and then trains two Stacked Ensemble models. Particular algorithms (or groups of algorithms) can be switched off using the ``exclude_algos`` argument.  This is useful if you already have some idea of the algorithms that will do well on your dataset.  As a recommendation, if you have really wide or sparse data, you may consider skipping the tree-based algorithms (GBM, DRF).

  A list of the hyperparameters searched over for each algorithm in the AutoML process is included in the appendix below.  More details about the hyperparamter ranges for the models will be added to the appendix at a later date.

  Both of the ensembles should produce better models than any individual model from the AutoML run.  One ensemble contains all the models, and the second ensemble contains just the best performing model from each algorithm class/family.  The "Best of Family" ensemble is optimized for production use since it only contains five models.  It should be relatively fast to use (to generate predictions on new data) without much degredation in model performance when compared to the "All Models" ensemble.   

-  **How do I save AutoML runs?**

  Rather than saving an AutoML object itself, currently, the best thing to do is to save the models you want to keep, individually.  A utility for saving all of the models at once, along with a way to save the AutoML object (with leaderboard), will be added in a future release.


Appendix: Grid Search Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AutoML performs hyperparameter search over a variety of H2O algorithms in order to deliver the best model. In AutoML, the following hyperparameters are supported by grid search.  Random Forest and Extremely Randomized Trees are not grid searched (in the current version of AutoML), so they are not included in the list below.

**GBM Hyperparameters**

-  ``score_tree_interval``
-  ``histogram_type``
-  ``ntrees``
-  ``max_depth``
-  ``min_rows``
-  ``learn_rate``
-  ``sample_rate``
-  ``col_sample_rate``
-  ``col_sample_rate_per_tree``
-  ``min_split_improvement``

**GLM Hyperparameters**

-  ``alpha``
-  ``missing_values_handling``

**Deep Learning Hyperparameters**

-  ``epochs``
-  ``adaptivate_rate``
-  ``activation``
-  ``rho``
-  ``epsilon``
-  ``input_dropout_ratio``
-  ``hidden``
-  ``hidden_dropout_ratios``


Additional Information
~~~~~~~~~~~~~~~~~~~~~~

- AutoML development is tracked `here <https://0xdata.atlassian.net/issues/?filter=20700>`__. This page lists all open or in-progress AutoML JIRA tickets.
- AutoML is currently in experimental mode ("V99" in the REST API).  This means that, although unlikely, the API (REST, R, Python or otherwise) may be subject to breaking changes.
