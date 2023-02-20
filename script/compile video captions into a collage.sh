#!/usr/bin/env bash

# bash a.sh *

# ffmpeg -i /tmp/a.webm  -vf "fps=1,crop=1280:50:0:595" -q:v 2 outimage_%03d.jpeg

min=1
max=${#@}

for n in $(seq 1 $((max/100)))
do
	local_min=$((n*100-100+1))
	local_max=$((n*100))
	images=$(seq -f 'outimage_%03g.jpeg' $local_min $local_max)
	convert -append $images "appended-$local_min.jpg"
done