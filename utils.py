import os

def banner():
    import os, psutil  # Get the parent process name. #pip install psutil
    pprocName = psutil.Process(os.getppid()).name()
    if "cmd.exe" in pprocName:
        os.system('color')
    try:
        with open(".git/HEAD","r") as f:
            branch = f.readlines()[0].replace("ref: refs/heads/",'').strip()
    except:
        branch = "unknown"
    redux =r""" __  __  ___   ____     _    
|  \/  ||_ _| / ___|   / \   
| |\/| | | | | |      / _ \ The Ghost
| |  | | | | | |___  / ___ \ In the Machine
|_|  |_||___| \____|/_/   \_\ """
    infos = "Modular Interdependent Chatbot for Assistance - "+branch+" branch"
    print("\x1b[38;2;79;193;255m",end='')
    print(redux)
    print(infos)
    print('',end = '\033[0m\n')

def send_notification(title,text):
    from plyer import notification

    notification.notify(
        title = title,
        message = text,
        app_name = "Mica",
        app_icon = os.path.join(os.path.dirname(__file__),"..","tools","mica.ico"),
        timeout = 2,
    )