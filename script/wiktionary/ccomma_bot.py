#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
#gen = site.search(': "Korean" hastemplate:trans-top insource:/\|ko\|[㐀-龥]/')
#gen = site.search(': "Korean" hastemplate:trans-top insource:/\|ko\|[^|}]*\[\[[㐀-龥]/')
gen = site.search(': "Korean" hastemplate:trans-top insource:/\|ko\|[^|}]*\[\[[㐀-龥]/')

replaced = []

def doer(match):
	d = match.group(0)
	# remove |sc=
	d = re.sub(r'\|sc=[A-Za-z]+', r'', d)
	#
	d = re.sub(r'-?\[\[([㐀-龥]+)\]\]-?', r'\1', d)
	# {{t+|ko|단념하다}} ({{t+|ko|斷念|alt=斷念하다|tr=-}})
	d = re.sub(r'([㐀-龥]+)\|alt=\1하다', r'\1하다', d)
	# {{t+|ko|적격|alt=적격의}} ({{t+|ko|適格|alt=適格의|tr=-}})
	d = re.sub(r'([㐀-龥]+)\|alt=\1의', r'\1', d)
	# remove |tr= for hanja
	d = re.sub(r'(?<=[㐀-龥])\|tr=[^|}]+', r'', d)
	d = re.sub(r'(?<=[㐀-龥]하다)\|tr=[^|}]+', r'', d)
	# {{t+|ko|고대|alt=고대의}} ({{t+|ko|古代}})
	d = re.sub(r'({{(?:tt?|tt?[+-][a-z]*)\|ko\|)([^|}]+)(?:\|alt=\2의)([^}]*)(}}),?\s*[(（]?{{(?:tt?|tt?[+-][a-z]*)\|ko\|([㐀-龥]+)}}[)）]?', r'\1[[\2(\5)]]-의\3\4', d)
	d = re.sub(r'({{(?:tt?|tt?[+-][a-z]*)\|ko\|)([^|}]+)(?:\|alt=\2인)([^}]*)(}}),?\s*[(（]?{{(?:tt?|tt?[+-][a-z]*)\|ko\|([㐀-龥]+)}}[)）]?', r'\1[[\2(\5)]]-인\3\4', d)
	# ([^|}]+)([^}]*) to capture the first parameter + anything else, to avoid {{t+|ko|^일본해|lit=Sea of Japan(日本海)}}
	d = re.sub(r'({{(?:tt?|tt?[+-][a-z]*)\|ko\|)([^|}]+)하다([^}]*)(}}),?\s*[(（]?{{(?:tt?|tt?[+-][a-z]*)\|ko\|([㐀-龥]+)}}[)）]?', r'\1\2(\5)하다\3\4', d)
	d = re.sub(r'({{(?:tt?|tt?[+-][a-z]*)\|ko\|)([^|}]+)([^}]*)(}}),?\s*[(（]?{{(?:tt?|tt?[+-][a-z]*)\|ko\|([㐀-龥]+)}}[)）]?', r'\1\2(\5)\3\4', d)
	d = re.sub(r'({{(?:tt?|tt?[+-][a-z]*)\|ko\|)([^|}]+)하다([^}]*)(}}),?\s*[(（]?{{(?:tt?|tt?[+-][a-z]*)\|ko\|([㐀-龥]+)하다}}[)）]?', r'\1\2(\5)하다\3\4', d)
	print('..' + d)
	replaced.append(d)
	return d

for page in gen:
	print(page.title())
	try:
		text_old = page.text
		replaced = []
		page.text = re.sub(
			r'{{(?:tt?|tt?[+-][a-z]*)\|ko\|[^}]+}},?\s*[(（]?{{(?:tt?|tt?[+-][a-z]*)\|ko\|[^|}]*[㐀-龥][^}]*}}[)）]?',
			doer,
			page.text,
		)

		#if re.search(r'(\|ko\|[㐀-龥]|\|ko\|[^}]+alt=)', page.text):
		#	# oh no!
		#	print('X ' + re.search(r'.+(ko\|[㐀-龥]|ko\|[^}]+alt=).+', page.text).group(0))
		if 0:
			pass
		elif text_old != page.text:
			pywikibot.showDiff(text_old, page.text)
			reply = input('[press enter to continue, x enter to cancel]')
			#reply = ''

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save('ko: update tl fmt: ' + ', '.join(set(replaced)))
				print('Saved.')
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print()
	print()
	print('＠＠＠＠')
	print()
	print()
