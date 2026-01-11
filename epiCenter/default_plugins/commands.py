import threading

def __init__(self):
    self.external_methods = []
    self.external_methods.append({"plugin":"commands", "method":self.help, "cmd":"help", "help":"Prints out the help of the specified command, or every command if none is specified"})

def interpret_command(self, query):
    arguments = query.split(" ")[1:]
    for method in self.external_methods:
        if query.split(" ")[0].lower() == method["cmd"].lower():
            local_method = method.copy()
            if "args" not in local_method.keys():
                local_method["args"] = []
            local_method["args"].extend(arguments)
            self.execute_method(local_method)
            return local_method
    return False
        
def execute_startup_commands(self):
    for command in self.startup_commands:
        print(">",command)
        self.interpret_command(command)
        
def help(self,specific_command = False):
    for method in self.external_methods:
        if not specific_command or method["cmd"] == specific_command:
            print(method["plugin"],"->",self.accent_color+method["cmd"]+self.normal_color,":",method["help"])
