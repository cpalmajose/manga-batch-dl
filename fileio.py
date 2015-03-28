'''
Created on Mar 19, 2015

@author: Chris A
'''
import os

# Exception Classes
class FileWriteError(OSError):
    ''' raises if cannot write file at directory destination'''
    def __init__(self, message):
        self.message = "Cannot create file - '" + message + "'"
        super(OSError, self).__init__("Cannot create file - '" + message + "'")
        
class DirNotFoundError(OSError):
    ''' raises if directory cannot be opened'''
    def __init__(self, message):
        self.message = "Cannot Open Directory - '" + message + "'"
        super(OSError,self).__init__("Cannot Open Directory - '" + message + "'")

# Wrapper class for writing to a directory
class WriteFile:
    def __init__(self, fname, fstream=None):
        self.fname = fname
        self.fstream = fstream

# Class to open a current directory
class Directory:
    ''' Opens the current directory passed as argument. If Nothing is passed, uses the user directory'''
    def __init__(self, directory=None):
        if directory and type(directory) != str:
            raise ValueError()
        
        try:
            if not directory:
                os.chdir(os.path.expanduser("~"))
                self.dir = "~"
            else:
                os.chdir(directory) 
                self.dir = directory
        except OSError:
            raise DirNotFoundError(directory)
         
    def write(self, writeobj, mode=None):
        ''' writes the file specified in writeobj '''
        if type(writeobj) != WriteFile:
            raise ValueError("Must be of class(WriteFile)")
        
        if mode:
            writemode = mode
        else:
            writemode = 'wb'
        
        (dirname, fname) = os.path.split(os.path.join(os.getcwd(), writeobj.fname))
        try:
            os.chdir(dirname)
        except OSError:
            os.mkdir(dirname)
            os.chdir(dirname)
            
        try:
            fh = open(fname, mode=writemode)
            if writeobj.fstream != None:
                fh.write(writeobj.fstream.read())
            else:
                print("fsteam empty. File: " + fname)
            fh.close()
        except OSError:
            os.chdir(self.dir)
            raise FileWriteError(fname)
        
        if self.dir == '~':
            os.chdir(os.path.expanduser("~"))
        else:
            os.chdir(self.dir)
        
    def mkdir(self, dirname):
        if not isinstance(dirname, str):
            raise TypeError("Argument not type (str): " + str)
        os.mkdir(dirname)
        
