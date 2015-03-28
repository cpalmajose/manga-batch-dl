'''
Created on Mar 19, 2015

@author: Chris A
'''
from __future__ import print_function
from threading import Thread
from time import gmtime, strftime
import re
import time
import sys
import os
import parse


try:
    from multiprocessing import cpu_count   # ver 2
except ImportError:
    from os import cpu_count                # ver 3

spinner = ["|", "/", "-", "\\"]

URL_PATTERN = re.compile(r'^(\w+([.]\w+)+)((/(.*))*)*')
HTTP_STRIP_PATTERN = re.compile(r"^http://(.*)")
oldpattern = re.compile(r'/([\d]+-[\d]+-)([\d]+)(.+)')
newpattern = re.compile(r'((.+)/)([\d]+)$')
test = newpattern.search("/dragon-ball/1/1").groups()
for i in test:
    print(i)
b = "/dragon-ball/1/2".split("/")
print(b)

print(parse.nextpage("/ore-monogatari/1/99"))
print(parse.nextpage("/115-3543-1/hajime-no-ippo/sdfd.html"))


'''class A(Thread):
    def run(self):
        for i in range(5):
            sys.stdout.write(str(i)+"\r")
            sys.stdout.flush()
            time.sleep(1)

A().run()'''

#test_str = "('Content-Type', 'text/html; charset=utf-8')"
#test = fileio.Directory("D:/")
#test.write(fileio.WriteFile("pic/test/pic.jpg"))

#print(threading.active_count(), end="\r")

#print(str(cpu_count()))
print(os.getcwd())
print(os.path.split(os.path.join(os.getcwd(), "test/testfile.txt")))