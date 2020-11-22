"""Minimalistic PySciter sample for Windows."""

import sciter
import os

if True:
    from .puzzle_generators import *
    from . import puzzle_game_main
    from .puzzle_ModePresetValue import *
else:
    from puzzle_generators import *
    import puzzle_game_main
    from puzzle_ModePresetValue import *

class Frame(sciter.Window):

    ##############################################    INITIALIZER FUNCTIONS

    def __init__(self):
        super().__init__(ismain=True, uni_theme=False, debug=False)
        self.set_dispatch_options(enable=True, require_attribute=False)
        self.buildData()
        self.curModePlay = "none"
        
    def buildData(self):
        self.parameters = {
            "Number Search": {
                "Game Timer (m): ":["number", [1,100], "Time"],
                "Box Width: ": ["number", [6,30], "SizeX"],
                "Box Height: ": ["number", [6,30], "SizeY"],
                "How Many To Search: ": ["number", [1,23], "HowManyNum"],
                "Number Length: ": ["number", [3,15], "NumLength"],
                "Directions: ": ["choice", ["Down Right", "Down Right Diagonal", "All Possible Direction"], "Direction"]
                },        
            "Crossword": {
                "Game Timer (m): ":["number", [1,100], "Time"],
                "Hide Chance(%): ": ["number", [1,100], "HideChance"],
                "Directions: ": ["choice", ["Down Right", "Down Right and Reverse"], "Direction"],
                }, 
            "Maze": {
                "Game Timer (m): ":["number", [1,100], "Time"],
                "Box Width: ": ["number", [6,40], "SizeX"],
                "Box Height: ": ["number", [6,40], "SizeY"],
                }, 
            "Kakuro": {
                "Game Timer (m): ":["number", [1,100], "Time"],
                "Hide Chance(%): ": ["number", [1,100], "HideChance"],
                "Check every (n) seconds: ": ["number", '60', "CheckTime"],
                "Box Width: ": ["number", [5,35], "SizeX"],
                "Box Height: ": ["number", [5,35], "SizeY"],
                },  
            "Hidato": {
                "Game Timer (m): ":["number", [1,100], "Time"],
                "Box Width: ": ["number", [3,15], "SizeX"],
                "Box Height: ": ["number", [3,15], "SizeY"],
                "Hide Chance(%): ": ["number", [1,70], "HideChance"],
                "Directions: ": ["choice", ["No Diagonals", "Diagonal Included"], "Direction"]
                }, 
            "Nonogram": {
                "Game Timer (m): ":["number", [1,100], "Time"],
                "Box Size: ": ["choice", ["16x16", "24x24", "32x32", "48x48"], "Size_Nono"],
                },  
            "Cryptogram": {
                "Game Timer (m): ":["number", [1,100], "Time"],
                "Initial Letter Shown: ": ["number", [0,26], "InitialLetters"]
                }, 
            }

        def modeValues():
            easy = {
                "Number Search": {
                    "Game Timer (m): ": ["number", '15', "Time"],
                    "Box Width: ": ["number", ModePresets.ns_eas_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.ns_eas_height, "SizeY"],
                    "How Many To Search: ": ["number",ModePresets.ns_eas_howMany, "HowManyNum"],
                    "Number Length: ": ["number", ModePresets.ns_eas_length, "NumLength"],
                    "Directions: ": ["choice", ModePresets.ns_eas_direction, "Direction"],
                    }, 
                
                "Crossword": {
                    "Game Timer (m): ": ["number", '15', "Time"],
                    "Hide Chance(%): ": ["number", ModePresets.cw_eas_hideChance, "HideChance"],
                    "Directions: ": ["choice", ModePresets.cw_eas_directions, "Direction"],
                    }, 
                
                "Maze": {
                    "Game Timer (m): ": ["number", '15', "Time"],
                    "Box Width: ": ["number", ModePresets.mz_eas_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.mz_eas_height, "SizeY"],
                    }, 
                
                "Kakuro": {
                    "Game Timer (m): ": ["number", '15', "Time"],
                    "Check every (n) seconds: ": ["number", '30', "CheckTime"],
                    "Hide Chance(%): ": ["number", ModePresets.kk_eas_hideChance, "HideChance"],
                    "Box Width: ": ["number", ModePresets.kk_eas_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.kk_eas_height, "SizeY"],
                    },  
                
                "Hidato": {
                    "Game Timer (m): ": ["number", '15', "Time"],
                    "Hide Chance(%): ": ["number", ModePresets.hd_eas_hideChance, "HideChance"],
                    "Box Width: ": ["number", ModePresets.hd_eas_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.hd_eas_height, "SizeY"],
                    "Directions: ": ["choice", ModePresets.hd_eas_directions, "Direction"]
                    }, 
                
                "Nonogram": {
                    "Game Timer (m): ": ["number", '15', "Time"],
                    "Box Size: ": ["choice", ModePresets.nn_eas_boxSize, "Size_Nono"],
                    },  
                
                "Cryptogram": {
                    "Game Timer (m): ": ["number", '15', "Time"],
                    "Initial Letter Shown: ": ["number", ModePresets.cc_eas_showLetter, "InitialLetters"]
                    }, 
                
                }
            
            medium = {
                
                "Number Search": {
                    "Game Timer (m): ": ["number", '10', "Time"],
                    "Box Width: ": ["number", ModePresets.ns_med_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.ns_med_height, "SizeY"],
                    "How Many To Search: ": ["number",ModePresets.ns_med_howMany, "HowManyNum"],
                    "Number Length: ": ["number", ModePresets.ns_med_length, "NumLength"],
                    "Directions: ": ["choice", ModePresets.ns_med_direction, "Direction"],
                    }, 
                
                "Crossword": {
                    "Game Timer (m): ": ["number", '10', "Time"],
                    "Hide Chance(%): ": ["number", ModePresets.cw_med_hideChance, "HideChance"],
                    "Directions: ": ["choice", ModePresets.cw_med_directions, "Direction"],
                    }, 
                
                "Maze": {
                    "Game Timer (m): ": ["number", '10', "Time"],
                    "Box Width: ": ["number", ModePresets.mz_med_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.mz_med_height, "SizeY"],
                    }, 
                
                "Kakuro": {
                    "Game Timer (m): ": ["number", '25', "Time"],
                    "Check every (n) seconds: ": ["number", '90', "CheckTime"],
                    "Hide Chance(%): ": ["number", ModePresets.kk_med_hideChance, "HideChance"],
                    "Box Width: ": ["number", ModePresets.kk_med_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.kk_med_height, "SizeY"],
                    },  
                
                "Hidato": {
                    "Game Timer (m): ": ["number", '10', "Time"],
                    "Hide Chance(%): ": ["number", ModePresets.hd_med_hideChance, "HideChance"],
                    "Box Width: ": ["number", ModePresets.hd_med_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.hd_med_height, "SizeY"],
                    "Directions: ": ["choice", ModePresets.hd_med_directions, "Direction"]
                    }, 
                
                "Nonogram": {
                    "Game Timer (m): ": ["number", '10', "Time"],
                    "Box Size: ": ["choice", ModePresets.nn_med_boxSize, "Size_Nono"],
                    "Picture to Solve<optional>:  ": ["button", 0, "NonogramFile"],
                    },  
                
                "Cryptogram": {
                    "Game Timer (m): ": ["number", '10', "Time"],
                    "Initial Letter Shown: ": ["number", ModePresets.cc_med_showLetter, "InitialLetters"]
                    }, 
                
                }
            
            hard = {
                "Number Search": {
                    "Game Timer (m): ": ["number", '5', "Time"],
                    "Box Width: ": ["number", ModePresets.ns_hard_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.ns_hard_height, "SizeY"],
                    "How Many To Search: ": ["number",ModePresets.ns_hard_howMany, "HowManyNum"],
                    "Number Length: ": ["number", ModePresets.ns_hard_length, "NumLength"],
                    "Directions: ": ["choice", ModePresets.ns_hard_direction, "Direction"],
                    }, 
                
                "Crossword": {
                    "Game Timer (m): ": ["number", '5', "Time"],
                    "Hide Chance(%): ": ["number", ModePresets.cw_hard_hideChance, "HideChance"],
                    "Directions: ": ["choice", ModePresets.cw_hard_directions, "Direction"],
                    }, 
                
                "Maze": {
                    "Game Timer (m): ": ["number", '5', "Time"],
                    "Box Width: ": ["number", ModePresets.mz_hard_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.mz_hard_height, "SizeY"],
                    }, 
                
                "Kakuro": {
                    "Game Timer (m): ": ["number", '35', "Time"],
                    "Check every (n) seconds: ": ["number", '300', "CheckTime"],
                    "Hide Chance(%): ": ["number", ModePresets.kk_hard_hideChance, "HideChance"],
                    "Box Width: ": ["number", ModePresets.kk_hard_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.kk_hard_height, "SizeY"],
                    },  
                
                "Hidato": {
                    "Game Timer (m): ": ["number", '5', "Time"],
                    "Hide Chance(%): ": ["number", ModePresets.hd_hard_hideChance, "HideChance"],
                    "Box Width: ": ["number", ModePresets.hd_hard_width, "SizeX"],
                    "Box Height: ": ["number", ModePresets.hd_hard_height, "SizeY"],
                    "Directions: ": ["choice", ModePresets.hd_hard_directions, "Direction"]
                    }, 
                
                "Nonogram": {
                    "Game Timer (m): ": ["number", '5', "Time"],
                    "Box Size: ": ["choice", ModePresets.nn_hard_boxSize, "Size_Nono"],
                    "Picture to Solve<optional>:  ": ["button", 0, "NonogramFile"],
                    },  
                
                "Cryptogram": {
                    "Game Timer (m): ": ["number", '5', "Time"],
                    "Initial Letter Shown: ": ["number", ModePresets.cc_hard_showLetter, "InitialLetters"]
                    }, 
                
                }
            
            return {"Easy":easy, "Medium":medium, "Hard": hard}

        self.modeSet = modeValues()

        self.variables = {
            "Time": 0,
            "SizeX": 10,
            "SizeY": 10,
            "HowManyNum": 0,
            "NumLength": 0,
            "Direction": 0,
            "Key": 0,
            "KeyandClue": 0,
            "OnePath": 0,
            "Size_Nono": 0,
            "Message": 0,
            "InitialLetters": 0,
            "CheckTime": 0,
            "HideChance": 0,
            "NonogramFile": 0,
            "SaveLocation": 0,
            "FileLocation": 0,
            "FileList": 0,
            "ImageSize": 750,
        }

        self.gameEngine = None


    ##############################################   SCITER SCRIPTS THAT WILL BE CALLED BY THE APP

    '''
    let sample = {
        "Width" : ["number", 10, 10, 20], //mode, current, min, max
        "Height" : ["number", 10, 10, 20], //mode, current, min, max
        "How Many To Search" : ["number", 10, 10, 20], //mode, current, min, max
        "Length of Words" : ["number", 10, 10, 20], //mode, current, min, max
        "Directions" : ["choice", 1, ["Down Right", "Down Right Diagonal", "All Direction"]], //mode, index, choices
    }
    '''

    @sciter.script
    def loadPlayData(self, title, mode):
        toRet = {}
        self.curModePlay = title
        for key, value in self.parameters[title].items():

            retChunk = ["mode", 0, 0, 0]

            retChunk[0] = value[0]

            if value[0] == "number":
                retChunk[1] = int(self.modeSet[mode][title][key][1])
                retChunk[2] = value[1][0]
                retChunk[3] = value[1][1]
            elif value[0] == "choice":
                retChunk[2] = value[1]
                retChunk[1] = value[1][int(self.modeSet[mode][title][key][1])]

            retChunk.append(title)
            toRet[key] = retChunk
        return toRet

    @sciter.script
    def loadPlayPreset(self, mode):
        toRet = {}
        for key, value in self.parameters[self.curModePlay].items():

            retChunk = ["mode", 0]

            retChunk[0] = value[0]

            if value[0] == "number":
                retChunk[1] = int(self.modeSet[mode][self.curModePlay][key][1])
            elif value[0] == "choice":
                retChunk[1] = value[1][int(self.modeSet[mode][self.curModePlay][key][1])]

            toRet[key] = retChunk
        return toRet

    @sciter.script
    def loadPlayStartGame(self, data):

        for item, value in data.items():
            self.variables[
                self.parameters[self.curModePlay][item][2]
                ] = value

        print(self.variables)
        

        self.load_Game()
        #insert the general game loader here

    ##############################################   FUNCTIONS USED TO CALL PYTHON HEAVY LIFTINGS

    def load_Game(self):
        
        { #            self.variables["param"]
            "Time": 0,
            "Size": 0,
            "AvailNum": 0,
            "HowManyNum": 0,
            "NumLength": 0,
            "Direction": 0,
            "Key": 0,
            "KeyandClue": 0,
            "OnePath": 0,
            "Size_Nono": 0,
            "Message": 0,
            "InitialLetters": 0,
            "CheckTime": 0,
            "HideChance": 0,
            "SaveLocation": 0
        }
        
        def A():
            ns = NumberSearch()
            ns.setBoard(self.variables["SizeX"], self.variables["SizeY"], ".") #width, height, filler
            
            ns.generateKeys(self.variables["HowManyNum"], self.variables["NumLength"]-2, self.variables["NumLength"]) #generate keys of 10 that has a length between 5 and 8
            
            dirModes = {
                "Down Right": 0,
                "Down Right Diagonal": 1,
                "All Possible Direction": 2
                }

            ns.setDirection(dirModes[self.variables["Direction"]])
            ns.buildBoard() #build the board
            
            self.gameEngine = puzzle_game_main.mainGame(ns, ns.title)
            self.gameEngine.build(self.variables["Time"]*60)

        def B():
            cw = Crossword()
            cw.setBoard(self.variables["SizeX"], self.variables["SizeY"], ".")
            
            dir_loc = "CrosswordTemplates/" 
                
            cw.loadText(dir_loc + random.choice(os.listdir(dir_loc)))
            
            dirModes = {
                "Down Right": 0, 
                "Down Right and Reverse":1
            }

            cw.setDirection(dirModes[self.variables["Direction"]])
            
            cw.difficulty = self.variables["HideChance"]/100
            
            cw.buildBoard()
            #cw.printBoard()
            
            self.gameEngine = puzzle_game_main.mainGame(cw, cw.title)
            self.gameEngine.build(self.variables["Time"]*60)
        
        def C():
            mz = MazeB()
            mz.setBoard(self.variables["SizeX"],self.variables["SizeY"], ".")
            
            #mz.setOnePath(self.variables["OnePath"])
            
            mz.buildBoard()
                
            self.gameEngine = puzzle_game_main.mainGame(mz, mz.title)
            self.gameEngine.build(self.variables["Time"]*60)
        
        def D():
            kk = Kakuro()
            kk.setBoard(self.variables["SizeX"],self.variables["SizeY"], ".")
            
            kk.difficulty = self.variables["HideChance"]/100
            
            kk.buildBoard()
            
            self.gameEngine = puzzle_game_main.mainGame(kk, kk.title)
            self.gameEngine.build(self.variables["Time"]*60, self.variables["CheckTime"]*60)
            
        def E():
            
            hd = Hidato()
            
            
            hd.diagonals = (self.variables["Direction"] == "Diagonal Included")
            hd.difficulty = self.variables["HideChance"]/100
            
            if (self.variables["SizeX"]+self.variables["SizeY"])//2 > 6:
                hd.pureRandomRate = 0.75
                hd.extremeFast = True
            
            hd.setBoard(self.variables["SizeX"], self.variables["SizeY"], '.')
            
            hd.buildBoard()
            
            self.gameEngine = puzzle_game_main.mainGame(hd, hd.title)
            self.gameEngine.build(self.variables["Time"]*60, diagonals=(self.variables["Direction"] == "Diagonal Included"))
            
        def F():
            nn = Nonogram()
            
            if self.variables["NonogramFile"] == 0:
                #load an image based on the input
                dir_loc = "NonoImages/" + self.variables["Size_Nono"] + "/"
                
                nn.loadImage(dir_loc + random.choice(os.listdir(dir_loc)), size=self.variables["Size_Nono"])
            
            else: nn.loadImage(self.variables["NonogramFile"], self.variables["Size_Nono"])
            
            nn.buildBoard()
            
            self.gameEngine = puzzle_game_main.mainGame(nn, nn.title)
            self.gameEngine.build(self.variables["Time"]*60)
            
        def G():
            def getAQuote():
                
                with open('quotes.json', 'r', encoding="utf-8") as f:
                    data = json.load(f)
                
                pick = random.choice(data['quotes'])
                
                return [pick["quote"], pick["author"]]
                
                #return load
                
            cc = Cryptogram()
            
            x = getAQuote()
            cc.load_Text(x[0],x[1])
                
            cc.revealAmount = self.variables["InitialLetters"]
            cc.process_Text()
            
            self.gameEngine = puzzle_game_main.mainGame(cc, cc.title)
            self.gameEngine.build(self.variables["Time"]*60)
        
        if self.gameEngine != None:
            if self.gameEngine.checkRun():
                self.call_function('overlay_ShowNotification', "Hey! A game is already running", "Close the already running program first before opening a new one")
                return False
        if self.curModePlay == "Number Search": A()
        elif self.curModePlay == "Crossword":   B()
        elif self.curModePlay == "Maze":    C()
        elif self.curModePlay == "Kakuro":  D()
        elif self.curModePlay == "Hidato":  E()
        elif self.curModePlay == "Nonogram":    F()
        elif self.curModePlay == "Cryptogram":    G()

    ##############################################   UNDER THESE ARE UTILITY FUNCTIONS

    @sciter.script
    def gprint(self, *var):
        print("----------------")
        for i in var:
            print("-> ", i)




if __name__ == '__main__':
    # create window
    frame = Frame()
    
    #debug as on
    frame.setup_debug()

    # load file
    frame.load_file("./html/index.html")

    frame.run_app()
