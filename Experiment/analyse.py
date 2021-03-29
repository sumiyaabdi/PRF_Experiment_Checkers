import pandas as pd
from pandas.core.common import SettingWithCopyWarning
import warnings
warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def analyse(folder):
    "Analyse and plot figure for each attention task run"
    sub,ses,task,run = [i.split('-')[-1] for i in folder.split('_')]
    sz = task[-1]
    task=task[:-1]





fname='0_ses-0_task-2afcL_run-0_Logs'
analyse(fname)