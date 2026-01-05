#!/usr/bin/env bash

# bash a.sh *

# ffmpeg -i /tmp/a.webm  -vf "fps=1,crop=1280:50:0:595" -q:v 2 outimage_%03d.jpeg

set=25
rounds=$(($#/set))
offset=1 # $0 is the executable name

for round in $(seq 0 $rounds)
do
	from=$((offset+round*set))
	images=${@:from:set}
	convert -append $images "appended-$round.jpg"
done