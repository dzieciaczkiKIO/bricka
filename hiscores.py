
import os
import pygame
import consty
import dataloader

GRACZE = "Daciur","Konor","Dembski","Szwoch","Lebiedz","Kowalczuk","Dziubich","Boing","Matuszek"

class HiScores:
    def __init__(yy):
        yy.scores = []
        yy.sel = 0
        yy.font = pygame.font.SysFont("Impact",20)
        yy.title = dataloader.loadimage("data/yyhiscore.png")
        _w,_h = yy.title.get_size()
        yy.xTitle = consty.SCREEN_SIZE[0]/2-_w/2
        
    def get_selected(yy):
        return GRACZE[yy.sel%len(GRACZE)]
        
    def move_selection(yy,d):
        yy.sel+=d
    
    def load(yy,file):
        if os.path.isfile(file):
            f = open(file,"r")
            lines = f.readlines()
            f.close()
            for line in lines:
                if not len(line)<4:
                    yy.scores.append([line.split(";")[0],int(line.split(";")[1])])
        else:
            for i in range(10,0,-1):
                yy.scores.append(["Szwoch",(i+1)*100])
    
    def scored(yy,score):
        i=0
        for s in yy.scores:
            if score>s[1]:
                return i
            else:
                i+=1
        return False
    
    def set_score(yy,name,value):
        v = yy.scored(value)
        new_scores=[]
        for i in range(0,v):
            new_scores.append(yy.scores[i])
        new_scores.append([name,value])
        for i in range(v,9):
            new_scores.append(yy.scores[i])
        yy.scores = new_scores
    
    def save(yy,file):
        f = open(file,"w")
        for s in yy.scores:
            f.write("%s;%s\n" % (s[0],str(s[1])))
        f.close()
        
    def draw(yy,surface):
        y = 128
        surface.blit(yy.title,(yy.xTitle,16))
        for score in yy.scores:
            surf = yy.font.render("%s" % score[0],False,consty.BLACK)
            surf2 = yy.font.render("%d" % score[1],False,consty.BLACK)
            w,h = surf.get_size()
            w2,h2 = surf2.get_size()
            y+=h+12
            surface.blit(surf,(128,y))
            surface.blit(surf2,(consty.SCREEN_SIZE[1]-128-w2,y))