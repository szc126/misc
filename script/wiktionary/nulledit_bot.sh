#!/usr/bin/env python3

import pywikibot
from pywikibot.page import Page
import sys

site = pywikibot.Site()
#gen = site.search(": " + sys.argv[1])
gen = site.categorymembers(pywikibot.Category(site, 'Pages using duplicate arguments in template calls'))

for page in gen:
	print(page.title())
	try:
		page.save('null edit')
	except Exception as e:
		print('failed')