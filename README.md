# Mica
A plugin-based, fully modular python assistant

## About the Project

Mica is a tool that provides a platform for everyone to create its own plugins and make them interact with each other.

While Mica is theoretically cross-platform, it was programmed and tested with Windows, as it is supposed to be a companion for your daily tasks

## Quick Start

Run setup.py to add it to PYTHONPATH, install the required packages from pypi, and create a handy shortcut

for Windows:
```bash
python setup.py
```

Once the setup is complete, simply click on the shortcut, or run it from the command line:
```bash
python -m mica
```

You should end up with a window showing this:
```
 __  __  ___   ____     _
|  \/  ||_ _| / ___|   / \
| |\/| | | | | |      / _ \ The Ghost
| |  | | | | | |___  / ___ \ In the Machine
|_|  |_||___| \____|/_/   \_\
Multi Independent Chatbot for Assistance - unknown branch - Version 5

Loading plugins from default
commands... Done
core... Done
eliza... Done
Plugins loaded successfuly

>
```

## Plugin management

Plugins to be loaded are described as follow in epicenter_config.json:
```json
{
    "plugins_to_start": [

        ...

        {"path":"path to plugin",
        "name":"plugin name"},

        ...
    ]
}
```

The path to the plugin is either the absolute path or the path relative from mica.py

the plugin name is the plugin file name without the .py

The specified file will directly be loaded as a plugin, if you want to load a specific class as a plugin, register it as follows:
```json
{
    "plugins_to_start": [

        ...

        {"path":"path to plugin",
        "name":"plugin name",
        "class":"class name"},

        ...
    ]
}
```

## Plugins logic

For Mica, plugins work by registering more methods and variables to the Mica instance, this makes the code beginner friendly.

This also allows plugins to take advantage of methods and variables created/edited by other plugins, as everything is placed in the same Mica instance

For example, plugin A sets the variable color_of_banana:
```python
#In plugin A
def set_banana_color(self):
    self.color_of_banana = "yellow"
```

Plugin B will be able to manipulate color_of_banana:
```python
#In plugin B
def manipulate_banana_color(self):
    print(self.color_of_banana)
    self.color_of_banana = "blue"
    print(self.color_of_banana)
```

Essentially, every method and variable will operate as if they were from the same class

This allows everyone to come up with their own plugins and integrate them easily with others, this comes especially handy when some plugins act as enablers or others

## Create your own plugins

Plugins have a very lightweight architecture, allowing them to be created quickly, and even to "pluginise" existing scripts

plugins/eliza.py is a good example of a "pluginised" script, as it is untouched code apart from 4 methods added to connect it to Mica

Simply create python methods with the first argument being the reference to the Mica instance (i.e. self) so they can be called by other plugins
```python
#this is the very start of the file, no underlying class
import foo
import bar

def set_banana_color(self,new_color):
    self.color_of_banana = new_color
    #code here is callable by any other plugins simply by using self.my_callable_method(new_color)
```

If you want to run code at plugin import, simply create an init method like so:
```python
#this is the very start of the file, no underlying class
import foo
import bar

def __init__(self):
    #code here will be run at plugin import
```
This is especially useful if you want to register methods as commands, add a method as a callback to a value change through the internal event loop, or simply execute logic depending on pre-existing instance data

methods not having "self" as first argument will be callable, but not by other plugins unless they manually import them