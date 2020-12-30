#!/usr/bin/env python3

import unihan

import pywikibot
from pywikibot import pagegenerators
from bs4 import BeautifulSoup
import re

# [[Talk:相応しい]]

# TODO:
# failed detection
# https://en.wiktionary.org/w/index.php?title=%E7%AB%8B%E3%81%A4&diff=59766890&oldid=59001774
# https://en.wiktionary.org/w/index.php?title=%E7%AB%8B%E3%81%A4&diff=60423013&oldid=60422862
# https://en.wiktionary.org/w/index.php?title=%E6%80%92%E3%82%8B&diff=59053688&oldid=55513843
#if ins:
#	if contains 'ja-usex': # change pertains to a line containing ja-usex
#		save for manual review
# failed detection
# https://en.wiktionary.org/w/index.php?title=%E7%BF%92%E3%81%86&diff=prev&oldid=59071182
# -- how?

site = pywikibot.Site()
gen = pywikibot.User(site, 'Onionbar').contributions(namespaces = pywikibot.site.Namespace(0))

quote_attrib = '{{RQ:ja:XSD}}'
pages = set()
time_back_limit = pywikibot.Timestamp.fromISOformat('2020-02-10T00:00:00Z')

def text_strip(text):
	text = re.sub(r'\[\[([^\[\]]+)\|([^\[\]]+)\]\]', r'\2', text)
	text = re.sub(r'\[\[([^\[\]]+)\]\]', r'\1', text)
	text = re.sub(r'[ %\'-]', r'', text)
	return text

def extract_usex(text):
	text = re.search(r'{\{ja-usex(?:-inline)?\|(.+)\}\}', text)
	if text:
		text = text.group(1)
		text = text_strip(text)
		text = re.search(r'^([^|}]+)', text)
		if text:
			text = text.group(1)
	return text

# get all pages
for page, revid, timestamp, summary in gen:
	pages.add(page)

# work on pages
for page in pages:
	print(page.title())

	usexes = set()
	usexes_done = set()

	try:
		for rev in page.revisions(reverse = True, starttime = time_back_limit):
			if rev['user'] == 'Onionbar':
				print(rev)
				targets_prelim = set()

				# collect added text
				if rev['_parent_id'] == 0:
					for line in str.splitlines(page.getOldVersion(oldid = rev['revid'])):
						targets_prelim.add(line)
				else:
					rev_previous = pywikibot.page.Revision(rev['_parent_id'], None, None)
					diff = site.compare(rev_previous, rev)
					#print(diff)
					diff = BeautifulSoup(diff, 'html.parser')
					for td in diff.find_all('td', class_ = 'diff-addedline'):
						# moved text doesn't matter:
						# if User:Example added it, we will encounter it eventually

						if td.find('ins'):
							for ins in td.find_all('ins'):
								targets_prelim.add(ins.string)
						else:
							targets_prelim.add(td.string)

				# search collected text for usexes
				for target in targets_prelim:
					if target:
						#print(target)
						target = extract_usex(target)
						if target:
							#print('↓')
							#print(target)
							usexes.add(target.replace('。', ''))

		# print collection of usexes
		print(usexes)

		# save page text for diff
		text_old = page.text

		# insert quote attribution
		page_lines = str.splitlines(page.text)
		for i, line in enumerate(page_lines):
			usex = extract_usex(line)
			print(usex)
			if (usex) and (usex.replace('。', '') in usexes):
				line = re.sub('(#+)(:.+)', r'\1* ' + quote_attrib + r'\n\1*\2', line)
				page_lines[i] = line
				usexes_done.add(usex.replace('。', ''))
		page.text = '\n'.join(page_lines)

		# diff and save
		pywikibot.showDiff(text_old, page.text)
		if text_old != page.text:
			reply = input('[press enter to continue, x enter to cancel]')

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save('add quote attribution')
				print('Saved.')
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	if (usexes - usexes_done):
		print('[could not add attribution]')
		print(usexes - usexes_done)
		input()

	print('----')
