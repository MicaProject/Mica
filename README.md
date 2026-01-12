# Mica - The assistant tailored for you !

```
 __  __  ___   ____     _    
|  \/  ||_ _| / ___|   / \   
| |\/| | | | | |      / _ \ The Ghost
| |  | | | | | |___  / ___ \ In the Machine
|_|  |_||___| \____|/_/   \_\ 
Modular Interdependent Chatbot for Assistance
```
![Say Hi!](tools/mica.ico)

Mica leverages a plugin-based approach so you can integrate your plugins to fit exactly your needs.

It is also shipped with an array of plugins showing the extent of its capabilities.


## Adding/Removing plugins

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

If your plugin relies on another plugin's variables/methods, you can explicitly write the required plugins at the start of the file:
```python
import foo
import bar
required_plugins = ["core", ]
...
```
If the required plugins are not loaded yet, its loading will be delayed until they are.

## Plugins shipped as default
Each of these plugins can be disabled or swapped, so tailor them to your needs !

---
### core
Core makes available several utility methods like restarting mica or getting the origin of a variable created in the main instance, this is espacially useful when debugging

---
### commands
Commands allows each plugin to declare commands that will allow the user to call a specific method from a given command-line interface, it  will also display these commands in a neat manner by typing:
```
> help
```
More info [here](#commands-the-simplest-way-to-interact-with-your-assistant)

---
### nlp_core
This plugin allows users to bind sentence templates to methods. More info [here](#talk-to-your-assistant-)

---
### git_plugin_manager
The simplest way to add plugins made by the community ! More info [here](#share-plugins-with-the-community-)

---
### browser_interface
This plugin allows the user to open the browser with specific queries that facilitate the search of specified music, routes, or weather information. So far it has a connection with Google, Qwant, Google maps, Youtube, Youtube Music, and some public services.

---
## Commands: the simplest way to interact with your assistant
To call a method from the command line, simply bind a command to a method like so:
```python
self.external_methods.append({"plugin":"example_plugin","method":self.example_method,"cmd":"example","help":"prints some example text","args":[],"dargs":[]})
```
It then can be called in the command-line interface:
```
> example
```

## Talk to your assistant !
While command are useful, its often best to just talk to it ! The nlp_core plugin offers the possibility to bind natural language to command with arguments. For example, we can type the sentence "Search Robert Schuman on Google" into self.auto_engine("google", "Robert Schuman"). The underlying algorithm allows for much more complex natural language processing.

### Binding your method to natuaral language templates
in plugins/nlp, the file core_templates.json is the link between natural language and method, for example:
```json
{
    ...
    "auto_engine": [
        "Open {browser} and search {*query}",
        "On {browser} search {*query}",
        "with {browser} search/open {*query}",
        "open/search/play {*query} on/with {browser}"
    ],
    ...
}
```
This template will ensure that any fitting sentence will trigger the method auto_engine with the arguments browser and query

if an argument starts with *, it means it can be composed of several words, this separation is useful if several arguments are next to each other

When two words are separated by a /, nlp_core will generate every possible variant at runtime. this allows to create many variations in relatively few lines.
For example, the template
```json
{
    ...
    "auto_engine": [
        "open/search/play {*query} on/with {browser}"
    ],
    ...
}
```
will generate all these variants:
```
open {*query} on {browser}
search {*query} on {browser}
play {*query} on {browser}
open {*query} with {browser}
search {*query} with {browser}
play {*query} with {browser}
```
### Adding/removing templates at runtime
If you realise that this method could be easily started with a template, no need to restart Mica to add it, simply type:
```
> Append {*template_to_add} to {method_to_add}
```
and it will be made immediately available to you (it will also update the appropriate json file) !

Same if you find one template does not fit well while using it, you can type:
```
> Remove {*template_to_remove} from {linked_method}
```

both are also templates, so you can add/remove syntax for these as well !

### Using specific template files
When you create your own plugins, you might want to use this feature, in order to add templates that would be callable only when your plugin is active, you can create a separate template file calling your methods. To register this new file in nlp_core, call this method in your plugin:
```python
self.load_template_file("path/to/the/template_file.json")
```
This has to be done after the nlp_core plugin is loaded

## Get plugins made by the community !
On [this page](https://github.com/search?q=mica-assistant-plugin+in%253Atopics) you can find all the plugins people made

If you want to try one, simply type in your assistant:
```
add plugin Creator/PluginName
```
for example, you can install the plugin calculator by calling:
```
add plugin Oddball74/calculator
```
and the plugin will automatically be downloaded and launched !

If you want to remove it, simply type in your assistant:
```
remove plugin PluginName
```
and restart your assistant to apply the changes !

## Share plugins with the community !
You like your plugin and thinks others could use it ?

Simply create a public github repository named the same as the plugin, and place your code in the root of the repo, once it is uploaded, add the tag:
```
mica-assistant-plugin
```
and voila, everyone can install your creation by typing
```
add plugin YourName/YourPlugin
```

If your plugin needs additional plugins to be downloaded, you can create a file named "required-plugins.txt"
and write one plugin to be downloaded per line like YourName/YourPlugin
They will all be installed first, and their required plugins will also be installed

