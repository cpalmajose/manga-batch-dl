import zipfile, io, requests


URL = "http://reader.vortex-scans.com/reader/download/minamotokun_monogatari__/en/0/"

FILE = "/[Vortex-Scans]Minamoto-kun_Monogatari__c"
CHP = 128

response = requests.get(URL + str(CHP) + "/")
z = zipfile.ZipFile(io.BytesIO(response.content))
z.extractall()
