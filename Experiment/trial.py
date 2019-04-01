#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:06:36 2019

@author: marcoaqil
"""

from exptools2.core.trial import Trial

class PRFTrial(Trial):

    def __init__(self, session, trial_nr, bar_orientation, bar_position_in_ori, bar_direction, *args, **kwargs):
#
        self.ID = trial_nr
        self.bar_orientation = bar_orientation
        self.bar_position_in_ori = bar_position_in_ori
        self.bar_direction = bar_direction
        self.session=session

        

        phase_durations = [self.session.settings['mri']['TR']]#config['TR']]
#
        super().__init__(session, trial_nr,
            phase_durations,
            *args,
            **kwargs)
#



    def draw(self, *args, **kwargs):
        # draw stimuli:

        self.session.draw_stimulus() 

        self.session.mask_stim.draw()
        
    