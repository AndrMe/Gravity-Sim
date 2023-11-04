'''core file makes the programm work'''
import pygame
import simulation
import renderer
import controls
from loader import*

def fist_start_confs():
    delta_time=1
    scale_power=1
    g=1
    scr_height=1000
    scr_width=1200
    configs={
        'running':True,'stopped':True,'scale_power':scale_power,'scr_height':scr_height,'scr_width':scr_width,
        'g':g,'delta_time':delta_time
        }
    return configs
    
def init():
    ''' load all the configs,init all the objects'''
    #load_data() -> planets, delta_time, trace,v_dict, (configs)
    # StartPygame() like surface=pygame.surface.Surface((height,width))
    pygame.init()
    configs,planets,trace=load_init_data('gravity_save.json')
    if configs==None:
        configs=fist_start_confs()
    scr_width=configs['scr_width']
    scr_height=configs['scr_height']
    sim_core=simulation.Simulation(planets,configs['g'],configs['delta_time'])
    screen = pygame.display.set_mode((scr_width,scr_height),pygame.RESIZABLE )
    render=renderer.Renderer(screen,scr_height,scr_width,configs['scale_power'],trace) #trace is renderer's
    # interf=interface.Interface() -> renderer
    return render,sim_core,configs

def update_state(sim_core:simulation.Simulation,render:renderer.Renderer,configs:set()):
    sim_core.update_state(configs)

def run_program(render:renderer.Renderer,sim_core:simulation.Simulation,configs:set()):
    '''Run the loop'''
    configs['running']=True
    configs['stopped']=True
    while configs['running']:
        configs=controls.update(pygame.event.get(),sim_core,render,configs)
        render.new_frame()
        if not configs['stopped']: 
            sim_core.sim_cycle()
            render.transit_trace(sim_core.get_trace_updates())     
        #configs['running']=False #debug
    end_program(configs,sim_core.planets,render.trace) 

def end_program(configs,planets,trace):
    '''all that should be done when shutting down the program'''

    save_data={'configs':configs,'planets':planets,'trace':trace}
    update_data_in_file(save_data,'gravity_save.json')
    print('ending')

if __name__=='__main__':
    '''All works from here'''
    render,sim_core,configs=init()
    run_program(render,sim_core,configs)
