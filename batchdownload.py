from __future__ import print_function
from time import strftime, gmtime

from tools.parse import mangareader
from tools.fileio import fileio
from tools.wrapper import httpclient

import sys
import getopt

import io

# Needs Fixing
USAGE = "USAGE: batchdownload.py <url> -h | --help -d | --dir[full directory]\n"

TIME_FORMAT = "%a_%d_%b_%Y_%H%M%S"


def main(argv):
   
    d = None
    try:
        opts, args = getopt.getopt(argv, "hd:", ["help", "dir="])
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
        
        conn = httpclient.HTTPGetRequest(args[0])
        print(conn.main)
        fd = httpclient.HTTPResponse(conn.getresponse())
        if fd.status == 200 and fd.MIME_type == httpclient.TEXT_HTML:
            chapterParse = mangareader.MangaReaderChapter(mangareader.CHAPTER)
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
                    conn2 = httpclient.HTTPGetRequest(str(conn.main) + str(pageLink))
                    fd2 = httpclient.HTTPResponse(conn2.getresponse())
                    if fd2.status == 200 and fd.MIME_type == httpclient.TEXT_HTML:
                        imgParse = mangareader.MangaReaderImage(mangareader.IMAGE)
#print(type(fd2.content))
                        imgParse.feed(fd2.content)
                        if imgParse.imglink:
                            conn3 = httpclient.HTTPGetRequest(imgParse.imglink)
                            fd3 = httpclient.HTTPResponse(conn3.getresponse())
                            if fd3.status == 200 and fd3.MIME_type == httpclient.IMG_JPEG:
                                print(''.join(["Downloading: " , imgParse.imglink , ". . ."]), end="")
                                fstream = io.BytesIO(fd3.content)
                                filename = ''.join([cur_time , "/" , str(chp) , "/" , str(img) , ".jpeg"])
                                wdir.write(fileio.WriteFile(filename, fstream), 'wb')
                                print("done")
                                pageLink = mangareader.nextpage(pageLink)
                                img = img + 1                             
                            else:
                                print("Error Getting Image")
                        else:
                            print("Error Getting Image Link")
                            pageLink = mangareader.nextpage(pageLink)
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
    #except Exception as e:
    #    print(type(e))
    #    print("\nERROR: " + str(e) + "\n")
    #    sys.exit(2)
    
        
if __name__ == "__main__":
	main(sys.argv[1:])
    
