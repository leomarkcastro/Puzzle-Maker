from puzzle.puzzle_HTMLGeneral import Frame
import os

os.chdir("./puzzle")

if __name__ == '__main__':
    # create window
    frame = Frame()
    
    #debug as on
    frame.setup_debug()

    # load file
    frame.load_file("./html/index.html")

    frame.run_app()