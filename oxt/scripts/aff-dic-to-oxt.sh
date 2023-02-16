#!/bin/bash

# REF:
#   - https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
#   - https://www.systutorials.com/docs/linux/man/4-hunspell/
#   - $ man 5 hunspell
#   - $ man hunspell
#   - $ hunspell -h

script_path="$(realpath "$0")"
script_dir_path="$(dirname "$script_path")"
aff_dir="$PWD"

today=$(date +%Y%m%d)
ver=$(date +%Y.%m.%d)

name=$(basename "$aff_dir")
langtag=$(echo "$name" | awk -F'_' '{print $1}')
lang=$(echo "$name" | awk -F'_' '{print $2}')

makeoxt \
    -d "${langtag}.aff" \
    -l "$lang" \
    -t west \
    -v "$ver" \
    "$langtag" ./"dict-${lang}-${today}_lo.oxt"
