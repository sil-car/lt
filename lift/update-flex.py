#!/bin/env python3

"""
Update target DB with entries in source DB.

Use 2 FLEx database SFM exports:
- source.db (LWC)
- target.db (minority language)
"""

import argparse
import time

from pathlib import Path
from lxml import etree


def get_xml_tree(file_object):
    # Remove existing line breaks to allow pretty_print to work properly later.
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(file_object, parser)

def get_lx_text_for_sense(sense):
    return sense.getparent().find('lexical-unit').find('form').find('text').text

def get_cawl_from_field(field):
    cawl = None
    if field.get('type') == 'CAWL':
        cawl = field.find('form').find('text').text
    return cawl

def get_cawls(xml_tree):
    cawls = []
    fields = xml_tree.findall('.//field[@type]')
    for field in fields:
        cawl = get_cawl_from_field(field)
        if cawl:
            cawls.append(cawl)
    cawls = list(set(cawls))
    return cawls

def get_glosses(xml_tree, cawl_str):
    glosses = []
    fields = xml_tree.findall('.//field[@type]')
    for field in fields:
        cawl = get_cawl_from_field(field)
        if cawl == cawl_str:
            gloss = get_lx_text_for_sense(field.getparent())
            glosses.append(gloss)

    return glosses

def update_gloss(xml_tree, cawl_str, lang, glosses):
    """Update an existing gloss field or add a new gloss field in the given XML tree."""
    fields = xml_tree.findall('.//field[@type]')
    for field in fields:
        if field.get('type') == 'CAWL':
            cawl = field.find('form').find('text').text
            if cawl == cawl_str:
                sense = field.getparent()
                lx_text = get_lx_text_for_sense(sense)
                gloss_exists = False
                for g in sense.findall('gloss'):
                    if g.get('lang') == lang:
                        g_lang = g.find('text')
                        gloss_exists = True
                        break
                if gloss_exists:
                    # Update existing gloss.
                    # print(f"Need to update gloss for {lang} in {cawl_str} of sense {sense.get('id')} in {lx_text}")
                    g_lang.text = ' ; '.join(glosses)
                else:
                    # Create new gloss.
                    # print(f"Need new gloss for: {lang} in {cawl_str} of sense {sense.get('id')} in {lx_text}")
                    gloss = etree.SubElement(sense, 'gloss')
                    gloss.attrib['lang'] = lang
                    gloss_text = etree.SubElement(gloss, 'text')
                    gloss_text.text = ' ; '.join(glosses)

    return xml_tree

def get_unicode(text):
    unicode = "".join(map(lambda c: rf"\u{ord(c):04x}", text))
    return unicode

def get_lx_lang(xml_entry):
    return xml_entry.find('lexical-unit').find('form').get('lang', None)

def get_outfile_object(old_file_obj):
    new_file_name = f"{old_file_obj.stem}-updated.lift"
    new_file_obj = old_file_obj.with_name(new_file_name)
    return(new_file_obj)

def save_xml_to_file(xml_tree, infile_path):
    outfile = get_outfile_object(infile_path)
    xml_tree.write(outfile, encoding='UTF-8', pretty_print=True, xml_declaration=True)
    print(f"Updated file saved as \"{outfile}\"")

def update_file(lang, source_xml, target_xml, target_file):
    target_cawls = get_cawls(target_xml)
    # g_times = []
    # u_times = []
    for cawl in target_cawls:
        print('.', end='', flush=True)
        # gs = time.perf_counter()
        updated_glosses = get_glosses(source_xml, cawl)
        # ge = time.perf_counter()
        # g_times.append(ge - gs)
        # us = time.perf_counter()
        target_xml = update_gloss(target_xml, cawl, lang, updated_glosses)
        # ue = time.perf_counter()
        # u_times.append(ue - us)
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
    args = parser.parse_args()

    # Parse script arguments.
    if args.source_db: # update target file(s)
        # Gather source file data.
        source_file = Path(args.source_db).resolve()
        source_xml = get_xml_tree(source_file)
        lang = get_lx_lang(source_xml.findall('entry')[0])

        # Gather target files.
        target_files = [Path(f).resolve() for f in args.target_db]
        file_list = '\n'.join([str(f) for f in target_files])

        # Process files.
        print(f"Taking \"{lang}\" lexemes from \"{source_file}\" to update glosses in:\n{file_list}")
        for target_file in target_files:
            target_xml = get_xml_tree(target_file)
            update_file(lang, source_xml, target_xml, target_file)

    else: # print 1st file given to stdout
        target_xml = get_xml_tree(Path(args.target_db[0]))
        print(etree.tostring(target_xml, encoding='UTF-8', pretty_print=True, xml_declaration=True).decode())


if __name__ == '__main__':
    main()
