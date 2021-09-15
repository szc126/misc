#!/usr/bin/env bash

folder="$1"
args="-crop 50%x100% +repage"

if [ -z "$folder" ]; then
	echo "Which folder?"
	exit 1
fi

case $(basename "$folder") in
	"nihongoAccentJiten")
		args="-rotate 0.7 -crop 2360x2230+910+250 +repage -crop 50%x100%"
		;;
	"kainangoSyoho")
#		args="-rotate 1.0 -crop 2800x2400+710+140 +repage -crop 50%x100%"
		args="-rotate 1.0 +repage -crop 2800x2400+710+140 +repage -crop 50%x100%"
		;;
	"nissenNitijoKaiwa")
		args="-rotate 0 +repage -crop 4890x3430+370+160 +repage -crop 50%x100%"
		;;
	"igakGoi")
		args="+repage -crop 3100x2500+634+210 +repage -crop 50%x100%"
#		args="+repage -crop 3100x2500+1410+210 +repage -crop 50%x100%" # centered page
		;;
	"igakGoi-2")
		args="+repage -crop 3100x2500+1410+210 +repage -crop 50%x100%" # centered page
		;;
esac

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

echo "Take this time to review the cropped images. Press enter to continue."
read

for file in crop/*.jpg; do
	file=$(basename "$file")
	echo "converting $file"

	#convert "crop/${file}" "crop-pbm/${file}.pbm"
	#cjb2 -clean "crop-pbm/${file}.pbm" "crop-djvu/${file}.djvu"

	c44 "crop/${file}" "crop-djvu/${file}.djvu"

	echo
done

echo "building final djvu"

djvm -create out.djvu crop-djvu/*.djvu

# https://commons.wikimedia.org/wiki/Help:Creating_a_DjVu_file#On_Linux,_FreeBSD,_etc.
# https://en.wikisource.org/wiki/Help:DjVu_files#Linux
