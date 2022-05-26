#!/usr/bin/python3

"""
Search a given Paratext project for details about a specific word.
"""

import re
import sys

from pathlib import Path

pt_home = Path.home() / "Paratext8Projects"


def count_string_occurrences_in_book(book_file, word):
    pat = f"^.*{word}.*$"
    matches = re.findall(pat, book_file.read_text(), re.MULTILINE)
    count = len(matches)
    return count, matches

def count_byte_occurrences_in_book(book_file, word):
    pat = str.encode(f"^.*{word}.*$")
    matches = re.findall(pat, book_file.read_bytes(), re.MULTILINE)
    count = len(matches)
    return count, matches

def list_projects(pt_home):
    # List projects in PT directory as a guide.
    for dir in pt_home.iterdir():
        if dir.is_dir() and dir.stem[0] != '_':
            print(dir.name)


# Ensure proper number of arguments passed.
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <project name> <search term>")
    print(f"\nAvailable projects:")
    list_projects(pt_home)
    exit(1)
else:
    project = sys.argv[1]
    proj_dir = pt_home / project
    word = sys.argv[2]

    # Input strings can be one of: unicode, unicode_escape, bytecode.
    if word[:2] == '\\x':
        # Bytecode-escape word passed.
        word_string = word.encode('utf-8').decode()
        word_bytes = word.encode('utf-8') # TODO: Wrong: This escapes the "\" with another one.
        word_unicode = word.encode('unicode-escape').decode('utf-8')
        #word_unicode = word.encode('unicode-escape')
    elif word[:2] == '\\u':
        # Unicode-escape word passed.
        word_string = word.encode('unicode-escape').decode('utf-8', 'replace')
        word_bytes = word.encode('unicode-escape')
        word_unicode = word
    else:
        # Assume unicode string.
        word_string = word
        word_bytes = word.encode('utf-8')
        word_unicode = word.encode('unicode-escape').decode('utf-8')

# Ensure project exists.
if not proj_dir.exists():
    print(f"Error: No project \"{project}\".\n\nPlease choose one from this list:")
    list_projects(pt_home)
    exit(1)

# List and sort the project book files.
files = proj_dir.iterdir()
book_files = [file for file in files if file.suffix == '.SFM']
book_files.sort()

# Check for search term in book files.
word_ct = 0
occurrences_dict = {}
for book_file in book_files:
    if word[:2] == "\\x":
        count, matches = count_byte_occurrences_in_book(book_file, word)
    else:
        count, matches = count_string_occurrences_in_book(book_file, word)
    occurrences_dict[book_file] = matches
    word_ct += count

# Summarize results.
print(f"{word_ct} total occurrences of \"{word}\" (unicode-escaped: {word_unicode}; bytes: {word_bytes})")
if word_ct == 0:
    exit()
try:
    input("Press [Enter] to see full results or Ctrl+C to quit. ")
except KeyboardInterrupt:
    print()
    exit(0)

# Print complete results.
for file_name, lines in occurrences_dict.items():
    if lines:
        print(f"\n{file_name}")
        for line in lines:
            print(line)
