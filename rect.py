import pygame
import gfx
import consty
from random import randint
import math

class Brick(pygame.Rect):
    
    def __init__(self,x,y,w,h,color=(0,0,0)):
        pygame.Rect.__init__(self,x,y,w,h)
        self.color = color

class Ball(pygame.Rect):
    def __init__(self,x,y,w,h):
        pygame.Rect.__init__(self,x,y,w,h)
        self.angle=45
        self.vx=math.cos(math.radians(self.angle))*consty.BALL_SPEED
        self.vy=math.sin(math.radians(self.angle))*consty.BALL_SPEED
        self.speed = consty.BALL_SPEED
    
    def move(self):
        self.top-=self.vy
        self.left+=self.vx
    
    def fix_vy(self):
        if self.vy>-0.5 and self.vy<0.5:
            if self.vy<0:
                self.vy=-0.55
            elif self.vy>0:
                self.vy=0.55
    
    def yflip(self):
        if self.speed<self.vx:
            self.vy=-self.vy
        elif self.vy>0:            
            self.vy=-math.sqrt(math.fabs(self.speed*self.speed - self.vx*self.vx))
        else:
            self.vy=math.sqrt(math.fabs(self.speed*self.speed - self.vx*self.vx))
        self.fix_vy()
    
    def xflip(self):
        self.vx=-self.vx
        self.fix_vy()
    
    def set_vx_factor(self,factor):
        self.vx=factor*self.speed
        self.fix_vy()
    
    def set_angle(self,angle):
        self.angle=angle
        self.vx=math.cos(math.radians(self.angle))*self.speed
        self.vy=math.sin(math.radians(self.angle))*self.speed
        
class Konor(pygame.Rect):
    def __init__(self,x,y,w,h,dir=90):
        pygame.Rect.__init__(self,x,y,w,h)
        self.vy = math.sin(math.radians(dir))*consty.KONOR_SPEED
        self.vx = math.cos(math.radians(dir))*consty.KONOR_SPEED
        
    def move(self):
        self.top-=self.vy
        self.left+=self.vx

class DaciuText(pygame.Rect):
    def __init__(self,x,y,text,accelerate=1.0):
        pygame.Rect.__init__(self,x-1,y-1,2,2)
        offset = randint(0,len(consty.TEXTCOLORS))
        font = randint(0,len(consty.FONTS)-1)
        self.surfaces=[]
        self.fnt = pygame.font.SysFont(consty.FONTS[font],consty.MAX_FONT_SIZE)
        for i in range(0,3):
            self.surfaces.append(self.fnt.render(text,False,consty.TEXTCOLORS[(offset+i) % len(consty.TEXTCOLORS)]))
        self.tick=0
        self.scale=consty.INITIAL_TEXT_SCALE
        self.alpha=0.1
        self.v_alpha=(1.0-self.alpha)*3/float(consty.MAX_TEXT_TICKS)
        self.v_scale=(1.0-self.scale)*accelerate/float(consty.MAX_TEXT_TICKS)
        self.finished=False
        
    def tickme(self):
        self.tick+=1
        if self.alpha<1.0:
            self.alpha+=self.v_alpha
            if self.alpha>1.0:
                self.alpha=1.0
        if self.scale<1.0:
            self.scale+=self.v_scale
        if self.tick>=consty.MAX_TEXT_TICKS:
            self.finished=True
    
    def render(self,screen):
        scaled = gfx.scaled(self.surfaces[int(self.tick/3)%len(self.surfaces)],self.scale)
        _w,_h = scaled.get_size()
        scaled.set_alpha(int(255.0*self.alpha))
        screen.blit(scaled,(self.x-_w/2,self.y-_h/2))
        
class ComboText(DaciuText):
    def __init__(self,x,y,text,accelerate=1.0):
        DaciuText.__init__(self,x,y,text,accelerate)
        del self.surfaces[2]
        del self.surfaces[1]
        
    def refresh(self,text):
        self.tick=0
        self.surfaces[0]=self.fnt.render(text,False,consty.TEXTCOLORS[randint(0,len(consty.TEXTCOLORS)) % len(consty.TEXTCOLORS)])