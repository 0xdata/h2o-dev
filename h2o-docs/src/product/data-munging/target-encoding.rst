Target Encoding
---------------

Target encoding is the process of replacing a categorical value with the mean of the target variable. In this example, we will be trying to predict ``bad_loan`` using our cleaned lending club data: https://raw.githubusercontent.com/h2oai/app-consumer-loan/master/data/loan.csv.

One of the predictors is ``addr_state``, a categorical column with 50 unique values. To perform target encoding on ``addr_state``, we will calculate the average of ``bad_loan`` per state (since ``bad_loan`` is binomial, this will translate to the proportion of records with ``bad_loan = 1``).

For example, target encoding for ``addr_state`` could be:

+---------------+---------------------+
| addr\_state   | average bad\_loan   |
+===============+=====================+
| AK            | 0.1476998           |
+---------------+---------------------+
| AL            | 0.2091603           |
+---------------+---------------------+
| AR            | 0.1920290           |
+---------------+---------------------+
| AZ            | 0.1740675           |
+---------------+---------------------+
| CA            | 0.1780015           |
+---------------+---------------------+
| CO            | 0.1433022           |
+---------------+---------------------+

Instead of using state as a predictor in our model, we could use the target encoding of state.

In this topic, we will walk through the steps for using target encoding to convert categorical columns to numeric. This can help improve machine learning accuracy since algorithms tend to have a hard time dealing with high cardinality columns.

The jupyter notebook, `categorical predictors with tree based model <https://github.com/h2oai/h2o-tutorials/blob/master/best-practices/categorical-predictors/gbm_drf.ipynb>`__, discusses two methods for dealing with high cardinality columns:

-  Comparing model performance after removing high cardinality columns
-  Parameter tuning (specifically tuning ``nbins_cats`` and ``categorical_encoding``)

In this topic, we will try using target encoding to improve our model performance.

Train Baseline Model
~~~~~~~~~~~~~~~~~~~~


.. example-code::
   .. code-block:: r

    library(h2o)
    h2o.init()
    h2o.no_progress()

    # Start by training a model using the original data. 
    # Below we import our data into the H2O cluster.
    df <- h2o.importFile("https://raw.githubusercontent.com/h2oai/app-consumer-loan/master/data/loan.csv")
    df$bad_loan <- as.factor(df$bad_loan)

    # Randomly split the data into 75% training and 25% testing. 
    # We will use the testing data to evaluate how well the model performs.
    splits <- h2o.splitFrame(df, seed = 1234, 
                             destination_frames=c("train.hex", "test.hex"), 
                             ratios = 0.75)
    train <- splits[[1]]
    test <- splits[[2]]

    # Now train the baseline model. 
    # We will train a GBM model with early stopping.
    response <- "bad_loan"
    predictors <- c("loan_amnt", "int_rate", "emp_length", "annual_inc", "dti", 
                    "delinq_2yrs", "revol_util", "total_acc", "longest_credit_length",
                    "verification_status", "term", "purpose", "home_ownership", 
                    "addr_state")

    gbm_baseline <- h2o.gbm(x = predictors, y = response, 
                            training_frame = train, validation_frame = test,
                            score_tree_interval = 10, ntrees = 500,
                            sample_rate = 0.8, col_sample_rate = 0.8, seed = 1234,
                            stopping_rounds = 5, stopping_metric = "AUC", 
                            stopping_tolerance = 0.001,
                            model_id = "gbm_baseline.hex")

    # Get the AUC on the training and testing data:
    train_auc <- h2o.auc(gbm_baseline, train = TRUE)
    valid_auc <- h2o.auc(gbm_baseline, valid = TRUE)

    auc_comparison <- data.frame('Data' = c("Training", "Validation"),
                                 'AUC' = c(train_auc, valid_auc))

    auc_comparison
            Data       AUC
    1   Training 0.7492599
    2 Validation 0.7070187


   .. code-block:: python

    import h2o
    h2o.init()

    # Start by training a model using the original data. 
    # Below we import our data into the H2O cluster.
    df = h2o.import_file("https://raw.githubusercontent.com/h2oai/app-consumer-loan/master/data/loan.csv")
    df['bad_loan'] = df['bad_loan'].asfactor()

    # Randomly split the data into 75% training and 25% testing. 
    # We will use the testing data to evaluate how well the model performs.
    train, test = df.split_frame(ratios=[0.75], seed=1234)

    # Now train the baseline model. 
    # We will train a GBM model with early stopping.

    from h2o.estimators.gbm import H2OGradientBoostingEstimator
    predictors = ["loan_amnt", "int_rate", "emp_length", "annual_inc", "dti", 
                  "delinq_2yrs", "revol_util", "total_acc", "longest_credit_length",
                  "verification_status", "term", "purpose", "home_ownership", 
                  "addr_state"]
    response = "bad_loan"

    gbm_baseline=H2OGradientBoostingEstimator(score_tree_interval=10,
                                              ntrees=500,
                                              sample_rate=0.8,
                                              col_sample_rate=0.8,
                                              seed=1234,
                                              stopping_rounds=5,
                                              stopping_metric="AUC",
                                              stopping_tolerance=0.001,
                                              model_id="gbm_baseline.hex")

    gbm_baseline.train(x=predictors, y=response, training_frame=train,
                       validation_frame=test)

    # Get the AUC on the training and testing data:
    train_auc = gbm_baseline.auc(train=True)
    train_auc
    0.7492599314713426

    valid_auc = gbm_baseline.auc(valid=True)
    valid_auc
    0.707018686126265


Our training data has much higher AUC than our validation data.

The variables with the greatest importance are ``int_rate``, ``addr_state``, ``annual_inc``, and ``term``. It makes sense that the ``int_rate`` has such high variable importance because this is related to loan default, but it is surprising that ``addr_state`` has such high variable importance. The high variable importance could be because our model is memorizing the training data through this high cardinality categorical column.

.. example-code::
   .. code-block:: r

    # Variable Importance
    h2o.varimp_plot(gbm_baseline)

   .. code-block:: python

    # Variable Importance
    gbm_baseline.varimp_plot()

.. figure:: ../images/gbm_variable_importance1.png
   :alt: GBM Variable importance - first run
   :height: 348
   :width: 325

See if the AUC improves on the test data if we remove the ``addr_state`` predictor. This can indicate that the model is memorizing the training data.

.. example-code::
   .. code-block:: r


    predictors <- setdiff(predictors, "addr_state")

    gbm_no_state <- h2o.gbm(x = predictors, y = response, 
                            training_frame = train, validation_frame = test, 
                            score_tree_interval = 10, ntrees = 500,
                            sample_rate = 0.8, col_sample_rate = 0.8, seed = 1234,
                            stopping_rounds = 5, stopping_metric = "AUC", stopping_tolerance = 0.001,
                            model_id = "gbm_no_state.hex")

    # Get the AUC for the baseline model and the model without ``addr_state``
    auc_baseline <- h2o.auc(gbm_baseline, valid = TRUE)
    auc_nostate <- h2o.auc(gbm_no_state, valid = TRUE)

    auc_comparison <- data.frame('Model' = c("Baseline", "No addr_state"),
                                 'AUC' = c(auc_baseline, auc_nostate))

    auc_comparison
              Model       AUC
    1      Baseline 0.7070187
    2 No addr_state 0.7076197

   .. code-block:: python

    predictors = ["loan_amnt", "int_rate", "emp_length", "annual_inc", "dti",
                  "delinq_2yrs", "revol_util", "total_acc", "longest_credit_length",
                  "verification_status", "term", "purpose", "home_ownership"]

    gbm_no_state=H2OGradientBoostingEstimator(score_tree_interval=10,
                                              ntrees=500,
                                              sample_rate=0.8,
                                              col_sample_rate=0.8,
                                              seed=1234,
                                              stopping_rounds=5,
                                              stopping_metric="AUC",
                                              stopping_tolerance=0.001,
                                              model_id="gbm_no_state.hex")

    gbm_no_state.train(x=predictors, y=response, training_frame=train,
                       validation_frame=test)

    auc_baseline = gbm_baseline.auc(valid=True)
    auc_baseline
    0.707018686126265

    auc_nostate = gbm_no_state.auc(valid=True)
    auc_nostate
    0.7076197256885596

We see a slight improvement in our test AUC if we do not include the ``addr_state`` predictor. This is a good indication that the GBM model may be overfitting with this column.

Target Encoding in H2O-3
~~~~~~~~~~~~~~~~~~~~~~~~

Now we will perform target encoding on ``addr_state`` to see if this representation improves our model performance.

Target encoding in H2O-3 is performed in two steps:


1. Create (fit) a target encoding map. This will contain the sum of the response column and the count. This can include an optional ``fold_column``. 
2. Transform a target encoding map. The target encoding map is applied to the data by adding new columns with the target encoding values.

 The following options are available when transforming the target encoding, we have several options included to prevent overfitting:

 -  ``holdout_type``: Specify whether or not a holdout should be used in constructing the target average. This can help prevent overfitting. Options include ``kfold``, ``loo``, and ``none``. 
 -  ``blended_avg``: Specify whether to perform a blended average. This can help prevent overfitting.
 -  ``noise``: Specify whether to include random noise to the average. This can help prevent overfitting.
 -  ``fold_column``: Specify the name or column index of the fold column in the data. This defaults to NULL (no `fold_column`). This option is only required if `holdout_type = "KFold"`.
 -  ``seed``: Specify a random seed used to generate draws from the uniform distribution for random noise. Defaults to -1.

Holdout Type
''''''''''''

The ``holdout_type`` parameter defines whether the target average should be constructed on all rows of data. Overfitting can be prevented by removing some hold out data when calculating the target average on the training data.

The ``h2o.target_encode_apply`` (R)/``transform`` (Python) function offers the following ``holdout_type`` options:

-  ``none``: no holdout. The mean is calculating on all rows of data \*\*. This should be used for test data
-  ``loo``: mean is calculating on all rows of data excluding the row itself.

   -  This can be used for the training data. The target of the row itself is not included in the average to prevent overfitting.

-  ``kfold``: The mean is calculating on out-of-fold data only. (This options requires a fold column.)

   -  This can be used for the training data. The target average is calculated on the out of fold data to prevent overfitting

Blended Average
'''''''''''''''

The ``blended_avg`` parameter defines whether the target average should be weighted based on the count of the group. It is often the case, that some groups may have a small number of records and the target average will be unreliable. To prevent this, the blended average takes a weighted average of the group's target value and the global target value.

Noise
'''''

The ``noise`` parameter determines if random noise should be added to the target average.

Perform Target Encoding
~~~~~~~~~~~~~~~~~~~~~~~

Start by creating the target encoding map. This has the number of bad loans per state (``numerator``) and the number of rows per state (``denominator``). We can later use this information to create the target encoding per state.

.. example-code::
   .. code-block:: r

    train$fold <- h2o.kfold_column(train, 5, seed = 1234)
    te_map <- h2o.target_encode_create(train, x = list("addr_state"), 
                                       y = response, fold_column = "fold")
    head(te_map$addr_state)

    ##   addr_state fold numerator denominator
    ## 1         AK    0         3          11
    ## 2         AK    1         0           5
    ## 3         AK    2         1          10
    ## 4         AK    3         2          13
    ## 5         AK    4         1           7
    ## 6         AL    0         7          52

   .. code-block:: python

    foldColumnName="fold"
    train[foldColumnName] = train.kfold_column(n_folds=5, seed=1234)
    
    from h2o.targetencoder import TargetEncoder
    teColumns=["addr_state"]
    te_map = TargetEncoder(x=teColumns, y=response, fold_column="fold", blending_avg=True)
    te_map.fit(train)


Apply the target encoding to our training and testing data. For our training data, we will use the parameters:

-  ``holdout_type``: "KFold"
-  ``blended_avg``/``blending_avg``: TRUE
-  ``noise_level``/``noise``: NULL (by default it will add 0.01 \* range of y of random noise)

.. example-code::
   .. code-block:: r

    ext_train <- h2o.target_encode_apply(train, x = list("addr_state"), y = response, 
                                         target_encode_map = te_map, holdout_type = "KFold",
                                         fold_column = "fold",
                                         blended_avg = TRUE, noise_level = 0, seed = 1234)

    head(ext_train[c("addr_state", "fold", "TargetEncode_addr_state")])

    ##   addr_state fold TargetEncode_addr_state
    ## 1         AK    0               0.1212239
    ## 2         AK    0               0.1212239
    ## 3         AK    0               0.1212239
    ## 4         AK    0               0.1212239
    ## 5         AK    0               0.1212239
    ## 6         AK    0               0.1212239

   .. code-block:: python

    ext_train = te_map.transform(is_train_or_valid=True, 
                                 frame=train, 
                                 holdout_type="kfold", 
                                 noise=0.0,
                                 seed=1234)

    head_ext_train = ext_train.head(rows=5, cols=17)


For our testing data, we will use the parameters:

-  ``holdout_type``: "None"
-  ``blended_avg``: False
-  ``noise_level``: 0

We do not need to apply any of the overfitting prevention techniques since our target encoding map was created on the training data, not the testing data.

.. example-code::
   .. code-block:: r

    ext_test <- h2o.target_encode_apply(test, x = list("addr_state"), y = response,
                                        target_encode_map = te_map, holdout_type = "None",
                                        fold_column = "fold",
                                        blended_avg = FALSE, noise_level = 0)

    head(ext_test[c("addr_state", "TargetEncode_addr_state")])

    ##   addr_state TargetEncode_addr_state
    ## 1         AK               0.1521739
    ## 2         AK               0.1521739
    ## 3         AK               0.1521739
    ## 4         AK               0.1521739
    ## 5         AK               0.1521739
    ## 6         AK               0.1521739

   .. code-block:: python

    ext_test = te_map.transform(is_train_or_valid=True, 
                                frame=test, 
                                holdout_type="none", 
                                noise=0.0,
                                seed=1234)

    head_ext_test = ext_test.head()



Train Model with KFold Target Encoding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Train a new model, this time replacing the ``addr_state`` with the ``TargetEncode_addr_state``.

.. example-code::
   .. code-block:: r

    predictors <- c("loan_amnt", "int_rate", "emp_length", "annual_inc", 
                    "dti", "delinq_2yrs", "revol_util", "total_acc", 
                    "longest_credit_length", "verification_status", "term", 
                    "purpose", "home_ownership", "TargetEncode_addr_state")

    gbm_state_te <- h2o.gbm(x = predictors, 
                            y = response, 
                            training_frame = ext_train, 
                            validation_frame = ext_test, 
                            score_tree_interval = 10, 
                            ntrees = 500,
                            stopping_rounds = 5, 
                            stopping_metric = "AUC", 
                            stopping_tolerance = 0.001,
                            model_id = "gbm_state_te.hex")

   .. code-block:: python

    predictors = ["loan_amnt", "int_rate", "emp_length", "annual_inc", 
                  "dti", "delinq_2yrs", "revol_util", "total_acc", 
                  "longest_credit_length", "verification_status", 
                  "term", "purpose", "home_ownership", "addr_state_te"]

    gbm_state_te=H2OGradientBoostingEstimator(score_tree_interval=10,
                                              ntrees=500,
                                              sample_rate=0.8,
                                              col_sample_rate=0.8,
                                              seed=1234,
                                              stopping_rounds=5,
                                              stopping_metric="AUC",
                                              stopping_tolerance=0.001,
                                              model_id="gbm_no_state.hex")

    gbm_state_te.train(x=predictors, y=response, training_frame=ext_train,
                       validation_frame=ext_test)


The AUC of the first and second model is shown below:

.. example-code::
   .. code-block:: r

    # Get AUC
    auc_state_te <- h2o.auc(gbm_state_te, valid = TRUE)

    auc_comparison <- data.frame('Model' = c("No Target Encoding", 
                                             "No addr_state", 
                                             "addr_state Target Encoding"),
                                 'AUC' = c(auc_baseline, auc_nostate, auc_state_te))

    auc_comparison
                           Model       AUC
    1         No Target Encoding 0.7198658
    2              No addr_state 0.7270537
    3 addr_state Target Encoding 0.7254448

  .. code-block:: python

   # Get AUC
   auc_state_te = gbm_state_te.auc(valid=True)
   auc_state_te
   0.7091353041718448



We see a slight increase in the AUC on the test data. Now the ``addr_state`` has much smaller variable importance. It is no longer the most important feature but the 8th.

.. example-code::
   .. code-block:: r

    # Variable Importance
    h2o.varimp_plot(gbm_state_te)

   .. code-block:: python

    # Variable Importance
    gbm_state_te.varimp_plot()


.. figure:: ../images/gbm_variable_importance2.png
   :alt: GBM Variable importance - second run
   :height: 336
   :width: 470

References
~~~~~~~~~~

-  `Target Encoding in H2O-3 Demo <https://github.com/h2oai/h2o-3/blob/master/h2o-r/demos/rdemo.target_encode.R>`__
-  `Automatic Feature Engineering Webinar <https://www.youtube.com/watch?v=VMTKcT1iHww>`__
-   Daniele Micci-Barreca. 2001. A preprocessing scheme for high-cardinality categorical attributes in classification and prediction problems. SIGKDD Explor. Newsl. 3, 1 (July 2001), 27-32.
