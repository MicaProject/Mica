from websockets.sync.server import serve #pip install websockets
from ansi2html import Ansi2HTMLConverter #pip install ansi2html
import json



def __init__(self):
    self.websocket_port = 7800
    self.external_methods.append({"plugin":__name__,"method":self.activate_server,"cmd":"server","help":"Activates the Websocket server","args":[],"dargs":[],"thread":True})
    self.external_methods.append({"plugin":__name__,"method":self.deactivate_server,"cmd":"serverstop","help":"Activates the Websocket server","args":[],"dargs":[],"thread":True})
    pass

def answer_ws_request(self,websocket):
    for message_encoded in websocket:
        try:
            message = json.loads(message_encoded)
            if message["command"] == "get_dict":
                conv = Ansi2HTMLConverter()
                self.html_printout = ""
                #self.html_printout = conv.convert('\n'.join(self.print_buffer[:-2][:]))
                self.html_printout = conv.convert(self.print_buffer[0])

                #removing issue that triggered a runaway multiplication of a specific line
                self.html_printout = self.html_printout.replace(".ansi38-079193255 { color: #4FC1FF; }","TOREPLACE",1)
                self.html_printout = self.html_printout.replace(".ansi38-079193255 { color: #4FC1FF; }\n","")
                self.html_printout = self.html_printout.replace("TOREPLACE",".ansi38-079193255 { color: #4FC1FF; }")
                

                #print(self.html_printout)
                copied_self = self.smart_copy(self.__dict__)
                encoded_self = json.dumps(copied_self)
                websocket.send(encoded_self)
                del conv
            elif message["command"] == "exec_method":
                pass
            elif message["command"] == "interpret_command":
                self.output_text("*> "+message["value"])
                self.text_input.append(message["value"])
                websocket.send(json.dumps("Executed command"))
            else:
                websocket.send(json.dumps("Unknown command"))
        except Exception as e:
            #print(e)
            pass

    

def activate_server(self):
    self.output_text("Websocket server is active, you can access the presentation page for a cleaner experience...")
    with serve(self.answer_ws_request, "localhost", self.websocket_port) as self.websocket_server:
        self.websocket_server.serve_forever()

def deactivate_server(self):
    self.websocket_server.shutdown()