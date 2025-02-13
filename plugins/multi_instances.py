import os, sys, time
import socket
import threading
import dill as pickle


def __init__(self):
    self.mica_socket_port = 40674
    self.mica_advertising_port = 40675
    self.mica_advertising_magic = "fna349fn"
    self.local_main_socket = socket.socket()
    self.socket_threads = []
    pass

#----------------------- Logic if set as server
def create_server(self):
    self.local_main_socket.bind(('', self.mica_socket_port))
    self.client_sockets = []
    self.server_active = True
    self.socket_threads.append(threading.Thread(target=self.wait_for_client_loop,daemon=True))
    self.socket_threads[-1].start()
    self.socket_threads.append(threading.Thread(target=self.advertise_server,daemon=True))
    self.socket_threads[-1].start()


def wait_for_clients_loop(self):
    while self.running and self.server_active:
        client_socket, client_addr = self.local_main_socket.accept()

        #here maybe add security layer ?
        client_info = {"socket":client_socket,"address":client_addr}
        self.client_sockets.append(client_info)
        self.socket_threads.append(threading.Thread(target=self.wait_for_remote,daemon=True,args=(client_info,)))
        self.socket_threads[-1].start()

def advertise_server(self):
    
    advertising_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #create UDP socket
    advertising_socket.bind(('', 0))
    advertising_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #this is a broadcast socket
    my_ip= socket.gethostbyname(socket.gethostname()) #get our IP. Be careful if you have multiple network interfaces or IPs
    while self.server_active:
        data = self.mica_advertising_magic+my_ip
        self.sendto(data, ('<broadcast>', self.mica_advertising_port))
        time.sleep(5)

#----------------------- Logic if set as client

def connect_to_server(self, server_ip):
    self.local_main_socket.connect((server_ip,self.mica_socket_port))
    self.server_info = {"socket":self.local_main_socket,"address":(server_ip,self.mica_socket_port)}
    self.socket_threads.append(threading.Thread(target=self.wait_for_remote,daemon=True,args=(self.server_info,)))
    self.socket_threads[-1].start()

#----------------------- Functions for both client and server

def wait_for_remote(self, remote_info, additional_condition = True):
    while self.running and additional_condition:
        try:
            encoded_data = remote_info["socket"].recv(1024)
        except (ConnectionResetError, ConnectionAbortedError, OSError, EOFError):
            self.handle_disconnect(remote_info)
            break
        decoded_data = pickle.loads(encoded_data)
        self.interpret_received_command(self,decoded_data)

def interpret_received_command(self, received_value):
    if received_value["operation"] == "update_value":
        self.__dict__[received_value["varname"]] = received_value["value"]

    elif received_value["operation"] == "exec_function":
        self.execute_function(received_value["func_dict"])

def handle_disconnect(self,disconnected_info):
    if "client_sockets" in self.__dict__ and disconnected_info in self.client_sockets:
        self.client_sockets.pop(self.client_sockets.index(disconnected_info))
    #here goes the logic for the client
