
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('random_word')
install('Pillow')
install('numpy')
install('opencv-python')
install('pysciter')