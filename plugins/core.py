import os, sys
import time
import importlib.util
def __init__(self):
    self.external_methods.append({"plugin":__name__,"method":self.get_variable_origin,"cmd":"origin","help":"Returns the file and line of a variable's initialisation","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.load_plugin_wrapper,"cmd":"plug","help":"(plugin/path/plugin_name) Starts the designated plugin","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.load_plugin_wrapper,"cmd":"unplug","help":"(plugin/path/plugin_name) Stops the designated plugin","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.stop,"cmd":"quit","help":"Stops The assistant","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.restart,"cmd":"r","help":"Restarts The assistant","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.restart,"cmd":"restart","help":"Restarts The assistant","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.update,"cmd":"update","help":"Pulls from the repository and restarts","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.set_variable,"cmd":"set","help":"Pulls from the repository and restarts","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.list_variables,"cmd":"list","help":"Pulls from the repository and restarts","args":[],"dargs":[]})
    if "check_packages" in self.__dict__ and self.check_packages:
        self.install_missing_packages(os.getcwd())

def install_missing_packages(self,path):
    for root,dirs,files in os.walk(path,topdown = False):
        for file in files:
            if file.endswith(".py") and file not in ["core.py", "pipScan.py"]:
                with open(os.path.join(root,file),"r", encoding="utf-8") as f:
                    for line in f.readlines():
                        if line.lstrip().startswith("from ") or line.lstrip().startswith("import "):
                            package_names = line.lstrip().split(' ')[1].split('.')[0].strip().split(',')
                            for package_name in package_names:
                                if package_name in ['']:
                                    continue
                                spec = importlib.util.find_spec(package_name)
                                if spec is None:
                                    #print([package_name],"is not installed")
                                    if "pip install " in line:
                                        package_name = line.split("pip install ")[1]
                                        print("installing with command: pip install",package_name)
                                        os.system("pip install "+package_name)
                        

def get_variable_origin(self,varname):
    files_to_check = [*self.config["plugins_to_start"]]

    for plugin in self.config["plugins_to_start"]:
        with open(os.path.join(plugin["path"],plugin["name"]+'.py'),"r") as f:
            lines = f.readlines()
        for i,line in enumerate(lines):
            if f".{varname}=" in line.replace(' ',''):

                self.output_text(f'Variable "{varname}" is first initialised in {os.path.join(plugin["path"],plugin["name"]+".py")} line {i}')
                return
    self.output_text(f'Variable "{varname}" is not found in any file in the config')

def load_plugin_wrapper(self, plugin_path):
    directory = '/'.join(plugin_path.replace('\\','/').split('/')[:-1])
    file = plugin_path.replace('\\','/').split('/')[-1].replace('.py','')
    plugin = {"path":directory,"name":file}
    try:
        self.load_plugin(plugin)
        self.output_text(f'Plugin {file} loaded sucessfully')
    except Exception as e:
        self.output_text(f'Plugin {file} not loaded ({e})')

def unload_plugin(self, plugin_name):
    for index, callback in enumerate(self.callbacks[:]):
        if callback["plugin"] == plugin_name:
            self.unsubscribe_from_variable(callback["variable"],callback["plugin"],callback["method"])

    for index, command in enumerate(self.external_methods):
        if command["plugin"] == plugin_name:
            self.external_methods.pop(index)

    del globals()[plugin_name]
    self.output_text(f'Plugin {plugin_name} unplugged')
    
def check_subdict_in_dict_list(self, subdict, dict_list):
    for full_dict in dict_list:
        if subdict.items() <= full_dict.items():
            return True
    return False

def stop(self):
    self.running = False
    
def set_variable(self,var_name,new_value):
    try:
        if isinstance(self.__dict__[var_name],str):
            self.__dict__[var_name] = str(new_value)
        elif isinstance(self.__dict__[var_name],bool):
            self.__dict__[var_name] = bool(new_value)
        elif isinstance(self.__dict__[var_name],int):
            self.__dict__[var_name] = int(new_value)
        elif isinstance(self.__dict__[var_name],float):
            self.__dict__[var_name] = float(new_value)
        self.output_text("Changed "+var_name+" to "+str(new_value))
    except:
        self.output_text("Cant change "+var_name+"("+type(self.__dict__[var_name])+")"+" to "+str(new_value))
        
def list_variables(self):
    for varname in self.__dict__:
        self.output_text(varname)
    
        
    
def restart(self):
    os.system('start cmd.exe @cmd /k "python mica.py"')
    time.sleep(0.3)
    os.system("title MICAEND")
    os.system('taskkill /f /fi "WindowTitle eq MICAEND"')
    self.restart = True
    stop(self)
    
def update(self):
    os.chdir(self.root_directory)
    os.system("git pull")
    restart(self)