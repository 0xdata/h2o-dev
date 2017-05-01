# -*- encoding: utf-8 -*-
import h2o
from h2o.job import H2OJob
from h2o.frame import H2OFrame
from h2o.utils.typechecks import assert_is_type

class H2OAutoML(object):
    """
    AutoML: Automate parts of the model training process

    :examples:
    >>> # Setting up an H2OAutoML object
    >>> a1 = H2OAutoML(max_runtime_secs=30)
    """
    def __init__(self,max_runtime_secs = None,build_control=None):

        #Check if H2O jar contains AutoML
        try:
            h2o.api("GET /3/Metadata/schemas/AutoMLV99")
        except h2o.exceptions.H2OResponseError as e:
            print e
            print "*******************************************************************\n" \
                  "*Please verify that your H2O jar has the proper AutoML extensions.*\n" \
                  "*******************************************************************\n" \
                  "\nVerbose Error Message:"

        if max_runtime_secs is None:
            max_runtime_secs = 600
            self.max_runtime_secs = max_runtime_secs
        else:
            assert_is_type(max_runtime_secs,int)
            self.max_runtime_secs = max_runtime_secs

        if build_control is None:
            self.build_control = {
                'stopping_criteria': {
                    'max_runtime_secs': max_runtime_secs,
                }
            }
        else:
            assert_is_type(build_control,dict)
            build_control["stopping_criteria"]["max_runtime_secs"] = max_runtime_secs

        self._job=None
        self._automl_key=None
        self._leader_id=None
        self._leaderboard=None

    def train(self,x=None,y=None,training_frame=None,validation_frame=None,test_frame=None):
        """
        Begins the automl task, which is a background task that incrementally improves
        over time. At any point, the user may use the "predict"/"performance"
        to inspect the incremental

        :param x: A list of column names or indices indicating the predictor columns.
        :param y: An index or a column name indicating the response column.
        :param training_frame: The H2OFrame having the columns indicated by x and y (as well as any
            additional columns specified by fold, offset, and weights).
        :param validation_frame: H2OFrame with validation data to be scored on while training.
        :param test_frame: H2OFrame with test data to be scored on in the leaderboard.

        :returns: An H2OAutoML object.

        :examples:
        >>> # Set up an H2OAutoML object
        >>> a1 = H2OAutoML(response_column="class", training_path=training_path, build_control=build_control)
        >>> # Launch H2OAutoML
        >>> a1.train()
        """

        #Minimal required argumens are training_frame and y (response)
        if y is None:
            raise ValueError('The response_column is not set; please set it to the name of the column that you are trying to predict in your data.')
        else:
            assert_is_type(y,int,str)
            input_spec = {
                'response_column': y,
            }

        if training_frame is None:
            raise ValueError('The training frame is not set!')
        else:
            assert_is_type(training_frame,H2OFrame)
            input_spec['training_frame'] = training_frame.frame_id

        if validation_frame is not None:
            assert_is_type(training_frame,H2OFrame)
            input_spec['validation_frame'] = validation_frame.frame_id

        if test_frame is not None:
            assert_is_type(training_frame,H2OFrame)
            input_spec['test_frame'] = test_frame.frame_id

        if x is not None:
            assert_is_type(x,list)
            names = training_frame.names
            ignored_columns = set(names) - {y} - set(x)
            input_spec['ignored_columns'] = list(ignored_columns)

        automl_build_params = {
            'input_spec': input_spec,
        }

        # NOTE: if the user hasn't specified some block of parameters don't send them!
        # This lets the back end use the defaults.
        if None is not self.build_control:
            automl_build_params['build_control'] = self.build_control

        resp = h2o.api('POST /99/AutoMLBuilder',json=automl_build_params)
        if 'job' not in resp:
            print("Exception from the back end: ")
            print(resp)
            return

        self._job = H2OJob(resp['job'], "AutoML")
        self._automl_key = self._job.dest_key
        self._job.poll()
        self._fetch()

    def project_name(self):
        """
        Retrieve the project name for an H2OAutoML object

        :return: the project name (a string) of the H2OAutoML object

        :examples:
        >>> # Set up an H2OAutoML object
        >>> a1 = H2OAutoML(response_column="class", training_path=training_path, build_control=build_control)
        >>> # Get the project name
        >>> a1.project_name()
        """
        res = h2o.api("GET /99/AutoML/"+self._automl_key)
        return res["project"]

    def get_leader(self):
        """
        Retrieve the top model from an H2OAutoML object

        :return: an H2O model

        :examples:
        >>> # Set up an H2OAutoML object
        >>> a1 = H2OAutoML(response_column="class", training_path=training_path, build_control=build_control)
        >>> # Launch H2OAutoML
        >>> a1.train()
        >>> # Get the top model
        >>> a1.get_leader()
        """
        leader = h2o.get_model(self._leader_id)
        return leader

    def get_leaderboard(self):
        """
        Retrieve the leaderboard from an H2OAutoML object

        :return: an H2OFrame with model ids in the first column and evaluation metric in the second column sorted
                 by the evaluation metric

        :examples:
        >>> # Set up an H2OAutoML object
        >>> a1 = H2OAutoML(response_column="class", training_path=training_path, build_control=build_control)
        >>> # Launch H2OAutoML
        >>> a1.train()
        >>> # Get the leaderboard
        >>> a1.get_leaderboard()
        """
        res = h2o.api("GET /99/AutoML/"+self._automl_key)
        return res["leaderboard_table"]

    def predict(self, test_data):
        """
        Predict on a dataset.

        :param H2OFrame test_data: Data on which to make predictions.

        :returns: A new H2OFrame of predictions.

        :examples:
        >>> #Set up an H2OAutoML object
        >>> a1 = H2OAutoML(response_column="class", training_path=training_path, build_control=build_control)
        >>> #Launch H2OAutoML
        >>> a1.train()
        >>> #Predict with #1 model from H2OAutoML leaderboard
        >>> a1.predict()

        """
        if self._fetch():
            self._model = h2o.get_model(self._leader_id)
            return self._model.predict(test_data)
        print("No model built yet...")

    #-------------------------------------------------------------------------------------------------------------------
    # Private
    #-------------------------------------------------------------------------------------------------------------------
    def _fetch(self):
        res = h2o.api("GET /99/AutoML/"+self._automl_key)
        self._leaderboard = [key["name"] for key in res['leaderboard']['models']]

        if self._leaderboard is not None and len(self._leaderboard) > 0:
            self._leader_id = self._leaderboard[0]
        else:
            self._leader_id = None
        return self._leader_id is not None

