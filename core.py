'''core file makes the programm work'''
import pygame
import simulation
import renderer
import controls
import time
from loader import*

def fist_start_confs():
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
    
def init():
    ''' load all the configs,init all the objects'''
    #load_data() -> planets, delta_time, trace,v_dict, (configs)
    # StartPygame() like surface=pygame.surface.Surface((height,width))
    pygame.init()
    rend_clock=pygame.time.Clock()
    configs,planets,trace=load_init_data('gravity_save.json')
    if configs==None:
        configs=fist_start_confs()
    scr_width=configs['scr_width']
    scr_height=configs['scr_height']
    planets=dict_to_pl(planets)
    #planets.append(simulation.Planet(100,100,2,5,3,1))   #Test
    sim_core=simulation.Simulation(planets,configs['g'],configs['delta_time'])
    screen = pygame.display.set_mode((scr_width,scr_height),pygame.RESIZABLE )
    render=renderer.Renderer(screen,scr_height,scr_width,configs['scale_power'],trace,rend_clock,configs['fps']) #trace is renderer's
    # interf=interface.Interface() -> renderer
    return render,sim_core,configs

def update_state(sim_core:simulation.Simulation,render:renderer.Renderer,configs:set()):
    sim_core.update_state(configs)
    render.update_state(configs)

def run_program(render:renderer.Renderer,sim_core:simulation.Simulation,configs:set()):
    '''Run the loop'''
    configs['running']=True
    configs['stopped']=False
    while configs['running']:
        t1=time.time()
        configs=controls.update(pygame.event.get(),sim_core,render,configs)
        update_state(sim_core,render,configs)
        if not configs['stopped']: 
            sim_core.sim_cycle()
            t2=time.time()
            used_time=(t2-t1)*1000
            render.transit_trace(sim_core.get_trace_updates())
        est_rend_time=1/configs['fps']*1000-used_time
        render.new_frame(sim_core.planets,est_rend_time)    
        #configs['running']=False #debug
    end_program(configs,sim_core.planets,render.trace) 

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

def end_program(configs,planets,trace):
    '''all that should be done when shutting down the program'''
    planets=pl_to_dicts(planets)
    save_data={'configs':configs,'planets':planets,'trace':trace}
    update_data_in_file(save_data,'gravity_save.json')
    print('ending')

if __name__=='__main__':
    '''All works from here'''
    render,sim_core,configs=init()
    run_program(render,sim_core,configs)
