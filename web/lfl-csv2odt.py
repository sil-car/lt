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
outfile = lfl_data / f"Lessons from Luke - Sango.odt"
