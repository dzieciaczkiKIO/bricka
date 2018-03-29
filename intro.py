import pygame
import gfx

class Intro:

    
    def __init__(self):
        self.frame = 0
        self.index = 1
        self.frames = [0,200,400,600,800]
        self.dembski = pygame.image.load('data/dembski.png').convert_alpha()
        
        
        pass

    def tick(self):
        self.frame+=1
        if self.frames[self.index]==self.frame:
            self.index+=1

    def draw(self,screen):
        alpha = 255*(self.frame-self.frames[self.index-1])/(self.frames[self.index]-self.frames[self.index-1])
        gfx.centerblit(screen,dembski)

    def finished(self):
        if self.frame>=self.frames[-1]:
            return True
        else return False
        
