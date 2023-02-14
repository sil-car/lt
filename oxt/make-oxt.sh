#!/bin/bash

# REF:
#   - https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
#   - https://www.systutorials.com/docs/linux/man/4-hunspell/
#   - $ man 5 hunspell
#   - $ man hunspell
#   - $ hunspell -h

today=$(date +%Y-%m-%d)
langtag='sg-CF'
lang='sango'
ver='0.1'
if [[ -n "$1" ]]; then
    name=$(basename "$1")
    langtag=$(echo "$name" | awk -F'_' '{print $1}')
    lang=$(echo "$name" | awk -F'_' '{print $2}')
    all_txt=$(ls "$name" | grep 'all_.*\.txt')
    ver_fmt=$(echo "$all_txt" | awk -F'_' '{print $2}')
    ver="${ver_fmt%.*}"
fi

makeoxt \
    -d ./"${name}/${all_txt}" \
    -l "$lang" \
    -t west \
    -v "$ver" \
    "$langtag" ./"${name}/${lang}-dictionnaire-${today}.oxt"
