# [X] Enabled
# Program or script: F:\DOCS\awb uxi.py
# Arguments/Parameters: %%file%%
# Input/Output file: E:\temp.txt
# (X) Pass article text as file
#
# (see tooltip for "Pass article text as parameter")

import os
import sys
import re

def processUsex(match):
	marker = match.group(1)
	nv = match.group(2)
	delim = match.group(3)
	en = match.group(4)

	nv = re.sub(r'{{lang\|nv\|(.*?)}}', r'\1', nv)
	nv = re.sub(r'{{l\|nv\|([^}]+)\|([^}]+)}}', r'[[\1|\2]]', nv)
	nv = re.sub(r'{{l\|nv\|([^}]+)}}', r'[[\1]]', nv)
	en = re.sub(r'\'\'(.+)\'\'$', r'\1', en)

	return marker + '{{uxi|nv|' + nv + '|' + en + '}}'

def processUsex2(match):
	marker = match.group(1)
	templatehead = match.group(2)
	content = match.group(3)

	content = re.sub(r'{{lang\|nv\|(.*?)}}', r'\1', content)
	content = re.sub(r'{{l\|nv\|([^}]+)}}', r'[[\1]]', content)

	content = re.sub(r'^ *', r'', content)
	content = re.sub(r' *$', r'', content)
	content = re.sub(r' *\| *', r'|', content)
	content = re.sub(r' *= *', r'=', content)

	if 'inline' in content:
		content = re.sub(r'\|inline=1 *', r'', content)
		templatehead = '{{uxi|nv|'

	return marker + templatehead + content

def processLink(match):
	core = match.group(1)
	templateTail = match.group(2)
	en = match.group(3)

	return core + '|t=' + en + templateTail


def main():
	filePath = sys.argv[1]
	lines = None

	with open(filePath, mode='r', encoding='utf-8') as file:
		lines = file.readlines()

		for i, line in enumerate(lines):
			processed = line
			#processed = re.sub(r'(#:+\**\*?\s*)(.*?)(\s*[-—]+\s*)(.+)', processUsex, processed)
			processed = re.sub(r'(#[*: ]*)({{uxi?\|nv\|)(.+)', processUsex2, processed)
			processed = re.sub(r'(\* {{l\|nv\|[^}].*?)(}})\s*\((.*?)\)', processLink, processed)

			if line != processed:
				print("_______________________")
				print(line)
				print(processed)

			lines[i] = processed

	with open(filePath, mode='w', encoding='utf-8') as file:
		file.writelines(lines)

try:
	main()
	#input()
except Exception as e:
	print(e)
	input()


# https://stackoverflow.com/a/12597709
# https://stackoverflow.com/a/4719562