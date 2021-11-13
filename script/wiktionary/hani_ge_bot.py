#!/usr/bin/env python3

import unihan

import pywikibot
from pywikibot import pagegenerators
from pywikibot.page import Page
import re
import sys
import os

# from pywikibot.textlib
from collections import OrderedDict, namedtuple
_Section = namedtuple('_Section', ('title', 'content'))

site = pywikibot.Site()
#gen = site.search('hastemplate:"Han simp" -"glyph origin" -"japanese Han characters" -"korean han characters" -"vietnamese han characters" hastemplate:zh-see')
#gen = site.search('hastemplate:"Han etym" insource:/Han ety[lm].+==Chinese/')
gen = site.search('hastemplate:zh-see "glyph origin" "the simplified form" insource:/=Glyph origin=.+=Chinese=/')

done = set()

for page in gen:
	z = page.title()
	save_summary = ''

	if z in done:
		continue
	if len(z) != 1:
		continue

	try:
		text_old = page.text
		text_new = pywikibot.textlib.extract_sections(page.text)
		text_new_new = (text_new[0], [], text_new[2])

		section_ge = False

		for section in text_new[1]:
			if section.title == '===Etymology===' and not section_ge: # not section_ge: [[疋]]#Japanese#Etymology
				section_ge = section
			elif section.title == '===Glyph origin===' and not section_ge: # [[兪]]#Translingual#Glyph_origin
				section_ge = section
			elif section.title == '==Chinese==':
				if not section_ge:
					break

				content_new = ''
				content_new += '===Glyph origin===\n' + section_ge.content.strip()
				content_new += (not re.search(r'zh-see.+zh-see', page.text, flags = re.DOTALL) and not 'zh-forms' in page.text) and '\n\n===Definitions===' or '' # [[傮]] multiple zh-see
				content_new = ('zh-forms' in page.text) and (section.content + content_new + '\n\n') or ('\n\n' + content_new + section.content) # [[匽]] full entry

				text_new_new[1].append(
					_Section(
						section.title,
						content_new
					)
				)
			else:
				text_new_new[1].append(section)

		page.text = text_new_new[0] + ''.join(header + body for header, body in text_new_new[1]) + text_new_new[2]

		save_summary = 'move Glyph origin from /* Translingual */ to /* Chinese */'

		os.system('clear') #
		print(page.text) #

		if text_old != page.text:
			pywikibot.showDiff(text_old, page.text)
			reply = input('[press enter to continue, x enter to cancel]')

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save(save_summary)
				print('Saved.')

		done.add(z)
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print()
	print()
	print('＠＠＠＠')
	print()
	print()
