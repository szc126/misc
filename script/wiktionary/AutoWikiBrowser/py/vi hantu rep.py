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

headwordTemplateMap = {
	"noun": "noun",
	"verb": "verb",
	"adjective": "adj",
	"adverb": "adv",
	"proper noun": "proper noun",
}

def processFoo(match):
	headLevA = match.group(1)
	pos = match.group(2)
	headLevB = match.group(3)
	headwordTemplateName = headwordTemplateMap[pos.lower()]
	# seems to pause if a PoS is not found in the dictionary
	# which is alright

	return headLevA + pos + headLevB + '\n{{vi-' + headwordTemplateName + '|sc=Hani}}'

def main():
	filePath = sys.argv[1]
	lines = None

	with open(filePath, mode='r', encoding='utf-8') as file:
		lines = file.read()

		lines = re.sub(r'(===+)([^\n=]+)(===+)\n{{vi-hantu[^\n]+', processFoo, lines)

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