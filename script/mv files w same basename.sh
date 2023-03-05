#!/usr/bin/env bash

echo "Moving files from $1 to $2."
read
comm --nocheck-order -12 \
<(ls $1 | sed -E 's/[.][a-z0-9]+$//g; s/【thumb】$//g') \
<(ls $2 | sed -E 's/[.][a-z0-9]+$//g; s/【thumb】$//g') \
| while read file
do
	#mv -nv "$1/$file".* "$2"
	mv -nv "$1/$file【thumb】".* "$2"
done