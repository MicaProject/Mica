from github import Github #pip install PyGithub
import pygit2 #pip install pygit2
import os, sys
import shutil
import json


def __init__(self):
    self.community_plugins_path = "community_plugins"
    self.required_plugins_filename = "required-plugins.txt"
    self.found_repositories = []
    if not os.path.exists(self.community_plugins_path):
        os.makedirs(self.community_plugins_path)
    self.external_methods.append({"plugin":__name__,"method":self.refresh_available_plugins,"cmd":"refresh-plugins","help":"Fetches all available plugins from github.com","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.add_plugin,"cmd":"plugin-add","help":"Pulls and activates a plugin, needs a valid plugin clone url as argument","args":[],"dargs":[]})
    self.external_methods.append({"plugin":__name__,"method":self.remove_plugin,"cmd":"plugin-remove","help":"Deletes a downloaded plugin, takes a plugin name as argument","args":[],"dargs":[]})
    
def refresh_available_plugins(self):
    
    try:
        g = Github()
        repositories = g.search_repositories(query='topic:mica-assistant-plugin',sort='stars')
    except Exception as e:
        self.output_text(f"Cant fetch plugins from Github ({e})")
        return
    self.output_text("Indexing available plugins...")
    for repo in repositories:
        self.found_repositories.append(repo)
    self.output_text("Indexed "+str(len(self.found_repositories))+" repositories sucessfuly")
    g.close()

# -- plugin file management --

def clone_plugin(self, plugin_clone_url):
    name = plugin_clone_url.split('/')[-1].replace('.git','')
    path = os.path.join(self.community_plugins_path, name)
    if os.path.exists(path):
        self.output_text("Plugin already exists, please delete it to refresh it")
        return path
    pygit2.clone_repository(plugin_clone_url, path)
    self.output_text(f"Plugin {name} cloned to {path}")
    return path

def delete_plugin(self, plugin_name):
    path = os.path.join(self.community_plugins_path, plugin_name)
    shutil.rmtree(path)
    self.output_text(f"Plugin {plugin_name} removed from {path}")

# -- plugin config management --

def add_plugin_to_config(self, plugin_clone_url):
    name = plugin_clone_url.split('/')[-1].replace('.git','')
    path = os.path.join(self.community_plugins_path, name)
    with open(self.config_path,"r") as f:
        full_config = json.load(f)
    full_config["loaded_plugins"].append({'path':path,'name':name})
    with open(self.config_path,"w") as f:
        json.dump(full_config,f,indent=4)
    self.output_text(f"Plugin {name} added to config {self.config_path}")
    
def remove_plugin_from_config(self, plugin_name):
    with open(self.config_path,"r") as f:
        full_config = json.load(f)
    for i, plugin in enumerate(full_config["loaded_plugins"]):
        if plugin["name"] == plugin_name:
            full_config["loaded_plugins"].pop(i)
            break
    with open(self.config_path,"w") as f:
        json.dump(full_config,f,indent=4)
    self.output_text(f"Plugin {plugin_name} removed from config {self.config_path}")

# -- High level methods

def add_plugin(self, plugin_clone_url):
    self.refresh_available_plugins()
    plugin_path = self.clone_plugin(plugin_clone_url)
    if os.path.exists(os.path.join(plugin_path,self.required_plugins_filename)):
        with open(os.path.join(plugin_path,self.required_plugins_filename),"r") as f:
            required_plugins = f.readlines()
        for required_plugin in required_plugins:
            found = False
            for repo in self.found_repositories:
                if repo.name == required_plugin:
                    found = True
                    self.output_text(f"{plugin_path}: getting required plugin {required_plugin}")
                    self.add_plugin(repo.clone_url)
            if not found:
                self.output_text(f"{plugin_path}: plugin {required_plugin} not found !")
    self.add_plugin_to_config(plugin_clone_url)
    
    name = plugin_clone_url.split('/')[-1].replace('.git','')
    path = os.path.join(self.community_plugins_path, name)
    self.output_text(self.accent_color+name+self.normal_color+"... ",end = "", flush = True)
    self.install_missing_packages(path)
    self.load_plugin({'path':path,'name':name})
    self.output_text("Done")

def remove_plugin(self, plugin_name):
    #plugin_name can be clone url
    if plugin_name.endswith(".git"):
        plugin_name = plugin_name.split('/')[-1].replace('.git','')
    self.remove_plugin_from_config(plugin_name)
    self.delete_plugin(plugin_name)
    self.output_text(f"Plugin {plugin_name} removed, please restart me to apply changes")
    
