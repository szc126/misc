#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
#gen = pagegenerators.TextIOPageGenerator(source='/tmp/pywikibot.txt', site=site)
gen = site.categorymembers(pywikibot.Category(site, 'Nivkh dialect synonyms data modules'))
replaced = []

def doer(m):
	term = m.group(0)
	q, tr = False, False
	try:
		term, q = term.split(':')
	except:
		True
	try:
		term, tr = term.split('/')
	except:
		True
	return term + (f'<tr:{tr}>' if tr else '') + (f'<q:{q}>' if q else '')

for page in gen:
	print()
	print()
	print('＠＠＠＠＠')
	print()
	print()
	print(page.title())
	print(page.full_url())

	try:
		text_old = page.text
		page.text = re.sub(r"{[^\n]+}", lambda x: re.sub(r"(?<=\").+?(?=\")", doer, x[0]), page.text)
		summary = 'Update to use inline modifiers'

		if text_old != page.text:
			print('\t' + summary)
			pywikibot.showDiff(text_old, page.text, context = 0)
			reply = input('[press enter to continue, x enter to cancel]')

			if reply == '':
				page.save(summary)
			elif reply == 'x':
				print('Skipped.')
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')