#!/usr/bin/env bash

id="$1"
end="$2"
folder="$3"

if [ -z "$id" ]; then
	echo "Which book?"
	exit 1
fi

if [ -z "$end" ]; then
	echo "To what page?"
	exit 1
fi

if [ -z "$folder" ]; then
	folder="$id"
fi

for i in $(seq --format="%07g" 1 "$end"); do
	url="https://www.dl.ndl.go.jp/api/iiif/${id}/R${i}/full/full/0/default.jpg"
	echo "$url"
	wget \
		--output-document="$folder/$i.jpg" \
		--continue \
		--show-progress \
		--verbose \
		"$url"
	if [ "$?" -ne 0 ]; then
		echo "Failed!"
		exit 1
	fi
	echo
done
