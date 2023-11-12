'''Handles events and control user inputs'''
import pygame
def update(events,sim,render,configs):
    '''based on inputs controls settings,simulation,render'''
    #configs are like {'stopped':True} {'dscale':0}
    configs['scr_width'],configs['scr_height']=pygame.display.get_window_size()
    configs['mouse_move']=(0,0)
    for event in events: 
        if event.type==pygame.QUIT:
            configs['running']=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_down(event,configs)
        if event.type==pygame.MOUSEBUTTONUP:
            mouse_up(event,configs)
        if event.type==pygame.MOUSEMOTION:
            move_mouse(event,configs)
    return configs

def mouse_down(event:pygame.event.Event,configs):
    if event.button==pygame.BUTTON_LEFT:
        l_click(event,configs)
    elif event.button==pygame.BUTTON_RIGHT:
        r_click(event,configs)
    
def l_click(event,configs):
    x,y=event.pos
    pointing_map=True
    if pointing_map:
        configs['map_l_click']=True
        configs['last_cords']=(x,y)

def r_click(event,configs):
    pass

def mouse_up(event,configs):
    if event.button==pygame.BUTTON_LEFT:
        l_up(event,configs)
    elif event.button==pygame.BUTTON_RIGHT:
        r_up(event,configs)

def l_up(event,configs):
    configs['map_l_click']=False

def r_up(event,configs):
    pass
def move_mouse(event,configs):
    if configs['map_l_click']:
        new_x,new_y=event.pos
        dx=new_x-configs['last_cords'][0]
        dy=new_y-configs['last_cords'][1]
        configs['mouse_move']=(dx,dy)
        configs['last_cords']=(new_x,new_y)
