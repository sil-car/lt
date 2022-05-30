#!/bin/env python3

"""
Update target LIFT file(s) with entries in source LIFT file.

Use 2 FLEx database LIFT exports:
- source.lift (LWC)
- target.lift (minority language)
- [target.lift...]
"""

import argparse
import datetime
import sys
import time

from pathlib import Path
from lxml import etree

SOURCE_CAWL_TYPE = ''
TARGET_CAWL_TYPE = ''
DEBUG = False

def verify_venv():
    bin_dir = Path(sys.prefix)
    if bin_dir.name == 'usr':
        script_dir = Path(__file__).parent
        env_full_path = script_dir.resolve() / 'env'
        if env_full_path.is_dir():
            activate_path = env_full_path / 'bin' / 'activate'
        else:
            print(f"ERROR: Virtual environment not found at \"{env_full_path}\"")
            exit(1)
        # Virtual environment not activated.
        print("ERROR: Need to activate virtual environment:")
        print(f"$ . {activate_path}")
        exit(1)

def get_xml_tree(file_object):
    # Remove existing line breaks to allow pretty_print to work properly later.
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(file_object, parser)

def get_lx_text_for_sense(sense):
    entry = sense.getparent()
    lexical_unit = entry.find('lexical-unit')
    form = lexical_unit.find('form')
    lx_text = form.find('text')
    return lx_text.text

def get_cawl_from_field(field, cawl_type):
    cawl = None
    if field.get('type') == cawl_type:
        cawl = field.find('form').find('text').text
    return cawl

def get_cawls(xml_tree, cawl_type):
    cawls = []
    fields = xml_tree.findall('.//field[@type]')
    for field in fields:
        cawl = get_cawl_from_field(field, cawl_type)
        if cawl:
            cawls.append(cawl)
    cawls = list(set(cawls))
    return cawls

def get_glosses(xml_tree, cawl_str, cawl_type):
    glosses = []
    fields = xml_tree.findall('.//field[@type]')
    for field in fields:
        cawl = get_cawl_from_field(field, cawl_type)
        if cawl == cawl_str:
            gloss = get_lx_text_for_sense(field.getparent())
            # if DEBUG:
            #     print(f"{gloss=}")
            glosses.append(gloss)

    return glosses

def update_gloss(xml_tree, cawl_str, lang, glosses):
    """Update an existing gloss field or add a new gloss field in the given XML tree."""
    fields = xml_tree.findall('.//field[@type]')
    for field in fields:
        if field.get('type') == TARGET_CAWL_TYPE:
            cawl = field.find('form').find('text').text
            # if DEBUG:
            #     print(f"{cawl=}")
            if cawl == cawl_str:
                sense = field.getparent()
                entry = sense.getparent()
                gloss_exists = False
                for g in sense.findall('gloss'):
                    if g.get('lang') == lang:
                        g_lang = g.find('text')
                        gloss_exists = True
                        break
                if gloss_exists:
                    # Update existing gloss.
                    g_lang.text = ' ; '.join(glosses)
                else:
                    # Create new gloss.
                    gloss = etree.SubElement(sense, 'gloss')
                    gloss.attrib['lang'] = lang
                    gloss_text = etree.SubElement(gloss, 'text')
                    gloss_text.text = ' ; '.join(glosses)
                update_timestamp_for_entry(entry)

    return xml_tree

def update_timestamp_for_entry(entry):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    timestamp = now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
    entry.attrib['dateModified'] = timestamp

def get_unicode(text):
    unicode = "".join(map(lambda c: rf"\u{ord(c):04x}", text))
    return unicode

def get_lx_lang(xml_entry):
    return xml_entry.find('lexical-unit').find('form').get('lang', None)

def get_outfile_object(old_file_obj):
    new_file_name = f"{old_file_obj.stem}-updated.lift"
    new_file_obj = old_file_obj.with_name(new_file_name)
    return new_file_obj

def save_xml_to_file(xml_tree, infile_path):
    outfile = get_outfile_object(infile_path)
    xml_tree.write(outfile, encoding='UTF-8', pretty_print=True, xml_declaration=True)
    print(f"Updated file saved as \"{outfile}\"")

def update_file(lang, source_xml, target_xml, target_file):
    target_cawls = get_cawls(target_xml, TARGET_CAWL_TYPE)
    # if DEBUG:
    #     print(f"{target_cawls=}")
    # g_times = []
    # u_times = []
    for cawl in target_cawls:
        if DEBUG:
            print(f"{cawl=}")
        else:
            print('.', end='', flush=True)
        # gs = time.perf_counter()
        source_glosses = get_glosses(source_xml, cawl, SOURCE_CAWL_TYPE)
        if DEBUG:
            print(f"{source_glosses=}")
        # ge = time.perf_counter()
        # g_times.append(ge - gs)
        # us = time.perf_counter()
        target_xml = update_gloss(target_xml, cawl, lang, source_glosses)
        # ue = time.perf_counter()
        # u_times.append(ue - us)
    if not DEBUG:
        print()
    # print(f"times: get: {sum(g_times)/len(g_times)}; upd: {sum(u_times)/len(u_times)}")

    # Create updated target file, preserving original.
    save_xml_to_file(target_xml, target_file)

def main():
    # Define arguments and options.
    parser = argparse.ArgumentParser(
        description="Show or update FLEx database files in LIFT format.",
    )
    parser.add_argument(
        "source_db",
        nargs='?',
        help="The source file to get updates from.",
    )
    parser.add_argument(
        "target_db",
        nargs='+',
        help="The target file(s) to be shown or updated.",
    )
    parser.add_argument(
        '-s', '--source-cawl-type',
        help="The value used in the source's 'type' attribute to designate a CAWL entry. [CAWL]",
    )
    parser.add_argument(
        '-t', '--target-cawl-type',
        help="The value used in the target's 'type' attribute to designate a CAWL entry. [CAWL]",
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
    )
    args = parser.parse_args()

    # Verify virtual environment.
    verify_venv()

    # Set debug mode.
    global DEBUG
    DEBUG = True if args.debug else False

    # Parse script arguments.
    if args.source_db: # update target file(s)
        # Set 'type' attribute for CAWL entries.
        global SOURCE_CAWL_TYPE
        SOURCE_CAWL_TYPE = args.source_cawl_type if args.source_cawl_type else 'CAWL'
        global TARGET_CAWL_TYPE
        TARGET_CAWL_TYPE = args.target_cawl_type if args.target_cawl_type else 'CAWL'
        if DEBUG:
            print(f"{SOURCE_CAWL_TYPE=}")
            print(f"{TARGET_CAWL_TYPE=}")

        # Gather source file data.
        source_file = Path(args.source_db).resolve()
        source_xml = get_xml_tree(source_file)
        lang = get_lx_lang(source_xml.findall('entry')[0])
        if DEBUG:
            print(f"{lang=}")

        # Gather target files.
        target_files = [Path(f).resolve() for f in args.target_db]
        file_list = '\n'.join([str(f) for f in target_files])

        # Process files.
        print(f"Taking \"{lang}\" lexemes from \"{source_file}\" to update glosses in:\n{file_list}")
        for target_file in target_files:
            if DEBUG:
                print(f"{target_file=}")
            target_xml = get_xml_tree(target_file)
            update_file(lang, source_xml, target_xml, target_file)

    else: # print 1st file given to stdout
        target_xml = get_xml_tree(Path(args.target_db[0]))
        print(etree.tostring(target_xml, encoding='UTF-8', pretty_print=True, xml_declaration=True).decode())


if __name__ == '__main__':
    main()
