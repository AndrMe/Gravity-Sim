'''Can be used is sim data shold be stored as a class'''
from phys_func import distance
class Planet():
    def __init__(self,x,y,v_x,v_y,radius,mass):
        '''Create a planet for simulation'''
        self.x=x
        self.y=y
        self.radius=radius
        self.velocity_x=v_x
        self.velocity_y=v_y
        self.mass=mass
        self.force_x=0
        self.force_y=0
class Simulation():
    def __init__(self,planets=[],trace=None,g=1,delta_time=1):
        '''Get all necessary for sim data'''
        self.planets=planets
        self.trace=trace
        self.gravity=g
        self.delta_time=delta_time
    def update_forces(self):
        '''calculate forces'''
        for i in range(len(self.planets)):
            for j in range(i,len(self.planets)):
                self.calculate_forces(self.planets[i],self.planets[j])
    def calculate_forces(self,p1:Planet,p2:Planet):
        '''calculates forces beetween two objects(Planets)'''
        r=distance(p1.x,p1.y,p2.x,p2.y)
        force=self.gravity*p1.mass*p2.mass/(r**2)
