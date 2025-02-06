import os, sys
import time
def __init__(self):
    self.command_manifest.append({"plugin":__name__,"function":"get_variable_origin","command":"origin","help":"Returns the file and line of a variable's initialisation","args":["self"],"rargs":[]})
    self.command_manifest.append({"plugin":__name__,"function":"load_plugin_wrapper","command":"plug","help":"(plugin/path/plugin_name) Starts the designated plugin","args":["self"],"rargs":[]})
    self.command_manifest.append({"plugin":__name__,"function":"stop","command":"quit","help":"Stops The assistant","args":["self"],"rargs":[]})
    self.command_manifest.append({"plugin":__name__,"function":"restart","command":"r","help":"Restarts The assistant","args":["self"],"rargs":[]})
    self.command_manifest.append({"plugin":__name__,"function":"restart","command":"restart","help":"Restarts The assistant","args":["self"],"rargs":[]})
    self.command_manifest.append({"plugin":__name__,"function":"update","command":"update","help":"Pulls from the repository and restarts","args":["self"],"rargs":[]})
    self.command_manifest.append({"plugin":__name__,"function":"set_variable","command":"set","help":"Sets an available variable to a desired value","args":["self"],"rargs":[]})
    self.command_manifest.append({"plugin":__name__,"function":"list_variables","command":"list","help":"Lists the variables in the Mica instance","args":["self"],"rargs":[]})
    self.check_subdict_in_dict_list = check_subdict_in_dict_list


def get_variable_origin(self,varname):
    files_to_check = [*self.config["plugins_to_start"]]

    for plugin in self.config["plugins_to_start"]:
        with open(os.path.join(plugin["path"],plugin["name"]+'.py'),"r") as f:
            lines = f.readlines()
        for i,line in enumerate(lines):
            if f".{varname}=" in line.replace(' ',''):

                self.text_output.append(f'Variable "{varname}" is first initialised in {os.path.join(plugin["path"],plugin["name"]+".py")} line {i}')
                return
    self.text_output.append(f'Variable "{varname}" is not found in any file in the config')

def load_plugin_wrapper(self, plugin_path):
    directory = '/'.join(plugin_path.replace('\\','/').split('/')[:-1])
    file = plugin_path.replace('\\','/').split('/')[-1].replace('.py','')
    plugin = {"path":directory,"name":file}
    try:
        self.load_plugin(plugin)
        self.text_output.append(f'Plugin {file} loaded sucessfully')
    except Exception as e:
        self.text_output.append(f'Plugin {file} not loaded ({e})')

def unload_plugin(self, plugin_name):
    for index, callback in enumerate(self.callbacks[:]):
        if callback["plugin"] == plugin_name:
            self.unsubscribe_from_variable(callback["variable"],callback["plugin"],callback["function"])

    for index, command in enumerate(self.command_manifest):
        if command["plugin"] == plugin_name:
            self.command_manifest.pop(index)

    del globals()[plugin_name]
    self.text_output.append(f'Plugin {plugin_name} unplugged')
    
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
        self.text_output.append("Changed "+var_name+" to "+str(new_value))
    except:
        self.text_output.append("Cant change "+var_name+"("+type(self.__dict__[var_name])+")"+" to "+str(new_value))
        
def list_variables(self):
    self.text_output.extend([varname for varname in self.__dict__])
        
    
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