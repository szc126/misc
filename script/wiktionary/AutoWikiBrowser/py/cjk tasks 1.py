# [X] Enabled
# Program or script: F:\DOCS\awb uxi.py
# Arguments/Parameters: %%file%%
# Input/Output file: E:\temp.txt
# (X) Pass article text as file
#
# (see tooltip for "Pass article text as parameter")

import os
import sys
import re
import traceback

def readViHantu(match):
	head = match.group(1)
	body = match.group(2)
	tail = match.group(3)

	if re.search(r'^[^|]', body):
		# false positive, like {{vi-hantutab}}
		return head + body + tail

	args = re.findall(r'\|([^|}]+)', body)
	out = []
	for text in args:
		if '=' not in text:
			text = 'reading=' + text
		out.append(text)
	out = '|' + '|'.join(out)

	print(out)

	return '{{vi-readings' + out + tail

def readKoHanja(match):
	head = match.group(1)
	body = match.group(2)
	tail = match.group(3)

	args = re.findall(r'\|([a-z]+)=([^|}]+)', body)
	do_convert = True
	for k, v in args:
		if k == 'hangeul' and re.search(r'[,\[\] ]', v):
			do_convert = False
		elif k == 'eumhun' and v != '':
			do_convert = False

	if do_convert:
		for k, v in args:
			if k == 'hangeul':
				body = '|' + v

	return head + body + tail

def readJaReadings(match, hz):
	head = match.group(1)
	body = match.group(2)
	tail = match.group(3)

	args = re.findall(r'\|([a-z]+)=([^|}]+)', body)
	args = test13(args, hz)

	print(args)

	return args

def test13(a, hz):
	# a = _
	# hz = _
	# yomi = _
	out = []
	order = ['goon', 'kanon', 'toon', 'kanyoon', 'soon', 'on', 'kun', 'nanori']
	processed = {}
	# missing = []

	for type, text in a:
		text = re.sub(r'\s*\([a-zāīūēō\.\-]\)', '', text)
		text = re.sub(r'{{non\-joyo\-reading}}\s*', '', text)
		text = re.sub(r'\s*{{q[a-z]*\|non\-\[\[w:Jōyō kanji\|Jōyō\]\] reading}}', '', text)
		text = re.sub(r',\s*{{q[a-z]*\|historical}}', '<', text)
		text = re.sub(r'\[\[(' + hz + '[ぁ-ー]+)\]\]', '', text)
		text = re.sub(r'{{[jal|-]+(' + hz + '[ぁ-ー]+)}}', '', text)
		text = re.sub(r'\[\[([^\]\|]+)\|([^\]\|]+)\]\]', lambda match:
			re.sub(r'\.', '-', match.group(1))
		, text)
		#

		text = re.sub(r'([^ぁ-ー])\.([^ぁ-ー])', '@', text)
		text = re.sub(r'[^ぁ-ー\-<>.]+', '@', text)
		text = re.sub(r'(@*)[<>](@*)', '<', text) # or something. also, the > is intentional (some entries indeed have backwards arrows)

		text = re.sub(r'^@', '', text)
		text = re.sub(r'@$', '', text)
		text = re.sub(r'@', ', ', text)

		if type != 'kun':
			text = re.sub(r'\-', '', text)
		#

		processed[type] = text
	#

	out.append('{{ja-readings')

	for type in order:
		if type in processed:
			out.append('|'+type+'='+processed[type])
		#
	#

	out.append('}}')

	out = '\n'.join(out)

	return out

def main():
	filePath = sys.argv[1]
	lines = None

	with open(filePath, mode='r', encoding='utf-8') as file:
		lines = file.read()

		lines = re.sub(r'\n\* *(\{\{(Han ref|ja-readings|ja-pron))', r'\n\1', lines)

		lines = re.sub(r'(\{\{Han ref)([^}]*)(\|ud=[^|}]+)([^}]*)(\}\})', r'\1\2\4\5', lines)
		lines = re.sub(r'(\{\{Han ref)([^}]*)(\|bd=[^|}]+)([^}]*)(\}\})', r'\1\2\4\5', lines)
		lines = re.sub(r'(\{\{Han ref)([^}]*)(\|bh=[^|}]+)([^}]*)(\}\})', r'\1\2\4\5', lines)
		lines = re.sub(r'({{Han ref)([^}]+)(}})', lambda match:
			match.group(1) + re.sub(r'(\|[a-z]+=)([^|}]*)', lambda match:
				((match.group(1) + match.group(2)) if match.group(2) != '' else '')
			, match.group(2)) + match.group(3)
		, lines)

		lines = re.sub(r'({{vi-hantu)([^}]+)(}})', readViHantu, lines)

		#lines = re.sub(r'({{vi-readings)([^}]+)(}})', lambda match:
		#	match.group(1) + re.sub(r'\|\s*hanviet\s*=\s*', r'|reading=', match.group(2)) + match.group(3)
		#, lines)

		lines = re.sub(r'({{ja-readings)([^}]+)(}})', lambda match: readJaReadings(match, 'XXX'), lines)

		lines = re.sub(r'{{ko-hanja/new', '{{ko-hanja', lines)
		lines = re.sub(r'({{ko-hanja)([^}]+)(}})', readKoHanja, lines)

		lines = re.sub(r'{{Han etyl([\|}])', r'{{Han etym\1', lines)
		lines = re.sub(r'({{zh-pron)([^}]+)(}})', lambda match:
			match.group(1) + match.group(2) + (
				'|cat=\n}}' if (
					'|cat=' not in match.group(2) and # zh-pron does not contain '|cat='
					not re.search(r'[㐀-鿕]$', match.group(2)) # never mind if the so-called 'zh-pron' content ends in a hanzi (the regex is stupid and the so-called end of {{zh-pron}} may be inside {{zh-l}}, as in [[萬]])
				) else '}}'
			)
		, lines)
	with open(filePath, mode='w', encoding='utf-8') as file:
		file.writelines(lines)

try:
	main()
	#input('press enter')
except Exception as e:
	print(traceback.format_exc())
	input('press enter')

# https://stackoverflow.com/a/12597709
# https://stackoverflow.com/a/4719562
# https://stackoverflow.com/questions/1278705/python-when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number