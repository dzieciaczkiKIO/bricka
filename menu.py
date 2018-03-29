import os
import pygame
import consty
import dataloader

class YYMenu:
    def __init__(self):
        self.selection = 0
        self.items = []
        
        self.Logo = dataloader.loadimage("data/logo.png")
        _w,_h = self.Logo.get_size()
        self.xLogo=consty.SCREEN_SIZE[0]/2-_w/2
        y=_h+32
        self.items.append(MenuItem(dataloader.loadimage("data/yyplay.png"),y))
        y+=12+self.items[-1].get_h()
        self.items.append(MenuItem(dataloader.loadimage("data/yyhiscore.png"),y))
        y+=12+self.items[-1].get_h()
        self.items.append(MenuItem(dataloader.loadimage("data/yywrap.png"),y))
        y+=12+self.items[-1].get_h()
        
        
    def draw(self,surface):
        surface.blit(self.Logo,(self.xLogo,16))
        for item in self.items:
            item.draw(surface)
        pygame.draw.rect(surface, consty.BLUE, self.items[self.selection], 4)
        
    def get_selection(self):
        return self.selection
        
    def move_up(self):
        self.selection-=1
        self.selection%=len(self.items)
        
    def move_down(self):
        self.selection+=1
        self.selection%=len(self.items)
        
class MenuItem(pygame.Rect):
    def __init__(self,image,y):
        pygame.Rect.__init__(self,1,2,3,4)
        self.image = image
        self.w,self.h = image.get_size()
        self.left = consty.SCREEN_SIZE[0]/2-self.w/2
        self.top = y
        
    def get_h(self):
        return self.h
        
    def draw(self,surface):
        surface.blit(self.image,(self.left,self.top))
        return self.h