#!/usr/bin/env python3

import unihan

import pywikibot
from pywikibot import pagegenerators
import re

# [[Talk:相応しい]]

site = pywikibot.Site()
gen = pywikibot.User(site, 'Onionbar').contributions(total = 50)

template = '{{RQ:ja:XSD}}'
pages = []
usexes = {
	# 'usex_text': entry,
}
time_back_limit = pywikibot.Timestamp.fromISOformat('2020-02-10T00:00:00Z')

# [[User:Erutuon]]:
# would have to separately look up revid and parentid and generate a diff
# https://doc.wikimedia.org/pywikibot/master/api_ref/pywikibot.site.html#pywikibot.site.APISite.compare
# https://doc.wikimedia.org/pywikibot/master/api_ref/pywikibot.page.html#pywikibot.page.Revision
# you could use iterate through User.contributions and
#	for each revison tuple
#		retrieve a Revision object for the revision ID (the second tuple element) and
#		get a second Revision element for the parentid of the Revision
#		and then do a diff

# search diff or new page text for new usex
# record usex
# try to amend latest revision
# if not, write the usex down for manual dealing

def text_strip(text):
	text = re.replace(r'\[\[(.*?)|(,*?)\]\]', '$1', text)
	text = re.replace(r'\[\[(,*?)\]\]', '$1', text)
	text = re.replace(r'[ %\'-]', '', text)
	return text

for page, revid, timestamp, summary in gen:
	pages.append(page)

for page in pages:
	print(page.title())
	try:
		for rev in page.revisions(reverse = True, starttime = time_back_limit):
			if rev['user'] == 'Onionbar':
				print(rev)
				if rev['_parent_id'] == 0:
					pass
					# look for usexes
					# record usexes
				else:
					rev_previous = pywikibot.page.Revision(rev['_parent_id'], None, None)
					diff = site.compare(rev_previous, rev)
					# parse $diff as html
					# look for <ins> elements
					# look for usexes in the <ins> elements
					# record usexes

					# what about moved text?
			rev_previous = rev
		input()
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print('----')
