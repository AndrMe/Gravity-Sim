'''makes frames to display'''
import pygame
import interface
class Renderer():
    def __init__(self,screen,height,width,scale,trace,clock,fps):
        self.screen=screen
        self.height=height
        self.width=width
        self.scale_pow=scale
        self.trace=trace
        self.scale=1.1**self.scale_pow
        self.screen_posdata=[[0,0],[width,height]]
        self.clock=clock
        self.fps=fps

    def new_frame(self,planets,est_time):
        '''Draws new frame'''
        self.screen.fill((0,0,0))

        self.draw_planets(planets)
        self.display_trace()
        self.draw_fps()
        pygame.display.flip()
        self.clock.tick(self.fps)
    
    def update_state(self,configs):
        '''Apply current configs state'''
        x,y=self.screen_posdata[0]
        dx,dy=configs['mouse_move']
        self.screen_posdata=[[x-dx/self.scale,y-dy/self.scale],[configs['scr_width'],configs['scr_height']]]
        self.scale_pow=configs['scale_power']
        self.scale=1.1**self.scale_pow

    def pl_inscr(self,cords,rad):
        '''Return true if planet with cords and adius is in screen'''
        if (cords[0]-rad)<=self.width and (cords[0]+rad)>=0 and (cords[1]-rad)<=self.height and (cords[1]+rad)>=0:
            return True
        return False

    def draw_planets(self,planets):
        '''draw planets to the display'''
        for planet in planets:
            cords=((planet.x-self.screen_posdata[0][0])*self.scale,(planet.y-self.screen_posdata[0][1])*self.scale)
            if self.pl_inscr(cords,planet.radius):
                pygame.draw.circle(self.screen,(0,0,255),cords,planet.radius*self.scale)

    def draw_interface(self):
        '''draw interface'''
    def draw_fps(self):
        'displays fps'
        font=pygame.font.SysFont('Times New Roman',30)
        text_surface = font.render('FPS:'+str(round(self.clock.get_fps())), False,(255,255,255))
        self.screen.blit(text_surface, (10,10))

    def transit_trace(self,trace):
        '''get list of tace cords -> list of separate lines'''
        pass

    def display_trace(self):
        '''disply pre-rendered surfaces onto the display'''
        pass
    def render_new_traces(self,estimated_time):
        '''draws lines to buffer surfaces'''
        pass
