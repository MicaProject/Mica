#pip install winshell
#source https://www.codespeedy.com/create-the-shortcut-of-any-file-in-windows-using-python/
import os,sys

def create_shortcut(name,target,icon=False,destinationFolder=False):
    if sys.platform == "win32":
        create_shortcut_windows(name,target,icon,destinationFolder)

def create_shortcut_windows(name,target,icon=False,destinationFolder=False):
    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    if destinationFolder:#whatever else that is not false is custom
        shortcut = shell.CreateShortCut(destinationFolder+"\\{}.lnk".format(name))
    else:
        shortcut = shell.CreateShortCut("\\".join(target.split("\\")[:-1])+"\\{}.lnk".format(name))
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = "\\".join(target.split("\\")[:-1])
    if icon: 
        shortcut.IconLocation = icon
    shortcut.save()
    