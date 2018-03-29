import pygame
from rect import Brick
from consty import BRICK_WIDTH,BRICK_HEIGHT,BRICK_COLORS
from random import randint
import os

class Level:
    def __init__(yy,level='test'):
        yy.bricks=[]
        yy.origbricks=[]
        if level=='test':
            yy.yytestlevel()
        else:
            x=0
            y=72
            if os.path.isfile(level):
                f = open(level,'r')
                lines = f.readlines()
                f.close()
                for l in lines:
                    x=64
                    for c in l:
                        if c=='#':
                            yy.origbricks.append(Brick(x,y,BRICK_WIDTH,BRICK_HEIGHT,BRICK_COLORS[randint(0,len(BRICK_COLORS)-1)]))
                        x+= BRICK_WIDTH + 10
                    y+=BRICK_HEIGHT + 5
        
    def yybricks(yy,screen):
        for brick in yy.bricks:
            pygame.draw.rect(screen, brick.color, brick)
        
    def yytestlevel(yy):
        y_ofs = 72
        yy.origbricks = []
        for i in range(4):
            x_ofs = 64
            for j in range(10):
                if j<=3 or j>=6:
                    yy.origbricks.append(Brick(x_ofs,y_ofs,BRICK_WIDTH,BRICK_HEIGHT,BRICK_COLORS[randint(0,len(BRICK_COLORS)-1)]))
                x_ofs += BRICK_WIDTH + 10
            y_ofs += BRICK_HEIGHT + 5
        
    def yycreate(yy): #create bricks
        yy.bricks = []
        for b in yy.origbricks:
            yy.bricks.append(b)
        