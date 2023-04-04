#!/usr/bin/env python

import requests
import re
import sys
import xml.etree.ElementTree as ET

def param(*args):
	return {
		'no_pagination': str(args[0]), # return page number n
		'num_per_page': str(args[1]), # return n items
		'skey': str(args[2] or sys.argv[1]), # search keyword
		'orderby': str(args[3] or 'reg_date desc'),
	}

s = requests.Session()
s.get('http://www.uriminzokkiri.com/index.php?ptype=cmusic')

url_writelist = 'http://www.uriminzokkiri.com/index.php?ptype=cmusic&mtype=writeList'
pagenum = 1
num_per_page = 40
page = s.post(url_writelist, data = param(pagenum, num_per_page, None, None)).json()

total_counts = int(page['counts_music'])
last_page = (int(total_counts / num_per_page)) + (1 if total_counts % num_per_page else 0)
if not sys.argv[1]:
	print('no search keyword: returning page 1')
	last_page = 1

artist = '조선민주주의인민공화국'
album = '우리민족끼리'

m3u = ['#EXTM3U', '#EXTENC:UTF-8', '#EXTALB:' + album]
asx = ET.Element('asx', version = '3.0')
asx_main_title = ET.SubElement(asx, 'title')
asx_main_title.text = album

for pagenum in range(1, last_page + 1):
	print('page ' + str(pagenum) + ' of ' + str(last_page))
	m3u.append('#EXTGRP:page ' + str(pagenum))
	for song in page['lists']:
		title = re.sub(r'<.+?>', r'', song['title'])
		no = song['no']
		url_mp3 = 'http://www.uriminzokkiri.com/index.php?ptype=cmusic&mtype=download&no=' + no
		print(title)
		m3u.append('#EXTINF:0,' + artist + ' - ' + title)
		m3u.append(url_mp3)
		asx_entry = ET.SubElement(asx, 'entry')
		asx_title = ET.SubElement(asx_entry, 'title')
		asx_title.text = title
		asx_author = ET.SubElement(asx_entry, 'author')
		asx_author.text = artist
		asx_ref = ET.SubElement(asx_entry, 'ref', href = url_mp3)

	pagenum += 1
	page = s.post(url_writelist, data = param(pagenum, num_per_page, None, None)).json()

with open('uriminzokkiri.m3u8', 'w') as f:
	f.write('\n'.join(m3u))
with open('uriminzokkiri.asx', 'w') as f:
	ET.indent(asx, space = '\t')
	text = ET.tostring(asx, encoding = 'utf-8').decode()
	f.write(text)
