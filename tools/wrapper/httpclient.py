import re
import gzip
import io

try:
    from http.client import HTTPConnection
    import http.client as httplib
except ImportError: 
    from httplib import HTTPConnection
    import httplib
    
    
# Constants
C_TYPE = "Content-Type"
C_ENCODING = "Content-Encoding"

# headers for the program
headers = {'Accept-Encoding' : 'compress, gzip'}

# Img MIME Types
IMG_JPEG = "image/jpeg"
TEXT_HTML = "text/html"

# Link Parsing Patterns
HTTP_STRIP_PATTERN = re.compile(r"http://(.*)")
URL_PATTERN = re.compile(r'^(\w+([.]\w+)+)((/(.*))*)*')

# Pattern Parsing Result
MIME_TYPE_PATTERN = re.compile(r'(\w+/\w+)')
CHARSET_PATTERN = re.compile(r'charset=([\w-]+)')

class HTTPGetRequest(HTTPConnection, object):
    '''wraps the link into a http GET request to send to the server'''
    def __init__(self, link, retry=5):     
        self.retry = retry
        if type(link) != str:
            raise ValueError("HTTPRequest argument not type (string)")             
        try:
            r = HTTP_STRIP_PATTERN.search(link)
            if r:
                r = URL_PATTERN.search(r.group(1))
            else:
                r = URL_PATTERN.search(link)
            self.main, self.page = r.group(1), r.group(4)
        except AttributeError:
            raise Exception("Invalid URL - ", link)
        except IndexError:
            raise Exception("Invalid URL - ", link)
        
        HTTPConnection.__init__(self, self.main, 80)
        self.request("GET", self.page, headers=headers)
     
    ''' Method override for getresponse()'''
    def getresponse(self):
        fd = None
        for i in range(self.retry):
            fd = super(HTTPGetRequest,self).getresponse()
            if fd.status != 504:
                break
            else:
                fd.read() # Need to clear stream before request again
                self.request("GET", self.page, headers=headers)
        return fd

class HTTPResponse():
    ''' http.client.HTTPResponse Wrapper class to parse additional data'''
    def __init__(self, http_response):
        # wrap the response inside the class IF it is of that type
        if not isinstance(http_response, httplib.HTTPResponse):
            print(http_response.__class__)
            raise ValueError("Incorrect argument type. Usage: HTTPResponseWrapper(http.client.HTTPResponse)")
        
        self.http_response = http_response
        self.content = ""
        
        # parse meta-header data
        # check if Content is encoded (gzip, compress)
        self.encoding = http_response.getheader(C_ENCODING)         
        
        # encoding of request
        self.MIME_type, self.charset = http_response.getheader(C_TYPE), None
        if self.MIME_type != None:
            try:
                self.charset = CHARSET_PATTERN.search(self.MIME_type).group(1)
            except AttributeError:
                pass
            self.MIME_type = MIME_TYPE_PATTERN.search(self.MIME_type).group(1)
            
        # status of request
        self.status = http_response.status
        self.reason = http_response.reason
        
        # content of request if any
        self.content = http_response.read()
        
        # if file is compressed
        if self.encoding == 'gzip':
            self.content = io.BytesIO(self.content)
            self.content = gzip.GzipFile(fileobj=self.content).read()
            
        if self.charset == 'utf-8':
            self.content = self.content.decode('utf-8')

    