#!/usr/bin/env python3

"""
1. Add verse numbers to songbook SFM file.
    This only works with prepared files where the verse line begins like this:
    \\v  Verse text that follows two spaces, which immediately follow \\v marker.
    It inserts the correct verse number in between the two spaces described above.
2. Ensure choruses are repeated after each verse.
3. Set chorus SFM as /q2.
"""
# TODO: Consider adding:
# - Insert song number on own line after song title.

import argparse
import re
import sys
import unicodedata

from pathlib import Path


def strip_non_printables(input_lines):
    output_lines = []
    all_chars = (chr(i) for i in range(sys.maxunicode))
    control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
    control_char_re = re.compile(f"[{re.escape(control_chars)}]")
    for input_line in input_lines:
        line = control_char_re.sub('', input_line)
        output_lines.append(line + '\n') # add newlines back in
    return output_lines

def get_first_letter_indexes(s):
    indexes = [0]
    separators = ' -'
    for i, c in enumerate(s):
        if i == len(s) - 1:
            break
        if c in separators:
            indexes.append(i+1)
    return indexes

def get_sfm(line):
    if line[0] == '\\':
        sfm = line.split()[0]
    else:
        sfm = None
    # print(f"sfm: {sfm}\nline[0]: \"{line[0]}\"")
    return sfm

def set_sfm(line, new_sfm):
    terms = line.split(' ')
    if terms[0][0] == '\\': # update existing SFM
        terms[0] = new_sfm
    else: # insert SFM at beginning
        terms.insert(0, new_sfm)
    return ' '.join(terms)

def get_sfm_data_int(line):
    data_int = None
    sfm = get_sfm(line)
    if sfm == '\c' or sfm == '\\v':
        try:
            data_int = int(line.split(' ')[1])
        except ValueError: # not a number
            pass
    return data_int

def get_songs(lines):
    songs = {}
    song_number = None
    for line in lines:
        sfm = get_sfm(line)
        if sfm == '\id': # 1st line of file
            song_number = 0
            songs[song_number] = []
        elif sfm == '\c': # start of song
            song_number = get_sfm_data_int(line)
            songs[song_number] = []
        if song_number is None:
            continue
        songs[song_number].append(line)
    return songs

def get_text_blocks(song_number, lines):
    # Text blocks are a series of lines beginning with \q1,
    #   followed by other \q1 markers or \v markers.
    blocks = []
    block_number = None
    for i, line in enumerate(lines):
        sfm = get_sfm(line)
        prev_sfm = None
        next_sfm = None
        if i > 0:
            prev_sfm = get_sfm(lines[i-1])
        if i < len(lines)-1:
            next_sfm = get_sfm(lines[i+1])
        if sfm == '\c' and not block_number: # start of the title block
            block_number = 0
            blocks.append({
                'type': 'title',
                'lines': [],
            })
        elif sfm == '\q1' and len(line.split()) == 1: # start of verse block
            block_number += 1

            blocks.append({
                'type': 'verse',
                'lines': [],
            })
        elif ( sfm == '\q1' and prev_sfm != '\q1' and prev_sfm != '\\v' ) or ( sfm == '\q2' and prev_sfm != '\q2' ): # start of chorus block
            block_number += 1
            blocks.append({
                'type': 'chorus',
                'lines': []
            })
        blocks[block_number]['lines'].append(line)

    # Ensure correct chorus SFMs.
    output_blocks = []
    for block in blocks:
        if block.get('type') == 'chorus':
            # print(f"updating block {block}")
            block['lines'] = ensure_chorus_sfm(block.get('lines'))
        output_blocks.append(block)

    # print(output_blocks)
    return output_blocks

def ensure_chorus_sfm(chorus_lines):
    output_chorus_lines = chorus_lines.copy()
    for i, line in enumerate(chorus_lines):
        if get_sfm(line) != '\q1':
            continue
        output_chorus_lines[i] = set_sfm(line, '\q2')
    return output_chorus_lines

def ensure_verse_numbers(input_lines):
    v = 1 # initialize verse number
    output_lines = input_lines.copy()
    for i, line in enumerate(input_lines):
        sfm = get_sfm(line)
        # print(f"{i}: {line.rstrip()}")
        if sfm == '\c': # start of new "chapter"/song
            # print(f"Start of next song")
            v = 1
        elif sfm == '\\v':
            # print(f"Start of next verse")
            # if line[:4] == '\\v  ':
            verse_number = get_sfm_data_int(line)
            if not verse_number:
                print(f"{i}: Inserting verse number \"{v}\"")
                # line = f"\\v {v} {line[4:]}"
                terms = line.split()
                terms.insert(1, str(v))
                line = ' '.join(terms)
                v += 1
            # elif line[3] == str(v): # verse already correctly numbered
            elif verse_number == v: # verse already correctly numbered
                # print(f"Verse number already correct.")
                v += 1
            else: # wrong verse number
                print(f"{i}: Correcting verse number \"{verse_number}\" to \"{v}\"")
            # elif line[3] != ' ': # verse malformed
            #     print(f"ERROR: Bad line format.")
        output_lines[i] = line
    return output_lines

def ensure_repeated_choruses(songs):
    output_lines = [songs[0][0]]
    for n, lines in songs.items():
        if n == 0:
            continue
        text_blocks = get_text_blocks(n, lines)
        text_blocks_out = text_blocks.copy()
        chorus_data = None
        for block_data in text_blocks:
            if block_data.get('type') == 'chorus':
                chorus_data = block_data
        if chorus_data:
            for i, block_data in enumerate(text_blocks):
                try:
                    next_block_data = text_blocks[i+1]
                except IndexError:
                    next_block_data = None
                next_block_type = next_block_data.get('type') if next_block_data else None
                if block_data.get('type') == 'verse' and next_block_type != 'chorus': # insert chorus
                    # Determine insertion index by position from end of original list.
                    insertion_index = i-len(text_blocks)+1
                    if insertion_index == 0: # use end position of new list
                        insertion_index = len(text_blocks_out)
                    # print(f"Song: {n}; inserting chorus to index {insertion_index}")
                    text_blocks_out.insert(insertion_index, chorus_data)
        for text_block in text_blocks_out:
            output_lines.extend(text_block.get('lines'))
    return output_lines

def ensure_title_case(input_lines):
    output_lines = input_lines.copy()
    for i, line in enumerate(input_lines):
        if get_sfm(line) == '\s': # all titles are assumed to be \s lines
            # text = line.split()[1:]
            # updated_text = ['\s']
            updated_line = ''
            j_firsts = get_first_letter_indexes(line)
            for j, c in enumerate(line):
                if j not in j_firsts:
                    c = c.lower()
                updated_line += c
            output_lines[i] = updated_line
    return output_lines

def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "infile",
        metavar="infile",
        nargs=1,
        help="the file to be cleaned up",
    )
    p.add_argument(
        "-c", "--choruses",
        action="store_true",
        help="ensure choruses use \q2 SFM markers and put the chorus after every verse",
    )
    p.add_argument(
        "-n", "--verse-numbers",
        action="store_true",
        help="ensure accurate verse numbering",
    )
    p.add_argument(
        "-t", "--titles",
        action="store_true",
        help="ensure song titles use Title Case",
    )
    args = p.parse_args()

    # Handle commandline arguments
    if not args.verse_numbers and not args.choruses and not args.titles:
        print(f"error: Please pass at least one option.")
        p.print_help()
        exit(1)

    infile = Path(args.infile[0]) # only 1 infile allowed
    outfile = infile.with_suffix('.mod.sfm')
    with infile.open() as f:
        original_lines = f.readlines()

    # Always strip non-printable characters.
    lines = strip_non_printables(original_lines)

    if args.verse_numbers:
        lines = ensure_verse_numbers(lines)

    if args.choruses:
        lines = ensure_repeated_choruses(get_songs(lines))

    if args.titles:
        lines = ensure_title_case(lines)

    # Write out new file.
    outfile.write_text(''.join(lines))

if __name__ == '__main__':
    main()
