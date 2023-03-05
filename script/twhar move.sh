#!/usr/bin/env zsh

indices=$(cat .indices.txt)

for folder in *(F)
do
	for file in "$folder/"*
	do
		if [[ "$file" == *".mp4" ]]
		then
			mv "$file" "$folder.mp4" --no-clobber
		else
			image_id_and_ext=$(basename "$file" | sed -E 's/^[0-9]+\_(.+)\.([a-z]{3})$/\1 \2/g')
			image_id=$(echo "$image_id_and_ext" | cut -d' ' -f1)
			image_ext=$(echo "$image_id_and_ext" | cut -d' ' -f2)
			# max-count: the pythonscript is 'append', not 'write'. run the script twice, get two entries
			index=$(echo "$indices" | grep "$image_id" --max-count=1 | cut -d' ' -f2)

			mv "$file" "$folder-$index.$image_ext" --no-clobber
		fi
	done
done

find . -type d -empty -exec rmdir {} \;