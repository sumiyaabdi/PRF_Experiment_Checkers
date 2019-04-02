#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:06:36 2019

@author: marcoaqil
"""

from exptools2.core.trial import Trial

class PRFTrial(Trial):

    def __init__(self, session, trial_nr, bar_orientation, bar_position_in_ori, bar_direction, *args, **kwargs):
        
        #trial number and bar parameters   
        self.ID = trial_nr
        self.bar_orientation = bar_orientation
        self.bar_position_in_ori = bar_position_in_ori
        self.bar_direction = bar_direction
        self.session=session

        #here we decide how to go from each trial (bar position) to the next.    
        if self.session.settings['mri']['scanning']==True or self.session.settings['mri']['simulate']==True:
            #dummy value: if scanning or simulating a scanner, everything is synced to the output 't' of the scanner
            phase_durations = [1000]
        else:
            #if not synced to a real or simulated scanner, take the TR setting as phase/trial duration
            phase_durations = [self.session.settings['mri']['TR']]

        super().__init__(session, trial_nr,
            phase_durations,
            *args,
            **kwargs)


    def draw(self, *args, **kwargs):
        # draw bar stimulus and circular (raised cosine) aperture from Session class
        self.session.draw_stimulus() 
        self.session.mask_stim.draw()
        
        
        
        
    