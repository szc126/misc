#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
gen = site.search(' insource:/=Etymology=.+=Chinese=/ -intitle:/[A-Za-z0-9]/ -"foreign scripts" insource:"japanese han simp" hastemplate:"Han simp" ')

for page in gen:
	try:
		text_old = page.text

		et = re.findall(
			r'===Etymology===\n(.+?)(?====)',
			page.text,
			flags = re.S
		)
		page.text = re.sub(
			r'===Etymology===\n(.+?)(?====)',
			'',
			page.text,
			count = 1,
			flags = re.S
		)
		"""
		page.text = re.sub(
			r'==Chinese==(\n{{zh-forms.*}})?',
			lambda x: x.group(0) + "\n\n===Glyph origin===\n" + et[0].strip().replace("{{rfe|mul", "{{rfe|zh") + ("Chinese==\n{{zh-see" in page.text and "\n\n===Definitions===" or ""),
			page.text,
		)
		"""
		page.text = re.sub(
			r'==Japanese==(\n{{ja-kanji forms.*}})?',
			lambda x: x.group(0) + "\n\n===Glyph origin===\n" + et[0].strip().replace("{{rfe|mul", "{{rfe|ja"),
			page.text,
		)

		if text_old != page.text:
			pywikibot.showDiff(text_old, page.text)
			print(page.text)
			reply = input('[press enter to continue, x enter to cancel]')

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save('mul #Etymology→ja #Glyph origin')
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
