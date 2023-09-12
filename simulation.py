'''Can be used is sim data shold be stored as a class'''
class planet():
    def __init__(self,x,y,v_x,v_y,radius):
        '''Create a planet for simulation'''
        self.x=x
        self.y=y
        self.radius=radius
        self.velocity_x=v_x
        self.velocity_y=v_y

class Simulation():
    def __init__(self,planets=[],trace=None,g=1,delta_time=1):
        '''Get all necessary for sim data'''
        self.planets=planets
        self.trace=trace
        self.gravity=g
        self.delta_time=delta_time
    def update_forces(self):
        '''calculate forces'''
        pass
