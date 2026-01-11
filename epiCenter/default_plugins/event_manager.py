import time
import threading
import os, sys
import json

def __init__(self):
    self.debug_callback = False
    self.callbacks = []
    self.to_add_callbacks = []
    self.callbacks_active = False

def start_callback_loop(self):
    
    self.value_archive = self.copy_callbacks_values()
    while self.callbacks_active:
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
                        print("I am func",callback["method"],"and the variable",callback["variable"],"went from",self.value_archive[callback["variable"]],"to",self.__dict__[callback["variable"]])
                    before = True
                    after = False
                    while before != after:
                        before = self.copy_callbacks_values()[callback["variable"]]
                        self.execute_method(callback)
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
                                        print("Since",key,"has been edited",callback["method"],"will be called eventually")
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
    callback = {"variable": variable_name, "plugin": plugin_name, "method":function_name, "thread":thread, "args":args, "dargs":rargs, "kwargs":kwargs}
    if not self.callbacks_active:
        self.to_add_callbacks = []
    if callback not in self.callbacks:
        self.to_add_callbacks.append(callback) #makes addition differed to when 
    if not self.callbacks_active:
        self.callbacks_active = True
        self.callback_loop = threading.Thread(target=self.start_callback_loop, daemon=True)
        self.callback_loop.start()

def unsubscribe_to_variable(self, variable_name, plugin_name, function_name):
    for index, callback in enumerate(self.callbacks):
        if callback["variable"] == variable_name and callback["plugin"] == plugin_name and callback["method"] == function_name:
            self.callbacks.pop(index)

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
        try:
            json.dumps(original_object)
            return original_object
        except:
            return "Object not serializable"
        
