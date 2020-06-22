import re

filenames = ['hydzd-variants.txt', 'twedu-variants.txt', 'cjkvi-simplified.txt']

for filename in filenames:
	compendium = dict()

	with open(f'../{filename}', mode='r', encoding='utf-8') as file:
		for line in file:
			matches = re.search('(.+),\w+/(\w+),(.+)', line)

			if (matches) and not ('#' in line):
				orthodox, type, variant = matches.group(1), matches.group(2), matches.group(3)

				if variant.__len__() > 1:
					type += '-sp'

				try:
					compendium[type]
				except:
					compendium[type] = {} # is this really the right way to do this

				try:
					compendium[type][orthodox]
				except:
					compendium[type][orthodox] = []

				compendium[type][orthodox].append(variant)

	with open(f'out-{filename}', mode='w', encoding='utf-8') as file:
		for type in compendium:
			for char in compendium[type]:
				file.write(f'{type}\t{char}\t' + '\t'.join(compendium[type][char]) + '\n')