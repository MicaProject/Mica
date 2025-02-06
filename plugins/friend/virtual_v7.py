from tkinter import * #pip install tkinter
#for linux sudo apt-get install python-tk
import time
import os,random, sys
from PIL import Image, ImageTk#sudo apt-get install python3-pil.imagetk #pip install pillow
from sys import platform,argv
from screeninfo import get_monitors#pip install screeninfo
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from utils import *
from threading import Thread

action_idle = {
        "name":"idle",
        "possible_x":[-1,1],
        "possible_y":[0],
        "max_range":0,
        "max_time":30,
        "animation":"Idle",
        "refresh_rate":90
    }
action_walk = {
        "name":"walk",
        "possible_x":[-1,1],
        "possible_y":[-1,1],
        "max_range":500,
        "max_time":20,
        "animation":"Walk",
        "refresh_rate":40
    }
action_sprint = {
        "name":"sprint",
        "possible_x":[-3,3],
        "possible_y":[-3,3],
        "max_range":1000,
        "max_time":10,
        "animation":"Run",
        "refresh_rate":40
    }

def __init__(self):
    self.friend = virtualFriend()
    self.friend_thread = Thread(target=self.friend.go,daemon=True)
    self.friend_thread.start()
    self.command_manifest.append({"plugin":"virtual_v7","function":"stop_friend","command":"chew","help":"Stops the friend running around","args":["self"],"rargs":[]})
    
def stop_friend(self):
    self.friend.run = False

class virtualFriend():
    run = True
    loading = True
    wSize = 80

    def __init__(self,relative_spritepath = "friend_sprites"):

        self.selected_action = {}
        #self.manager.create_shared_var("selected_action")
        self.get_screens()
        directory = os.path.dirname(__file__)
        self.sprite_dir = os.path.join(directory,relative_spritepath)
    def load_images(self,name,orientation):
        list = []
        size = 0
        for filename in os.listdir(self.sprite_dir):
            if filename.endswith('.png') and name in filename:
                if orientation == " (r1)" and 'r1' in filename:
                    size += 1
                elif orientation == '' and 'r1' not in filename:
                    size += 1
                    #print(filename)
        for i in range(1,size+1):
            path = os.path.join(self.sprite_dir,'{}{} ({}).png'.format(name,orientation,i))
            key = filename[:-4]
            raw = Image.open(path)
            list.append(ImageTk.PhotoImage(raw.resize((self.wSize, self.wSize))))

        return list

    def get_screens(self):
        left = 0
        right = 0
        top = 0
        down = 0
        for m in get_monitors():
            if m.x < left:
                left = m.x
            if m.x+m.width > right:
                right = m.x+m.width
            if m.y < top:
                top = m.y
            if m.y+m.height > down and m.is_primary:
                down = m.y+m.height
        self.minRight = left
        self.maxRight = right -self.wSize
        self.minDown = top
        self.maxDown = down -self.wSize
        



    def update(self):
        if self.loading == False:
            try:
                frame = self.frames[self.ind]
                self.ind += 1
                if self.ind >= len(self.frames)-1:
                    self.ind = 0
                if self.loading == False:
                    self.label.configure(image=frame)
            except:
                #print("whoops")
                self.ind = 0
        else:
            pass
            #print("almost changed frame while loading")
        
        self.root.after(self.selected_action["refresh_rate"], self.update)

    def sprint(self,event):
        #invoked to make Mica
        #print("sprintning now !")
        speed_multiplicator = 4
        selected_action_large = action_sprint
        self.loading = True
        self.selected_action = {
            "name":selected_action_large["name"],
            "x":random.choice(selected_action_large["possible_x"]),
            "y":random.choice(selected_action_large["possible_y"]),
            "range_x":random.randint(0,selected_action_large["max_range"]),
            "range_y":random.randint(0,selected_action_large["max_range"]),
            "time":random.randint(5,selected_action_large["max_time"]),
            "animation":selected_action_large["animation"],
            "refresh_rate":round(selected_action_large["refresh_rate"]/speed_multiplicator)
        }
        way = ""
        if self.selected_action["x"]<0:
            way = " (r1)"
        self.frames = self.load_images(self.selected_action["animation"],way)
        self.ind = 0
        self.loading = False
        
    def move(self):
        if self.stop_friend == False or time.time()>=self.stop_friend:
            
            if self.stop_friend == False: #first move
                selected_action_large = action_walk
                self.selected_action = {
                    "name":selected_action_large["name"],
                    "x":-1,
                    "y":-1,
                    "range_x":500,
                    "range_y":500,
                    "time":15,
                    "animation":selected_action_large["animation"],
                    "refresh_rate":selected_action_large["refresh_rate"]
                }
            else:
            
                selected_action_large = random.choice([action_idle,action_walk,action_sprint])
                self.selected_action = {
                    "name":selected_action_large["name"],
                    "x":random.choice(selected_action_large["possible_x"]),
                    "y":random.choice(selected_action_large["possible_y"]),
                    "range_x":random.randint(0,selected_action_large["max_range"]),
                    "range_y":random.randint(0,selected_action_large["max_range"]),
                    "time":random.randint(2,selected_action_large["max_time"]),
                    "animation":selected_action_large["animation"],
                    "refresh_rate":selected_action_large["refresh_rate"]
                }
            
            #print(self.selected_action)
            way = ""
            if self.selected_action["x"]<0:
                way = " (r1)"

            self.loading = True
            self.frames = self.load_images(self.selected_action["animation"],way)
            self.loading = False
            self.base_x = self.window.winfo_x()
            self.base_y = self.window.winfo_y()
            #print(base_x,base_y)
            self.new_x = self.base_x
            self.new_y = self.base_y

            self.stop_friend = time.time()+self.selected_action["time"]
        else:
            if 'run' in self.__dict__ and self.run == False:
                self.root.quit()
            flag_h = True
            flag_v = True
            if abs(self.new_x-self.base_x) < self.selected_action["range_x"]:
                if (self.selected_action["x"] >0 and self.new_x < self.maxRight)or(self.selected_action["x"] < 0 and self.minRight<self.new_x):
                    self.new_x = self.new_x + self.selected_action["x"]
                    flag_h = False

            if abs(self.new_y-self.base_y) < self.selected_action["range_y"]:
                if (self.selected_action["y"] >0 and self.new_y < self.maxDown)or(self.selected_action["y"] < 0 and self.minDown<self.new_y):
                    self.new_y = self.new_y + self.selected_action["y"]
                    flag_v = False


            if flag_h and flag_v and self.selected_action["name"] != "idle":#restart when not moving anymore
                self.stop_friend = time.time()-1
            
            self.window.geometry("+{}+{}".format(self.new_x,self.new_y))
            self.window.update()
        self.root.after(self.selected_action["refresh_rate"], self.move)
                    
    def go(self):
        self.root = Tk()
        self.root.attributes('-alpha', 0.0) #For icon

        self.root.iconify()
        self.root.update()
        self.window = Toplevel(self.root)
        self.window.attributes('-topmost', True)

        self.window.overrideredirect(1) #Remove border
        self.window.geometry("{}x{}".format(self.wSize,self.wSize)) #Whatever size
        self.window.geometry("+{}+{}".format(self.maxRight-500,self.maxDown+self.wSize))
        self.window.bind("<Button-1>",self.sprint)
        self.window.update()
        self.frames = self.load_images("Idle","")
        if platform == "linux" or platform == "linux2":
            self.label = Label(self.window)
            self.root.overrideredirect(True)
            self.root.wait_visibility(self.root)
            self.root.wm_attributes("-alpha", 0.0)
        elif platform == "win32":
            self.label = Label(self.window,bg='#00B6FA')
            self.root.wm_attributes("-disabled", True)
            self.root.wm_attributes("-transparentcolor", "#00B6FA")
            #self.window.wm_attributes("-disabled", True)
            self.window.wm_attributes("-transparentcolor", "#00B6FA")
        
        self.label.pack(fill="both",expand=1)
        
        self.stop_friend =False
        self.ind = 0

        try:
            self.window.after(70, self.move)
            self.window.after(70, self.update)
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Quitting")
            self.root.quit()

if __name__ == "__main__":          
    f = virtualFriend()
    f.go()
