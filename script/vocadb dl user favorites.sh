#!/usr/bin/env bash

# https://discord.com/channels/309072240639737866/666326527197315091/806817707097194516

user_id=$1

for i in `seq 0 100 500`; do wget "https://vocadb.net/api/users/$user_id/ratedSongs?start=$i&maxResults=100"; done
grep -P "(?<=publishDate\":\")[0-9]{4}" * --only-matching --no-filename | sort | uniq --count