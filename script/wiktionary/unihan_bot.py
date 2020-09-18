#!/usr/bin/env python3

import unihan

import pywikibot
from pywikibot import pagegenerators
from pywikibot.page import Page
import re

site = pywikibot.Site()
gen = pywikibot.User(site, '350bot').contributions(namespaces = pywikibot.site.Namespace(0))

done = set()

for page, revid, timestamp, summary in gen:
	z = page.title()

	if z in done:
		continue
	if len(z) != 1:
		continue

	try:
		text_old = page.text

		text_new = pywikibot.textlib.extract_sections(page.text)

		text_mul = unihan.newhzmul({
			'char': z,
			'x': page.text,
		})
		text_mul = pywikibot.textlib.extract_sections(text_mul)

		text_new_new = (text_new[0], text_mul[1], text_new[2])

		if pywikibot.textlib.does_text_contain_section(page.text, 'Translingual'):
			if not 'character info' in text_new_new[0]:
				text_new_new[0] += text_mul[0]
			bool_keep = True
			for section in text_new[1]:
				if 'Translingual' in section[0]:
					bool_keep = False
				elif re.search(r'^==[^=]', section[0]):
					bool_keep = True
				if bool_keep == True:
					text_new_new[1].append(section)

			page.text = text_new_new[0] + ''.join(header + body for header, body in text_new_new[1]) + text_new_new[2]

			print('◆')
			print(page.text)
			print('◆')

			pywikibot.showDiff(text_old, page.text)
			input('[press enter to continue]')
			page.save('/* Translingual */ rewrite')
		else:
			if not 'character info' in text_new_new[0]:
				text_new_new[0] += text_mul[0]
			text_new_new[1].insert(0, text_mul[1][0])

			page.text = text_new_new[0] + ''.join(header + body for header, body in text_new_new[1]) + text_new_new[2]

			pywikibot.showDiff(text_old, page.text)
			input('[press enter to continue]')
			page.save('/* Translingual */ init')
		done.add(z)
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print('----')
