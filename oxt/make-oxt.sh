#!/bin/bash

# REF:
#   - https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
#   - https://www.systutorials.com/docs/linux/man/4-hunspell/
#   - $ man 5 hunspell
#   - $ man hunspell
#   - $ hunspell -h

today=$(date +%Y%m%d)
ver=$(date +%Y.%m.%d)
langtag='sg-CF'
lang='sango'
if [[ -n "$1" ]]; then
    name=$(basename "$1")
    langtag=$(echo "$name" | awk -F'_' '{print $1}')
    lang=$(echo "$name" | awk -F'_' '{print $2}')
    infile=$(ls "$name" | grep 'all_.*\.txt')
    if [[ -n "$2" ]]; then
        echo "Doesn't work yet with nested files."
        exit 1
        if [[ ${2##*.} == 'aff' ]]; then
            # Make OXT from passed AIF/DIC files.
            infile="$2"
        fi
    fi
fi

makeoxt \
    -d ./"${name}/${infile}" \
    -l "$lang" \
    -t west \
    -v "$ver" \
    "$langtag" ./"${name}/dict-${lang}-${today}_lo.oxt"
