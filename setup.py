import sys, os
os.chdir(os.path.dirname(__file__))
from tools import pipScan, set_script_as_global, shortcutCreator

def setup():
    print("Making scripts available everywhere")
    os.chdir(os.path.dirname(__file__))
    set_script_as_global.set("mica")

    print("Installing required packages")
    pipScan.pipScan(os.path.dirname(__file__))

    print("Creating shortcut")
    os.chdir(os.path.join(os.path.dirname(__file__),"tools"))
    print(os.getcwd())
    target = os.path.join(os.path.dirname(__file__),"mica.py")
    print(target)
    shortcutCreator.create_shortcut(name="Mica Assistant",target=target,icon=os.path.join(os.path.dirname(__file__),"tools","mica.ico"))

if __name__ == "__main__":
    setup()