#!/usr/bin/env bash

# https://wiki.archiveteam.org/index.php/Wget#Creating_WARC_with_wget

# > f=1; t=$((f + 99)); export wo="utauuuta $f $t"; export wi="-"; echo "https://w.atwiki.jp/utauuuta/?cmd=backup&action=source&pageid="{$f..$t}"\n" | warcget

LANG=en_US.utf8

wua="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"

wget \
-e robots=off \
--waitretry 5 --timeout 60 --tries 5 --wait 1 --random-wait \
--warc-header "operator: Archive Team" --warc-cdx --warc-file="${wo?}" \
-U "${wua?}" -i "${wi?}" -P "/tmp/warc/${wo?}" "$@"