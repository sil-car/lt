#!/bin/env python3

# Show a string with its unicode representation inline.
# Accept piped input or a series of arguments.
# Ref:
# - https://stackoverflow.com/questions/58942873/convert-a-string-into-a-unicode-escape-sequence#58943018

import sys


def chr_to_unicode(c):
    return rf'\u{ord(c):04x}'

def str_to_unicode(s):
    return ''.join(map(chr_to_unicode, s))

def print_output_item(ustring):
    print(f"{w} {str_to_unicode(w)}  ", end='')

usage = f"Usage:\n\t{sys.argv[0]} STRING OF TEXT\n\techo \"STRING OF TEXT\" | {sys.argv[0]}"
output = "STRING \\u0053\\u0054\\u0052\\u0049\\u004e\\u0047  OF \\u004f\\u0046  TEXT \\u0054\\u0045\\u0058\\u0054"
help = "Output a string along with its unicode representation; accepts piped input or a series of arguments."
if '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    print(f"Output:\n\t{output}\n")
    print(help)
    exit()

if not sys.stdin.isatty():
    for line in sys.stdin:
        for w in line.strip().split():
            print_output_item(str_to_unicode(w))
        print()
elif len(sys.argv) > 1:
    for w in sys.argv[1:]:
        print_output_item(str_to_unicode(w))
    print()
