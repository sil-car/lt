#!/usr/bin/env python3

"""
This script takes a URL as input and outputs a table of links from the URL:
 "URL Title" | "URL link"
"""

import json
import sys
import urllib.request

from html.parser import HTMLParser

input_url = sys.argv[1]

class Parse(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, link in attrs:
                if name == 'href':
                    self.links.append(input_url + link)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass
        #self.datas.append(data)


print(f"\nLinks from: \"{input_url}\"")

def getResponse(url):
    try:
        operUrl = urllib.request.urlopen(url)
    except urllib.error.URLError:
        # Timed out?
        print("Error: Timed out.")
        exit(1)
    if operUrl.getcode() == 200:
        data = operUrl.read().decode()
    else:
        data = None
        print("Error receiving data", operUrl.getcode())
    return data


data = getResponse(input_url)

p = Parse()
p.feed(data)
#print(p.links)
for l in p.links:
    print(l)
