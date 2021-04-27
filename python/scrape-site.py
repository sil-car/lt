#!/usr/bin/env python3

"""This script takes a URL as input and outputs an MD-formatted list of (.mp4) links from the URL:
 ["URL Title"]("URL link")"""

import argparse
import json
import urllib.parse
import urllib.request

from html.parser import HTMLParser


class Parse(HTMLParser):
    def __init__(self, filetypes):
        super().__init__()
        self.links = []
        self.filetypes = filetypes
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, link in attrs:
                end = link.split('.')[-1]
                if name == 'href' and end in self.filetypes:
                    if link[:4] != 'http':
                        url_out = input_url + link
                    else:
                        url_out = link
                    self.links.append(
                        {
                            "url": url_out,
                            "title": urllib.parse.unquote(link)
                        }
                    )

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


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

def filetype_list(string):
    return string.split(',')


# Define allowed arguments.
parser = argparse.ArgumentParser(
    prog="scrape-site.py",
    description="Find download links of the given filetype from the given link."
)
parser.add_argument(
    '--types',
    type=filetype_list,
    default='mp4',
    nargs=1,
    help="Define which filetype(s) to find (default is 'mp4'). Multiple values should be separated by commas: exe,mp4"
)
parser.add_argument(
    'URL',
    help='The link to the site you wish to scrape for file downloads.'
)

# Parse arguments; set variables.
args = parser.parse_args()
types = args.types[0]
filetypes = []
for filetype in types:
    filetypes.append(filetype.lower())
input_url = args.URL

# Parse webpage.
data = getResponse(input_url)
p = Parse(filetypes)
p.feed(data)

# Create output.
print(f"### {input_url}")
for l in p.links:
    print(f"[{l['title']}]({l['url']})  ")
