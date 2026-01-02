#!/usr/bin/env python3

import pywikibot
from pywikibot.page import Page
from pywikibot import pagegenerators
import sys

# https://doc.wikimedia.org/pywikibot/stable/api_ref/pywikibot.site.html
site = pywikibot.Site()
#gen = site.search(": " + sys.argv[1])
gen = site.categorymembers(pywikibot.Category(site, 'Pages using duplicate arguments in template calls'))
#gen = pagegenerators.TextIOPageGenerator(source='/tmp/pywikibot.txt', site=site)

for page in gen:
	print(page.title())
	print(page.full_url())

	try:
		if page.exists():
			page.save('null edit')
	except Exception as e:
		print('failed')