#!/usr/bin/env python3

"""Find plural words from sango DIC file and update the singular forms to include
plural prefixes."""

import re
import sys

from pathlib import Path

infile = Path(sys.argv[1]).expanduser().resolve()
outfile = infile.with_name(f"{infile.stem}_mod.dic")

with infile.open() as f:
    infile_lines = f.readlines()

words = [l.strip() for l in infile_lines]
possible_plurals = [w for w in words if w[0] == 'a' or w[:2] == 'a-']

updated_words = words.copy()
plurals = []
for p in possible_plurals:
    for j, w in enumerate(words):
        if len(p) < 2:
            continue
        if p[1:] == w or (p[1] == '-' and p[2:] == w):
            # print(f"Found singular \"{words[i]}\" for {p}")
            updated_words[j] = f"{updated_words[j]}/A"
            plurals.append(p)

updated_words = [w for w in updated_words if w not in plurals]


with outfile.open('w') as f:
    for w in updated_words:
        f.write(f"{w}\n")
