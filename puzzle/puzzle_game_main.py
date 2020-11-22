
if True: #
    from .puzzle_game_sprites import *
    from .puzzle_generators import *
    from . import puzzle_menu
else:
    from puzzle_game_sprites import *
    from puzzle_generators import *
    import puzzle_menu
    
from textwrap import wrap

class mainGame():
    
    def __init__(self, puzzle_class, mode):
        
        pygame.init()
        self.puzzleClass = puzzle_class
        
        gameModes = {
            "Number Search" : 'A',
            'Crossword' : 'B',
            'Maze' : 'C',
            'Kakuro' : 'D',
            'Hidato' : 'E',
            "Nonogram": "F",
            "Cryptogram": "G",
            "MazeB" : "H",
            }
        
        self.run = gameModes[mode]
        
        self.localScreenWidth = 0
        self.localScreenHeight = 0
        
        self.printMode = False
        
        self.clock = pygame.time.Clock()
        
    def checkRun(self):
        return len(self.run) != 0

    def _initBoard(self):
        minSize = {
            "A": 20,
            "B": 20,
            "C": 15,
            "D": 25,
            "E": 25,
            "F": 15,
            "G": 20,
            "H": 15,
            }
        
        
       
        if self.run != 'G': #Shit implementation
        
            self.boxSize = max(minSize[self.run],500 // self.puzzleClass.height)
            
            self.localScreenHeight = max(Screen.SCREENHEIGHT, self.boxSize*self.puzzleClass.height+100)
            self.localScreenWidth = max(Screen.SCREENWIDTH, self.boxSize*self.puzzleClass.width+100)
            self.ypad = 130
            
            if self.run == "F":
                self.localScreenHeight = max(Screen.SCREENHEIGHT, self.localScreenHeight+100)
                
        else:
            
            #self.boxSize = max(minSize[self.run],500 // self.puzzleClass.height)
            
            #self.localScreenWidth = max(Screen.SCREENWIDTH, self.boxSize*self.puzzleClass.width)
            self.localScreenHeight= Screen.SCREENHEIGHT
            self.localScreenWidth= Screen.SCREENWIDTH
            
            
            
        
            
        if self.printMode:
            self.gameDisplay = pygame.display.set_mode((400,300),Screen.FLAGS)
            pygame.display.set_caption(Screen.SCREENCAPTION + " Print Mode")
        else:
            self.gameDisplay = pygame.display.set_mode((self.localScreenWidth,self.localScreenHeight),Screen.FLAGS)
            pygame.display.set_caption(Screen.SCREENCAPTION)
        
        
        self.GeneralDeclarations()
        
        self.SceneLooper()
        
    def build(self, time, autoCheck=None, diagonals=True):
        self.timer = time
        
        self.diagonals = diagonals 
        
        self.autoCheck = autoCheck
        
        Color.defaultColor()
        
        self._initBoard()
    
    def printBoard(self, amount = 1, location="./ImageSave", resultingSize=750):
        self.printMode = True
        self.printAmount = amount
        self.resultingSize = resultingSize
        
        self.saveLocation = location + '/'
        
        if not os.path.exists(location):
            os.makedirs(location)
            
        Color.monochrome()
        
        self.boardLoc = "Board/"
        self.answerLoc = "Answers/"
        self.clueLoc = "Clue/"
        self.boardClueLoc = "BoardwithClue/"
        
        checkFolder(self.saveLocation + self.boardLoc)
        checkFolder(self.saveLocation + self.answerLoc)
        
        if self.run in ['A']:
            checkFolder(self.saveLocation + self.boardClueLoc)
        if self.run in ['B']:
            checkFolder(self.saveLocation + self.clueLoc)
        
        self._initBoard()
        
    
    
    
    def GeneralDeclarations(self):
        self.general_GameTitle = None
        self.general_GameTimer = None
        self.general_GameMoves = None
        
        self.general_sprite = pygame.sprite.Group()
        
        self.puzzleHolder = pygame.surface.Surface(dt(self.localScreenWidth,self.localScreenHeight))
        
        self.click = False
        
    def SceneLooper(self):
        while len(self.run) != 0:
            if self.run == 'A':
                self.NumberSearch()
            elif self.run == 'B':
                self.Crossword()
            elif self.run == 'C':
                self.Maze()
            elif self.run == 'D':
                self.Kakuro()
            elif self.run == 'E':
                self.Hidato()
            elif self.run == 'F':
                self.Nonogram()
            elif self.run == 'G':
                self.Cryptogram()
            elif self.run == 'H':
                self.MazeB()
            elif self.run == '0':
                self.SceneYouWin()
            elif self.run == '1':
                self.SceneYouLose()
        
        pygame.quit()
        try: self.gClues.destroy()
        except: pass
    
    
    def SceneGeneral(self):
        
        def BottomBar():
            if int(self.tick[1]) >= 10:
                if int(self.tick[0]) >= 1:
                    raise ValueError("Wh" + "at the"  + " hell is g" + "oing on, oh" + " no. Bamb" + "oozled")
        
        def TopBar():
            self.general_GameTitle = TextBox(text="Game Loading", 
                        pos=dt(25,17))
            
            self.general_GameTimer = TextBox(text="Time: --", 
                        pos=dt(284, 17))
            
            self.general_GameMoves = TextBox(text="Moves Made: --", 
                        pos=dt(537, 17))
            
            self.tick = self.general_GameTitle.dateTime().split('/')
            
            #BottomBar()
            
            self.general_sprite.add(self.general_GameTitle)
            self.general_sprite.add(self.general_GameTimer)
            self.general_sprite.add(self.general_GameMoves)
        
        TopBar()
   
    def SceneYouWin(self):
        
        def MessageBar():
            self.gameEnd = TextBox(text="Game Finished!", 
                        pos=dt(0,(self.localScreenHeight-90)),
                        size=dt(800, 90),
                        bg_color=Color.SKYBLUE)
            
            self.general_sprite = pygame.sprite.Group()
            
            self.general_sprite.add(self.gameEnd)
            
        
        MessageBar()
        
        def loop():
            while self.run == '0':
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = ''
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_SPACE:
                            self.run = ''
                            
                                            
                self.general_sprite.draw(self.puzzleHolder)
                
                self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
                pygame.display.flip()
                
                self.clock.tick(Screen.FPS)
                
        loop()
        
    def SceneYouLose(self):
        
        def MessageBar():
            self.gameEnd = TextBox(text="Game Lose!", 
                        pos=dt(0,0),
                        size=dt(800, 70),
                        bg_color=Color.RED,
                        f_color=font_color["WhiteNone"])
            self.general_sprite = pygame.sprite.Group()
            
            self.general_sprite.add(self.gameEnd)
            
        
        MessageBar()
        
        def loop():
            while self.run == '1':
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = ''
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_SPACE:
                            self.run = ''
                            
                                            
                self.general_sprite.draw(self.puzzleHolder)
                
                self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
                pygame.display.flip()
                
                self.clock.tick(Screen.FPS)
                
        loop()
    
    def ScenePrintProcess(self,maxAmount):
        
        def createScene():
            self.general_PrintTitle = TextBox(text=self.puzzleClass.title + " Printing...", 
                        pos=dt(0,0),
                        size=dt(400,70))
            
            self.general_Print01 = TextBox(text="  Generating Board Data", 
                        pos=dt(56, 86),
                        size=dt(289,27),
                        f_typo = font_typo["Comfortaa"]["Small"])
            
            self.general_Print02 = TextBox(text="  Creating Board Image", 
                        pos=dt(56, 123),
                        size=dt(289,27),
                        f_typo = font_typo["Comfortaa"]["Small"])
            
            self.general_Print03 = TextBox(text="  Creating Board Solution Image", 
                        pos=dt(56, 162),
                        size=dt(289,27),
                        f_typo = font_typo["Comfortaa"]["Small"])
            
            self.general_PrintLoadingText = TextBox(text="Creating Board {0} of {1}".format(0, maxAmount), 
                        pos=dt(26, 208),
                        size=dt(349, 21),
                        f_typo = font_typo["Comfortaa"]["XSmall"])
            
            self.general_PrintLoadingBar = LoadingBox(Color.GREEN,
                        pos=dt(95, 248),
                        size=dt(211,25))
            
            self.general_PrintLoadingBarBorder = TextBorder('', 
                        pos=dt(90, 243), 
                        size=dt(221, 35), 
                        bg_color=Color.BLACK, 
                        bd_color=Color.BLACK2)
            
            self.general_sprite.add(self.general_PrintTitle)
            self.general_sprite.add(self.general_Print01)
            self.general_sprite.add(self.general_Print02)
            self.general_sprite.add(self.general_Print03)
            self.general_sprite.add(self.general_PrintLoadingText)
            self.general_sprite.add(self.general_PrintLoadingBar)
            self.general_sprite.add(self.general_PrintLoadingBarBorder)
            
        def updateScene(curMode=0, curProg=0, loadPercent=0):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = ''
            
            if loadPercent != None:
                self.general_PrintLoadingBar.updateValue(loadPercent)
            if curProg != None:
                self.general_PrintLoadingText.set_Text("Creating Board {0} of {1}".format(curProg, maxAmount))
                                    
            if curMode != None:
                self.general_Print01.set_Text("{0}  Generating Board Data".format('>' if curMode==0 else ' '))
                self.general_Print02.set_Text("{0}  Creating Board Image".format('>' if curMode==1 else ' '))
                self.general_Print03.set_Text("{0}  Creating Board Solution Image".format('>' if curMode==2 else ' '))
            
            self.gameDisplay.fill(Color.WHITE)
            self.general_sprite.draw(self.gameDisplay)
            pygame.display.flip()
            
        createScene()
        
        return updateScene
  
  
    
    def NumberSearch(self):
        
        def start():
            
            def build_Loaders():
                
                self.updateList = []
                self.mouseUpdateList = []
                
                for item in self.general_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                        
                for item in self.table_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                
                for item in self.table_sprite:
                    if callable(getattr(item, 'mouseDetect', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.mouseUpdateList.append(item)
            
            def build_Table():
                
                self.boardBlocks = {}
                self.table_sprite = pygame.sprite.Group()
                
                boxSize = int(self.boxSize)
                
                left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                
                typo = 0
                if boxSize > 25:
                    typo = font_typo["Comfortaa"]["Regular"]
                else:
                    typo = font_typo["Comfortaa"]["Small"]
                
                width = self.puzzleClass.width
                rawBoard = self.puzzleClass.getBoard(mode=1)
                filler = self.puzzleClass.filler
                
                x = ColorBox(Color.BLACK,
                       pos=dt(left_pad, 75),
                       size=dt((self.puzzleClass.width*boxSize),(self.puzzleClass.height*boxSize)))
                x.static = True
                self.table_sprite.add(x)
                
                for i in range(len(rawBoard)):
                    
                    if rawBoard[i] != filler:
                    
                        self.boardBlocks[i] = TextBorder(rawBoard[i], 
                                                         pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                         size=dt(boxSize+1,boxSize+1), 
                                                         f_typo= typo,
                                                         id=i)
                        
                        
                        
                    else:
                        
                        self.boardBlocks[i] = ColorBox(Color.BLACK,
                                                       pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                       size=dt(boxSize+1,boxSize+1), 
                                                       id=i)
                    
                    
                    self.table_sprite.add(self.boardBlocks[i])
               
            def build_ClueWindow():
                self.gClues = puzzle_menu.GameClues({"Numbers To Find": self.puzzleClass.getKeys(0)})
                self.fontSize = 15
                self.gClues.setPosition(850, 12)
                self.gClues.build()
            
            self.SceneGeneral()
            
            self.moves = 0
            
            self.lastTick = pygame.time.get_ticks()
            
            self.general_GameTitle.set_Text("Number Search")
            self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
            
            
            self.lineList = []
            self.curLine = []
            self.curPoints = []
            self.curHandler = []
            self.lineMode = False
            
            self.answer = []
            
            self.keys = self.puzzleClass.getKeys(1)
            self.keysTitle = self.puzzleClass.getKeys(0)
            
            build_Table()
            
            build_Loaders()
            
            build_ClueWindow()
            
            
            loop()
        
        def printStart():
            
            def printInit(count):
            
                def build_Table():
                    
                    self.boardBlocks = {}
                    self.table_sprite = pygame.sprite.Group()
                    
                    boxSize = int(self.boxSize)
                    
                    self.left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                    
                    typo = 0
                    if boxSize > 25:
                        typo = font_typo["Comfortaa"]["Regular"]
                    else:
                        typo = font_typo["Comfortaa"]["Small"]
                    
                    width = self.puzzleClass.width
                    rawBoard = self.puzzleClass.getBoard(mode=1)
                    filler = self.puzzleClass.filler
                    
                    self.boardWidth =(self.puzzleClass.width*boxSize)
                    self.boardHeight = (self.puzzleClass.height*boxSize)
                    
                    x = ColorBox(Color.BLACK2,
                           pos=dt(self.left_pad, 75),
                           size=dt(self.boardWidth,self.boardHeight))
                    x.static = True
                    self.table_sprite.add(x)
                    
                    for i in range(len(rawBoard)):
                        
                        if rawBoard[i] != filler:
                        
                            self.boardBlocks[i] = TextBorder(rawBoard[i], 
                                                             pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                             size=dt(boxSize+1,boxSize+1), 
                                                             f_typo= typo,
                                                             id=i)
                            
                            
                            
                        else:
                            
                            self.boardBlocks[i] = ColorBox(Color.BLACK,
                                                           pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                           size=dt(boxSize+1,boxSize+1), 
                                                           id=i)
                        
                        
                        self.table_sprite.add(self.boardBlocks[i])
                        
                    #We'll generate the clues here
                    
                    
                    posY = 75
                    padClueLeft = 10
                    self.padPosY = 10 #margin
                    wrapLength = 40
                    
                    '''x = TextBoxLeft(text="Numbers to Find", 
                            pos=dt(self.left_pad+self.boardWidth, posY + self.padPosY),
                            size=dt(self.boardWidth,30),
                            bg_color = Color.WHITE,
                            f_color = font_color["Black2None"],
                            f_typo = font_typo["Comfortaa"]["Regular"])
                    self.table_sprite.add(self.boardBlocks[i])
                    self.padPosY += 30
                    self.table_sprite.add(x)
                        '''
                    keys = self.puzzleClass.getKeys(0)
                    
                    '''mid = len(keys)//2
                    keysA = keys[:mid]
                    keysAPad = int(self.padPosY)
                    keysB = keys[mid:]
                    keysBPad = int(self.padPosY)'''
                    
                    
                    #define vertKeys
                    for index, item in enumerate(keys):
                        
                        x = TextBoxLeft(text="{0}: {1}".format(index+1, item), 
                                pos=dt(self.left_pad+self.boardWidth+padClueLeft, posY + self.padPosY),
                                size=dt(self.boardWidth//2,25),
                                bg_color = Color.WHITE,
                                f_color = font_color["Black2None"],
                                f_typo = font_typo["Comfortaa"]["Small"])
                        self.table_sprite.add(self.boardBlocks[i])
                        self.padPosY += 25
                        self.table_sprite.add(x)
                        
                    
                    self.puzzleHolder = pygame.surface.Surface(dt(self.localScreenWidth+self.boardWidth//2,self.localScreenHeight+self.padPosY+100))
                   
                def print_Table():
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                    name = self.boardClueLoc + "{1}_{0}_BOARDCLUE.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75,
                                 self.boardWidth+self.boardWidth//3,
                                  self.boardHeight,
                                  result_width=self.resultingSize)
                    
                    name = self.boardLoc + "{1}_{0}_BOARDONLY.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75,
                                 self.boardWidth,
                                  self.boardHeight,
                                  result_width=self.resultingSize)
                    
                def get_Solution():
                    for item in self.keys:
                        item.sort()
                        self.answer.append(
                            [
                                self.boardBlocks[item[0]].rect.center,
                                self.boardBlocks[item[1]].rect.center
                                ]
                            )    
                        
                def print_Solution():
                    self.puzzleHolder.fill(Color.WHITE)
                    
                    filler = self.puzzleClass.filler
                    
                    for item in self.boardBlocks:
                        self.boardBlocks[item].bdcolor = Color.LIGHTLIGHTGRAY
                        self.boardBlocks[item].f_color = font_color["Gray2None"]
                        self.boardBlocks[item].update()
                        
                    for i,item in enumerate(self.puzzleClass.getBoard(0)):
                        if item != filler:
                            self.boardBlocks[i].bdcolor = Color.LIGHTLIGHTGRAY
                            self.boardBlocks[i].f_color = font_color["Black2None"]
                            self.boardBlocks[i].update()
                    
                    for item in self.answer:
                        self.table_sprite.add(RoundRectangle(item[0], item[1], Color.BLACK, int(self.boxSize*0.85)))
            
                    self.table_sprite.draw(self.puzzleHolder)
                    
                    '''for item in self.answer:
                        pygame.draw.line(self.puzzleHolder, Color.RED, item[0], item[1], 5)'''
                    
                    name = self.answerLoc + "{1}_{0}_SOLUTION.png".format(count, self.puzzleClass.title)    
                    
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75,
                                 self.boardWidth,
                                  self.boardHeight,
                                  result_width=self.resultingSize)
                   
                self.lineList = []
                self.curLine = []
                self.curPoints = []
                self.curHandler = []
                self.lineMode = False
                
                self.answer = []
                
                self.keys = self.puzzleClass.getKeys(1)
                self.keys = self.puzzleClass.getKeys(1)
                self.keysTitle = self.puzzleClass.getKeys(0)
                
                #renew table
                
                build_Table()
                
                #print board
                
                print_Table()
                
                #get solution to board
                
                get_Solution()
                
                self.printProcess(curMode=1, curProg=None, loadPercent=None)
                
                #print solution
                
                print_Solution()

                self.printProcess(curMode=2, curProg=None, loadPercent=None)

            self.printProcess = self.ScenePrintProcess(self.printAmount)
            self.printProcess(curMode=0, curProg=1, loadPercent=0)

            for i in range(self.printAmount):
                self.puzzleClass.re_init()
                self.puzzleClass.setBoard(self.puzzleClass.width, self.puzzleClass.height, ".") #width, height, filler
                self.puzzleClass.generateKeys(self.puzzleClass.amount, self.puzzleClass.minLength, self.puzzleClass.maxLength)
                self.puzzleClass.buildBoard()
                printInit(i)
                self.printProcess(curMode=0, curProg=i+1, loadPercent=i/self.printAmount)
                
            self.printProcess(curMode=2, curProg=i+1, loadPercent=1)
            
            pygame.time.wait(1000)
            
            self.run = ''
        
        def show_solution():
                
            for item in self.keys:
                self.answer.append(
                    [
                        self.boardBlocks[item[0]].center,
                        self.boardBlocks[item[1]].center
                        ]
                    )
                
            loop_display()
            
        
        def loop_control():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = ''
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        #pygame.image.save(self.puzzleHolder, "Sample.png")
                        self.run = ''
            
                if 4 <= event.type <= 6: #Mouse Button Move and Click Up and Down
                    for item in self.mouseUpdateList:
                        if not self.click:
                            if item.mouseDetect():
                                
                                if not self.lineMode:
                                    self.curLine.append(item.center)
                                    self.lineMode = True
                                    self.curPoints.append(item.id)
                                else:
                                    
                                    self.moves += 1
                                    self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
                                    
                                    self.curPoints.append(item.id)
                                    
                                    match = False
                                    
                                    for i in range(len(self.keysTitle)):
                                        if len(set(self.curPoints) & set(self.keys[i])) == 2:
                                            self.keys.pop(i)
                                            self.gClues.removeClue(self.keysTitle[i])
                                            self.keysTitle.pop(i)
                                            match = True
                                            break
                                        
                                        
                                    if match:
                                        self.curLine.append(item.center)
                                        self.lineList.append(self.curLine)
                                        
                                    self.curLine = []
                                    self.lineMode = False
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = False
                                
        def loop_logic():
            
            for item in self.updateList:
                if item.updating == False:
                    continue
                item.update()
            
            try:
                self.gClues.runUpdate()
            except:
                pass
            
            if pygame.time.get_ticks() - self.lastTick > 1000:
                self.timer -= 1  
                self.general_GameTimer.set_Text("Time: {0}:{1}".format(self.timer//60, self.timer%60))
                self.lastTick = pygame.time.get_ticks()
                if self.timer < 1:
                    show_solution()
                    self.run = '1'
                    
            if len(self.keysTitle)==0:
                self.run = '0'
    
        def loop_display():
            self.puzzleHolder.fill(Color.WHITE)
            
            self.general_sprite.draw(self.puzzleHolder)
            self.table_sprite.draw(self.puzzleHolder)
            
            if self.lineMode:
                pygame.draw.line(self.puzzleHolder, Color.BLACK, self.curLine[0], pygame.mouse.get_pos(), 5)
                
            for item in self.lineList:
                pygame.draw.line(self.puzzleHolder, Color.BLACK, item[0], item[1], 5)
            
            for item in self.answer:
                pygame.draw.line(self.puzzleHolder, Color.RED, item[0], item[1], 5)
            
            self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
            
            pygame.display.flip()
        

        
        def loop():
            while self.run == 'A':
                loop_control()
                loop_logic()
                loop_display()
                
                self.clock.tick(Screen.FPS)
        
        if self.printMode:
            printStart()
        else:
            start()

    def Crossword(self):
        
        def start():
            
            def build_Loaders():
                
                self.updateList = []
                self.mouseUpdateList = []
                
                for item in self.general_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                
                for item in self.table_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                
                for item in self.table_sprite:
                    if callable(getattr(item, 'mouseDetect', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.mouseUpdateList.append(item)
            
            def build_Table():
                
                self.checkList = []
                self.boardBlocks = {}
                self.table_sprite = pygame.sprite.Group()
                
                boxSize = int(self.boxSize)
                
                left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                
                typo = 0
                if boxSize > 25:
                    typo = font_typo["Comfortaa"]["Regular"]
                else:
                    typo = font_typo["Comfortaa"]["Small"]
                
                width = self.puzzleClass.width
                rawBoard = self.puzzleClass.getBoard(mode=1)
                filler = self.puzzleClass.filler
                blank = self.puzzleClass.blank
                
                x = ColorBox(Color.BLACK,
                       pos=dt(left_pad, 75),
                       size=dt((self.puzzleClass.width*boxSize),(self.puzzleClass.height*boxSize)))
                x.static = True
                self.table_sprite.add(x)
                
                for i in range(len(rawBoard)):
                    
                    if rawBoard[i] != filler:
                    
                        self.boardBlocks[i] = TextBorderID(rawBoard[i], 
                                                         pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                         size=dt(boxSize+1,boxSize+1), 
                                                         f_typo= typo,
                                                         id=i)
                        
                        #Make it irrelevant if the board already has answer
                        if rawBoard[i] == blank:
                            self.boardBlocks[i].static = False
                            self.checkList.append(i)
                        
                    else:
                        
                        self.boardBlocks[i] = ColorBox(Color.BLACK,
                                                       pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                       size=dt(boxSize+1,boxSize+1), 
                                                       id=i)
                    
                    
                    self.table_sprite.add(self.boardBlocks[i])
            
                keysBoard = self.puzzleClass.getKeys(7)
                width = self.puzzleClass.width
                
                
                for i,item in enumerate(keysBoard):
                    if item != filler:
                        self.boardBlocks[i].setID(str(item+1))
                        
            def build_ClueWindow():
                
                x = {"Vertical":[], "Horizontal":[]}
                defin = self.puzzleClass.getKeys(5)
                
                for i in self.puzzleClass.getKeys(1).keys():
                    x["Vertical"].append(defin[i])
                    
                for i in self.puzzleClass.getKeys(2).keys():
                    x["Horizontal"].append(defin[i])
                
                self.gClues = puzzle_menu.GameClues(x)
                self.gClues.fontSize = 8
                self.gClues.setPosition(850, 12)
                self.gClues.build()
            
            self.SceneGeneral()
            
            self.moves = 0
            
            self.lastTick = pygame.time.get_ticks()
            
            self.general_GameTitle.set_Text("Crossword")
            self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
            
            self.curBlock = None
            self.width = self.puzzleClass.width
            
            self.answerKey = self.puzzleClass.getBoard(0)
            
            build_Table()
            
            build_Loaders()
            
            self.curNum = self.checkList[0]
            
            build_ClueWindow()
            
            loop()
        
        
        def printStart():
            
            def printInit(count):
            
                def build_Table():
                    
                    self.checkList = []
                    self.boardBlocks = {}
                    self.table_sprite = pygame.sprite.Group()
                    
                    boxSize = int(self.boxSize)
                    
                    
                    
                    typo = 0
                    if boxSize > 25:
                        typo = font_typo["Comfortaa"]["Regular"]
                    else:
                        typo = font_typo["Comfortaa"]["Small"]
                    
                    width = self.puzzleClass.width
                    rawBoard = self.puzzleClass.getBoard(mode=1)
                    filler = self.puzzleClass.filler
                    blank = self.puzzleClass.blank
                    
                    
                    
                    self.boardWidth = (self.puzzleClass.width*boxSize)
                    
                    self.localScreenWidth = max((self.puzzleClass.width*boxSize), 600)
                    
                    self.boardHeight = (self.puzzleClass.height*boxSize)
                    
                    
                    
                    self.left_pad = (self.localScreenWidth - self.boardWidth) // 2
                    
                    x = ColorBox(Color.WHITE,
                           pos=dt(self.left_pad, 75),
                           size=dt(self.localScreenWidth,self.boardHeight))
                    x.static = True
                    self.table_sprite.add(x)
                    
                    for i in range(len(rawBoard)):
                        
                        if rawBoard[i] != filler:
                        
                            self.boardBlocks[i] = TextBorderID(rawBoard[i], 
                                                             pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                             size=dt(boxSize+1,boxSize+1), 
                                                             f_typo= typo,
                                                             id=i)
                            
                            #Make it irrelevant if the board already has answer
                            if rawBoard[i] == blank:
                                self.boardBlocks[i].static = False
                                self.checkList.append(i)
                            
                        else:
                            
                            self.boardBlocks[i] = ColorBox(Color.WHITE,
                                                           pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                           size=dt(boxSize+1,boxSize+1), 
                                                           id=i)
                        
                        
                        self.table_sprite.add(self.boardBlocks[i])
                
                    vertKeys = list(self.puzzleClass.getKeys(1).keys()) #Vert
                    horiKeys = list(self.puzzleClass.getKeys(2).keys()) #Vert
                    posKeys = self.puzzleClass.getKeys(3)
                    width = self.puzzleClass.width
                    
                    keysBoard = self.puzzleClass.getKeys(7)
                    width = self.puzzleClass.width
                    
                    
                    for i,item in enumerate(keysBoard):
                        if item != filler:
                            self.boardBlocks[i].setID(str(item+1))
                    
                    
                    #We'll generate the clues here
                    
                    self.clue_Sprite = pygame.sprite.Group()
                    
                    definitions = self.puzzleClass.getKeys(5)
                    
                    posY = 75 + self.boardHeight
                    self.padPosY = 30 #margin
                    
                    wrapLength = Screen.SCREENWIDTH // 13
                    
                    x = TextBoxLeft(text="Vertical", 
                                        pos=dt(5, self.padPosY),
                                        size=dt(Screen.SCREENWIDTH,30),
                            bg_color = Color.WHITE,
                            f_color = font_color["Black2None"],
                            f_typo = font_typo["Comfortaa"]["Bold"])
                    self.padPosY += 50
                    self.clue_Sprite.add(x)
                    
                    
                      
                    #define vertKeys
                    for index, item in enumerate(vertKeys):
                        
                        item = definitions[item]
                        firstLine = True
                        
                        for text in wrap(item, wrapLength):
                            if firstLine:
                                x = TextBoxLeft(text="{0}: {1}".format(index+1, text), 
                                        pos=dt(5, self.padPosY),
                                        size=dt(Screen.SCREENWIDTH,25),
                                        bg_color = Color.WHITE,
                                        f_color = font_color["Black2None"],
                                        f_typo = font_typo["Comfortaa"]["Regular"])
                                self.padPosY += 35
                                self.clue_Sprite.add(x)
                                firstLine = False
                            else:
                                x = TextBoxLeft(text="   {1}".format(index+1, text), 
                                        pos=dt(5, self.padPosY),
                                        size=dt(Screen.SCREENWIDTH,25),
                                        bg_color = Color.WHITE,
                                        f_color = font_color["Black2None"],
                                        f_typo = font_typo["Comfortaa"]["Regular"])
                                self.padPosY += 35
                                self.clue_Sprite.add(x)
                                firstLine = False
                    
                    self.padPosY += 50
                    
                    x = TextBoxLeft(text="Horizontal", 
                            pos=dt(5, self.padPosY),
                            size=dt(Screen.SCREENWIDTH,30),
                            bg_color = Color.WHITE,
                            f_color = font_color["Black2None"],
                            f_typo = font_typo["Comfortaa"]["Bold"])
                    self.clue_Sprite.add(x)
                    
                    self.padPosY += 50
                    
                    #define horiKeys
                    for index, item in enumerate(horiKeys):
                        item = definitions[item]
                        firstLine = True
                        
                        for text in wrap(item, wrapLength):
                        
                            if firstLine:
                                x = TextBoxLeft(text="{0}: {1}".format(index+1, text), 
                                        pos=dt(5, self.padPosY),
                                        size=dt(Screen.SCREENWIDTH,25),
                                        bg_color = Color.WHITE,
                                        f_color = font_color["Black2None"],
                                        f_typo = font_typo["Comfortaa"]["Regular"])
                                self.padPosY += 35
                                self.clue_Sprite.add(x)
                                firstLine = False
                            else:
                                x = TextBoxLeft(text="   {1}".format(index+1, text), 
                                        pos=dt(5, self.padPosY),
                                        size=dt(Screen.SCREENWIDTH,25),
                                        bg_color = Color.WHITE,
                                        f_color = font_color["Black2None"],
                                        f_typo = font_typo["Comfortaa"]["Regular"])
                                self.padPosY += 35
                                self.clue_Sprite.add(x)
                                firstLine = False
                    
                    self.clueHolder = pygame.surface.Surface(dt(Screen.SCREENWIDTH, self.padPosY+100))
                    self.puzzleHolder = pygame.surface.Surface(dt(self.localScreenWidth ,max(self.localScreenHeight, self.boardHeight)+self.padPosY+100))
                    
                def print_Table():
                    self.gameDisplay.fill(Color.WHITE)
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                    
                    name = self.boardLoc + "{1}_{0}_BOARDONLY.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75-5,
                                 self.boardWidth,
                                  self.boardHeight,
                                  result_width=self.resultingSize)
                    
                    
                    self.clueHolder.fill(Color.WHITE)
                    
                    self.clue_Sprite.draw(self.clueHolder)
                    
                    name = self.clueLoc + "{1}_{0}_CLUE.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.clueHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                0, 0,
                                 Screen.SCREENWIDTH,
                                  self.padPosY+100,
                                  result_width=self.resultingSize)
                    
                    
                    
                def get_Solution():
                    for i in self.checkList:
                        if self.boardBlocks[i].text != self.answerKey[i]:
                            self.boardBlocks[i].ready = False
                            self.boardBlocks[i].setContent(self.answerKey[i], "RedNone", True)
                
                def print_Solution():
                    
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                        
                    name = self.answerLoc + "{1}_{0}_SOLUTION.png".format(count, self.puzzleClass.title)    
                    
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75-5,
                                 self.boardWidth,
                                  self.boardHeight,
                                  result_width=self.resultingSize)
                   
                self.curBlock = None
                self.width = self.puzzleClass.width
                
                self.answerKey = self.puzzleClass.getBoard(0)
                
                #renew table
                
                build_Table()
                
                #print board
                
                print_Table()
                
                #get solution to board
                
                get_Solution()
                
                self.printProcess(curMode=1, curProg=None, loadPercent=None)
                
                #print solution
                
                print_Solution()

                self.printProcess(curMode=2, curProg=None, loadPercent=None)

            self.printProcess = self.ScenePrintProcess(self.printAmount)
            self.printProcess(curMode=0, curProg=1, loadPercent=0)

            for i in range(self.printAmount):
                self.puzzleClass.re_init()
                self.puzzleClass.setBoard(self.puzzleClass.width, self.puzzleClass.height, ".") #width, height, filler
                self.puzzleClass.nextTextQueue()
                self.puzzleClass.buildBoard()
                printInit(i)
                self.printProcess(curMode=0, curProg=i+1, loadPercent=i/self.printAmount)
                
            self.printProcess(curMode=2, curProg=i+1, loadPercent=1)
            
            pygame.time.wait(1000)
            
            self.run = ''
        
        
        def show_solution():
            
            for i in self.checkList:
                if self.boardBlocks[i].text != self.answerKey[i]:
                    self.boardBlocks[i].ready = False
                    self.boardBlocks[i].setContent(self.answerKey[i], "RedNone", True)
            
            loop_display()
        
        def checkBoard():
            done = True
            
            for i in self.checkList:
                if self.boardBlocks[i].text != self.answerKey[i]:
                    done = False
            
            return done
               
        def loop_control():
            
            def setCurBlock(item=None, index=None):
                if self.curBlock != None:
                        #Clear the last selected
                        self.curBlock.ready = False
                        self.curBlock.update()
                    
                    #Set the current selected
                self.curBlock = item
                self.curBlock.ready = True
                self.curBlock.update()
                self.curNum = index
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = ''
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        if (self.curNum - 1) in self.checkList:
                            self.curNum -= 1
                            setCurBlock(self.boardBlocks[self.curNum], self.curNum )
                        
                    elif event.key == pygame.K_RIGHT:
                        if (self.curNum + 1) in self.checkList:
                            self.curNum += 1
                            setCurBlock(self.boardBlocks[self.curNum], self.curNum )         
                                        
                    elif event.key == pygame.K_UP:
                        if (self.curNum - self.width) in self.checkList:
                            self.curNum -= self.width
                            setCurBlock(self.boardBlocks[self.curNum], self.curNum )
                                                  
                    elif event.key == pygame.K_DOWN:
                        if (self.curNum + self.width) in self.checkList:
                            self.curNum += self.width
                            setCurBlock(self.boardBlocks[self.curNum], self.curNum )
                         
                    elif event.key == pygame.K_BACKSPACE:
                        self.curBlock.setContent("")
                        self.moves += 1
                        
                    else:
                        self.curBlock.setContent(event.unicode.upper())
                        if checkBoard():
                            self.run = '0'
                        self.moves += 1
                    self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
                                
                if 4 <= event.type <= 6: #Mouse Button Move and Click Up and Down
                    for _,item in enumerate(self.mouseUpdateList):
                        if not self.click:
                            if item.mouseDetect():
                                setCurBlock(item, item.id)
                                
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = False
                                
        def loop_logic():
            
            for item in self.updateList:
                if item.updating == False:
                    continue
                item.update()
            
            try:
                self.gClues.runUpdate()
            except:
                pass
            
            if pygame.time.get_ticks() - self.lastTick > 1000:
                self.timer -= 1  
                self.general_GameTimer.set_Text("Time: {0}:{1}".format(self.timer//60, self.timer%60))
                self.lastTick = pygame.time.get_ticks()
                if self.timer < 1:
                    show_solution()
                    self.run = '1'
                    
            if False:
                self.run = '0'
    
        def loop_display():
            self.puzzleHolder.fill(Color.WHITE)
            
            self.general_sprite.draw(self.puzzleHolder)
            self.table_sprite.draw(self.puzzleHolder)
            
            self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
            
            pygame.display.flip()
        

        
        def loop():
            while self.run == 'B':
                loop_control()
                loop_logic()
                loop_display()
                
                self.clock.tick(Screen.FPS)
        
        if self.printMode:
            printStart()
        else:
            start()

    def Maze(self):
        
        def start():
            
            def build_Loaders():
                
                self.updateList = []
                self.mouseUpdateList = []
                
                for item in self.general_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                        
                for item in self.table_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                
                
                for index, item in enumerate(self.table_sprite):
                    if callable(getattr(item, 'mouseDetect', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        if hasattr(item, 'ready'):
                            if item.ready == False:
                                continue
                        self.mouseUpdateList.append(item)
                                  
            def build_Table():
                
                self.boardBlocks = {}
                self.table_sprite = pygame.sprite.Group()
                
                boxSize = int(self.boxSize)
                
                left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                
                width = self.puzzleClass.width
                rawBoard = self.puzzleClass.getBoard(mode=1)
                
                filler = self.puzzleClass.filler
                start = self.puzzleClass.start
                end = self.puzzleClass.end
                
                x = ColorBox(Color.WHITE,
                       pos=dt(left_pad, 75),
                       size=dt((self.puzzleClass.width*boxSize),(self.puzzleClass.height*boxSize)))
                x.static = True
                self.table_sprite.add(x)
                
                for i in range(len(rawBoard)):
                    
                    if rawBoard[i] != filler:
                        
                        if rawBoard[i] == start:
                            self.boardBlocks[i] = ColorBoxDynamic(dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                        size=dt(boxSize+1,boxSize+1), 
                                                        inactive = Color.BLUE,
                                                        active = Color.BLUE,
                                                        active2 = Color.BLUE,
                                                        id = i)
                            
                            self.boardBlocks[i].ready = True
                            
                        
                        elif rawBoard[i] == end:
                            self.boardBlocks[i] = ColorBoxDynamic(dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                        size=dt(boxSize+1,boxSize+1), 
                                                        inactive = Color.GREEN,
                                                        active = Color.YELLOW,
                                                        active2 = Color.BLUE,
                                                        id = i)
                            
                            self.endBlock = self.boardBlocks[i]
                        
                        else:
                            self.boardBlocks[i] = ColorBoxDynamic(dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                        size=dt(boxSize+1,boxSize+1), 
                                                        inactive = Color.WHITE,
                                                        active = Color.YELLOW,
                                                        active2 = Color.BLUE,
                                                        id = i)
                        
                    else:
                        self.boardBlocks[i] = ColorBox(Color.BLACK,
                                                       pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                       size=dt(boxSize+1,boxSize+1), 
                                                       id=i)
                    
                    
                    self.table_sprite.add(self.boardBlocks[i])
            
            self.SceneGeneral()
            
            self.general_sprite.add(TextBox(text="Hover over the Blue Box, a yellow block will appear, which is walkable", 
                        pos=dt(0,self.localScreenHeight-20),
                        size=(800, 20),
                        f_typo = font_typo["Comfortaa"]["Small"]))
            
            self.moves = 0
            
            self.endBlock = None
            
            self.lastTick = pygame.time.get_ticks()
            
            self.general_GameTitle.set_Text("Maze")
            self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
            
            self.keysMap = self.puzzleClass.getBoard(1)
            
            build_Table()
            
            self.width = self.puzzleClass.width
            self.height = self.puzzleClass.height
            self.boardSize =  self.width * self.height 
            
            build_Loaders()
            
            
            loop()
        
        
        def printStart():
            
            def printInit(count):
            
                def build_Table():
                    
                    def validate_path(loc, bound=True):
                        #Check if loc is checkable
                        safe = True
                        
                        if (
                            (loc//width <= 0) or 
                            (loc//width >= height-1) or
                            (loc%width <= 0) or
                            (loc%width >= width-1)
                            ) and bound:
                            
                            safe = False
                        
                        return safe
                    
                    def checkCorner(loc, bound = True):
                        #I dont know what to call this, it'll check if block is not on corner or loc 
                        
                        minimize = False
                        
                        if self.rawBoard[loc] == self.filler:
                            minimize = True
                        
                        return minimize
                    
                    self.checkList = []
                    self.boardBlocks = {}
                    self.table_sprite = pygame.sprite.Group()
                    
                    boxSize = int(self.boxSize)
                    
                    self.left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                    
                    width = self.puzzleClass.width
                    height = self.puzzleClass.height
                    rawBoard = self.puzzleClass.getBoard(mode=1)
                    
                    self.rawBoard = rawBoard
                    
                    self.filler = self.puzzleClass.filler
                    start = self.puzzleClass.start
                    end = self.puzzleClass.end
                    
                    self.boardWidth =(self.puzzleClass.width*boxSize)
                    self.boardHeight = (self.puzzleClass.height*boxSize)
                    
                    x = ColorBox(Color.BLACK2,
                           pos=dt(self.left_pad, 75),
                           size=dt(self.boardWidth,self.boardHeight))
                    x.static = True
                    self.table_sprite.add(x)
                    
                    for i in range(len(rawBoard)):
                        
                        if rawBoard[i] != self.filler:
                            
                            if rawBoard[i] == start:
                                self.boardBlocks[i] = ColorBoxDynamic(dt(self.left_pad+(i%width*(boxSize*0.8)), 75+(i//width*(boxSize*0.8))), 
                                                            size=dt(boxSize*(1/self.expand),boxSize*(1/self.expand)), 
                                                            inactive = Color.BLUE,
                                                            active = Color.BLUE,
                                                            active2 = Color.BLUE,
                                                            id = i)
                                
                                self.boardBlocks[i].ready = True
                                
                            
                            elif rawBoard[i] == end:
                                self.boardBlocks[i] = ColorBoxDynamic(dt(self.left_pad+(i%width*(boxSize*0.8)), 75+(i//width*(boxSize*0.8))), 
                                                            size=dt(boxSize*(1/self.expand),boxSize*(1/self.expand)), 
                                                            inactive = Color.GREEN,
                                                            active = Color.YELLOW,
                                                            active2 = Color.BLUE,
                                                            id = i)
                                
                                self.endBlock = self.boardBlocks[i]
                            
                            else:
                                self.boardBlocks[i] = ColorBoxDynamic(dt(self.left_pad+(i%width*(boxSize*0.8)), 75+(i//width*(boxSize*0.8))), 
                                                            size=dt(boxSize*(1/self.expand),boxSize*(1/self.expand)), 
                                                            inactive = Color.WHITE,
                                                            active = Color.YELLOW,
                                                            active2 = Color.BLUE,
                                                            id = i)
                            
                        else:
                            #up down left right
                            dirCorners = [i-width, i+width, i-1, i+1]
                            
                            for index, dirc in enumerate(dirCorners):
                                if validate_path(dirc):
                                    dirCorners[index] = checkCorner(dirc)
                                else:
                                    dirCorners[index] = False
                            
                            self.boardBlocks[i] = ColorBoxThin(Color.BLACK, Color.WHITE,
                                                           pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                           size=dt(boxSize+1,boxSize+1), 
                                                           thinDir = dirCorners,
                                                           id=i)
                        
                        
                        self.table_sprite.add(self.boardBlocks[i])

                    
                def print_Table():
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                    name = "{1}_{0}_BOARD.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75,
                                 self.boardWidth*self.expand*1.01,
                                  self.boardHeight*self.expand*1.01)
                    
                def get_Solution():
                    for i in self.puzzleClass.keys:
                        self.boardBlocks[i].curMode = 3
                        self.boardBlocks[i].update()
                
                def print_Solution():
                    
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                        
                    name = "{1}_{0}_SOLUTION.png".format(count, self.puzzleClass.title)    
                    
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75,
                                 self.boardWidth*self.expand*1.01,
                                  self.boardHeight*self.expand*1.01)
                   
                self.endBlock = None
                self.keysMap = self.puzzleClass.getBoard(1)
                self.width = self.puzzleClass.width
                self.height = self.puzzleClass.height
                self.boardSize =  self.width * self.height 
                self.expand = 1/1.35
                
                #renew table
                
                build_Table()
                
                #print board
                
                print_Table()
                
                #get solution to board
                
                get_Solution()
                
                self.printProcess(curMode=1, curProg=None, loadPercent=None)
                
                #print solution
                
                print_Solution()

                self.printProcess(curMode=2, curProg=None, loadPercent=None)

            self.printProcess = self.ScenePrintProcess(self.printAmount)
            self.printProcess(curMode=0, curProg=1, loadPercent=0)

            for i in range(self.printAmount):
                self.puzzleClass.re_init()
                self.puzzleClass.setBoard(self.puzzleClass.width, self.puzzleClass.height, ".")
                self.puzzleClass.buildBoard()
                
                printInit(i)
                self.printProcess(curMode=0, curProg=i+1, loadPercent=i/self.printAmount)
                
            self.printProcess(curMode=2, curProg=i+1, loadPercent=1)
            
            pygame.time.wait(1000)
            
            self.run = ''
        
        
        
        def show_solution():
            for i in self.puzzleClass.keys:
                self.boardBlocks[i].curMode = 3
                self.boardBlocks[i].update()
            
        
        def loop_control():
            
            def checkProximity(idx):
                if idx-1 >0:
                    item = self.boardBlocks[idx-1]
                    if callable(getattr(item, 'setReady', None)):
                        if item.curMode == 0:
                            item.setReady()
                            self.mouseUpdateList.append(item)
                        
                if idx+1 < self.boardSize-1:
                    item = self.boardBlocks[idx+1]
                    if callable(getattr(item, 'setReady', None)):
                        if item.curMode == 0:
                            item.setReady()
                            self.mouseUpdateList.append(item)
                        
                if idx+self.width < self.boardSize-1:
                    item = self.boardBlocks[idx+self.width]
                    if callable(getattr(item, 'setReady', None)):
                        if item.curMode == 0:
                            item.setReady()
                            self.mouseUpdateList.append(item)
                        
                if idx-self.width > 0:
                    item = self.boardBlocks[idx-self.width]
                    if callable(getattr(item, 'setReady', None)):
                        if item.curMode == 0:
                            item.setReady()
                            self.mouseUpdateList.append(item)
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = ''
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        #pygame.image.save(self.puzzleHolder, "Sample.png")
                        self.run = ''
            
                if 4 <= event.type <= 6: #Mouse Button Move and Click Up and Down
                    for item in self.mouseUpdateList:
                        if not self.click:
                            if item.mouseDetect():
                                if item.curMode == 1:
                                    checkProximity(item.id)
                                    item.setMode(2)
                                    self.moves += 1
                                    self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
                                    if self.endBlock.curMode == 2:
                                        self.run = '0'
                                    
                                elif item.curMode != 2:
                                    checkProximity(item.id)
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = False
                                
        def loop_logic():
            
            for item in self.updateList:
                if item.updating == False:
                    continue
                item.update()
  
            if pygame.time.get_ticks() - self.lastTick > 1000:
                self.timer -= 1  
                self.general_GameTimer.set_Text("Time: {0}:{1}".format(self.timer//60, self.timer%60))
                self.lastTick = pygame.time.get_ticks()
                if self.timer < 1:
                    show_solution()
                    self.run = '1'
            
    
        def loop_display():
            self.gameDisplay.fill(Color.WHITE)
            
            self.puzzleHolder.fill(Color.WHITE)
            
            self.general_sprite.draw(self.puzzleHolder)
            self.table_sprite.draw(self.puzzleHolder)
            
            self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
            
            pygame.display.flip()
        

        
        def loop():
            while self.run == 'C':
                loop_control()
                loop_logic()
                loop_display()
                
                self.clock.tick(Screen.FPS)
        
        if self.printMode:
            printStart()
        else:
            start()
            
    def MazeB(self):
        
        def start():
            
            def build_Loaders():
                
                self.updateList = []
                self.mouseUpdateList = []
                
                for item in self.general_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                        
                for item in self.table_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                
                
                for index, item in enumerate(self.table_sprite):
                    if callable(getattr(item, 'mouseDetect', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        if hasattr(item, 'ready'):
                            if item.ready == False:
                                continue
                        self.mouseUpdateList.append(item)
                                  
            def build_Table():
                
                self.boardBlocks = {}
                self.table_sprite = pygame.sprite.Group()
                
                boxSize = int(self.boxSize)
                
                left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                
                width = self.puzzleClass.width
                rawBoard = self.puzzleClass.getBoard(mode=1)
                
                filler = self.puzzleClass.filler
                start = self.puzzleClass.start
                end = self.puzzleClass.end
                
                x = ColorBox(Color.LIGHTLIGHTGRAY,
                       pos=dt(left_pad, 75),
                       size=dt((self.puzzleClass.width*boxSize),(self.puzzleClass.height*boxSize)))
                x.static = True
                self.table_sprite.add(x)
                
                y = ColorBox(Color.WHITE,
                       pos=dt(left_pad+boxSize, 75+boxSize),
                       size=dt((self.puzzleClass.width*boxSize)-boxSize*2,(self.puzzleClass.height*boxSize)-boxSize*2))
                y.static = True
                self.table_sprite.add(y)
                
                
                
                for i in range(len(rawBoard)):
                    
                    if rawBoard[i] != filler:
                        
                        if rawBoard[i] == start:
                            self.boardBlocks[i] = MazeThinBlock("D",dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                        size=dt(boxSize+1,boxSize+1), 
                                                        inactive = Color.BLUE,
                                                        active = Color.BLUE,
                                                        active2 = Color.BLUE,
                                                        id = i,
                                                        borders=False)
                            
                            self.boardBlocks[i].ready = True
                            
                        
                        elif rawBoard[i] == end:
                            self.boardBlocks[i] = MazeThinBlock("U", dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                        size=dt(boxSize+1,boxSize+1), 
                                                        inactive = Color.GREEN,
                                                        active = Color.YELLOW,
                                                        active2 = Color.BLUE,
                                                        id = i,
                                                        borders=False)
                            
                            self.endBlock = self.boardBlocks[i]
                        
                        else:
                            self.boardBlocks[i] = MazeThinBlock(rawBoard[i], dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                        size=dt(boxSize+1,boxSize+1), 
                                                        inactive = Color.WHITE,
                                                        active = Color.YELLOW,
                                                        active2 = Color.BLUE,
                                                        id = i)
                        
                    else:
                        self.boardBlocks[i] = ColorBox(Color.LIGHTLIGHTGRAY,
                                                       pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                       size=dt(boxSize+1,boxSize+1), 
                                                       id=i)
                    
                    
                    self.table_sprite.add(self.boardBlocks[i])
            
            self.SceneGeneral()
            
            self.general_sprite.add(TextBox(text="Hover over the Blue Box, a yellow block will appear, which is walkable", 
                        pos=dt(0,self.localScreenHeight-20),
                        size=(800, 20),
                        f_typo = font_typo["Comfortaa"]["Small"]))
            
            self.moves = 0
            
            self.endBlock = None
            
            self.lastTick = pygame.time.get_ticks()
            
            self.general_GameTitle.set_Text("MazeB")
            self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
            
            self.keysMap = self.puzzleClass.getBoard(1)
            
            build_Table()
            
            self.width = self.puzzleClass.width
            self.height = self.puzzleClass.height
            self.boardSize =  self.width * self.height 
            
            build_Loaders()
            
            
            loop()
        
        def printStart():
            
            def printInit(count):
            
                def build_Table():
                
                    self.boardBlocks = {}
                    self.table_sprite = pygame.sprite.Group()
                    
                    boxSize = int(self.boxSize)
                    
                    self.left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                    
                    width = self.puzzleClass.width
                    rawBoard = self.puzzleClass.getBoard(mode=1)
                    
                    #print(rawBoard)
                    
                    filler = self.puzzleClass.filler
                    start = self.puzzleClass.start
                    end = self.puzzleClass.end
                    
                    self.boardWidth = (self.puzzleClass.width*boxSize)
                    self.boardHeight = (self.puzzleClass.height*boxSize)
                    
                    x = ColorBox(Color.LIGHTLIGHTGRAY,
                           pos=dt(self.left_pad, 75),
                           size=dt(self.boardWidth,self.boardHeight))
                    x.static = True
                    self.table_sprite.add(x)
                    
                    y = ColorBox(Color.WHITE,
                           pos=dt(self.left_pad+boxSize, 75+boxSize),
                           size=dt((self.puzzleClass.width*boxSize)-boxSize*2,(self.puzzleClass.height*boxSize)-boxSize*2))
                    y.static = True
                    self.table_sprite.add(y)
                    
                    
                    for i in range(len(rawBoard)):
                        
                        if rawBoard[i] != filler:
                            
                            if rawBoard[i] == start:
                                self.boardBlocks[i] = MazeThinBlock("D",dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                            size=dt(boxSize+1,boxSize+1), 
                                                            inactive = Color.BLUE,
                                                            active = Color.BLUE,
                                                            active2 = Color.BLUE,
                                                            id = i,
                                                            borders=False)
                                
                                self.boardBlocks[i].ready = True
                                
                            
                            elif rawBoard[i] == end:
                                self.boardBlocks[i] = MazeThinBlock("U", dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                            size=dt(boxSize+1,boxSize+1), 
                                                            inactive = Color.GREEN,
                                                            active = Color.YELLOW,
                                                            active2 = Color.BLUE,
                                                            id = i,
                                                            borders=False)
                                
                                self.endBlock = self.boardBlocks[i]
                            
                            else:
                                self.boardBlocks[i] = MazeThinBlock(rawBoard[i], dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                            size=dt(boxSize+1,boxSize+1), 
                                                            inactive = Color.WHITE,
                                                            active = Color.YELLOW,
                                                            active2 = Color.BLUE,
                                                            id = i)
                            
                        else:
                            self.boardBlocks[i] = ColorBox(Color.LIGHTLIGHTGRAY,
                                                           pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                           size=dt(boxSize+1,boxSize+1), 
                                                           id=i)
                        
                        
                        self.table_sprite.add(self.boardBlocks[i])

                def print_Table():
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                    name = self.boardLoc + "{1}_{0}_BOARD.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75,
                                 self.boardWidth,
                                  self.boardHeight,
                                  result_width=self.resultingSize)
                    
                def get_Solution():
                    self.toDraw = []
                    for i in self.puzzleClass.keys:
                        '''self.boardBlocks[i].curMode = 3
                        self.boardBlocks[i].update()'''
                        self.toDraw.append(self.boardBlocks[i].center)
                
                def print_Solution():
                    
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                    
                    prevPoint = None
                    for item in self.toDraw:
                        if prevPoint != None:
                            pygame.draw.line(self.puzzleHolder, Color.BLACK, prevPoint, item, 3)
                        prevPoint = item
                        
                    name = self.answerLoc + "{1}_{0}_SOLUTION.png".format(count, self.puzzleClass.title)    
                    
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75,
                                 self.boardWidth,
                                  self.boardHeight,
                                  result_width=self.resultingSize)
                   
                self.endBlock = None
                self.keysMap = self.puzzleClass.getBoard(1)
                self.width = self.puzzleClass.width
                self.height = self.puzzleClass.height
                self.boardSize =  self.width * self.height 
                
                #renew table
                
                build_Table()
                
                #print board
                
                print_Table()
                
                #get solution to board
                
                get_Solution()
                
                self.printProcess(curMode=1, curProg=None, loadPercent=None)
                
                #print solution
                
                print_Solution()

                self.printProcess(curMode=2, curProg=None, loadPercent=None)

            self.printProcess = self.ScenePrintProcess(self.printAmount)
            self.printProcess(curMode=0, curProg=1, loadPercent=0)

            for i in range(self.printAmount):
                self.puzzleClass.re_init()
                self.puzzleClass.setBoard(self.puzzleClass.width, self.puzzleClass.height, ".")
                self.puzzleClass.buildBoard()
                
                printInit(i)
                self.printProcess(curMode=0, curProg=i+1, loadPercent=i/self.printAmount)
                
            self.printProcess(curMode=2, curProg=i+1, loadPercent=1)
            
            pygame.time.wait(1000)
            
            self.run = ''
        
        
        
        def show_solution():
            for i in self.puzzleClass.keys:
                self.boardBlocks[i].curMode = 3
                self.boardBlocks[i].update()
            
        
        def loop_control():
            
            def checkProximity(idx, dirCodes):
                if idx-1 >0 and ('L' in dirCodes):
                    item = self.boardBlocks[idx-1]
                    if callable(getattr(item, 'setReady', None)):
                        if item.curMode == 0:
                            item.setReady()
                            self.mouseUpdateList.append(item)
                        
                if idx+1 < self.boardSize-1 and ('R' in dirCodes):
                    item = self.boardBlocks[idx+1]
                    if callable(getattr(item, 'setReady', None)):
                        if item.curMode == 0:
                            item.setReady()
                            self.mouseUpdateList.append(item)
                        
                if idx+self.width < self.boardSize-1  and ('D' in dirCodes):
                    item = self.boardBlocks[idx+self.width]
                    if callable(getattr(item, 'setReady', None)):
                        if item.curMode == 0:
                            item.setReady()
                            self.mouseUpdateList.append(item)
                        
                if idx-self.width > 0 and ('U' in dirCodes):
                    item = self.boardBlocks[idx-self.width]
                    if callable(getattr(item, 'setReady', None)):
                        if item.curMode == 0:
                            item.setReady()
                            self.mouseUpdateList.append(item)
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = ''
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        #pygame.image.save(self.puzzleHolder, "Sample.png")
                        self.run = ''
            
                if 4 <= event.type <= 6: #Mouse Button Move and Click Up and Down
                    for item in self.mouseUpdateList:
                        if not self.click:
                            if item.mouseDetect():
                                if item.curMode == 1:
                                    
                                    checkProximity(item.id, item.mode)
                                    item.setMode(2)
                                    
                                    self.moves += 1
                                    self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
                                    
                                    if self.endBlock.curMode == 2:
                                        self.run = '0'
                                    
                                elif item.curMode != 2:
                                    checkProximity(item.id, item.mode)
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = False
                                
        def loop_logic():
            
            for item in self.updateList:
                if item.updating == False:
                    continue
                item.update()
  
            if pygame.time.get_ticks() - self.lastTick > 1000:
                self.timer -= 1  
                self.general_GameTimer.set_Text("Time: {0}:{1}".format(self.timer//60, self.timer%60))
                self.lastTick = pygame.time.get_ticks()
                if self.timer < 1:
                    show_solution()
                    self.run = '1'
            
    
        def loop_display():
            self.gameDisplay.fill(Color.WHITE)
            
            self.puzzleHolder.fill(Color.WHITE)
            
            self.general_sprite.draw(self.puzzleHolder)
            self.table_sprite.draw(self.puzzleHolder)
            
            self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
            
            pygame.display.flip()
        

        
        def loop():
            while self.run == 'H':
                loop_control()
                loop_logic()
                loop_display()
                
                self.clock.tick(Screen.FPS)
        
        if self.printMode:
            printStart()
        else:
            start()

    def Kakuro(self):
        
        def start():
            
            def build_Loaders():
                
                self.updateList = []
                self.mouseUpdateList = []
                
                for item in self.general_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                        
                for item in self.table_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                        self.movesBeforeChecking += 1
                        
                for item in self.table_sprite:
                    if callable(getattr(item, 'mouseDetect', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.mouseUpdateList.append(item)
            
            def build_Table():
                
                self.checkList = []
                
                self.boardBlocks = {}
                self.table_sprite = pygame.sprite.Group()
                
                boxSize = int(self.boxSize)
                
                left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                
                typo = 0
                if boxSize > 45:
                    typo = font_typo["Comfortaa"]["Regular"]
                else:
                    typo = font_typo["Comfortaa"]["XSmall"]
                
                width = self.puzzleClass.width
                rawBoard = self.puzzleClass.getBoard(mode=1)
                filler = self.puzzleClass.filler
                blank = self.puzzleClass.white
                
                clues = self.puzzleClass.getKey(2)
                
                x = ColorBox(Color.BLACK,
                       pos=dt(left_pad, 75),
                       size=dt((self.puzzleClass.width*boxSize),(self.puzzleClass.height*boxSize)))
                x.static = True
                self.table_sprite.add(x)
                
                for i in range(len(rawBoard)):
                    
                    if rawBoard[i] != filler:
                        
                        x = str(rawBoard[i])
                        
                        if rawBoard[i] == blank:
                            x = ''
                        
                        self.boardBlocks[i] = TextBorderKakuro(x, 
                                                 pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                 size=dt(boxSize+1,boxSize+1), 
                                                 f_typo= typo,
                                                 id=i)
                        
                        if rawBoard[i] == blank:
                            self.boardBlocks[i].static = False
                            self.checkList.append(i)
                        
                    else:
                        
                        if i in clues:
                            down = str(clues[i][0]) if clues[i][0] != None else ''
                            right = str(clues[i][1]) if clues[i][1] != None else ''
                            self.boardBlocks[i] = KakuroClues(down, right, 
                                                     pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                     size=dt(boxSize+1,boxSize+1), 
                                                     bg_color=Color.ULTRAGRAY, 
                                                     f_typo = typo,
                                                     id=i)
                        
                        else:
                            self.boardBlocks[i] = ColorBoxCross(Color.ULTRAGRAY,
                                                       pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                       size=dt(boxSize+1,boxSize+1), 
                                                       id=i)
                    
                    
                    self.table_sprite.add(self.boardBlocks[i])
             
            self.SceneGeneral()
            
            self.moves = 0
            
            
            self.lastTick = pygame.time.get_ticks()
            
            self.general_GameTitle.set_Text("Kakuro")
            self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
            
            self.curBlock = None
            self.width = self.puzzleClass.width
            
            
            self.keys_counter = self.puzzleClass.getKey(0)
            self.keys_cell = self.puzzleClass.getKey(1)
            
            
            build_Table()
            
            self.curNum = self.checkList[0]
            
            self.movesBeforeChecking = 0
            
            build_Loaders()
            
            self.movesBeforeChecking -= 1
            
            self.countCheck = 0
            if self.autoCheck != None:
                self.countCheckMax = self.autoCheck 
            else:
                self.countCheckMax = 24*60*60
            
            
            #build_ClueWindow()
            
            
            loop()
        
        
        def printStart():
            
            def printInit(count):
            
                def build_Table():
                    
                    self.checkList = []
                
                    self.boardBlocks = {}
                    self.table_sprite = pygame.sprite.Group()
                    
                    boxSize = int(self.boxSize)
                    
                    self.left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                    
                    typo = 0
                    if boxSize > 45:
                        typo = font_typo["Comfortaa"]["Regular"]
                    else:
                        typo = font_typo["Comfortaa"]["XSmall"]
                    
                    width = self.puzzleClass.width
                    rawBoard = self.puzzleClass.getBoard(mode=1)
                    filler = self.puzzleClass.filler
                    blank = self.puzzleClass.white
                    
                    clues = self.puzzleClass.getKey(2)
                    
                    self.boardWidth =(self.puzzleClass.width*boxSize)
                    self.boardHeight = (self.puzzleClass.height*boxSize)
                    
                    x = ColorBox(Color.LIGHTGRAY,
                           pos=dt(self.left_pad, 75),
                           size=dt(self.boardWidth,self.boardHeight))
                    x.static = True
                    self.table_sprite.add(x)
                    
                    for i in range(len(rawBoard)):
                        
                        if rawBoard[i] != filler:
                            
                            x = str(rawBoard[i])
                            
                            if rawBoard[i] == blank:
                                x = ''
                            
                            self.boardBlocks[i] = TextBorderKakuro(x, 
                                                     pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                     size=dt(boxSize+1,boxSize+1), 
                                                     bd_color = Color.LIGHTLIGHTGRAY,
                                                     f_typo= typo,
                                                     id=i)
                            
                            if rawBoard[i] == blank:
                                self.boardBlocks[i].static = False
                                self.checkList.append(i)
                            
                        else:
                            
                            if i in clues:
                                down = str(clues[i][0]) if clues[i][0] != None else ''
                                right = str(clues[i][1]) if clues[i][1] != None else ''
                                self.boardBlocks[i] = KakuroClues(down, right, 
                                                     pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                     size=dt(boxSize+1,boxSize+1), 
                                                     bg_color=Color.ULTRAGRAY, 
                                                     f_typo = typo,
                                                     id=i)
                        
                            else:
                                self.boardBlocks[i] = ColorBoxCross(Color.ULTRAGRAY,
                                                           pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                           size=dt(boxSize+1,boxSize+1), 
                                                           id=i)
                        
                        
                        self.table_sprite.add(self.boardBlocks[i])
                    
    
                def print_Table():
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                    name = self.boardLoc + "{1}_{0}_BOARD.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75,
                                 self.boardWidth,
                                  self.boardHeight,
                                  result_width=self.resultingSize)
                    
                def get_Solution():
                    filler = self.puzzleClass.filler
                    checkBoard = self.puzzleClass.getBoard()
                    for index,item in enumerate(checkBoard):
                        if item != filler:
                            if self.boardBlocks[index].text != item:
                                self.boardBlocks[index].setContent(str(item), color ="Black2None", force=True)
                
                def print_Solution():
                    
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                        
                    name = self.answerLoc + "{1}_{0}_SOLUTION.png".format(count, self.puzzleClass.title)    
                    
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad, 75,
                                 self.boardWidth,
                                  self.boardHeight,
                                  result_width=self.resultingSize)
                   
                self.width = self.puzzleClass.width
                
                self.keys_counter = self.puzzleClass.getKey(0)
                self.keys_cell = self.puzzleClass.getKey(1)
                    
                #renew table
                
                build_Table()
                
                #print board
                
                print_Table()
                
                #get solution to board
                
                get_Solution()
                
                self.printProcess(curMode=1, curProg=None, loadPercent=None)
                
                #print solution
                
                print_Solution()

                self.printProcess(curMode=2, curProg=None, loadPercent=None)

            self.printProcess = self.ScenePrintProcess(self.printAmount)
            self.printProcess(curMode=0, curProg=1, loadPercent=0)

            for i in range(self.printAmount):
                self.puzzleClass.re_init()
                self.puzzleClass.setBoard(self.puzzleClass.width, self.puzzleClass.height, ".")
                self.puzzleClass.buildBoard()
                
                printInit(i)
                self.printProcess(curMode=0, curProg=i+1, loadPercent=i/self.printAmount)
                
            self.printProcess(curMode=2, curProg=i+1, loadPercent=1)
            
            pygame.time.wait(1000)
            
            self.run = ''
        
        
        def show_solution():
                
            filler = self.puzzleClass.filler
            checkBoard = self.puzzleClass.getBoard()
            for index,item in enumerate(checkBoard):
                if item != filler:
                    if self.boardBlocks[index].text != item:
                        self.boardBlocks[index].setContent(str(item), color ="RedNone", force=True)
            
                
            loop_display()
            
        def checkBoard(idx):
            
            checkable = {}
            
            curVal = self.boardBlocks[idx].text
            
            totSum = {}
            
            for checker in self.keys_cell[idx]:
                if checker == None:
                    continue
                totSum[checker] = 0
                checkable[checker] = True
                checkerData = self.keys_counter[checker]
                for cell in checkerData[0]:
                    
                    if (self.boardBlocks[cell].text) != '':
                        if idx != cell:
                            if self.boardBlocks[cell].text == curVal:
                                self.boardBlocks[cell].setMode(0)
                        totSum[checker] += int(self.boardBlocks[cell].text)
                    else:
                        checkable[checker] = False
            
            for checker in self.keys_cell[idx]:
                if checker == None:
                    continue
                if checkable[checker]:
                    checkerData = self.keys_counter[checker]
                    for cell in checkerData[0]:
                        if (totSum[checker] != checkerData[1]):
                            self.boardBlocks[cell].setMode(0)
        
        def checkBoardAll(draw = True, mode=2):
            
            if mode == 1: #Check by comparing your answers into the generated board key
                toRed = []
                
                finish = True
                
                filler = self.puzzleClass.filler
                checkBoard = self.puzzleClass.getBoard()
                for index,item in enumerate(checkBoard):
                    if item != filler:
                        if self.boardBlocks[index].text == '':
                            finish = False
                            continue
                        if self.boardBlocks[index].text != item:
                            toRed.append(index)
                            finish = False
                
                if draw:         
                    for item in toRed:
                        self.boardBlocks[item].setMode(0)
                
                return finish
            
            elif mode == 2: #Check by getting the sum of everything and if nothing has error
                toRed = []
                
                finish = True
                
                filler = self.puzzleClass.filler
                
                for key, checker in self.keys_counter.items():
                    checkerList = checker[0]
                    
                    finishLine = True
                    
                    totSum = 0
                    for cell in checkerList:
                        if self.boardBlocks[cell].text != '':
                            totSum += int(self.boardBlocks[cell].text) 
                        else:
                            finish = False
                            finishLine = False
                    
                    
                    
                    if not finishLine: continue
                    
                    else:
                        if totSum != checker[1]:
                            finish = False
                            for cell in checkerList:
                                toRed.append(cell)
                        
                
                if draw:         
                    for item in set(toRed):
                        self.boardBlocks[item].setMode(0)
                
                return finish
            
        def loop_control():
            
            def setCurBlock(item=None, index=None):
                if self.curBlock != None:
                        #Clear the last selected
                        self.curBlock.ready = False
                        self.curBlock.update()
                    
                    #Set the current selected
                self.curBlock = item
                self.curBlock.ready = True
                self.curBlock.update()
                self.curNum = index
                
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = ''
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        #pygame.image.save(self.puzzleHolder, "Sample.png")
                        #self.run = ''
                        pass
                    
                    elif event.key == pygame.K_LEFT:
                        if (self.curNum - 1) in self.checkList:
                            self.curNum -= 1
                            setCurBlock(self.boardBlocks[self.curNum], self.curNum )
                        
                    elif event.key == pygame.K_RIGHT:
                        if (self.curNum + 1) in self.checkList:
                            self.curNum += 1
                            setCurBlock(self.boardBlocks[self.curNum], self.curNum )         
                                        
                    elif event.key == pygame.K_UP:
                        if (self.curNum - self.width) in self.checkList:
                            self.curNum -= self.width
                            setCurBlock(self.boardBlocks[self.curNum], self.curNum )
                                                  
                    elif event.key == pygame.K_DOWN:
                        if (self.curNum + self.width) in self.checkList:
                            self.curNum += self.width
                            setCurBlock(self.boardBlocks[self.curNum], self.curNum )
                        
                    elif event.key == pygame.K_BACKSPACE:
                        self.curBlock.setContent("")
                        self.moves += 1
                        
                    else:
                        x = event.unicode
                        if x.isnumeric() and x != '0':
                            self.curBlock.setContent(x)
                            checkBoard(self.curBlock.id)
                            self.moves += 1
                            self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
                            if self.moves > self.movesBeforeChecking:
                                if checkBoardAll(False):
                                    self.run = '0'
            
                if 4 <= event.type <= 6: #Mouse Button Move and Click Up and Down
                    for item in self.mouseUpdateList:
                        if not self.click:
                            if item.mouseDetect():
                                setCurBlock(item, item.id)
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = False
                                
        def loop_logic():
            
            for item in self.updateList:
                if item.updating == False:
                    continue
                item.update()
            
            if pygame.time.get_ticks() - self.lastTick > 1000:
                self.timer -= 1  
                self.countCheck += 1
                self.general_GameTimer.set_Text("Time: {0}:{1}".format(self.timer//60, self.timer%60))
                self.lastTick = pygame.time.get_ticks()
                if self.timer < 1:
                    show_solution()
                    self.run = '1'
                if self.countCheck >= self.countCheckMax:
                    self.countCheck = 0
                    checkBoardAll(True)
                    
        def loop_display():
            self.puzzleHolder.fill(Color.WHITE)
            
            self.general_sprite.draw(self.puzzleHolder)
            self.table_sprite.draw(self.puzzleHolder)
            
            self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
            
            pygame.display.flip()
        

        
        def loop():
            while self.run == 'D':
                loop_control()
                loop_logic()
                loop_display()
                
                self.clock.tick(Screen.FPS)
        
        if self.printMode:
            printStart()
        else:
            start()
    
    def Hidato(self):
        
        def start():
            
            def build_Loaders():
                
                self.updateList = []
                self.mouseUpdateList = []
                
                for item in self.general_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                        
                for item in self.table_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                
                for item in self.table_sprite:
                    if callable(getattr(item, 'mouseDetect', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.mouseUpdateList.append(item)
            
            def build_Table():
                
                self.boardBlocks = {}
                self.table_sprite = pygame.sprite.Group()
                
                boxSize = int(self.boxSize)
                
                left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                
                typo = 0
                if boxSize > 30:
                    typo = font_typo["Comfortaa"]["Regular"]
                else:
                    typo = font_typo["Comfortaa"]["XSmall"]
                
                width = self.puzzleClass.width
                rawBoard = self.puzzleClass.getBoard(mode=1)
                filler = self.puzzleClass.filler
                blank = self.puzzleClass.hidden
                
                x = ColorBox(Color.BLACK,
                       pos=dt(left_pad, 75),
                       size=dt((self.puzzleClass.width*boxSize),(self.puzzleClass.height*boxSize)))
                x.static = True
                
                self.table_sprite.add(x)
                
                for i in range(len(rawBoard)):
                    
                    if rawBoard[i] != filler:
                        if rawBoard[i] == blank:
                            self.boardBlocks[i] = TextBorderKakuro(rawBoard[i].replace(blank, ''), 
                                                         pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                         size=dt(boxSize+1,boxSize+1), 
                                                         bg_color=[Color.WHITE, Color.LIGHTLIGHTGRAY, Color.YELLOW, Color.RED, Color.BLUE], 
                                                         f_typo= typo,
                                                         id=i)
                            
                        else:
                            self.boardBlocks[i] = TextBorderKakuro(rawBoard[i].replace(blank, ''), 
                                                         pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                         size=dt(boxSize+1,boxSize+1), 
                                                         bg_color=[Color.WHITE, Color.WHITE, Color.YELLOW, Color.RED, Color.BLUE], 
                                                         f_typo= typo,
                                                         id=i)
                            self.boardBlank.remove(int(rawBoard[i]))
                    else:
                        
                        self.boardBlocks[i] = ColorBox(Color.BLACK,
                                                       pos=dt(left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                       size=dt(boxSize+1,boxSize+1), 
                                                       id=i)
                    
                    
                    self.table_sprite.add(self.boardBlocks[i])
            
            def build_DirectionIndication():
                self.directionUI = []
                
                self.directionUI.append(TextBox("Going Up", 
                                                pos = (0,150),
                                                size = (150,50),
                                                f_typo=font_typo["Open Sans"]["Small"]))
                self.directionUI.append(TextBox("Going Down", 
                                                pos = (0,400),
                                                size = (150,50),
                                                f_typo=font_typo["Open Sans"]["Small"]))
                self.directionUI.append(TextBox("25", 
                                                pos = (0,200),
                                                size = (150,200),
                                                f_typo=font_typo["Comfortaa"]["BigRegular"]))
                self.directionUI.append(TextBox("Press UP and Down to change increment direction", 
                                                pos = (0,self.localScreenHeight-25),
                                                size = (800,25),
                                                f_typo=font_typo["Comfortaa"]["Small"]))
                
                for i in self.directionUI:
                    self.general_sprite.add(i)
                    
            
            self.SceneGeneral()
            
            self.moves = 0
            
            self.lastTick = pygame.time.get_ticks()
            
            self.general_GameTitle.set_Text("Hidato")
            self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
            
            self.boardBlank = [i for i in range(1,(self.puzzleClass.width-2) * (self.puzzleClass.width-2)+1)]
            
            self.blank = self.puzzleClass.hidden
            
            self.gameWidth = self.puzzleClass.width
            self.key = self.puzzleClass.getKey()
            
            self.boardKey = self.puzzleClass.getBoard()
            
            self.direction = 1
            
            
            build_DirectionIndication()
            
            self.directionUI[1].set_Text('')
            
            build_Table()
            
            self.boardBlankChecker = list(self.boardBlank)
            if self.direction==1:
                self.curIndex = self.boardBlank[0]  
            else: 
                self.curIndex = self.boardBlank[len(self.boardBlank)-1]
                
            self.directionUI[2].set_Text(str(self.curIndex))
            
            build_Loaders()
            
            
            
            loop()
        
        
        def printStart():
            
            def printInit(count):
            
                def build_Table():
                    
                    self.boardBlocks = {}
                    self.table_sprite = pygame.sprite.Group()
                    
                    boxSize = int(self.boxSize)
                    
                    self.left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                    
                    typo = 0
                    if boxSize > 30:
                        typo = font_typo["Comfortaa"]["Regular"]
                    else:
                        typo = font_typo["Comfortaa"]["XSmall"]
                    
                    width = self.puzzleClass.width
                    rawBoard = self.puzzleClass.getBoard(mode=1)
                    filler = self.puzzleClass.filler
                    blank = self.puzzleClass.hidden
                    
                    self.boardWidth =(self.puzzleClass.width*boxSize)
                    self.boardHeight = (self.puzzleClass.height*boxSize)
                    
                    x = ColorBox(Color.BLACK2,
                           pos=dt(self.left_pad, 75),
                           size=dt(self.boardWidth,self.boardHeight))
                    x.static = True
                    self.table_sprite.add(x)
                    
                    self.table_sprite.add(x)
                    
                    for i in range(len(rawBoard)):
                        
                        if rawBoard[i] != filler:
                            if rawBoard[i] == blank:
                                self.boardBlocks[i] = TextBorderKakuro(rawBoard[i].replace(blank, ''), 
                                                             pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                             size=dt(boxSize+1,boxSize+1), 
                                                             bg_color=[Color.WHITE, Color.LIGHTLIGHTGRAY, Color.YELLOW, Color.RED, Color.BLUE], 
                                                             f_typo= typo,
                                                             id=i)
                                
                            else:
                                self.boardBlocks[i] = TextBorderKakuro(rawBoard[i].replace(blank, ''), 
                                                             pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)), 
                                                             size=dt(boxSize+1,boxSize+1), 
                                                             bg_color=[Color.WHITE, Color.WHITE, Color.YELLOW, Color.RED, Color.BLUE], 
                                                             f_typo= typo,
                                                             id=i)
                                self.boardBlank.remove(int(rawBoard[i]))
                        else:
                            
                            self.boardBlocks[i] = ColorBox(Color.BLACK,
                                                           pos=dt(self.left_pad+(i%width*boxSize), 75+(i//width*boxSize)),
                                                           size=dt(boxSize+1,boxSize+1), 
                                                           id=i)
                        
                        
                        self.table_sprite.add(self.boardBlocks[i])
                    
                    startEnd = self.puzzleClass.getKey(1)
                    
                    for i, value in startEnd.items():
                        #self.boardBlocks[value].bgcolor[0] = Color.LIGHTLIGHTLIGHTGRAY
                        self.boardBlocks[value].significant = True
                        self.boardBlocks[value].update()
                    
                def print_Table():
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                    
                    '''for i, value in startEnd.items():
                        draw_bordered_rounded_rect(self.puzzleHolder, self.boardBlocks[value].rect, Color.WHITE, Color.BLACK2, self.boxSize//3, 2)'''
                    
                    name = self.boardLoc + "{1}_{0}_BOARD.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad+self.boxSize, 75+self.boxSize,
                                 self.boardWidth-self.boxSize*2,
                                  self.boardHeight-self.boxSize*2,
                                  result_width=self.resultingSize)
                    
                def get_Solution():
                    for indx,itemx in self.boardBlocks.items():
                        if hasattr(itemx, 'text'):
                            if itemx.text != self.boardKey[indx]:
                                itemx.setContent(str(self.boardKey[indx]), color="RedNone", force = True)
                
                def print_Solution():
                    
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                        
                    name = self.answerLoc + "{1}_{0}_SOLUTION.png".format(count, self.puzzleClass.title)    
                    
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad+self.boxSize, 75+self.boxSize,
                                 self.boardWidth-self.boxSize*2,
                                  self.boardHeight-self.boxSize*2,
                                  result_width=self.resultingSize)
                   
                self.boardBlank = [i for i in range(1,(self.puzzleClass.width-2) * (self.puzzleClass.width-2)+1)]
            
                self.blank = self.puzzleClass.hidden
                
                self.gameWidth = self.puzzleClass.width
                self.key = self.puzzleClass.getKey()
                
                self.boardKey = self.puzzleClass.getBoard()
                
                #renew table
                
                build_Table()
                
                #print board
                
                print_Table()
                
                #get solution to board
                
                get_Solution()
                
                self.printProcess(curMode=1, curProg=None, loadPercent=None)
                
                #print solution
                
                print_Solution()

                self.printProcess(curMode=2, curProg=None, loadPercent=None)

            self.printProcess = self.ScenePrintProcess(self.printAmount)
            self.printProcess(curMode=0, curProg=1, loadPercent=0)

            for i in range(self.printAmount):
                self.puzzleClass.re_init()
                self.puzzleClass.setBoard(self.puzzleClass.width, self.puzzleClass.height, ".")
                self.puzzleClass.setRandomRate(self.puzzleClass.origRandomRate)
                self.puzzleClass.buildBoard()
                
                printInit(i)
                self.printProcess(curMode=0, curProg=i+1, loadPercent=i/self.printAmount)
                
            self.printProcess(curMode=2, curProg=i+1, loadPercent=1)
            
            pygame.time.wait(1000)
            
            self.run = ''
        
        
        def show_solution():
            for indx,itemx in self.boardBlocks.items():
                if hasattr(itemx, 'text'):
                    if itemx.text != self.boardKey[indx]:
                        itemx.setContent(str(self.boardKey[indx]), color="RedNone", force = True)
            
            loop_display()

        def checkWin():
            if len(self.boardBlank) == 0:
                self.run = '0'
        
        def loop_control():
            
            def getNextVal(num=0, Falsify = True):
                self.curIndex = num
                while self.curIndex not in self.boardBlank:
                    self.curIndex += self.direction
                    if 0 > self.curIndex  or self.curIndex > self.gameWidth*self.gameWidth:
                        self.curIndex = num
                        break
                
            def getLegalMoves(index):
                rootNum = str(self.curIndex - self.direction)
                #print(rootNum)
                legal = False
                
                toCheck = [
                    index - 1, 
                    index + 1, 
                    index + self.gameWidth, 
                    index - self.gameWidth,]
                
                if self.diagonals:
                    toCheck += [
                    index + self.gameWidth+1,
                    index + self.gameWidth-1,
                    index - self.gameWidth+1,
                    index - self.gameWidth-1,]
                
                for place in toCheck:
                    if place in self.key:
                        if rootNum == self.boardBlocks[place].text:
                            legal = True
                            
                return legal
                    
            def findLegalMove(num):
                for i in self.mouseUpdateList:
                    if i.text == num:
                        i.setMode(0)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = ''
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        #pygame.image.save(self.puzzleHolder, "Sample.png")
                        self.run = ''
                    elif event.key == pygame.K_UP:
                        self.direction = 1
                        self.directionUI[0].set_Text('Going Up')
                        self.directionUI[1].set_Text('')
                        self.directionUI[2].set_Text(str(self.curIndex))
                        getNextVal()
                    elif event.key == pygame.K_DOWN:
                        self.direction = -1
                        self.directionUI[0].set_Text('')
                        self.directionUI[1].set_Text('Going Down')
                        getNextVal(self.gameWidth*self.gameWidth)
                        self.directionUI[2].set_Text(str(self.curIndex))
            
                if 4 <= event.type <= 6: #Mouse Button Move and Click Up and Down
                    for item in self.mouseUpdateList:
                        if not self.click:
                            if item.mouseDetect():
                                if item.text == '':
                                    if getLegalMoves(item.id):
                                        item.setContent(str(self.curIndex), force = True)
                                        self.boardBlank.remove(self.curIndex)
                                        getNextVal(int(item.text))
                                    else:
                                        findLegalMove(str(self.curIndex-self.direction))
                                    
                                elif int(item.text) in self.boardBlankChecker:
                                    self.boardBlank.append(int(item.text))
                                    getNextVal(int(item.text))
                                    item.setContent('', force = True)
                                    
                                else:
                                    getNextVal(int(item.text)-1)
                                self.directionUI[2].set_Text(str(self.curIndex))
                                self.moves += 1
                                self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
                                checkWin()
                                    
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = False
                                
        def loop_logic():
            
            for item in self.updateList:
                if item.updating == False:
                    continue
                item.update()

            
            if pygame.time.get_ticks() - self.lastTick > 1000:
                self.timer -= 1  
                self.general_GameTimer.set_Text("Time: {0}:{1}".format(self.timer//60, self.timer%60))
                self.lastTick = pygame.time.get_ticks()
                if self.timer < 1:
                    show_solution()
                    self.run = '1'
                    
    
        def loop_display():
            self.puzzleHolder.fill(Color.WHITE)
            
            self.general_sprite.draw(self.puzzleHolder)
            self.table_sprite.draw(self.puzzleHolder)
            
            self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
            
            pygame.display.flip()
        

        
        def loop():
            while self.run == 'E':
                loop_control()
                loop_logic()
                loop_display()
                
                self.clock.tick(Screen.FPS)
        
        if self.printMode:
            printStart()
        else:
            start()
        
    def Nonogram(self):
        
        def start():
            
            def build_Loaders():
                
                self.updateList = []
                self.mouseUpdateList = []
                
                for item in self.general_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                        
                for item in self.table_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                
                for item in self.table_sprite:
                    if callable(getattr(item, 'mouseDetect', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.mouseUpdateList.append(item)
            
            def build_Table():
                
                self.boardBlocks = {}
                self.table_sprite = pygame.sprite.Group()
                
                boxSize = int(self.boxSize)
                
                left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                
                typo = 0
                if boxSize > 15:
                    typo = font_typo["Comfortaa"]["Regular"]
                else:
                    typo = font_typo["Comfortaa"]["Small"]
                    #self.ypad = 80
                
                rawBoard = self.puzzleClass.getBoard(mode=1)
                width = self.puzzleClass.width
                
                ypad = self.ypad
                
                x = ColorBox(Color.BLACK,
                       pos=dt(left_pad, ypad),
                       size=dt((self.puzzleClass.width*boxSize),(self.puzzleClass.height*boxSize)))
                x.static = True
                self.table_sprite.add(x)
                
                for i in range(len(rawBoard)):
                    self.boardBlocks[i] = NonogramBlocks('', 
                                             pos=dt(left_pad+(i%width*boxSize), ypad+(i//width*boxSize)), 
                                             size=dt(boxSize+1,boxSize+1), 
                                             f_typo= typo,
                                             id=i)
                        
                    self.table_sprite.add(self.boardBlocks[i])
                        
            def build_Clues():
                self.boardCluesY = {}
                self.boardCluesX = {}
                
                boxSize = int(self.boxSize)
                width = self.puzzleClass.width
                
                left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                
                typo = 0
                if boxSize > 25:
                    typo = font_typo["Comfortaa"]["Regular"]
                else:
                    typo = font_typo["Comfortaa"]["XSmall"]
                
                ypad = self.ypad
                
                #Build Vertical
                for keys, items in self.keyClues[0].items():
                    clue = len(items.strip().split(' '))
                    
                    self.boardCluesY[keys] = NonogramClues(items, 
                                             pos=dt(left_pad+(keys%width*boxSize), ypad-(boxSize*clue)*0.8+(keys//width*boxSize)), 
                                             size=dt(boxSize,boxSize*clue*0.8),
                                             f_typo= typo,
                                             id=keys,
                                             direction="vert")
                        
                    self.table_sprite.add(self.boardCluesY[keys])
                
                #Build Horizontal
                for keys, items in self.keyClues[1].items():
                    clue = len(items.strip().split(' '))
                    
                    self.boardCluesX[keys] = NonogramClues(items, 
                                             pos=dt(left_pad-(boxSize*clue)*0.8, ypad+(keys*boxSize)), 
                                             size=dt(boxSize*clue*0.8,boxSize),
                                             f_typo= typo,
                                             id=keys,
                                             direction="hori")
                    
                    self.table_sprite.add(self.boardCluesX[keys])
                        
            self.SceneGeneral()
            
            self.moves = 0
            
            self.lastTick = pygame.time.get_ticks()
            
            self.keyClues = [self.puzzleClass.getKeys(0), self.puzzleClass.getKeys(1)]
            
            self.general_GameTitle.set_Text("Nonogram")
            self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
            
            self.boardWidth = self.puzzleClass.width
            self.boardHeight = self.puzzleClass.height
            
            self.white = self.puzzleClass.paint
            
            self.movesBeforeChecking = 0
            
            self.boardKeys = self.puzzleClass.getBoard()
            
            for i in self.boardKeys:
                if i == self.white:
                    self.movesBeforeChecking += 1
                    
            self.movesBeforeChecking = int(self.movesBeforeChecking * 0.90)
            
            build_Table()
            
            build_Clues()
            
            build_Loaders()
            
            
            loop()
        
        
        def printStart():
            
            def printInit(count):
            
                def build_Table():
                    
                    self.boardBlocks = {}
                    self.table_sprite = pygame.sprite.Group()
                    
                    boxSize = int(self.boxSize)
                    
                    self.left_pad = (self.localScreenWidth - boxSize * self.puzzleClass.width) // 2
                    
                    typo = 0
                    if boxSize > 15:
                        typo = font_typo["Comfortaa"]["Regular"]
                    else:
                        typo = font_typo["Comfortaa"]["Small"]
                        #self.ypad = 80
                    
                    rawBoard = self.puzzleClass.getBoard(mode=1)
                    width = self.puzzleClass.width
                    
                    ypad = self.ypad
                    
                    self.boardWidth =(self.puzzleClass.width*boxSize)
                    self.boardHeight = (self.puzzleClass.height*boxSize)
                    
                    x = ColorBox(Color.BLACK2,
                           pos=dt(self.left_pad, ypad),
                           size=dt((self.puzzleClass.width*boxSize),(self.puzzleClass.height*boxSize)))
                    x.static = True
                    self.table_sprite.add(x)
                    
                    for i in range(len(rawBoard)):
                        self.boardBlocks[i] = NonogramBlocks('', 
                                                 pos=dt(self.left_pad+(i%width*boxSize), ypad+(i//width*boxSize)), 
                                                 size=dt(boxSize+1,boxSize+1), 
                                                 bd_width=1,
                                                 f_typo= typo,
                                                 id=i)
                            
                        self.table_sprite.add(self.boardBlocks[i])

                def build_Clues():
                    self.boardCluesY = {}
                    self.boardCluesX = {}
                    
                    boxSize = int(self.boxSize)
                    width = self.puzzleClass.width
            
                    typo = 0
                    if boxSize > 25:
                        typo = font_typo["Comfortaa"]["Regular"]
                    else:
                        typo = font_typo["Comfortaa"]["XSmall"]
                    
                    ypad = self.ypad
                    
                    self.maxYNeg = 0
                    self.maxXNeg = 0
                    
                    #Build Vertical
                    for keys, items in self.keyClues[0].items():
                        clue = len(items.strip().split(' '))
                        self.maxYNeg = max(self.maxYNeg, (boxSize*clue)*0.82)
                        self.boardCluesY[keys] = NonogramClues(items, 
                                                 pos=dt(self.left_pad+(keys%width*boxSize), ypad-(boxSize*clue)*0.82+(keys//width*boxSize)), 
                                                 size=dt(boxSize,boxSize*clue*0.8),
                                                 f_typo= typo,
                                                 id=keys,
                                                 direction="vert")
                            
                        self.table_sprite.add(self.boardCluesY[keys])
                    
                    #Build Horizontal
                    for keys, items in self.keyClues[1].items():
                        clue = len(items.strip().split(' '))
                        self.maxXNeg = max(self.maxXNeg, (boxSize*clue)*0.82)
                        self.boardCluesX[keys] = NonogramClues(items, 
                                                 pos=dt(self.left_pad-(boxSize*clue)*0.82, ypad+(keys*boxSize)), 
                                                 size=dt(boxSize*clue*0.8,boxSize),
                                                 f_typo= typo,
                                                 id=keys,
                                                 direction="hori")
                        
                        self.table_sprite.add(self.boardCluesX[keys])
                    
                def print_Table():
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                    name = self.boardLoc + "{1}_{0}_BOARD.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad-self.maxXNeg*1.2, self.ypad-self.maxYNeg*1.2,
                                 self.boardWidth+self.maxXNeg*1.5,
                                  self.boardHeight+self.maxYNeg*1.5,
                                  result_width=self.resultingSize)
                    
                def get_Solution():
                    for i, item in enumerate(self.boardKeys):
                        if item == self.white:
                            if self.boardBlocks[i].mode != 1:
                                self.boardBlocks[i].mode = 2
                                self.boardBlocks[i].update()
                
                def print_Solution():
                    
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                        
                    name = self.answerLoc + "{1}_{0}_SOLUTION.png".format(count, self.puzzleClass.title)    
                    
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.left_pad-self.maxXNeg*1.2, self.ypad-self.maxYNeg*1.2,
                                 self.boardWidth+self.maxXNeg*1.5,
                                  self.boardHeight+self.maxYNeg*1.5,
                                  result_width=self.resultingSize)
                   
                   
                self.keyClues = [self.puzzleClass.getKeys(0), self.puzzleClass.getKeys(1)]
            
                self.boardWidth = self.puzzleClass.width
                self.boardHeight = self.puzzleClass.height
                
                self.white = self.puzzleClass.paint
                
                self.boardKeys = self.puzzleClass.getBoard()
                
                #renew table
                
                build_Table()
                
                build_Clues()
                
                #print board
                
                print_Table()
                
                #get solution to board
                
                get_Solution()
                
                self.printProcess(curMode=1, curProg=None, loadPercent=None)
                
                #print solution
                
                print_Solution()

                self.printProcess(curMode=2, curProg=None, loadPercent=None)

            self.printProcess = self.ScenePrintProcess(self.printAmount)
            self.printProcess(curMode=0, curProg=1, loadPercent=0)

            for i in range(self.printAmount):
                self.puzzleClass.re_init()
                self.puzzleClass.loadNextImageQueue()
                self.puzzleClass.buildBoard()
                
                
                printInit(i)
                self.printProcess(curMode=0, curProg=i+1, loadPercent=i/self.printAmount)
                
            self.printProcess(curMode=2, curProg=i+1, loadPercent=1)
            
            pygame.time.wait(1000)
            
            self.run = ''
        
        
        def show_solution():
            
            for i, item in enumerate(self.boardKeys):
                if item == self.white:
                    if self.boardBlocks[i].mode != 1:
                        self.boardBlocks[i].mode = 2
                        self.boardBlocks[i].update()
                    
            
            loop_display()
            
        
        def loop_control():
            
            def checkBoard():
                self.boardWidth
                
                #Check horizontally 
                for y, item in self.keyClues[1].items():
                    
                    forChecking = ""
                    
                    item = item.strip().split(' ')
                    
                    counter = 0
                    counting = False
                    
                    for x in range(self.boardWidth):
                        if self.boardBlocks[y*self.boardWidth + x].mode == 1:
                            if counting:
                                counter += 1
                            else: 
                                counting = True
                                counter = 1
                        elif counting:
                            forChecking += "{0} ".format(counter)
                            counting = False
                            
                    if counting: 
                        forChecking += "{0} ".format(counter)
                        counting = False
                    
                    forChecking = forChecking.strip().split(' ')
                    
                    hasError = False
                    
                    if len(forChecking) > len(item):
                        hasError = True
                    
                    for i in range(min(len(forChecking), len(item))):
                        if forChecking[i] == '':
                            continue
                        if int(forChecking[i]) > int(item[i]):
                            hasError = True
                    
                    
                    if hasError:
                        self.boardCluesX[y].setMode(0)
                        
                #Check vertically 
                
                counting = False
                for x, item in self.keyClues[0].items():
                    
                    forChecking = ""
                    
                    item = item.strip().split(' ')
                    
                    counter = 0
                    counting = False
                    
                    for y in range(self.boardHeight):
                        if self.boardBlocks[y*self.boardWidth + x].mode == 1:
                            if counting:
                                counter += 1
                            else: 
                                counting = True
                                counter = 1
                        elif counting:
                            forChecking += "{0} ".format(counter)
                            counting = False
                        
                    if counting: 
                        forChecking += "{0} ".format(counter)
                        counting = False
                    
                    forChecking = forChecking.strip().split(' ')
                    
                    hasError = False
                    
                    if len(forChecking) > len(item):
                        hasError = True
                    
                    for i in range(min(len(forChecking), len(item))):
                        if forChecking[i] == '':
                            continue
                        if int(forChecking[i]) > int(item[i]):
                            hasError = True
                    
                    
                    if hasError:
                        self.boardCluesY[x].setMode(0)
                      
            def checkBoardWin():
                done = True
                for i, item in enumerate(self.boardKeys):
                    if item == self.white:
                        if self.boardBlocks[i].mode != 1:
                            done = False
                        
                if done:
                    self.run = '0'
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = ''
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        #pygame.image.save(self.puzzleHolder, "Sample.png")
                        self.run = ''
            
                if 4 <= event.type <= 6: #Mouse Button Move and Click Up and Down
                    for item in self.mouseUpdateList:
                        if not self.click:
                            if item.mouseDetect():
                                item.mode ^= 1
                                self.moves += 1
                                self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
                                item.update()
                                
                                if self.moves > self.movesBeforeChecking:
                                    checkBoardWin()
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #self.click = True
                    pass
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    #self.click = False
                    checkBoard()
                                
        def loop_logic():
            
            for item in self.updateList:
                if item.updating == False:
                    continue
                item.update()
            
            if pygame.time.get_ticks() - self.lastTick > 1000:
                self.timer -= 1  
                self.general_GameTimer.set_Text("Time: {0}:{1}".format(self.timer//60, self.timer%60))
                self.lastTick = pygame.time.get_ticks()
                if self.timer < 1:
                    show_solution()
                    self.run = '1'
                    
    
        def loop_display():
            self.puzzleHolder.fill(Color.WHITE)
            
            self.general_sprite.draw(self.puzzleHolder)
            self.table_sprite.draw(self.puzzleHolder)
            
            self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
            
            pygame.display.flip()
        

        
        def loop():
            while self.run == 'F':
                loop_control()
                loop_logic()
                loop_display()
                
                self.clock.tick(Screen.FPS)
         
        if self.printMode:
            printStart()
        else:
            start()
         
    def Cryptogram(self):
        
        def start():
            
            def build_Loaders():
                
                self.updateList = []
                self.mouseUpdateList = []
                
                for item in self.general_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                        
                for item in self.table_sprite:
                    if callable(getattr(item, 'update', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.updateList.append(item)
                
                for item in self.table_sprite:
                    if callable(getattr(item, 'mouseDetect', None)):
                        if hasattr(item, 'static'):
                            if item.static == True:
                                continue
                        self.mouseUpdateList.append(item)
            
            def build_Table():
                
                self.boardBlocks = {}
                self.table_sprite = pygame.sprite.Group()
                
                curLen = 0
                curLine = 0
                i = 0
                
                startX = (self.wholeSIZE['X'] - self.wrapLength * self.boxSizeX) / 2
                startY = (self.wholeSIZE['Y'] - self.wrapsCut * self.boxSizeY) / 2
                
                self.puzzleHolder = pygame.surface.Surface((self.localScreenWidth,self.wholeSIZE['Y']+100*self.wrapsCut))
                
                padding = 25
                x = (TextBorder('', dt(startX-padding, startY), 
                        size=dt(self.boxSizeX * (self.wrapLength+1)+padding*2, self.boxSizeY * (self.wrapsCut+2)+padding*2), 
                        bg_color=Color.BLACK, 
                        id = None))
                x.static = True
                self.table_sprite.add(x)
                
                if self.puzzleClass.author != "":
                    y = (TextBorder(" ~ " + self.puzzleClass.author, dt(startX-padding, startY + self.boxSizeY * (self.wrapsCut+2)+padding*2), 
                            size=dt(self.boxSizeX * (self.wrapLength+1)+padding*2, 100), 
                            bg_color=Color.WHITE, 
                            bd_color=Color.BLACK,
                            f_typo =font_typo["Comfortaa"]["Small"],
                            f_color=font_color["GrayNone"],
                            id = None))
                    y.static = True
                    self.table_sprite.add(y)
                
                for y, text in enumerate(self.board):
                    
                    if curLen + len(text) > self.wrapLength:
                        curLen = 0
                        curLine += 1    
                    elif text=="\n":
                        curLen = 0
                        curLine += 1    
                        continue
                    
                    
                    for x, letter in enumerate(text):
                        clue = self.boardKeys[y][x]
                        self.boardBlocks[i] = CryptogramCell('' if letter =='_' else letter, 
                                                             clue if clue.isalpha() else '',
                                                             self.boardAnswers[y][x], 
                                                    dt(startX + self.boxSizeX * curLen, startY + self.boxSizeY * curLine + 50), 
                                                    size=dt(self.boxSizeX,self.boxSizeY), 
                                                    id = i)
                        
                        self.boardBlocks[i].static = letter != '_'
                        self.table_sprite.add(self.boardBlocks[i])
                        curLen += 1
                        i += 1
                    
                    curLen += 1
                    
                self.maxLetter = i
                    
                
            self.SceneGeneral()
            
            self.moves = 0
            
            self.lastTick = pygame.time.get_ticks()
            
            self.board = self.puzzleClass.get_Text(2).strip().replace('\n', ' \n ')
            self.boardKeys = self.puzzleClass.get_Text(1).strip().replace('\n', ' \n ').split(' ')
            self.boardAnswers = self.puzzleClass.get_Text(0).replace('\n', ' \n ').strip().split(' ')
            
            self.boxSizeX = 30
            self.boxSizeY = 60

            self.wrapLength = 20
            self.wrapsCut = len(self.board) // self.wrapLength
            
            self.boxSizeY *= 1.5
            
            self.board = self.board.split(' ')
            
            self.setCurID = 0
            
            
            self.wholeSIZE = {
                'X': max(750, self.wrapLength * self.boxSizeX + 50),
                'Y': max(500, self.wrapsCut * self.boxSizeY + 50)
                }
            
            
            self.gameDisplay = pygame.display.set_mode((self.localScreenWidth,self.wholeSIZE['Y']+200),Screen.FLAGS)
            
            self.general_GameTitle.set_Text("Cryptogram")
            self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
            
            self.toChange = []
            self.maxLetter = 0
            
            build_Table()
            
            build_Loaders()
            
            
            loop()
        
        
        def printStart():
            
            def printInit(count):
            
                def build_Table():
                    
                    self.boardBlocks = {}
                    self.table_sprite = pygame.sprite.Group()
                    self.toCheck = pygame.sprite.Group()
                    
                    curLen = 0
                    curLine = 0
                    i = 0
                    
                    
                    
                    startX = (self.wholeSIZE['X'] - self.wrapLength * self.boxSizeX) / 2
                    startY = (self.wholeSIZE['Y'] - self.wrapsCut * self.boxSizeY) / 2
                    padding = 25
                    
                    
                    self.puzzleHolder = pygame.surface.Surface((self.localScreenWidth,self.wholeSIZE['Y']+100*self.wrapsCut))
                    
                    self.startX = startX-padding
                    self.startY = startY
                    self.boardWidth = self.boxSizeX * (self.wrapLength+1)+padding*2
                    self.boardHeight = self.boxSizeY * (self.wrapsCut+2)+padding*2
                    
                    
                    x = (TextBorder('', dt(startX-padding, startY), 
                            size=dt(self.boardWidth, self.boardHeight), 
                            bg_color=Color.BLACK, 
                            bd_color=Color.BLACK,
                            id = None))
                    x.static = True
                    self.table_sprite.add(x)
                    
                    for y, text in enumerate(self.board):
                        
                        if curLen + len(text) > self.wrapLength:
                            curLen = 0
                            curLine += 1    
                        elif text=="\n":
                            curLen = 0
                            curLine += 1    
                            continue
                        
                        
                        for x, letter in enumerate(text):
                            clue = self.boardKeys[y][x]
                            self.boardBlocks[i] = CryptogramCell('' if letter =='_' else letter, 
                                                                 clue if clue.isalpha() else '',
                                                                 self.boardAnswers[y][x], 
                                                        dt(startX + self.boxSizeX * curLen, startY + self.boxSizeY * curLine + 50), 
                                                        size=dt(self.boxSizeX,self.boxSizeY), 
                                                        id = i)
                            
                            self.boardBlocks[i].static = letter != '_'
                            self.table_sprite.add(self.boardBlocks[i])
                            self.toCheck.add(self.boardBlocks[i])
                            curLen += 1
                            i += 1
                        
                        curLen += 1
                        
                    self.maxLetter = i
                    
                    if self.puzzleClass.author != "":
                        y = (TextBorder(" ~ " + self.puzzleClass.author, dt(startX-padding, startY + self.boxSizeY * (self.wrapsCut+2)+padding*1.5), 
                                size=dt(self.boxSizeX * (self.wrapLength+1)+padding*2, 25), 
                                bg_color=Color.WHITE, 
                                bd_color=Color.BLACK,
                                f_typo =font_typo["Comfortaa"]["Small"],
                                f_color=font_color["GrayNone"],
                                id = None))
                        y.static = True
                        self.table_sprite.add(y)

                def print_Table():
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                    name = self.boardLoc + "{1}_{0}_BOARD.png".format(count, self.puzzleClass.title)
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.startX, self.startY,
                                 self.boardWidth,
                                  self.boardHeight+25,
                                  result_width=self.resultingSize)
                    
                def get_Solution():
                    for i in self.toCheck:
                        if i.text != i.anstext:
                            i.text = i.anstext
                            i.f_color = font_color["RedNone"]
                            i.update()
                
                def print_Solution():
                    
                    self.puzzleHolder.fill(Color.WHITE)
            
                    self.table_sprite.draw(self.puzzleHolder)
                        
                    name = self.answerLoc + "{1}_{0}_SOLUTION.png".format(count, self.puzzleClass.title)    
                    
                    pygame.image.save(self.puzzleHolder, self.saveLocation + name)
                    
                    crop_image(self.saveLocation + name,
                               self.saveLocation + name,
                                self.startX, self.startY,
                                 self.boardWidth,
                                  self.boardHeight+25,
                                  result_width=self.resultingSize)
                   
                self.board = self.puzzleClass.get_Text(2).strip().replace('\n', ' \n ')
                self.boardKeys = self.puzzleClass.get_Text(1).strip().replace('\n', ' \n ').split(' ')
                self.boardAnswers = self.puzzleClass.get_Text(0).replace('\n', ' \n ').strip().split(' ')
                
                self.boxSizeX = 30
                self.boxSizeY = 60
                
                self.boxSizeY *= 1.5
                
                self.wrapLength = 20
                self.wrapsCut = len(self.board) // self.wrapLength
                
                self.board = self.board.split(' ')
                
                self.setCurID = 0
                
                self.wholeSIZE = {
                    'X': max(750, self.wrapLength * self.boxSizeX + 50),
                    'Y': max(500, self.wrapsCut * self.boxSizeY + 50)
                    }
                
                #renew table
                
                build_Table()
                
                #print board
                
                print_Table()
                
                #get solution to board
                
                get_Solution()
                
                self.printProcess(curMode=1, curProg=None, loadPercent=None)
                
                #print solution
                
                print_Solution()

                self.printProcess(curMode=2, curProg=None, loadPercent=None)

            self.printProcess = self.ScenePrintProcess(self.printAmount)
            self.printProcess(curMode=0, curProg=1, loadPercent=0)

            for i in range(self.printAmount):
                self.puzzleClass.re_init()
                self.puzzleClass.nextTextQueue()
                self.puzzleClass.process_Text()
                
                printInit(i)
                self.printProcess(curMode=0, curProg=i+1, loadPercent=i/self.printAmount)
                
            self.printProcess(curMode=2, curProg=i+1, loadPercent=1)
            
            pygame.time.wait(1000)
            
            self.run = ''
        
        
        
        def show_solution():
            
            for i in self.mouseUpdateList:
                if i.text != i.anstext:
                    i.text = i.anstext
                    i.f_color = font_color["RedNone"]
                    i.update()
            loop_display()
            
        
        def loop_control():
            
            def getSimilar(text):
                self.toChange = []
                for i in self.mouseUpdateList:
                    i.ready = False
                    if i.crptext ==text:
                        i.ready = True
                        self.toChange.append(i)
                    i.update()
                    
            def updateText(text):
                for i in self.toChange:
                    i.setText(text)
                    
            def updateCurID(value):
                self.setCurID += value
                self.setCurID = min(max(0,self.setCurID), self.maxLetter-1)
                getSimilar(self.boardBlocks[self.setCurID].crptext)
                
            def checkWin():
                done = True
                for i in self.mouseUpdateList:
                    if i.text != i.anstext:
                        done = False
                if done:
                    self.run = "0"
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = ''
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        #pygame.image.save(self.puzzleHolder, "Sample.png")
                        self.run = ''
                        
                    elif event.key == pygame.K_BACKSPACE:
                        updateText('')
                        
                    elif event.key == pygame.K_LEFT:
                            updateCurID(-1)
                        
                    elif event.key == pygame.K_RIGHT:
                            updateCurID(1)         
                                        
                    elif event.key == pygame.K_UP:
                            updateCurID(-self.wrapLength)
                                                  
                    elif event.key == pygame.K_DOWN:
                            updateCurID(self.wrapLength)
                        
                    else:
                        updateText(event.unicode.upper())
                        checkWin()
                        self.moves += 1
                    self.general_GameMoves.set_Text("Moves Made: {0}".format(self.moves))
            
                if 4 <= event.type <= 6: #Mouse Button Move and Click Up and Down
                    for item in self.mouseUpdateList:
                        if not self.click:
                            if item.mouseDetect():
                                self.setCurID = item.id
                                getSimilar(item.crptext)
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = False
                                
        def loop_logic():
            
            for item in self.updateList:
                if item.updating == False:
                    continue
                item.update()
            
                pass
            
            if pygame.time.get_ticks() - self.lastTick > 1000:
                self.timer -= 1  
                self.general_GameTimer.set_Text("Time: {0}:{1}".format(self.timer//60, self.timer%60))
                self.lastTick = pygame.time.get_ticks()
                if self.timer < 1:
                    show_solution()
                    self.run = '1'
    
        def loop_display():
            self.puzzleHolder.fill(Color.WHITE)
            
            self.general_sprite.draw(self.puzzleHolder)
            self.table_sprite.draw(self.puzzleHolder)
            
            
            self.gameDisplay.blit(self.puzzleHolder, (0,0))
            
            
            pygame.display.flip()
        

        
        def loop():
            while self.run == 'G':
                loop_control()
                loop_logic()
                loop_display()
                
                self.clock.tick(Screen.FPS)
        
        if self.printMode:
            printStart()
        else:
            start()

if __name__ == "__main__":
    cw = Crossword()
    cw.setBoard(12, 12, ".")
    cw.generateKeys(10)
    cw.buildBoard()
    
    mainGame(cw, cw.title).printBoard(2)
    
