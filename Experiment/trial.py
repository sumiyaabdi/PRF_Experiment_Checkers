#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:06:36 2019

@author: marcoaqil
"""

from exptools2.core.trial import Trial
from psychopy import event


class PRFTrial(Trial):

    def __init__(self, session, trial_nr, bar_orientation, bar_position_in_ori, bar_direction, *args, **kwargs):
        
        #trial number and bar parameters   
        self.ID = trial_nr
        self.bar_orientation = bar_orientation
        self.bar_position_in_ori = bar_position_in_ori
        self.bar_direction = bar_direction
        self.session=session

        #here we decide how to go from each trial (bar position) to the next.    
        if self.session.settings['PRF stimulus settings']['Scanner sync']==True:
            #dummy value: if scanning or simulating a scanner, everything is synced to the output 't' of the scanner
            phase_durations = [1000]
        else:
            #if not synced to a real or simulated scanner, take the bar pass step as length
            phase_durations = [self.session.settings['PRF stimulus settings']['Bar step length']] 

        super().__init__(session, trial_nr,
            phase_durations,
            *args,
            **kwargs)


    def draw(self, *args, **kwargs):
        # draw bar stimulus and circular (raised cosine) aperture from Session class
        self.session.draw_stimulus() 
        self.session.mask_stim.draw()
        
        
        
    def get_events(self):
         """ Logs responses/triggers """
         events = event.getKeys(timeStamped=self.session.clock)
         if events:
             if 'q' in [ev[0] for ev in events]:  # specific key in settings?
                 self.session.win.saveMovieFrames('./logs/Screenshots/Screenshot.png')
                 self.session.close()
                 self.session.quit()
 
             for key, t in events:
 
                 if key == self.session.mri_trigger:
                     event_type = 'pulse'
                     #marco edit. the second bit is a hack to avoid double-counting of the first t when simulating a scanner
                     if self.session.settings['PRF stimulus settings']['Scanner sync']==True and t>0.1:                       
                         self.exit_phase=True
                         #ideally, for speed, would want  getMovieFrame to be called right after the first winflip. 
                         #but this would have to be dun from inside trial.run()
                         self.session.win.getMovieFrame()
                 else:
                     event_type = 'response'
 
                 idx = self.session.global_log.shape[0]
                 self.session.global_log.loc[idx, 'trial_nr'] = self.trial_nr
                 self.session.global_log.loc[idx, 'onset'] = t
                 self.session.global_log.loc[idx, 'event_type'] = event_type
                 self.session.global_log.loc[idx, 'phase'] = self.phase
                 self.session.global_log.loc[idx, 'response'] = key
 
                 for param, val in self.parameters.items():
                     self.session.global_log.loc[idx, param] = val
 
                 #self.trial_log['response_key'][self.phase].append(key)
                 #self.trial_log['response_onset'][self.phase].append(t)
                 #self.trial_log['response_time'][self.phase].append(t - self.start_trial)
 
                 if key != self.session.mri_trigger:
                     self.last_resp = key
                     self.last_resp_onset = t
        
    