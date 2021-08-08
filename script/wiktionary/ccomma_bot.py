#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
gen = site.search('hastemplate:zh-pron "cantonese lemmas" insource:/\|c=[^|}=]+, /')

for page in gen:
	if '——' in page.title():
		continue

	if '，' in page.title():
		continue

	print(page.title())
	try:
		text_old = page.text
		page.text = re.sub(
			r'\|c=.+',
			lambda match: re.sub(r'\s*,\s*', r',', match.group(0)),
			page.text,
		)
		pywikibot.showDiff(text_old, page.text)

		if text_old != page.text:
			reply = input('[press enter to continue, x enter to cancel]')

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save('{{zh-pron}} Cantonese: remove improper spaces surrounding commas')
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
