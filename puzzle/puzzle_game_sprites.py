import math

if True: 
    from .puzzle_game_variables import *
else: 
    from puzzle_game_variables import *
    
    
############################# SHITTY PATCH AHEAD

import pygame.gfxdraw

def draw_rounded_rect(surface, rect, color, corner_radius):
    ''' Draw a rectangle with rounded corners.
    Would prefer this: 
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    but this option is not yet supported in my version of pygame so do it ourselves.

    We use anti-aliased circles to make the corners smoother
    '''
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)


def draw_bordered_rounded_rect(surface, rect, color, border_color, corner_radius, border_thickness):
    if corner_radius < 0:
        raise ValueError(f"border radius ({corner_radius}) must be >= 0")

    rect_tmp = pygame.Rect(rect)
    center = rect_tmp.center

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect_tmp)
        else:
            draw_rounded_rect(surface, rect_tmp, border_color, corner_radius)

        rect_tmp.inflate_ip(-2*border_thickness, -2*border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect_tmp)
    else:
        draw_rounded_rect(surface, rect_tmp, color, inner_radius)
        
#############################################################################

class ColorBox(pygame.sprite.Sprite):
    def __init__(self, color, pos, size, id=None):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.fill(Color.WHITE2)
        self.image.set_colorkey(Color.WHITE2)
        
        pygame.draw.rect(self.image, color, [0, 0, size[0], size[1]])
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.updating = False
        
        self.static = True
        
        self.id = id
        
        self.update()
        
    def update(self):
        #self.rect.x += 1
        pass
    
class ColorBoxCross(pygame.sprite.Sprite):
    def __init__(self, color, pos, size, id=None):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.fill(Color.WHITE2)
        self.image.set_colorkey(Color.WHITE2)
        
        pygame.draw.rect(self.image, color, [0, 0, size[0], size[1]])
        pygame.draw.line(self.image, Color.LIGHTLIGHTGRAY, (0, 0), (size[0], size[1]), 3)
        pygame.draw.line(self.image, Color.LIGHTLIGHTGRAY, (size[0], 0), (0, size[1]), 3)
        pygame.draw.rect(self.image, Color.LIGHTLIGHTGRAY, [0, 0, size[0]*0.975, size[1]*0.975], 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.updating = False
        
        self.static = True
        
        self.id = id
        
        self.update()
        
    def update(self):
        #self.rect.x += 1
        pass
    
class ColorBoxThin(pygame.sprite.Sprite):
    def __init__(self, color, bg, pos, size, thinDir, id=None):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.fill(Color.BLACK2)
        self.image.set_colorkey(Color.BLACK2)
        
        pygame.draw.rect(self.image, color, [0, 0, size[0], size[1]])
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        # up down left right
        
        thinPercent = 0.4
        
        if thinDir[3] and False:
            pygame.draw.rect(self.image, bg, [0, 0, size[0], size[1]*thinPercent])
        if thinDir[2] and False:
            pygame.draw.rect(self.image, bg, [0, size[1]*(1-thinPercent), size[0], size[1]*thinPercent])
        if thinDir[0] and False:
            pygame.draw.rect(self.image, bg, [0, 0, size[0]*thinPercent, size[1]])
        if thinDir[1] and False:
            pygame.draw.rect(self.image, bg, [size[1]*(1-thinPercent), 0, size[0]*thinPercent, size[1]])
        
        self.updating = False
        
        self.static = True
        
        self.id = id
        
        self.update()
        
    def update(self):
        #self.rect.x += 1
        pass

class LoadingBox(pygame.sprite.Sprite):
    def __init__(self, color, pos, size):
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.fill(Color.WHITE)
        self.image.set_colorkey(Color.WHITE)
        
        self.curValue = 0
        
        self.color = color
        self.size = size
        
        pygame.draw.rect(self.image, color, [0, 0, size[0]*self.curValue, size[1]])
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.updating = False
        
        self.static = True
        
        self.id = id
        
        
        self.update()
        
    def updateValue(self,value):
        self.image.fill(Color.WHITE)
        
        self.curValue = value
        
        pygame.draw.rect(self.image, self.color, [0, 0, self.size[0]*self.curValue,self.size[1]])
        
        
    def update(self):
        #self.rect.x += 1
        pass
    
    
class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, pos, 
                        size=dt(223,38), 
                        bg_color=Color.WHITE, 
                        f_color=font_color["Black2None"], 
                        f_typo = font_typo["Comfortaa"]["Regular"]):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.bgcolor = bg_color
        self.text = text
        self.pos = pos
        self.size = size
        self.f_color = f_color
        self.f_typo = f_typo
        
        self.updating = True
        self.static = False

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.update()
        
    def _game_display_text(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.textSurf, self.textRect)
        
    def set_Text(self, text):
        self.text = text
        self.updating = True
        self.update()
        
    def dateTime(self):
        now = datetime.now()
        return now.strftime("%d/%m")
    
    def update(self):
        pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])
        self._game_display_text(self.text)
        self.updating = False
        
class TextBoxLeft(pygame.sprite.Sprite):
    def __init__(self, text, pos, 
                        size=dt(223,38), 
                        bg_color=Color.WHITE, 
                        f_color=font_color["Black2None"], 
                        f_typo = font_typo["Comfortaa"]["Regular"]):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.bgcolor = bg_color
        self.text = text
        self.pos = pos
        self.size = size
        self.f_color = f_color
        self.f_typo = f_typo
        
        self.updating = True
        self.static = False

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.update()
        
    def _game_display_text(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.center = self.image.get_rect().center
        self.textRect.left = self.image.get_rect().left
        self.image.blit(self.textSurf, self.textRect)
        
    def set_Text(self, text):
        self.text = text
        self.updating = True
        self.update()
        
    def dateTime(self):
        now = datetime.now()
        return now.strftime("%d/%m")
    
    def update(self):
        pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])
        self._game_display_text(self.text)
        self.updating = False
       
class TextBorder(pygame.sprite.Sprite):
    def __init__(self, text, pos, 
                        size=dt(50,50), 
                        bg_color=Color.WHITE, 
                        bd_color=Color.BLACK2,
                        bd_width=2,
                        f_color=font_color["Black2None"], 
                        f_typo = font_typo["Comfortaa"]["Regular"],
                        id = None):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.bgcolor = bg_color
        self.bdcolor = bd_color
        self.text = text
        self.pos = pos
        self.size = size
        self.f_color = f_color
        self.f_typo = f_typo
        
        self.prevMouseType = 0
        self.mouseType = 0 #0 Off 1 Hover 2 Click
        
        self.hoverColor = Color.YELLOW
        self.clickColor = Color.GREEN
        
        self.width = bd_width
        
        self.updating = True
        self.id = id

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.center = self.rect.center
        self.topLeft = self.rect.topleft
        self.bottomRight = self.rect.bottomright
        
        self.update()
        
    def game_display_text(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.textSurf, self.textRect)
    
    def update(self):
        if self.mouseType == 1:
            pygame.draw.rect(self.image, self.hoverColor, [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, self.bdcolor, [0, 0, self.size[0]*0.975, self.size[1]*0.975],self.width)
            self.game_display_text(self.text)
            self.updating = False
        elif self.mouseType == 2:
            pygame.draw.rect(self.image, self.clickColor, [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, self.bdcolor, [0, 0, self.size[0]*0.975, self.size[1]*0.975],self.width)
            self.game_display_text(self.text)
            self.updating = False
        else:
            pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])
            pygame.draw.rect(self.image, self.bdcolor, [0, 0, self.size[0]*0.975, self.size[1]*0.975],self.width)
            self.game_display_text(self.text)
            self.updating = False
    
    def mouseDetect(self):
        self.mouseType = 0
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.mouseType += 1
                return True
            self.mouseType += 1
            self.prevMouseType = self.mouseType
            self.updating = True
        if self.mouseType == 0 and self.prevMouseType != 0:
            self.updating = True
            self.prevMouseType = 0
        return 0




class NonogramClues(pygame.sprite.Sprite):
    def __init__(self, text, pos, 
                        size=dt(223,38), 
                        bg_color=Color.WHITE, 
                        f_color=font_color["Black2None"], 
                        f_typo = font_typo["Comfortaa"]["Regular"],
                        id=None,
                        direction = None):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.bgcolor = bg_color
        self.text = text
        self.pos = pos
        self.size = size
        self.f_color = f_color
        self.f_typo = f_typo
        
        #Extract clues
        self.text = self.text.strip()
        self.cluesList = self.text.split(' ')
        
        self.id = id
        
        self.curMode = 1
        self.lastTick = pygame.time.get_ticks()
        
        self.updating = True
        self.static = False

        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.update()
        
    def _game_display_text(self, text, index):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        if self.direction == "vert":
            self.textRect.center = self.image.get_rect().center
            self.textRect.y = self.image.get_rect().height/len(self.cluesList) * index
            self.textRect.height = self.image.get_rect().height/len(self.cluesList)
        elif self.direction == "hori":
            self.textRect.center = self.image.get_rect().center
            self.textRect.x = self.image.get_rect().width/len(self.cluesList) * index
            self.textRect.width = self.image.get_rect().width/len(self.cluesList)
        self.image.blit(self.textSurf, self.textRect)
    
    def _colorFadeUtil(self, value):
        return value*255
    
    def setMode(self, mode):
        self.curMode = mode
        self.lastTick = pygame.time.get_ticks()
        self.updating = True
        self.update()
    
    def update(self):
        pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])
        
        if self.curMode < 1:
            x = int(self._colorFadeUtil(self.curMode))
            pygame.draw.rect(self.image, (255 | x, 0 | x, 0 | x), [0, 0, self.size[0], self.size[1]])
        
        
        for index, item in enumerate(self.cluesList):
            self._game_display_text(item, index)
        
        if self.curMode < 1:
            if self.lastTick + 1000/Screen.FPS < pygame.time.get_ticks():
                self.curMode +=  1 / 6
                self.curMode = min(self.curMode, 1)
                self.lastTick = pygame.time.get_ticks()
        
        if self.curMode == 1:
            self.updating = False
  
class NonogramBlocks(pygame.sprite.Sprite):
    def __init__(self, text, pos, 
                        size=dt(50,50), 
                        bg_color=[Color.WHITE, Color.BLACK2, Color.LIGHTLIGHTLIGHTGRAY], 
                        bd_color=Color.BLACK2,
                        bd_width=2,
                        f_color=font_color["Black2None"], 
                        f_typo = font_typo["Comfortaa"]["Regular"],
                        id = None):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.bgcolor = bg_color
        self.bdcolor = bd_color
        self.text = text
        self.pos = pos
        self.size = size
        self.f_color = f_color
        self.f_typo = f_typo
        
        self.prevMouseType = 0
        self.mouseType = 0 #0 Off 1 Hover 2 Click
        
        self.hoverColor = Color.YELLOW
        self.clickColor = Color.GREEN
        
        self.width = bd_width
        
        self.updating = True
        self.id = id
        
        self.mode = 0
        self.ready = True

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.center = self.rect.center
        
        self.update()
        
    def game_display_text(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.textSurf, self.textRect)
    
    def update(self):
        pygame.draw.rect(self.image, self.bgcolor[self.mode], [0, 0, self.size[0], self.size[1]])
        pygame.draw.rect(self.image, self.bdcolor, [0, 0, self.size[0]-1, self.size[1]-1],self.width)
        self.game_display_text(self.text)
        self.updating = False
        
    def mouseDetect(self):
        self.mouseType = 0
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouseType += 1
            if pygame.mouse.get_pressed()[0] and self.ready:
                self.mouseType += 1
                self.ready = False
                return True
            self.prevMouseType = self.mouseType
            self.updating = True
        if self.mouseType == 0 and self.prevMouseType != 0:
            self.updating = True
            self.prevMouseType = 0
            self.ready = True
        return 0




class ColorBoxDynamic(pygame.sprite.Sprite):
    def __init__(self, pos, 
                        size=dt(50,50), 
                        inactive = Color.WHITE,
                        active = Color.YELLOW,
                        active2 = Color.BLUE,
                        active3 = Color.RED,
                        id = None):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.colors = [inactive, active, active2, active3]
        self.pos = pos
        self.size = size
        self.id = id
        
        self.curMode = 0
        
        self.updating = True
        self.prevMouseType = 0
        self.mouseType = 0 #0 Off 1 Hover 2 Click
        
        self.ready = False
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.center = self.rect.center
        
        self.update()
    
    def setReady(self):
        self.ready = True
        self.setMode(1)
    
    def setMode(self, mode):
        self.curMode = mode
        self.update()
    
    def update(self):
        pygame.draw.rect(self.image, self.colors[self.curMode], [0, 0, self.size[0], self.size[1]])
        self.updating = False
        
    def mouseDetect(self):
        self.mouseType = 0
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.mouseType += 1
            self.mouseType += 1
            self.prevMouseType = self.mouseType
            self.updating = True
        if self.mouseType == 0 and self.prevMouseType != 0:
            self.updating = True
            self.prevMouseType = 0
        return self.mouseType


class MazeThinBlock(pygame.sprite.Sprite):
    def __init__(self, mode,pos, 
                        size=dt(50,50), 
                        inactive = Color.WHITE,
                        active = Color.YELLOW,
                        active2 = Color.BLUE,
                        active3 = Color.RED,
                        id = None,
                        borders = True):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.colors = [inactive, active, active2, active3]
        self.pos = pos
        self.size = size
        self.id = id
        
        self.borders = borders
        
        #Up down left right, True means passable
        self.border = [True] * 4
        self.border[0] = 'U' in mode
        self.border[1] = 'D' in mode
        self.border[2] = 'L' in mode
        self.border[3] = 'R' in mode
        self.mode = mode
        
        self.curMode = 0
        
        self.updating = True
        self.prevMouseType = 0
        self.mouseType = 0 #0 Off 1 Hover 2 Click
        
        self.ready = False
        
        self.width = 2
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.center = self.rect.center
        
        self.update()
    
    def setReady(self):
        self.ready = True
        self.setMode(1)
    
    def setMode(self, mode):
        self.curMode = mode
        self.update()
    
    def update(self):
        pygame.draw.rect(self.image, self.colors[self.curMode], [0, 0, self.size[0], self.size[1]])
        
        if self.borders:
            if not self.border[0]: pygame.draw.line(self.image, Color.BLACK2, [0,0], [self.size[0],0], self.width)  #UP
            if not self.border[1]: pygame.draw.line(self.image, Color.BLACK2, [0,self.size[1]-1], [self.size[0],self.size[1]-1], self.width)  #DOWN
            if not self.border[2]: pygame.draw.line(self.image, Color.BLACK2, [0,0], [0,self.size[1]], self.width)  #LEFT
            if not self.border[3]: pygame.draw.line(self.image, Color.BLACK2, [self.size[0],0], [self.size[0],self.size[1]], self.width)  #RIGHT
        
        self.updating = False
        
    def mouseDetect(self):
        self.mouseType = 0
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.mouseType += 1
            self.mouseType += 1
            self.prevMouseType = self.mouseType
            self.updating = True
        if self.mouseType == 0 and self.prevMouseType != 0:
            self.updating = True
            self.prevMouseType = 0
        return self.mouseType
   
class KakuroClues(pygame.sprite.Sprite):
    def __init__(self, textD, textR, pos, 
                        size=dt(223,38), 
                        bg_color=Color.WHITE, 
                        f_color=font_color["Black2None"], 
                        f_typo = font_typo["Comfortaa"]["Small"],
                        id=None):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.bgcolor = bg_color
        self.textD = textD
        self.textR = textR
        self.pos = pos
        self.size = size
        self.f_color = f_color
        self.f_typo = f_typo
        
        self.id = id
        
        self.updating = True
        self.static = True

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.update()
        
    def _game_display_textR(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.topright = self.image.get_rect().topright
        self.textRect.right -= 3
        self.textRect.top += 3
        self.image.blit(self.textSurf, self.textRect)
        
    def _game_display_textD(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.bottomleft = self.image.get_rect().bottomleft
        self.textRect.left += 3
        self.textRect.bottom -= 3
        self.image.blit(self.textSurf, self.textRect)
        
    def set_Text(self, text):
        self.text = text
        self.updating = True
        
    
    def update(self):
        pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])
        self._game_display_textD(self.textD)
        self._game_display_textR(self.textR)
        pygame.draw.line(self.image, Color.LIGHTLIGHTGRAY, (0,0), (self.size[0], self.size[1]), 3)
        pygame.draw.rect(self.image, Color.LIGHTLIGHTGRAY, [0, 0, self.size[0]*0.975, self.size[1]*0.975], 2)
        self.updating = False
    

class CryptogramCell(pygame.sprite.Sprite):
    def __init__(self, text, crptext, anstext, pos, 
                        size=dt(50,50), 
                        bg_color=[Color.WHITE, Color.LIGHTLIGHTGRAY, Color.YELLOW], 
                        bd_color=Color.BLACK,
                        bd_width=2,
                        f_color=font_color["Black2None"], 
                        f_typo = font_typo["Comfortaa"]["Regular"],
                        id = None):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.bgcolor = bg_color
        self.bdcolor = bd_color
        
        self.text = text
        self.crptext = crptext
        self.anstext = anstext
        
        self.pos = pos
        self.size = size
        self.f_color = f_color
        self.f_typo = f_typo
        
        self.prevMouseType = 0
        self.mouseType = 0 #0 Off 1 Hover 2 Click
        
        self.ready = False
        
        self.width = bd_width
        
        self.static = False
        self.updating = True
        
        self.id = id

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.center = self.rect.center
        
        self.update()
        
    def game_display_text(self):
        self.textSurf, self.textRect = textdisplay(self.text, self.f_color, self.f_typo)
        self.textRect.center = self.image.get_rect().center
        self.textRect.y = self.image.get_rect().height//8
        self.textRect.height = self.image.get_rect().height // 2
        
        self.image.blit(self.textSurf, self.textRect)
        
        self.textSurf2, self.textRect2 = textdisplay(self.crptext, font_color["GrayNone"], font_typo["Comfortaa"]["Small"])
        self.textRect2.center = self.image.get_rect().center
        self.textRect2.y = self.image.get_rect().height // 2
        self.textRect2.height = self.image.get_rect().height // 2
        
        self.image.blit(self.textSurf, self.textRect)
        
        self.image.blit(self.textSurf2, self.textRect2)
        
    def setText(self, text, color="BlueNone"):
        self.text = text
        self.f_color = font_color[color]
        self.update()
    
    def update(self):
        if not self.ready:
            pygame.draw.rect(self.image, self.bgcolor[self.mouseType], [0, 0, self.size[0], self.size[1]])
        else:
            pygame.draw.rect(self.image, self.bgcolor[2], [0, 0, self.size[0], self.size[1]])
        pygame.draw.rect(self.image, self.bdcolor, [0, 0, self.size[0]-1, self.size[1]-1],self.width)
        self.game_display_text()
        
        pygame.draw.rect(self.image, Color.BLACK2,  [0, 0, self.size[0]*0.975, self.size[1]//2],1)
        
        self.updating = False
        
    def mouseDetect(self):
        self.mouseType = 0
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True
            self.mouseType += 1
            self.prevMouseType = self.mouseType
            self.updating = True
        if self.mouseType == 0 and self.prevMouseType != 0:
            self.updating = True
            self.prevMouseType = 0
        return 0


class TextBorderID(pygame.sprite.Sprite):
    def __init__(self, text, pos, 
                        size=dt(50,50), 
                        bg_color=Color.WHITE, 
                        bd_color=Color.BLACK2,
                        bd_width=2,
                        f_color=font_color["Black2None"], 
                        f_typo = font_typo["Comfortaa"]["Regular"],
                        id = None,
                        container_id = ''):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.bgcolor = bg_color
        self.bdcolor = bd_color
        self.text = text
        self.pos = pos
        self.size = size
        self.f_color = f_color
        self.f_typo = f_typo
        self.containerID = container_id
        
        self.prevMouseType = 0
        self.mouseType = 0 #0 Off 1 Hover 2 Click
        
        self.hoverColor = Color.LIGHTGRAY
        self.clickColor = Color.GREEN
        self.selectedColor = Color.YELLOW
        
        self.width = bd_width
        
        self.ready = False
        
        self.updating = True
        self.static = False
        
        self.id = id

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.center = self.rect.center
        
        self.update()
        
    def game_display_text(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.textSurf, self.textRect)
        
    def game_display_text_ID(self, text):
        self.textSurf, self.textRect = textdisplay(text, font_color["GrayNone"], font_typo["Open Sans"]["XSmall"])
        parent = self.image.get_rect()
        self.textRect.x = parent.x + parent.width * 0.1
        self.textRect.y = parent.y + parent.height * 0.1
        self.textRect.width = parent.width * 0.25
        self.textRect.height = parent.height * 0.25
        self.image.blit(self.textSurf, self.textRect)
        
    def setID(self, ID):
        self.containerID = ID
        self.update()
        
    def setContent(self, text, color ="BlueNone", force=False):
        if self.ready or force:
            self.text = text
            self.f_color = font_color[color]
            self.update()
    
    def update(self):
        if self.ready:
            pygame.draw.rect(self.image, self.selectedColor, [0, 0, self.size[0], self.size[1]])
            
        elif self.mouseType == 1:
            pygame.draw.rect(self.image, self.hoverColor, [0, 0, self.size[0], self.size[1]])
            
        elif self.mouseType == 2:
            pygame.draw.rect(self.image, self.clickColor, [0, 0, self.size[0], self.size[1]])
            
        else:
            pygame.draw.rect(self.image, self.bgcolor, [0, 0, self.size[0], self.size[1]])
            
        
        pygame.draw.rect(self.image, self.bdcolor, [0, 0, self.size[0]*0.95, self.size[1]*0.95],self.width)
        self.game_display_text(self.text)
        self.game_display_text_ID(self.containerID)
        self.updating = False
        
    def mouseDetect(self):
        self.mouseType = 0
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.mouseType += 1
                return True
            self.mouseType += 1
            self.prevMouseType = self.mouseType
            self.updating = True
        if self.mouseType == 0 and self.prevMouseType != 0:
            self.updating = True
            self.prevMouseType = 0
        return False
    
class TextBorderKakuro(pygame.sprite.Sprite):
    def __init__(self, text, pos, 
                        size=dt(50,50), 
                        bg_color=[Color.WHITE, Color.LIGHTLIGHTGRAY, Color.YELLOW, Color.RED, Color.BLUE], 
                        bd_color=Color.BLACK2,
                        bd_width=2,
                        f_color=font_color["Black2None"], 
                        f_typo = font_typo["Comfortaa"]["Regular"],
                        id = None,
                        container_id = ''):
        
        super().__init__()
        
        self.image = pygame.Surface(size)
        self.image.set_colorkey(Color.BLACK)
        
        self.bgcolor = bg_color
        self.bdcolor = bd_color
        self.text = text
        self.pos = pos
        self.size = size
        self.f_color = f_color
        self.f_typo = f_typo
        self.containerID = container_id
        
        self.prevMouseType = 0
        self.mouseType = 0 #0 Off 1 Hover 2 Click
        
        self.width = bd_width
        
        self.curColor = 0
        self.curMode = 1
        
        self.lastTick = pygame.time.get_ticks()
        
        self.ready = False
        
        self.updating = True
        self.static = False
        
        self.id = id
        
        self.significant = False

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.center = self.rect.center
        
        self.update()
        
    def game_display_text(self, text):
        self.textSurf, self.textRect = textdisplay(text, self.f_color, self.f_typo)
        self.textRect.center = self.image.get_rect().center
        self.image.blit(self.textSurf, self.textRect)
        
    def game_display_text_ID(self, text):
        self.textSurf, self.textRect = textdisplay(text, font_color["GrayNone"], font_typo["Open Sans"]["XSmall"])
        parent = self.image.get_rect()
        self.textRect.x = parent.x + parent.width * 0.1
        self.textRect.y = parent.y + parent.height * 0.1
        self.textRect.width = parent.width * 0.25
        self.textRect.height = parent.height * 0.25
        self.image.blit(self.textSurf, self.textRect)
        
    def setID(self, ID):
        self.containerID = ID
        self.update()
        
    def setMode(self, mode):
        self.curMode = mode
        self.lastTick = pygame.time.get_ticks()
        self.updating = True
        self.update()
        
    def setContent(self, text, color ="BlueNone", force=False):
        if self.ready or force:
            self.text = text
            self.f_color = font_color[color]
            self.update()
    
    def _colorFadeUtil(self, value):
        return value*255
    
    def update(self):        
        
        pygame.draw.rect(self.image, self.bgcolor[self.mouseType], [0, 0, self.size[0], self.size[1]])

        if self.curMode < 1:
            x = int(self._colorFadeUtil(self.curMode))
            pygame.draw.rect(self.image, (self.bgcolor[3][0] | x, self.bgcolor[3][1] | x, self.bgcolor[3][2] | x), [0, 0, self.size[0], self.size[1]])
        
        if self.curMode < 1:
            if self.lastTick + 1000/Screen.FPS < pygame.time.get_ticks():
                self.curMode +=  1 / 6
                self.curMode = min(self.curMode, 1)
                self.lastTick = pygame.time.get_ticks()
        
        if self.significant:
            x = self.size[0]
            y = self.size[1]
            #draw_bordered_rounded_rect(self.image, self.rect, Color.LIGHTLIGHTLIGHTGRAY, Color.LIGHTLIGHTLIGHTGRAY, int(self.size[1]*0.4), 2)
            pygame.draw.ellipse(self.image, Color.LIGHTLIGHTLIGHTGRAY, [int(x*0.05),int(y*0.05),int(x*0.90),int(y*0.90)])
            
        pygame.draw.rect(self.image, self.bdcolor, [0, 0, self.size[0]*0.975, self.size[1]*0.975],self.width)
        
        if self.ready:
            pygame.draw.rect(self.image, self.bgcolor[4], [0, 0, self.size[0]*0.975, self.size[1]*0.975], self.width*2)
        
            
        self.game_display_text(self.text)
        self.game_display_text_ID(self.containerID)
        
        if self.curMode == 1:
            self.updating = False
        
    def mouseDetect(self):
        self.mouseType = 0
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.mouseType += 1
                return True
            self.mouseType += 1
            self.prevMouseType = self.mouseType
            self.updating = True
        if self.mouseType == 0 and self.prevMouseType != 0:
            self.updating = True
            self.prevMouseType = 0
        return False
        





class RoundRectangleCopy(pygame.sprite.Sprite):
    def __init__(self, start, end, color, width, **options):
        self.__dict__.update(options)
        self.start = start
        self.end = end
        self.color=color
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the blob, and its x and y position, width and height
        # Set the background color and make it transparent
        self.width = width

        # Draw the path
        self.redraw()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (self.start[0]-self.width//2+self.ix,
                                    self.start[1]-self.width//2+self.iy)
        if self.inversed:
            self.rect.y-=(math.ceil(self.image.get_rect()[3]/2)-self.iy)

    def redraw(self):
        dis, angle = Pol(self.end[0]-self.start[0], self.end[1]-self.start[1])
        dis += self.width
        _image = pygame.Surface([dis, self.width])
        _image.fill([255, 255, 255])
        _image.set_colorkey([255, 255, 255])
        '''pygame.draw.rect(_image, self.color, pygame.Rect(0, 0, dis, self.width), 3, \
                         border_radius=-1, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1)'''
        draw_bordered_rounded_rect(_image, pygame.Rect(0, 0, dis, self.width), Color.WHITE, Color.BLACK,  self.width//3, 2)
        nangle = (180-angle)%360
        self.inversed = nangle>=180
        self.image = pygame.transform.rotate(_image, nangle)
        i1 = _image.get_rect()
        i2 = self.image.get_rect()
        ix = i2[2]-i1[2]
        iy = i2[3]-i1[2]
        self.ix = ix//2
        self.iy = iy//2

class RoundRectangle(pygame.sprite.Sprite):
    def __init__(self, start, end, color, width, **options):
        self.__dict__.update(options)
        self.start = start
        self.end = end
        self.color=color
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the blob, and its x and y position, width and height
        # Set the background color and make it transparent
        self.width = width

        # Draw the path
        self.redraw()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        if self.iy==0:
            self.rect.x, self.rect.y = (self.start[0]-self.width//2+self.ix,
                                        self.start[1])
        elif self.angle != 0 and self.angle != 90:
            self.rect.x, self.rect.y = (self.start[0]-int(self.width*0.75)+self.ix,
                                        self.start[1]-int(self.width*0.75))
        else:
            self.rect.x, self.rect.y = (self.start[0]-self.width//2+self.ix,
                                        self.start[1]-self.width//2)
        #print(self.rect.y, self.start[1], self.width//2 ,self.iy)
        if self.inversed:
            self.rect.y-=(math.ceil(self.image.get_rect()[3]/2)-self.iy)

    def redraw(self):
        #Took the distance and angle, which works fine
        dis, angle = Pol(self.end[0]-self.start[0], self.end[1]-self.start[1])
        #print(angle)
        self.angle = int(angle)
        
        #Added to accomodate the given width of the line
        dis += self.width
        
        #Created the surface where the rectangle will be drawn
        _image = pygame.Surface([dis, self.width])
        _image.fill([255, 255, 255])
        _image.set_colorkey([255, 255, 255])
        
        '''pygame.draw.rect(_image, self.color, pygame.Rect(0, 0, dis, self.width), 3, \
                         border_radius=-1, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1)'''
        
        #drawn the rectangle
        draw_bordered_rounded_rect(_image, pygame.Rect(0, 0, dis, self.width), Color.WHITE, Color.BLACK,  int(self.width/2.5), 2)
        
        #Actually, I have no problem with the angle, it works just fune
        nangle = (180-angle)%360
        self.inversed = nangle>=180
        
        #This is the actual final product, a rotated rectangle
        self.image = pygame.transform.rotate(_image, nangle)
        
        # 0 1   2     3
        # x y width height
        #Gets the rect of rect surface
        i1 = _image.get_rect()
        
        #Gets the rect of main surface
        i2 = self.image.get_rect()
        
        
        ix = i2[0]-i1[0]
        iy = i2[3]-i1[3]
        self.ix = ix//2
        self.iy = iy//2
        