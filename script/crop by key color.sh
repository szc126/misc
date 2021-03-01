#!/usr/bin/env bash

# http://www.imagemagick.org/discourse-server/viewtopic.php?t=24959

for file in *
do
	bg_color=$(convert "$file" -format '%[pixel:p{0,0}]' info:)
	echo $bg_color
	convert "$file" -transparent $bg_color -trim ".$file.png"
done
