#!/usr/bin/env python3

import regex as re
# import re # look-behind requires fixed-width pattern
import sys

from pathlib import Path

infile = Path(sys.argv[1])
outfile = infile.with_name(f"{infile.stem}_clean.txt")

file_bytes = infile.read_bytes()

## Byte-level cleanup.
# Remove null page-break characters from PDF scraping
file_bytes = re.sub(b'\x0A\x0C', b'\x0A', file_bytes)

## Text-level cleanup.
file_text = file_bytes.decode()
# Squeeze repeated spaces.
file_text = re.sub(r' +', r' ', file_text)
# Squeeze 3 or more newlines to 2.
file_text = re.sub(r'\n{3,}', r'\n\n', file_text)
# Remove end-of-line spaces.
file_text = re.sub(r' *(?=\n)', r'', file_text)
# Fix double-single quotes.
file_text = re.sub(r'‘{2}', r'“', file_text)
file_text = re.sub(r'’{2}', r'”', file_text)
# Remove double newlines after TOC pg. numbers.
file_text = re.sub(r'(?<=\. *\d+)\n{2}', r'\n', file_text)
# Remove double newlines before bullet points.
file_text = re.sub(r'\n{2}(?=•)', r'\n', file_text)
# Remove double newlines after bulleted lines if mid-sentence.
file_text = re.sub(r'(?<=•.*[\pL;])\n{2}(?=[\pL])', r'\n', file_text)
# Remove double newlines after colons.
file_text = re.sub(r': *\n{2,}', r':\n', file_text)
# Re-insert double newlines after "Film”:".
file_text = re.sub(r'(?<=Film”: *)', r'\n', file_text)
# Remove double newlines before lines beginning in "(" (Bible references).
file_text = re.sub(r'\n+ *\(', r'\n(', file_text)
# Remove mid-sentence double newlines.
file_text = re.sub(r'(?<=\pL) *\n{2,} *(?=\pL)', r'\n', file_text)
# Re-insert double newlines before "A Situation and a Choice:".
file_text = re.sub(r'(?<=\S)\n(?=A Situation and a Choice:)', r'\n\n', file_text)
file_text = re.sub(r'(?<=\S)\n(?=Soro oko na popo ni:)', r'\n\n', file_text)

outfile.write_text(file_text)
