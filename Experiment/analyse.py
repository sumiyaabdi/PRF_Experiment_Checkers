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

def analyse2afc(folder):
    wd = os.getcwd()
    f = glob.glob(f"{wd}/logs/{folder}/*.tsv")[0]

    sub,ses,task,run,_ = [i.split('-')[-1] for i in folder.split('_')]
    sz = task[-1]
    task=task[:-1]

    df = pd.read_table(f,keep_default_na=True)
    df = df[df.event_type == 'response']
    df.drop(['nr_frames','duration'],axis=1,inplace=True)
    df['attn_size']=sz
    df['corr_L'] = np.nan
    df['corr_S'] = np.nan

    cols = [['large_prop','small_prop'],['corr_L','corr_S']]
    summary = pd.DataFrame([])
    not_task = pd.DataFrame([])

    for prop,cor in zip(cols[0],cols[1]):
        true_left = df[(df[prop] > 0.5) & (df.response == 'left')].index
        false_left = df[(df[prop] < 0.5) & (df.response == 'left')].index
        true_right = df[(df[prop] < 0.5) & (df.response == 'right')].index
        false_right = df[(df[prop] > 0.5) & (df.response == 'right')].index

        df.loc[np.hstack((true_left,true_right)), cor] = 1
        df.loc[np.hstack((false_left,false_right)), cor] = 0
        df =  df.dropna(subset=[cor])

        diffs = sorted(df[prop].unique())
        task_summary = pd.DataFrame([])

        for idx, diff in enumerate(diffs):
            task_summary.loc[idx,'attn_size'] = prop.split('_')[0][0]
            task_summary.loc[idx,'diff'] = diff
            task_summary.loc[idx,'n_trials'] = len(df[df[prop] == diff])
            task_summary.loc[idx,'resp_left'] = len(df[(df[prop] == diff ) & (df.response == "left")])/len(df[df[prop] == diff])
            task_summary.loc[idx,'n_correct'] = len(df[(df[prop] == diff) & (df[cor] == 1)])
            task_summary.loc[idx,'percent_correct'] = 100*len(df[(df[prop] == diff) & (df[cor] == 1)])/len(df[df[prop] == diff])

        summary = summary.append(task_summary, ignore_index=True)

    return df, summary

def sigmoid(x,x0,k):
    y = np.array(1 / (1 + np.exp(-k*(x-x0))))
    return y

def weibull(x,x0,k,g,l):
    y = g +(1-g -l)*sigmoid(x,k)
    return y

def inv_sigmoid(y,x0,k):
    return x0 - (np.log((1/y)-1)/k)


f = 'sub-001_ses-1_task-2afcL_run-1_Logs'
task = '2afc'
attn = 'l'

df, summary = analyse2afc(f)

print(f'ATTENTION TASK IS: {df.attn_size.iloc[0]}')

# Plot performance for large and small tasks (check if participant is doing expected task)
fig, axs = plt.subplots(1,2, figsize=(12,4))
fig.suptitle(f'ATTENTION SIZE: {attn}', fontsize=16)

axs[0].set_title('SmallAF Performance')
axs[0].set_ylim(0,1)
axs[0].set_ylabel('Response Left')
axs[0].set_xlabel('% Blue')
axs[0].scatter(summary[summary.attn_size == 's']['diff'],summary[summary.attn_size == 's'].resp_left)

axs[1].set_title('LargeAF Performance')
axs[1].set_ylim(0,1)
axs[1].set_ylabel('Response Left')
axs[1].set_xlabel('% Blue')
axs[1].scatter(summary[summary.attn_size == 'l']['diff'],summary[summary.attn_size == 'l'].resp_left)
fig.savefig(f'./logs/{f})')

# plot sigmoid and print 20% and 80% values

xdata = summary[summary.attn_size == attn]['diff']
ydata = summary[summary.attn_size == attn].resp_left

popt, pcov = curve_fit(sigmoid, xdata, ydata)

val = (abs(0.5-inv_sigmoid(.2,*popt))+abs(0.5-inv_sigmoid(.2,*popt)))/2

print(f'20%: {inv_sigmoid(.2,*popt):.2f} \
    \n80%: {inv_sigmoid(.8,*popt):.2f} \
    \nYes/No Values: {0.5+val:.3f} , {0.5-val:.3f}')

x = np.linspace(0, 1, 20)
y = sigmoid(x, *popt)

fig2, ax = plt.subplots(1,1, figsize=(8,6))


ax.plot(xdata, ydata, 'o', label='data')
ax.set_title(f'{attn.upper()} AF')
ax.plot(x,y, label='sigmoid')
ax.set_ylim(0, 1)
ax.set_ylabel('Response Left')
ax.set_xlabel('% Blue')
plt.legend(loc='best')
fig2.savefig(f'./logs/{f})')

plt.show()