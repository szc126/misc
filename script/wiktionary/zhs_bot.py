#!/usr/bin/env python3

import unihan

import pywikibot
from pywikibot import pagegenerators
from pywikibot.page import Page
import re

site = pywikibot.Site()
cat = pywikibot.Category(site, 'Chinese terms with uncreated forms')
gen = site.categorymembers(cat)

for page_t in gen:
	print(page_t.title())
	try:
		s_found = re.findall(
			r'\|(?:s|t\d+)=([^|}]+)',
			page_t.text,
		)

		for s in s_found:
			# don't ignorantly create pages for imaginary simplified forms.
			if len(s) == 1 and re.search('{{character info}}', page_t.text):
				page_s = Page(site, s)
				if not page_s.exists():
					page_s.text = unihan.newhzmul({
						'char': s,
					})
					page_s.text += '\n\n----\n\n==Chinese==\n{{zh-see|' + page_t.title() + '}}'
					page_s.save('init. {{zh-see|' + page_t.title() + '}}')
					#input('[press enter to continue]')
				else:
					print('[it already exists]')
			else:
				page_s = Page(site, s)

				# get page creator
				user = ''
				for rev in page_t.revisions(content = False):
					user = rev['user']

				if (not page_s.exists()) and (
					user == 'Justinrleung' or
					user == '恨国党非蠢即坏' or
					user == 'Mar vin kaiser' or
					user == 'Michael Ly' or
					user == 'RcAlex36' or
					user == 'Suzukaze-c' or
					user == 'Tooironic' or
					False
				):
					page_s.text += '==Chinese==\n{{zh-see|' + page_t.title() + '}}'
					page_s.save('{{zh-see|' + page_t.title() + '}}')
					#input('[press enter to continue]')
				else:
					#input('[it already exists]')
					pass
		page_t.save('null edit')
	except Exception as e:
		print(page_t.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print('----')
