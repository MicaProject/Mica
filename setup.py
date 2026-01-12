import sys, os, time
import subprocess, platform 
os.chdir(os.path.dirname(__file__))
from tools import set_script_as_global, shortcutCreator

def setup():

    try:
        print("Making scripts available everywhere")
        os.chdir(os.path.dirname(__file__))
        set_script_as_global.set("mica")
    except:
        print("Whoops, something happened")

    try:
        print("Creating shortcut")
        os.chdir(os.path.join(os.path.dirname(__file__),"tools"))
        print(os.getcwd())
        target = os.path.join(os.path.dirname(__file__),"mica.py")
        print(target)
        shortcutCreator.create_shortcut(name="Mica Assistant",target=target,icon=os.path.join(os.path.dirname(__file__),"tools","mica.ico"))
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"docs","index.html")
    except:
        print("Whoops, something happened")

    os.system('pip install prompt_toolkit')#its the only one we have to install first

    try:
        #opening the presentation page
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))
    except:
        print("Whoops, something happened")
    print("Setup complete, will terminate in 5 seconds")
    time.sleep(5)
if __name__ == "__main__":
    setup()
