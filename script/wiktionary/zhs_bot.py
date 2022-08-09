#!/usr/bin/env python3

import unihan

import pywikibot
from pywikibot import pagegenerators
from pywikibot.page import Page
import re
import sys

site = pywikibot.Site()
cat = pywikibot.Category(site, 'Chinese terms with uncreated forms')
gen = site.categorymembers(cat)

zs = '濕溼裡裏群羣床牀衛衞污汙為爲偽僞炮砲秘祕麵麪喧諠嘩譁鄰隣線綫眾衆'
zss = '臺輓遊閒'

def change_to_variant(text):
	if len(re.findall('[' + zs + ']', text)) != 1:
		return False
	text = re.sub('[' + zs + ']', lambda match: zs[(z_index := zs.index(match.group(0))) + (1 if z_index % 2 == 0 else -1)], text)
	return text

for page_t in gen:
	if '{{rfv|' in page_t.text or '{{rfd|' in page_t.text:
		continue

	print(page_t.title())

	try:
		s_found = []

		zh_formss = re.findall(
			r'{{zh-forms([^}]*)}}',
			page_t.text,
		)
		for zh_forms in zh_formss:
			s_found += re.findall(
				r'\|(?:s\d*|t\d+)=([^|}]+)',
				zh_forms,
			)

		varianted = change_to_variant(page_t.title())
		print(varianted)
		if varianted and varianted != page_t.title():
			s_found += [varianted]
		print(s_found)

		for s in s_found:
			# (don't ignorantly create pages for imaginary simplified forms described with IDS.)
			if len(page_t.title()) == 1 and len(s) != 1:
				pass
			elif len(page_t.title()) == 1:
				page_s = Page(site, s)
				if not page_s.exists():
					page_s.text = unihan.newhzmul({
						'char': s,
					})
					page_s.text += '\n\n----\n\n==Chinese==\n{{zh-see|' + page_t.title() + '}}'
					page_s.save('init. {{zh-see|' + page_t.title() + '}}')
					#input('[press enter to continue]')
				else:
					print('[it already exists]')
			else:
				page_s = Page(site, s)

				# get page creator
				user = ''
				for rev in page_t.revisions(content = False):
					user = rev['user']

				if (not page_s.exists()) and (user in sys.argv[1:]):
					page_s.text += '==Chinese==\n{{zh-see|' + page_t.title() + '}}'
					page_s.save('{{zh-see|' + page_t.title() + '}}')
					#input('[press enter to continue]')
				else:
					#input('[it already exists]')
					pass
		page_t.save('null edit')
	except Exception as e:
		print(page_t.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print()
	print()
	print('＠＠＠＠')
	print()
	print()
