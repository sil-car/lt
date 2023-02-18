#!/usr/bin/env python3

"""
Create an inclusive-orthography Sango DIC file from a worlist.txt file.
  - Start with lexicon.txt and add entries to DIC file with affixes according to parts of speech.
  - Find plural words from wordlist file and ensure that the singular forms include
plural prefixes.
"""

import re
import sys

from pathlib import Path

PUNC = '!@#$%^&*()_[]{}|<>«»\'"/\\+:;,.?\n'

class Affix():
    def __init__(self, flag=None, valid_parts=[]):
        self.flag = flag
        self.parts_of_speech = valid_parts

class DicLine():
    def __init__(self, line_str=None):
        self.word = None
        self.flags = []
        if line_str is not None:
            self.word, self.flags = self.parse_dic_line(line_str)

    def add_flag(self, flag):
        if flag in self.flags:
            return
        self.flags.append(flag)
        self.flags.sort()

    def parse_dic_line(self, dic_line_str):
        line = dic_line_str.split('/')
        word =  line[0]
        flags_str = ''
        if len(line) > 1:
            flags_str = line[1]
        flags = list({f for f in flags_str.strip()})
        flags.sort()
        return word, flags[:]

    def to_str(self):
        if len(self.flags) > 0:
            return f"{self.word}/{''.join(self.flags)}"
        else:
            return self.word

class LexLine():
    def __init__(self, line_str=None):
        self.word = None
        self.parts_of_speech = []
        if line_str is not None:
            self.word, self.parts_of_speech = self.parse_lex_line(line_str)

    def parse_lex_line(self, lex_line_str):
        line = lex_line_str.split('\t')
        word = line[0]
        parts_str = ''
        if len(line) > 1:
            parts_str = line[1]
        parts = list({p for p in parts_str.strip().split()})
        parts.sort()
        return word, parts[:]

    def to_str(self):
        if len(self.parts_of_speech) > 0:
            return f"{self.word}\t{' '.join(self.parts_of_speech)}"
        else:
            return self.word

def ensure_affix(affix_obj, dic_line_obj, lex_line_obj):
    # Check if any item from list1 is in list2 using set intersection '&'.
    # - Ref: https://stackoverflow.com/a/31456860
    if set(affix_obj.parts_of_speech) & set(lex_line_obj.parts_of_speech):
        dic_line_obj.add_flag(affix_obj.flag)
    return dic_line_obj

def update_dic_line_flags(dic_line_str, flags):
    dic_line = DicLine(line_str=dic_line_str)
    for f in flags:
        dic_line.add_flag(f)
    return dic_line.to_str()

def lex_to_dic_entry(lex_line_str, dic_line_str=None):
    dic_line = DicLine(line_str=dic_line_str)
    lex_line = LexLine(line_str=lex_line_str)
    dic_line.word = lex_line.word

    # Add flags.
    # Ensure 'A' prefix.
    A = Affix(flag='A', valid_parts=['Adjective', 'Noun', 'Verb'])
    dic_line = ensure_affix(A, dic_line, lex_line)

    return dic_line.to_str()

def main():
    # Ensure wordlist file is passed.
    if len(sys.argv) < 2 or sys.argv[1].split('.')[1] != 'txt':
        print(f"USAGE: {sys.argv[0]} WORDLIST.txt")
        exit(1)

    # Set other filenames based on wordlist file.
    words_file = Path(sys.argv[1]).expanduser().resolve()
    lex_file = words_file.with_name(f"lexicon.txt")
    dic_file = words_file.with_name(f"{words_file.stem}.dic")

    # Initialize output lines.
    dic_lines = []

    # Add dic lines from lexicon.
    if lex_file.is_file():
        with lex_file.open() as f:
            lex_lines = f.readlines()

        for l in lex_lines:
            dic_lines.append(lex_to_dic_entry(l))


    # Prepare dic lines from wordlist.
    if words_file.is_file():
        with words_file.open() as f:
            words = f.read().split()

        for word in words:
            for c in word:
                if c in PUNC:
                    word.replace(c, '')

        # Handle plural words.
        flag = 'A'
        possible_plurals = [w for w in words if len(w) > 2 and (
                w[0] == 'a' or w[0] == 'â' or w[:2] == 'a-' or w[:2] == 'â-'
            )
        ]

        wordlist_dic_lines = words.copy()
        plurals = []
        for p in possible_plurals:
            for i, w in enumerate(words):
                if len(w) < 2:
                    # Skip single-letter items.
                    continue
                if p[1:] == w or (p[1] == '-' and p[2:] == w):
                    dic_line = DicLine(line_str=w)
                    # if flag in dic_line.flags:
                    #     continue
                    dic_line.add_flag(flag)
                    wordlist_dic_lines[i] = dic_line.to_str()
                    plurals.append(p)

        wordlist_dic_lines = [w for w in wordlist_dic_lines if w not in plurals]

        # Merge dic_lines from wordlist to DIC.
        dic_line_words = [DicLine(l).word for l in dic_lines]
        for l in wordlist_dic_lines:
            d = DicLine(l)
            if d.word not in dic_line_words:
                dic_lines.append(d.to_str())
        dic_lines.sort()

    with dic_file.open('w') as f:
        f.write(f"{len(dic_lines)}\n")
        n = '\n'
        f.write(f"{n.join(dic_lines)}")


if __name__ == '__main__':
    main()
