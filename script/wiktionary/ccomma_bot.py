#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
#page = pywikibot.Page(site, 'Template:Song box')
#gen = page.getReferences(page)
gen = site.search(' "japanese katakana" "japanese nouns" -etymology -insource:/((alternative|alt) (form|spelling|sp)|short for|clip)|ja-(def|see)|\{\{elements|head=\[\[/ -"japanese proper nouns" -intitle:/ー/ -insource:/ja-noun\|[^}]+ / -hastemplate:ja-kanjitab -hastemplate:"U:ja:biology" ')

replaced = []

def doer(match):
	a = ['', match.group(1), match.group(2)]
	a[2] = re.sub(r'{{date\|([^|}]+)\|([^|}]+)\|([^|}]+)}}', r'\2 \3, \1', a[2], flags = re.I)
	replaced.append(match.group(2) + '→' + a[2])
	return ''.join(a)

bool_skip = True
for page in gen:
	"""
	if bool_skip:
		print(page.title())
		if page.title()[0] == 'ス': # start from this point in the list instead of from the top
			bool_skip = False
		else:
			continue
	"""

	if 'Etymology' in page.text:
		continue

	print(page.title())
	try:
		text_old = page.text
		lang_code = ''
		while not lang_code == 'next':
			replaced = []
			#page.text = re.sub(r'(\|date.+)({{date.+)', doer, page.text, flags = re.I)

			candidates = re.search(r'\[\[([^\]:]+)\]\]', page.text)
			if not candidates:
				candidates = re.search(r'# *([a-z]+)', page.text)
			if not candidates:
				lang_code = 'next'
				continue
			if lang_code == '':
				ety = '{{internationalism|ja}}; see {{cog|en|' + candidates.group(1) + '}}.'
			else:
				ety = '{{bor+|ja|' + lang_code + '|' + candidates.group(1) + '}}.'
			replaced.append(ety)

			print('\thttps://en.wiktionary.org/wiki/' + page.title())
			print('\thttps://www.weblio.jp/content/' + page.title())
			print('\thttps://en.wiktionary.org/wiki/' + candidates.group(1).replace(' ', '_'))

			temp = page.text.split('===')
			if "Alternative forms" in page.text:
				temp.insert(3, 'Etymology')
				temp.insert(4, '\n' + ety + '\n\n')
			else:
				temp.insert(1, 'Etymology')
				temp.insert(2, '\n' + ety + '\n\n')
			page.text = '==='.join(temp)

			if text_old != page.text:
				summary = 'add Ety: ' + ', '.join(set(replaced))
				print('\t' + summary)
				#pywikibot.showDiff(text_old, page.text)
				print(page.text)
				reply = input('[press enter to continue, x enter to cancel, langcode enter to change]')

				if reply == '':
					lang_code = 'next'
					page.save(summary)
					print('Saved.')
				elif reply == 'x':
					lang_code = 'next'
					print('Skipped.')
				else:
					lang_code = reply
					page.text = text_old
					print('Trying again.')
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print()
	print()
	print('＠＠＠＠')
	print()
	print()
