import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

if True:
    from .puzzle_generators import *
    from . import puzzle_game_main
    from .puzzle_ModePresetValue import *
else:
    from puzzle_generators import *
    import puzzle_game_main
    from puzzle_ModePresetValue import *

import os

class GameClues:
    def __init__(self, clueDict):
        self.root = tk.Tk()
        self.root.title("Clues")
        self.root.geometry("+300+100")
        
        self.clueDict = clueDict
        
        self.fontSize = 15
        
        self.entryList = {}
        
        
    def build(self):
        self.buildUI(self.root)
        
    def buildUI(self, master):
        
        frame_1 = ttk.Frame(master)
        
        title = ttk.Label(frame_1)
        title.config(font='{Comfortaa} 18 {}', padding='15 25', text='Game Clues')
        title.pack(side='top')
        
        
        
        for category in self.clueDict.keys():
            
            counter = 1
            
            x = ttk.Labelframe(frame_1)
            
            for item in self.clueDict[category]:
                self.entryList[item] = ttk.Label(x)
                self.entryList[item].config(text="{0}: {1}".format(counter, item), font='{open sans} %d {}'%self.fontSize)
                self.entryList[item].pack(side='top')
                counter += 1
        
            x.config(height='200', text=str(category), width='200')
            x.pack(expand='true', fill='both', padx='5', side='left')
            x = ttk.Labelframe(frame_1)
            
        
        
        frame_1.config(height='200', width='200')
        frame_1.pack(side='top')

        # Main widget
        self.mainwindow = frame_1

    
    def removeClue(self, item):
        try:
            self.entryList[item].destroy()
        except:
            pass
    
    def setPosition(self, x, y):
        self.root.geometry("+{0}+{1}".format(x,y))
    
    def runUpdate(self):
        self.mainwindow.update()
        
    def run(self):
        self.mainwindow.mainloop()
        
    def destroy(self):
        self.root.destroy()


class PuzzlePack:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Puzzle Pack")
        self.root.geometry("+50+15")
        self.build(self.root)
        self.run()
        
    def build(self, master):
        self.declareVariables()
        self.paramHolder = {}
        self.labelHolder = {}
        self.labelHolderB = {}
        
        # build ui
        self.buildUI(master)
        
    def declareVariables(self):
        # Param_strings are slider+range, input+None, spinbox+choice, checkbox+None, bigText+None, button+None
        self.param_type = 0
        self.param_value = 1
        self.param_varTarget = 2
        
        self.curMode = 'None'
        
        self.ignore = ["Directions: ", "Numbers To Search <optional>: ",
                        "Words <optional>: ", "Only One Path To End: ", "Message <Optional>: "
                        ,"Game Timer (m): ","Check every (n) seconds: ",
                         "Picture to Solve<optional>:  "]
        
        self.printParamType = {
            "Number Search" : ["count"],
            "Crossword" : ["select_multiple", (("Select a text file","*.txt"),("All Files","*.*"))],
            "Maze" : ["count"],
            "Kakuro" : ["count"],
            "Hidato" : ["count"],
            "Nonogram" : ["select_multiple", (("Select a png file","*.png"),("All Files","*.*"))],
            "Cryptogram" : ["select", (("Select a text file","*.txt"),("All Files","*.*"))],
            }
        
        self.frm_param = None
        self.frm_print = None
        self.buttons =  ["Number Search", "Crossword", "Maze", "Kakuro", "Hidato", "Nonogram", "Cryptogram"]
        self.parameters = {
            "Number Search": {
                "Game Timer (m): ": ["input", '3', "Time"],
                "Box Width: ": ["slider", [6,30], "SizeX"],
                "Box Height: ": ["slider", [6,30], "SizeY"],
                "How Many To Search: ": ["slider", [1,23], "HowManyNum"],
                "Number Length: ": ["slider", [3,15], "NumLength"],
                "Directions: ": ["spinbox", ["Down Right", "Down Right Diagonal", "All Possible Direction"], "Direction"]
                }, 
            
            "Crossword": {
                "Game Timer (m): ": ["input", '3', "Time"],
                "Hide Chance(%): ": ["slider", [1,100], "HideChance"],
                "Directions: ": ["spinbox", ["Down Right", "Down Right and Reverse"], "Direction"],
                }, 
            "Maze": {
                "Game Timer (m): ": ["input", '3', "Time"],
                "Box Width: ": ["slider", [6,40], "SizeX"],
                "Box Height: ": ["slider", [6,40], "SizeY"],
                }, 
            "Kakuro": {
                "Game Timer (m): ": ["input", '3', "Time"],
                "Hide Chance(%): ": ["slider", [1,100], "HideChance"],
                "Check every (n) seconds: ": ["input", '60', "CheckTime"],
                "Box Width: ": ["slider", [5,35], "SizeX"],
                "Box Height: ": ["slider", [5,35], "SizeY"],
                },  
            "Hidato": {
                "Game Timer (m): ": ["input", '3', "Time"],
                "Box Width: ": ["slider", [3,15], "SizeX"],
                "Box Height: ": ["slider", [3,15], "SizeY"],
                "Hide Chance(%): ": ["slider", [1,70], "HideChance"],
                "Directions: ": ["spinbox", ["No Diagonals", "Diagonal Included"], "Direction"]
                }, 
            "Nonogram": {
                "Game Timer (m): ": ["input", '3', "Time"],
                "Box Size: ": ["spinbox", ["16x16", "24x24", "32x32", "48x48"], "Size_Nono"],
                "Picture to Solve<optional>:  ": ["button", None, "NonogramFile"],
                },  
            "Cryptogram": {
                "Game Timer (m): ": ["input", '3', "Time"],
                "Initial Letter Shown: ": ["slider", [0,26], "InitialLetters"]
                }, 
            }
        
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
        

    def buildUI(self, master):
        
        def createMain():
            #The Main Frame
            self.frame_1 = ttk.Frame(master)
            
            
            #The Title Label Frame
            self.label_1 = ttk.Label(self.frame_1)
            self.label_1.config(cursor='arrow', 
                           font='{Comfortaa} 40 {}', 
                           padding='25 20', 
                           text='Puzzle Pack')
            self.label_1.pack(side='top')

        def createGameSelect():

            self.frm_selectmode = ttk.Labelframe(self.frame_1)
            
            buttons = self.buttons
            
            self.btn_SelectMode = {}
            
            #The buttons generated here are based on the self.button input, which means, this is easily expandable
            for i in buttons:
                self.btn_SelectMode[i] = ttk.Button(self.frm_selectmode)
                self.btn_SelectMode[i].config(text=i)
                self.btn_SelectMode[i]['command'] = lambda label=i: self.param_click(label)
                self.btn_SelectMode[i].pack(expand='true', fill='x', ipadx='21', ipady='3', pady='1', side='top')
            
            self.frm_selectmode.config(borderwidth='12', cursor='arrow', height='200', text='Select Game Mode')
            self.frm_selectmode.config(width='200')
            self.frm_selectmode.pack(expand='false', fill='none',ipadx='40', ipady='2', pady="0", side='left')
            
            '''frame_1_2 = ttk.Frame(self.frm_selectmode)
            frame_1_2.config(height='360', width='0')
            frame_1_2.pack(side='top')'''
            
        createMain()
        #1. Create the main frame of tkinter
        
        createGameSelect()
        #2. Generate the game mode select based on the self.button list
        
        
        self.frame_1.config(height='200', width='200', borderwidth='0')
        self.frame_1.pack(side='top')

        # Main widget
        self.mainwindow = self.frame_1    
        
        
                
    def param_create(self, params):
        # This creates the frame that handles all the parameter for the game generation
        
        def createParameters(params):
            #Based on the params passed above, the below code will generate the appropriate input method
            
            # Param_strings are slider+range, input+PlaceHolder, spinbox+choice, bigtext+PlaceHolder
            
            def paramBuilder(param_info, ctr):
                
                if param_info[self.param_type] == "slider":
                    self.paramHolder[ctr] = ttk.Scale(self.frm_param)
                    self.paramHolder[ctr].config(orient='horizontal', 
                                                 from_=param_info[self.param_value][0], 
                                                 to = param_info[self.param_value][1],
                                                 command=lambda x: self.label_showValue())
                    self.paramHolder[ctr].pack(pady='5', side='top')
                    self.paramHolder[ctr].set(int((param_info[self.param_value][0] + param_info[self.param_value][1]) * 0.25))
                    
                elif param_info[self.param_type] == "input":
                    self.paramHolder[ctr] = ttk.Entry(self.frm_param)
                    _text_ = param_info[self.param_value]
                    self.paramHolder[ctr].delete('0', 'end')
                    self.paramHolder[ctr].insert('0', _text_)
                    self.paramHolder[ctr].pack(pady='5', side='top')
                
                elif param_info[self.param_type] == "spinbox":
                    self.paramHolder[ctr] = ttk.Combobox(self.frm_param)
                    self.paramHolder[ctr].config(values=param_info[self.param_value])
                    self.paramHolder[ctr].current(0)
                    self.paramHolder[ctr].pack(side='top')
                
                elif param_info[self.param_type] == "bigtext":
                    self.paramHolder[ctr] = tk.Text(self.frm_param)
                    self.paramHolder[ctr].config(height='10', width='30', wrap="word")
                    _text_ = param_info[self.param_value]
                    self.paramHolder[ctr].insert('0.0', _text_)
                    self.paramHolder[ctr].pack(side='top')
                
                elif param_info[self.param_type] == "button":
                    self.paramHolder[ctr] = ttk.Button(self.frm_param)
                    self.paramHolder[ctr].config(takefocus=False, text='Pick File')
                    self.paramHolder[ctr]['command'] = lambda x=param_info[self.param_varTarget]: self.pickFile(x)
                    self.paramHolder[ctr].pack(side='top')
                    self.paramHolder[ctr].config()
                    
            
            ctr = 0
            
            self.labelHolder = {}
            
            for item in params.keys():
            
                self.labelHolder[item] = tk.StringVar()
                self.labelHolder[item].set(item)
                self.labelHolderB[item] = item
                
                if item not in self.ignore:
                    x = ttk.Label(self.frm_param, textvariable = self.labelHolder[item])
                    x.config(text=item)
                    x.pack(side='top')
                else:
                    x = ttk.Label(self.frm_param)
                    x.config(text=item)
                    x.pack(side='top')
                
                paramBuilder(params[item], "{0}".format(item))
                
                ctr += 1
              
            #print(self.labelHolder)
            
        def buildDifficultyButtons():
            #I could had used a dictionary here and made an iteration but meh
            
            self.frame_3 = ttk.Frame(self.frm_param)
        
            self.btn_Easy = ttk.Button(self.frame_3)
            self.btn_Easy.config(text='Easy', command=lambda mode="Easy": self.modes_preset(mode))
            self.btn_Easy.pack(side='left')
            
            self.btn_Medium = ttk.Button(self.frame_3)
            self.btn_Medium.config(text='Medium', command=lambda mode="Medium": self.modes_preset(mode))
            self.btn_Medium.pack(side='left')
            
            self.btn_Hard = ttk.Button(self.frame_3)
            self.btn_Hard.config(text='Hard', command=lambda mode="Hard": self.modes_preset(mode))
            self.btn_Hard.pack(side='left')
            
            self.frame_3.config(height='100', width='200')
            self.frame_3.pack(pady='20', side='top')
        
        def buildPlayOptions():
            self.frame_4 = ttk.Frame(self.frm_param)
        
            self.btn_Play = ttk.Button(self.frame_4)
            self.btn_Play.config(text='Play Board', command = self.play_Board)
            self.btn_Play.pack(ipadx='20', ipady='15', side='left')
            
            self.btn_Print = ttk.Button(self.frame_4)
            self.btn_Print.config(text='Print Board', command = self.print_Board)
            self.btn_Print.pack(ipadx='20', ipady='15', side='left')
            
            self.frame_4.config(height='200', width='200')
            self.frame_4.pack(side='top')
        
        self.frm_param = ttk.Labelframe(self.frame_1)
        #Create the handler of the parameters
    
        self.paramHolder = {}
        #If a previous parameter has already been made, clean it
        
        createParameters(params)
        
        buildDifficultyButtons()
        
        buildPlayOptions()
        
        self.frm_param.config(height='200', relief='flat', text='Parameters', width='200')
        self.frm_param.pack(ipadx='25', side='left')
        
    def param_click(self, label):
        # The callback function when you clicked on a game mode
        
        if self.frm_param != None:
            self.frm_param.destroy()
        
        if self.frm_print != None:
            self.frm_print.destroy()
        
        self.curMode = label
        self.param_create(self.parameters[label])
    
    
    def modes_preset(self, mode):
        
        
        def paramImplementer(param_info, ctr):
            
            if param_info[self.param_type] == "slider":
                self.paramHolder[ctr].set(param_info[self.param_value])
                
            elif param_info[self.param_type] == "input":
                _text_ = param_info[self.param_value]
                self.paramHolder[ctr].delete('0', 'end')
                self.paramHolder[ctr].insert('0', _text_)
            
            elif param_info[self.param_type] == "spinbox":
                self.paramHolder[ctr].current(param_info[self.param_value])
            
            elif param_info[self.param_type] == "bigtext":
                _text_ = param_info[self.param_value]
                self.paramHolder[ctr].delete('0.0', 'end')
                self.paramHolder[ctr].insert('0.0', _text_)
                
            elif param_info[self.param_type] == "button":
                self.variables[param_info[self.param_varTarget]] = param_info[self.param_value]
        
        def modeValues():
            easy = {
                "Number Search": {
                    "Game Timer (m): ": ["input", '15', "Time"],
                    "Box Width: ": ["slider", ModePresets.ns_eas_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.ns_eas_height, "SizeY"],
                    "How Many To Search: ": ["slider",ModePresets.ns_eas_howMany, "HowManyNum"],
                    "Number Length: ": ["slider", ModePresets.ns_eas_length, "NumLength"],
                    "Directions: ": ["spinbox", ModePresets.ns_eas_direction, "Direction"],
                    }, 
                
                "Crossword": {
                    "Game Timer (m): ": ["input", '15', "Time"],
                    "Hide Chance(%): ": ["slider", ModePresets.cw_eas_hideChance, "HideChance"],
                    "Directions: ": ["spinbox", ModePresets.cw_eas_directions, "Direction"],
                    }, 
                
                "Maze": {
                    "Game Timer (m): ": ["input", '15', "Time"],
                    "Box Width: ": ["slider", ModePresets.mz_eas_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.mz_eas_height, "SizeY"],
                    }, 
                
                "Kakuro": {
                    "Game Timer (m): ": ["input", '15', "Time"],
                    "Check every (n) seconds: ": ["input", '30', "CheckTime"],
                    "Hide Chance(%): ": ["slider", ModePresets.kk_eas_hideChance, "HideChance"],
                    "Box Width: ": ["slider", ModePresets.kk_eas_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.kk_eas_height, "SizeY"],
                    },  
                
                "Hidato": {
                    "Game Timer (m): ": ["input", '15', "Time"],
                    "Hide Chance(%): ": ["slider", ModePresets.hd_eas_hideChance, "HideChance"],
                    "Box Width: ": ["slider", ModePresets.hd_eas_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.hd_eas_height, "SizeY"],
                    "Directions: ": ["spinbox", ModePresets.hd_eas_directions, "Direction"]
                    }, 
                
                "Nonogram": {
                    "Game Timer (m): ": ["input", '15', "Time"],
                    "Box Size: ": ["spinbox", ModePresets.nn_eas_boxSize, "Size_Nono"],
                    "Picture to Solve<optional>:  ": ["button", 0, "NonogramFile"],
                    },  
                
                "Cryptogram": {
                    "Game Timer (m): ": ["input", '15', "Time"],
                    "Initial Letter Shown: ": ["slider", ModePresets.cc_eas_showLetter, "InitialLetters"]
                    }, 
                
                }
            
            medium = {
                
                "Number Search": {
                    "Game Timer (m): ": ["input", '10', "Time"],
                    "Box Width: ": ["slider", ModePresets.ns_med_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.ns_med_height, "SizeY"],
                    "How Many To Search: ": ["slider",ModePresets.ns_med_howMany, "HowManyNum"],
                    "Number Length: ": ["slider", ModePresets.ns_med_length, "NumLength"],
                    "Directions: ": ["spinbox", ModePresets.ns_med_direction, "Direction"],
                    }, 
                
                "Crossword": {
                    "Game Timer (m): ": ["input", '10', "Time"],
                    "Hide Chance(%): ": ["slider", ModePresets.cw_med_hideChance, "HideChance"],
                    "Directions: ": ["spinbox", ModePresets.cw_med_directions, "Direction"],
                    }, 
                
                "Maze": {
                    "Game Timer (m): ": ["input", '10', "Time"],
                    "Box Width: ": ["slider", ModePresets.mz_med_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.mz_med_height, "SizeY"],
                    }, 
                
                "Kakuro": {
                    "Game Timer (m): ": ["input", '25', "Time"],
                    "Check every (n) seconds: ": ["input", '90', "CheckTime"],
                    "Hide Chance(%): ": ["slider", ModePresets.kk_med_hideChance, "HideChance"],
                    "Box Width: ": ["slider", ModePresets.kk_med_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.kk_med_height, "SizeY"],
                    },  
                
                "Hidato": {
                    "Game Timer (m): ": ["input", '10', "Time"],
                    "Hide Chance(%): ": ["slider", ModePresets.hd_med_hideChance, "HideChance"],
                    "Box Width: ": ["slider", ModePresets.hd_med_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.hd_med_height, "SizeY"],
                    "Directions: ": ["spinbox", ModePresets.hd_med_directions, "Direction"]
                    }, 
                
                "Nonogram": {
                    "Game Timer (m): ": ["input", '10', "Time"],
                    "Box Size: ": ["spinbox", ModePresets.nn_med_boxSize, "Size_Nono"],
                    "Picture to Solve<optional>:  ": ["button", 0, "NonogramFile"],
                    },  
                
                "Cryptogram": {
                    "Game Timer (m): ": ["input", '10', "Time"],
                    "Initial Letter Shown: ": ["slider", ModePresets.cc_med_showLetter, "InitialLetters"]
                    }, 
                
                }
            
            hard = {
                "Number Search": {
                    "Game Timer (m): ": ["input", '5', "Time"],
                    "Box Width: ": ["slider", ModePresets.ns_hard_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.ns_hard_height, "SizeY"],
                    "How Many To Search: ": ["slider",ModePresets.ns_hard_howMany, "HowManyNum"],
                    "Number Length: ": ["slider", ModePresets.ns_hard_length, "NumLength"],
                    "Directions: ": ["spinbox", ModePresets.ns_hard_direction, "Direction"],
                    }, 
                
                "Crossword": {
                    "Game Timer (m): ": ["input", '5', "Time"],
                    "Hide Chance(%): ": ["slider", ModePresets.cw_hard_hideChance, "HideChance"],
                    "Directions: ": ["spinbox", ModePresets.cw_hard_directions, "Direction"],
                    }, 
                
                "Maze": {
                    "Game Timer (m): ": ["input", '5', "Time"],
                    "Box Width: ": ["slider", ModePresets.mz_hard_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.mz_hard_height, "SizeY"],
                    }, 
                
                "Kakuro": {
                    "Game Timer (m): ": ["input", '35', "Time"],
                    "Check every (n) seconds: ": ["input", '300', "CheckTime"],
                    "Hide Chance(%): ": ["slider", ModePresets.kk_hard_hideChance, "HideChance"],
                    "Box Width: ": ["slider", ModePresets.kk_hard_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.kk_hard_height, "SizeY"],
                    },  
                
                "Hidato": {
                    "Game Timer (m): ": ["input", '5', "Time"],
                    "Hide Chance(%): ": ["slider", ModePresets.hd_hard_hideChance, "HideChance"],
                    "Box Width: ": ["slider", ModePresets.hd_hard_width, "SizeX"],
                    "Box Height: ": ["slider", ModePresets.hd_hard_height, "SizeY"],
                    "Directions: ": ["spinbox", ModePresets.hd_hard_directions, "Direction"]
                    }, 
                
                "Nonogram": {
                    "Game Timer (m): ": ["input", '5', "Time"],
                    "Box Size: ": ["spinbox", ModePresets.nn_hard_boxSize, "Size_Nono"],
                    "Picture to Solve<optional>:  ": ["button", 0, "NonogramFile"],
                    },  
                
                "Cryptogram": {
                    "Game Timer (m): ": ["input", '5', "Time"],
                    "Initial Letter Shown: ": ["slider", ModePresets.cc_hard_showLetter, "InitialLetters"]
                    }, 
                
                }
            
            return {"Easy":easy, "Medium":medium, "Hard": hard}

        modeSet = modeValues()
        
        for item in modeSet[mode][self.curMode]:
            paramImplementer(modeSet[mode][self.curMode][item], item)
            
        self.label_showValue()
    
    
    def label_showValue(self):
        for i in self.labelHolder:
            x = 0
            try:
                x = (self.paramHolder[i].get())
            except:
                try:
                    x = (self.paramHolder[i].get("1.0"))
                except:
                    pass
            
            try:
                self.labelHolder[i].set(self.labelHolderB[i] + str(int(x)))
            except:
                pass
    
    
    
    def print_Window(self):
        
        def createForm():
        
            self.frm_print = ttk.Labelframe(self.frame_1)
            
            {"count", "select_multiple", "select"}
            
            #ENTRY HOW MUCH TO PRINT
            if self.printParamType[self.curMode][0] == "count":
                label_1_2 = ttk.Label(self.frm_print)
                label_1_2.config(text='How Many Puzzles to Generate')
                label_1_2.pack(pady='10', side='top')
            
                self.printAmount = ttk.Entry(self.frm_print)
                self.printAmount.config(exportselection='true', font='TkDefaultFont', justify='center', state='normal')
                _text_ = '''5'''
                self.printAmount.delete('0', 'end')
                self.printAmount.insert('0', _text_)
                self.printAmount.pack(ipadx='5', ipady='5', side='top')
                
            elif self.printParamType[self.curMode][0] == "select":
                label_1_2 = ttk.Label(self.frm_print)
                label_1_2.config(text='Select a file to process')
                label_1_2.pack(pady='10', side='top')
                
                button_2 = ttk.Button(self.frm_print)
                button_2.config(text='Pick File Location')
                button_2.pack(side='top')
                
                self.labelLoad = tk.StringVar()
                self.labelLoad.set('None')
                button_2['command'] = lambda x="FileLocation": self.pickFile(x, self.printParamType[self.curMode][1], self.labelLoad)
                
                Location = ttk.Label(self.frm_print, textvariable = self.labelLoad)
                Location.config(text='None')
                Location.pack(side='top')
                
            elif self.printParamType[self.curMode][0] == "select_multiple":
                label_1_2 = ttk.Label(self.frm_print)
                label_1_2.config(text='Select a file(s) to process')
                label_1_2.pack(pady='10', side='top')
                
                button_2 = ttk.Button(self.frm_print)
                button_2.config(text='Pick Files List')
                button_2.pack(side='top')
                
                self.labelLoad = tk.StringVar()
                self.labelLoad.set('None')
                button_2['command'] = lambda x="FileList": self.pickFiles(x, self.printParamType[self.curMode][1],  self.labelLoad)
                
                Location = ttk.Label(self.frm_print, textvariable = self.labelLoad)
                Location.config(text='None')
                Location.pack(side='top')
            
            #SIZE
            label_1_3 = ttk.Label(self.frm_print)
            label_1_3.config(text='Size of the image')
            label_1_3.pack(pady='10', side='top')
        
            self.printSize = ttk.Entry(self.frm_print)
            self.printSize.config(exportselection='true', font='TkDefaultFont', justify='center', state='normal')
            _text_ = '''{0}'''.format(self.variables["ImageSize"])
            self.printSize.delete('0', 'end')
            self.printSize.insert('0', _text_)
            self.printSize.pack(ipadx='5', ipady='5', side='top')
            
            
            #BUTTON WHERE TO SAVE
            label_3_4 = ttk.Label(self.frm_print)
            label_3_4.config(text='Save Location')
            label_3_4.pack(pady='10', side='top')
            
            button_1 = ttk.Button(self.frm_print)
            button_1.config(text='Pick File Location')
            button_1.pack(side='top')
            
            
            #SAVE String Var
            self.labelSave = tk.StringVar()
            self.labelSave.set('./')
            button_1['command'] = lambda x="SaveLocation": self.pickFolder(x, self.labelSave)
            
            Location = ttk.Label(self.frm_print, textvariable = self.labelSave)
            Location.config(text='./')
            Location.pack(side='top')
            
            button_2 = ttk.Button(self.frm_print)
            button_2.config(text='SAVE!', command = self.print_Game)
            button_2.pack(ipadx='10', ipady='20', pady='20', side='top')
            
            self.frm_print.config(height='200', relief='flat', text='Print Options', width='200')
            self.frm_print.pack(ipadx='20', side='left')
        
        if self.frm_print != None:
            self.frm_print.destroy()
        
        createForm()
        
    
    
    
    def pickFile(self, locVar, typeSave = (("png files","*.png"),("all files","*.*")), stringToChange=None):
        self.variables[locVar] = filedialog.askopenfilename(
            initialdir = "../",
            title = "Select a file to process",
            filetypes = typeSave
            )
        
        if stringToChange != None:
            text = self.variables[locVar].split('/')
            stringToChange.set(text[len(text)-1])
        
    def pickFiles(self, locVar, typeSave = (("png files","*.png"),("all files","*.*")), stringToChange=None):
        self.variables[locVar] = filedialog.askopenfilenames(
            initialdir = "../",
            title = "Select file(s) to process",
            filetypes = typeSave
            )
        
        if stringToChange != None:
            stringToChange.set("Files to Process: {0}".format(len(self.variables[locVar])))
        
    def pickFolder(self, locVar, stringtoChange=None):
        self.variables[locVar] = filedialog.askdirectory(
            initialdir = "../",
            title = "Select a folder location",
            )
        
        if stringtoChange != None:
            stringtoChange.set(self.variables[locVar])
    
    
    
    
    def play_Board(self):
        
        
        toIgnore = [
            "Picture to Solve<optional>:  "
            ]
        
        for i in self.labelHolder:
            y = self.parameters[self.curMode][i][self.param_varTarget]
            
            x = 0
            try:
                x = (self.paramHolder[i].get())
            except:
                try:
                    x = (self.paramHolder[i].get("1.0", "end"))
                except:
                    pass
            
            if i not in toIgnore:
                self.variables[y] = x
        
        toInt = [
            "Time",
            "SizeX",
            "SizeY",
            "HowManyNum",
            "NumLength",
            "InitialLetters",
            "CheckTime",
            "HideChance",
            ]
        
        for i in toInt:
            self.variables[i] = int(self.variables[i])
            
        
    
        self.variables["OnePath"] = False if self.variables["OnePath"]==0 else True
            
        print(self.curMode, self.variables)
        
        self.root.destroy()
        
        self.load_Game()
        
        
    def print_Board(self):
        #filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        #print (filename)
        self.print_Window()
    
    
    
    
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
            
            puzzle_game_main.mainGame(ns, ns.title).build(self.variables["Time"]*60)
            
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
            
            puzzle_game_main.mainGame(cw, cw.title).build(self.variables["Time"]*60)
        
        def C():
            mz = MazeB()
            mz.setBoard(self.variables["SizeX"],self.variables["SizeY"], ".")
            
            #mz.setOnePath(self.variables["OnePath"])
            
            mz.buildBoard()
                
            puzzle_game_main.mainGame(mz, mz.title).build(self.variables["Time"]*60)
        
        def D():
            kk = Kakuro()
            kk.setBoard(self.variables["SizeX"],self.variables["SizeY"], ".")
            
            kk.difficulty = self.variables["HideChance"]/100
            
            kk.buildBoard()
            
            puzzle_game_main.mainGame(kk, kk.title).build(self.variables["Time"]*60, self.variables["CheckTime"]*60)
            
        def E():
            
            hd = Hidato()
            
            
            hd.diagonals = (self.variables["Direction"] == "Diagonal Included")
            hd.difficulty = self.variables["HideChance"]/100
            
            if (self.variables["SizeX"]+self.variables["SizeY"])//2 > 6:
                hd.pureRandomRate = 0.75
                hd.extremeFast = True
            
            hd.setBoard(self.variables["SizeX"], self.variables["SizeY"], '.')
            
            hd.buildBoard()
            
            puzzle_game_main.mainGame(hd, hd.title).build(self.variables["Time"]*60, diagonals=(self.variables["Direction"] == "Diagonal Included"))
            
        def F():
            nn = Nonogram()
            
            if self.variables["NonogramFile"] == 0:
                #load an image based on the input
                dir_loc = "NonoImages/" + self.variables["Size_Nono"] + "/"
                
                nn.loadImage(dir_loc + random.choice(os.listdir(dir_loc)))
            
            else: nn.loadImage(self.variables["NonogramFile"], self.variables["Size_Nono"])
            
            nn.buildBoard()
            
            
            puzzle_game_main.mainGame(nn, nn.title).build(self.variables["Time"]*60)
            
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
            
            puzzle_game_main.mainGame(cc, cc.title).build(self.variables["Time"]*60)
          
        if self.curMode == "Number Search": A()
        elif self.curMode == "Crossword":   B()
        elif self.curMode == "Maze":    C()
        elif self.curMode == "Kakuro":  D()
        elif self.curMode == "Hidato":  E()
        elif self.curMode == "Nonogram":    F()
        elif self.curMode == "Cryptogram":    G()
            
    def print_Game(self):
        
        def printProc():
        
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
            
            # To fix
            # Very important
            '''
            >  B = Crossword ||| 
                In the puzzle menu, pass the list of text file to process. Pass the list into the crossword processor
                
                Create a method inside crossword that will accept a file location(s).
                It will open the text file with properly formatted text and parse it into processible string
                After processing the text, call the setKeys(within the function) itself
                
                ! Remove the amount to generate, instead replace it with button to get the list of crossword
                
                In the printer pygame class, set a function that calls the processor multiple times
            '''
            
            '''
            >  F = Nonogram ||| 
                In the puzzle menu, pass the list of image files to process. Pass the list into the nonogram processor
                
                Create a method inside nonogram that will accept a file location(s).
                It will open the images in file location, call the processor function and etc
                After processing the text, call the setKeys(within the function) itself
                
                ! Remove the amount to generate, instead replace it with button to get the list of crossword
                
                In the printer pygame class, set a function that calls the processor multiple times
            '''
            
            '''
            >  G = Cryptogram ||| 
                In the puzzle menu, pass a text file location to process. Pass the list into the cryptogram processor
                
                Create a method inside Cryptogram that will accept a file location(s).
                It will open the text file with properly formatted text and parse it into processible string
                After processing the text, call the setKeys(within the function) itself
                
                ! Remove the amount to generate, instead replace it with button to get the list of crossword
                
                In the printer pygame class, set a function that calls the processor multiple times
            '''
            
            # Important
            '''
            >  D = Kakuro ||| 
                Code a generator algorithm that will generate a board with unique solution
                
                Do the high low high technique that scans only puts number with unique solutions in the board
                ^ This will be a recursion
                
            '''
            
            # Need Attention
            '''
            >  E = Hidato ||| 
                The hidato generator algorithm is too slow!!!
            '''
            
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
                
                extension = "/NumberSearch"
                
                puzzle_game_main.mainGame(ns, ns.title).printBoard(int(self.printAmount.get()),\
                                                                    self.variables["SaveLocation"]+extension, int(self.printSize.get()))
                
            def B():
                cw = Crossword()
                cw.setBoard(self.variables["SizeX"], self.variables["SizeY"], ".")
                
                #x = self.variables["Key"].strip()
                
                cw.createTextQueue(self.variables["FileList"])

                dirModes = {
                    "Down Right": 0, 
                    "Down Right and Reverse":1
                }
    
                cw.setDirection(dirModes[self.variables["Direction"]])
                
                cw.difficulty = self.variables["HideChance"]/100
                
                #cw.buildBoard()
                #cw.printBoard()
                extension = "/Crossword"
                puzzle_game_main.mainGame(cw, cw.title).printBoard(cw.amount,\
                                                                    self.variables["SaveLocation"]+extension, int(self.printSize.get()))
            
            def C():
                mz = MazeB()
                mz.setBoard(self.variables["SizeX"],self.variables["SizeY"], ".")
                
                #mz.setOnePath(self.variables["OnePath"])
                
                mz.buildBoard()
                    
                extension = "/Maze"
                puzzle_game_main.mainGame(mz, mz.title).printBoard(int(self.printAmount.get()), \
                                                                    self.variables["SaveLocation"]+extension, int(self.printSize.get()))
            
            def D():
                kk = Kakuro()
                kk.setBoard(self.variables["SizeX"],self.variables["SizeY"], ".")
                
                kk.difficulty = self.variables["HideChance"]/100
                
                kk.buildBoard()
                
                extension = "/Kakuro"
                puzzle_game_main.mainGame(kk, kk.title).printBoard(int(self.printAmount.get()), \
                                                                    self.variables["SaveLocation"]+extension, int(self.printSize.get()))
                
            def E():
                hd = Hidato()
                
                
                hd.diagonals = (self.variables["Direction"] == "Diagonal Included")
                hd.difficulty = self.variables["HideChance"]/100
                
                if (self.variables["SizeX"]+self.variables["SizeY"])//2 > 6:
                    hd.setRandomRate(0.75)
                    hd.extremeFast = True
                
                hd.setBoard(4,4, '.')
                
                hd.buildBoard()
                
                hd.setBoard(self.variables["SizeX"], self.variables["SizeY"], '.')
                
                extension = "/Hidato"
                puzzle_game_main.mainGame(hd, hd.title).printBoard(int(self.printAmount.get()),\
                                                                    self.variables["SaveLocation"]+extension, int(self.printSize.get()))
                
            def F():
                nn = Nonogram()
                
                '''if self.variables["NonogramFile"] == 0:
                    #load an image based on the input
                    dir_loc = "NonoImages/" + self.variables["Size_Nono"] + "/"
                    
                    nn.loadImage(dir_loc + random.choice(os.listdir(dir_loc)))'''
                
                nn.createImageQueue(self.variables["FileList"])
                
                nn.setImageQueueSize(self.variables["Size_Nono"])
                
                #else: nn.loadImage(self.variables["NonogramFile"])
                
                #nn.buildBoard()
                
                extension = "/Nonogram"
                puzzle_game_main.mainGame(nn, nn.title).printBoard(nn.amount,\
                                                                    self.variables["SaveLocation"]+extension, int(self.printSize.get()))
                
            def G():
                    
                cc = Cryptogram()
                
                cc.createTextQueue(self.variables["FileLocation"])
                    
                cc.revealAmount = self.variables["InitialLetters"]
                #cc.process_Text()
                
                extension = "/Cryptogram"
                puzzle_game_main.mainGame(cc, cc.title).printBoard(cc.amount, \
                                                                    self.variables["SaveLocation"]+extension, int(self.printSize.get()))
              
            if self.variables["SaveLocation"] == 0:
                self.variables["SaveLocation"] = "./"
              
            if self.curMode == "Number Search": A()
            elif self.curMode == "Crossword":   B()
            elif self.curMode == "Maze":    C()
            elif self.curMode == "Kakuro":  D()
            elif self.curMode == "Hidato":  E()
            elif self.curMode == "Nonogram":    F()
            elif self.curMode == "Cryptogram":    G()
    
        toIgnore = [
            "Picture to Solve<optional>:  "
            ]
        
        for i in self.labelHolder:
            y = self.parameters[self.curMode][i][self.param_varTarget]
            
            x = 0
            try:
                x = (self.paramHolder[i].get())
            except:
                try:
                    x = (self.paramHolder[i].get("1.0", "end"))
                except:
                    pass
            
            if i not in toIgnore:
                self.variables[y] = x
        
        toInt = [
            "Time",
            "SizeX",
            "SizeY",
            "HowManyNum",
            "NumLength",
            "InitialLetters",
            "CheckTime",
            "HideChance",
            ]
        
        for i in toInt:
            self.variables[i] = int(self.variables[i])
            
    
        self.variables["OnePath"] = False if self.variables["OnePath"]==0 else True
        
        
        print(self.curMode, self.variables)
        
        printProc()
        
        self.root.destroy()
        PuzzlePack()
        
        
        
        
    def run(self):
        self.mainwindow.mainloop()



if __name__ == "__main__":
    PuzzlePack()
