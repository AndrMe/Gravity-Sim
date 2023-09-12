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
    surface=pygame.surface.Surface((scr_height,scr_width))

    return surface,delta_time,planets,trace,scale,g
def run_program():
    '''Run the loop'''
    pass
def end_program():
    '''all that should be done when shutting down the program'''
    pass

if __name__=='__main__':
    '''All works from here'''
    process_data=init()
    run_program(process_data)
    end_program()