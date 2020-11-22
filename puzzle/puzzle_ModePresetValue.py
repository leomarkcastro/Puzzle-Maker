class ModePresets():
    
    def __init__(self):
        self.NumberSearch()
        self.Crossword()
        self.Maze()
        self.Kakuro()
        self.Hidato()
        self.Nonogram()
        self.Cryptogram()
    
    def NumberSearch(self):
        ############################## EASY PARAMETERS ##############################
        
        self.ns_eas_width = 10       #Parameters range are 6 to 30
        self.ns_eas_height = 10      #Parameters range are 6 to 30
        self.ns_eas_howMany = 8      #Parameters range are 1 to 23
        self.ns_eas_length = 6       #Parameters range are 5 to 15
        self.ns_eas_direction = 0    #Parameters in option: 0 -> Down Right |+| 1 -> Down Right Diagonal |+| 2 -> All Direction
        
        ############################## MEDIUM PARAMETERS ##############################
        
        self.ns_med_width = 15
        self.ns_med_height = 15
        self.ns_med_howMany = 13
        self.ns_med_length = 8
        self.ns_med_direction = 1
        
        ############################## HARD PARAMETERS ##############################
        
        self.ns_hard_width = 20
        self.ns_hard_height = 20
        self.ns_hard_howMany = 19
        self.ns_hard_length = 10
        self.ns_hard_direction = 2
        
    
    def Crossword(self):
        ############################## EASY PARAMETERS ##############################
        
        self.cw_eas_hideChance = 60     #Parameters range from [1 to 100]
        self.cw_eas_directions = 0      #Parameters options [0 -> Down Right |+| 1 -> Down Right and Reverse]
        
        ############################## MEDIUM PARAMETERS ##############################
        
        self.cw_med_hideChance = 70
        self.cw_med_directions = 1
        
        ############################## HARD PARAMETERS ##############################
        
        self.cw_hard_hideChance = 80
        self.cw_hard_directions = 1
    
    def Maze(self):
        ############################## EASY PARAMETERS ##############################
        
        self.mz_eas_width= 15       #Parameters range from [6 to 45]
        self.mz_eas_height = 15     #Parameters range from [6 to 40]
        
        ############################## MEDIUM PARAMETERS ##############################
        
        self.mz_med_width= 30
        self.mz_med_height = 30
        
        ############################## HARD PARAMETERS ##############################
        
        self.mz_hard_width= 40
        self.mz_hard_height = 40
    
    def Kakuro(self):
        ############################## EASY PARAMETERS ##############################
        
        self.kk_eas_hideChance = 40     #Parameters range from [1 to 100]
        self.kk_eas_width = 5           #Parameters range from [6 to 35]
        self.kk_eas_height = 5          #Parameters range from [6 to 35]
        
        ############################## MEDIUM PARAMETERS ##############################
        
        self.kk_med_hideChance = 95
        self.kk_med_width = 15
        self.kk_med_height = 15
        
        ############################## HARD PARAMETERS ##############################
        
        self.kk_hard_hideChance = 100
        self.kk_hard_width = 20
        self.kk_hard_height = 20
    
    def Hidato(self):
        ############################## EASY PARAMETERS ##############################
        
        self.hd_eas_hideChance = 50     #Parameters range from [1 to 70]
        self.hd_eas_width = 4           #Parameters range from [3 to 15]
        self.hd_eas_height = 4          #Parameters range from [3 to 15]
        self.hd_eas_directions = 0      #Parameters options [0-> No diagonals |+| 1-> Diagonals Included]
        
        ############################## MEDIUM PARAMETERS ##############################
        
        self.hd_med_hideChance = 50
        self.hd_med_width = 8
        self.hd_med_height = 8
        self.hd_med_directions = 1
        
        ############################## HARD PARAMETERS ##############################
        
        self.hd_hard_hideChance = 50
        self.hd_hard_width = 10
        self.hd_hard_height = 10
        self.hd_hard_directions = 1
    
    def Nonogram(self):
        ############################## EASY PARAMETERS ##############################
        
        self.nn_eas_boxSize = 0     #Parameters options [0 -> 16x16 || 1 -> 24x24 || 2 -> 32x32 || 3 -> 48x48]
        
        ############################## MEDIUM PARAMETERS ##############################
        
        self.nn_med_boxSize = 1
        
        ############################## HARD PARAMETERS ##############################
        
        self.nn_hard_boxSize = 2
    
    def Cryptogram(self):
        ############################## EASY PARAMETERS ##############################
        
        self.cc_eas_showLetter = 5      #Parameters range from [0 to 26]
        
        ############################## MEDIUM PARAMETERS ##############################
        
        self.cc_med_showLetter = 2
        
        ############################## HARD PARAMETERS ##############################
        
        self.cc_hard_showLetter = 0
    
ModePresets = ModePresets()