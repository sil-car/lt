#!/usr/bin/env python3

# Convert plain text document (Biblical book) with chapter and verse numbers to SFM format.

import regex as re
import sys

from pathlib import Path


def has_footnotes(text):
    # Assumes footnote text looks like: "a 1.11 footnote text"
    matched_string = re.search(r'^[a-z] [0-9]+\.[0-9]+', text, flags=re.MULTILINE)
    return matched_string is not None


# Handle infile and outfile.
txt_file = Path(sys.argv[1]).expanduser().resolve()
sfm_file = txt_file.with_suffix('.sfm')

# Slurp infile.
text = txt_file.read_text()
if has_footnotes(text):
    print("WARNING: This script doesn't handle footnotes. Move them inline first; e.g. \"\\f + \\fr #.# \\ft text \\fq quote \\f*\"")
    exit(1)

# GENERAL CLEANUP
# Remove repeated spaces.
text = re.sub(r' {2,}', r' ', text)
# Remove spaces from otherwise empty lines.
text = re.sub(r'^ *$', r'', text, flags=re.MULTILINE)
# Remove spaces from either end of lines.
text = re.sub(r'^ *(.*) *$', r'\1', text, flags=re.MULTILINE)
# Remove text from lines that start with 2 or more capital letters (i.e. page titles/numbers).
text = re.sub(r'\n+\d*\s*[[:upper:]]{2}.*\n+(?:\d*\s*[[:upper:]]{2}.*\n+)*', r'\n', text)

# ADD SFM MARKERS
# Add \c chapter markers.
text = re.sub(r'^(?=[0-9]+$)', r'\\c ', text, flags=re.MULTILINE)
# Add \v verse markers for line-start verse numbers.
text = re.sub(r'^(?=[0-9]+ .)', r'\\v ', text, flags=re.MULTILINE)
# Add \v verse markers for mid-line verse numbers.
text = re.sub(r'(?<!\\v)(?= [0-9]+ )', r'\n\\v', text)
# Add \s1 section titles markers to single non-marked lines, double-spaced before and after.
text = re.sub(r'(?<=\n{2}|^\n)(?=[^\\].*\n{2})', r'\\s1 ', text)
# Add \p paragraph markers with newline before double text lines, double-spaced before, starting with a verse marker.
text = re.sub(r'(?<=\n{2}|^\n)(?=\\v.*\n.)', r'\\p\n', text)
# Add \p paragraph markers before double text lines, double-spaced before, starting with text.
text = re.sub(r'(?<=\n{2}|^\n)(?=[^\\v\s].*\n.)', r'\\p ', text)
# Remove mid-sentence line breaks.
text = re.sub(r'(?<!\\p|\\c \d+|\n)\n(?!\s|\\)', r' ', text)

# FINAL CLEANUP
# Swap section titles and chapter number lines if in wrong order.
text = re.sub(r'(\\s[^\n]+\n+)(\\c[^\n]+\n+)', r'\2\1', text)
# Remove repeated newlines.
text = re.sub(r'\n+', r'\n', text)
# Write outfile.
sfm_file.write_text(text)