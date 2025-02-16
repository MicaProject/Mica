import json
import os, sys
import time
import threading
import types

#              .___________                __                
#  ____ ______ |__\_   ___ \  ____   _____/  |_  ___________ 
#_/ __ \\____ \|  /    \  \/_/ __ \ /    \   __\/ __ \_  __ \
#\  ___/|  |_| |  \     \___\  ___/|   |  \  | \  ___/|  | \/
# \_____|   __/|__|\________/\_____|___|__/__|  \_____|__|   
#       |__| 
# Epicenter Version 1
# hash 3.12.3
# -6960679630773435528


class epiCenter():
    
    running = False
    callbacks = [] #Must look like: {"variable": "var_to_watch", "plugin": "plugin_name", "function":"function_name", "thread":True/False, "args":["self"], "kwargs":{"k1":True}}
    success_color = "\x1b[38;2;35;209;139m"
    failure_color = "\x1b[38;2;241;76;76m"
    default_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"epicenter_config.json")
    def __init__(self, config_file_path = default_config_file):
        #forcing the cwd to be pointing to the root path
        os.chdir(os.path.dirname(__file__))
        if os.path.exists(config_file_path):
            self.config_path = config_file_path
        else:
            self.config_path = self.default_config_file
        
        self.debug_callback = False
        

        #Small manipulation to simplify life down the line
        self.__dict__["self"] = self
        self.override_warnings = True
        self.plugins = {}
        with open(self.config_path,'r') as conf:
            self.config = json.load(conf)
        #print(self.config)
        if "print_errors" in self.config.keys():
            self.print_errors = self.config["print_errors"]
        else:
            self.print_errors = True

        if "break_on_error" in self.config.keys():
            self.break_on_error = self.config["break_on_error"]
        else:
            self.break_on_error = True
        
        if "config_name" in self.config.keys():
            self.config_name = self.config["config_name"]
            print("Loading plugins from "+self.success_color+self.config_name+"\033[0m")
        else:
            print("Loading plugins")

        for plugin in self.config["plugins_to_start"]:

            print(f"{self.success_color}{plugin['name']}\033[0m...",end = ' ',flush=True)
            try:
                self.load_plugin(plugin)
                print("Done")
            except Exception as e:
                print("Failed")
                if self.break_on_error:
                    raise e
                if self.print_errors:
                    print(e)
                
            

        print("Plugins loaded successfuly")

    def load_plugin(self, plugin):
        if plugin["path"] not in sys.path:
                sys.path.append(plugin["path"])

        if "class" in plugin.keys():

            components = plugin["class"].split('.')
            mod = __import__(plugin["name"])
            for comp in components:#https://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
                mod = getattr(mod, comp)
            
            self.plugins[plugin["name"]] = mod

            for attribute in self.plugins[plugin["name"]].__dict__.keys():
                if not attribute.startswith('__'):
                    if attribute in self.__dict__.keys() and self.override_warnings:
                        print(f'Warn: Existing attribute "{attribute}" ({type(self.plugins[plugin["name"]].__dict__[attribute])}) from plugin {plugin["name"]} is overriding an existing attribute')
                    if callable(self.plugins[plugin["name"]].__dict__[attribute]):
                        setattr(self,attribute,self.plugins[plugin["name"]].__dict__[attribute].__get__(self, self.__class__))
                    else:
                        setattr(self,attribute,self.plugins[plugin["name"]].__dict__[attribute])
                    
            
        else:
            self.plugins[plugin["name"]] = __import__(plugin["name"])
            for attribute in self.plugins[plugin["name"]].__dict__.keys():
                if callable(self.plugins[plugin["name"]].__dict__[attribute]):
                    self.__dict__[attribute] = types.MethodType(self.plugins[plugin["name"]].__dict__[attribute],self)
    
        if "__init__" in dir(self.plugins[plugin["name"]]):
            self.plugins[plugin["name"]].__init__(self)



    def start_callback_loop(self):
        
        self.value_archive = self.copy_callbacks_values()
        while self.running:
            new_values = self.copy_callbacks_values()
            if self.value_archive != new_values:
                edited_values = []
                for key in self.value_archive.keys():
                    if self.value_archive[key] != new_values[key] and key not in edited_values:
                        edited_values.append(key)
                callbacks_to_do = self.callbacks[:]
                #for callback in callbacks_to_do:
                while len(callbacks_to_do) > 0:
                    callback = callbacks_to_do.pop(0)
                    if callback["variable"] in edited_values:
                        if self.debug_callback:
                            print("I am func",callback["function"],"and the variable",callback["variable"],"went from",self.value_archive[callback["variable"]],"to",self.__dict__[callback["variable"]])
                        before = True
                        after = False

                        while before != after:
                            before = self.copy_callbacks_values()[callback["variable"]]
                            self.execute_function(callback)
                            after = self.copy_callbacks_values()[callback["variable"]]
                            if self.debug_callback:
                                print(" - iterate",before,"to",after)
                        
                        new_values = self.copy_callbacks_values()
                        for key in self.value_archive.keys():
                            if self.value_archive[key] != new_values[key] and key not in edited_values:
                                edited_values.append(key)
                                for potential_new_callback in self.callbacks:
                                    if potential_new_callback["variable"] == key and potential_new_callback not in callbacks_to_do:
                                        if self.debug_callback:
                                            print("Since",key,"has been edited",callback["function"],"will be called eventually")
                                        callbacks_to_do.append(potential_new_callback)

                    
                        if self.debug_callback:
                            print(" - and now it is",self.__dict__[callback["variable"]])

            else:
                if self.to_add_callbacks != []:
                    self.callbacks.extend(self.to_add_callbacks)
                    self.to_add_callbacks = []
            self.value_archive = self.copy_callbacks_values()
            time.sleep(0.1)

    def subscribe_to_variable(self, variable_name, plugin_name, function_name, thread=False, args=[],rargs=[], kwargs={}):
        callback = {"variable": variable_name, "plugin": plugin_name, "function":function_name, "thread":thread, "args":args, "rargs":rargs, "kwargs":kwargs}
        if not self.running:
            self.to_add_callbacks = []
        if callback not in self.callbacks:
            self.to_add_callbacks.append(callback) #makes addition differed to when 
        if not self.running:
            self.running = True
            self.callback_loop = threading.Thread(target=self.start_callback_loop, daemon=True)
            self.callback_loop.start()
    

    def unsubscribe_to_variable(self, variable_name, plugin_name, function_name):
        for index, callback in enumerate(self.callbacks):
            if callback["variable"] == variable_name and callback["plugin"] == plugin_name and callback["function"] == function_name:
                self.callbacks.pop(index)


    def execute_function(self,func_dict):
        #func dict must consist of {"plugin":"plugin_name", "function":"function_name","args":["self"],"rargs":[],"kwargs":{}}

        #functions adding standard fields in case they are forgotten
        if not "rargs" in func_dict.keys():
            func_dict["rargs"] = []


        if func_dict["plugin"] == "self":
            scope = self
        elif isinstance(self.plugins[func_dict["plugin"].split('.')[-1]],type):
            scope = self
        else:
            scope = self.plugins[func_dict["plugin"].split('.')[-1]]
        f = getattr(scope, func_dict["function"])
        arguments = []
        
        arguments = [self.__dict__[argument] for argument in func_dict["args"]]
        arguments.extend(func_dict["rargs"])
        try:
            f(*arguments)
        except Exception as e:
            if self.break_on_error:
                raise e
            if self.print_errors:
                print(e)

    def copy_callbacks_values(self):
        archived_callbacks = {}
        for callback in self.callbacks:
            archived_callbacks[callback["variable"]] = self.__dict__[callback["variable"]]
        copy = self.smart_copy(archived_callbacks)
        return copy

    def smart_copy(self,original_object):
        if isinstance(original_object,list):
            return [self.smart_copy(item) for item in original_object]
        elif isinstance(original_object,dict):
            output_dict = {}
            for key in original_object.keys():
                if key != "value_archive":
                    output_dict[key] = self.smart_copy(original_object[key])
            return output_dict
        else:
            return original_object