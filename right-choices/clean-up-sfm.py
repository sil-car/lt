#!/usr/bin/env python3

import regex as re
# import re # look-behind requires fixed-width pattern
import sys

from pathlib import Path


contents = {
    'en': "Contents",
    'sg': "Atënë kue ti mbeti ni",
}
choices = {
    'en': "Choices",
    'sg': "Asorongo-ye",
}
situation = {
    'en': "A Situation and a Choice:",
    'sg': "Soro oko na popo ni:",
}
memory_verse = {
    'en': "Memory Verse:",
    'sg': "Bata sura so na li ti mo:",
}
think = {
    'en': "Think and Explore:",
    'sg': "Gbu li ti mo na mo gi ndani:",
}
how = {
    'en': "How Should I Live Out the ‘Right Choice’?",
    'sg': "Na lege nye si mbi lingbi soro ye ti Mbirimbiri?",
}
prayer = {
    'en': "Prayer:",
    'sg': "Sambela:",
}
read = {
    'en': "Read the Story in Your Bible:",
    'sg': "Diko mbaye ni na ya ti mbeti ti Nzapa ti mo:",
}

def handle_toc_text(m):
    ttext = m.group(0)
    # Mark each entry line as a new paragraph and a verse.
    ttext = re.sub(r'(.*\.+\s*\d+)', r'\\ip \1', ttext)
    # Mark each description line as a new paragraph.
    ttext = re.sub(r'(.*\.+\s*\d+\n\n)', r'\1\\ip ', ttext)
    # Remove blank lines.
    ttext = re.sub(r'\n\n', r'\n', ttext)
    return ttext

def handle_choices_text(m):
    ctext = m.group(0)
    

def handle_lesson_text(m):
    ltext = m.group(0)
    # Mark the Section Header.
    ltext = re.sub(r'(?<=\\c.*\n)(.*\n)\n', r'\\s1 \1', ltext)
    # Mark list items.
    ltext = re.sub(r'(?<=\n)(?=•)', r'\\li1 ', ltext)
    for t in situation.values():
        # Mark the Section Subeader.
        ltext = re.sub(r'(?=%s)' % t, r'\\s2 ', ltext)
        # Mark the Summary line as v1.
        ltext = re.sub(r'(?<=%s\n)' % t, r'\\p\n\\v 1 ', ltext)
        # Mark the next line of text as v2.
        ltext = re.sub(r'(?<=%s\n.*\n\n)' % t, r'\\p\n\\v 2 ', ltext)
    for t in memory_verse.values():
        # Mark Memory Verse as s2.
        ltext = re.sub(r'(?=%s)' % t, r'\\s2 ', ltext)
        # Mark the next line of text as v3.
        ltext = re.sub(r'(?<=%s\n)' % t, r'\\v 3 ', ltext)
    for t in think.values():
        # Mark line before as v4.
        ltext = re.sub(r'(?<=\n)(?=.*\n\n%s)' % t, r'\\p\n\\v 4 ', ltext)
        # Mark Think line as v5.
        ltext = re.sub(r'(?=%s)' % t, r'\\p\n\\v 5 ', ltext)
    for t in how.values():
        # Mark How line as v6.
        ltext = re.sub(r'(?=%s)' % t, r'\\p\n\\v 6 ', ltext)
    for t in prayer.values():
        # Mark Prayer line as v7.
        ltext = re.sub(r'(?=%s)' % t, r'\\p\n\\v 7 ', ltext)
    for t in read.values():
        # Mark Read line as v8.
        ltext = re.sub(r'(?=%s)' % t, r'\\p\n\\v 8 ', ltext)
        # Insert new paragraph before verse reference line.
        ltext = re.sub(r'(?<=%s\n)' % t, r'\\p ', ltext)
    # Add p markers to each remaining unmarked line.
    ltext = re.sub(r'(?<=\n)(?=[\pL“(])', r'\\p ', ltext)
    # Remove blank lines.
    ltext = re.sub(r'\n\n', r'\n', ltext)
    return ltext

infiles = sys.argv[1:]
for infile in infiles:
    f = Path(infile)
    outfile = f.with_name(f"{f.stem}_sfm.sfm")
    text = f.read_text()
    for l in ['en', 'sg']:
        text = re.sub(r'(?s)(?<=\n\n%s)(.*)(?=\n\n%s)' % (contents.get(l), choices.get(l)), handle_toc_text, text)
    text = re.sub(r'(?s)(\\c \d+.*)(?=\n\n\\c|\n\nDottie & Josh McDowell)', handle_lesson_text, text)

    outfile.write_text(text)
