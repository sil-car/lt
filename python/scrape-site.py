#!/usr/bin/env python3

"""
This script takes a URL as input and outputs a table of (.mp4) links from the URL:
 "URL Title" | "URL link"
"""

import json
import sys
import urllib.parse
import urllib.request

from html.parser import HTMLParser


class Parse(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, link in attrs:
                if name == 'href' and link.endswith(".mp4"):
                    self.links.append(
                        {
                            "url": input_url + link,
                            "title": urllib.parse.unquote(link)
                        }
                    )

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass
        #self.datas.append(data)


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


input_url = sys.argv[1]
data = getResponse(input_url)
p = Parse()
p.feed(data)

for l in p.links:
    print(f"[{l['title']}]({l['url']})")
