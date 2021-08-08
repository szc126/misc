#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

import subprocess

suffix = '를|을|는|은|에|의|로|으로|이|가'
replaced = []
ignore = ['consultant']

site = pywikibot.Site()
gen = site.search('insource:/\]\[\[(' + suffix + ')\]\]/')

def doer(match):
	d = match.group(1) + '🧡' + match.group(2) + match.group(3) + match.group(4)
	replaced.append(d)
	return d

for page in gen:
	print(page.title())
	if page.title() in ignore:
		continue

	try:
		replaced = []
		text_old = page.text

		# do twice: {{t|ko|[[손바닥]][[을]] [[얼굴]][[에]] [[대다]]}}
		page.text = re.sub(
			r"((?:\[\[[가-힣]+\]\]|'''[가-힣]+'''|[가-힣]+)\[\[)(" + suffix + r")(\]\])( [^\s{}]*?(?:\]\]|''')[|} .,!?]| [^\s{}]*?[} .,!?])",
			doer,
			page.text,
		)
		page.text = re.sub(
			r"((?:\[\[[가-힣]+\]\]|'''[가-힣]+'''|[가-힣]+)\[\[)(" + suffix + r")(\]\])( [^\s{}]*?(?:\]\]|''')[|} .,!?]| [^\s{}]*?[} .,!?])",
			doer,
			page.text,
		)
		summary = suffix + '：' + '◆'.join(replaced).replace("'''", "")
		print(summary.replace('🧡', '-'))

		pywikibot.showDiff(text_old, page.text)
		page.text = page.text.replace('🧡', '-') # 🧡 because the normal hyphen has extremely low visibility in the diff

		if text_old != page.text:
			reply = input('[press enter to continue, x enter to cancel]')

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save(summary.replace('🧡', '-'))
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
