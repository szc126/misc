#!/usr/bin/env bash

id="${1}"

ua='Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.97 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' # tiwiki seigen-wo kwaihi
url_ch="https://manga.line.me/book/viewer?id=${id}"
html=$(wget -O- "${url_ch}" -U "${ua}")

if [ "$?" -eq 8 ]
then
	ua="Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
	url_ch="https://webcache.googleusercontent.com/search?hl=en&q=cache:https://manga.line.me/book/viewer?id=${id}"
	html=$(wget -O- "${url_ch}" -U "${ua}")
fi

meta_desc=$(echo "${html}" | pcregrep -o1 'meta name="description" content="(.+)"')
meta_desc_ch_name=$(echo "${meta_desc}" | cut -d'|' -f1)
meta_desc_title_author=$(echo "${meta_desc}" | cut -d'|' -f2)
meta_desc_kaidai=$(echo "${meta_desc}" | cut -d'|' -f3)

meta_desc_title=$(echo "${meta_desc_title_author}" | pcregrep -o1 "(.+)\((.+)\)")
meta_desc_author=$(echo "${meta_desc_title_author}" | pcregrep -o2 "(.+)\((.+)\)")

# ALTERNATIVE ONELINER:
#wget $(wget -O- "${url_ch}" -U "${ua}" | pcregrep -o1 "'url': +'(.+)'")

i=0
for url_frame in $(echo "${html}" | pcregrep -o1 "'url': +'(.+)'")
do
	((i++))
	out_folder="【${meta_desc_author}】${meta_desc_title}【LINEマンガ】/【${id}】${meta_desc_ch_name}"
	out_file="${i}-"$(basename "${url_frame}")
	mkdir --parents "${out_folder}"

	wget --output-document "${out_folder}/${out_file}" "${url_frame}"
done
