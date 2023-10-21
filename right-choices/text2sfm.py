#!/usr/bin/env python3

import regex as re
# import re # look-behind requires fixed-width pattern
import sys

from pathlib import Path

# def seqchap(m):
#     t.setdefault(m.group(0))

infiles = sys.argv[1:]
for infile in infiles:
    f = Path(infile)
    outfile = f.with_suffix('.sfm')
    text = f.read_text()

    # Remove final null page-break characters from PDF scraping.
    text = re.sub(b'\x0A\x0C', b'\x0A', text.encode()).decode()
    # Remove double newlines after bulleted lines if mid-sentence.
    text = re.sub(r'(?<=•.*[\pL;,])\n{2}(?=[\pL])', r'\n', text)
    # Remove page numbers.
    text = re.sub(r'\n{2}\d+\n{2}\d+\n{2}', r'\n', text) # double group
    text = re.sub(r'\n{2}\d+\n{2}', r'\n', text) # single group
    # Re-add 2x newline before "memory verse" (English).
    text = re.sub(r'(?<=\pP\n)(?=Memory Verse:)', r'\n', text)
    # Re-add 2x newline before "memory verse" (Sango).
    text = re.sub(r'(?<=\pP\n)(?=Bata sura so na li ti mo:)', r'\n', text)
    # Re-add 2x newline after memory verse reference.
    text = re.sub(r'(?<=\(.*[\db]\)\n)(?!\n)', r'\n', text)
    # Ensure 2x newline before lesson title (English)
    text = re.sub(r'(?<=\S\n)(.+\n{2})(?=A Situation and a Choice:)', r'\n\n\1', text)
    # Ensure 2x newline before lesson title (Sango).
    text = re.sub(r'(?<=\S\n)(.+\n{2})(?=Soro oko na popo ni:)', r'\n\n\1', text)
    # Add 2x newline after line-ending colons that should stay end-of-line.
    end_words = [
        'Choice:',
        'Soro oko na popo ni:',
        'Verse:',
        'na li ti mo:',
        'Film”:',
        'Explore:',
        'mo gi ndani:',
        'Prayer:',
        'Sambela:',
        'Bible:',
        '\nmo:',
        '\nti mo:',
    ]
    for w in end_words:
        text = re.sub(r'(?<=%s)' % w, r'\n', text)
    # Remove mid-paragraph newlines.
    text = re.sub(r'(?<=[\w\.,,?;”’»!:\)—-])\n(?=[\w“‘«\(])', r' ', text) 
    # Remove 2x newline after line-ending colons.
    for w in end_words:
        text = re.sub(r'(?<=%s\n)\n' % w, r'', text)
    # Remove extra 2x newline after Bible Verse (Sango).
    text = re.sub(r'(?<=mbeti ti Nzapa ti mo:\n)\n', r'', text)
    # Put Memory Verse reference back on own line (English).
    text = re.sub(r'(?<=Memory Verse:\n.* )(?=\()', r'\n', text)
    # Put Memory Verse reference back on own line (Sango).
    text = re.sub(r'(?<=Bata sura so na li ti mo:\n.* )(?=\()', r'\n', text)
    # Squeeze 3+ newlines into 2.
    text = re.sub(r'\n{3,}', r'\n\n', text)
    # Add \c markers before each lesson.
    # Add \v markers: 1: prose; 2: study page
    # Add other markers...

    outfile.write_text(text)
