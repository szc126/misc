#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
#page = pywikibot.Page(site, 'Template:Song box')
#gen = page.getReferences(page)
gen = site.search(' "japanese katakana" "japanese nouns" -etymology -"alternative form of" -hastemplate:ja-see -hastemplate:ja-def -"short for" -"clipping of"   -"alternative spelling of" -hastemplate:elements -"japanese proper nouns" ')

replaced = []

def doer(match):
	a = ['', match.group(1), match.group(2)]
	a[2] = re.sub(r'{{date\|([^|}]+)\|([^|}]+)\|([^|}]+)}}', r'\2 \3, \1', a[2], flags = re.I)
	replaced.append(match.group(2) + '→' + a[2])
	return ''.join(a)

ffwd = 0
for page in gen:
	if ffwd == 0:
		print(page.title())
		if page.title()[0] == 'ハ':
			ffwd = 1
		else:
			continue

	if 'Etymology' in page.text:
		continue

	print(page.title())
	try:
		text_old = page.text
		replaced = []
		#page.text = re.sub(r'(\|date.+)({{date.+)', doer, page.text, flags = re.I)

		candidates = re.search(r'\[\[([^\]:]+)\]\]', page.text)
		if not candidates:
			continue
		ety = 'From {{bor|ja|en|' + candidates.group(1) + '}}.'
		replaced.append(ety)

		print('\thttps://en.wiktionary.org/wiki/' + page.title())
		print('\thttps://www.weblio.jp/content/' + page.title())
		print('\thttps://en.wiktionary.org/wiki/' + candidates.group(1))

		temp = page.text.split('===')
		temp.insert(1, 'Etymology')
		temp.insert(2, '\n' + ety + '\n\n')
		page.text = '==='.join(temp)

		if text_old != page.text:
			summary = 'add Etymology: ' + ', '.join(set(replaced))
			print('\t' + summary)
			#pywikibot.showDiff(text_old, page.text)
			print(page.text)
			reply = input('[press enter to continue, x enter to cancel]')
			#reply = ''

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save(summary)
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
