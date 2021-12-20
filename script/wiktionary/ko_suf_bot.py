#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

import subprocess

suffix = '이|를|을|는|은|에|의|으로|까지|에서|부터|께|께서|만|들|며|에는|도|가|한테|에게|로|와|과|뿐|라도|라고|이랑|랑'
suffix_other = '이다|요' # these are special-cased below. this is just for notes
replaced = []
ignore = ['consultant']

site = pywikibot.Site()
gen = site.search('insource:/\]\[\[(' + suffix + '|' + suffix_other + ')(\]\]|\|)/ -incategory:"Middle Korean lemmas"', namespaces = [0])
# currently; [[x]][[suffix]]
# TODO: '''foo'''[[suffix]]

def doer_3(match):
	d = match.group(1) + match.group(2).replace('[[', '[[🧡').replace('|', '|🧡')
	d = d.replace('🧡-', '-')
	replaced.append(d + match.group(3)) if '🧡' in d else 0
	return d

def doer_2(match):
	d = match.group(1) + match.group(2).replace('[[', '[[🧡').replace('|', '|🧡')
	d = d.replace('🧡-', '-')
	replaced.append(d) if '🧡' in d else 0
	return d

for page in gen:
	print(page.title())
	if page.title() in ignore:
		continue

	try:
		replaced = []
		text_old = page.text

		# one or more links to suffixes (perhaps already with hyphen)
		# (and perhaps with alternate link text like [[를|ᄅᆞᆯ]]),
		# preceded by
		# linked text, bold text, or pure Hangul, or {{ruby}} stuff
		# <s>(multiple to catch [[않다|않]]'''음'''[[은]] instead of '''음'''[[은]]), and</s>
		# NVM: causes rejection of [[에]] in {{ruby|[[[外國]]](외국)}}[[에]][[🧡는|🧡ᄂᆞᆫ]]
		# followed by
		# a space + a following word + final punctuation
		# NOTE: allow pipe only for links, else it also matches
		# {{uxi|ko|[[이]]
		# NOTE:
		# [[그]][[들]][[의]] [[의견]][[들]][[은]] '''일맥상통'''[[으로]] [[통하다|통했다]]
		page.text = re.sub(
			r"((?:\[\[[^\[\]]+\]\]|'''[^']+'''|{{[^{}]+}}|[가-힣ᄀ-ᇿ🧡-]+))((?:\[\[-?(?:" + suffix + r")(?:\|[^]]+)?\]\])+)(?=( (?:\[\[[^\[\]]+\]\]|'''[^']+'''|{{[^{}]+}}|[가-힣ᄀ-ᇿ🧡-]+)[| .,!?]?))",
			doer_3,
			page.text,
		)
		# sentence final
		# [[앞]][[에서]][[요]].
		# [[사람]][[이다|이에]][[요]].
		page.text = re.sub(
			r"(\[\[\S+?\]\]|'''\S+?'''|[가-힣々ᄀ-ᇿ()㐀-龥🧡-]+?)(\[\[요\]\])",
			doer_2,
			page.text,
		)
		# 이다 inflexion
		# [[국가]][[이다]].
		# [[것]][[이다|인]][[데]]
		page.text = re.sub(
			r"(\[\[\S+?\]\]|'''\S+?'''|[가-힣々ᄀ-ᇿ()㐀-龥🧡-]+?)(\[\[이다(?:\|[가-힣ᄀ-ᇿ]+)?\]\])",
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

		if text_old != page.text:
			pywikibot.showDiff(text_old, page.text)
			page.text = page.text.replace('🧡', '-') # 🧡 because the normal hyphen has extremely low visibility in the diff
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
