#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
gen = site.linter_pages(lint_categories='bogus-image-options', namespaces='')
replaced = []

for page in gen:
	print()
	print()
	print('＠＠＠＠＠')
	print()
	print()
	print(page.title())
	print(page.full_url())

	try:
		text_old = page.text
		summary = []
		le_compilation = {}

		params = {
			'action': 'query',
			'list': 'linterrors',
			'lnttitle': page.title(),
		}
		data = site.simple_request(**params).submit()

		if not 'linterrors' in data['query']:
			print('no more errors here!')
			continue

		for le in data['query']['linterrors']:
			if le['category'] != 'bogus-image-options':
				continue

			if not str(le['location']) in le_compilation:
				le_compilation[str(le['location'])] = [ page.text[ le['location'][0] : le['location'][1] ], le['params']['items'][0] ]
			le_compilation[str(le['location'])].append(le['category'])

		for le in le_compilation.values():
			if False:
				continue
			elif le[1] == 'thumb' and le[0].startswith('<gallery'):
				page.text = page.text.replace(
					le[0],
					le[0].replace('|thumb', '')
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[2:]]) + ': ' + 'thumb')
			elif le[1] == 'thumb':
				page.text = page.text.replace(
					le[0],
					le[0].replace('|thumb', '', count = 1)
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[2:]]) + ': ' + 'thumb')
			elif True:
				# le[0] - fragment
				# le[1] - flagged option

				# strict testing: make sure the invalid instruction mirrors the file name
				# so that i can set it on automatic and kick back.
				# (where did these even come from? VisualEditor?)
#				page.text = re.sub(r'(:' + re.escape(le[1]) + r'\.\w+(?:\|thumb)?)\|\s*' + re.escape(le[1]), r'\1', page.text)
#				page.text = re.sub(r'(:' + re.escape(le[1].replace('_', ' ')) + r'\.\w+(?:\|thumb)?)\|\s*' + re.escape(le[1]), r'\1', page.text)
#				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[2:]]) + ': ' + 'duplicated file name')

#				page.text = page.text.replace(
#					le[0],
#					le[0].replace('|' + le[1] + '|' + le[1], '|' + le[1])
#				)
#				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[2:]]) + ': ' + 'duplicated caption')

				page.text = page.text.replace(
					le[0],
					re.sub(r'\|+', r'|', le[0]).replace('|]]', ']]')
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[2:]]) + ': ' + 'null option')

#				page.text = page.text.replace(
#					le[1],
#					re.sub(r'(\|\d+)(ppx|ox|x)', r'\1px', le[1])
#				)
#				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[2:]]) + ': ' + 'misspelled')

				continue

		summary = '; '.join(summary)

		if text_old != page.text:
			print('\t' + summary)
			pywikibot.showDiff(text_old, page.text, context = 5)
			reply = input('[press enter to continue, x enter to cancel]')
			#reply = ''

			if reply == '':
				page.save(summary)
				print('Saved.')
			elif reply == 'x':
				print('Skipped.')
		else:
			print(le_compilation)
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')