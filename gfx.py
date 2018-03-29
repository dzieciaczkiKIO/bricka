import pygame

def scalerotate(image,scale,rotate):
    _w,_h = image.get_size()
    return pygame.transform.scale(pygame.transform.rotate(image,rotate),(int(_w*scale),int(_h*scale)))
    
def centerblit(screen,image):
    _w,_h = image.get_size()
    _sw,_sh = screen.get_size()
    screen.blit(image,(_sw/2-_w/2,_sh/2-_h/2))
    
def scaled(surface,scale):
    _w,_h=surface.get_size()
    _w = int(_w*scale)
    _h = int(_h*scale)
    return pygame.transform.scale(surface,(_w,_h))


def abs_scale(surface,w,h):
    return pygame.transform.scale(surface,(w,h))
    
