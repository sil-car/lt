#!/bin/env python3

# Update target DB with entries in source DB.
#
# Use 2 FLEx database SFM exports:
#   source.db (LWC)
#   target.db (minority language)

import argparse
import sys

from pathlib import Path


def import_sfm_to_dict(file):
    data_dict = {
        'meta-data': {}
    }
    lx_lan = '\lx_'
    hm_key = f"\hm 1"
    sn_key = f"\sn 1"

    with file.open() as f:
        lines = f.readlines()

    lines_dict = {}
    for i, l in enumerate(lines):
        # Update lx_lan variable from file entries.
        if l[:4] == '\lx_':
            lx_lan = l.split()[0]
        lines_dict[i] = l

    # Add meta-data to dictionary.
    data_dict['meta-data']['lx_lan'] = lx_lan

    for i, l in lines_dict.items():
        # print(f"{lx_lan}[{i+1}]: \"{l}\" ({get_unicode(l)})")
        # List of placeholders used in databases when data is not available.
        placeholders = [
            None,
            '??',
        ]

        # Ignore lines not starting with '\'.
        if l[0] != '\\':
            continue

        # Parse line's data.
        data = l.split()
        tag = data[0]
        text = ' '.join(data[1:])

        # Add entry to dict if tag is '\lx'.
        if tag == '\lx':
            if not text or text in placeholders:
                text = f"empty[{i}]"
            lx_key = f"{tag} {text}"
            lx_lan_key = f"{lx_lan} {text}"
            hm_key = '\hm 1'
            sn_key = '\sn 1'
            if not data_dict.get(lx_key):
                data_dict[lx_key] = {
                    lx_lan_key: {
                        hm_key: {
                            sn_key: {}
                        }
                    }
                }

        elif tag[:4] == '\lx_':
            if not text or text in placeholders:
                text = f"empty[{i}]"
            lx_lan_key = f"{tag} {text}"
            # Ensure lx_lan_key.
            if not data_dict.get(lx_key).get(lx_lan_key):
                data_dict[lx_key][lx_lan_key] = {
                    hm_key: {
                        sn_key: {}
                    }
                }

        elif tag == '\hm':
            # Ensure hm_key.
            hm_key = f"{tag} {text}"
            if not data_dict.get(lx_key).get(lx_lan_key).get(hm_key):
                data_dict[lx_key][lx_lan_key][hm_key] = {
                    sn_key: {}
                }

        elif tag == '\sn':
            # Ensure sn_key.
            sn_key = f"{tag} {text}"
            if not data_dict.get(lx_key).get(lx_lan_key).get(hm_key).get(sn_key):
                data_dict[lx_key][lx_lan_key][hm_key][sn_key] = {}

        else:
            # Update data_dict info.
            data_dict[lx_key][lx_lan_key][hm_key][sn_key][tag] = text

    return data_dict

def get_item_path(nested_dict, value, prepath=None):
    if prepath is None:
        prepath = []
    for k, v in nested_dict.items():
        path = prepath.append(k)
        if v == value: # found value
            return path
        elif hasattr(v, 'items'): # v is a dict
            p = get_item_path(v, value, path) # recursive call
            if p is not None:
                return p

def get_unicode(text):
    unicode = "".join(map(lambda c: rf"\u{ord(c):04x}", text))
    return unicode

def get_lang_name(langs_dict, g_lan_string):
    for lg, names in langs_dict.items():
        if g_lan_string in names:
            return lg
    return None

def get_g_lan_string(langs_dict, lang, target_dict):
    # print(f"Get g_lan_string for {lang}")
    for lx, lx_v in target_dict.items():
        for lx_lan, lx_lan_v in lx_v.items():
            for hm, hm_v in lx_lan_v.items():
                for sn, sn_v in hm_v.items():
                    for k, v in sn_v.items():
                        if k[:3] == '\g_' and get_lang_name(langs_dict, k) == lang:
                            return(k)
    return langs_dict[lang][0]

def get_lx_lan_string(langs_dict, file):
    pass

def filter_dict_entries(full_dict):
    # Remove entries that don't contain \z0 or \g_San
    filtered_dict = full_dict.copy()
    for e, v in full_dict.items():
        keep = False
        for vk, vv in v.items():
            if vk[:2] == 'sn':
                # print(vv)
                # exit()
                if vv.get('\z0') and vv.get('\g_San'):
                    keep = True
                    continue
        if not keep:
            filtered_dict.pop(e, None)

    # print(len(full_dict))
    # print(len(filtered_dict))
    return filtered_dict

def export_dict_to_sfm(data_dict):
    sfm_lines = []
    data_dict.pop('meta-data', None)
    sorted_entries = sorted(data_dict.keys())
    for lx in sorted_entries:
        # sfm_lines.append('\n')
        sfm_lines.append(f"\n{lx}")
        for lx_lan, lx_lan_v in data_dict.get(lx).items():
            sfm_lines.append(lx_lan)
            for hm, hm_v in lx_lan_v.items():
                sfm_lines.append(hm)
                for sn, sn_v in hm_v.items():
                    sfm_lines.append(sn)
                    for k, v in sn_v.items():
                        sfm_lines.append(f"{k} {v}")
    return sfm_lines

def update_dict(source_dict, target_dict, langs):

    def print_new_glosses(cawl_id, target_lx, target_gloss, source_lx_list):
        print(f"Target \lx: {target_lx}")
        print(f"Sango gloss in Gbeya DB: {target_gloss}")
        print(f"CAWL ID: {cawl_id}")
        print(f"Sango lexemes in Sango DB: {'; '.join(sorted(source_lx_list))}\n")

    tmeta = target_dict.pop('meta-data')
    smeta = source_dict.pop('meta-data')
    updated_target_dict = target_dict.copy()

    tlx_lan = tmeta['lx_lan']
    slx_lan = smeta['lx_lan']

    # Get tg_lan variable from slx_lan.
    slang_string = slx_lan.split('_')[1]
    slx_lan_name = get_lang_name(langs, f"\g_{slang_string}")
    tg_lan = get_g_lan_string(langs, slx_lan_name, target_dict)

    for tlx_v in target_dict.values():
        # Get CAWL IDs and glosses for this entry in target database.
        glosses_init = {}
        for tlx_lan_v in tlx_v.values():
            for thm_v in tlx_lan_v.values():
                for tsn_v in thm_v.values():
                    cawl_id = tsn_v.get('\z0')
                    if cawl_id:
                        glosses_init[cawl_id] = tsn_v.get(tg_lan)
                        # print(tg_lan, tlx_v)

        # Check for corresponding CAWL IDs in source database.
        glosses_new = []
        for id, gloss in glosses_init.items():
            # Loop through entries in source database.
            for slx, slx_v in source_dict.items():
                # Loop through entry values in each source database entry.
                for slx_lan, slx_lan_v in slx_v.items():
                    for shm, shm_v in slx_lan_v.items():
                        for ssn, ssn_v in shm_v.items():
                            sid = ssn_v.get('\z0')
                            if sid == id and slx != gloss:
                                gtext = ' '.join(slx.split()[1:])
                                glosses_new.append(gtext)

        # Update glosses in target DB.
        ug_lan = tg_lan
        if glosses_new:
            # print_new_glosses(id, tlx, gloss, glosses_new)
            for ulx, ulx_v in updated_target_dict.items():
                for ulx_lan, ulx_lan_v in ulx_v.items():
                    for uhm, uhm_v in ulx_lan_v.items():
                        for usn, usn_v in uhm_v.items():
                            if usn_v.get('\z0', 'not given') == cawl_id:
                                updated_target_dict[ulx][ulx_lan][uhm][usn][ug_lan] = ' ; '.join(sorted(list(set(glosses_new))))
    # print(updated_target_dict)
    return updated_target_dict

def sort_file(target_file):
    target_dict = import_sfm_to_dict(target_file)
    sfm_lines = export_dict_to_sfm(target_dict)
    print('\r\n'.join(sfm_lines))

def update_file(source_file, target_file, langs):
    # Parse file contents into dicts.
    source_dict = import_sfm_to_dict(source_file)
    target_dict = import_sfm_to_dict(target_file)

    # Check for updated glosses in source DB.
    updated_target_dict = update_dict(source_dict, target_dict, langs)

    # Export dict to SFM.
    sfm_lines = export_dict_to_sfm(updated_target_dict)
    # print(sfm_lines)

    # Create updated target file, preserving original.
    outfile_name = f"{target_file.stem}-updated.db"
    outfile = target_file.with_name(outfile_name)
    with open(outfile, mode='w') as f:
        for l in sfm_lines:
            f.write(f"{l}\r\n")

    print(f"Updated file saved as \"{outfile}\"")

def main():
    # Reference for determining lx_lan tags.
    langs = {
        'sg': ['\g_San', '\g_sg'],
        'en': ['\g_Eng', '\g_en'],
        'fr': ['\g_Fra', '\g_fr', '\g_Frn'],
    }

    # Define arguments and options.
    parser = argparse.ArgumentParser(
        description="Sort or update FLEx database files in SFM format.",
    )
    parser.add_argument(
        "source_db",
        nargs='?',
        help="The source file to get updates from.",
    )
    parser.add_argument(
        "target_db",
        nargs='+',
        help="The target file(s) to be updated.",
    )
    args = parser.parse_args()

    # Parse script arguments.
    if args.source_db: # updating target file
        source_file = Path(args.source_db).resolve()
        target_files = [Path(f).resolve() for f in args.target_db]
        file_list = '\n'.join([str(f) for f in target_files])
        print(f"Taking lexemes from \"{source_file}\" to update glosses in:\n{file_list}")
        for target_file in target_files:
            update_file(source_file, target_file, langs)
    else: # sort 1st file given on stdout
        sort_file(Path(args.target_db[0]))


if __name__ == '__main__':
    main()
