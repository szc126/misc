#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import zhdialsyn as pwb_source

site = pywikibot.Site()
gen = pagegenerators.PrefixingPageGenerator('Module:zh/data/dial-syn/')
ignore_list = [
	'Module:zh/data/dial-syn/documentation',
	'Module:zh/data/dial-syn/template',
]

counter = 0
counter_limit = 5
for page in gen:
	if page.title() in ignore_list:
		continue

	print(page.title())
	try:
		page = pwb_source.main(page)
		page.save('update with new locations')
	except Exception as e:
		print(page.text)
		input('[press enter to continue]')

	counter += 1
	if counter >= counter_limit:
		input('[go review]')
		counter = 0

	print()
	print()
	print('＠＠＠＠')
	print()
	print()
