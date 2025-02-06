import os, sys
import time
from utils import *

def __init__(self):
    self.command_manifest = []
    self.cmd_prefixes = ['!','.',':']
    self.subscribe_to_variable("text_input", "commands", "interpret_command", thread=False, args=["self"], kwargs={}, rargs = [])
    #commands related
    self.command_manifest.append({"plugin":__name__,"function":"print_help","command":"help","help":"Prints the help for each available command","args":["self"],"rargs":[]})
    self.command_manifest.append({"plugin":__name__,"function":"print_plugins","command":"plugins","help":"Prints the active plugins","args":["self"],"rargs":[]})
    self.command_manifest.append({"plugin":__name__,"function":"start_plugin","command":"startplugin","help":"Starts the selected plugin","args":["self"],"rargs":[]})
    



def general_ping(self, *args):
    for plugin in self.plugin_names:
        self.internal_commands.append(' '.join([plugin,'ping']))

def print_help(self, *args):
    self.text_output.append("To input commands, place these prefixes: "+str(self.cmd_prefixes)+" like !command")
    grouped_commands = []
    for available_command in self.command_manifest:
        
        for already_existing in grouped_commands:
            if available_command["help"] == already_existing["help"]:
                already_existing["command"] = already_existing["command"]+', '+available_command["command"]
        if not any(available_command["help"] == already_existing["help"] for already_existing in grouped_commands):
            grouped_commands.append(available_command)
    txt_to_print = []
    for available_command in grouped_commands:
        #print("---",available_command["command"])
        txt_to_print.append(available_command["command"]+": "+available_command["help"])
    self.text_output.extend(txt_to_print)

def print_plugins(self, *args):
    self.text_output.append('- '+'\n- '.join(self.plugin_names))

def start_plugin(self,*args):
    self.internal_commands.append('mica start_plugin '+' '.join(args[1:]))

def interpret_command(self,*args):

    for index,text in enumerate(self.text_input):
        word_list = text.split(' ')
        if any(text.startswith(prefix) for prefix in self.cmd_prefixes):
            
            command = word_list[0][1:]
            additional_arguments = []
            if len(text) > 1:
                additional_arguments = word_list[1:]
            for command_manifest in self.command_manifest:
                if command_manifest["command"] == command:
                    self.text_input.pop(index)
                    local_command_manifest = self.smart_copy(command_manifest)
                    local_command_manifest["rargs"].extend(additional_arguments)

                    self.execute_function(local_command_manifest)


