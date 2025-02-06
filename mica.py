import os,sys, time
import threading
import epiCenter
import utils
#hash 3.12.3
#-6960679630773435528
if sys.platform == "nt":
    os.system("color")

class Mica(epiCenter.epiCenter):
    
    def __init__(self):
        self.text_output = []
        self.text_input = []
        self.plugin_print = False
        self.color_start = "\x1b[38;2;79;193;255m"
        self.color_end = "\033[0m"
        self.root_directory = os.path.dirname(__file__)
        self.security = False
        
        os.system("title Mica Assistant")

        utils.banner()

        self.success_color = self.color_start
        super().__init__("mica_config.json")

        print('')
        self.running = True
        self.restart = False
        self.subscribe_to_variable("text_output","self","print_text",args=["self"])
        input_thread = threading.Thread(target=self.input_loop,daemon=True)
        input_thread.start()
        time.sleep(0.1)
        self.print_text(self)
        
        while self.running:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.running = False
                print("Bye Bye...")
                break

                

    def input_loop(self):
        while self.running:         
            input_text = input("> ")
            self.text_input.append(input_text)

    def print_text(self,*args):
        if len(self.text_output) > 0:
            print("\r",end = '')
            print(self.text_output.pop(0),flush=True)
            if len(self.text_output) == 0:
                print("\n> ", end = '',flush=True)
        
            


if __name__ == "__main__":
    M = Mica()