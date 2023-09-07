import pygame
import math
WIDTH = 1200  # ширина игрового окна
HEIGHT = 1000 # высота игрового окна
FPS = 120 # частота кадров в секунду
BLACK = (0, 0, 0)
RED=(255,0,0)
WHITE=(255,255,255)
BLUE=(120,219,226)
GREY=(100,100,100)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
d_click_cl=pygame.time.Clock()
entr_cl=pygame.time.Clock()
Running=True
time=800
planets=[]
map_l_click=False
shift_x=0
shift_y=0
scale=0.00001
stopped=True
static_texts=[]
bars=[]
text_inputs=[]
buttons=[]
inworld_buttons=[]
add_list=[]
add_list2=[]
adding_planet=False
keys=list(range(pygame.K_0,pygame.K_9))+list(range(pygame.K_a,pygame.K_z))+[pygame.K_COMMA,pygame.K_PERIOD]+[pygame.K_MINUS]
g=6.67430*10**(-11)

v_dict={'time':time,'g':g,'scale':scale,
        'add_mass':0,'add_radius':0,'add_x':0,'add_y':0,
        'add_vel_x':0,'add_vel_y':0}
class Drawable_text():
    def init_text(self,lines,enabled):
        self.lines=lines
        self.font=pygame.font.SysFont('Times New Roman',18)
        self.length=0
        self.height=0
        self.enabled=enabled
        for line in lines:
            line_length,line_height=self.font.size(line)
            self.height+=line_height
            self.length=max(self.length,line_length)
    def update_text(self,lines,enabled):
        if lines!=[]:
            self.lines=lines
        for line in lines:
            line_length,line_height=self.font.size(line)
            self.height+=line_height
            self.length=max(self.length,line_length)
        self.enabled=enabled
    def draw_text(self,x,y):
        if self.enabled:
            dy=0
            for line in self.lines:
                surf=self.font.render(line,True,WHITE)
                screen.blit(surf,(x,y+dy))
                dy+=surf.get_height()
    
class Static_text(Drawable_text):
    def __init__(self,x,y,lines=['*'],enabled=True):
        self.init_text(lines,enabled)
        self.x=x
        self.y=y
        static_texts.append(self)
    def update(self,lines=[],enabled=True):
        self.update_text(lines,enabled)
    def draw(self):
        self.draw_text(self.x,self.y)
    def delete(self):
        static_texts.remove(self)
class Basic_button():
    def init_but(self,method):
        self.clicked=False
        self.method=method
    def update_but(self):
        if self.method and self.clicked:
            self.method()
            self.clicked=False
class Button(Drawable_text,Basic_button):
    def __init__(self,x,y,lines=['*'],enabled=True,method=None) :
        self.init_text(lines,enabled)
        self.x=x
        self.y=y
        self.init_but(method)
        buttons.append(self)
    def update(self,lines=[],enabled=True):
        self.update_text(lines,enabled)
        self.update_but()
    def draw(self):
        if self.enabled:
            pygame.draw.rect(screen,GREY,(self.x,self.y,self.length,self.height))
            self.draw_text(self.x,self.y)
    def delete(self):
        buttons.remove(self)
class Inworld_button(Drawable_text,Basic_button):
    def __init__(self, x, y, lines=['*'], enabled=True, method=None):
        self.x=x
        self.y=y
        self.init_text(lines,enabled)
        self.init_but(method)
        inworld_buttons.append(self)
        self.screen_x=self.x*scale+shift_x
        self.screen_y=self.y*scale+shift_y
    def update(self,lines=[],enabled=True):
        self.update_text(lines,enabled)
        self.update_but()
    def draw(self):
        self.screen_x=self.x*scale+shift_x
        self.screen_y=self.y*scale+shift_y
        pygame.draw.rect(screen,GREY,(self.screen_x,self.screen_y,self.length,self.height))
        self.draw_text(self.screen_x,self.screen_y)
    def delete(self):
        inworld_buttons.remove(self)
class Scalebar():
    def __init__(self,x,y,length,scale_width,handle_width,handle_length,scale_color,handle_color,screen,min,max,base,variable=None):
        global bars
        self.x=x
        self.y=y
        self.length=length
        self.scale_width=scale_width
        self.handle_width=handle_width
        self.handle_length=handle_length
        self.scale_color=scale_color
        self.handle_color=handle_color
        self.screen=screen
        self.min=min
        self.max=max
        self.z=base
        self.handle_x=self.x+(self.z-self.min)/(self.max-self.min)*self.length
        bars.append(self)
        self.variable=variable
        self.active=False
    def update(self):
        global v_dict
        if self.variable:
            if self.active:    
                v_dict[self.variable]=self.z
            else:
                self.z=v_dict[self.variable]
            if self.z<self.min:
                self.z=self.min
            elif self.z>self.max:
                self.z=self.max
            self.handle_x=self.x+self.length*((self.z-self.min)/(self.max-self.min))
    def draw(self):
        pygame.draw.line(self.screen,self.scale_color,(self.x,self.y+self.handle_length/2),(self.x+self.length,self.y+self.handle_length/2),self.scale_width)
        pygame.draw.line(self.screen,self.handle_color,(self.handle_x,self.y),(self.handle_x,self.y+self.handle_length),self.handle_width)

class Text_input():
    def __init__(self,x,y,screen,text='',variable=None,z=None,border_color=WHITE,border_width=1,
                 text_font='Times New Roman',font_size=18,text_color=WHITE,var_type='Number',active_color=BLUE):
        text_inputs.append(self)
        self.x=x
        self.y=y
        self.text=text
        self.variable=variable
        self.border_color=border_color
        self.border_width=border_width
        self.screen=screen
        self.text_color=text_color
        self.font=pygame.font.SysFont(text_font,font_size)
        self.surf=self.font.render(self.text,True,text_color)
        self.length=self.surf.get_width()
        self.height=self.surf.get_height()
        self.var_type=var_type
        self.editing=False
        self.active_color=active_color
        self.entry_marker=False
        self.entry_time=0
        self.error=False
        self.end=False
        if self.variable and z:
            v_dict[self.variable]=z
            self.z=z
        if self.variable and not z:
            self.z=v_dict[self.variable]
    def update(self):
        self.error=False 
        
        if self.variable and not self.editing: 
            if not self.end:
                self.text=str(round(v_dict[self.variable],8))
            if self.var_type=='Number':
               
                try:
                    self.z=float(self.text)
                except ValueError:
                    self.error=True
            else:
                self.z=self.text
            
            v_dict[self.variable]=self.z
        self.end=False
    def draw(self):
        self.surf=self.font.render(self.text,True,self.text_color)
        self.length=self.surf.get_width()
        self.height=self.surf.get_height()
        if self.editing:
            draw_color=self.active_color
        elif self.error:
            draw_color=(255,0,0)
        else:
            draw_color=self.border_color
        p1=(self.x-self.border_width,self.y-self.border_width)
        p2=(self.x+self.length+self.border_width+2,self.y-self.border_width)
        p3=(self.x+self.length+self.border_width+2,self.y+self.height+self.border_width)
        p4=(self.x-self.border_width,self.y+self.height+self.border_width)
        pygame.draw.lines(self.screen,draw_color,True,[p1,p2,p3,p4],
                                                              self.border_width)
        if self.editing:
            t=entr_cl.tick()
            self.entry_time+=t
            if self.entry_time>1000:
                self.entry_marker=not self.entry_marker
                self.entry_time=0
            if self.entry_marker:
                p1=(self.x+self.length,self.y-1)
                p2=(self.x+self.length,self.y+self.height-1)
                pygame.draw.line(self.screen,WHITE,p1,p2,2)   
            


        screen.blit(self.surf,(self.x,self.y))
    def delete(self):
        text_inputs.remove(self)
class Trace():
    def __init__(self,x,y,screen):
        self.list=[(x,y),(x,y)]
        self.screen=screen
        self.path=0
        self.last_cords=(x,y)
    def update(self,x,y):
        move_x=x-self.last_cords[0]
        move_y=y-self.last_cords[1]
        self.path+=math.sqrt(move_x**2+move_y**2)
        self.last_cords=(x,y)
        if self.path>1500000:
            self.list.append((x,y))
            self.path=0
        if len(self.list)>1000:
            self.list.pop(0)
    def draw(self):
        global shift_x,shift_y
        for i in range(1,len(self.list)):
            screen_last=((self.list[i-1][0])*scale+shift_x,(self.list[i-1][1])*scale+shift_y)
            scereen_new=((self.list[i][0])*scale+shift_x,(self.list[i][1])*scale+shift_y)
            if abs(screen_last[0]-WIDTH/2)<=WIDTH/2+5*scale and abs(screen_last[1]-HEIGHT/2)<=HEIGHT/2+5*scale:
                pygame.draw.line(self.screen,BLUE,screen_last,scereen_new,3)
class Planet():
    def __init__(self,mass,radius,x,y,vel_x,vel_y):
        global screen,planets
        self.mass=mass
        self.x=x
        self.y=y
        self.vel_x=vel_x
        self.vel_y=vel_y
        self.radius=radius
        self.screen_radius=radius*scale
        self.ax=0
        self.ay=0
        self.screen=screen
        planets.append(self)
        self.trace=Trace(self.x,self.y,screen)
        self.screen_x=(x)*scale+shift_x
        self.screen_y=(y)*scale+shift_y
    def update(self,planets):
        global v_dict
        g=v_dict['g']
        self.ax=0
        self.ay=0
        for pl in planets:
            if pl!=self:
                r=math.sqrt(((self.x-pl.x)**2+(self.y-pl.y)**2))
                f=g*self.mass*pl.mass/(r**2)
                self.ay+=((pl.y-self.y)*f/r)/self.mass
                self.ax+=((pl.x-self.x)*f/r)/self.mass
    def move(self):
        global v_dict
        time=v_dict['time']
        self.x+=self.vel_x*time+self.ax*time**2
        self.y+=self.vel_y*time+self.ay*time**2
        
        self.vel_x+=self.ax*time
        self.vel_y+=self.ay*time
        self.trace.update(self.x,self.y)
    def draw(self):
        global WHITE,shift_y,shift_x
        self.screen_x=(self.x)*scale+shift_x
        self.screen_y=(self.y)*scale+shift_y
        self.screen_radius=self.radius*scale
        pygame.draw.circle(self.screen,WHITE,[self.screen_x,self.screen_y],self.screen_radius)
        self.trace.draw()
def draw_fps():
    current_fps=clock.get_fps()
    font=pygame.font.SysFont('Times New Roman',18)
    text_surf=font.render('FPS:'+str(round(current_fps)),1,WHITE,)
    screen.blit(text_surf,(10,0))
def handle_left_click(event):
    global map_l_click
    map_l_click=True
    move_last_cords=list(event.pos)
    x,y=event.pos
    for bar in bars:
        if abs(x-bar.handle_x)<=bar.handle_width+1 and abs(y-bar.y-bar.handle_length/2)<(bar.handle_length/2+1):
            bar.active=True
            map_l_click=False
    for text in text_inputs:
        if (x>text.x)and(x<text.x+text.length)and(y>text.y)and(y<text.y+text.height):
            if d_click_cl.tick()<=500:
                text.editing=True
                for text2 in text_inputs:
                    if text2!=text:
                        if text2.editing:
                            text2.editing=False
                            text2.end=True
                map_l_click=False
    for button in buttons:
        if (x>button.x)and(x<button.x+button.length)and(y>button.y)and(y<button.y+button.height):
            button.clicked=True
    for button in inworld_buttons:
        if (x>button.screen_x)and(x<button.screen_x+button.length)and(y>button.screen_y)and(y<button.screen_y+button.height):
            button.clicked=True
def handle_right_click(event):
    global New_planet_button
    if not adding_planet:
        screen_x,screen_y=event.pos
        x=(screen_x-shift_x)/scale
        y=(screen_y-shift_y)/scale
        if New_planet_button:
            New_planet_button.delete()
        New_planet_button=Inworld_button(x,y,['New Planet'],method=button1)
        New_planet_button.x=New_planet_button.x-New_planet_button.length/2/scale
        New_planet_button.y=New_planet_button.y+New_planet_button.height/2/scale
def do_events(events):
    global Running,map_l_click,shift_x,shift_y,move_last_cords,stopped,scale,static_texts,New_planet_button
    for event in events:
        if event.type == pygame.QUIT:
            Running = False
        elif event.type==pygame.MOUSEBUTTONDOWN:  
            move_last_cords=list(event.pos)                                          #Нажатие мыши
            if event.button==1:
                handle_left_click(event)
            if event.button==3:
                handle_right_click(event)
        elif event.type==pygame.MOUSEBUTTONUP:                                          #Отжатие мыши
            if event.button==1:
                map_l_click=False
            for bar in bars:
                bar.active=False    
        elif event.type==pygame.MOUSEMOTION:                                           #Движение мыши
            if map_l_click:
                move_new_cords=list(event.pos)
                shift_x+=move_new_cords[0]-move_last_cords[0]
                shift_y+=move_new_cords[1]-move_last_cords[1]
                move_last_cords=move_new_cords
            for bar in bars:
                if bar.active:
                    move_new_cords=list(event.pos)
                    dx=move_new_cords[0]-move_last_cords[0]
                    move_last_cords=move_new_cords
                    bar.z+=dx/bar.length*(bar.max-bar.min)
                    if bar.z>bar.max:
                        bar.z=bar.max
                    if bar.z<bar.min:
                        bar.z=bar.min
                    if move_last_cords[0]>bar.length+bar.x:
                        bar.z=bar.max
                    if move_last_cords[0]<bar.x:
                        bar.z=bar.min
        elif event.type==pygame.KEYDOWN:                                  #Кнопка клавиатуры
            if event.key==pygame.K_SPACE:
                stopped=not stopped
            elif event.key==pygame.K_RETURN:
                for text in text_inputs:
                    if text.editing:
                        text.editing=False
                        text.end=True
            else:
                for text in text_inputs:
                    if text.editing:
                        if event.key==pygame.K_BACKSPACE:
                            text.text=text.text[:-1]
                        elif event.key in keys:
                            text.text=text.text+pygame.key.name(event.key)                       
        elif event.type==pygame.MOUSEWHEEL:                                     # Колесо мыши
            x, y = pygame.mouse.get_pos()                           
            if event.y>0:
                shift_x=x-(event.y/10+1)*(x-shift_x)
                shift_y=y-(event.y/10+1)*(y-shift_y)
                scale*=(event.y/10+1)              
            else:
                shift_x=x-1/(-event.y/10+1)*(x-shift_x)
                shift_y=y-1/(-event.y/10+1)*(y-shift_y)
                scale=scale/(-event.y/10+1) 
    for button in buttons:
        button.update()      #Test
    for button in inworld_buttons:
        button.update()        
def init():
    global planets,screen,t1,t2,sc,New_planet_button
    # p1=planet(500,40,500,500,20,0,screen,planets)
    # p2=planet(500,20,500,700,-20,0,screen,planets)
    # p3=planet(500,20,600,200,25,15,screen,planets)


    # sp=(-11*100-20)/1000
    # sun=Planet(1000,25,250,250,-sp,0)
    # p1=Planet(100,10,250,450,-10,0)
    # p2=Planet(10,4,250,465,-22,0)
    # p3=Planet(600,20,600,729,-6,-2)

    # p4=Planet(1000,25,250,250,-8,0)
    # p5=Planet(500,15,250,350,16,0)
    e_v=0
    earth=Planet(5.9722*10**24,6371*1000,0,0,0+e_v,0)
    moon=Planet(7.35*10**22,1737.1*1000,0,364600000,1080+e_v,0)
    t1=Static_text(350,60,['time is'])
    t2=Static_text(WIDTH/2-20,100,['PAUSED'])
    
    b1=Scalebar(300,20,200,10,8,30,WHITE,BLUE,screen,0.01,0.2,0.1,'time')
    c1=Text_input(410,60,screen,f'{time}',variable='time')
    sc=Static_text(10,50,[f"Scale={scale}"])
    New_planet_button=None
def button2():
    global adding_planet,end_adding_button
    end_adding_button.delete()
    end_adding_button=None
    mass=v_dict['add_mass']
    x=v_dict['add_x']
    y=v_dict['add_y']
    vel_x=v_dict['add_vel_x']
    vel_y=v_dict['add_vel_y']
    radius=v_dict['add_radius']
    pl_new=Planet(mass,radius,x,y,vel_x,vel_y)
    adding_planet=False
    for i in add_list:
        i.delete()
    for i in add_list2:
        i.delete()     
def button1():

    # Нужно добавить класс New planet text/input
    #Нужно реализовать авто добавление в список add_list
    # реализовать авто расположение виджетов?

    global stopped,adding_planet,New_planet_button,end_adding_button,add_list,add_list2
    adding_planet=True
    add_list=[]
    add_list2=[]
    mass_text=Static_text(New_planet_button.screen_x,New_planet_button.screen_y,['mass:  '])
    mass_input=Text_input(New_planet_button.screen_x+mass_text.length,New_planet_button.screen_y,screen,'500','add_mass') 
    radius_text=Static_text(mass_text.x,mass_text.y+mass_text.height+5,['radius:  '])
    radius_input=Text_input(mass_text.x+radius_text.length,mass_text.y+mass_text.height+5,screen,'20','add_radius')     
    x_text=Static_text(radius_text.x,radius_text.y+radius_text.height+5,['x is:  '])
    x_input=Text_input(
        radius_text.x+x_text.length,x_text.y,screen,
        str(New_planet_button.x+New_planet_button.length/2/scale),   # можно сократить в два раза
        'add_x'
    )
    y_text=Static_text(x_text.x,x_text.y+x_text.height+5,['y is:  '])
    y_input=Text_input(x_text.x+x_text.length,y_text.y,screen,str(New_planet_button.y),'add_y')
    vel_x_text=Static_text(y_text.x,y_text.y+y_text.height+5,['horisontal velosity is:  '])
    vel_x_input=Text_input(y_text.x+vel_x_text.length,vel_x_text.y,screen,'0','add_vel_x')
    vel_y_text=Static_text(vel_x_text.x,vel_x_text.y+vel_x_text.height+5,['vertical velosity is:  '])
    vel_y_input=Text_input(vel_x_text.x+vel_y_text.length,vel_y_text.y,screen,'0','add_vel_y')
    max_x = vel_x_input.x
    add_list.append(mass_input)         # Теоретически этогоо не будет
    add_list.append(radius_input)
    add_list.append(x_input)
    add_list.append(y_input)
    add_list.append(vel_x_input)
    add_list.append(vel_y_input)
    add_list2.append(mass_text)
    add_list2.append(radius_text)
    add_list2.append(x_text)
    add_list2.append(y_text)
    add_list2.append(vel_x_text)
    add_list2.append(vel_y_text)
    for i in add_list:
        v_dict[i.variable]=float(i.text)   
    for i in add_list:
        i.x=max_x
    end_adding_button=Button((max_x+New_planet_button.screen_x)/2-10,vel_y_text.y+vel_y_text.height+10,['Submit planet'],method=button2)
    New_planet_button.delete()
    New_planet_button=None

def handle_new_planet():
    global stopped,adding_planet,New_planet_button,end_adding_button,add_list,add_list2
    
    if adding_planet:
        stopped=True
        
def draw_new_planet():
    if adding_planet:
        x=v_dict['add_x']*scale+shift_x
        y=v_dict['add_y']*scale+shift_y
        radius=v_dict['add_radius']
        pygame.draw.circle(screen,RED,(x,y),radius*scale)
def update():
    global time,t1,v_dict,stopped,t2,sc,adding_planet,New_planet_button
    global planets,HEIGHT,WIDTH
    WIDTH=screen.get_width()
    HEIGHT=screen.get_height()
    handle_new_planet()
    if not stopped:
        for pl in planets:
            pl.update(planets)
        for pl in planets:
            pl.move()
    t1.update(['time is'])
    sc.update([f"Scale={scale}"])
    t2.x=WIDTH/2-20
    if not stopped:
        t2.update(enabled=False)
        
    else:
        t2.update(enabled=True)
    for bar in bars:
        bar.update()    
    for text in text_inputs:
        text.update()
    
    
def draw():
    global planets
    screen.fill(BLACK)
    draw_new_planet()
    for pl in planets:
        pl.draw()
    for text in static_texts:
        text.draw()
    for bar in bars:
        bar.draw()
    for text in text_inputs:
        text.draw()
    for button in buttons:
        button.draw()
    for button in inworld_buttons:
        button.draw()
    draw_fps() 
    pygame.display.update()
init()
while Running:
    events=pygame.event.get()
    do_events(events)
    update()
    draw()
    clock.tick(FPS)
pygame.quit()
