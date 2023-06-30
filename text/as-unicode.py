#!/bin/env python3

# Convert a string to its unicode representation.
# Accept piped input or a series of arguments.
# Ref:
# - https://stackoverflow.com/questions/58942873/convert-a-string-into-a-unicode-escape-sequence#58943018

import sys

SPACES=False

def to_unicode_escape(c):
    # Don't convert spaces by default in order to improve readability.
    if SPACES:
        return rf"\u{ord(c):04x}"
    else:
        return c if c == ' ' else rf"\u{ord(c):04x}"

usage = f"Usage:\n\t{sys.argv[0]} STRING\n\techo \"STRING\" | {sys.argv[0]}"
output = "\\u0053\\u0054\\u0052\\u0049\\u004e\\u0047"
help = "Convert a string to its unicode representation; accepts piped input or a series of arguments."
if '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    print(f"Output:\n\t{output}\n")
    print(help)
    exit()
elif '-s' in sys.argv or '--spaces' in sys.argv:
    SPACES=True

if not sys.stdin.isatty():
    for line in sys.stdin:
        print("".join(to_unicode_escape(c) for c in line.rstrip()))
elif len(sys.argv) > 1:
    string = ' '.join(sys.argv[1:])
    print("".join(to_unicode_escape(c) for c in string.rstrip()))
