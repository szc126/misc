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
			if le['category']  in ('night-mode-unaware-background-color', 'duplicate-ids'):
				continue

			if not str(le['location']) in le_compilation:
				# saving the relevant page fragment now.
				# if i keep just the coordinates,
				# the coords will become unusable after one round of edits.
				# that means that i have to do a `page.text.replace()`
				# relying on the fragment, which is gross, but that's how it is.
				# SAD!
				#le_compilation[str(le['location'])] = [ page.text[ le['location'][0] : le['location'][1] ] ]
				# JS `.slice()` counts by utf16!! hell!!
				# who up homily they anglo-saxon church!!!!!!!
				le_compilation[str(le['location'])] = [ page.text.encode('utf-16-le')[ le['location'][0]*2 : le['location'][1]*2 ].decode('utf-16-le') ]
			le_compilation[str(le['location'])].append(le['category'])

		for le in le_compilation.values():
			# all of this could be greatly eased by
			# proper parsing of matching brackets.
			# i will not be doing that.
			if False:
				continue
			elif le[0] == "''" or le[0] == "'':" or le[0] == "''.":
				print('Skipping: orphaned trailing italics')
#			elif "'''" + page.title()[:2] in le[0]:
#				replaced = []
#				def doer(match):
#					a = ['', match.group(1), match.group(2), match.group(3)]
#					print(a)
#					replaced.append(a[2])
#					a[3] = "'''"
#					return ''.join(a)
#
#				page.text = page.text.replace(
#					le[0],
#					re.sub(r"(''')(" + page.title()[:2] + r".+?)()(?=[,.!?;:])", doer, le[0])
#				)
#				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-bold: /' + '/ /'.join(replaced) + '/')
			elif le[0].startswith("''{{tax"):
				page.text = page.text.replace(
					le[0],
					le[0].lstrip("'")
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': remove mw-italic: taxonomic')
			elif le[0].startswith("''") and re.search(r"{{tax.+?}}''", page.text):
				page.text = re.sub(r"({{tax.+?}})(?:'')(" + re.escape(le[0].lstrip("'")) + r")", r"\1\2", page.text)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': remove mw-italic: taxonomic - backwards search')
			elif le[0].startswith("''["):
				page.text = page.text.replace(
					le[0],
					re.sub(r"(])(?:'?)([^]]*)$", r"\1＊＊\2", le[0])
				)
				# undo doubled processing of identical fragments. [[aheawan]]
				page.text = page.text.replace("＊＊＊＊", "''")
				# apos + bracket + text + apos + bracket. [[chartarius]]
				page.text = page.text.replace("'']＊＊", "]''").replace("'']]＊＊", "]]''")
				# restore
				page.text = page.text.replace("＊＊", "''")
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: link')
			elif le[0].startswith("''{"):
#				page.text = page.text.replace(
#					le[0],
#					re.sub(r"(})(?:'?)([^}]*)$", r"\1''\2", le[0])
#				)
				page.text = page.text.replace(
					le[0],
					re.sub(r"(}})", r"\1''", le[0], count = 1)
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: template')
			elif le[0].startswith("''(") and le[0].endswith(')'):
				page.text = page.text.replace(
					le[0],
					re.sub(r"(\))(?:'?)$", r"\1''", le[0])
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: parentheses')
			elif le[0].startswith("''") and le[0].endswith(')'):
				page.text = page.text.replace(
					le[0],
					re.sub(r"(?:'?)(\))$", r"''\1", le[0])
				)
				# unbreaking my text editor's syntax highlighting. "''",
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: parentheses')
			elif le[0].startswith("'' ") or le[0].startswith("'',") or le[0].startswith("'')"):
				# `"The Mysterious Ekron Goddess Revisited," Journal of The Ancient Near Eastern Society''`
				#                                         \1 \2                                         \3
				# excluding newlines is necessary. [[Audubon's shearwater]]
				page.text = re.sub(r"( )(?:'?)([^,\n]+)(" + re.escape(le[0]) + r")", r"\1''\2\3", page.text)
				# `one might say ''fekruna tal-art'' and fekruna tal-baħar'' to refer to a tortoise and turtle, respectively.`
				# TODO
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: other text with comma - backwards search')
#			elif le[0].startswith("''") and "'" in le[0].lstrip("'"):
#				page.text = page.text.replace(
#					le[0],
#					re.sub(r"(')([^']*)$", r"\1'\2", le[0])
#				)
#				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: other text')
			elif "," in le[0] and le[0].endswith(('.', '?', '!')):
				# `''The best tiramisu I've ever tasted, '''bar none'''.`
				page.text = page.text.replace(
					le[0],
					le[0] + "''"
				)
				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: other text')
#			elif "," in le[0]:
#				page.text = page.text.replace(
#					le[0],
#					re.sub(r",", r"'',", le[0], count = 1)
#				)
#				# unbreaking my text editor's syntax highlighting. "''",
#				summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: other text with comma')
			else:
				text_old_post = page.text
				page.text = page.text.replace(
					le[0] + "\n''",
					le[0] + "''"
				)
				if text_old_post != page.text:
					summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: newline')
					continue

				# `.rstrip()` `<ref>''Fjalori i Mehmet Elezit'</ref>`
				text_old_post = page.text
				page.text = page.text.replace(
					le[0],
#					le[0].rstrip("'") + "''"
					le[0] + "''"
				)
				if text_old_post != page.text:
					summary.append(', '.join(['[[Special:LintErrors/' + le_c + ']]' for le_c in le[1:]]) + ': balance mw-italic: other text')
					continue

		summary = '; '.join(summary)

		if text_old != page.text:
			print('\t' + summary)
			pywikibot.showDiff(text_old, page.text, context = 5)
			reply = input('[press enter to continue, x enter to cancel]')

			if reply == '':
				page.save(summary)
			elif reply == 'x':
				print('Skipped.')
				print(le_compilation)
		else:
			print(le_compilation)
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')