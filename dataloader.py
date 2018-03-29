import pygame
from random import randint
from os import path

CONVERT_ALPHA = 0
CONVERT = 1
NO_CONVERT = 255


def loadimage(file,convert=CONVERT_ALPHA):
    if not path.isfile(file):
        return None
    if convert==CONVERT_ALPHA:
        return pygame.image.load(file).convert_alpha()
    elif convert==CONVERT:
        return pygame.image.load(file).convert()
    else:
        return pygame.image.load(file)

def yyload(self):
    self.Won = loadimage("data/won.png")
    self.Dead = loadimage("data/dead.png")

    self.BallImage = loadimage("data/bricka.png")
    if self.BallImage is not None:
        self.BallImageW,self.BallImageH = self.BallImage.get_size()
    self.BallAngle = 0
    self.BallScale = 1.0
    self.BallScaleDown = False;
        
    self.BackgroundImage = None
    self.BackgroundImage = loadimage("data/daxiux.jpg",CONVERT)
    self.walecdaciuk = pygame.Rect(0,0,800,600)
    self.EnableBackground = True
    
    self.sndJ = None
    self.sndJ = pygame.mixer.Sound("data/j.ogg")
    self.sndD = None
    self.sndD = pygame.mixer.Sound("data/d.ogg")
    self.sndS = None
    self.sndS = pygame.mixer.Sound("data/s.ogg")
    
    self.BonusImages = [None,None,None]
    self.BonusImages[0] = loadimage("data/dembski.png")
    self.BonusImages[1] = loadimage("data/smiatacz.png")
    self.BonusImages[2] = loadimage("data/ocet.png")
    
    self.KonorImage = loadimage("data/konor.png")
    
    self.PaddleImage = loadimage("data/paddle.jpg",CONVERT)
