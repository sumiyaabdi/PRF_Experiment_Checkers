#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:04:44 2019

@author: marcoaqil
"""
import sys
import os
from session import PRFSession, PsychophysSession
from analyse import *
from datetime import datetime
datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main():
    subject = sys.argv[1]
    sess =  sys.argv[2]
    # 5 conditions: PRF2R, PRF1R, PRF1S, PRF4R, PRF4F 
    #(2 squares Regular speed, 1 square Regular, 1 square Slow, 4 square Regular, 4 square Fast)
    # task = sys.argv[3]
    #in the full experiment we would do 3 runs
    run = sys.argv[3]

    task = ''
    while task not in ('2afc', 'yesno'):
        task = input("Which attention task ['2afc' / 'yesno']?: ")

    attn = ''
    while attn not in ('s','l'):
        attn = input('Which attention size [small (s) / large (l)]?: ')

    eyetrack = ''
    while eyetrack not in ('y','yes','n','no'):
        eyetrack = input('Eyetracking (y/n)?: ')
    
    output_str= subject+'_ses-'+sess+'_task-'+task+attn.upper()+'_run-'+run
    print(f'Output folder: {output_str}')
    
    output_dir = './logs/'+output_str+'_Logs'
    
    if os.path.exists(output_dir):
        print("Warning: output directory already exists. Renaming to avoid overwriting.")
        output_dir = output_dir + datetime.now().strftime('%Y%m%d%H%M%S')
    
    settings_file='expsettings/expsettings_'+task+'.yml'

    if task == 'yesno':
        if (eyetrack == 'n') or (eyetrack == 'n'):
            ts = PRFSession(output_str=output_str,
                            output_dir=output_dir,
                            settings_file=settings_file,
                            eyetracker_on=False)
        else:
            ts = PRFSession(output_str=output_str,
                            output_dir=output_dir,
                            settings_file=settings_file)
        ts.create_stimuli()
        ts.create_trials()
        ts.run()

    elif task == '2afc':
        if (eyetrack == 'n') or (eyetrack == 'n'):
            ts = PsychophysSession(output_str=output_str,
                                   output_dir=output_dir,
                                   settings_file=settings_file,
                                   eyetracker_on=False)
        else:
            ts = PsychophysSession(output_str=output_str,
                                   output_dir=output_dir,
                                   settings_file=settings_file)
        ts.create_stimuli()
        ts.create_trials()
        ts.run()
    
    return output_str, task, attn


if __name__ == '__main__':
    output_str, task, attn = main()

    if task == '2afc':
        df, summary = analyse2afc(output_str)

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

        plt.show()

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

        plt.plot(xdata, ydata, 'o', label='data')
        plt.title(f'{attn.upper()} AF')
        plt.plot(x,y, label='sigmoid')
        plt.ylim(0, 1)
        plt.ylabel('Response Left')
        plt.xlabel('% Blue')
        plt.legend(loc='best')
        plt.show()