#!/usr/bin/env python3
import os
import requests
import re
import sys

TEMPLATE_URL = 'https://en.wiktionary.org/w/index.php?title=Module:zh/data/dial-syn&action=raw'
TEMPLATE_LOCAL_PATH = '/tmp/zh-dial-syn-template.txt'
template_content = ''

collection = {
	'content': {},
	'other': [],
}
lines_ignore = [
	'local export = {}',
	'export.list = {',
	'}',
	'return export',
	'\t',
	'',
]

# ----

def main(page):
	if not os.path.exists(TEMPLATE_LOCAL_PATH):
		with open(TEMPLATE_LOCAL_PATH, mode = 'x', encoding = 'utf-8') as file:
			print('Downloading template...')
			template_content = requests.get(TEMPLATE_URL).content.decode('utf-8')
			file.write(template_content)
	else:
		with open(TEMPLATE_LOCAL_PATH, mode = 'r', encoding = 'utf-8') as file:
			print('Loaded template from local.')
			template_content = file.read()

	# ----

	print(page)

	lines = page.text.split('\n')

	# sort lines into content, ignore, and other
	for line in lines:
		if re.findall(r'^\t\[', line):
			_ = re.findall(r'"([^"]+)"', line)
			dial_point = _[0]
			collection['content'][dial_point] = line
		elif line in lines_ignore:
			pass
		else:
			collection['other'].append(line)

	# ----

	lines = template_content.split('\n')

	# recall line
	for i, line in enumerate(lines):
		if re.findall(r'^\t\[', line):
			_ = re.findall(r'"([^"]+)"', line)
			dial_point = _[0]
			if dial_point in collection['content']:
				lines[i] = collection['content'][dial_point]

	page.text = '\n'.join(lines)

	if len(collection['other']) > 0:
		with open('other.txt', mode = 'a', encoding = 'utf-8') as file:
			file.write('####\n')
			file.write(collection['content']['meaning'] + '\n')
			for line in collection['other']:
				file.write(line + '\n')
			file.write('####' + '\n')
		print(collection['other'])
		input()

	# TODO: record line context and try to re-insert it?

	return page

if __name__ == '__main__':
	class ObjectFoo(object):
		pass
	page = ObjectFoo()

	with open(sys.argv[1], mode = 'r', encoding = 'utf-8') as file:
		page.text = file.read()
	page = main(page)
	print(page.text)
