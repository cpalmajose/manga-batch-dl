try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser
    
import re

CHAPTER = "chapterlist"
IMAGE = "imgholder"

def nextpage(prev):
    ''' Determines the next page of the the chapter'''
    oldpattern = re.compile(r'(/[\d]+-[\d]+-)([\d]+)(.+)')
    newpattern = re.compile(r'(.+)/([\d]+)$')
    r = oldpattern.search(prev)
    if r:
        
        return r.group(1) + str(int(r.group(2)) + 1) + r.group(3)
    else:
        r = newpattern.search(prev)
        t = prev.split("/")
        if not r:
            raise Exception("Error with prev link")
        elif(len(t)) == 3:
            return prev + "/2"
          
        return r.group(1) + "/" + str(int(r.group(2)) + 1)    
            

class MangaReaderChapter(HTMLParser):
    
    # initializer : (dcname : class name of chapter list) (content : html feed)
    def __init__(self, idname):
        HTMLParser.__init__(self)
        self.inDiv = False      # check if inside div class for chapter links
        self.idname = idname    # the div class name 
        self.links = []
        self.divlvl = 0
        
    # handle Start tags
    def handle_starttag(self, tag, attrs):
        #get chapter page url.
        if tag == 'a' and self.inDiv == True:
            for attr in attrs:
                #print("attr: " + attr)
                if attr[0] == 'href':
                    self.links.append(attr[1])
                    
        #if in div tag and correct lass name
        if tag == 'div':
            if self.divlvl > 0:
                self.divlvl = self.divlvl + 1
            for attr in attrs:
                #print(tag + ": attr - " + str(attr))
                if attr[0] == 'id' and attr[1] == self.idname:
                    self.divlvl = self.divlvl + 1
                    self.inDiv = True
                            
    #handle end_tags
    def handle_endtag(self, tag):
        if tag == 'div' and self.inDiv == True:
            self.divlvl = self.divlvl - 1
            if self.divlvl == 0:
                self.inDiv = False

class MangaReaderImage(HTMLParser):
    
    # initializer : (dcname : class name of chapter list) (content : html feed)
    def __init__(self, idname):
        HTMLParser.__init__(self)
        self.idname = idname    # the div class name 
        self.inDiv = False 
        self.divlvl = 0
        self.imglink = ""
        
    # handle Start tags
    def handle_starttag(self, tag, attrs):
        #get chapter page url.
        if tag == 'img' and self.inDiv == True:
            for attr in attrs:
                if attr[0] == 'src':
                    self.imglink = attr[1]
                    break
                    
        #if in div tag and correct lass name
        if tag == 'div':
            if self.divlvl > 0:
                self.divlvl = self.divlvl + 1
            for attr in attrs:
                #print(tag + ": attr - " + str(attr))
                if attr[0] == 'id' and attr[1] == self.idname:
                    self.divlvl = self.divlvl + 1
                    self.inDiv = True
                            
    #handle end_tags
    def handle_endtag(self, tag):
        if tag == 'div' and self.inDiv == True:
            self.divlvl = self.divlvl - 1
            if self.divlvl == 0:
                self.inDiv = False