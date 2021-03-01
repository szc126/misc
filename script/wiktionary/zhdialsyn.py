#!/usr/bin/env python3
import os
import requests
import re
import sys

TEMPLATE_URL = 'https://en.wiktionary.org/w/index.php?title=Module:zh/data/dial-syn&action=raw'
TEMPLATE_LOCAL_PATH = '/tmp/zh-dial-syn-template.txt'

lines_ignore = [
	'local export = {}',
	'export.list = {',
	'}',
	'return export',
	'\t',
	'',
]

'''
Erutuon:
idea: temporarily collect comment lines and
associate them with the next content line with a dict
(where keys are content lines and values are lists of preceding comments), then
insert them into lines before the content lines in the "recall line" loop

in the two examples above,
the rough equivalent of `comments['export.list = {'] = ['-- th = 趿; s = 靸 (except Hainan, where s -> t; Min Dong)']`
would have to happen somehow in the "sort" loop, and then
in the "recall line" loop, `if line in comments: lines[i] = "\n".join(comments[line]) + "\n" + lines[i]`

if current line is comment,
insert into current_comments, otherwise if
current_comments is not empty,
comments[line] = current_comments and empty current_comments;
assuming nobody adds a comment on the last line for some reason
'''

# ----

def main(page):
	# collection of lines.
	# if global and this is used as a module,
	# this is not cleared on every invocation if it is global
	# and words carry over. blargh
	collection = {
		'content': {},
		'comments': [],
		'other': [],
	}

	template_content = None
	if not os.path.exists(TEMPLATE_LOCAL_PATH):
		with open(TEMPLATE_LOCAL_PATH, mode = 'x', encoding = 'utf-8') as file:
			print('Downloading template...')
			template_content = requests.get(TEMPLATE_URL).content.decode('utf-8')
			file.write(template_content)
	else:
		with open(TEMPLATE_LOCAL_PATH, mode = 'r', encoding = 'utf-8') as file:
			print('Loaded template from local.')
			template_content = file.read()

	#deprecated = ['Sabah', 'Luchuan', 'Doumen', 'Huidong']

	# ----

	# fix tabs
	page.text = re.sub(r'^ {4}', r'\t', page.text, flags = re.M)

	# load text
	lines = page.text.splitlines()

	# sort lines into content, ignore, and other
	for i, line in enumerate(lines):
		# trim whitespace, right
		line = line.rstrip()

		if re.findall(r'^\t(--)?\[', line):
			is_comment = re.search(r'^\t--"', line)[1]
			location = re.search(r'"([^"]+)"', line)[1]
			line = re.search(r' *= *(.+)$', line)[1]

			# add commas
			line = re.sub(r'(\})( *--.+|)$', r'\1,\2', line)

			collection['content'][location] = (is_comment, line)
		elif re.findall(r'^\t*--', line):
			collection['comments'].append((lines[i], lines[i], lines[i+1]))
		elif line in lines_ignore:
			pass
		else:
			collection['other'].append(line)

	# ----

	lines = template_content.splitlines()

	# recall line
	for i, line in enumerate(lines):
		if re.findall(r'^\t(--)?\[', line):
			_ = re.findall(r'"([^"]+)"', line)
			location = _[0]
			if location in collection['content']:
				lines[i] = re.sub(r'(= )(.+)$', r'\1', lines[i])
				lines[i] += collection['content'][location]

				# detect lines that were not recalled
				# such as misspelled locations
				collection['content'].pop(location)

	page.text = '\n'.join(lines)

	# deprecated locations
	# regex abuse :))
	#page.text = re.sub(r'\n\t--\["[A-Za-z]+"\]\t+= { "" },\n', r'\n', page.text)

	# print lines that were not recalled
	if len(collection['content']) > 0:
		with open('leftover.txt', mode = 'a', encoding = 'utf-8') as file:
			file.write('####\n')
			file.write(page.title() + '\n')
			for line in collection['content']:
				file.write(line + '\n')
			file.write('####' + '\n')
		print(collection['content'])
		input()

	# print comments that were not recalled
	if len(collection['comments']) > 0:
		with open('comments.txt', mode = 'a', encoding = 'utf-8') as file:
			file.write('####\n')
			file.write(page.title() + '\n')
			for line in collection['comments']:
				file.write(line + '\n')
			file.write('####' + '\n')
		print(collection['comments'])
		input()

	# print other lines
	if len(collection['other']) > 0:
		with open('other.txt', mode = 'a', encoding = 'utf-8') as file:
			file.write('####\n')
			file.write(page.title() + '\n')
			for line in collection['other']:
				file.write(line + '\n')
			file.write('####' + '\n')
		print(collection['other'])
		input()

	return page

if __name__ == '__main__':
	# dummy object
	# https://stackoverflow.com/a/2827664
	class ObjectFoo(object):
		pass
	page = ObjectFoo()
	def _():
		return 'Project:Foobar'
	page.title = _

	with open(sys.argv[1], mode = 'r', encoding = 'utf-8') as file:
		page.text = file.read()
	page = main(page)
	print(page.text)
