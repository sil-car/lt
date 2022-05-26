#!/bin/env python3

# Convert a string to its unicode representation.
# Accept piped input or a series of arguments.
# Ref:
# - https://stackoverflow.com/questions/58942873/convert-a-string-into-a-unicode-escape-sequence#58943018

import sys

usage = f"Usage:\n\t{sys.argv[0]} STRING\n\techo \"STRING\" | {sys.argv[0]}"
output = "\\u0053\\u0054\\u0052\\u0049\\u004e\\u0047"
help = "Convert a string to its unicode representation; accepts piped input or a series of arguments."
if '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    print(f"Output:\n\t{output}\n")
    print(help)
    exit()

if not sys.stdin.isatty():
    for line in sys.stdin:
        print("".join(map(lambda c: rf"\u{ord(c):04x}", line.rstrip())))
elif len(sys.argv) > 1:
    string = ' '.join(sys.argv[1:])
    print("".join(map(lambda c: rf"\u{ord(c):04x}", string)))
