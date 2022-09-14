#!/bin/bash

# Convert PDF of Action Bible pages to a video.
# - Each video frame will be 2 opposing pages from the Action Bible.
# - Each frame will be visible for a reasonable amount of time so that the text
#   can be read.

# Set variables.
DELAY=60 # seconds per frame
HEIGHT=1080 # pixels

if [[ -n "$1" ]]; then
    SRC_DIR="$1"
    DST_DIR="$1"
else
    SRC_DIR="$HOME"
    DST_DIR="$HOME"
fi

if [[ -n "$2" ]]; then
    DST_DIR="$2"
fi


add_leading_zeroes() {
    len=2
    if [[ "$2" -gt 2 ]]; then
        len="$2"
    fi
    printf "%0${len}d" "$1"
}

remove_leading_zeroes() {
    echo "$1" | sed -r 's/0*([0-9]*)/\1/'
}

convert_pdf_to_jpgs() {
    echo -n "Converting PDFs to JPGs..."
    start_dir="$PWD"
    mkdir -p "$1"
    rm -f "$1"/*.jpg

    cd "$1"
    for pdf in "${SRC_DIR}/"*.pdf; do
        echo -n '.'
        range=$(basename "$pdf" | grep -Eo "[0-9]+-[0-9]+")
        start=$(echo "$range" | grep -Eo "^[0-9]+")
        pdftoppm "$pdf" "$start" -jpeg

        # ### TODO: Temp. backstop for testing
        # ((count++))
        # if [[ $count -gt 2 ]]; then
        #     break
        # fi
        # ###
    done
    echo

    # Rename images.
    echo "Renaming JPGs..."
    for jpg in "${pages_dir}/"*.jpg; do
        start_i=$(basename "$jpg" | grep -Eo '^[0-9]+')
        start=$(remove_leading_zeroes "$start_i")
        rel_pg_i=$(echo "$jpg" | sed -r 's/^.*-([0-9]+).jpg/\1/')
        rel_pg=$(remove_leading_zeroes "$rel_pg_i")
        pg_i=$((rel_pg + start - 1))
        # pg=$(printf "%02d" "$pg_i")
        pg=$(add_leading_zeroes "$pg_i" 3)
        # echo "Renaming $(basename $jpg) to $pg.jpg..."
        mv $(basename "$jpg") "${pg}-pdf.jpg"
    done

    cd "$start_dir"
}

concatenate_images() {
    echo -n "Concatenating images..."
    start_dir="$PWD"
    mkdir -p "$2"
    rm -f "$2"/*.jpg
    cd "$2"

    left_side=
    right_side=
    file_list="list.txt"
    > "$file_list"
    find "$1" -iname '*-pdf.jpg' | sort -n | while IFS= read -r jpg; do
        echo "$jpg" >> "$file_list"
        pg_i=$(basename "$jpg" | grep -Eo '[0-9]+')
        pg=$(remove_leading_zeroes "$pg_i")
        mod=$((pg % 2))
        if [[ "$mod" -eq 1 ]]; then
            left_side="$jpg"
        else
            right_side="$jpg"
            num_i=$((pg / 2))
            num=$(add_leading_zeroes "$num_i" 3)
        fi
        if [[ -n "$left_side" && -n "$right_side" ]]; then
            echo -n '.'
            montage "$left_side" "$right_side" -tile 2x1 -geometry +10+10 "frame-${num}.jpg"
            left_side=
            right_side=
        fi
    done
    echo

    cd "$start_dir"
}

# Convert each PDF to a series of JPGs.
pages_dir="${DST_DIR}/pages"
ans=
if [[ -d "$pages_dir" ]]; then
    read -p "Re-convert PDFs to JPGs? [y/N]: " ans
    ans=$(echo "${ans,,}") # force lowercase
fi

if [[ ! -d "$pages_dir" || "$ans" == 'y' ]]; then
    convert_pdf_to_jpgs "$pages_dir"
fi

# Concatenate every pair of images.
frames_dir="${DST_DIR}/frames"
ans=
if [[ -d "$frames_dir" ]]; then
    read -p "Re-concatenate images to frames? [y/N]: " ans
    ans=$(echo "${ans,,}") # force lowercase
fi

if [[ ! -d "$frames_dir" || "$ans" == 'y' ]]; then
    concatenate_images "$pages_dir" "$frames_dir"
fi

# String images together into MP4.
echo "Creating MP4..."
outfile="${DST_DIR}/video.mp4"
cd "$frames_dir"
ffmpeg -y -framerate 1/$DELAY -pattern_type sequence \
    -i "frame-%03d.jpg" -vf "scale=-1:$HEIGHT" "$outfile" >/dev/null 2>&1
echo "$outfile"
cd "$DST_DIR"
