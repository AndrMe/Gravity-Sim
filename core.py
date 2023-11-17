'''core file makes the programm work'''
import pygame
import simulation
import renderer
import controls
import time
from loader import*

class App():   
    def __init__(self):
        ''' load all the configs,init all the objects'''
        pygame.init()
        configs,planets,trace=load_init_data('gravity_save.json')
        if configs==None:
            configs=self.get_default_confs()
        self.configs=configs
        planets=dict_to_pl(planets)
        #planets.append(simulation.Planet(500,400,1,1,20,3))   #Test
        self.sim_core=simulation.Simulation(planets,self.configs['g'],self.configs['delta_time'])
        screen = pygame.display.set_mode((self.configs['scr_width'],self.configs['scr_height']),pygame.RESIZABLE )
        rend_clock=pygame.time.Clock()
        self.render=renderer.Renderer(
            screen,self.configs['scr_height'],self.configs['scr_width'],
            self.configs['scale_power'],trace,rend_clock,self.configs['fps']
            ) #trace is renderer's
        self.controler=controls.Controler(self.sim_core,self.render,self.configs)
        # interf=interface.Interface() -> renderer
        
    def get_default_confs(self):
        delta_time=1
        scale_power=1
        g=1
        scr_height=1000
        scr_width=1200
        configs={
            'running':True,'stopped':True,'scale_power':scale_power,'scr_height':scr_height,'scr_width':scr_width,
            'g':g,'delta_time':delta_time,'fps':60,'map_l_click':False,'last_cords':(0,0),'mouse_move':(0,0)
            }
        return configs
    
    def run_program(self):
        '''Run the loop'''
        self.configs['running']=True
        self.configs['stopped']=False
        while self.configs['running']:
            t1=time.time()
            self.controler.update()
            self.update_state()
            if not self.configs['stopped']: 
                self.sim_core.sim_cycle()
                t2=time.time()
                used_time=(t2-t1)*1000
                print(used_time) #test
                self.render.transit_trace(self.sim_core.get_trace_updates())
            est_rend_time=1/self.configs['fps']*1000-used_time
            self.render.new_frame(self.sim_core.planets,est_rend_time)    
            #configs['running']=False #debug
        self.end_program() 

    def update_state(self):
        self.sim_core.update_state(self.configs)
        self.render.update_state(self.configs)

    def end_program(self):
        '''all that should be done when shutting down the program'''
        planets=pl_to_dicts(self.sim_core.planets)
        save_data={'configs':self.configs,'planets':planets,'trace':self.render.trace}
        #update_data_in_file(save_data,'gravity_save.json')
        print('ending')
        
def pl_to_dicts(planets):
    '''Transits list of planets to list of dicts'''
    pl_dicts=[]
    for planet in planets:
        pl_dicts.append(planet.__dict__)
    return pl_dicts

def dict_to_pl(planets):
    pl_list=[]
    for planet in planets:
        pl_list.append(simulation.Planet(planet['x'],planet['y'],planet['velocity_x'],planet['velocity_y'],planet['radius'],planet['mass']))
    return pl_list

if __name__=='__main__':
    '''All works from here'''
    sim_app=App()
    sim_app.run_program()
