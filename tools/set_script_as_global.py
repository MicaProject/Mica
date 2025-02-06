#Unfinished and untested
import shutil
import os,sys
import subprocess
def get_filepath(filename):
    for root, dirs, files in os.walk(os.getcwd(),topdown=True):
        for file in files:
            print(file)
            if filename == file or filename+'.py' == file:
                return os.path.join(root,'')

def create_file(scriptname,filepath):
    with open(f'{scriptname}.pth', 'w') as f:
        f.write(filepath)
        print("Path written :",filepath)
        f.close()
    walletPath = os.path.dirname(os.path.realpath(__file__))
    return walletPath

def move_windows():
    n = 0
    list = []
    for root,dirs,files in os.walk('C:\\Users\\',topdown = False):
        for name in dirs:
            if "Program" in os.path.join(root,name) and False:
                print(os.path.join(root,name))
                print(name)
            print('Checked',n,'folders',end='\r')
            
            if 'site-packages' == name and 'Python3' in root:
                print('Found python installation :',os.path.join(root,name))
                list.append(os.path.join(root,name))
                #shutil.move('wallet.pth',os.path.join(root,name,'wallet.pth'))
            n = n +1
    print("")
    return list

def move_linux():
    n = 0
    list = []
    process = subprocess.Popen('python3 -m site --user-site',
                        stdout = subprocess.PIPE, 
                        stderr = subprocess.PIPE,
                        text = True,
                        shell = True)
    while True:
        output = process.stdout.readline().strip()
        if output != '':
            print(output)
            path =str(output)
            return [path]

def set(scriptName):
    if sys.platform == 'win32':
        L = move_windows()
    else:
        L = move_linux()

    filepath = get_filepath(scriptName)
    
    for path in L:
        pth_path = os.path.join(path,scriptName+'.pth')
        if os.path.isfile(pth_path):
            if open(pth_path,'r').readline(0) == filepath:

                continue
        
        walletPath = create_file(scriptName,filepath)
        shutil.move(scriptName+'.pth',pth_path)
        print(scriptName,"added to",path)
    try:
        os.remove(os.path.join(walletPath,'wallet.pth'))
    except:
        pass

if __name__ == "__main__":
    sys.path.insert(1, os.path.join(os.path.dirname(__file__),'..'))
    #os.chdir(os.path.join(os.path.dirname(__file__),'..'))
    set("fal")
    set("mica")