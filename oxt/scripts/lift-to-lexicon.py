#!/usr/bin/env python3

"""Convert a LIFT file into a basic lexicon with word + parts of speech."""

import sys

from lxml import etree
from pathlib import Path


def get_xml_tree(file_object):
    # Remove existing line breaks to allow pretty_print to work properly later.
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(str(file_object), parser)

def get_lift_entries(xml_tree):
    # Retrieve raw data.
    entries = xml_tree.findall(f'.//entry')
    # Discard multi-word entries.
    single_entries = [e for e in entries if len(get_lexical_unit_text(e).split()) == 1]
    # Discard non-word entries.
    non_letters = ['*', '-', 'a', 'a-']
    word_entries = [
        e for e in single_entries if (
            get_lexical_unit_text(e)[0] not in non_letters and get_lexical_unit_text(e)[:2] not in non_letters
        )
    ]
    return word_entries

def get_lexical_unit_text(entry):
    return entry.findall(f"./lexical-unit/form/text")[0].text

def get_entry_data(entry):
    """
    return:
        - ./lexical-unit/form[@lang=sg]/text
        - [senses]
            - ./sense/grammatical-info[@value=*]
    """
    g_info = [g.values()[0] for g in entry.findall(f".//grammatical-info[@value]")]
    g_info = list(set(g_info)) # remove dupes
    return {get_lexical_unit_text(entry): g_info}

def pretty_print_xml(xml_tree):
    print(
        etree.tostring(
            xml_tree, encoding='UTF-8', pretty_print=True, xml_declaration=True
        ).decode().rstrip()
    )

def main():
    if len(sys.argv) > 1:
        lift_file = Path(sys.argv[1]).expanduser().resolve()
    else:
        print(f"ERROR: Need to pass LIFT file as 1st argument.")
        exit(1)

    cmd = None
    if len(sys.argv) > 2:
        cmd = sys.argv[2]

    xml = get_xml_tree(lift_file)

    if cmd == 'xml':
        pretty_print_xml(xml)
    elif cmd == 'entries':
        for e in get_lift_entries(xml):
            print(get_entry_data(e))
    elif cmd is None:
        # Write output file.
        outfile = Path('lexicon.txt')
        entries = get_lift_entries(xml)
        wordlist = [list(get_entry_data(e).keys())[0] for e in entries]
        wordlist = list(set(wordlist)) # remove dupes
        wordlist.sort()
        data = []
        for w in wordlist:
            for e in entries:
                entry_data = get_entry_data(e)
                if list(entry_data.keys())[0] == w:
                    data.append(entry_data)
                    break
        with outfile.open('w') as f:
            for d in data:
                for k, v in d.items():
                    if v:
                        f.write(f"{k}\t{' '.join(v)}\n")
                    else:
                        f.write(f"{k}\n")

if __name__ == '__main__':
    main()
