# Experiment Summarizer

## Installing the package
After cloning the repo, navigate to the base directory and run the following:
```
pip install .
```
This will install the model_summarizer package across your local system

## Initializing a model summary
To start, you will need to initialize an ExperimentSummary object. This object stores the details about the model you are developing as well as the details of all previous experiments.
Whether you are creating a new experiment history or reading in an existing dataset the syntax is the same.
```python
from model_summarizer.summarizer import ExperimentSummary

model_name = 'model_example'
model_path = 'C:\Documents\data-science\model_dir'

summary = ExperimentSummary(model_name, model_path)
```
In order to initialize the ModelSummary object both a model name and the absolute path to the model directory is required. 
When the ModelSummary is initialized, it looks for an experiment history with this model name in the provided directory. If the directory or the model history CSV file is not found, they will be created.

## Creating a new experiment
To create a new experiment, an Experiment object will also need to be initialized.

```python
from model_summarizer.summarizer import Experiment

title = 'Experiment #1'
desc = 'Some details and description about the experiment that is being run'
exp_dir = 'C:\Documents\data-science\model_dir\first_exp'

exp = Experiment(title, desc, exp_dir)
```

The title, description, and experiment path are required for object creation, but there are additional variables that can be included now or added later.
Please see the full documentation for the Experiment class below. 

## Features and Hyper Parameters
Features and hyper parameters are common attributes of all model experiments. 
These can both be provided as arguments during experiment initialization or they can be added later.
The features should be passed as a list and the hyper parameters should be passed as a dict.

```python
feature_list = ['col_one', 'col_two', 'col_three']
hyperparam_dict = {'param_one': 1, 'param_twp': 'value_two', 'param_three': True}

# Option 1: Specify at initialization
exp = Experiment(title, desc, exp_dir, features=feature_list, hyper_params=hyperparam_dict)

# Option 2: Add later
exp.set_features(feature_list)
exp.set_hyper_params(hyperparam_dict)
```

## Experiment Metrics
The summary interface currently support two types of model metrics: values and images. 
### Value-based
Value-based metrics are displayed as-is and support any of the built-in python data types (str, int, list, etc.). 
Adding value-based metrics to an experiment:

```python
exp.add_metric('numeric_metric', 0.12345)
exp.add_metric('text_metric', 'Some text value')
exp.add_metric('list_metric', [1, 2, 3, 4, 5])

bool_name = 'new_metric'
bool_value = True
exp.add_metric(bool_name, bool_value)
```

If features or hyper parameters are not specified they will be initialized as an empty list and empty dict respectively

### Images and Charts
When run, the summarizer will also attempt to identify image-based metrics such as charts, tables, etc.
The addition of these metric is identical to above, but the value should be the absolute path to an image file. 
When run, the summarizer will look through all metrics and if any of the values appear to be the path to an image file it will attempt to read in the image and display it. 
If the image cannot be read in, it will return an error message instead. 

```python
exp.add_metric('image_metric', 'C:\Documents\data-science\model_dir\first_exp\some_image.png')
```

## Adding the experiment to the model summary
At the end of the experiment code the experiment is added to the model summary:

```python
summary.add_experiment(exp)
```

## Running the Summary interface
### Installing streamlit
Streamlit is a required library for the summary interface and can be installed using pip
    
```
pip install streamlit
```

See the streamlit documentation for more information: https://docs.streamlit.io/en/stable/

### Running the interface
Open the command line and navigate to the parent directory that contains the model directory. In the above example, this would be `C:\Documents\data-science\`, which contains `model_dir`.

To run the interface you need to tell streamlit to run the experiment_summary.py file that is included in the model_summarizer repo. 
* **NOTE:** The easiest way to do this may be to copy this file into the parent directory (e.g. data-science)

The last step is to tell streamlit to run the application and include the `model_name` and `model_dir` as ordered parameters (these should be the same as what was passed to the ExperimentSummary initialization)
```
streamlit run <path to model_summarizer/streamlit_app.py> <model_name> <model_dir>
```
Using above example:
```
streamlit run streamlit_app.py model_example model_dir
```
This command should open the interface as a new window in your browser

## Examples
There is also an example of initializing and model summary and adding two experiments. It can be found in the ```examples``` directory. 