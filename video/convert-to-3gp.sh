#!/usr/bin/env bash

# H263 resolution options:
# 128 x 96
# 176 x 144
# 352 x 288
# 704 x 576
# 1408 x 1152

# ffmpeg rotation ("transpose") options:
# 0 = 90° counterclockwise and vertical flip (default)
# 1 = 90° clockwise
# 2 = 90° counterclockwise
# 3 = 90° clockwise and vertical flip

framerate=23  # fps
usage="usage: $0 FILE.MP4"
scale="176:144"
scale="352:288"
scale="704:576"
transpose=-1
if [[ $1 == '-h' || $1 == '--help' ]]; then
    echo "$usage"
    echo -e "\nOUTFILE will be saved to $PWD"
    exit 0
elif [[ $1 == p ]]; then
    scale="144:176"
    scale="288:352"
    scale="576:704"
    transpose=2
    shift
elif [[ -z "$1" ]]; then
    echo "$usage"
    exit 1
fi

for infile in "${@}"; do
    filename="$(basename "$infile")"
    filestem="${filename%.*}"
    if [[ $transpose == '-1' ]]; then
        vf="scale=${scale}:force_original_aspect_ratio=1,pad=${scale}:(ow-iw)/2:(oh-ih)/2"
    else
        vf="scale=${scale}:force_original_aspect_ratio=1,pad=${scale}:(ow-iw)/2:(oh-ih)/2,transpose=${transpose}"
    fi
    ffmpeg -i "$infile" \
        -vf "$vf" \
        -r "$framerate" -ar 8000 -ab 4750 -ac 1 \
        "${filestem}.3gp"
done