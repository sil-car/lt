#!/bin/bash

if [[ -z "$1" || ! -d "$1" ]]; then
    echo "USAGE: $0 BASE_DIR"
    exit 1
fi

base_dir="${1%/}" # remove trailing slash
find -L "${base_dir}/" -iname '*-wordlist.txt' -exec cat {} + | sort -u > "${base_dir}/wordlist.txt"
