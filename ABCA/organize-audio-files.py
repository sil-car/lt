#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path


def convert_file_paths(files, testament=None):
    """Convert file paths to the correct flat, sequential format.

    I.e. "./B0#___##_Book_name____SAGCAR.mp3"
    """

    ot_book_abbrevs = [
        "GEN", "EXO", "LEV", "NUM", "DEU",
        "JOS", "JDG", "RUT", "1SA", "2SA",
        "1KI", "2KI", "1CH", "2CH", "EZR",
        "NEH", "EST", "JOB", "PSA", "PRO",
        "ECC", "SNG", "ISA", "JER", "LAM",
        "EZK", "DAN", "HOS", "JOL", "AMO",
        "OBA", "JON", "MIC", "NAM", "HAB",
        "ZEP", "HAG", "ZEC", "MAL",
    ]

    nt_book_idxs = {}
    ct = 0
    for n in range(40, 67):
        ct += 1
        nt_book_idxs[f"B{ct:02d}"] = f"B{n}"

    ct = 0
    ot_book_idxs = {}
    for bk in ot_book_abbrevs:
        ct += 1
        ot_book_idxs[bk] = f"B{ct:02d}"

    new_names = []
    if testament.lower() == 'old':
        for fp in files:
            suf = fp.suffix
            nam, cha = fp.stem.split('_')
            new_name = f"{ot_book_idxs.get(nam)}___{cha}_{nam}____SAGCAR{suf}"
            new_names.append((fp, new_name))
    elif testament.lower() == 'new':
        for fp in files:
            nbk = fp.name.split('___')[0]
            new_name = fp.name.replace(nbk, nt_book_idxs.get(nbk))
            new_names.append((fp, new_name))

    return new_names


def ensure_file_copy(outdir, conversions):
    for op, nn in conversions:
        np = outdir / nn
        if not np.is_file():
            print(f"{op} > {np}...")
            shutil.copy(op, np)


def main():
    # Handle commandline.
    if len(sys.argv) < 2:
        print("Error: Need to pass root directory as 1st argument")
        exit(1)
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print(f"Usage: {sys.argv[0]} /AUDIO/FILE/ROOT/DIR")
        exit()
    else:
        root_dir = Path(sys.argv[1])
        if not root_dir.is_dir():
            print(f"Error: Not a valid directory: {root_dir}")
            exit(1)

    ot_dir = root_dir / 'AT'
    nt_dir = root_dir / 'NT'
    out_dir = root_dir / 'flat'
    out_dir.mkdir(parents=True, exist_ok=True)

    # Begin processing.
    ot_files = (f for f in ot_dir.rglob('*') if f.is_file())
    ot_conversions = convert_file_paths(ot_files, testament='old')
    ensure_file_copy(out_dir, ot_conversions)

    nt_files = nt_dir.iterdir()
    nt_conversions = convert_file_paths(nt_files, testament='new')
    ensure_file_copy(out_dir, nt_conversions)


if __name__ == '__main__':
    main()
