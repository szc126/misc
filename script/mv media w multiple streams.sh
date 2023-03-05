#!/usr/bin/env zsh

alias ffprobe-json='command ffprobe -v quiet -hide_banner -print_format json -show_format'

echo "Moving files from $1 to $2."
read
for file in $1; do; if (( $(ffprobe-json $file|jq .format.nb_streams) > 1 )); then; mv -vn $file $2; else; echo pass $file; fi; done