#!/usr/bin/env python3

import unihan

import pywikibot
from pywikibot import pagegenerators
from pywikibot.page import Page
import re

site = pywikibot.Site()
gen = site.search('')

# TODO:
# interesting functions:
# pywikibot.textlib.does_text_contain()
# pywikibot.textlib.extract_sections()

for page in gen:
	z = page.title()
	if len(z) != 1:
		continue
	try:
		page.text = re.sub(r'{{character info}}\n', '', page.text)

		text_old = page.text
		text_new = []
		mul_text = unihan.newhzmul({
			'char': z,
			'x': page.text,
		})
		mul_text = re.sub(r'(----)\n\n', '----', mul_text)

		if 'Translingual' in page.text:
			b_add_lines = 1
			for line in page.text.split('\n'):
				if line == '==Translingual==':
					b_add_lines = 0
					text_new.append(mul_text)
				elif b_add_lines == 0 and line == '----':
					b_add_lines = 1
				elif b_add_lines == 1:
					text_new.append(line)
			page.text = '\n'.join(text_new)

			print('==================')
			print(page.text)
			print('==================')

			pywikibot.showDiff(text_old, page.text)
			input('[press enter to continue]')
			page.save('/* Translingual */ rewrite')
		else:
			page.text = mul_text + page.text
			pywikibot.showDiff(text_old, page.text)
			input('[press enter to continue]')
			page.save('/* Translingual */ init')

		#input('[press enter to continue]')
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print('----')
