DACIUR_TEXTY = "kisi najlepsza katedra","uajuajrap()","gnu bajsyn","dobre folje","slowacka ksiazka","ajajmor","lista o 18 xD","dr.hab.inz.jandaciuk","KW_BEGIN"

SCREEN_SIZE   = 800,600

# Object dimensions
BRICK_WIDTH   = 60
BRICK_HEIGHT  = 25
PADDLE_WIDTH  = 161
PADDLE_HEIGHT = 17
BALL_DIAMETER = 64
BALL_RADIUS   = BALL_DIAMETER / 2

MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
BRICK_COLOR = (200,200,0)
RED = (255,0,0)
GREEN = (0,255,0)

BRICK_COLORS = (200,200,0),(0,200,200),(200,0,200),(100,200,0),(200,100,0),(200,0,100),(100,0,200),(100,100,0),(200,100,100),(100,200,100),(100,100,200)

TEXTCOLORS = BLACK,BLUE,BRICK_COLOR,RED,GREEN
FONTS = "Comic Sans MS","Times New Roman","Arial","Calibri","Courier New","Tahoma","Verdana"
MAX_FONT_SIZE = 108
INITIAL_TEXT_SCALE=0.25
MAX_TEXT_TICKS=80

KONOR_SPEED=8.0
BALL_SPEED=7.07
ORIG_BALL_SPEED=7.07

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3
STATE_LOGO = 4
STATE_HISCORE = 5
STATE_MENU = 6
STATE_SCORES = 7

BONUS_NAMES = "dembski.fis", "zmiatacz!", "C:\\Ocet.exe -c main.c"