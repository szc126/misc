#!/usr/bin/env zsh

for file in $@
do
	text=$(cat $file)
	if (( $(echo $text | wc -l) == 1 )) && [[ $text == "http"* ]] && [[ $text != *"#"* ]] && [[ $text != *" "* ]]
	then
		echo $text
		echo '[InternetShortcut]\nURL='$text > $file
		mv "$file" "${file%.txt}.URL"
	else
		echo SKIPPED
		echo $text
	fi
	echo "----"
done