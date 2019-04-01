#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:04:44 2019

@author: marcoaqil
"""
import sys
from session import PRFSession


def main():
    output_str = sys.argv[1]
    settings_file = sys.argv[2]


    ts = PRFSession(output_str=output_str, settings_file=settings_file)
    ts.run()

if __name__ == '__main__':
    main()