import os,sys
from sys import argv
import subprocess

def analyseFile(filePath):
    #print('Analyse path :',filePath)
    packageList = []
    #print(filePath[len(filePath) - 3:])
    if ".py" != filePath[len(filePath) - 3:]:
        return []
    with open(filePath, errors='replace') as f:
        
        lines = f.readlines()
        
        for line in lines:
            if '#pip install' in line and not filePath.endswith("pipScan.py"):
                line = line.split(' ')
                i = 0
                endOfLine = False
                while "#pip" not in line[i] and not endOfLine:
                    i = i+1
                    if i+1 == len(line):
                        endOfLine = True
                if not endOfLine:
                    word = line[i+2].strip('\n')
                    
                    packageList.append(word)
        f.close()
    return packageList
    
def installPackage(package):
    if "win32" in sys.platform:
        command = ["python -m pip install"]
    else:
        command = ["pip3 install"]
    
    command.append(package)
    #print(' '.join(command))
    process = subprocess.Popen(' '.join(command),
                        stdout = subprocess.PIPE, 
                        stderr = subprocess.PIPE,
                        text = True,
                        shell = True)
    while True:
        output = process.stdout.readline().strip()
        if output != '':
            print(output)
        if 'error' in output:
            return ['',package]
            break
        return_code = process.poll()
        if return_code is not None:
            #print(f'Returned the following return code: {return_code}')
            for std_output in process.stdout.readlines():
                print(std_output)
                return [package,'']
            for std_err in process.stderr.readlines():
                print(std_err)
                return ['',package]
            return [package,'']

def pipScan(path,autoInstall = True):
    print("Scanning for packages in",path)
    
    packages = []
    ignoreList = ['psd-tools3',"pickle"]
    if os.path.isfile(path):
        analyseFile(path)
    else:
        for root,dirs,files in os.walk(path,topdown = False):
            
            for name in files:
                print("Packages found :",len(packages),end='\r')
                if 'MicaP_v2' not in root and 'chatbotfiles' not in root :
                    
                    packages.extend(analyseFile(os.path.join(root,name)))

    #getting rid of doubles
    newList = []
    for element in packages:
        if element not in newList and not element in ignoreList:
            newList.append(element)
    packages = newList
    print("")

    if autoInstall:
        complete = []
        error = []
        for package in packages:
            print("Installing package",package)
            status = installPackage(package)
            if status[0] != '':
                complete.append(status[0])
            else:
                error.append(status[1])
        print("----------------------------------------------------")
        print("Installation complete !")
        print("Sucessful installs :",len(complete))
        print("Failed installs :",len(error))
        if len(error)>0:
            print(error)
if "main" in __name__:
    pipScan(argv[1])