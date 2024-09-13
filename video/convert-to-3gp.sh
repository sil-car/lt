#!/usr/bin/env bash

framerate=23  # fps
usage="usage: $0 FILE.MP4"
if [[ $1 == '-h' || $1 == '--help' ]]; then
    echo "$usage"
    echo -e "\nOUTFILE will be saved to $PWD"
    exit 0
elif [[ -z "$1" ]]; then
    echo "$usage"
    exit 1
fi

for infile in "${@}"; do
    filename="$(basename "$infile")"
    filestem="${filename%.*}"
    ffmpeg -i "$infile" \
        -vf "scale=176:144:force_original_aspect_ratio=1,pad=176:144:(ow-iw)/2:(oh-ih)/2" \
        -r "$framerate" -ar 8000 -ab 4750 -ac 1 \
        "${filestem}.3gp"
done