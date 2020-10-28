import os
import pandas as pd
from datetime import datetime


class Experiment:
    """
    A single instance of a model experiment that can be added to ExperimentSummary

    :param str title: title of experiment
    :param str description: experiment details
    :param Path exp_path: path to output directory
    :param list features: model features
    :param str model_type: type of model used
    :param dict hyper_params: model hyperparameters
    :param dict metrics: additional model metrics

    |
    """

    def __init__(self, title,
                 description,
                 exp_path,
                 features=None,
                 model_type=None,
                 hyper_params=None,
                 metrics=None):

        self.title = title
        self.description = description
        self.exp_path = exp_path
        self.init_time = datetime.now()

        if features is None:
            self.features = []
        else:
            self.features = features.copy()

        if model_type is None:
            self.model_type = ''
        else:
            self.model_type = model_type

        if hyper_params is None:
            self.hyper_params = {}
        else:
            self.hyper_params = hyper_params.copy()

        if metrics is None:
            self.metrics = {}
        else:
            self.metrics = metrics.copy()

    def set_features(self, features):
        """
        Replaces all features with provided list

        :param list features: list of features

        |
        """

        self.features = features.copy()

    def add_feature(self, feature):
        """
        Adds a feature to the experiment

        :param str feature: feature to add

        |
        """

        self.features.append(feature)

    def set_model_type(self, model_type):
        """
        Sets/replaces the model type

        :param str model_type: model type

        |
        """

        self.model_type = model_type

    def set_hyper_params(self, hyper_params):
        """
        Sets/replaces the model hyper parameters

        :param dict hyper_params: hyper parameter dictionary

        |
        """

        self.hyper_params = hyper_params.copy()

    def add_hyper_param(self, key, val):
        """
        Adds a hyper parameter to the experiment
        :param str key: parameter name
        :param val: parameter value

        |
        """

        self.hyper_params[key] = val

    def set_metrics(self, metrics: dict):
        """
        Replaces the metric dictionary

        :param dict metrics: metric dict

        |
        """
        self.metrics = metrics.copy()

    def add_metric(self, key, val, overwrite=False):
        """
        Adds a metric to the experiment

        :param str key: metric name
        :param val: metric value
        :param bool overwrite: replace value if metric key already exists

        .. warning:: If ``overwrite = False`` and the key already exists, an exception will be thrown

        |
        """

        if key in self.metrics.keys() and not overwrite:
            raise Exception(f'Metric for key "{key}" already exists. '
                            f'Set overwrite=True to overwrite the value for this key')
        else:
            self.metrics[key] = val

    def get_metrics(self):
        """
        Returns the metric dict

        :return: dict

        |
        """
        return self.metrics

    def to_dict(self):
        """
        Returns the Experiment object as a dict

        :return: dict

        |
        """
        out_d = {
            'title': self.title,
            'description': self.description,
            'exp_path': self.exp_path,
            'init_time': self.init_time,
            'model_type': self.model_type,
            'features': self.features,
            'hyper_params': self.hyper_params
        }

        out_d.update(self.metrics)
        return out_d

    def get_col_order(self):
        """
        Returns the correct column order for the output DataFrame

        :return: list

        |
        """

        base_cols = ['title', 'description', 'exp_path', 'init_time', 'model_type', 'features', 'hyper_params']
        return base_cols + list(self.metrics.keys())


class ExperimentSummary:
    """
    Records and stores results during model training and evaluation

    Storage options:
     - Locally stored CSV file
     - Local database (likely either PostgresDB or MySQL)
    """

    def __init__(self, model_name, csv_path: str, create_path: bool = False):
        """
        :param model_name: Name of model, is used to name the CSV file and/or database table
        :param csv_path: Absolute path to the CSV file that is used to store experiment details
        """

        self.model_name = model_name
        self.csv_path = csv_path
        self.csv_file = f'{model_name}_model_summary.csv'

        self.df = self.__connect_data_source()

        if not os.path.isdir(csv_path):
            os.makedirs(csv_path)

    def update_csv_path(self, csv_path: str):
        """
        Sets/updates the csv_path parameter
        :param csv_path: Upadted path to the CSV file
        """

        self.csv_path = csv_path
        self.csv_file = f'{self.model_name}_model_summary.csv'
        self.__connect_data_source()

    def __connect_data_source(self):
        """
        Checks to ensure that the provided storage method exists
            - CSV file: Checks if file exists, if so, reads it in
            - Database: Verifies database & table exists, if not, creates it
        """

        # Checks to see if the CSV file already exists
        if os.path.isfile(os.path.join(self.csv_path, self.csv_file)):
            df = pd.read_csv(os.path.join(self.csv_path, self.csv_file))

        else:
            df = pd.DataFrame()

        return df

    def add_experiment(self, model_exp: Experiment):
        """
        Adds the provided Experiment instance to the dataset
        :param model_exp: Instance of the Experiment class
        """

        # Getting the model metrics and creating new columns in dataset as necessary
        metric_d = model_exp.get_metrics()
        for k, v in metric_d.items():
            if k not in self.df.columns:
                self.df[k] = None

        # Adding the new experiment to the dataset and making sure the column order is still correct
        new_df = pd.DataFrame([model_exp.to_dict()])
        col_order = model_exp.get_col_order()
        self.df = pd.concat([self.df, new_df])
        self.df = self.df[col_order]

        # Saving the updated DataFrame
        self.df.to_csv(os.path.join(self.csv_path, self.csv_file), index=False)

    def get_data(self):
        """
        :return: DataFrame
        """
        return self.df

    def row_to_dict(self, idx):
        """
        Given an index in DataFrame, returns the row as a dict
        :param idx: Row index to return
        :return: dict
        """

        row = self.df.iloc[idx]
        return row.to_dict()
