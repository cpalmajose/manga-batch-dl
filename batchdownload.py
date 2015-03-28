'''
Created on Mar 21, 2015

@author: Chris A
'''
from __future__ import print_function
from time import strftime, gmtime

import sys
import getopt

import fileio
import parse
import wrapper
import io

USAGE = "USAGE: batchdownload.py <url> -h -d[relative directory] -D[full directory]\n"
TIME_FORMAT = "%a_%d_%b_%Y_%H%M%S"


def main(argv):
   
    d = None
    try:
        opts, args = getopt.getopt(argv, "hd:D:", ["help", "rdir=", "fdir="])
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)
    for opt, value in opts:
        if opt == 'd' or '--rdir':
            d = "~" . value
        elif opt == 'D' or '--fdir':
            d = value
        else:
            print(USAGE)
            sys.exit(1)
    
    if len(args) != 1:
        print("\nArgument Error: URL of manga required\n")
        print(USAGE)
        sys.exit(2)
    
    try:
        wdir = fileio.Directory(d)    
        logger = fileio.Directory(d)  # implement later
        
        cur_time = strftime(TIME_FORMAT, gmtime())
        wdir.mkdir(str(cur_time))
        
        conn = wrapper.HTTPGetRequest(args[0])
        print(conn.main)
        fd = wrapper.HTTPResponse(conn.getresponse())
        if fd.status == 200 and fd.MIME_type == wrapper.TEXT_HTML:
            chapterParse = parse.MangaReaderChapter(parse.CHAPTER)
            chapterParse.feed(fd.content)
            if len(chapterParse.links) == 0:
                print("No Chapter Links")
                sys.exit(1)
            chp, img = (1, 1)
            for link in chapterParse.links:
                done = False
                pageLink = link
                wdir.mkdir(''.join([cur_time, "/" , str(chp)]))
                
                while not done:
                    conn2 = wrapper.HTTPGetRequest(str(conn.main) + str(pageLink))
                    fd2 = wrapper.HTTPResponse(conn2.getresponse())
                    if fd2.status == 200 and fd.MIME_type == wrapper.TEXT_HTML:
                        imgParse = parse.MangaReaderImage(parse.IMAGE)
                        imgParse.feed(fd2.content)
                        if imgParse.imglink:
                            conn3 = wrapper.HTTPGetRequest(imgParse.imglink)
                            fd3 = wrapper.HTTPResponse(conn3.getresponse())
                            if fd3.status == 200 and fd3.MIME_type == wrapper.IMG_JPEG:
                                print(''.join(["Downloading: " , imgParse.imglink , ". . ."]), end="")
                                fstream = io.BytesIO(fd3.content)
                                filename = ''.join([cur_time , "/" , str(chp) , "/" , str(img) , ".jpeg"])
                                wdir.write(fileio.WriteFile(filename, fstream), 'wb')
                                print("done")
                                pageLink = parse.nextpage(pageLink)
                                img = img + 1                             
                            else:
                                print("Error Getting Image")
                        else:
                            print("Error Getting Image Link")
                            pageLink = parse.nextpage(pageLink)
                            img = img + 1
                    elif fd2.status == 404:
                        print("Finished Downloading Chapter: " + str(chp))
                        chp = chp + 1
                        img = 1
                        done = True
                    else:
                        print("Error Getting Chapter Images")                    
            else:
                print("Error with URL: Content not text/html") # or if done getting all links 
        
    except fileio.DirNotFoundError as e:
        print("\nERROR: " + e.message + "\n")
        sys.exit(2)
    except Exception as e:
        print("\nERROR: " + str(e) + "\n")
        sys.exit(2)
    
        
if __name__ == "__main__":
    main(sys.argv[1:])
    
