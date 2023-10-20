'''Handles events and control user inputs'''
import pygame
def update(events,sim,render,configs):
    '''based on inputs controls settings,simulation,render'''
    #configs be like {'stopped':True} {'dscale':0}
    configs['scr_width'],configs['scr_height']=pygame.display.get_window_size()
    for event in events: 
        if event.type==pygame.QUIT:
            configs['running']=False
        # if event.type==
    return configs