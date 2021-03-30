import pandas as pd
from pandas.core.common import SettingWithCopyWarning
import warnings
warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

##  UNDER CONSTRUCTION ##

def analyse(folder):
    wd = os.getcwd()
    f = glob.glob(f"{wd}/logs/{folder}/*.tsv")[0]

    sub, ses, task, run, _ = [i.split('-')[-1] for i in folder.split('_')]
    sz = task[-1]
    task = task[:-1]

    df = pd.read_table(f, keep_default_na=True)
    df = df[df.event_type == 'response']
    df.drop(['nr_frames', 'duration'], axis=1, inplace=True)
    df['attn_size'] = sz
    df['corr_L'] = np.nan
    df['corr_S'] = np.nan

    cols = [['large_prop', 'small_prop'], ['corr_L', 'corr_S']]
    summary = pd.DataFrame([])
    not_task = pd.DataFrame([])

    for prop, cor in zip(cols[0], cols[1]):
        true_left = df[(df[prop] > 0.5) & (df.response == 'left')].index
        false_left = df[(df[prop] < 0.5) & (df.response == 'left')].index
        true_right = df[(df[prop] < 0.5) & (df.response == 'right')].index
        false_right = df[(df[prop] > 0.5) & (df.response == 'right')].index

        df.loc[np.hstack((true_left, true_right)), cor] = 1
        df.loc[np.hstack((false_left, false_right)), cor] = 0
        df = df.dropna(subset=[cor])

        diffs = sorted(df[prop].unique())
        task_summary = pd.DataFrame([])

        for idx, diff in enumerate(diffs):
            task_summary.loc[idx, 'attn_size'] = prop.split('_')[0]
            task_summary.loc[idx, 'diff'] = diff
            task_summary.loc[idx, 'n_trials'] = len(df[df[prop] == diff])
            task_summary.loc[idx, 'resp_left'] = len(df[(df[prop] == diff) & (df.response == "left")]) / len(
                df[df[prop] == diff])
            task_summary.loc[idx, 'n_correct'] = len(df[(df[prop] == diff) & (df[cor] == 1)])
            task_summary.loc[idx, 'percent_correct'] = 100 * len(df[(df[prop] == diff) & (df[cor] == 1)]) / len(
                df[df[prop] == diff])

        summary = summary.append(task_summary, ignore_index=True)

    return df, summary


