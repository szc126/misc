#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
gen = site.search(' intitle:/群/ hastemplate:"tracking/zh-forms/entry possibly missing a variant form" ')
zs = '濕溼裡裏群羣床牀衛衞污汚為爲偽僞炮砲秘祕麵麪喧諠嘩譁鄰隣線綫眾衆'
zss = '臺輓遊閒'

replaced = []

def doer(match):
	t2 = re.sub(r'.', doer2, page.title())
	zhf = '{{zh-forms|t2=' + t2 + match.group(1) + '}}'
	replaced.append(t2)

	return zhf

def doer2(match):
	z = match.group(0)
	try:
		if zs.index(z) % 2 == 0:
			z = zs[zs.index(z) + 1]
		elif zs.index(z) % 2 == 1:
			z = zs[zs.index(z) - 1]
	except:
		pass
	return z

bool_skip = True
for page in gen:
	"""
	if bool_skip:
		print(page.title())
		if page.title()[0] == 'ス': # start from this point in the list instead of from the top
			bool_skip = False
		else:
			continue
	"""

	if '|t2=' in page.text:
		continue

	print(page.title())
	try:
		text_old = page.text
		replaced = []

		page.text = re.sub(r'{{zh-forms(.*)}}', doer, page.text)

		if text_old != page.text:
			summary = 'add variant form: ' + ', '.join(set(replaced))
			print('\t' + summary)
			pywikibot.showDiff(text_old, page.text)
			#reply = input('[press enter to continue, x enter to cancel, langcode enter to change]')
			reply=''

			if reply == '':
				lang_code = 'next'
				page.save(summary)
				print('Saved.')
			elif reply == 'x':
				lang_code = 'next'
				print('Skipped.')
			else:
				lang_code = reply
				page.text = text_old
				print('Trying again.')
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print()
	print()
	print('＠＠＠＠')
	print()
	print()
