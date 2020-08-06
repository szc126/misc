#!/usr/bin/env python3

# use with http://level0.osmz.ru/

# for a [name] (assumed to be zh-Hant),
# change it to zh-Hans and
# add [name:zh-Hant] and [name:zh-Hans]

from opencc import OpenCC
converter = OpenCC('/usr/share/opencc/t2s.json')

with open('OSM.txt') as f:
	x = f.read()
	x = x.split('\n\n')

	for i, way_block in enumerate(x):
		if 'int_name' in way_block:
			way_block = way_block.split('\n')

			for j, item in enumerate(way_block):
				if '  name = ' in item:
					n_t = item.replace('  name = ', '')
					n_s = converter.convert(n_t)
					item = ''
					item += '\n  name = ' + n_s
					item += '\n  name:zh-Hant = ' + n_t
					item += '\n  name:zh-Hans = ' + n_s
				if '  is_in = ' in item:
					item = ''
				way_block[j] = item
			way_block = '\n'.join(way_block)
			way_block = way_block.replace('\n\n', '\n')
		x[i] = way_block
	x = '\n\n'.join(x)
	print(x)