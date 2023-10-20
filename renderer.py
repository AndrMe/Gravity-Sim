'''makes frames to display'''
import pygame
import interface
class Renderer():
    def __init__(self,screen,height,width,scale,trace):
        self.screen=screen
        self.height=height
        self.width=width
        self.scale_pow=scale
        self.trace=trace
        self.scale=1.1**self.scale_pow
        self.screen_posdata=[[0,0],[width,height]]
    def transit_trace(self,trace):
        '''get list of tace cords -> list of separate lines'''
        pass
    def new_frame(self):
        '''Draws new frame'''
        pygame.display.flip()
        pass
    def draw_planets(self,simulation):
        '''draw planets to the display'''
    def draw_interface(self):
        '''draw interface'''
    def display_trace(self):
        '''disply pre-rendered surfaces onto the display'''
    def render_new_races(self,estimated_time):
        '''draws lines to buffer surfaces'''
