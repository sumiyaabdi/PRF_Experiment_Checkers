#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:04:44 2019

@author: marcoaqil
"""
import sys
import os
from session import PRFSession


def main():
    subject = sys.argv[1]
    # 5 conditions: PRF2R, PRF1R, PRF1S, PRF4R, PRF4F 
    #(2 squares Regular speed, 1 square Regular, 1 square Slow, 4 square Regular, 4 square Fast)
    task = sys.argv[2]
    #in the full experiment we would do 3 runs
    run = sys.argv[3]
    
    
    output_str= subject+'_task-'+task+'_run-'+run
    
    output_dir = './'+output_str+'_Logs'
    
    if os.path.exists(output_dir):
        print("Warning: output directory already exists. Renaming to avoid overwriting.")
        output_dir = output_dir + '-redo'
    
    settings_file='./expsettings_'+task+'.yml'

    ts = PRFSession(output_str=output_str, output_dir=output_dir, settings_file=settings_file)
    ts.run()

if __name__ == '__main__':
    main()