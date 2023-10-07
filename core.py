'''core file makes the programm work'''
import pygame
import simulation
import renderer


def init():
    ''' load all the configs,init all the objects'''
    #load_data() -> planets, delta_time, trace,v_dict, (init_dict)
    # StartPygame() like surface=pygame.surface.Surface((height,width))
    pygame.init()
    delta_time=1
    planets=[]
    trace=[]
    scale=1
    g=1
    scr_height=1000
    scr_width=1200
    sim_core=simulation.Simulation(planets,g,delta_time)
    screen = pygame.display.set_mode((scr_width, scr_height),pygame.RESIZABLE)
    render=renderer.Renderer(screen,scr_height,scr_width,scale,trace) #trace is renderer's
    return render,sim_core

def run_program(render=renderer.Renderer,sim_core=simulation.Simulation):
    '''Run the loop'''
    running=True
    stopped=False
    while running:
        if not stopped:
            sim_core.sim_cycle()
            render.transit_trace(sim_core.get_trace_updates())
            render.new_frame()
        running=False #debug
        
def end_program():
    '''all that should be done when shutting down the program'''
    print('ending')

if __name__=='__main__':
    '''All works from here'''
    render,sim_core=init()
    run_program(render,sim_core)
    end_program()
