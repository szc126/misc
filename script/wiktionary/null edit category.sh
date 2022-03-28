#!/usr/bin/env python3

import pywikibot
from pywikibot.page import Page
import sys

site = pywikibot.Site()
cat = pywikibot.Category(site, sys.argv[1])
gen = site.categorymembers(cat)

for page in gen:
	print(page.title())
	try:
		page.save('null edit')
	except Exception as e:
		print('failed')