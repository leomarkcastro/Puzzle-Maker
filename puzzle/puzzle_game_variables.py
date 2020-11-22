import pygame
import random
import math
import os, json
from datetime import datetime
from math import ceil

game_folder = os.path.dirname(__file__)   

pygame.init()


#############################################################
#    SCREEN VARIABLES
#############################################################

class Screen():
    def __init__(self):
        self.SCREEN_X = 50
        self.SCREEN_Y = 45
        self.SCREENWIDTH = 800
        self.SCREENHEIGHT = 600
        self.FPS = 30
        self.FLAGS = 0 #pygame.FULLSCREEN|pygame.HWSURFACE
        self.SCREENCAPTION = 'Puzzle Game'
        
Screen = Screen()

def dt(x,y):
    x = ceil(x / 800 * Screen.SCREENWIDTH)
    y = ceil(y / 600 * Screen.SCREENHEIGHT)
    
    return (x,y)

def intsize(x,y):
    x = int(x)
    y = int(y)
    
    return (x,y)

#This sets up the spawning location of the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(Screen.SCREEN_X,Screen.SCREEN_Y)

#############################################################
#    UNIVERSAL VARIABLES FOR UNIFORMITY
#############################################################

loadedData = 0

'''with open("STYLES.json") as f:
    loadedData = json.load(f)

def parseData(id):
    return eval(loadedData[id], {})'''

class Color():
    def __init__(self):
        self.monochrome()
    
    def monochrome(self):
        
        self.WHITE = (255,255,255)
        self.WHITE2 = (254,254,254)
        self.BLACK = (0,0,0)
        self.BLACK2 = (1,1,1)
        self.RED = (125,125,125)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.YELLOW = (255,255,0)
        self.VIOLTER = (255,0,255)
        self.SKYBLUE = (0,255,255)
        self.LIGHTGRAY = (50,50,50)
        self.LIGHTLIGHTGRAY = (150,150,150)
        self.LIGHTLIGHTLIGHTGRAY = (200,200,200)
        self.ULTRAGRAY = (225,225,225)
    
    def defaultColor(self):
        self.WHITE = (255,255,255)
        self.WHITE2 = (254,254,254)
        self.BLACK = (0,0,0)
        self.BLACK2 = (1,1,1)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.YELLOW = (255,255,0)
        self.VIOLTER = (255,0,255)
        self.SKYBLUE = (0,255,255)
        self.LIGHTGRAY = (100,100,100)
        self.LIGHTLIGHTGRAY = (200,200,200)
        
Color = Color()

class Direction():
    def __init__(self):
        self.UP = 0
        self.LEFT = 1
        self.DOWN = 2
        self.RIGHT = 3
    
Direction = Direction()
    
#############################################################
#    FONTS MANAGEMENT
#############################################################

font_folder = os.path.join(game_folder, 'Fonts')

font_array = {
    'Comfortaa' : os.path.join(font_folder, "Comfortaa-Regular.ttf"),
    'Comfortaa-Bold' : os.path.join(font_folder, "Comfortaa-Bold.ttf"),
    'Open Sans' : os.path.join(font_folder, "OpenSans-Regular.ttf"),
    'Open Sans-Bold' : os.path.join(font_folder, "OpenSans-Bold.ttf"),
    }

font_typo = {
    "Comfortaa" : {
        "XXSmall": (font_array['Comfortaa'],8),
        "XSmall": (font_array['Comfortaa'],10),
        "Small": (font_array['Comfortaa'],15),
        "Regular" : (font_array['Comfortaa'],23),
        "Bold" : (font_array['Comfortaa-Bold'],23),
        "BigRegular" : (font_array['Comfortaa'],40),
        "BigBold" : (font_array['Comfortaa-Bold'],40),
        },
    "Open Sans" : {
        "XXSmall": (font_array['Open Sans'],5),
        "XSmall": (font_array['Open Sans'],10),
        "Small": (font_array['Open Sans'],15),
        "Regular" : (font_array['Open Sans'],23),
        "Bold" : (font_array['Open Sans-Bold'],23),
        "BigRegular" : (font_array['Open Sans'],40),
        "BigBold" : (font_array['Open Sans-Bold'],40),
        },
    }

font_color = {
    "BlackWhite": (Color.BLACK, Color.WHITE),
    "WhiteNone": (Color.WHITE, None),
    "BlackNone": (Color.BLACK, None),
    "Black2None": (Color.BLACK2, None),
    "GrayNone": (Color.LIGHTGRAY, None),
    "Gray2None": (Color.LIGHTLIGHTGRAY, None),
    "BlueNone": (Color.BLUE, None),
    "RedNone": (Color.RED, None),
    }
    
def textdisplay(message, color, fontset):
    font = pygame.font.Font(fontset[0],fontset[1])
    text = font.render(message, True, color[0], color[1])
    textRect = text.get_rect()
    
    return text,textRect

from PIL import Image, ImageEnhance
import cv2

def crop_image(input_image, output_image, start_x, start_y, width, height, result_width=2000, sharpRate = 1, antiAlias = True):
    """Pass input name image, output name image, x coordinate to start croping, y coordinate to start croping, width to crop, height to crop """
    input_img = Image.open(input_image)
    box = (start_x, start_y, start_x + width, start_y + height)
    output_img = input_img.crop(box)
    
    output_img.save(output_image, quality=100)
    
    enlarge_image_cv(output_image, result_width)
    
def enlarge_image_cv(src, width=750):
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
 
    or_width = img.shape[0]
    or_height = img.shape[1]
    ratio = or_height/or_width
 
    height = width*ratio
    dim = intsize(height, width)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
    
    cv2.imwrite(src, resized)
     
    

def checkFolder(loc):
    if not os.path.exists(loc):
        os.makedirs(loc)
        
def Pol(x, y):
    """Converts rectangular coordinates into polar ones"""
    if x == 0: # This might be the source of my problems, but without it, it raises ZeroDivisionErrors at certain places
        if y >= 0:
            return [y, 90]
        else:
            return [-y, 270]
    r     = math.sqrt(x**2+y**2)
    angle = (math.degrees(math.atan((y/x))))%360
    return [r, angle]

