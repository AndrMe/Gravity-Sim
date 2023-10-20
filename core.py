'''core file makes the programm work'''
import pygame
import simulation
import renderer
import controls
def init():
    ''' load all the configs,init all the objects'''
    #load_data() -> planets, delta_time, trace,v_dict, (configs)
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
    configs={
        'running':True,'stopped':True,'scale_power':1,'scr_height':scr_height,'scr_width':scr_width,
        'g':g,'delta_time':delta_time
        }
    # interf=interface.Interface() -> renderer
    return render,sim_core,configs
def update_state(sim_core=simulation.Simulation,render=renderer.Renderer,configs=set()):
    sim_core.update_state(configs)
def run_program(render=renderer.Renderer,sim_core=simulation.Simulation,configs={}):
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
        
def end_program():
    '''all that should be done when shutting down the program'''
    print('ending')

if __name__=='__main__':
    '''All works from here'''
    render,sim_core,configs=init()
    run_program(render,sim_core,configs)
    end_program()
