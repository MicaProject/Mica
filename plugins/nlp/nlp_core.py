import json
import os, sys

#rules and possibilities of the nlp templates
# A template file is always a Json dictionary with the function to call as key, and a list of expressions that can call it
# In the expressions, one can use [i] to set an argument at position i (starting 0)
# In the expression one can use {keyword} to set a keyword argument
# In args or kwargs, specifying * (like [*0] or {*query}) tells the parser that it might be multiple words, it is forbidden to put two not separated by an anchor word
# If two words in an expression are separated by / (like on/with) the nlp will understand a sentence with either these words, this is to reduce the amount of added lines


def __init__(self):
    self.template_files = {}
    self.natural_language_history = []
    self.external_methods.append({"plugin":__name__,"method":self.print_templates,"cmd":"nlphelp","help":"Prints what expression can be said with the loaded nlp templates","args":[],"dargs":[]})
    self.standard_template_file = "plugins/nlp/core_templates.json"
    self.load_template_file(self.standard_template_file)
    #self.get_arguments_from_template("on google search le petit prince","On [0] search [1]")
    pass

def get_permutations(self, template_text):
    existing_p = []#existing permutations
    word_list = template_text.split(' ')
    for word in word_list:
        if '/' in word:
            pre_existing_p = existing_p[:]
            existing_p = []
            sub_perm = word.split('/')
            if pre_existing_p == []:
                for sub in sub_perm:
                    existing_p.append(sub)
            else:
                for sub in sub_perm:
                    sublist = pre_existing_p[:]
                    new_sublist = []
                    for element in sublist:
                        new_sublist.append(element+' '+sub)
                    existing_p += new_sublist
        else:
            if existing_p == []:
                existing_p.append(word)
            else:
                for i,element in enumerate(existing_p):
                    existing_p[i] =  element+' '+word
    temp_p = []
    for permutation in existing_p:
        temp_p.append(permutation.replace('  ',' '))
    existing_p = temp_p
    return existing_p
                    
def load_template_file(self, path):
    with open(path,"r",encoding="utf-8") as f:
        self.template_files[os.path.abspath(path)] = json.load(f)
    self.parse_templates()

def store_template_file(self,path):
    json_to_save = self.template_files[os.path.abspath(path)]
    
    with open(path,"w",encoding="utf-8") as f:
        json.dump(json_to_save,f,indent=4)

def parse_templates(self):
    self.templates = {}
    for file in self.template_files.keys():
        for method in self.template_files[file].keys():
            for expression_mux in self.template_files[file][method]:
                for expression in self.get_permutations(expression_mux):
                    self.templates[expression] = {"expression":expression, "method":method, "file":file}
    return self.templates

def print_templates(self):
    for file in self.template_files.keys():
        self.output_text(f'In {file}:')
        for method in self.template_files[file].keys():
            self.output_text(f'Method "{self.accent_color}{method}{self.normal_color}" is triggered by expressions:')
            for expression in self.template_files[file][method]:
                for parsed_expression in self.get_permutations(expression):
                    self.output_text(f' - {parsed_expression}')

def get_arguments_from_template(self,text,template):
    #example text will be Search Dua lipa on youtube
    #expected template is "Search [1] on [0]"
    text_list = text.lower().split(' ')
    template_list = template.lower().split(' ')
    anchors = []#list of tuple with (anchor, pos_in_text, pos_in_template)
    current_pos_in_text = 0
    if template == 'remove the plugin named {plugin_name}':
        pass
    for i,word in enumerate(template_list):
        if not word.startswith('[') and not word.startswith('{'):
            if word not in text_list[current_pos_in_text:]:
                return False
            current_pos_in_text = text_list.index(word,current_pos_in_text)
           
            anchors.append((word,current_pos_in_text,i))
    # Turn these tuples into hole-text couples
    couples = [] #tuple with (text, hole(can be several))
    if anchors[0][1]!=0 and anchor[0][2]!=0:
        couples.append((text_list[:anchor[0][1]],template_list[:anchor[0][2]]))
    elif anchors[0][1]==0 and anchors[0][2]!=0:
        return False
    elif anchors[0][1]!=0 and anchors[0][2]==0:
        return False
    for i,anchor in enumerate(anchors):
        if i<len(anchors)-1:
            couples.append((text_list[anchors[i][1]+1:anchors[i+1][1]],template_list[anchors[i][2]+1:anchors[i+1][2]]))
    if anchors[-1][1]<len(text_list)-1 and anchors[-1][2]<len(template_list)-1:
        couples.append((text_list[anchors[-1][1]+1:],template_list[anchors[-1][2]+1:]))

    #finally we connect text to the args/kwargs
    i = 0
    for element in template_list:
        if element.startswith('['):
            i +=1
    args = [None]*i
    kwargs = {}
    for couple in couples:
        couple_c = list(couple)[:]
        block_l = False
        block_r = False
        while True:
            # we will take one left and one right each loop, as long as we dont fall on the wildcard *
            if len(couple_c[1])==0:
                break
            if '*' not in couple_c[1][0]:
                interesting_pair = (couple_c[0].pop(0),couple_c[1].pop(0))
                if interesting_pair[1].startswith('['):
                    args[int(interesting_pair[1][1:-1])] = interesting_pair[0]
                elif interesting_pair[1].startswith('{'):
                    kwargs[interesting_pair[1][1:-1]] = interesting_pair[0]
            else:
                block_l = True
            if len(couple_c[1])==0:
                break
            if '*' not in couple_c[1][-1]:
                interesting_pair = (couple_c[0].pop(-1),couple_c[1].pop(-1))
                if interesting_pair[1].startswith('['):
                    args[int(interesting_pair[1][1:-1])] = interesting_pair[0]
                elif interesting_pair[1].startswith('{'):
                    kwargs[interesting_pair[1][1:-1]] = interesting_pair[0]
            else:
                block_r = True
            if block_l and block_r: #probably they arrived at the same conclusion, whatever is left is the wildcard
                if len(couple_c[1]) > 1:
                    return False #we could even raise an error here
                if couple_c[1][0].startswith('['):
                    args[int(couple_c[1][0][2:-1])] = ' '.join(couple_c[0])
                elif couple_c[1][0].startswith('{'):
                    kwargs[couple_c[1][0][2:-1]] = ' '.join(couple_c[0])
                break
    
    #Last check, ensuring there are no words in the template that could have been ignored by the first phase, and that are not part of the args and kwargs

    for word in text_list:
        if word.lower() not in template_list + args + ' '.join(list(kwargs.values())).split(' '):
            return False

    return (args, kwargs)


def interpret_natural_language(self,input_text):
    #this function should be fine tuned in the future
    possible_templates = self.parse_templates()
    for template in possible_templates.keys():
        output = self.get_arguments_from_template(input_text,template)
        if output != False:
            
            args, kwargs = output
            method = getattr(self, possible_templates[template]["method"])
            self.output_text("Executing "+'"'+possible_templates[template]["method"]+'"'+" from template "+template)
            self.execute_method({"method":method, "args": args, "kwargs":kwargs})
            self.natural_language_history.append(possible_templates[template])
            
            return
    self.output_text('I didnt get it, perhaps you could ask, "What can I say ?"')
    pass
    
def add_template_to(self,template_to_add,method_to_add):
    #will check if this template already has a list in a config file, otherwise will add it in the default path
    found = False
    
    for file in self.template_files.keys():
        if method_to_add in self.template_files[file].keys():
            self.template_files[file][method_to_add].append(template_to_add)
            file_to_reload = file
            found = True
            break
    if not found:
        self.template_files[os.path.abspath(self.standard_template_file)][method_to_add] = [template_to_add]
        file_to_reload = os.path.abspath(self.standard_template_file)
    self.store_template_file(file_to_reload)
    self.parse_templates()
    self.output_text("Added new expression !")

def remove_template_from(self, template_to_remove, linked_method):
    for file in self.template_files.keys():
        if linked_method in self.template_files[file].keys():
            if template_to_remove in self.template_files[file][linked_method]:
                self.template_files[file][linked_method].pop(self.template_files[file][linked_method].index(template_to_remove))
                self.store_template_file(file)
                self.parse_templates()
                self.output_text('Removed expression "'+template_to_remove+'"')
                return
    self.output_text('Couldnt remove expression, perhaps it was badly formulated ?')

    