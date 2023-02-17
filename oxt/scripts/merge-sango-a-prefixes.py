#!/usr/bin/env python3

"""Find plural words from sango DIC file and update the singular forms to include
plural prefixes."""

import re
import sys

from pathlib import Path

if len(sys.argv) < 2 or sys.argv[1].split('.')[1] != 'dic':
    print(f"USAGE: {sys.argv[0]} FILE.dic")
    exit(1)
infile = Path(sys.argv[1]).expanduser().resolve()
outfile = infile.with_name(f"{infile.stem}_mod.dic")

with infile.open() as f:
    infile_lines = f.readlines()

words = [l.strip() for l in infile_lines]
words = words[1:] # remove first line word count
possible_plurals = [w for w in words if w[0] == 'a' or w[0] == 'â' or w[:2] == 'a-' or w[:2] == 'â-']
possible_plurals = [p for p in possible_plurals if len(p) > 1] # remove single-letter items

updated_words = words.copy()
plurals = []
for p in possible_plurals:
    for i, w in enumerate(words):
        if len(w) < 2:
            # Skip single-letter items.
            continue
        if p[1:] == w or (p[1] == '-' and p[2:] == w):
            # print(f"Found singular \"{words[i]}\" for {p}")
            if 'A' in updated_words[i].split('/')[1]:
                # Don't add 'A' more than once.
                continue
            updated_words[i] = f"{updated_words[i]}/A"
            plurals.append(p)

updated_words = [w for w in updated_words if w not in plurals]
updated_words_ct = len(updated_words)


with outfile.open('w') as f:
    f.write(f"{updated_words_ct}\n")
    for w in updated_words:
        f.write(f"{w}\n")
