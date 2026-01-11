from re import search
import webbrowser
import geocoder #pip install geocoder
import geopy #pip install geopy
from youtubesearchpython import VideosSearch #pip install youtube-search-python
from ytmusicapi import YTMusic #pip install ytmusicapi
import sys, os
import os, sys

from meteofrance_api import MeteoFranceClient #pip install meteofrance-api
def txtToURL(textToSearch):
    videosSearch = VideosSearch(textToSearch, limit = 2)
    out = videosSearch.result()
    out1 = out.get('result')
    out2 = out1[0]
    out3 = out2.get('link')
    return out3

def get_coords():
    g = geocoder.ip('me')
    return g.latlng

def get_pos_info(coords):
    lat = coords[0]
    lon = coords[1]
    
    geo_locator = geopy.Nominatim(user_agent='1234')
    r = geo_locator.reverse((lat, lon))
    return r.raw


def __init__(self):
    self.allow_open = True
    self.coords_placeholder = False#if not false, must be a list of the two coords !!!
    self.browser = False
    self.browser_keyword_list = []
    #self.manager.create_shared_var('browser_keyword_list')
    self.browser_keywords = {
        'Youtube':["youtube"],
        'Youtube Music':["youtube-music","yt-music","ytmusic","music"],
        'Google':["google"],
        'Google Maps':["googlemaps","gmaps","google maps","gm","maps"],
        'Qwant Maps':["qm","qwantmaps","qmaps"],
        'Meteo France':['meteo'],
        "Wikipedia": ["wikipedia", "wiki"]
    }
    temprorary = []
    self.external_methods.append({"plugin":__name__,"method":"open_page","cmd":"web","help":"Opens the given url with the default browser","args":[],"dargs":[]})
    for key in self.browser_keywords:
        for keyword in self.browser_keywords[key]:
            self.external_methods.append({"plugin":__name__,"method":self.auto_engine,"cmd":keyword,"help":"Opens the query with "+key,"args":[keyword],"dargs":[]})

def open_page(self,url,*args,incognito = False):
    url = url+" "+" ".join(args)
    if self.plugin_print:
        print('Opening page:',url)
    if self.allow_open:
        
        webbrowser.open(url,2)
    self.output_url = url

def youtube_search(self,searchQuery):
    refinedQuery = searchQuery.replace(' ','+')
    url = "https://www.youtube.com/results?search_query="+refinedQuery
    self.open_page(url)
    
def youtube_music(self,searchQuery):
    if self.plugin_print:
        print("SearchQuery",searchQuery)
    if searchQuery == '':
        url = 'https://music.youtube.com'
    else:
        ytmusic = YTMusic()
        result_list = ytmusic.search(searchQuery,'songs')
        id = ""
        #print(result_list)
        for result in result_list:
            if self.plugin_print:
                print(result)
            if result["category"] == 'Songs' or result["category"] == 'Single' or result["category"] == 'Videos':
                id = result["videoId"]
                break
        url = "https://music.youtube.com/watch?v="+id
    
    self.open_page(url)

def youtube(self,searchQuery):
    if searchQuery == '':
        url = 'https://www.youtube.com'
    else:
        url = txtToURL(searchQuery)
    self.open_page(url)

def wikipedia(self,searchQuery):
    url = "https://wikipedia.org/w/index.php?search="+searchQuery.replace(' ','+')
    self.open_page(url)
    
def googleMaps(self,mainQuery,startQuery = False):
    '''MainQuery is the place to search or destination
    startQuery is the place to start from (optional)
    is startQuery ="me", it will use own postion (GPS or geoloc)'''
    refinedQuery = mainQuery.replace(' ','+')
    if startQuery == False:#Looking for a place
        url = "https://www.google.fr/maps/search/"+refinedQuery+'/'
    else:
        if startQuery == "me":
            if self.coords_placeholder != False:
                coords = self.coords_placeholder
            else:
                coords = get_coords()
            url = "https://www.google.fr/maps/dir/"+str(coords[0])+','+str(coords[1])+'/'+refinedQuery+'/'
        else:#from startQuery to mainQuery
            refinedStartQuery = startQuery.replace(' ','+')
            url = "https://www.google.fr/maps/dir/"+refinedStartQuery+'/'+refinedQuery+'/'
    self.open_page(url)
    
def googleSearch(self,mainQuery):
    '''MainQuery is the place to search or destination
    startQuery is the place to start from (optional)
    is startQuery ="me", it will use own postion (GPS or geoloc)
    https://www.google.com/search?client=firefox-b-d&q=carrier+command+2'''
    refinedQuery = mainQuery.replace(' ','+')
    
    url = "https://www.google.com/search?client=firefox-b-d&q="+refinedQuery
    
    self.open_page(url)

def qwantMaps(self,mainQuery,startQuery = False):
    '''MainQuery is the place to search or destination
    startQuery is the place to start from (optional)
    is startQuery ="me", it will use own postion (GPS or geoloc)'''
    refinedQuery = mainQuery.replace(' ','+')
    if startQuery == False:#Looking for a place
        url = "https://www.qwant.com/maps/?q="+refinedQuery+'/'
    

    self.open_page(url)

    
def meteoFrance(self,query = False):#for now only local search
    
    query = False
    if query != False:
        client = MeteoFranceClient()
        place = client.search_places(query)
        if self.plugin_print:
            print(place)
    else:
        coords = get_coords()
        pos = get_pos_info(coords)
        #print(pos)
        city = pos['address']["municipality"].lower()
        code = pos['address']['postcode']
        #print(city,code)
        url = "https://meteofrance.com/previsions-meteo-france/"+city+'/'+code
        self.open_page(url)
        
    
def auto_engine(self,browser,query):#includes the name of the engine
    if browser in self.browser_keywords['Wikipedia']:
        self.wikipedia(query)
        self.output_text("Displaying results for "+query)
    if browser in self.browser_keywords['Youtube']:
        self.youtube(query)
        self.output_text("Displaying results for "+query)
    if browser in self.browser_keywords['Youtube Music']:
        self.youtube_music(query)
        self.output_text("Starting "+query+" on youtube music")
    if browser in self.browser_keywords["Google"]:
        self.googleSearch(query)
        self.output_text("Searching "+query+" on google")
    elif browser.lower() in self.browser_keywords['Google Maps']:
        if ' to ' in query:
            querys = query.split(' to ')
            self.googleMaps(querys[1],querys[0])
            self.output_text("Going from "+querys[0]+" to "+querys[1])
        else:
            if self.plugin_print:
                print("Query:", query)
            self.googleMaps(query)
            self.output_text("Displaying "+query)
    elif browser.lower() in self.browser_keywords['Qwant Maps']:
        self.qwantMaps(query)
        self.output_text("Displaying "+query)

    elif browser.lower() in self.browser_keywords['Meteo France']:
        self.meteoFrance()
        self.output_text("Displaying meteo")
    else:
        self.output_text("No able browser found in query")

def return_link(self,completeQuery,replace_coords = False):
    self.allow_open = False
    self.coords_placeholder = replace_coords
    completeQueryList = completeQuery.split(' ')
    browser = completeQueryList[0]
    query = ' '.join(completeQueryList[1:])
    if browser in self.browser_keywords['Youtube']:
        self.youtube(query)
        
    elif browser in self.browser_keywords['Youtube Music']:
        self.youtube_music(query)
    
    elif browser.lower() in self.browser_keywords['Google Maps']:
        if ' to ' in query:
            querys = query.split(' to ')
            self.googleMaps(querys[1],querys[0])
            
        else:
            self.googleMaps(query)

    elif browser.lower() in self.browser_keywords['Meteo France']:
        self.meteoFrance()
    else:
        self.output_url = "ERROR"
    #resetting the values for later use
    self.allow_open = True
    self.coords_placeholder = False
    return self.output_url
    