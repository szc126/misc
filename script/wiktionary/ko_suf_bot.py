#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

import subprocess

suffix = '이|를|을|는|은|에|의|으로|까지|에서|부터|께|께서|만|들|며|에는|도'
suffix_other = '이다|요' # these are special-cased below. this is just for notes
replaced = []
ignore = ['consultant']

site = pywikibot.Site()
gen = site.search('insource:/\]\[\[(' + suffix + ')\]\]/', namespaces = [0])

def doer_3(match):
	d = match.group(1) + match.group(2).replace('[[', '[[🧡') + match.group(3)
	replaced.append(d)
	return d

def doer_2(match):
	d = match.group(1) + match.group(2).replace('[[', '[[🧡').replace('|', '|🧡')
	replaced.append(d)
	return d

for page in gen:
	print(page.title())
	if page.title() in ignore:
		continue

	try:
		replaced = []
		text_old = page.text

		# one or more links to suffixes,
		# preceded by
		# linked Hangul, bold Hangul, or pure Hangul, and
		# followed by
		# a space + other stuff that made sense during adjustment
		# NOTE: pipe only for links, else it also matches
		# {{uxi|ko|[[이]]
		page.text = re.sub(
			r"(\[\[[가-힣🧡|-]+\]\]|'''[가-힣🧡-]+'''|[가-힣🧡-]+)((?:\[\[(?:" + suffix + r")\]\])+)( [^\s{}]*?(?:\]\]|''')[|} .,!?]| [^\s{}]*?[} .,!?])",
			doer_3,
			page.text,
		)
		# do twice
		# [[손바닥]][[을]] [[얼굴]][[에]] [[대다]]
		page.text = re.sub(
			r"(\[\[[가-힣🧡|-]+\]\]|'''[가-힣🧡-]+'''|[가-힣🧡-]+)((?:\[\[(?:" + suffix + r")\]\])+)( [^\s{}]*?(?:\]\]|''')[|} .,!?]| [^\s{}]*?[} .,!?])",
			doer_3,
			page.text,
		)
		# sentence final
		# [[앞]][[에서]][[요]].
		# [[사람]][[이다|이에]][[요]].
		page.text = re.sub(
			r"(\[\[[가-힣🧡|-]+\]\]|'''[가-힣🧡-]+'''|[가-힣🧡-]+)(\[\[요\]\])",
			doer_2,
			page.text,
		)
		# 이다 inflexion
		# [[것]][[이다|인]][[데]]
		page.text = re.sub(
			r"(\[\[[가-힣🧡|-]+\]\]|'''[가-힣🧡-]+'''|[가-힣🧡-]+)(\[\[이다\|[가-힣]+\]\])",
			doer_2,
			page.text,
		)

		summary = '◆'.join(replaced).replace("'''", "")
		# delink non-additions.
		# cram more nonsense in the summary,
		# produce less html in the rendered summary,
		# and highlight the remaining additions
		summary = re.sub(
			r'(\[\[(?:[^\]]+\|)?([^]]+)\]\])',
			lambda match: match.group(2) if (not '🧡' in match.group(2)) else match.group(1),
			summary,
		)
		print(summary.replace('🧡', '-'))

		pywikibot.showDiff(text_old, page.text)
		page.text = page.text.replace('🧡', '-') # 🧡 because the normal hyphen has extremely low visibility in the diff

		if text_old != page.text:
			#reply = input('[press enter to continue, x enter to cancel]')
			reply = ''

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
