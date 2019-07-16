#!/usr/bin/env bash

folder="$1"
args="-crop 50%x100% +repage"

if [ -z "$folder" ]; then
	echo "Which folder?"
	exit 1
fi

if [ $(basename "$folder")=="nihongoAccentJiten" ]; then
	args="-rotate 0.7 -crop 2360x2230+910+250 +repage -crop 50%x100%"
fi

cd "$folder"

mkdir "crop" # tch
mkdir "crop-pbm"
mkdir "crop-djvu"

for file in *.jpg; do
	echo "cropping $file"

	convert \
		$args \
		"$file" \
		"crop/$file"

	echo
done

# Left side: page B
for file in crop/*-0.jpg; do
	echo "renaming $file"

	mv "$file" $(echo "$file" | sed "s/-0/-b/")

	echo
done

# Right side: page A
for file in crop/*-1.jpg; do
	echo "renaming $file"

	mv "$file" $(echo "$file" | sed "s/-1/-a/")

	echo
done

read "Take this time to review the cropped images. Press enter to continue."

for file in crop/*.jpg; do
	file=$(basename "$file")
	echo "converting $file"

	convert \
		"crop/$file" \
		"crop-pbm/${file}.pbm"

	cjb2 -clean "crop-pbm/${file}.pbm" "crop-djvu/${file}.djvu"

	echo
done

echo "building final djvu"

djvm -create out.djvu crop-djvu/*.djvu

# https://commons.wikimedia.org/wiki/Help:Creating_a_DjVu_file#On_Linux,_FreeBSD,_etc.
# https://en.wikisource.org/wiki/Help:DjVu_files#Linux
