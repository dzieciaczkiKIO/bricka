"""
 bricka (a breakout clone)
 Developed by Leonel Machava <leonelmachava@gmail.com>

 http://codeNtronix.com
"""
import sys
import pygame
from random import randint
from consty import *
import dataloader
import gfx
from rect import Brick,DaciuText,Konor,Ball,ComboText
import hiscores
from menu import YYMenu
from level import Level

def pow2(x):
    r = 1
    while x>0:
        r*=2
        x-=1
    return r

class YYBricka:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.joystick.init()
        
        self.screen = pygame.display.set_mode((800,600),pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        SCREEN_SIZE = self.screen.get_size()
        pygame.display.set_caption("KISI: The Game")
        
        self.gamepads=[]
        self.yygamepad()
        
        self.LowQuality=True
        
        self.clock = pygame.time.Clock()
        
        self.yymenu = YYMenu()
        dataloader.yyload(self)
        
        self.hiscores = hiscores.HiScores()
        self.hiscores.load("hiscores.txt")
        
        self.pressedButtons = {pygame.K_UP:False, pygame.K_DOWN:False, pygame.K_LEFT: False, pygame.K_RIGHT:False, pygame.K_ESCAPE:False}
        self.konorPress = False
        
        self.DaciuTexty = []
        self.ComboText = None
        self.bonusy = []
        
        self.levels = [Level('data/lev10.txt'),Level('data/lev3.txt'),Level('data/lev2.txt'),Level('data/lev4.txt'),Level('data/lev5.txt'),Level('data/lev6.txt'),Level('data/lev7.txt'),Level('data/lev8.txt'),Level('data/lev9.txt')]
        self.level = 0
        
        self.yydaciurs()
        
        self.rungame = True
        
        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        self.state=STATE_MENU
        #self.yyinit()

        
    def yyinit(self):
        self.lives = 5
        self.score = 0
        self.level = 0
        self.konory = 10
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = Ball(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)
        
        self.bonusy = []
        
        self.Konory = []
        
        self.combo = 0

        self.ball_vel = [5,-5]

        self.levels[self.level].yycreate()
        
    def yygamepad(self):
        if pygame.joystick.get_count()>0:
            print("Found %d gamepads" % pygame.joystick.get_count())
            for i in range(0,pygame.joystick.get_count()):
                self.gamepads.append(pygame.joystick.Joystick(i))
                self.gamepads[i].init()
        
    def yyinput(self):
        keys = pygame.key.get_pressed()
        
        if self.state==STATE_MENU:
            if keys[pygame.K_UP] and not self.pressedButtons[pygame.K_UP]:
                self.yymenu.move_up()
                self.pressedButtons[pygame.K_UP]=True
            elif keys[pygame.K_DOWN] and not self.pressedButtons[pygame.K_DOWN]:
                self.yymenu.move_down()
                self.pressedButtons[pygame.K_DOWN]=True
            elif keys[pygame.K_RETURN] or keys[pygame.K_x]:
                if self.yymenu.get_selection()==0:
                    self.yyinit()
                elif self.yymenu.get_selection()==2:
                    self.rungame=False
                elif self.yymenu.get_selection()==1:
                    self.state=STATE_SCORES
        
        if self.state==STATE_HISCORE:
            if keys[pygame.K_UP] and not self.pressedButtons[pygame.K_UP]:
                self.hiscores.move_selection(-1)
                self.pressedButtons[pygame.K_UP]=True
            elif keys[pygame.K_DOWN] and not self.pressedButtons[pygame.K_DOWN]:
                self.hiscores.move_selection(1)
                self.pressedButtons[pygame.K_DOWN]=True
            elif keys[pygame.K_RETURN]:
                self.hiscores.set_score(self.hiscores.get_selected(),self.score)
                self.hiscores.save("hiscores.txt")
                self.state=STATE_GAME_OVER
        
        if keys[pygame.K_LEFT] or (len(self.gamepads)>0 and self.gamepads[0].get_axis(0)<-0.1):
            self.paddle.left -= 8
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT] or (len(self.gamepads)>0 and self.gamepads[0].get_axis(0)>0.1):
            self.paddle.left += 8
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if (keys[pygame.K_SPACE] or (len(self.gamepads)>0 and self.gamepads[0].get_button(0))) and (self.state == STATE_BALL_IN_PADDLE or self.state == STATE_LOGO):
            self.ball_vel = [5,-5]
            self.state = STATE_PLAYING
            self.konorPress=True
        elif (keys[pygame.K_RETURN] or (len(self.gamepads)>0 and self.gamepads[0].get_button(9))) and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.yyinit()
            
        if self.konorPress and not keys[pygame.K_SPACE] and not keys[pygame.K_x] and (len(self.gamepads)<1 or not self.gamepads[0].get_button(0) and not self.gamepads[0].get_button(1)):
            self.konorPress=False
            
        if (keys[pygame.K_SPACE] or (len(self.gamepads)>0 and self.gamepads[0].get_button(0))) and (self.state == STATE_PLAYING) and not self.konorPress:
            self.konorPress=True
            self.yykonor(self.paddle.left+self.paddle.w/2,self.paddle.top-48)
            
        if (keys[pygame.K_x] or (len(self.gamepads)>0 and self.gamepads[0].get_button(1))) and (self.state == STATE_PLAYING) and not self.konorPress:
            self.konorPress=True
            self.yymultikonor(self.paddle.left+self.paddle.w/2,self.paddle.top-48)
        
        if keys[pygame.K_ESCAPE] and not self.pressedButtons[pygame.K_ESCAPE]:
            if self.state==STATE_MENU:
                self.rungame = False
            else:
                self.state=STATE_MENU
            self.pressedButtons[pygame.K_ESCAPE]=True
            
        if keys[pygame.K_b]:
            self.EnableBackground = not self.EnableBackground
            
        for (k,v) in self.pressedButtons.iteritems():
            if not keys[k] and self.pressedButtons[k]:
                self.pressedButtons[k]=False

    def yyball(self):
        self.ball.move()

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball.xflip()
            self.combo=0
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball.xflip()
            self.combo=0
        
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball.yflip()
        elif self.ball.top >= MAX_BALL_Y:            
            self.ball.top = MAX_BALL_Y
            self.ball.yflip()
            self.combo=0
            
    def yycolls(self):
        if self.level>=len(self.levels):
            return
        for brick in self.levels[self.level].bricks:
            if self.ball.colliderect(brick):
                self.score += 1 + pow2(self.combo)*2
                self.combo += 1
                self.ball.yflip()
                if self.sndJ is not None:
                    self.sndJ.play()
                self.yysmiatacz(brick.left+brick.width/2,brick.top+brick.height/2)
                _ra = randint(0,10)
                _ri = randint(0,2)
                if _ra>7:
                    self.bonusy.append([_ri,pygame.Rect(brick.left+brick.width/2-32,brick.top+brick.height/2-32,64,64)])
                self.levels[self.level].bricks.remove(brick)
                break
            for konor in self.Konory:
                if brick.colliderect(konor):
                    self.levels[self.level].bricks.remove(brick)
                    self.Konory.remove(konor)
                    self.score+=pow2(self.combo)
                    break     
        
        for bonus in self.bonusy:
            if self.paddle.colliderect(bonus[1]):
                id = bonus[0]
                if id==0:
                    self.score=self.score + 500
                    self.paddle.w = 320
                elif id==1:
                    self.score += 250
                    self.konory += 1
                elif id==2:
                    self.score += 300
                    self.lives += 1
                if self.sndS is not None:
                    self.sndS.play()
                self.yytext(BONUS_NAMES[id],bonus[1].left+32,bonus[1].top+32)
                self.bonusy.remove(bonus)

        if len(self.levels[self.level].bricks) == 0:
            if self.level>=len(self.levels):
                if self.hiscores.scored(self.score) is not None:
                    self.state = STATE_HISCORE
                else:
                    self.state = STATE_WON
            else:
                self.level+=1
                self.combo=0
                if self.level>=len(self.levels):
                    if self.hiscores.scored(self.score) is not None:
                        self.state = STATE_HISCORE
                    else:
                        self.state = STATE_WON
                else:
                    self.ball.speed*=1.1
                    self.levels[self.level].yycreate()
                    self.state = STATE_BALL_IN_PADDLE
            
        if self.ball.colliderect(self.paddle):
            self.combo=0
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            factor = (float(self.ball.centerx)-float(self.paddle.centerx))/(float(self.paddle.w)/2.0)
            self.ball.set_vx_factor(0.75*factor)
            self.ball.yflip()
            """ if factor < 0:
                factor = 0.001
            elif factor > 1:
                factor = 0.999
            elif factor > 0.49 and factor < 0.51:
                factor = 0.49
            self.ball.set_angle(165.0-factor*150.0) """
            if self.sndD is not None:
                self.sndD.play()
        elif self.ball.bottom >= SCREEN_SIZE[1]:
            self.combo=0
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                if self.hiscores.scored(self.score) is not False:
                    self.state = STATE_HISCORE
                else:
                    self.state = STATE_GAME_OVER
        
        if self.combo>2:
            if self.ComboText is not None and not self.ComboText.finished:
                self.ComboText.refresh("yykombo(%d)" % self.combo)
            else:
                self.ComboText = ComboText(400,300,"yykombo(%d)" % self.combo)

    def yyfps(self,fps):
        _w,_h=self.font.size("FPS="+str(fps))
        self.screen.blit(self.font.render("FPS="+str(fps),False,BLACK),(780-_w,8))
                
    def yystats(self):
        w_score,h_score = self.font.size("Punkty: "+str(self.score)+" Zycia: ")
        if self.BallImage:
            for i in range(self.lives):
                self.screen.blit(pygame.transform.scale(self.BallImage,(32,32)),(16+w_score+8+i*(32+4),8))
        if self.font:
            font_surface = self.font.render("Punkty: "+str(self.score)+" Zycia: ", False, BLACK).convert_alpha()
            self.screen.blit(font_surface, (16,8+(16-h_score/2)))
        
        w_score,h_score = self.font.size("Konory: ")
        if self.KonorImage:
            for i in range(self.konory):
                self.screen.blit(pygame.transform.scale(self.KonorImage,(32,32)),(16+w_score+8+i*(32+4),48))
        if self.font:
            font_surface = self.font.render("Konory: ", False, BLACK).convert_alpha()
            self.screen.blit(font_surface, (16,48+(16-h_score/2)))

    def yymessage(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, BLACK).convert_alpha()
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))
    
    def yydaciurs(self):
        self.daciurs=[]
        for i in range(16):
            _x = randint(30,SCREEN_SIZE[0]-30)
            _y = randint(30,SCREEN_SIZE[1]-30)
            _vx = randint(-10,10)
            _vy = randint(-10,10)
            _dir = randint(0,1)
            _n = randint(0,len(DACIUR_TEXTY)-1)
            _s = randint(24,38)
            _ff = randint(0,len(FONTS)-1)
            _f = pygame.font.SysFont(FONTS[_ff],_s)
            self.daciurs.append([_x,_y, _vx,_vy, _dir,_n,_f])
            
    def yyfloat(self):
        for i in range(0,len(self.daciurs)):
            if self.daciurs[i][4]==0:
                self.daciurs[i][0]+=self.daciurs[i][2]
                self.daciurs[i][1]+=self.daciurs[i][3]
            else:
                self.daciurs[i][0]-=self.daciurs[i][2]
                self.daciurs[i][1]-=self.daciurs[i][3]
            if self.daciurs[i][0]>=SCREEN_SIZE[0]-20 or self.daciurs[i][0]<=20 or self.daciurs[i][1]>=SCREEN_SIZE[1]-20 or self.daciurs[i][1]<=20:
                if self.daciurs[i][4]==0:
                    self.daciurs[i][4]=1
                else:
                    self.daciurs[i][4]=0
    
    def yydouble(self): ##drawing daciutextuw
        if self.LowQuality:
            for i in range(0,len(self.daciurs)):
                self.daciurs[i].render(screen)
        else:
            for i in range(0,len(self.daciurs)):
                _c = randint(0,len(TEXTCOLORS)-1)
                self.screen.blit(self.daciurs[i][6].render(DACIUR_TEXTY[self.daciurs[i][5]],False, TEXTCOLORS[_c]).convert_alpha(), (self.daciurs[i][0],self.daciurs[i][1]) )
    
    def yybonusy(self):
        for i in range(0,len(self.bonusy)):
            self.screen.blit(self.BonusImages[self.bonusy[i][0]], (self.bonusy[i][1].left,self.bonusy[i][1].top))
            
    def yywrap(self):
        i=0
        while i<len(self.bonusy):
            if(self.bonusy[i][1].top-32>SCREEN_SIZE[1]):
                self.bonusy.remove(self.bonusy[i])
            else:
                self.bonusy[i][1].top+=4
                i=i+1
        if self.paddle.w > PADDLE_WIDTH:
            self.paddle.inflate_ip(-1,0)
    
    def yyhalffloat(self): ## ticking daciutextuw
        if self.LowQuality:
            for text in self.DaciuTexty:
                if text.finished:
                    self.DaciuTexty.remove(text)
                else:
                    text.tickme()
        else:
            i=0;
            while i < len(self.DaciuTexty):
                if self.DaciuTexty[i][0]<80:
                    self.DaciuTexty[i][0]=self.DaciuTexty[i][0]+2
                    i=i+1
                else:
                    self.DaciuTexty.remove(self.DaciuTexty[i])
        if self.ComboText is not None:
            if self.ComboText.finished:
                self.ComboText = None
            else:
                self.ComboText.tickme()
    
    def yydembski(self): ##drawing daciutextuw
        if self.LowQuality:
            for text in self.DaciuTexty:
                text.render(self.screen)
        else:
            for i in range(0,len(self.DaciuTexty)):
                tekst = self.DaciuTexty[i][1] #tekstid
                fnt = FONTS[self.DaciuTexty[i][2]] #fontid
                ffont = pygame.font.SysFont(fnt,24+self.DaciuTexty[i][0])
                size = ffont.size(tekst)
                _c = randint(0,len(TEXTCOLORS)-1)
                font_surface = ffont.render(tekst,False,TEXTCOLORS[_c])
                self.screen.blit(font_surface, (self.DaciuTexty[i][3]-size[0]/2,self.DaciuTexty[i][4]-size[1]/2))
    
    def yytext(self,str,x,y,acc=1.0):
        if self.LowQuality:
            self.DaciuTexty.append(DaciuText(x,y,str,acc))
        else:
            self.DaciuTexty.append([0,str,randint(0,len(FONTS)-1),x,y])
    
    def yysmiatacz(self,x,y):
        self.yytext(DACIUR_TEXTY[randint(0,len(DACIUR_TEXTY)-1)],x,y,2.6)
    
    def yymultikonor(self,x,y):
        if self.konory>=3:
            self.konory-=1
            self.yykonor(x,y,90-15)
            self.yykonor(x,y,90)
            self.yykonor(x,y,90+15)
    
    def yykonor(self,x,y,dir=90):
        if self.konory>0:
            self.konory-=1
            self.Konory.append(Konor(x-24,y-24,48,48,dir))
    
    def yykonory(self):
        for konor in self.Konory:
            konor.move()
            if konor.top<-10:
                self.Konory.remove(konor)
                
    def yyjekon(self):
        for konor in self.Konory:
            self.screen.blit(self.KonorImage,(konor.left,konor.top))
    
    def run(self):
        while self.rungame:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit

            self.clock.tick(70)
            self.screen.fill(WHITE)
            
            # Draw walec daciuk
            if self.EnableBackground and self.BackgroundImage is not None:
                self.screen.blit(self.BackgroundImage, self.walecdaciuk)
                
            if self.ComboText is not None:
                self.ComboText.render(self.screen)
            
            self.yyinput()
            
#            self.yydouble()

            if self.state == STATE_MENU:
                self.yymenu.draw(self.screen)
            elif self.state == STATE_SCORES:
                self.hiscores.draw(self.screen)

            else:
                if self.state == STATE_PLAYING:
                    self.yyball()
                    self.yyfloat()
                    self.yycolls()
                    self.yyhalffloat()
                    self.yywrap()
                    self.yykonory()
                
                if self.level<len(self.levels):
                    self.levels[self.level].yybricks(self.screen)
                self.yybonusy()
                
                # Draw paddle
                if self.PaddleImage is not None:
                    self.screen.blit(gfx.abs_scale(self.PaddleImage,self.paddle.w,self.paddle.h),self.paddle)
                else:
                    pygame.draw.rect(self.screen, BLUE, self.paddle)

                self.yyjekon()
                
                # Draw ball
                if self.BallImage is not None:
                    pygame.draw.circle(self.screen, BLACK, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS, 2)
                    self.screen.blit(gfx.scalerotate(self.BallImage,self.BallScale,self.BallAngle),self.ball)
                    if self.BallScaleDown:
                        self.BallScale += 0.025;
                        if self.BallScale >= 1.15:
                            self.BallScaleDown=False;
                    else:
                        self.BallScale -= 0.025;
                        if self.BallScale <= 0.9:
                            self.BallScaleDown=True;
                    self.BallAngle+=3
                    self.BallAngle%=360
                else:
                    pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)
                            
                self.yydembski()
                
                if self.state == STATE_BALL_IN_PADDLE or self.state == STATE_LOGO:
                    self.ball.left = self.paddle.left + self.paddle.width / 2
                    self.ball.top  = self.paddle.top - self.ball.height
                    self.yymessage("PRESS SPACE TO LAUNCH THE DACIUK")
                elif self.state == STATE_HISCORE:
                    self.yymessage("Gracz /\\ %s \\/ uzyskal rekord %d" % (self.hiscores.get_selected(),self.score))
                elif self.state == STATE_GAME_OVER:
                    if self.Dead is not None:
                        gfx.centerblit(self.screen,self.Dead)
                    else:
                        self.yymessage("GAME OVER. PRESS ENTER TO PLAY AGAIN")
                elif self.state == STATE_WON:
                    if self.Won is not None:
                       gfx.centerblit(self.screen,self.Won)
                    else:
                        self.yymessage("YOU WON! PRESS ENTER TO PLAY AGAIN")
                
                self.yystats()
            self.yyfps(self.clock.get_fps())

            pygame.display.flip()
            
        pygame.mixer.quit()
        pygame.joystick.quit()

if __name__ == "__main__":
    YYBricka().run()
