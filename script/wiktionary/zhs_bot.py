#!/usr/bin/env python3

import unihan

import pywikibot
from pywikibot import pagegenerators
from pywikibot.page import Page
import re
import sys

site = pywikibot.Site()

zs = '濕溼裡裏群羣床牀衛衞污汙為爲偽僞炮砲秘祕麵麪喧諠嘩譁鄰隣線綫眾衆'
zss = '臺輓遊閒'

def change_to_variant(text):
	if len(re.findall('[' + zs + ']', text)) != 1:
		return False
	text = re.sub('[' + zs + ']', lambda match: zs[(z_index := zs.index(match.group(0))) + (1 if z_index % 2 == 0 else -1)], text)
	return text

def main():
	cat = pywikibot.Category(site, 'Chinese terms with uncreated forms')
	gen = site.categorymembers(cat)

	for page_t in gen:
		print()
		print('https://en.wiktionary.org/wiki/' + page_t.title())
		do_zh_forms(page_t)
		do_zh_see(page_t)

	cat = pywikibot.Category(site, 'Chinese redlinks/zh-see')
	gen = site.categorymembers(cat)

	for page_v in gen:
		print()
		print('https://en.wiktionary.org/wiki/' + page_v.title())
		do_zh_forms(page_v)

def do_zh_forms(page_t):
	print('[zh-forms]')
	if not '{{zh-forms' in page_t.text:
		print('[skipped: no zh-forms]')
		return
	if '{{rfv|' in page_t.text or '{{rfd|' in page_t.text:
		print('[skipped: RFV or RFD]')
		return

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
	if varianted and varianted != page_t.title():
		s_found += [varianted]
	print('[forms]', s_found, varianted)

	if len(page_t.title()) > 1:
		# who made this page?
		users = []
		for rev in page_t.revisions(content = False):
			# collapse consecutive edits
			try:
				if users[-1] != rev['user']:
					users.append(rev['user'])
			except IndexError:
				users.append(rev['user'])
		print('[users]', users[::-1], '(最舊→最新)')

	for s in s_found:
		# 字
		if len(s) == 1 and len(page_t.title()) == 1:
			page_s = Page(site, s)
			if not page_s.exists():
				page_s.text = unihan.newhzmul({
					'char': s,
				})
				page_s.text += '\n\n----\n\n==Chinese==\n{{zh-see|' + page_t.title() + '}}'
				page_s.save('+mul +zh {{zh-see|[[' + page_t.title() + ']]}}')
				#input('[press enter to continue]')
		# 詞
		elif len(s) == len(page_t.title()):
			page_s = Page(site, s)
			if (not page_s.exists()) and (users[-1] in sys.argv[1:]):
				page_s.text += '==Chinese==\n{{zh-see|' + page_t.title() + '}}'
				page_s.save('{{zh-see|[[' + page_t.title() + ']]}}')
				#input('[press enter to continue]')
		else:
			# don't create pages for imaginary simplified forms described with IDS or something
			print('[page title length mismatch]')
	page_t.save('null edit')

def do_zh_see(page_v):
	print('[zh-see]')
	if not '{{zh-see' in page_v.text:
		print('[skipped: no zh-see]')
		return
	if '{{rfv|' in page_v.text or '{{rfd|' in page_v.text:
		print('[skipped: RFV or RFD]')
		return

	t_found = []
	zh_sees = re.findall(
		r'{{zh-see\|([^}]+)}}',
		page_v.text,
	)
	for zh_see in zh_sees:
		params = zh_see.split('|')
		if len(params) == 1:
			params.append('s')
		t_found.append(params)
	print(t_found)

	for t in t_found:
		# 字
		if len(t[0]) == 1 and len(page_v.title()) == 1:
			page_t = Page(site, t[0])
			if not page_t.exists():
				page_t.text = unihan.newhzmul({
					'char': t[0],
				})
				page_t.text += '\n\n----\n\n' + '{{subst:#invoke:User:Suzukaze-c/02|newhz'
				page_t.text += '|' + t[1] + '=' + page_v.title()
				page_t.text += '}}'
				page_t.save('+mul +zh ' + '|' + t[1] + '=[[' + page_v.title() + ']]')
				#input('[press enter to continue]')
			elif page_t.exists() and not 'Chinese' in page_t.text:
				page_t.text += '\n\n----\n\n' + '{{subst:#invoke:User:Suzukaze-c/02|newhz'
				page_t.text += '|' + t[1] + '=' + page_v.title()
				page_t.text += '}}'
				page_t.save('+zh ' + '|' + t[1] + '=[[' + page_v.title() + ']]')
				#input('[press enter to continue]')
		else:
			print('[only 字 for now]')
	page_v.save('null edit')

try:
	main()
except KeyboardInterrupt:
	print('Exiting.')
