# [X] Enabled
# Program or script: F:\DOCS\awb uxi.py
# Arguments/Parameters: %%file%%
# Input/Output file: E:\temp.txt
# (X) Pass article text as file
#
# (see tooltip for "Pass article text as parameter")

# https://en.wiktionary.org/w/index.php?limit=25&title=Special%3AContributions&contribs=user&target=NadandoBot&namespace=&tagfilter=&start=&end=2018-07-18

import os
import sys
import re

def processLink(match):
	all = match.group(1)
	inner = match.group(2)

	if ('=' in inner) or ('||' in inner):
		return all
	elif '[[' in inner:
		return inner
	else:
		return '[[' + inner + ']]'

def main():
	filePath = sys.argv[1]
	lines = None

	with open(filePath, mode='r', encoding='utf-8') as file:
		lines = file.readlines()

		for i, line in enumerate(lines):
			if ('English:' in line) or ('desc|en' in line) or ('desc|bor=1|en' in line):
				pass
			else:
				processed = line
				processed = re.sub(r'({{l\|en\|([^}]*?)}})', processLink, processed)

#				if line != processed:
#					print("_______________________")
#					print(line)
#					print(processed)

				lines[i] = processed

	with open(filePath, mode='w', encoding='utf-8') as file:
		file.writelines(lines)

try:
	main()
	# input()
except Exception as e:
	print(e)
	input()


# https://stackoverflow.com/a/12597709
# https://stackoverflow.com/a/4719562