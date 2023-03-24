#!/usr/bin/env python3

import unihan

import pywikibot
from pywikibot import pagegenerators
from pywikibot.page import Page
import re
import sys
import mwparserfromhell

site = pywikibot.Site()
#gen = pywikibot.User(site, sys.argv[1]).contributions(namespaces = pywikibot.site.Namespace(0))
gen = site.search(' -insource:/Han char/ "CJK Unified Ideographs" ')

done = set()

for page in gen:
	z = page.title()
	save_summary = ''

	if z in done:
		continue
	if len(z) != 1:
		continue

	print('https://en.wiktionary.org/wiki/' + z)

	try:
		text_old = page.text

		text_new = page.text
		text_new = mwparserfromhell.parse(text_new)
		text_new = text_new.get_sections(include_lead=True,levels=[2])

		text_mul = unihan.newhzmul({
			'char': z,
			'x': page.text,
		})
		text_mul = mwparserfromhell.parse(text_mul)
		text_mul = text_mul.get_sections(include_lead=True,levels=[2])

		if pywikibot.textlib.does_text_contain_section(page.text, 'Translingual'):
			text_new[1] = text_mul[1]
			text_new = [str(element) for element in text_new]

			if not '{{character' in text_new[0]:
				text_new.insert(1, '{{character info}}\n')

			page.text = ''.join(text_new)
			save_summary = '/* Translingual */ rewrite'
		else:
			text_new.insert(1, text_mul[1])
			if not '{{character' in text_new[0]:
				text_new.insert(1, text_mul[0])
			text_new = [str(element) for element in text_new]

			page.text = ''.join(text_new)
			save_summary = '/* Translingual */ new'

		page.text = re.sub(r'^(=+) +', r'\1', page.text, flags = re.M)
		page.text = re.sub(r' +(=+)$', r'\1', page.text, flags = re.M)
		page.text = re.sub(r'\n*{{DEFAULTSORT:[^}]+}}', r'', page.text, flags = re.M)

		print('◆')
		print(page.text)
		print('◆')

		if text_old != page.text:
			pywikibot.showDiff(text_old, page.text)
			reply = input('[press enter to continue, x enter to cancel]')

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save(save_summary)
				print('Saved.')

		done.add(z)
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')
