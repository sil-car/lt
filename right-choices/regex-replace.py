#!/usr/bin/env python3

import regex as re
# import re # look-behind requires fixed-width pattern
import sys

from pathlib import Path

target_file = Path(sys.argv[1])
if not target_file.is_file():
    print(f"Error: Not a file: {sys.argv[1]}")
    exit(1)
if len(sys.argv) < 3:
    print(f"Error: Not enough arguments.")
    exit(1)

search_str = sys.argv[2]
if len(sys.argv) > 3:
    repl_str = (sys.argv[3])
else:
    repl_str = ''

text = target_file.read_text()
text = re.sub(search_str, repl_str, text)
print(text)
