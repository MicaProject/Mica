import os,sys, time
import threading
import epiCenter
import tools.utils as utils

from prompt_toolkit import prompt #pip install prompt_toolkit
from prompt_toolkit.completion import WordCompleter

import builtins
print_buffer = [""]
old_print = builtins.print
def custom_print(*args, **kwargs):
    old_print(*args, **kwargs)

    end = '\n'
    if "end" in kwargs:
        end = kwargs["end"]
    nargs = []
    for arg in args:
        nargs.append(str(arg))
    text = ' '.join(nargs)+end
    print_buffer[0] = print_buffer[0]+text

builtins.print = print = custom_print

#hash 3.12.3
#-6960679630773435528
if sys.platform == "nt":
    os.system("color")

class Mica(epiCenter.PluginManager):
    
    def __init__(self):
        self.running = True
        self.text_output = []
        self.text_input = []
        self.natural_language = []
        self.plugin_print = False
        self.color_start = "\x1b[38;2;79;193;255m"
        self.color_end = "\033[0m"
        self.root_directory = os.path.dirname(__file__)
        self.config_path = "mica_config.json"
        os.chdir(self.root_directory)
        self.security = False
        global print_buffer
        self.print_buffer = print_buffer
        
        os.system("title Mica Assistant")

        utils.banner()

        self.success_color = self.color_start
        self.initialise_command_backend()
        self.initialise_event_backend()
        super().__init__(os.path.join(self.root_directory,self.config_path))

        print('')
        self.running = True
        self.restart = False
        
        input_thread = threading.Thread(target=self.output_loop,daemon=True)
        input_thread.start()
        print("Running startup commands...")
        if "startup_commands" in self.config:
            for command in self.config["startup_commands"]:
                print('>',command)
                self.interpret_text(command)
        
        self.subscribe_to_variable("text_input","self",self.interpret_text,args=[])
        time.sleep(0.1)
        input_thread = threading.Thread(target=self.input_loop,daemon=True)
        input_thread.start()
        
        while self.running:
            try:
                if len(self.text_input) > 0:
                    self.interpret_text(self.text_input.pop())
                time.sleep(0.1)
            except KeyboardInterrupt:
                self.running = False
                print("Bye Bye...")
                break

    def input_loop(self):
        while self.running:
            try:
                completer = WordCompleter([command["cmd"] for command in self.external_methods])
                input_text = prompt("> ",completer=completer,in_thread=True)
            except:
                input_text = input('> ')
            if input_text != "":
                self.text_input.append(input_text)
                #self.interpret_text()
            else:
                pass
                self.output_text("",end="",flush = True)

    def output_loop(self,*args):
        while self.running: 
            if len(self.text_output) > 0:
                self.output_text(self.text_output.pop())
            time.sleep(0.1)

    def output_text(self,*text_to_print,**kwargs):
        if "flush" in kwargs:
            kwargs.pop("flush")
        print("\r",end = '')
        print(*text_to_print,**kwargs,flush=True)
        #print('',end = "", flush=True)

    def interpret_text(self,text_to_interpret=False):
        if text_to_interpret != False:
            text_list = [text_to_interpret]
        if text_to_interpret == False:
            text_list = self.text_input[:]
            self.text_input = []
        for text_to_interpret in text_list:
            answer = self.interpret_command(text_to_interpret)
            if answer == False:
                self.interpret_natural_language(text_to_interpret)
                #self.natural_language.append(text_to_interpret)
            self.output_text("\n> ",end="",flush = True)


if __name__ == "__main__":
    M = Mica()