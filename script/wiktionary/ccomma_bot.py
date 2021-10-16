#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
gen = site.search('korean insource:/[가-힣] \([㐀-龥]/')

replaced = []

def doer(match):
	d = re.sub(r'([가-힣 ]+) \(([㐀-龥]+)\)', r'\1(\2)', match.group(0))
	replaced.append(d)
	return d

for page in gen:
	print(page.title())
	try:
		text_old = page.text
		replaced = []
		page.text = re.sub(
			r'{{[^|]+\|ko[^}]*[가-힣 ]+ \([㐀-龥]+\)[^}]*}}',
			doer,
			page.text,
		)
		pywikibot.showDiff(text_old, page.text)

		if text_old != page.text:
			#reply = input('[press enter to continue, x enter to cancel]')
			reply = ''

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save('Korean: remove space before parens: ' + ', '.join(set(replaced)))
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
