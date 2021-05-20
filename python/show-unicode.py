#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def convert_line(line):
    raw = json.dumps(line)
    converted = raw.strip('"')
    if converted[-2:] == '\\n':
        converted = converted[:-2]
    print(converted)

def get_file_as_line_list(file):
    with open(file) as f:
        lines = f.readlines()
    return lines

def is_file(file):
    file = Path(file)
    if file.is_file():
        return True
    return False

def main():
    input = ' '.join(sys.argv[1:])
    
    if is_file(input):
        lines = get_file_as_line_list(input)
    else:
        # Assume stdin string.
        lines = [input]
    for line in lines:
        convert_line(line)


if __name__ == '__main__':
    main()
