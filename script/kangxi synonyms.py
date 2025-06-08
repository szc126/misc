#!/usr/bin/env python

# data from https://github.com/7468696e6b/kangxiDictText
# https://github.com/7468696e6b/kangxiDictText/blob/master/LICENSE

import re
import json

translation = {}
with open('kangxizidian-v3f.txt', 'r') as f_in:
	with open('syn.txt', 'w') as f_out:
		for line in f_in:
			head = line[0]
			matches = re.findall(r'(\b(\w)也|\w*[亦卽又曰猶謂云](\w)也|\w*疑?同(\w)\b|\w*(?:古文|作|俗)(\w)\w*|\w*[卽](\w)字\w*|\w*(\w)[本]字\w*)', line)
			if matches:
				for match in matches:
					synonym = ''.join(match[1:])
					explanation = match[0]
					f_out.write(head + '\t' + synonym + '\t' + explanation + '\n')

					if not head in translation:
						translation[head] = []
					if not synonym in translation:
						translation[synonym] = []
					translation[head].append(synonym + ':' + head + '' + explanation)
					translation[synonym].append(head + ':' + head + '' + explanation)
with open('syn.json', 'w') as f_out:
	json.dump(translation, f_out, ensure_ascii = False, separators = (',', ':'))