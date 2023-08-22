#!/usr/bin/env python

import time
import urllib.request
import json 
from pprint import pprint

while True:

    try:
        with urllib.request.urlopen("http://192.168.0.11:5000/position_json") as url:
            data = json.loads(url.read())
            #pprint(data)
            #print(type(data))
            print("quad: " + str(data['id']) + "lat: " + str(data['lat']) + "lng: " + str(data['lng']) + "alt: " + str(data['alt']) )

            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(5)
        pass

    