#!/usr/bin/env bash

pdf="$1"
working_dir="$2"

if [ -z "$pdf" ]; then
	echo "which pdf?"
	exit 1
fi

if [ -z "$working_dir" ]; then
	echo "to where?"
	exit 1
fi

echo "(mkdir ...)"
mkdir "$working_dir"
echo

echo "(working on $pdf)"
pdfimages -j -jp2 "$pdf" "$working_dir/pdfimages"
echo

for file in ${working_dir}/*.jp2; do
	echo "(converting $file to ppm)"
	convert "$file" "${file}.ppm"

	echo "(converting $file to djvu)"
	c44 "${file}.ppm" "${file}.djvu"

	echo
done

for file in ${working_dir}/*.pbm; do
	magic=$(file "$file")
	
	echo "(converting $file to djvu)"

	if echo "$magic" | grep "1034 x 204"; then
		echo "(skipped: deleted Google watermark)"
		rm "$file"
	elif echo "$magic" | grep "29 x 29"; then
		echo "(skipped: deleted Google QR code)"
		rm "$file"
	else
		cjb2 "${file}" "${file}.djvu"
	fi

	echo
done

echo "Take this time to review the images. Press enter to continue."
read

echo "(building djvu)"
djvm -create "${working_dir}/out.djvu" ${working_dir}/pdfimages-*.djvu