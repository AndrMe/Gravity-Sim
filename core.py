'''core file makes the programm work'''
import pygame
import simulation


def init():
    ''' load all the configs,init all the objects'''
    #pseudo: load_data() -> planets, delta_time, trace,v_dict, (init_dict)
    # StartPygame() like surface=pygame.surface.Surface((height,width))
    pygame.init()
    delta_time=1
    planets=[]
    trace=[]
    scale=1
    g=1
    scr_height=1000
    scr_width=1200
    sim_core=simulation.Simulation(planets,trace,g,delta_time)
    surface=pygame.surface.Surface((scr_height,scr_width))
    return surface,sim_core

def run_program(renderer,sim_core):
    '''Run the loop'''
    running=True
    stopped=False
    while running:
        if not stopped:
            sim_core.sim_cycle()
        renderer.new_frame()
        
def end_program():
    '''all that should be done when shutting down the program'''
    pass

if __name__=='__main__':
    '''All works from here'''
    renderer,sim_core=init()
    run_program(renderer,sim_core)
    end_program()
