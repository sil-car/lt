#!/usr/bin/env python3

"""Gather all json strings from the Lessons from Luke website and convert to an ODT file.
"""

import requests

from pathlib import Path

# The site is organized by language then lesson; e.g.
# lfl_api / language / [2,5] / lessons / [1-112]
# language 2 == French; language 5 == Sango
lfl_api = "https://luke.silcameroon.org/api"
lfl_data = Path(__file__).resolve().parent / 'lfl-data'
lfl_data.mkdir(exist_ok=True)
outfile = lfl_data / 'LessonsFromLuke_sg.odt'
# languages = [2, 5]
languages = [5] # Sango JSON files include both "source" (FR) and "text" (SG)
lessons = range(1, 113)

ans = input("Download text from the website? [y/N]: ")
if ans and ans.lower()[0] == 'y':
    # Copy JSON files to lfl_data.
    for language in languages:
        for lesson in lessons:
            outf = lfl_data / f"{language}-{lesson}-tStrings.json"
            print(f"Downloading language {language}, lesson {lesson}...")
            try:
                r = requests.get(f"{lfl_api}/languages/5/lessons/1/tStrings")
            except KeyboardInterrupt:
                print("\nInterrupted with Ctrl-C.")
                exit(1)
            outf.write_text(r.text)

data_files = [f for f in lfl_data.glob('*.json')]
data_files.sort()

