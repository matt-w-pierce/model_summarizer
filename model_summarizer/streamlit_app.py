import os
import sys
import ast
import pandas as pd
import streamlit as st
import matplotlib.image as mpimg

from model_summarizer.summarizer import ExperimentSummary

# TODO: Used for testing viewing model metrics as a table
use_metric_table = True

# Parse command line arguments
args = sys.argv
model_name = args[1]
model_dir = args[2]

# Splitting the app
st.beta_set_page_config(layout="wide")
st.title(model_name)

# Initialize the model summary
summary = ExperimentSummary(model_name, model_dir)
df = summary.get_data()
st.write(df)


# Functions
def get_metric(image_dict, metric_dict, exp_path, key, value):
    """
    For each metric, determines if it is image or value-based
    :param image_dict: Dictionary of image components
    :param metric_dict: Dictionary of value-based metrics
    :param exp_path: Path where the images are saved
    :param key: Metric name
    :param value: Metric value
    :return: image_dict, metric_dict
    """

    # Determines if it is an image
    img_txt = ('.png', '.jpeg', '.jpg')
    if (type(value) == str) and (os.path.isfile(os.path.join(exp_path, value))) and (value.lower().endswith(img_txt)):
        try:
            cwd = os.getcwd()
            exp_dir = os.path.basename(exp_path)
            img_path = os.path.join(cwd, model_dir, exp_dir, value)
            img = mpimg.imread(img_path)
            image_dict[key] = img
        except:
            err_txt = f'''\n Unable to read file: {value} in directory {exp_path}'''
            metric_dict[key] = err_txt
    else:
        metric_dict[key] = value

    return image_dict, metric_dict


def display_row(dis_col, data, show_f, show_hp):
    """
    Displays all of the data for a single row from the dataset
    :param dis_col: Which column to populate
    :param data: Row of data to be displayed
    :param show_f: Boolean to indicate if features should be displayed
    :param show_hp: Boolean to indicate if hyper parameters should be displayed
    :return: Text/formatting to be displayed
    """

    # Show the general model details
    txt = ''''''
    ignore_keys = ['title', 'description', 'init_time', 'exp_path', 'features', 'hyper_params']
    txt += f'''
    ### {data["title"]}
    \n**Description:** {data["description"]}
    \n**Run Time:** {data["init_time"]}
    \n**Output Folder:** {data["exp_path"]}
    \n**Model Type:** {data["model_type"]}
    '''

    # Show model features
    if show_f:
        txt += f'''\n**Features: **{data["features"]}'''

    # Show model hyperparameters
    if show_hp:
        # hp_dict = json.loads(row['hyper_params'])
        hp_dict = ast.literal_eval(data['hyper_params'])

        txt += f'''\n\n**Hyper Parameters: **'''
        if use_metric_table:
            dis_col.write(txt)
            txt = ''''''
            hp_df = pd.DataFrame.from_dict(hp_dict, orient='index').reset_index()
            hp_df.columns = ['parameter', 'value']
            dis_col.write(hp_df)
        else:
            for k, v in hp_dict.items():
                txt += f'''\n   * ***{k}:*** {v}'''

    # Sorting the model metrics into value-based and image metrics
    img_d = {}
    metric_d = {}
    txt += '''\n\n**Model Metrics: **'''
    for k, v in data.items():

        if k not in ignore_keys:
            img_d, metric_d = get_metric(img_d, metric_d, data['exp_path'], k, v)

    # Outputting the model metrics
    if use_metric_table:
        dis_col.write(txt)
        metric_df = pd.DataFrame.from_dict(metric_d, orient='index').reset_index()
        metric_df.columns = ['metric_name', 'metric_value']
        dis_col.write(metric_df)
    else:
        for k, v in metric_d.items():
            txt += f'''\n   * ***{k}:*** {v}'''
        dis_col.write(txt)

    # Outputting the model images
    dis_col.write(f'''\n\n**Model Images/Charts: **''')
    for k, v in img_d.items():
        dis_col.image(v, k)


# Setting up the StreamLit interface
def display_column(dis_col, exp_summary, row_idx):
    """
    Renders the entire column for the app
    :param dis_col: Which column to display as
    :param exp_summary: The model summarizer object
    :param row_idx: row index to display
    """

    row = exp_summary.row_to_dict(row_idx)
    display_row(dis_col, row, True, True)


# Displaying the columns
dis_cols = st.beta_columns(2)
for i, c in enumerate(dis_cols):
    option = c.selectbox(f'Row to view in column {i + 1}', df.index)
    display_column(c, summary, option)
