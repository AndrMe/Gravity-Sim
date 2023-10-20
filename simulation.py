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
        self.trace=[[self.x,self.y]]
        self.trace_appends=[[self.x,self.y]]
    def move(self,delta_t):
        '''Move it based on time and self force'''
        ax=self.force_x/self.mass
        ay=self.force_y/self.mass
        self.x+=self.velocity_x*delta_t+ax*delta_t**2
        self.y+=self.velocity_y*delta_t+ay*delta_t**2
        self.force_x=0
        self.force_y=0
    def update_trace(self):
        '''How we update traces'''
        self.trace.append([self.x,self.y])
        self.trace_appends.append([self.x,self.y])
    def get_traces(self):
        '''Needed to get all appends from last call'''
        s=self.trace_appends
        self.trace_appends=[[self.x,self.y]]
        return s

class Simulation():
    def __init__(self,planets=[],g=1,delta_time=1):
        '''Get all necessary for sim data'''
        self.planets=planets
        self.gravity=g
        self.delta_time=delta_time
    def update_state(self,configs):
        '''Apply current configs'''
        self.gravity=configs['g']
        self.delta_time=configs['delta_time']
        
    def update_forces(self):
        '''calculate forces'''
        for i in range(len(self.planets)):
            for j in range(i+1,len(self.planets)):
                self.calculate_forces(self.planets[i],self.planets[j])
    
    def calculate_forces(self,p1:Planet,p2:Planet):
        '''calculates forces beetween two objects(Planets)'''
        r=distance(p1.x,p1.y,p2.x,p2.y)
        force=self.gravity*p1.mass*p2.mass/(r**2)
        dx=p2.x-p1.x
        dy=p2.y-p1.y
        force_x=dx/r*force
        force_y=dy/r*force
        p1.force_x+=force_x
        p2.force_x+=-force_x
        p1.force_y+=force_y
        p2.force_y+=-force_y
    
    def step(self,delta_t):
        '''updates objects positions based on delta_time'''
        for p1 in self.planets:
            ax=p1.force_x/p1.mass
            ay=p1.force_y/p1.mass
            p1.x+=p1.velocity_x*delta_t+ax*delta_t**2
            p1.y+=p1.velocity_y*delta_t+ay*delta_t**2
            p1.force_x=0
            p1.force_y=0
    
    def sim_cycle(self):
        '''defines how force compution and steps will be combined'''
        time_keys=[0.2,0.4,0.3,0.1] #sum=1.0
        for time_key in time_keys:
            self.update_forces()
            self.step(self.delta_time*time_key)
    def get_trace_updates(self):
        '''returns apdates in traces happened from last request, list of lines(2cords)'''
        new_lines=[]
        for planet in self.planets:
            new_lines.append(planet.get_traces())
        return new_lines
        
