import json
from bs4 import BeautifulSoup as BSP
import urllib,urlparse
import requests
import os

URL="http://www.panoramio.com/map/get_panoramas.php?order=popularity&\
     set=public&from=0&to=20&minx=-77.037564&miny=38.896662&\
     maxx=-77.035564&maxy=38.898662&size=medium";
Res=requests.get(URL);
c=urllib.urlopen(URL);
j=json.loads(Res.content);

