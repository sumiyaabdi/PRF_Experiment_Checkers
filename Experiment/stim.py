#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:07:02 2019

@author: marcoaqil
"""
import numpy as np
from psychopy import visual
from psychopy import tools


class PRFStim(object):  
    def __init__(self, session, 
                        squares_in_bar=2 ,
                        bar_width_deg=1.25,
                        tex_nr_pix=1024,
                        flicker_frequency=6, 

                        **kwargs):
        self.session = session
        self.squares_in_bar = squares_in_bar
        self.bar_width_deg = bar_width_deg
        self.tex_nr_pix = tex_nr_pix
        self.flicker_frequency = flicker_frequency

        
        self.bar_width_in_pixels = tools.monitorunittools.deg2pix(bar_width_deg, self.session.monitor)*self.tex_nr_pix/self.session.win.size[1]
        print(self.bar_width_in_pixels)
        print(self.session.win.size)

        bar_width_in_radians = np.pi*self.squares_in_bar
        bar_pixels_per_radian = bar_width_in_radians/self.bar_width_in_pixels
        pixels_ls = np.linspace((-self.tex_nr_pix/2)*bar_pixels_per_radian,(self.tex_nr_pix/2)*bar_pixels_per_radian,self.tex_nr_pix)

        tex_x, tex_y = np.meshgrid(pixels_ls, pixels_ls)
        
        if squares_in_bar==1:
            self.sqr_tex = np.sign(np.sin(tex_x-np.pi/2) * np.sin(tex_y))
            self.sqr_tex_phase_1 = np.sign(np.sin(tex_x-np.pi/2) * np.sin(tex_y+np.sign(np.sin(tex_x-np.pi/2))*np.pi/4))
            self.sqr_tex_phase_2 = np.sign(np.sign(np.abs(tex_x-np.pi/2)) * np.sin(tex_y+np.pi/2))
        else:                
            self.sqr_tex = np.sign(np.sin(tex_x) * np.sin(tex_y))   
            self.sqr_tex_phase_1 = np.sign(np.sin(tex_x) * np.sin(tex_y+np.sign(np.sin(tex_x))*np.pi/4))
            self.sqr_tex_phase_2 = np.sign(np.sign(np.abs(tex_x)) * np.sin(tex_y+np.pi/2))
            
        
        bar_start_idx=int(np.round(self.tex_nr_pix/2-self.bar_width_in_pixels/2))
        bar_end_idx=int(bar_start_idx+self.bar_width_in_pixels)+1

        self.sqr_tex[:,:bar_start_idx] = 0       
        self.sqr_tex[:,bar_end_idx:] = 0

        self.sqr_tex_phase_1[:,:bar_start_idx] = 0                   
        self.sqr_tex_phase_1[:,bar_end_idx:] = 0

        self.sqr_tex_phase_2[:,:bar_start_idx] = 0                
        self.sqr_tex_phase_2[:,bar_end_idx:] = 0
        
        

        self.checkerboard_1 = visual.GratingStim(self.session.win, tex=self.sqr_tex,
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])
        self.checkerboard_2 = visual.GratingStim(self.session.win, tex=self.sqr_tex_phase_1,                                               
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])
        self.checkerboard_3 = visual.GratingStim(self.session.win, tex=self.sqr_tex_phase_2,                                                
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])
        
        
        
        #for reasons of symmetry, some textures (4 and 8) are generated differently between one square and multiple squares cases
        if self.squares_in_bar!=1:     
            
            self.checkerboard_4 = visual.GratingStim(self.session.win, tex=np.fliplr(self.sqr_tex_phase_1),
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])
            self.checkerboard_8 = visual.GratingStim(self.session.win, tex=-np.fliplr(self.sqr_tex_phase_1),
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])
            
 
            
        else:         
            self.checkerboard_4 = visual.GratingStim(self.session.win, tex=np.flipud(self.sqr_tex_phase_1),
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])
            
            self.checkerboard_8 = visual.GratingStim(self.session.win, tex=-np.flipud(self.sqr_tex_phase_1),
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])
        
        #all other textures are the same
        self.checkerboard_5 = visual.GratingStim(self.session.win, tex=-self.sqr_tex,
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])
            
        self.checkerboard_6 = visual.GratingStim(self.session.win, tex=-self.sqr_tex_phase_1,
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])
            
        self.checkerboard_7 = visual.GratingStim(self.session.win, tex=-self.sqr_tex_phase_2,
                                                 units='pix',
                                                 size=[self.session.win.size[1],self.session.win.size[1]])

            


            



        
        
        

    def draw(self, time, pos_in_ori, orientation,  bar_direction):


        x_pos, y_pos = np.cos((2.0*np.pi)*-orientation/360.0)*pos_in_ori, np.sin((2.0*np.pi)*-orientation/360.0)*pos_in_ori
        
        sin = np.sin(2*np.pi*time*self.flicker_frequency)
        cos = np.cos(2*np.pi*time*self.flicker_frequency)


        if bar_direction==0:
            if sin > 0 and cos > 0 and cos > sin:
                self.checkerboard_1.setPos([x_pos, y_pos])
                self.checkerboard_1.setOri(orientation)
                self.checkerboard_1.draw()
            elif sin > 0 and cos > 0 and cos < sin:
                self.checkerboard_2.setPos([x_pos, y_pos])
                self.checkerboard_2.setOri(orientation)
                self.checkerboard_2.draw()
            elif sin > 0 and cos < 0 and np.abs(cos) < sin:
                self.checkerboard_3.setPos([x_pos, y_pos])
                self.checkerboard_3.setOri(orientation)
                self.checkerboard_3.draw()
            elif sin > 0 and cos < 0 and np.abs(cos) > sin:
                self.checkerboard_4.setPos([x_pos, y_pos])
                self.checkerboard_4.setOri(orientation)
                self.checkerboard_4.draw()
            elif sin < 0 and cos < 0 and cos < sin:
                self.checkerboard_5.setPos([x_pos, y_pos])
                self.checkerboard_5.setOri(orientation)
                self.checkerboard_5.draw()
            elif sin < 0 and cos < 0 and cos > sin:
                self.checkerboard_6.setPos([x_pos, y_pos])
                self.checkerboard_6.setOri(orientation)
                self.checkerboard_6.draw()
            elif sin < 0 and cos > 0 and cos < np.abs(sin):
                self.checkerboard_7.setPos([x_pos, y_pos])
                self.checkerboard_7.setOri(orientation)
                self.checkerboard_7.draw()
            else:
                self.checkerboard_8.setPos([x_pos, y_pos])
                self.checkerboard_8.setOri(orientation)
                self.checkerboard_8.draw()
        else:
            if sin > 0 and cos > 0 and cos > sin:
                self.checkerboard_8.setPos([x_pos, y_pos])
                self.checkerboard_8.setOri(orientation)
                self.checkerboard_8.draw()
            elif sin > 0 and cos > 0 and cos < sin:
                self.checkerboard_7.setPos([x_pos, y_pos])
                self.checkerboard_7.setOri(orientation)
                self.checkerboard_7.draw()
            elif sin > 0 and cos < 0 and np.abs(cos) < sin:
                self.checkerboard_6.setPos([x_pos, y_pos])
                self.checkerboard_6.setOri(orientation)
                self.checkerboard_6.draw()
            elif sin > 0 and cos < 0 and np.abs(cos) > sin:
                self.checkerboard_5.setPos([x_pos, y_pos])
                self.checkerboard_5.setOri(orientation)
                self.checkerboard_5.draw()
            elif sin < 0 and cos < 0 and cos < sin:
                self.checkerboard_4.setPos([x_pos, y_pos])
                self.checkerboard_4.setOri(orientation)
                self.checkerboard_4.draw()
            elif sin < 0 and cos < 0 and cos > sin:
                self.checkerboard_3.setPos([x_pos, y_pos])
                self.checkerboard_3.setOri(orientation)
                self.checkerboard_3.draw()
            elif sin < 0 and cos > 0 and cos < np.abs(sin):
                self.checkerboard_2.setPos([x_pos, y_pos])
                self.checkerboard_2.setOri(orientation)
                self.checkerboard_2.draw()
            else:
                self.checkerboard_1.setPos([x_pos, y_pos])
                self.checkerboard_1.setOri(orientation)
                self.checkerboard_1.draw()            
            




