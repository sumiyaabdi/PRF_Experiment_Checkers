#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:05:10 2019

@author: marcoaqil
"""

import numpy as np
from psychopy import visual
from psychopy.visual import filters
from psychopy import tools

from exptools2.core.session import Session
from trial import PRFTrial
from stim import PRFStim



class PRFSession(Session):

    
    def __init__(self, output_str, settings_file):
        
        
        super().__init__(output_str=output_str, settings_file=settings_file)      
            
        
        self.create_stimuli()

        self.create_trials()




    def create_stimuli(self):
        
        
        mask = filters.makeMask(matrixSize=self.win.size[0], 
                                shape='raisedCosine', 
                                radius=np.array([self.win.size[1]/self.win.size[0], 1.0]),#4*self.deg2pix(self.settings['prf_max_eccentricity'])* #self.deg2pix(self.settings['prf_max_eccentricity']),#0.5,#self.settings['pixstim_bg_aperture_fraction']*(self.screen_pix_size[1]/self.screen_pix_size[0]),
                                center=(0.0, 0.0), 
                                range=[-1, 1], 
                                fringeWidth=0.02#self.settings['aperture_stim_sd']*(self.screen_pix_size[1]/self.screen_pix_size[0])
                                )

        self.prf_stim = PRFStim(session=self, 
                        squares_in_bar=self.settings['PRF stimulus settings']['Squares in bar'], 
                        bar_width_deg=self.settings['PRF stimulus settings']['Bar width in degrees'],
                        flicker_frequency=self.settings['PRF stimulus settings']['Checkers motion speed'])#self.deg2pix(self.settings['prf_max_eccentricity']))    
        


        self.instruction_string = """Please fixate in the center of the screen. Your task is to respond whenever the dot changes color."""
        




        self.mask_stim = visual.GratingStim(self.win, 
                                        mask=-mask, 
                                        tex=None, 
                                        units='pix',
                                        size=[self.win.size[0]/2,self.win.size[1]/2], 
                                        pos = np.array((0.0,0.0)), 
                                        color = [0,0,0]) 
        



        # fixation circle border
        print(self.win.size)
        fixation_radius_pixels=tools.monitorunittools.deg2pix(self.settings['PRF stimulus settings']['Size fixation dot in degrees'], self.monitor)/2
        print(fixation_radius_pixels)
        self.fixation_circle = visual.Circle(self.win, 
            radius=fixation_radius_pixels, 
            units='pix', lineColor='black')
        
        
        #two colors of the fixation circle for the task
        self.fixation_disk_0 = visual.Circle(self.win, 
            units='pix', radius=fixation_radius_pixels, 
            fillColor=[1,-1,-1])
        
        self.fixation_disk_1 = visual.Circle(self.win, 
            units='pix', radius=fixation_radius_pixels, 
            fillColor=[-1,1,-1])




    def create_trials(self):
        """creates trials by setting up prf stimulus sequence"""
        self.trial_list=[]
        #create as many trials as TRs, + one for initial instructions
        self.trial_number=self.settings['PRF stimulus settings']['Bar pass duration in TRs']*len(self.settings['PRF stimulus settings']['Bar orientations'])
        
        self.bar_orientation_at_TR = np.concatenate((-np.ones(1), np.repeat(self.settings['PRF stimulus settings']['Bar orientations'], self.settings['PRF stimulus settings']['Bar pass duration in TRs'])))
        self.bar_pos_in_ori = np.concatenate((np.zeros(1), self.win.size[1]*np.tile(np.linspace(-0.5,0.5,self.settings['PRF stimulus settings']['Bar pass duration in TRs']), len(self.settings['PRF stimulus settings']['Bar orientations']))))
        self.bar_direction_at_TR = np.round(np.random.rand(self.trial_number))
        
        
        for i in range(self.trial_number):
                
            self.trial_list.append(PRFTrial(session=self,
                                            trial_nr=i,
                                               
                           bar_orientation=self.bar_orientation_at_TR[i],
                           bar_position_in_ori=self.bar_pos_in_ori[i],
                           bar_direction=self.bar_direction_at_TR[i]
                           #,tracker=self.tracker
                           ))

        ##################################################################################
        ## timings etc for the bar passes
        ##################################################################################


 

        #the dot will changes colour approximately once every two TRs       
        self.total_time = self.settings['PRF stimulus settings']['Bar pass duration in TRs']*self.settings['mri']['TR']*len(self.settings['PRF stimulus settings']['Bar orientations'])
        self.dot_switch_color_times = np.sort(self.total_time*np.random.rand(int(self.trial_number/2))) 
        self.current_dot_time=0
        self.next_dot_time=1

 


    def draw_stimulus(self):
        present_time = self.clock.getTime() - self.current_trial_start_time
        prf_time = present_time / (self.settings['mri']['TR'])
  
    
    # print(present_time, present_bar_pass, prf_time)
        if self.current_trial.bar_orientation != -1:
            self.prf_stim.draw(time=prf_time, 
                               pos_in_ori=self.current_trial.bar_position_in_ori, 
                               orientation=self.current_trial.bar_orientation,
                               bar_direction=self.current_trial.bar_direction)
            
            

        if self.next_dot_time<len(self.dot_switch_color_times):
            if present_time<self.dot_switch_color_times[self.current_dot_time]:                
                self.fixation_disk_1.draw()
            else:
                if present_time<self.dot_switch_color_times[self.next_dot_time]:
                    self.fixation_disk_0.draw()
                else:
                    self.current_dot_time+=2
                    self.next_dot_time+=2
                    
        self.fixation_circle.draw()



    def run(self):
        """run the session"""
        # cycle through trials
        self.display_text('Waiting for scanner', keys=self.settings['mri'].get('sync', 't'))

        self.start_experiment()
        
        for trial_idx in range(len(self.trial_list)):
            self.current_trial = self.trial_list[trial_idx]
            self.current_trial_start_time = self.clock.getTime()
            self.current_trial.run()
            
            


        self.close()

        

