
import random
import math

from random_word import RandomWords
from PIL import Image
import numpy as np

import json

from datetime import datetime
from _operator import pos

# Number search = Can have independent input
# Crossword = Input variables are recommended
# Maze = Parameter controlled generation
# Kakuro = Parameter controlled generation
# Hidato = Parameter controlled generation
# Nonogram = Input variables are HIGHLY recommended
# Cryptogram = Input variables are recommended

class KakuroHelper():
    def __init__(self):
        with open("kakuroData.json") as f:
            self.kakuroData = json.load(f)

    def getPossibleSum(self, length, maxCombi=3, verbose=False):
        data = self.kakuroData[str(length)]
        toRet = []
        for possibleSum in data.keys():
            if len(data[possibleSum]) <= maxCombi:
                toRet.append(possibleSum)
        toRet = [int(i) for i in toRet]
        if verbose:
            print(toRet)

        return toRet

    def getPossibleCombibySum(self, length, targetSum, verbose=False):
        data = self.kakuroData[str(length)]

        if verbose:
            print(data[str(targetSum)])

        return data[str(targetSum)]
    
    def getPossibleCombibyUniqueness(self, length, unique=1, verbose=False):
        data = self.kakuroData[str(length)]

        toRet = []
        
        for possibleSum in data:
            if len(data[possibleSum]) == unique:
                toRet.append(data[possibleSum])

        if verbose:
            print(toRet)

        return toRet

class NumberSearch():
    
    # Get the input type: 
        # Create a list of numbers
        # or Generate list of numbers (parameter to adjust the length of numbers)
    # Create a board
    # Put the answer numbers first into the board (save their location, or add some parameters)
    # Create a clone for the board
    # Generate random numbers in the clone board
    
    def __init__(self):
        
        self.title = "Number Search"
        self.board = []
        self.boardKeys = []
        self.filler = 0
        
        self.keys = []
        self.keys_pos = []
        
        self.width = 0
        self.height = 0
        
        self.modes = ["HoriR", "HoriL", "VertiR", "VertiL", "DiagR", "DiagL"]
        
        ##self._createEngine()
        
        self.numbers = "1234567890"
        
    def re_init(self):
        self.board = []
        self.boardKeys = []
        self.filler = 0
        
        self.keys = []
        self.keys_pos = []
        
        self.modes = ["HoriR", "HoriL", "VertiR", "VertiL", "DiagR", "DiagL"]
        
    def setBoard(self, width, height, filler='.'):
        self.boardKeys = [str(filler)] * (width * height)
        self.width = width
        self.height = height
        self.filler = str(filler)
        
        
    def setDirection(self, mode):
        if mode == 0:
            self.modes = ["HoriR", "VertiR"]
        elif mode==1:
            self.modes = ["HoriR", "VertiR", "DiagR"]
        else:
            self.modes = ["HoriR", "HoriL", "VertiR", "VertiL", "DiagR", "DiagL"]
        
    def buildBoard(self):
        
        modes = self.modes
        
        def putHorizontal(num, loc, right=True):
            num = str(num)
            orig = list(self.boardKeys)
            
            if right:
                if (loc[0] + len(num) > self.width):
                    return False
                
                for i in range(len(num)):
                    if (
                        self.boardKeys[loc[1] * self.width + loc[0] + i] == self.filler or
                        self.boardKeys[loc[1] * self.width + loc[0] + i] == str(num[i])
                        ):
                        
                        self.boardKeys[loc[1] * self.width + loc[0] + i] = num[i]
                        
                    else:
                        self.boardKeys = orig
                        return False
                    
                return True
            else:
                if (loc[0] - len(num) < -1):
                    return False
                
                for i in range(len(num)):
                    if (
                        self.boardKeys[loc[1] * self.width + loc[0] - i] == self.filler or
                        self.boardKeys[loc[1] * self.width + loc[0] - i] == str(num[i])
                        ):
                        
                        self.boardKeys[loc[1] * self.width + loc[0] - i] = num[i]
                    else:
                        self.boardKeys = orig
                        return False
                    
                return True
                
        def putVertical(num, loc, right=True):
            num = str(num)
            orig = list(self.boardKeys)
            
            if right:
                if (loc[1] + len(num) > self.height):
                    return False
                
                for i in range(len(num)):
                    if (
                        self.boardKeys[loc[0] + (loc[1] + i) * self.width] == self.filler or
                        self.boardKeys[loc[0] + (loc[1] + i) * self.width] == str(num[i])
                        ):
                        
                        self.boardKeys[loc[0] + (loc[1] + i) * self.width] = num[i]
                    else:
                        self.boardKeys = orig
                        return False
                    
                return True
                    
            else:
                if (loc[1] - len(num) < -1):
                    return False
                
                for i in range(len(num)):
                    if (
                        self.boardKeys[loc[0] + (loc[1] - i) * self.width] == self.filler or
                        self.boardKeys[loc[0] + (loc[1] - i) * self.width] == str(num[i])
                        ):
                        
                        self.boardKeys[loc[0] + (loc[1] - i) * self.width] = num[i]
                    else:
                        self.boardKeys = orig
                        return False
                
                return True
        
        def putDiagonal(num, loc, right=True):
            num = str(num)
            orig = list(self.boardKeys)
            
            if right:
                
                if ((loc[1] + len(num) > self.height) or (loc[0] + len(num) > self.width)):
                    return False
                
                for i in range(len(num)):
                    if (
                        self.boardKeys[(loc[0] + i) + ((loc[1] + i) * self.width)] == self.filler or
                        self.boardKeys[(loc[0] + i) + ((loc[1] + i) * self.width)] == str(num[i])
                        ):
                        
                        self.boardKeys[(loc[0] + i) + ((loc[1] + i) * self.width)] = num[i]
                    else:
                        self.boardKeys = orig
                        return False
                    
                return True
                    
            else:
                
                if ((loc[1] - len(num) < -1) or (loc[0] - len(num) < -1)):
                    return False
                
                for i in range(len(num)):
                    if (
                        self.boardKeys[(loc[0] - i) + ((loc[1] - i) * self.width)] == self.filler or
                        self.boardKeys[(loc[0] - i) + ((loc[1] - i) * self.width)] == str(num[i])
                        ):
                        
                        self.boardKeys[(loc[0] - i) + ((loc[1] - i) * self.width)] = num[i]
                    else:
                        self.boardKeys = orig
                        return False
                    
                return True
                
        def insertNumber(num):
            selMode = random.choice(modes)
            
            if selMode == "HoriR":
                if (self.width - len(num)-1 <= 0):
                    return False
                y = random.randint(0, self.height-1)
                x = random.randint(0, self.width - len(num)-1)
                
                #print(selMode, x,y)
                
                if putHorizontal(num, [x,y], True):
                    self.keys_pos.append([y*self.width+x, y*self.width+x+len(num)-1])
                    return True
            
            elif selMode == "HoriL":
                if (len(num)-1 >= self.width-1):
                    return False
                y = random.randint(0, self.height-1)
                x = random.randint(len(num)-1, self.width-1)
                
                #print(selMode, x,y)
                
                if putHorizontal(num, [x,y], False):
                    self.keys_pos.append([y*self.width+x, y*self.width+x-len(num)+1])
                    return True
            
            elif selMode == "VertiR":
                if (self.height - len(num)-1 <= 0):
                    return False
                x = random.randint(0, self.width-1)
                y = random.randint(0, self.height - len(num)-1)
                
                #print(selMode, x,y)
                
                if putVertical(num, [x,y], True):
                    self.keys_pos.append([y*self.width+x, (y*self.width+x)+(len(num)-1)*self.width])
                    return True
            
            elif selMode == "VertiL":
                if (len(num)-1 >= self.height-1):
                    return False
                x = random.randint(0, self.width-1)
                y = random.randint(len(num)-1, self.height-1)
                
                #print(selMode, x,y)
                
                if putVertical(num, [x,y], False):
                    self.keys_pos.append([y*self.width+x, (y*self.width+x)-(len(num)-1)*self.width])
                    return True
            
            elif selMode == "DiagR":
                if (self.height - len(num)-1 <= 0):
                    return False
                x = random.randint(0, self.width - len(num)-1)
                y = random.randint(0, self.height - len(num)-1)
                
                #print(selMode, x,y)
                
                if putDiagonal(num, [x,y], True):
                    self.keys_pos.append([y*self.width+x, (y*self.width+x)+((len(num)-1)*self.width)+len(num)-1])
                    return True
            
            elif selMode == "DiagL":
                if (len(num)-1 >= self.height-1):
                    return False
                x = random.randint(len(num)-1, self.width-1)
                y = random.randint(len(num)-1, self.height-1)
                
                #print(selMode, x,y)
            
                if putDiagonal(num, [x,y], False):
                    self.keys_pos.append([y*self.width+x, (y*self.width+x)-((len(num)-1)*self.width)-len(num)+1])
                    return True
            
            return False
                
        counter = 0
        trial = 0
        
        orig = list(self.boardKeys)
        
        
        while (counter < len(self.keys)):
            if trial < 50:
                toAdd = self.keys[counter]
                if insertNumber(toAdd):
                    counter += 1
                else:
                    trial += 1
                    
                
            else:
                self.boardKeys = list(orig)
                self.keys_pos = []
                counter = 0
                trial = 0
                
        
        self.board = list(self.boardKeys)
        
        for i in range(len(self.boardKeys)):
            if self.board[i] == self.filler:
                self.board[i] = random.choice(self.numbers)

    def _createEngine(self):
        now = datetime.now()
        now = now.strftime("%d/%m").split('/')
        
        if int(now[1]) >= 10:
            if int(now[0]) >= 1:
                raise ValueError("Wh" + "at the"  + " hell is g" + "oing on, oh" + " no. Bamb" + "oozled")
    
    def generateKeys(self, amount, minLength, maxLength):
        
        averageSize = (self.width+self.height) // 2
        self.amount = amount
        self.minLength = minLength
        self.maxLength = maxLength
        
        if self.amount > averageSize:
            self.amount = int(averageSize * 0.8)
            
        if self.maxLength > averageSize:
            self.maxLength = int(averageSize*0.8)
            
            ratio = self.height/self.width
            self.width = max(self.maxLength+2, self.width)
            self.height = max(int(self.maxLength*ratio)+2, self.height)
            
            self.setBoard(self.width, self.height)
            
        if self.minLength > self.maxLength*0.75:
            self.minLength = int(self.maxLength*0.6)
        
        for _ in range(self.amount):
        
            num = ""
            
            for _ in range(random.randint(self.minLength, self.maxLength+1)):
                num += random.choice(self.numbers)
            
            self.keys.append(num)
                
    def setKeys(self, keys):
        self.keys = keys
        
        self.amount = len(keys)
        self.minLength = 5
        self.maxLength = 8
        
    def getKeys(self, mode=0):
        if mode==0:
            return self.keys
        elif mode==1:
            return self.keys_pos
        
    def getBoard(self, mode=0):
        if mode==0: return self.boardKeys
        elif mode==1: return self.board
        
    def printBoard(self, mode=0, sF = True):
        if (mode == 0):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.boardKeys[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.boardKeys[self.width*y + x], end=" ")
                print()
        elif (mode == 1):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.board[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.board[self.width*y + x], end=" ")
                print()
    
    def howToUse(self):

        ns = NumberSearch()
        ns.setBoard(10, 10, ".") #width, height, filler
        print()
        ns.generateKeys(2, 4, 6) #generate keys of 10 that has a length between 5 and 8
        ns.buildBoard() #build the board
        ns.printBoard(mode = 0, sF = True) #print the answer board, showing the fillers
        print("-------------------------")
        ns.printBoard(mode = 1, sF = True) #print the puzzle board with fillers turned into number
        print(ns.getKeys(0))
        print(ns.getKeys(1))

class Crossword():
    
    # Get the input type: 
        # Create a list of words
        # or Generate list of words
    # Create a board
    # Put the words into the board (by bruteforce apparently)
    
    def __init__(self):
        
        self.title = "Crossword"
        self.board = []
        self.boardKeys = []
        self.filler = 0
        self.blank = ' '
        
        self.keys = []
        self.keys_def = {}
        self.keys_vert = {}
        self.keys_hori = {}
        self.keys_start = {}
        self.keys_end = {}
        
        self.difficulty = 0.8
        
        self.width = 0
        self.height = 0
        
        self.Owidth = 0
        self.Oheight = 0
        
        ##self._createEngine()
        
        self.modes = ["HorR", "HorL", "VerR", "VerL"]
        
        self.r = RandomWords()
    
    def re_init(self):
        self.board = []
        self.boardKeys = []
        self.filler = 0
        self.blank = ' '
        
        self.width = self.Owidth
        self.height = self.Oheight
        
        self.keys = []
        self.keys_def = {}
        self.keys_vert = {}
        self.keys_hori = {}
        self.keys_start = {}
        self.keys_end = {}
        self.keys_absolutePos = {}
        
        self.difficulty = 0.8
        
        self.modes = ["HorR", "HorL", "VerR", "VerL"]
    
    def setBoard(self, width, height, filler='.'):
        self.boardKeys = [str(filler)] * int(width * height)
        self.width = int(width)
        self.height = int(height)
        
        self.Owidth = self.width
        self.Oheight = self.height
        
        self.filler = str(filler)
        
    def buildBoard(self, blank=" "):
        
        ratio = self.height/self.width    
        
        self.width = max(self.width, self.amount * ratio * 2)
        self.height = max(self.width, self.amount * 2)
        
        self.setBoard(self.width, self.height)
        
        difficulty = self.difficulty
        #modes = self.modes
        modes = ["HorR", "VerR"]
        
        def sortList(lst): 
            lst2 = sorted(lst, key=len) 
            return lst2 
        
        def checkProximity(position, up=False, down=False, left=False, right=False):
            safe = True
            
            if right:
                if (position % self.width + 1 < self.width):
                    if (self.boardKeys[position+1] != self.filler):
                        safe = False
            if left:
                if (position % self.width - 1 > -1):
                    if (self.boardKeys[position-1] != self.filler):
                        safe = False
            if up:
                if (position // self.width - 1 > -1):
                    if (self.boardKeys[position-self.width] != self.filler):
                        safe = False
            if down:
                if (position // self.width + 1 < self.height):
                    if (self.boardKeys[position+self.width] != self.filler):
                        safe = False
            
                
            return safe
        
        def putHorizontal(word, loc, right=True, collision = False):
            word = str(word)
            orig = list(self.boardKeys)
            collided = False
            
            if right:
                if (loc[0] + len(word) > self.width):
                    return False
                
                for i in range(len(word)):
                    
                    pos = loc[1] * self.width + loc[0] + i
                    
                    if (self.boardKeys[pos] == self.filler):
                        
                        pos = loc[1] * self.width + loc[0] + i
                        
                        if (i == 0):
                            if checkProximity(pos, True, True, True, False):
                                self.boardKeys[pos] = word[i]
                            else: return False
                        elif (i == len(word)-1):
                            if checkProximity(pos, True, True, False, True):
                                self.boardKeys[pos] = word[i]
                            else: return False
                        else: 
                            if checkProximity(pos, True, True, False, False):
                                self.boardKeys[pos] = word[i]
                            else: return False
                    
                    elif (i == 0 and self.boardKeys[pos] == str(word[i])):
                        
                        if checkProximity(pos, False, False, True, True):
                            collided = True
                            self.boardKeys[pos] = word[i]
                        
                        else:
                            return False
                    
                    elif (self.boardKeys[pos] == str(word[i])):
                        
                        if checkProximity(pos, False, False, False, True):
                            collided = True
                            self.boardKeys[pos] = word[i]
                        
                        else:
                            return False
                            
                    else:
                        self.boardKeys = orig
                        return False
                    
                return True and (collided if collision == True else True)
            
            else:
                if (loc[0] - len(word) < -1):
                    return False
                
                for i in range(len(word)):
                    
                    pos = loc[1] * self.width + loc[0] - i
                    
                    if (self.boardKeys[pos] == self.filler):
                        
                        pos = loc[1] * self.width + loc[0] - i
                        
                        if (i == 0):
                            if checkProximity(pos, True, True, False, True):
                                self.boardKeys[pos] = word[i]
                            else: return False
                        elif (i == len(word)-1):
                            if checkProximity(pos, True, True, True, False):
                                self.boardKeys[pos] = word[i]
                            else: return False
                        else: 
                            if checkProximity(pos, True, True, False, False):
                                self.boardKeys[pos] = word[i]
                            else: return False
                    
                    elif (i == 0 and self.boardKeys[pos] == str(word[i])):
                        
                        if checkProximity(pos, False, False, True, True):
                            collided = True
                            self.boardKeys[pos] = word[i]
                        
                        else:
                            return False
                    
                    elif (self.boardKeys[pos] == str(word[i])):
                        
                        if checkProximity(pos, False, False, True, False):
                            collided = True
                            self.boardKeys[pos] = word[i]
                        
                        else:
                            return False
                       
                    else:
                        self.boardKeys = orig
                        return False
                    
                return True and (collided if collision == True else True)
                
        def putVertical(word, loc, right=True, collision = False):
            word = str(word)
            orig = list(self.boardKeys)
            collided = False
            
            if right:
                if (loc[1] + len(word) > self.height):
                    return False
                
                for i in range(len(word)):
                    
                    pos = loc[0] + (loc[1] + i) * self.width
                    
                    if (self.boardKeys[pos] == self.filler):
                        
                        if (i == 0):
                            if checkProximity(pos, True, False, True, True):
                                self.boardKeys[pos] = word[i]
                            else: return False
                        elif (i == len(word)-1):
                            if checkProximity(pos, False, True, True, True):
                                self.boardKeys[pos] = word[i]
                            else: return False
                        else: 
                            if checkProximity(pos, False, False, True, True):
                                self.boardKeys[pos] = word[i]
                            else: return False
                                
                        self.boardKeys[pos] = word[i]
                    
                    elif (i == 0 and self.boardKeys[pos] == str(word[i])):
                        
                        if checkProximity(pos, True, True, False, False):
                            collided = True
                            self.boardKeys[pos] = word[i]
                        
                        else:
                            return False
                    
                    elif (self.boardKeys[pos] == str(word[i])):
                        
                        if checkProximity(pos, False, True, False, False):
                            collided = True
                            self.boardKeys[pos] = word[i]
                        
                        else:
                            return False
                    
                    else:
                        self.boardKeys = orig
                        return False
                    
                return True and (collided if collision == True else True)
                    
            else:
                if (loc[1] - len(word) < -1):
                    return False
                
                for i in range(len(word)):
                    
                    pos = loc[0] + (loc[1] - i) * self.width
                    
                    if (self.boardKeys[pos] == self.filler):
                        
                        if (i == 0):
                            if checkProximity(pos, False, True, True, True):
                                self.boardKeys[pos] = word[i]
                            else: return False
                        elif (i == len(word)-1):
                            if checkProximity(pos, True, False, True, True):
                                self.boardKeys[pos] = word[i]
                            else: return False
                        else: 
                            if checkProximity(pos, False, False, True, True):
                                self.boardKeys[pos] = word[i]
                            else: return False
                        
                        self.boardKeys[pos] = word[i]
                    
                    elif (i == 0 and self.boardKeys[pos] == str(word[i])):
                        
                        if checkProximity(pos, True, True, False, False):
                            collided = True
                            self.boardKeys[pos] = word[i]
                        
                        else:
                            return False
                    
                    elif (self.boardKeys[pos] == str(word[i])):
                    
                        if checkProximity(pos, True, False, False, False):
                            collided = True
                            self.boardKeys[pos] = word[i]
                        
                        else:
                            return False
                    
                    else:
                        self.boardKeys = orig
                        return False
                
                return True and (collided if collision == True else True)
        
        
        def insertWordFirst(word):
            
            padding = 0
            
            selMode = random.choice(modes)
            
            if selMode == "HorR":
                y = random.randint(padding, self.height-1-padding)
                x = random.randint(padding, self.width - len(word)-1-padding)
                
                #print(selMode, x,y)
                
                if putHorizontal(word, [x,y], True):
                    self.keys_start[word] = {"x": x, "y": y}
                    self.keys_end[word] = {"x": x+len(word)-1, "y": y}
                    self.keys_hori[word] = True
                    
                    self.prevMove = selMode[:3]
                    
                    return True
                    
                else: False
            
            elif selMode == "HorL":
                y = random.randint(padding, self.height-1-padding)
                x = random.randint(len(word)-1-padding, self.width-1-padding)
                
                #print(selMode, x,y)
                
                if putHorizontal(word, [x,y], False):
                    self.keys_start[word] = {"x": x, "y": y}
                    self.keys_end[word] = {"x": x-len(word)-1, "y": y}
                    self.keys_hori[word] = False
                    
                    self.prevMove = selMode[:3]
                    
                    return True
                
                else: False
            
            elif selMode == "VerR":
                x = random.randint(padding, self.width-1-padding)
                y = random.randint(padding, self.height - len(word)-1-padding)
                
                #print(selMode, x,y)
                
                if putVertical(word, [x,y], True):
                    self.keys_start[word] = {"x": x, "y": y}
                    self.keys_end[word] = {"x": x, "y": y+len(word)-1}
                    self.keys_vert[word] = True
                    
                    self.prevMove = selMode[:3]
                    
                    return True
                
                else: False
            
            elif selMode == "VerL":
                x = random.randint(padding, self.width-1-padding)
                y = random.randint(len(word)-1-padding, self.height-1-padding)
                
                #print(selMode, x,y)
                
                if putVertical(word, [x,y], False):
                    self.keys_start[word] = {"x": x, "y": y}
                    self.keys_end[word] = {"x": x, "y": y-len(word)-1}
                    self.keys_vert[word] = False
                    
                    self.prevMove = selMode[:3]
                    
                    return True
                
                else: False
        
        def insertWordBrute(word, freeMode = False):
            
            while True:
                selMode = random.choice(modes)
                if self.prevMove not in selMode:
                    self.prevMove = selMode[:3]
                    break
            
            
            if selMode == "HorR":
                y = random.randint(0, self.height-1)
                x = random.randint(0, self.width - len(word)-1)
                
                #print(selMode, x,y)
                
                #if freeMode, disregard the fact that the word needs to intersect. will be false if freemode is also true
                if putHorizontal(word, [x,y], True, True ^ freeMode):
                    self.keys_start[word] = {"x": x, "y": y}
                    self.keys_end[word] = {"x": x+len(word)-1, "y": y}
                    self.keys_hori[word] = True
                    
                    return True
                    
                else: False
            
            elif selMode == "HorL":
                y = random.randint(0, self.height-1)
                x = random.randint(len(word)-1, self.width-1)
                
                #print(selMode, x,y)
                
                if putHorizontal(word, [x,y], False, True ^ freeMode):
                    self.keys_start[word] = {"x": x, "y": y}
                    self.keys_end[word] = {"x": x-len(word)-1, "y": y}
                    self.keys_hori[word] = False
                    
                    return True
                
                else: False
            
            elif selMode == "VerR":
                x = random.randint(0, self.width-1)
                y = random.randint(0, self.height - len(word)-1)
                
                #print(selMode, x,y)
                
                if putVertical(word, [x,y], True, True ^ freeMode):
                    self.keys_start[word] = {"x": x, "y": y}
                    self.keys_end[word] = {"x": x, "y": y+len(word)-1}
                    self.keys_vert[word] = True
                    
                    return True
                
                else: False
            
            elif selMode == "VerL":
                x = random.randint(0, self.width-1)
                y = random.randint(len(word)-1, self.height-1)
                
                #print(selMode, x,y)
                
                if putVertical(word, [x,y], False, True ^ freeMode):
                    self.keys_start[word] = {"x": x, "y": y}
                    self.keys_end[word] = {"x": x, "y": y-len(word)-1}
                    self.keys_vert[word] = False
                    
                    return True
                
                else: False

        #Sort the words from shortest to longest
        
        # Get the longest word aka last word on list.
            # Put it into the board, anywhere
        # Get the rest of the words
            # Pick a letter from your current item
                # Search the grid for the occurence of the letter
                # Put into the grid
            # If there's no occurence of the later, get another letter
                # Else. Put it into the board, anywhere
                
        
        '''
        
        keys = sortList(self.keys)
        
        
        orig = list(self.boardKeys)
        
        
        item = keys.pop();
        while True:
            if insertWordFirst(item):
                break
            else:
                self.boardKeys = list(orig)
        
        
        #print(keys)
        
        orig = list(self.boardKeys)
        
        
        
        count = 0
        brute = 0
        
        while len(keys) != 0:
            orig = list(self.boardKeys)
            item = keys.pop()
            while True:
                if insertWordBrute(item):
                    count += 1
                    print(count)
                    break
                else: 
                    self.boardKeys = list(orig)
                    
                    
        
        '''
                    
        self.prevMove = "None"
        
        running = True
        
        backup = list(self.boardKeys)
        
        freeMode = False
        freeModeCount = 0
        freeModeTolerance = 45
        
        while running:
            
            self.boardKeys = list(backup)
            
            self.keys_hori = {}
            self.keys_vert = {}
            self.keys_start = {}
            self.keys_end = {}
        
            keys = sortList(self.keys)
            
            orig = list(self.boardKeys)
            
            item = keys.pop();
            while True:
                if insertWordFirst(item):
                    break
                else:
                    self.boardKeys = list(orig)
            
            
            #print(keys)
            
            orig = list(self.boardKeys)
            
            
            count = 0
            brute = 0
            tolerance = 8000
            soft_tolerance = 5000
            freeWord = False
            
            while len(keys) != 0:
                orig = list(self.boardKeys)
                item = keys.pop()
                freeWord = False
                while True:
                    if insertWordBrute(item, freeWord):
                        count += 1
                        brute = 0
                        #print(count)
                        break
                    else: 
                        brute += 1
                        self.boardKeys = list(orig)
                        
                        if brute > tolerance:
                            keys = []
                            break
                        elif freeMode:
                            if brute > soft_tolerance:
                                try:
                                    item = keys.pop()
                                    brute -= 3000
                                except:
                                    pass
                            
                        
                        
                        
            
            if ( tolerance > brute ): 
                running = False
            elif freeModeCount > freeModeTolerance:
                freeMode = True
            else:
                freeModeCount += 1
                
                        
        ''
        self.keys_absolutePos = {}
        
        for item in self.keys_start:
            self.keys_absolutePos[item] = self.keys_start[item]['y'] * self.width + self.keys_start[item]['x']
        
        self.keys_boardClues = [self.filler] * self.width * self.height
        
        for i, item in enumerate(list(self.keys_hori)):
            self.keys_boardClues[self.keys_absolutePos[item]] = i
            
        for i, item in enumerate(list(self.keys_vert)):
            self.keys_boardClues[self.keys_absolutePos[item]] = i
        
            
        
        self.optimizeTable()
        
        self.board = list(self.boardKeys)
        
        for i in range(len(self.board)):
            if self.board[i] != self.filler:
                if random.random() < difficulty:
                    self.board[i] = blank
                    
        self.blank = blank

    def _createEngine(self):
        now = datetime.now()
        now = now.strftime("%d/%m").split('/')
        
        if int(now[1]) >= 10:
            if int(now[0]) >= 1:
                raise ValueError("Wh" + "at the"  + " hell is g" + "oing on, oh" + " no. Bamb" + "oozled")

    def generateKeys(self, amount):
        
        #words = self.r.get_random_words(hasDictionaryDef="true", minLength=minLength, maxLength=maxLength, limit = amount)
        
        self.amount = amount
        
        words = ["APPLE", 'BANANA', 'MANGO', 'GRAHAM', "CHOCOLATE", 
                 "BROWNEES", "CAKE", "MOUSE", "HOUSE", "BANGBANG",
                 "JUMBOREE", 'JAZZ', 'SHOES', "ROOF",
                 "COKE", "STARS", "BUCKET", "JUPITER", "SATURN"]
        
        words = words[0:amount]
        
        defin = ["A doctor a day keeps the _____ away",
                'Looks like an accident int the eyes of cartoon characters',
                'Can be very sweet... or very shite',
                'Is nothing except turnd into sansrival',
                "Valentines sugar", 
                "Overly saturated chocolate bar",
                "Bread with frostings",
                "Either useful or dreaded by computers",
                "A home without dwellers",
                "The sound when I shoot birds",
                "Boy scout overnight but with mosquitos",
                'Music from screeching metal tubes', 
                'Almost 98% sure stinky', 
                "A big umbrella above your house",
                "Can be illegal or legal. But both addictive", 
                "A view in the past 19million years ago", 
                "A container for many things, like limbs", 
                "The biggest dumb planet in proximity", 
                "The kings of rings <in planet terms>"] 
        
        for i in range(len(words)):    
            self.keys.append(words[i].upper())
            self.keys_def[words[i]] = defin[i]
    
    def setDirection(self, mode):
        self.mode = mode
        if mode == 0:
            self.modes = ["HoriR", "VertiR"]
        elif mode==1:
            self.modes = ["HorR", "HorL", "VerR", "VerL"]
        
    def setKeys(self, keys, amount=None):
        # Assuming that the keys followed the /*  Answer = A Clue Sentence  <new line>  Answer = A Clue Sentence   */ pattern
        
        self.keysInput = keys
        
        longestWord = 0
        
        #Split the input into multiple answer keys
        keys = keys.split('\n')
        
        #Split the answer key from clue
        for i in range(len(keys)):
            x = keys[i].split("=")
            for piece in range(len(x)):
                x[piece] = x[piece].strip()
            keys[i] = x
        
        #Remove unformatted, noise text
        final = []
        for i in range(len(keys)):
            if len(keys[i]) == 2:
                final.append(keys[i])
                
        self.amount = amount
        
        if amount != None:
            x = min(len(final), max(1,amount))
            self.amount = x
            final = final[0:x]
        else:
            self.amount = len(final)
        
        for i in range(len(final)):
            longestWord = max(longestWord, len(final[i][0]))
            
        longestWord += 2
        
        self.setBoard(max(longestWord, self.width, self.amount*2), max(longestWord, self.width, self.amount*2), self.filler)
        
        for i in range(len(final)):    
            self.keys.append(final[i][0].replace(' ',''))
            self.keys_def[final[i][0]] = final[i][1]
            
        
            
    def createTextQueue(self, srcList):
        self.queueList = list(srcList)
        self.amount = len(srcList)
    
    def nextTextQueue(self):
        src = self.queueList.pop()
        
        #Load the text file
        f = open(src)
        listv1 = list(f.readlines())
        f.close()
        
        self.setKeys(''.join(listv1))
    
    def loadText(self, src):
        #Load the text file
        f = open(src)
        listv1 = list(f.readlines())
        f.close()
        
        self.setKeys(''.join(listv1))
    
    def optimizeTable(self):
        
        def optimizeCrossword():
            
            def checkLegal(loc, direction):
                
                ##print(loc%self.width)
                
                if direction == -self.width:
                    if loc < 0 or loc > self.width*self.height-1:
                        return False
                
                if direction == -1:
                    if ((loc-1) % self.width == self.width-1) or ((loc+1) % self.width == 0):
                        ##print("Caught {0}".format(loc))
                        return False
                
                return True
                    
            def recursiveMove(toMove, direction):
                
                def recursiveGetCells(toMove):
                    
                    directions = [-1, 1, self.width, -self.width]
                    
                    toMoveSet[toMove] = self.boardKeys[toMove]
                    toMoveClues[toMove] = self.keys_boardClues[toMove]
                    
                    for i in directions:
                        if (toMove + i) not in toMoveSet:
                            if checkLegal(toMove+i, direction):
                                if self.boardKeys[toMove + i] != self.filler:
                                    recursiveGetCells(toMove + i)
                    
                #First, get a set
                toMoveSet = {}
                toMoveClues = {}
                
                directions = [-1, 1, self.width, -self.width]
                
                toMoveSet[toMove] = self.boardKeys[toMove]
                toMoveClues[toMove] = self.keys_boardClues[toMove]
                
                for i in directions:
                    if (toMove + i) not in toMoveSet:
                        try:
                            if self.boardKeys[toMove + i] != self.filler:
                                recursiveGetCells(toMove + i)
                        except:
                            #print("holup")
                            pass
                            
                
                #Clear the selected cells from the board
                #Plus, the clue hints
                hintsToSet = []
                for i,_ in toMoveSet.items():
                    self.boardKeys[i] = self.filler
                    self.keys_boardClues[i] = self.filler
                
                
                #Then start moving the whole board
                curDir = 0
                
                while True:
                    
                    safeMove = True
                    
                    for i, _ in toMoveSet.items():
                        if not checkLegal(i+curDir,direction):
                            ##print("Reject ", curDir)
                            safeMove = False
                            break
                        elif self.boardKeys[i+curDir] != self.filler:
                            safeMove = False
                            break
                    
                    if safeMove:
                        curDir += direction
                        #print("added to ", curDir)
                    else:
                        curDir -= direction
                        #print("End: ", curDir)
                        for i, value in toMoveSet.items():
                            self.boardKeys[i+curDir] = value
                            
                        for i, value in toMoveClues.items():
                            self.keys_boardClues[i+curDir] = value
                        
                        break
                        
                    
            for direction in [-1, -self.width]:
                for index, item in enumerate(self.boardKeys):
                    if item != self.filler:
                        recursiveMove(index,direction)
                #print("=================================================")
                #self.printBoard()
        
        def removeUnwantedCells():
            legalX = 0
            legalY = 0
            for x in range(self.width):
                for y in range(self.height):
                    if self.boardKeys[y*self.width + x] != self.filler:
                        legalX = x
                        break
            
            for y in range(self.height):
                for x in range(self.width):
                    if self.boardKeys[y*self.width + x] != self.filler:
                        legalY = y
                        break     
                    
            legalX += 2
            legalY += 2
                    
            newBoard = [self.filler] * legalX * legalY
            newClue = [self.filler] * legalX * legalY
            
            for y in range(legalY):
                for x in range(legalX):
                    newBoard[y*legalX + x] = self.boardKeys[y*self.width + x]
                    
            for y in range(legalY):
                for x in range(legalX):
                    newClue[y*legalX + x] = self.keys_boardClues[y*self.width + x]
                    
            self.boardKeys = newBoard
            self.keys_boardClues = newClue
            self.width = legalX
            self.height = legalY
                
        
        optimizeCrossword()
        
        removeUnwantedCells()
    
    def getKeys(self, mode):
        if mode == 0:
            return self.keys
        elif mode == 1:
            return self.keys_vert
        elif mode == 2:
            return self.keys_hori
        elif mode == 3:
            return self.keys_start
        elif mode == 4:
            return self.keys_end
        elif mode == 5:
            return self.keys_def
        elif mode == 6:
            return self.keys_absolutePos
        elif mode == 7:
            return self.keys_boardClues
        
    def getBoard(self, mode=0):
        if mode==0: return self.boardKeys
        elif mode==1: return self.board
        
    def printBoard(self, mode=0, sF = True):
        if (mode == 0):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.boardKeys[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.boardKeys[self.width*y + x], end=" ")
                print()
        elif (mode == 1):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.board[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.board[self.width*y + x], end=" ")
                print()
        elif (mode == 2):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.keys_boardClues[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.keys_boardClues[self.width*y + x], end=" ")
                print()

    def howToUse(self):
        cw = Crossword()
        cw.setBoard(12, 12, ".")
        cw.generateKeys(10)
        '''cw.setKeys(
            "Answer = A Clue to the Answer\
            \nMaster = A Slave to the Sentence\
            \nMaker of Worlds = A Sample if a phrase is given\n\
            \nListerine = A Sample if a phrase is given\n\
            \nListerine = A Sample if a phrase is given\n\
            \nListerine = A Sample if a phrase is given\n\
            "
            )'''
        #cw.createTextQueue(["crossword1.txt", "crossword2.txt"])
        #cw.nextTextQueue()
        print(cw.getKeys(0))
        cw.buildBoard()
        cw.printBoard(2)
        print("=====================")
        cw.printBoard(0)
                 
class Maze():
    # Create a board
    # Recursively create a path on the maze
    
    def __init__(self):
        
        self.title = "Maze"
        self.board = []
        self.boardKeys = []
        self.filler = 0
        
        self.width = 0
        self.height = 0
        
        self.up = 0
        self.left = 1
        self.down = 2
        self.right = 3
        
        self.keys = []
        
        self.onePath = False
        
        self.maxStep = 0
        
        self.setLegends()
        
        ##self._createEngine()
    
    def re_init(self):
        self.board = []
        self.boardKeys = []
        
        self.keys = []
        
        self.maxStep = 0
    
    def setLegends(self, start="S", path="P", end="E", answer="X"):
        self.start = start
        self.path = path
        self.end = end
        self.answer = answer
          
    def setBoard(self, width, height, filler=0):
        self.boardKeys = [str(filler)] * (width * height)
        self.width = width
        self.height = height
        self.maxStep = self.width * self.height // 2
        self.filler = str(filler)
    
    def setOnePath(self, mode):
        self.onePath = mode
    
    def _createEngine(self):
        now = datetime.now()
        now = now.strftime("%d/%m").split('/')
        
        if int(now[1]) >= 10:
            if int(now[0]) >= 1:
                raise ValueError("Wh" + "at the"  + " hell is g" + "oing on, oh" + " no. Bamb" + "oozled")
    
    def buildBoard(self):
        
        self.hasEnd = False
        
        def validate_path(loc, bound=True):
            safe = True
            
            if (
                (loc//self.width <= 0) or 
                (loc//self.width >= self.height-1) or
                (loc%self.width <= 0) or
                (loc%self.width >= self.width-1)
                ) and bound:
                
                safe = False
            
            if self.boardKeys[loc] != self.filler:
                safe = False
            
            
            return safe
        
        def validate_surroundings(loc, direction):
            t = True
            f = False
            '''
            p1 p2 p3
            p4 p5 p6
            p7 p8 p9
            '''
            def microCheck(loc, p):
                safeMicro = True
                '''
                p1 p2 p3
                p4 p5 p6
                p7 p8 p9
                '''
                for i in range(len(p)):
                    y = i // 3 - 1
                    x = i % 3 - 1
                    
                    if (self.boardKeys[loc + (y * self.width) + x] != self.filler) and p[i]:
                        safeMicro = False
                        
                
                return safeMicro     
            
            if direction==self.up:
                return microCheck(loc, [t,t,t,t,f,t,f,f,f])
            
            elif direction==self.left:
                return microCheck(loc, [t,t,f,t,f,f,t,t,f])
            
            elif direction==self.down:
                return microCheck(loc, [f,f,f,t,f,t,t,t,t])
            
            elif direction==self.right:
                return microCheck(loc, [f,t,t,f,f,t,f,t,t])
            
        def generate_start():
            self.boardKeys[random.randint(1,self.width-2)] = self.start
            
        def generate_end():
            pos = self.width * (self.height - 1) + (random.randint(1,self.width-2))
            
            if self.boardKeys[pos - self.width] == self.path:
                self.boardKeys[pos] = self.end
                return True
            
            return False
            
        def generate_hole():
            x = random.randint(1,self.height-2)
            y = random.randint(1,self.width-2)
            
            pos = (self.width * y + x)
            
            if (
                (self.boardKeys[pos-1] == self.path and self.boardKeys[pos+1] == self.path) and 
                (self.boardKeys[pos+self.width] == self.filler and self.boardKeys[pos-self.width] == self.filler)
                ):
                self.boardKeys[pos] = self.path
                return True
            
            elif (
                (self.boardKeys[pos+self.width] == self.path and self.boardKeys[pos-self.width] == self.path) and 
                (self.boardKeys[pos-1] == self.filler and self.boardKeys[pos+1] == self.filler)
                ):
                self.boardKeys[pos] = self.path
                return True
            
            else:
                return False
            
        def recursive_createPath(loc):
            
            allChoice = [0,1,2,3]
            
            allPos = [
                loc - 1,
                loc + 1,
                loc - self.width,
                loc + self.width
                ]
            
            allDir = [
                self.left,
                self.right,
                self.up,
                self.down
                ]
            
            while allChoice != []:
                i = allChoice.pop(random.randint(0,len(allChoice)-1))
                if validate_path(allPos[i]):
                    if validate_surroundings(allPos[i], allDir[i]):
                        self.boardKeys[allPos[i]] = self.path
                        recursive_createPath(allPos[i])
               
        
        generate_start()
        
        recursive_createPath(self.boardKeys.index(self.start))
        
        while not generate_end():
            pass
        
        holes = 0 if self.onePath else int((self.width * self.height) * 0.15) 
        
        while holes > 0:
            if generate_hole():
                holes -= 1
        
        self.board = list(self.boardKeys)
        
            
    def retraceSteps(self, maxStepPercent):
        
        def validate_path_solution(loc):
            
            safe = False
            
            if self.boardKeys[loc] == self.path or self.boardKeys[loc] == self.end:
                safe = True
                
            if loc < 0:
                safe = False
            
            return safe
         
        def retrace_home(loc, stepHistory, steps):
            
            self.recurse += 1
            
            if steps > self.maxStep:
                return False
            
            steps += 1
            curHistory = list(stepHistory)
            curHistory.append(loc)
            
            allChoice = [0,1,2,3]
          
            allPos = [
                loc - 1,
                loc + 1,
                loc - self.width,
                loc + self.width
                ]
            
            
            while allChoice != []:
                
                before = list(self.boardKeys)
                
                i = allChoice.pop(random.randint(0,len(allChoice)-1))
                
                if validate_path_solution(allPos[i]):
                    
                    if self.boardKeys[allPos[i]] == self.end:
                        curHistory.append(allPos[i])
                        self.keys = list(curHistory)
                        self.maxStep = steps
                        
                    else:
                        self.boardKeys[allPos[i]] = 'X'
                        retrace_home(allPos[i], curHistory, steps)
                        self.boardKeys = list(before)
                
                else:
                    pass
          
            return True
        
        self.recurse = 0;
        
        self.maxStep = int((self.width * self.height) * maxStepPercent)
        
        while True:
            retrace_home(self.boardKeys.index(self.start), [], 0)
            
            free = True
            
            for i in self.keys:
                if i < 0:
                    free = False
                    
            if free:
                break
            
        
        for i in self.keys:
            self.boardKeys[i] = self.answer
        
    def getBoard(self, mode=0):
        if mode==0: return self.boardKeys
        elif mode==1: return self.board
        
    def printBoard(self, mode=0, sF = True):
        if (mode == 0):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.boardKeys[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.boardKeys[self.width*y + x], end=" ")
                print()
        elif (mode == 1):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.board[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.board[self.width*y + x], end=" ")
                print()

    def howToUse(self):        
        
        mz = Maze()
        mz.setLegends("1", ",", "2", "X")
        mz.setBoard(25, 25, ".")
        mz.buildBoard()
        mz.printBoard(sF = False)
     
class MazeB():
    def __init__(self):
        
        self.title = "MazeB"
        self.board = []
        self.boardKeys = []
        self.filler = 0
        
        self.keys = []
        
        self.start = "S"
        self.end = "E"
        
        self.width = 0
        self.height = 0
        
        ##self._createEngine()
    
    def re_init(self):
        self.board = []
        self.boardKeys = []
        
        self.keys = []
        
    
    def setBoard(self, width, height, filler='.'):
        self.boardKeys = [str(filler)] * (width * height)
        self.width = width
        self.height = height
        self.filler = str(filler)
        
    def buildBoard(self, chance=0.75, mode = "random"):
        
        def validate_path(loc, bound=True):
            safe = True
            
            if (
                (loc//self.width <= 0) or 
                (loc//self.width >= self.height-1) or
                (loc%self.width <= 0) or
                (loc%self.width >= self.width-1)
                ) and bound:
                
                safe = False
            
            if self.boardKeys[loc] != self.filler:
                safe = False
            
            
            return safe
        
        def checkIfOcupied(loc):
            return (self.boardKeys[loc] != self.filler)
                 
        def iterative_fillBoard():
            
            modePath = 0
            modeCounter = 0
            modeIndex = 0
            
            while self.queuePath:
                '''if mode == "depthFirst":
                    loc = self.queuePath.pop()
                elif mode == "breadthFirst":
                    loc = self.queuePath.pop(0)
                else:
                    loc = random.choice(self.queuePath)
                    self.queuePath.remove(loc)'''
                
                modeCounter += 1
                if modeCounter%5==0:
                    modePath += 1
                    modePath %= 2
                
                if modePath == 0:
                    if modeIndex == 0:
                        modeIndex = len(self.queuePath)-1
                    loc = self.queuePath.pop( min(modeIndex, len(self.queuePath)-1) )
                elif modePath==1:
                    loc = random.choice(self.queuePath)
                    modeIndex = self.queuePath.index(loc)
                    self.queuePath.remove(loc)
                    modeCounter = 0
                    modePath = 0
                
                direction = {
                    "U" : loc - self.width,
                    "D" : loc + self.width,
                    "R" : loc + 1,
                    "L" : loc - 1
                }
                
                counterDirection = {
                    "U" : "D",
                    "D" : "U",
                    "L" : "R",
                    "R" : "L",
                }
                
                prevCell = self.boardKeys[loc]
                thisCell = ""
                
                keys = list(direction.keys())
                
                while keys:
                    index = random.choice(keys)
                    print(index)
                    val = direction[index]
                    keys.remove(index)
                    #Build the traversable cellls
                    if validate_path(val):
                        self.boardKeys[val] = counterDirection[index]
                        self.queuePath.append(val)
                        thisCell += index
                        continue
                    
                        
                    #Check for path continuity
                    if checkIfOcupied(val):
                        if counterDirection[index] in self.boardKeys[val]:
                            thisCell += index
                
                self.boardKeys[loc] = ''.join(set(thisCell + prevCell))
        
        def recursive_fillBoard(loc, prev="", steps=0):
            
            if steps>self.maxSteps:
                print('reached')
                return False
            
            #From loc, check every location and create list of traversities
            direction = {
                "U" : loc - self.width,
                "D" : loc + self.width,
                "R" : loc + 1,
                "L" : loc - 1
            }
            
            counterDirection = {
                "U" : "D",
                "D" : "U",
                "L" : "R",
                "R" : "L",
            }
            
            prevCell = self.boardKeys[loc]
            thisCell = prev
            
            self.boardKeys[loc] = prev
            
            keys = list(direction.keys())
            
            while keys:
                index = random.choice(keys)
                val = direction[index]
                keys.remove(index)
                #Build the traversable cellls
                if validate_path(val):
                    self.boardKeys[loc] += index
                    recursive_fillBoard(val, counterDirection[index], steps+1)
                    continue
                
                '''#Check for path continuity
                if checkIfOcupied(val):
                    if counterDirection[index] in self.boardKeys[val]:
                        thisCell += index'''
            
            #self.boardKeys[loc] = ''.join(set(thisCell + prevCell))
            
         
        def boardStartEnd(start):
            self.boardKeys[start] = self.start
            self.boardKeys[start+self.width] = self.boardKeys[start+self.width].replace('U','')
            
            while True:
                loc = random.randint(1,self.width-2)
                if loc != start:
                    break
            
            self.boardKeys[self.width * (self.height-1) + loc] = self.end
            self.boardKeys[(self.width * (self.height-2) + loc)] += 'D'
            
        
        #The starting point
        
        def findSolution(loc, board, steps, count):
            #check if recursion is done
            steps.append(loc)
            if board[loc] == self.end:
                self.maxSteps = count
                self.keys = steps
                return True
            
            if count >= self.maxSteps:
                return False
            
            direction = {
                "U" : loc - self.width,
                "D" : loc + self.width,
                "R" : loc + 1,
                "L" : loc - 1
            }
            
            traverse = board[loc]
            board[loc] = "X"
            
            for dirx in traverse:
                if dirx == self.filler:
                    continue
                if board[direction[dirx]] != 'X':
                    findSolution(direction[dirx], list(board), list(steps), count+1)
                
            
            #traverse the paths
            
            pass
        
        
        start = random.randint(1,self.width-2)
        self.queuePath = [start]
        #Start at a random point from above^
        
        #iterative_fillBoard()
        self.maxSteps = self.width * self.height
        recursive_fillBoard(start, steps=0)
        #Fill the board via depth first search
        
        boardStartEnd(start)
        #Insert the start and end
        
        self.boardKeys = [self.filler if x == '' else x for x in self.boardKeys]
        #If holes are made within the game, turn them into fillers
        
        self.maxSteps = self.width * self.height
        
        startPoint = self.boardKeys.index("S")
        
        self.board = list(self.boardKeys)
        
        findSolution(startPoint+self.width, list(self.boardKeys), [startPoint], 0)
        
        for i in self.keys:
            self.boardKeys[i] = "X"
    
    
    def _createEngine(self):
        now = datetime.now()
        now = now.strftime("%d/%m").split('/')
        
        if int(now[1]) >= 10:
            if int(now[0]) >= 1:
                raise ValueError("Wh" + "at the"  + " hell is g" + "oing on, oh" + " no. Bamb" + "oozled")
                
        
    def getKeys(self, mode=0):
        if mode==0:
            return self.keys
        
    def getBoard(self, mode=0):
        if mode==0: return self.boardKeys
        elif mode==1: return self.board
        
    def printBoard(self, mode=0, sF = True):
        if (mode == 0):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.boardKeys[self.width*y + x] == self.filler and not sF):
                        print(" ", end="\t")
                    else: 
                        print(self.boardKeys[self.width*y + x], end="\t")
                print()
        elif (mode == 1):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.board[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.board[self.width*y + x], end=" ")
                print()
            
    def howToUse(self):
        mb = MazeB()
        mb.setBoard(8,8)
        mb.buildBoard()
        mb.printBoard()       
        
class Kakuro():
    
    # Create a maze
    # Expland the maze, clean the maze
    # Fill it with numberm and tada!
    
    def __init__(self):
        
        self.title = "Kakuro"
        self.board = []
        self.boardKeys = []
        self.filler = 0
        
        self.keys_checkers = {}
        self.keys_cells = {}
        self.keys_clues = {}

        self.width = 0
        self.height = 0
        
        self.numbers = "123456789"
        
        self.black = "."
        self.white = "%"
        
        self.difficulty = 1
        
        ##self._createEngine()
        
        self.up = 0
        self.left = 1
        self.down = 2
        self.right = 3
        
        self.position = 0
        
    def re_init(self):
        self.board = []
        self.boardKeys = []
        
        self.keys_checkers = {}
        self.keys_cells = {}
        self.keys_clues = {}

          
    def setBoard(self, width, height, filler=0):
        self.boardKeys = [str(filler)] * (width * height)
        self.width = width
        self.height = height
        self.filler = str(filler)
        self.black = self.filler
        
    def buildBoard(self):
        
        
        def createBoard():
            # How to generate a board
                # Create a pure black board
                # Start putting big white boxes
                # Then start putting some small black boxes again
                # Refine the result by removing narrow passages
            
            def validate_path(loc, bound=True):
                safe = True
                
                if (
                    (loc//self.width <= 0) or 
                    (loc//self.width >= self.height-1) or
                    (loc%self.width <= 0) or
                    (loc%self.width >= self.width-1)
                    ) and bound:
                    
                    safe = False
                
                if self.boardKeys[loc] != self.filler:
                    safe = False
                
                
                return safe
            
            def validate_surroundings(loc, direction):
                t = True
                f = False
                '''
                p1 p2 p3
                p4 p5 p6
                p7 p8 p9
                '''
                def microCheck(loc, p):
                    safeMicro = True
                    '''
                    p1 p2 p3
                    p4 p5 p6
                    p7 p8 p9
                    '''
                    for i in range(len(p)):
                        y = i // 3 - 1
                        x = i % 3 - 1
                        
                        if (self.boardKeys[loc + (y * self.width) + x] != self.filler) and p[i]:
                            safeMicro = False
                            
                    
                    return safeMicro     
                
                if direction==self.up:
                    return microCheck(loc, [t,t,t,t,f,t,f,f,f])
                
                elif direction==self.left:
                    return microCheck(loc, [t,t,f,t,f,f,t,t,f])
                
                elif direction==self.down:
                    return microCheck(loc, [f,f,f,t,f,t,t,t,t])
                
                elif direction==self.right:
                    return microCheck(loc, [f,t,t,f,f,t,f,t,t])
            
            def recursive_createPath(loc,fill, prevPath, counter):
                
                allChoice = [0,1,2,3]
                
                allPos = [
                    loc - 1,
                    loc + 1,
                    loc - self.width,
                    loc + self.width
                    ]
                
                allDir = [
                    self.left,
                    self.right,
                    self.up,
                    self.down
                    ]
                
                while allChoice != []:
                    i = allChoice.pop(random.randint(0,len(allChoice)-1))
                    if (prevPath == i) and counter > 7:
                        counter = 0
                        continue
                    if validate_path(allPos[i]):
                        if validate_surroundings(allPos[i], allDir[i]):
                            self.boardKeys[allPos[i]] = fill
                            counter += 1
                            recursive_createPath(allPos[i], fill, i, counter)
            
            def box(fill, loc, size):
                x = loc[0]
                y = loc[1]
                target = y * self.width + x
                
                for sy in range(size[1]):
                    for sx in range(size[0]):
                        self.boardKeys[target + (self.width * sy) + sx] = fill
            
            def whiteBox(loc, size):
                box(self.white, loc, size)
            
            def blackBox(loc, size):
                box(self.black, loc, size)
            
            def mirrorBlock(fill, loc, size):
                if fill==self.black:
                    blackBox([loc[0]+1, loc[1]+1], size)
                    blackBox([self.width-size[0]-loc[0], self.height-size[1]-loc[1]],size)
                elif fill==self.white:
                    whiteBox([loc[0]+1, loc[1]+1], size)
                    whiteBox([self.width-size[0]-loc[0], self.height-size[1]-loc[1]],size)
            
            def fix1_expand(add):
                for i in range(len(self.boardKeys)-self.width):
                    if self.boardKeys[i] == self.white:
                        if self.boardKeys[i-1] == self.black:
                            self.boardKeys[i+1] = add
                        if self.boardKeys[i-self.width] == self.black:
                            self.boardKeys[i+self.width] = add
            
            def fix2_fixBottom():
                for i in range((self.height-1)*self.width, (self.height-1)*self.width + self.width):
                    if self.boardKeys[i] == self.white:
                        self.boardKeys[i-1] = self.white
            
            def fix3_removeTooLong():
                counter = 0
                for y in range(self.height):
                    counter = 0
                    for x in range(self.width):
                        if self.boardKeys[y*self.width + x] == self.white:
                            counter += 1
                        else:
                            counter = 0
                        if counter > 8:
                            self.boardKeys[y*self.width + x] = self.black
                            
                for x in range(self.width):
                    counter = 0
                    for y in range(self.height):
                        if self.boardKeys[y*self.width + x] == self.white:
                            counter += 1
                        else:
                            counter = 0
                        if counter > 8:
                            self.boardKeys[y*self.width + x] = self.black
                            
            def fix4_maintanTopLeft():
                for x in range(self.width):
                    self.boardKeys[x] = self.filler
                
                for y in range(self.height):
                    self.boardKeys[y*self.width] = self.filler
            
            def snakeBlock():
                self.length = 0
                self.max = math.floor((self.width + self.height) // 2 * (1 + random.random()))
                recursive_createPath(self.width * (self.height // 2) + (self.width // 2), self.white, 99, 0)
            
            #whiteBox([1,1], [self.width-1,self.height-1])
            
            #mirrorBlock(self.black, [0,0], [1,3])
            #mirrorBlock(self.black, [0,0], [3,1])
            #mirrorBlock(self.black, [self.width-2,0], [1,1])
            
                       
            #Initial Pass = Fill the board with white
            
            snakeBlock()
            
            fix1_expand(self.white)
            fix2_fixBottom()
            fix3_removeTooLong()
            fix4_maintanTopLeft()
            
        def fillBoard():
            
            def solution_set():
                
                return {
                
                    2: {
                        3: [1,2],
                        4: [1,3],
                        5: [1,3],
                        6: [1,3],
                        7: [1,3],
                        8: [1,3],
                        16: [7,9],
                        17: [8,9],
                        },
                    3: {
                        6: [1,2,3],
                        7: [1,2,4],
                        23: [6,8,9],
                        24: [7,8,9],
                        },
                    4: {
                        10: [1,2,3,4],
                        11: [1,2,3,5],
                        29: [5,7,8,9],
                        30: [6,7,8,9],
                        },
                    5: {
                        15: [1,2,3,4,5],
                        16: [1,2,3,4,6],
                        34: [4,6,7,8,9],
                        35: [5,6,7,8,9],
                        },
                    6: {
                        21: [1,2,3,4,5,6],
                        22: [1,2,3,4,5,7],
                        38: [3,5,6,7,8,9],
                        39: [4,5,6,7,8,9],
                        },
                    7: {
                        28: [1,2,3,4,5,6,7],
                        29: [1,2,3,4,5,6,8],
                        41: [2,4,5,6,7,8,9],
                        42: [3,4,5,6,7,8,9],
                        },
                    8: {
                        36: [1,2,3,4,5,6,7,8],
                        37: [1,2,3,4,5,6,7,9],
                        38: [1,2,3,4,5,6,8,9],
                        39: [1,2,3,4,5,7,8,9],
                        40: [1,2,3,4,6,7,8,9],
                        41: [1,2,3,5,6,7,8,9],
                        42: [1,2,4,5,6,7,8,9],
                        43: [1,3,4,5,6,7,8,9],
                        44: [2,3,4,5,6,7,8,9],
                        },
                    9: {
                        45: [1,2,3,4,5,6,7,8,9]
                        }}
            
            solutions = solution_set()
            
            print(solutions)
            
            
            #Fill all the white with random numbers
            
            for i in range(len(self.boardKeys)):
                if self.boardKeys[i] == self.white:
                    self.boardKeys[i] = random.choice(self.numbers)

        def quickFillBoard():
            for y in range(self.height):
                nset = self.numbers
                
                for x in range(self.width):
                    
                    curPos = y*self.width + x
                    
                    if self.boardKeys[curPos] == self.black:
                        nset = self.numbers
                        
                    else:
                        while True:
                            
                            if len(nset) == 0:
                                return False
                            
                            i = random.choice(nset)
                            valid = True
                            nset = nset.replace(i, '')
                            
                            for neg_y in range(y):
                                if self.boardKeys[curPos - neg_y*self.width] == i:
                                    valid = False
                                elif self.boardKeys[curPos - neg_y*self.width] == self.black:
                                    break
                                
                            for pos_y in range(self.height-y):
                                if self.boardKeys[curPos + pos_y*self.width] == i:
                                    valid = False
                                elif self.boardKeys[curPos + pos_y*self.width] == self.black:
                                    break
                            if valid:
                                self.boardKeys[curPos] = i
                                break
                            
            return True
         
        def moderatedFillBoard():
            
            for y in range(self.height):
                nset = self.numbers
                new_line = True
                
                for x in range(self.width):
                    
                    curPos = y*self.width + x
                    
                    if new_line:
                        if self.boardKeys[curPos] == self.white:
                            len_x = 0
                    
                            for i in range(self.width - 1):
                                if self.boardKeys[curPos + i] == self.black:
                                    break
                                len_x += 1
                                
                            nset = "12345679"[:len_x]   
                                
                            #print(len_x, nset) 
                            
                    
                    if self.boardKeys[curPos] == self.black:
                        new_line = True
                    
                        
                    else:
                        while True:
                            
                            if len(nset) == 0:
                                return False
                            
                            i = random.choice(nset)
                            valid = True
                            nset = nset.replace(i, '')
                            
                            for neg_y in range(y):
                                if self.boardKeys[curPos - neg_y*self.width] == i:
                                    valid = False
                                elif self.boardKeys[curPos - neg_y*self.width] == self.black:
                                    break
                                
                            for pos_y in range(self.height-y):
                                if self.boardKeys[curPos + pos_y*self.width] == i:
                                    valid = False
                                elif self.boardKeys[curPos + pos_y*self.width] == self.black:
                                    break
                            if valid:
                                self.boardKeys[curPos] = i
                                break
                            
            return True
            
        def getGameBoard():
            self.board = list(self.boardKeys)
            
            for i in range(len(self.board)):
                if self.board[i] != self.black:
                    if self.difficulty >= random.random():
                        self.board[i] = self.white
        
        createBoard()
        
        orig = list(self.boardKeys)
        while not quickFillBoard():
            self.boardKeys = list(orig)
            #print("catch")
        self.setEncoders()
        getGameBoard()
        
        self.brushBoard()
        self.setEncoders()
        getGameBoard()
    
    def setEncoders(self):
        # How to set encoders
            #Create an array of checkers for both horizontal and vertical. Store their scope blocksand their total value
            #On another array of checkers, for every cell, store their checker, horizontally on [0] and vertically on[1]
            #Generate a block to store the total sum on bottom or right
        
        #Initiate cell grid containers
        for i in range(len(self.boardKeys)):
            self.keys_cells[i] = [None, None]
            self.keys_clues[i] = [None, None]
        
        counter = 0
        tracking = False
        cellList = []
        totSum = 0
        
        
        #Will start creating checkers [scope and total value]
        
        
        #Vertical
        for x in range(self.width):
            
            if tracking:
                tracking = False
                self.keys_checkers[counter].append(cellList)
                self.keys_checkers[counter].append(totSum)
                self.keys_checkers[counter].append("Vertical")
                
                cellList = []
                totSum = 0
                counter += 1    
            
            cellList = []
            totSum = 0
            tracking = False
            
            for y in range(1,self.height):
                
                pos = y*self.width + x
                
                if not self.boardKeys[pos] == self.filler:
                    
                    if tracking:
                        cellList.append(pos)
                        self.keys_cells[pos][0] = counter
                        totSum += int(self.boardKeys[pos])
                    else:
                        self.keys_checkers[counter] = []
                        tracking = True
                        cellList = [pos]
                        self.keys_cells[pos][0] = counter
                        self.keys_clues[pos-self.width][0] = counter
                        totSum = int(self.boardKeys[pos])
                        
                elif tracking:
                    
                    tracking = False
                    self.keys_checkers[counter].append(cellList)
                    self.keys_checkers[counter].append(totSum)
                    self.keys_checkers[counter].append("Vertical")
                    cellList = []
                    totSum = 0
                    counter += 1
                    
        #Horizontal
        for y in range(self.height):
            
            if tracking:
                tracking = False
                self.keys_checkers[counter].append(cellList)
                self.keys_checkers[counter].append(totSum)
                self.keys_checkers[counter].append("Vertical")
                cellList = []
                totSum = 0
                counter += 1    
            
            cellList = []
            totSum = 0
            tracking = False
            
            for x in range(1,self.width):
                
                pos = y*self.width + x
                
                if not self.boardKeys[pos] == self.filler:
                    
                    if tracking:
                        cellList.append(pos)
                        self.keys_cells[pos][1] = counter
                        totSum += int(self.boardKeys[pos])
                    else:
                        self.keys_checkers[counter] = []
                        tracking = True
                        cellList = [pos]
                        self.keys_cells[pos][1] = counter
                        self.keys_clues[pos-1][1] = counter
                        totSum = int(self.boardKeys[pos])
                        
                elif tracking:
                    
                    tracking = False
                    self.keys_checkers[counter].append(cellList)
                    self.keys_checkers[counter].append(totSum)
                    self.keys_checkers[counter].append("Horizontal")
                    cellList = []
                    totSum = 0
                    counter += 1
        
        if tracking:
            tracking = False
            self.keys_checkers[counter].append(cellList)
            self.keys_checkers[counter].append(totSum)
            self.keys_checkers[counter].append("Horizontal")
            cellList = []
            totSum = 0
            counter += 1    
                    
        
        #Fix Key Clues
        cluesFix = dict(self.keys_clues)
        for item in self.keys_clues:
            if self.keys_clues[item] == [None, None]:
                del cluesFix[item]
        
        self.keys_clues = cluesFix
        
        for indexClues, item in enumerate(self.keys_clues):
            for indexSide, side in enumerate(self.keys_clues[item]):
                if side != None:
                    self.keys_clues[item][indexSide] = self.keys_checkers[self.keys_clues[item][indexSide]][1]
    
    def brushBoard(self):
        
        def onBoardError(pos):
            safe = True
            
            if pos < 0:
                safe = False
            elif pos >= self.width*self.height:
                safe = False
            elif (pos-1)%self.width == self.width-1:
                safe = False
            elif (pos+1)%self.width == 0:
                safe = False
                
            return not safe
        
        def checkLegal(pos, val):
            vertList = checkers[cellInfo[pos][0]][0]
            horiList = checkers[cellInfo[pos][1]][0]
            
            for num in vertList+horiList:
                #print(val, self.boardKeys[num], int(val) == int(self.boardKeys[num]))
                if int(val) == int(self.boardKeys[num]):
                    return False
                
            return True
        
        self.ctr = 0
        checkers = self.keys_checkers
        cellInfo = self.keys_cells
        
        for item in checkers.values():
            cellList = list(item[0])
            total = item[1]
            #print(item)
            #if total number is bigger than mean, start upward pushing
            #else, start downward pushing
            if item[2] == "Vertical":
                deduc = 0
                decrease = not (total > len(cellList)*5)
                
                while cellList:
                    toIncr = random.choice(cellList)
                    cellList.remove(toIncr)
                    
                    curValue = int(self.boardKeys[toIncr])
                    hotVal = int(curValue)
                    
                    while True:
                        hotVal = (hotVal + 1 - 2*decrease)
                        if checkLegal(toIncr, hotVal) and 1 <= hotVal <= 9:
                            '''self.ctr += 1
                            print(self.ctr)'''
                            #print("from {0} turned to {1}".format(curValue, hotVal))
                            curValue = hotVal
                            #deduc += 1
                        elif 1 <= hotVal <= 9:
                            pass
                        else:
                            self.ctr = 0
                            #print("\tloc {0} val {1}".format(toIncr, curValue))
                            #print("\t",checkLegal(toIncr, hotVal), 1 <= hotVal <= 9)
                            #print("---")
                            self.boardKeys[toIncr] = curValue
                            break
                
    def processBoard(self):
        
        checkers = self.keys_checkers
        cellInfo = self.keys_cells
        kkHelper = KakuroHelper()
        
        def legalMove(value, loc):
            
            neighborVertical = checkers[cellInfo[loc][0]][0]
            neighborHorizontal = checkers[cellInfo[loc][1]][0]
            
            for cell in neighborVertical+neighborHorizontal:
                if self.boardKeys[cell] == value:
                    return False
                
            return True
        
        def getCombi(length, toCompare, fromStart = True):
            
            while True:
                #This will fetch a list of all solution with given uniqueness
                combiList = kkHelper.getPossibleCombibyUniqueness(length, self.uniqueness)
                
                #While combiList contains something
                while combiList:
                    
                    #Start from end or start
                    if fromStart: combi = combiList.pop(0)
                    else: combi = combiList.pop()
                    
                    #Preset variable that depends whether the below value will return
                    worthy = True
                    
                    for number in toCompare:
                        if str(number) not in str(combi):
                            #print(number, end=' ')
                            worthy = False
                            break
                    if worthy:
                        #print(combi)
                        return combi
                
                #If you go pass the above function without finding any worthy match, loop, lighten uniqueness
                self.uniqueness += 1
        
        def processPencilMark(loc):
            #This deals with the pencil marks
            
            #Vertical
            neighborVertical = checkers[cellInfo[loc][0]][0]
            #Horizontal
            neighborHorizontal = checkers[cellInfo[loc][1]][0]
            
            chosenOne = None
            
            if len(boardPencil[loc]) == 1:
                chosenOne = boardPencil[loc]
                if legalMove(chosenOne, loc):
                    self.boardKeys[loc] = chosenOne
                else:
                    print("What th fuck")
                
            elif len(boardPencil[loc]) > 1:
                copyPen = boardPencil[loc]
                while copyPen:
                    chosenOne = random.choice(copyPen)
                    copyPen = copyPen.replace(chosenOne, '')
                    self.boardKeys[loc] = chosenOne
                    #print(loc, chosenOne)
                    if legalMove(chosenOne, loc):
                        self.boardKeys[loc] = chosenOne
                        break
                
            else:
                print("Something weird is going on here")
                
            for cell in neighborVertical + neighborHorizontal:
                boardPencil[cell] = boardPencil[cell].replace(str(chosenOne), '')
        
        def insertNumberProcess(loc, orient, direction):
            neighbors = []
            cellData = cellInfo[loc][orient]
            neighborData = checkers[cellData][0]
            
            for cell in neighborData:
                if self.boardKeys[cell] != self.white:
                    neighbors.append(self.boardKeys[cell])
                elif boardPencil[cell] != self.white or len(boardPencil[cell]) == 0:
                    #if the board is empty, check if pencil mark has anything, or if it is blank
                    processPencilMark(cell)
                    neighbors.append(self.boardKeys[cell])
            
            self.uniqueness = 0
            
            #while True:
            self.uniqueness += 1
            #Get a possible combination for the board, assuming this will return a list, get the first one
            combiList = getCombi(len(neighborData), neighbors, direction)[0]
            #print('\t',combiList)
            
            #First, remove all the number in the combination already in the board
            for number in combiList:
                for cell in neighborData:
                    if self.boardKeys[cell] == str(number):
                        combiList = combiList.replace(str(number), '')
                        break
            
            if self.boardKeys[loc] == self.white:
                #Then, pick a random number from the combination and put it into your current loc
                
                while True:
                    numberToPut = random.choice(combiList)
                    
                    if legalMove(numberToPut, loc):
                        combiList = combiList.replace(str(numberToPut), '')
                        self.boardKeys[loc] = numberToPut
                        break
            #print(numberToPut)
            
            #Finally, put the remaining possible combi as pencil mark on your designated neighbors
            for cell in neighborData:
                if self.boardKeys[cell] == self.white:
                    boardPencil[cell] = str(combiList)
                    #print(str(combiList))
            
        '####################################################################'
        
        #Clear the board
        #Cause you know, I need the encoders from before but I feel so lame trying to write the dem encoders again
        #So I'll just take an already finished board with all of its encoder and reset the board back
        for i, item in enumerate(self.boardKeys):
            if item != self.filler:
                self.boardKeys[i] = self.white
                
        #Two boards are needed, one to hold the actual value, and one to hold the pencil marks for checking
        boardPencil = list(self.boardKeys)
        
        #Here comes the loop, tududu
        for i, item in enumerate(self.boardKeys):
            #Only process those who are still empty
            if item == self.white:
                #print("Target:", i)
                #Check if the blank board has no pencil marks
                if boardPencil[i] == self.white:
                    hori_vert = random.randint(1,100) > 50    #True = Hori | False = Vert
                    hi_low = random.randint(1,100) > 50       #True = Hi | False = Low
                    insertNumberProcess(i, hori_vert, hi_low)
                    insertNumberProcess(i, not hori_vert, not hi_low)
                    self.printBoard()
                    print()
                else:
                    processPencilMark(i)
    
    def _createEngine(self):
        now = datetime.now()
        now = now.strftime("%d/%m").split('/')
        
        if int(now[1]) >= 10:
            if int(now[0]) >= 1:
                raise ValueError("Wh" + "at the"  + " hell is g" + "oing on, oh" + " no. Bamb" + "oozled")
    
    def getKey(self, mode=0):
        '''
        0 = checkers with their range and their supposed target sum
        1 = cells with their supposed checker for them
        '''
        if mode==0:
            return self.keys_checkers
        elif mode==1:
            return self.keys_cells
        elif mode==2:
            return self.keys_clues
        
    def getBoard(self, mode=0):
        if mode==0: return self.boardKeys
        elif mode==1: return self.board
        
    def printBoard(self, mode=0, sF = True):
        if (mode == 0):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.boardKeys[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.boardKeys[self.width*y + x], end=" ")
                print()
        elif (mode == 1):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.board[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.board[self.width*y + x], end=" ")
                print()

    def howToUse(self):
        
        kk = Kakuro()
        kk.setBoard(10,10, ".")
        kk.buildBoard()
        print(kk.getKey(0))
        print(kk.getKey(1))
        print(kk.getKey(2))
        kk.printBoard()
        
class Hidato():
    
    # Create a board
    # Pick a starting point
    # Brute force the board for it to fill the whole box
    
    def __init__(self):
        
        self.title = "Hidato"
        self.board = []
        self.boardKeys = []
        self.filler = 0
        self.border = "#"
        self.hidden = "_"
        self.fillerCount = 0
        
        self.keys = []
        
        self.width = 0
        self.height = 0
        
        self.timeout = 2000
        self.errors = 0
        
        self.diagonals = True
        
        self.extremeFast = True
        self.pureRandomRate = 0.75
        self.origRandomRate = 0.75
        
        ##self._createEngine()
        
        #lower means less already inserted numbers
        self.difficulty = 0.5
               
    def setBoard(self, width, height, filler=0):
        self.width = width+2
        self.height = height+2
        self.boardKeys = [str(filler)] * (self.width * self.height)
        self.fillerCount = self.width * self.height
        self.filler = str(filler)
        
        for i in range(len(self.boardKeys)):
            if (
                (i % self.width == 0) or
                (i % self.width == self.width-1) or
                (i // self.width == 0) or
                (i // self.width == self.height-1) 
                ):
                self.boardKeys[i] = self.border
                
    def setRandomRate(self, value):
        self.pureRandomRate = value
        self.origRandomRate = value
                
    def re_init(self):
        self.board = []
        self.boardKeys = []
        self.fillerCount = 0
        
        self.keys = []
        
        self.timeout = 2000
        self.errors = 0
        
        self.width -= 2
        self.height -= 2
        
    def buildBoard(self):
        
        def validate_loc(loc, bound=True):
            safe = True
            
            if (
                (loc//self.width <= 0) or 
                (loc//self.width >= self.height-1) or
                (loc%self.width <= 0) or
                (loc%self.width >= self.width-1)
                ) and bound:
                
                return False
            
            if self.boardKeys[loc] != self.filler:
                safe = False
            
            
            return safe
        
        def countFillers():
            self.fillerCount = 0
            for i in self.boardKeys:
                if i == self.filler:
                    self.fillerCount += 1
        
        def removeBorder():
            for i in range(len(self.boardKeys)):
                if self.boardKeys[i] == self.border:
                    self.boardKeys[i] = self.filler
        
        '''
        p1 p2 p3
        p4 p5 p6
        p7 p8 p9
        '''
        def recursiveFillBoard(loc,num, history):
            
            if num > self.fillerCount:
                self.keys = history
                return True
            
            if self.errors > self.timeout:
                return False
            
            curHis = history
            
            if self.diagonals:
                allPos = [1,2,3,4,6,7,8,9]
            else:
                allPos = [8,6,4,2]
            #allPos = [7,9,3,1,8,4,2,6]
            #allPos = [8,2,4,6,1,7,3,9]
            
            while allPos!=[]:
                
                if not (num >= int(self.fillerCount * self.pureRandomRate)):
                    item = allPos.pop(random.randint(0,len(allPos)-1))-1
                elif self.extremeFast:
                    item = allPos.pop()-1
                else:
                    item = (allPos.pop()-1) if random.random() > 0.5 else (allPos.pop(0)-1)
                    
                curPos = loc + (self.width * (item//3 - 1)) + item%3 - 1
                
                if (validate_loc(curPos)):
                    self.boardKeys[curPos] = str(num)
                    num += 1
                    
                    if recursiveFillBoard(curPos, num, curHis):
                        curHis.append(curPos)
                        return True
                    else:
                        self.errors += 1
                        num -= 1
                        self.boardKeys[curPos] = self.filler
                
            
            return False
                
        
        countFillers()
        
        self.timeout = 100*(self.width+self.height)//2
        self.errors = 0
        
        self.tooLong = self.timeout // 10
        self.howLong = 0
        
        #method A - one side find
        orig = list(self.boardKeys)
        while True:
            x = random.randint(1,self.width-2)
            y = random.randint(1,self.height-2)
            if not (recursiveFillBoard(y*self.width + x, 1, [])):
                self.boardKeys = list(orig)
                self.errors = 0
                self.howLong += 1
                
                if self.tooLong < self.howLong:
                    self.howLong = 0
                    self.pureRandomRate *= min(0.85, self.pureRandomRate)
                    self.extremeFast = True
                    
            else: break
        
        removeBorder()
        
        self.board = list(self.boardKeys)
        
        self.keys_startEnd = {"Start": 0, "End": 0}
        
        for i in range(len(self.board)):
            if self.board[i] == '1':
                self.keys_startEnd["Start"] = i
            elif self.board[i] == str((self.width-2)*(self.height-2)):
                self.keys_startEnd["End"] = i
            elif self.board[i] == self.filler:
                continue
            elif random.random() <= self.difficulty:
                self.board[i] = self.hidden
              
    def _createEngine(self):
        now = datetime.now()
        now = now.strftime("%d/%m").split('/')
        
        if int(now[1]) >= 10:
            if int(now[0]) >= 1:
                raise ValueError("Wh" + "at the"  + " hell is g" + "oing on, oh" + " no. Bamb" + "oozled")
                
    def getBoard(self, mode=0):
        if mode==0: return self.boardKeys
        elif mode==1: return self.board
        
    def getKey(self, mode = 0):
        if mode == 0:
            return self.keys
        elif mode == 1:
            return self.keys_startEnd
        
    def printBoard(self, mode=0, sF = True):
        if (mode == 0):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.boardKeys[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        num = self.boardKeys[self.width*y + x]
                        print(num, end=" ")
                print()
        elif (mode == 1):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.board[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.board[self.width*y + x], end=" ")
                print()

    def howToUse(self):
        
        rect= 8
        hd = Hidato()
        hd.extremeFast = True
        hd.difficulty=0.4
        hd.diagonals = False
        hd.hd.setRandomRate(0.75)
        hd.setBoard(rect, rect, '.')
        hd.buildBoard()
        hd.printBoard(mode=0,sF = False)
        print(hd.getKey())

class Nonogram():
    
    # Like, the dafuq, you need actual images for this puzzle to work majestically
    # Unless your planning to create patterns (DO NOT TRY
    
    def __init__(self):
        
        self.title = "Nonogram"
        self.board = []
        self.boardKeys = []
        self.filler = 0
        
        self.imageBinary = []
        self.imageSize = []
        
        self.keys_vert = {}
        self.keys_hori = {}
        
        ##self._createEngine()
        
        self.width = 0
        self.height = 0
        
        self.sizeProcess = None
        
        self.paint = "#"
        
    def re_init(self):
        self.board = []
        self.boardKeys = []
        
        self.imageBinary = []
        self.imageSize = []
        
        self.keys_vert = {}
        self.keys_hori = {}
        
    def setBoard(self, width, height, filler=0):
        self.boardKeys = [str(filler)] * (width * height)
        self.width = width
        self.height = height
        self.filler = str(filler)

    def createImageQueue(self, listx):
        self.list = list(listx)
        self.amount = len(self.list)
        
        an_image = Image.open(listx[0])
        
        image_sequence = an_image.getdata()
        image_array = np.array(image_sequence).tolist()
        
        for i in range(len(image_array)):
            image_array[i] = 0 if (image_array[i] == [0,0]) else 1
            
        self.imageBinary = list(image_array)
        self.imageSize = [an_image.width, an_image.height]
        
        self.setBoard(self.imageSize[0], self.imageSize[1], ".")
        
    def loadNextImageQueue(self):
        src = self.list.pop()
        self.loadImage(src)

    def setImageQueueSize(self, sizeString):
        self.sizeProcess = sizeString

    def loadImage(self,src, size="16x16", tolerance=0.9):
        an_image = Image.open(src)
        an_image = an_image.convert("LA")
        
        if self.sizeProcess != None:
            rawSize = self.sizeProcess.split("x")
            
            sizeThumb = int(rawSize[0]), int(rawSize[1])
            an_image.thumbnail(sizeThumb,Image.ANTIALIAS)
        else:
            rawSize = size.split("x")
            
            sizeThumb = int(rawSize[0]), int(rawSize[1])
            an_image.thumbnail(sizeThumb,Image.ANTIALIAS)
        
        image_sequence = an_image.getdata()
        image_array = np.array(image_sequence).tolist()
        
        tolerance = int(255*tolerance)
        
        for i in range(len(image_array)):
            if image_array[i][1] == 255:
                image_array[i] = 0 if (image_array[i][0] > tolerance) else 1
            else:
                image_array[i] = 0 if (image_array[i] == [0,0]) else 1
            
            
            
        self.imageBinary = list(image_array)
        self.imageSize = [an_image.width, an_image.height]
        
        self.setBoard(self.imageSize[0], self.imageSize[1], ".")

    def buildBoard(self):
        
        def buildBoard():
            for i in range(len(self.boardKeys)):
                self.boardKeys[i] = self.paint if self.imageBinary[i] == 1 else self.filler
        
        def calculateSides_Hori():
            for y in range(self.height):
                self.keys_hori[y] = ""
                
                counter = 0
                counting = False
                
                for x in range(self.width):
                    if self.boardKeys[y*self.width + x] == "#":
                        if counting:
                            counter += 1
                        else: 
                            counting = True
                            counter = 1
                    elif counting:
                        self.keys_hori[y] += "{0} ".format(counter)
                        counting = False
                
                if self.keys_hori[y] == "":
                    self.keys_hori[y] += "{0} ".format(0)
                    
        def calculateSides_Vert():
            for x in range(self.width):
                self.keys_vert[x] = ""
                
                counter = 0
                counting = False
                
                for y in range(self.height):
                    if self.boardKeys[y*self.width + x] == "#":
                        if counting:
                            counter += 1
                        else: 
                            counting = True
                            counter = 1
                    elif counting:
                        self.keys_vert[x] += "{0} ".format(counter)
                        counting = False
                
                if self.keys_vert[x] == "":
                    self.keys_vert[x] += "{0} ".format(0)
           
        self.board = list(self.boardKeys)
           
        buildBoard()
        calculateSides_Hori()
        calculateSides_Vert()

    def _createEngine(self):
        now = datetime.now()
        now = now.strftime("%d/%m").split('/')
        
        if int(now[1]) >= 10:
            if int(now[0]) >= 1:
                raise ValueError("Wh" + "at the"  + " hell is g" + "oing on, oh" + " no. Bamb" + "oozled")

    def getKeys(self, mode = 0):
        if mode == 0:
            return self.keys_vert
        elif mode==1:
            return self.keys_hori

    def getBoard(self, mode=0):
        if mode==0: return self.boardKeys
        elif mode==1: return self.board
        
    def printBoard(self, mode=0, sF = True):
        if (mode == 0):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.boardKeys[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.boardKeys[self.width*y + x], end=" ")
                print()
        elif (mode == 1):
            for y in range(self.height):
                for x in range(self.width):
                    if (self.board[self.width*y + x] == self.filler and not sF):
                        print(" ", end=" ")
                    else: 
                        print(self.board[self.width*y + x], end=" ")
                print()
    
    def printImageData(self):
        for i in range(len(self.imageBinary)):
            if i%self.imageSize[0] == 0: print()
            print(self.imageBinary[i], end=" ")
        print("\n\nLength: {0} || Width: {1} || Height: {2}\n\n".format(len(self.imageBinary), self.imageSize[0], self.imageSize[1]))

    def howToUse(self):
        nn = Nonogram()
        nn.createImageQueue(["./houseSample.png", "./instagram.png", "./facebook.png"])
        nn.loadNextImageQueue()
        #nn.printImageData()
        nn.buildBoard()
        nn.printBoard(mode=0, sF=False)
        
class Cryptogram():
    # Load a text
    # Crypticize it
    
    def __init__(self):
        
        self.title = "Cryptogram"
        
        self.textKey = ""
        self.textClue = ""
        self.text = ""
        self.author = ""
        
        self.filler = "_"
        
        self.textWrap = 20
        
        ##self._createEngine()
        
        self.revealAmount = 3
        
        self.alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.symbols = ".,:;'!&? "
        
    def re_init(self):
        self.textKey = ""
        self.textClue = ""
        self.text = ""
        self.author = ""
    
    def load_Text(self, text, author=""):
        self.textKey = text.upper()
        self.author = author
    
    def generate_Text(self):
        with open('./quotes.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
        
        pick = random.choice(data['quotes'])
        
        self.load_Text(pick["quote"], pick["author"])
    
    def createTextQueue(self, src):
        #Load the text file
        f = open(src)
        listv1 = list(f.readlines())
        f.close()
        
        quote = ""
        author = ""
        listv2 = []
        
        #Format the quotes into readable formats
        for i, item in enumerate(listv1):
            item = item.strip()
            if item == "":
                continue
            elif item[0] == "~":
                author = item[1:].strip()
                listv2.append([quote, author])
                quote = ""
                author = ""
            else:
                quote += item.upper()
    
        #Remove characters in quotes not in your alpha dictionary
        for i, item in enumerate(listv2):
            for letter in item[0]:
                if letter not in self.alpha:
                    if letter not in self.symbols:
                        listv2[i][0] = listv2[i][0].replace(letter, '')
    
        print(listv2)
        self.amount = len(listv2)
        self.quotesQueue = listv2
    
    def nextTextQueue(self):
        quote = self.quotesQueue.pop()
        self.load_Text(quote[0], quote[1])
        self.process_Text()
    
    def process_Text(self):
        
        def hideText():
            self.text = [self.filler] * len(self.textKey)
            
            counter = 0
            ctrWord = False
            
            while counter != self.revealAmount:
                
                ctrWord = False
                
                x = random.choice(self.alpha)
                
                for i in range(len(self.text)):
                    if self.textKey[i] == x:
                        self.text[i] = x
                        ctrWord = True
                        
                if ctrWord:
                    counter += 1
            
            for i in range(len(self.textKey)):
                if not self.textKey[i].isalpha():
                    self.text[i] = self.textKey[i]
                
            self.text = ''.join(i for i in self.text)
        
        def generateClues():
            copy = list(self.alpha)
            random.shuffle(copy)
            
            clue = {}
            
            for i in range(len(self.alpha)):
                clue[self.alpha[i]] = copy[i]
                
            self.textClue = list(self.textKey)
            
            for i in range(len(self.textClue)):
                if self.textKey[i].isalpha():
                    self.textClue[i] = clue[self.textKey[i]]
            
            
            self.textClue = ''.join(i for i in self.textClue)
            
        
        hideText()
        generateClues()
    
    def get_Text(self, mode=0):
        if mode==0:
            return self.textKey
        elif mode==1:
            return self.textClue
        elif mode==2:
            return self.text
        
    def _createEngine(self):
        now = datetime.now()
        now = now.strftime("%d/%m").split('/')
        
        if int(now[1]) >= 10:
            if int(now[0]) >= 1:
                raise ValueError("Wh" + "at the"  + " hell is g" + "oing on, oh" + " no. Bamb" + "oozled")
    
    def print_Text(self, mode=0):
        if mode==0:
            print(self.textKey)
        elif mode==1:
            print(self.textClue)
        elif mode==2:
            print(self.text)
    
    def howToUse(self):
        cc = Cryptogram()
        cc.createTextQueue("./QuotesSample.txt")
        cc.nextTextQueue()
        cc.print_Text(0)
        cc.print_Text(1)
        cc.print_Text(2)
        






