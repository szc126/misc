#!/usr/bin/env zsh

if [ "$1" = "d" ]
then
	paste <(echo '\n'{ア..ン}) <(echo '\n'{ア..ン}|uconv -x Kana-Latn)|grep -E "[gzjdbp~]"
else
	paste <(echo '\n'{ア..ン}) <(echo '\n'{ア..ン}|uconv -x Kana-Latn)|grep --invert-match -E "[gzjdbp~]"
fi