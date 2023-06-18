#!/usr/bin/env bash

folder="$1"
args="-crop 50%x100% +repage"

if [ -z "$folder" ]; then
	echo "Which folder?"
	exit 1
fi

case $(basename "$folder") in
	"")
		args=""
		;;
esac

cd "$folder"

mkdir "crop" # tch

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

	mv "$file" "$(echo "$file" | sed "s/-0/-b/")"

	echo
done

# Right side: page A
for file in crop/*-1.jpg; do
	echo "renaming $file"

	mv "$file" "$(echo "$file" | sed "s/-1/-a/")"

	echo
done

echo "Take this time to review the cropped images. Press enter to continue."
read

echo "building final pdf"

img2pdf --output out.pdf crop/*.jpg
