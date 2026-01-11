import os
import copy
import json
import sys
import importlib
from inspect import getmembers, isfunction
import types
import threading



class PluginManager:
    mandatory_config_keys = []
    accent_color = "\x1b[38;2;79;193;255m"
    normal_color = "\033[0m"
    plugins = {}
    threads = {}
    imported_plugin_names = []
    
    def __init__(self,config_path,load_verbose = True):
        self.working_directory = os.getcwd()
        
        if load_verbose:
            print(self.accent_color+"Initiating Plugin Manager..."+self.normal_color)
            print("Loading file",config_path)
            
        with open(config_path, "r") as f:
            self.config = json.load(f)
        for key in self.config.keys(): self.__dict__[key] = self.config[key]
        
        plugins_to_import = self.loaded_plugins[:]
        name_cache = ""
        i=0
        while len(plugins_to_import) > 0:
            current_plugin = plugins_to_import.pop(0)
            if load_verbose:
                print(self.accent_color+current_plugin["name"]+self.normal_color+"... ",end = "", flush = True)
            is_loaded = self.load_plugin(current_plugin)
            if is_loaded == True:
                self.imported_plugin_names.append(current_plugin["name"])
                name_cache = ""
                if load_verbose:
                    print("Done")
            else:
                if load_verbose:
                    print("Waiting for parent plugins")
                plugins_to_import.append(current_plugin)
                if current_plugin["name"] != name_cache:
                    name_cache = current_plugin["name"]
                else:
                    raise ImportError(f"Plugin {name_cache} has missing parents")
    
    def load_plugin(self,plugin):
        self.plugins[plugin["name"]] = self.path_import(os.path.abspath(plugin["path"]),plugin["name"])
        if "required_plugins" in self.plugins[plugin["name"]].__dict__.keys():
            if any(requirement not in self.imported_plugin_names for requirement in self.plugins[plugin["name"]].required_plugins):
                return self.plugins[plugin["name"]].required_plugins
            
        for attribute, method in getmembers(self.plugins[plugin["name"]], isfunction):
            if not attribute.startswith("__") and method.__module__ == self.plugins[plugin["name"]].__name__:
                bound_method = types.MethodType(copy.deepcopy(method), self)
                self.__dict__[attribute] = bound_method
                globals()[attribute] = copy.deepcopy(getattr(self.plugins[plugin["name"]], attribute))
                
        
        if "__init__" in self.plugins[plugin["name"]].__dict__.keys():
            self.plugins[plugin["name"]].__init__(self)
        
        return True
    
    def execute_method(self, method_dict):
        arguments = []
        keyword_arguments = {}
        if isinstance(method_dict["method"],str):
            correct_module = self.plugins[method_dict["plugin"]]
            f = getattr(correct_module, method_dict["method"])
            arguments.append(self)
        else:
            f = method_dict["method"]
            
        if "args" in method_dict.keys(): arguments.extend(method_dict["args"])

        if "kwargs" in method_dict.keys(): keyword_arguments = method_dict["kwargs"]
        
        if "dargs" in method_dict.keys(): arguments.extend([self.__dict__[darg] for darg in method_dict["dargs"]])
        #Delayed args are something that you can create with a lamda method
        #https://medium.com/skiller-whale/late-binding-variables-its-a-trap-c17af980164f
        #kept if you need to use pugin specific
        
        if "thread" in method_dict.keys() and method_dict["thread"]:
            self.threads[method_dict["cmd"]] = threading.Thread(target=f,daemon = True, args = arguments, kwargs = keyword_arguments)
            self.threads[method_dict["cmd"]].start()
        else:
            f(*arguments, **keyword_arguments)
            
    #backend methods, used to initialise backends before running the init, this is useful if you need specific capabilities required by all of your plugins
    
    def initialise_command_backend(self,custom_backend = False):
        self.command_backend = {"name":"commands", "path":os.path.abspath(os.path.join(os.path.dirname(__file__),"default_plugins"))}
        if custom_backend != False:
            self.command_backend = custom_backend
        self.load_plugin(self.command_backend)
        self.imported_plugin_names.append(self.command_backend["name"])

    def initialise_event_backend(self,custom_backend = False):
        self.event_backend = {"name":"event_manager", "path":os.path.abspath(os.path.join(os.path.dirname(__file__),"default_plugins"))}
        if custom_backend != False:
            self.event_backend = custom_backend
        self.load_plugin(self.event_backend)
        self.imported_plugin_names.append(self.event_backend["name"])

    def path_import(self, directory,module_name):
        sys.path.insert(0, directory)
        module = importlib.import_module(module_name)
        sys.path.pop(sys.path.index(directory))
        return module
