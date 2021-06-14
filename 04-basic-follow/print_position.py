#!/usr/bin/env python

import time
import urllib.request, json 


while True:

    try:
        with urllib.request.urlopen("http://127.0.0.1:5000/position_json") as url:
            data = json.loads(url.read().decode())
            print(data)
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(5)
        pass

    