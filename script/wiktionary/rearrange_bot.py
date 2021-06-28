#!/usr/bin/env python3
import pywikibot
from pywikibot import pagegenerators
import re

site = pywikibot.Site()
gen = site.search('korean insource:/Usage notes.*\{\{(?:ko-paraintensive[ _]form[ _]of|ko-intensive[ _]form[ _]of|ko-yin[ _]form[ _]of|ko-yang[ _]form[ _]of)/')

for page in gen:
	try:
		text_old = page.text

		xxx = page.text.split('===Etymology ')
		for i, _ in enumerate(xxx):
			boxes = re.findall(
				r'(=+Usage notes=+\n)((?:{{(?:ko-paraintensive[ _]form[ _]of|ko-intensive[ _]form[ _]of|ko-yin[ _]form[ _]of|ko-yang[ _]form[ _]of)\|.+}}\s*)+)',
				xxx[i],
			)
			if len(boxes) > 0:
				xxx[i] = re.sub(
					r'((?:{{(?:ko-paraintensive[ _]form[ _]of|ko-intensive[ _]form[ _]of|ko-yin[ _]form[ _]of|ko-yang[ _]form[ _]of)\|.+}}\s*)+)',
					r'',
					xxx[i],
				)
				xxx[i] = re.sub(
					r'(=+Usage notes=+\n+$)',
					r'',
					xxx[i],
				)
				xxx[i] = re.sub(
					r'(=+Usage notes=+\n+)(\[\[Category|===)',
					r'\2',
					xxx[i],
				)
				xxx[i] = re.sub(
					r'(===+(?:Pronunciation|Etymology|Alternative forms)===+)',
					lambda x: re.sub(r'(.)', r'\1 ', x.group(0)),
					xxx[i],
				)
				xxx[i] = re.sub(
					r'(===+.+===+)',
					r'\1\n' + re.sub(r'\n+', r'\n', boxes[0][1].strip()),
					xxx[i],
					count = 1,
				)
				xxx[i] = re.sub(
					r'(= = .+)',
					lambda x: re.sub(r'(.)( )', r'\1', x.group(0)),
					xxx[i],
				)
		page.text = '===Etymology '.join(xxx)

		pywikibot.showDiff(text_old, page.text)

		print(page.text)

		if text_old != page.text:
			#reply = input('[press enter to continue, x enter to cancel]')
			reply = 'y'

			if reply == 'x':
				pass
				print('Skipped.')
			else:
				page.save('relocate Korean sound symbolism templates')
				print('Saved.')
	except Exception as e:
		print(page.text)
		print(e)
		input('[something went wrong. press enter to continue]')

	print('----')
