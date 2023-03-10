#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import sys

site = pywikibot.Site()
gen = site.search(' "Han char without ids" ')

idss = {}
with open(sys.argv[1], 'r') as f:
	for line in f:
		if line[0] == '#':
			continue
		line = line.split('\t')
		idss[line[0]] = line[1].strip()

for page in gen:
	print(page.title())
	if not page.title() in idss:
		continue

	text_old = page.text
	if '|ids=' in page.text:
		page.text = page.text.replace('|ids=}}', '|ids=' + idss[page.title()] + '}}')
	else:
		print('could not find |ids=')
	summary = '|ids=' + idss[page.title()]

	if text_old != page.text:
		pywikibot.showDiff(text_old, page.text)
		#reply = input('[press enter to continue, x enter to cancel]')
		reply = ''

		if reply == '':
			page.save(summary)
			print('Saved.')
		elif reply == 'x':
			print('Skipped.')