#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
gen = pagegenerators.TextIOPageGenerator(source='/tmp/pywikibot.txt', site=site)
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
			if le['category'] == 'night-mode-unaware-background-color':
				continue

			if not str(le['location']) in le_compilation:
				# saving the relevant page fragment now.
				# if i keep just the coordinates,
				# the coords will become unusable after one round of edits.
				# that means that i have to do a `page.text.replace()`
				# relying on the fragment, which is gross, but that's how it is.
				# SAD!
				le_compilation[str(le['location'])] = [ page.text[ le['location'][0] : le['location'][1] ] ]
			le_compilation[str(le['location'])].append(le['category'])

		for le in le_compilation.values():
			if False:
				continue
			elif '{{rfp|' in le[0]:
				page.text = page.text.replace(
					le[0],
					re.sub(r'({{(?:rfp)\|.+?)(}})', r'\1|inline=1\2', le[0])
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': ' + '{{rfp}} |inline=1')
			elif '{{rfap|' in le[0]:
				page.text = page.text.replace(
					le[0],
					re.sub(r'({{(?:rfap)\|.+?)(}})', r'\1|inline=1\2', le[0])
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': ' + '{{rfap}} |inline=1')
			elif '{{rfq|' in le[0] or '{{rfquote|' in le[0]:
				page.text = page.text.replace(
					le[0],
					re.sub(r'({{(?:rfq|rfquote)\|.+?)(}})', r'\1|inline=1\2', le[0])
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': ' + '{{rfquote}} |inline=1')
			elif le[0].startswith('* {{') or le[0].startswith('*{{'):
				page.text = page.text.replace(
					le[0],
					le[0].lstrip('* ')
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': ' + 'invalid list item ' + le[0])

		summary = '; '.join(summary)

		if text_old != page.text:
			print('\t' + summary)
			pywikibot.showDiff(text_old, page.text, context = 5)
			reply = input('[press enter to continue, x enter to cancel]')

			if reply == '':
				page.save(summary)
			elif reply == 'x':
				print('Skipped.')
		else:
			print(le_compilation)
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')