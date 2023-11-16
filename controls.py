'''Handles events and control user inputs'''
import pygame
class Controler():
    def __init__(self,sim,render,configs):
        self.sim=sim
        self.render=render
        self.configs=configs
        self.events=[]
        self.event=None

    def update(self):
        '''based on inputs controls settings,simulation,render'''
        #configs are like {'stopped':True} {'dscale':0}
        self.events=pygame.event.get()
        self.configs['scr_width'],self.configs['scr_height']=pygame.display.get_window_size()
        self.configs['mouse_move']=(0,0)
        for self.event in self.events: 
            if self.event.type==pygame.QUIT:
                self.configs['running']=False
            if self.event.type==pygame.MOUSEBUTTONDOWN:
                self.mouse_down()
            if self.event.type==pygame.MOUSEBUTTONUP:
                self.mouse_up()
            if self.event.type==pygame.MOUSEMOTION:
                self.move_mouse()
            if self.event.type==pygame.MOUSEWHEEL:
                self.wheel_move()

    def mouse_down(self):
        if self.event.button==pygame.BUTTON_LEFT:
            self.l_click()
        elif self.event.button==pygame.BUTTON_RIGHT:
            self.r_click()
        
    def l_click(self):
        x,y=self.event.pos
        pointing_map=True
        if pointing_map:
            self.configs['map_l_click']=True
            self.configs['last_cords']=(x,y)

    def r_click(self):
        pass

    def mouse_up(self):
        if self.event.button==pygame.BUTTON_LEFT:
            self.l_up()
        elif self.event.button==pygame.BUTTON_RIGHT:
            self.r_up()

    def l_up(self):
        self.configs['map_l_click']=False

    def r_up(self):
        pass

    def move_mouse(self):
        if self.configs['map_l_click']:
            new_x,new_y=self.event.pos
            dx=new_x-self.configs['last_cords'][0]
            dy=new_y-self.configs['last_cords'][1]
            self.configs['mouse_move']=(dx,dy)
            self.configs['last_cords']=(new_x,new_y)
        
    def wheel_move(self):
        self.configs['scale_power']+=self.event.y
