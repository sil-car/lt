#!/bin/bash

if [[ -z "$1" || "${1##*.}" != 'txt' ]]; then
    echo "USAGE: $0 WORDLIST.txt"
    exit 1
fi

# Ensure that wordlist has unique entries.
words=$(cat "$1" | sort -u)
word_ct=$(echo "$words" | wc -l)
echo "$word_ct" > wordlist.dic
echo "$words" >> wordlist.dic
